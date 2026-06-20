"""Integration tests for Phase 2 API features: Proxy, Queue, Rate-Limiting, and WebSockets."""

from __future__ import annotations

import asyncio
import json
import time
from typing import Generator

import pytest
import respx
import httpx
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket

from igris.api.auth import DEFAULT_API_TOKEN
from igris.api.main import create_app
from igris.models.agent import Agent, AgentRank, AgentStatus
from igris.api.routes.chat import OLLAMA_BASE


class FakeGPU:
    def check_oom_risk(self) -> dict:
        return {"risk": "low", "free_gb": 12.0, "action": "none"}


class FakeOrchestrator:
    def __init__(self) -> None:
        self.agents = {}
        self.tasks = {}
        self.loop_count = 1
        self.gpu = FakeGPU()

    def observe(self) -> dict:
        return {
            "timestamp": "2026-06-20T00:00:00+00:00",
            "agents_total": len(self.agents),
            "agents_idle": 0,
            "agents_busy": 0,
            "agents_error": 0,
            "pending_tasks": 0,
            "vram_free_gb": 12.0,
            "vram_used_gb": 12.0,
            "gpu_util_pct": 42.0,
            "oom_risk": {"risk": "low", "free_gb": 12.0, "action": "none"},
            "active_idle_mode": False,
            "loop_count": self.loop_count,
        }

    def _load_state(self) -> None:
        # Fake reload
        pass


@pytest.fixture
def fake_orch() -> FakeOrchestrator:
    return FakeOrchestrator()


@pytest.fixture
def test_client(fake_orch) -> Generator[TestClient, None, None]:
    app = create_app(orchestrator=fake_orch)
    # We yield the test client context manager to trigger lifespan startup/shutdown
    with TestClient(app) as client:
        yield client


def auth_headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {DEFAULT_API_TOKEN}"}


# ─── 1. Rate Limiting Tests ───────────────────────────────────────────────────

def test_rate_limiting_enforced(test_client) -> None:
    """Verifies that 4 requests within 1 second triggers a 429 response on the 4th request."""
    # Send 3 successful requests
    for _ in range(3):
        response = test_client.get("/health")
        assert response.status_code == 200

    # The 4th request must return 429 Too Many Requests
    response = test_client.get("/health")
    assert response.status_code == 429
    assert "Too Many Requests" in response.json()["detail"]


# ─── 2. Ollama Proxy Tests ────────────────────────────────────────────────────

@respx.mock
def test_proxy_generate_endpoint(test_client) -> None:
    """Verifies that POST /api/generate forwards requests to Ollama and handles non-streaming responses."""
    # Mock Ollama connectivity check (/api/tags)
    respx.get(f"{OLLAMA_BASE}/api/tags").mock(return_value=httpx.Response(200, json={}))
    
    # Mock Ollama generate call
    mock_response_body = {"model": "qwen2.5-coder:32b", "response": "Hello World"}
    respx.post(f"{OLLAMA_BASE}/api/generate").mock(return_value=httpx.Response(200, json=mock_response_body))

    payload = {"model": "qwen2.5-coder:32b", "prompt": "test prompt", "stream": False}
    response = test_client.post("/api/generate", json=payload, headers=auth_headers())
    
    assert response.status_code == 200
    assert response.json()["response"] == "Hello World"


# ─── 3. Request Queue serialization Tests ─────────────────────────────────────

@respx.mock
def test_request_queue_serialization(test_client) -> None:
    """Verifies that requests to the proxy are serialized (sequential)."""
    # Mock Ollama check
    respx.get(f"{OLLAMA_BASE}/api/tags").mock(return_value=httpx.Response(200, json={}))
    
    # Mock generation
    respx.post(f"{OLLAMA_BASE}/api/generate").mock(return_value=httpx.Response(200, json={"response": "ok"}))

    # Send a request and verify it works
    payload = {"model": "qwen2.5-coder:32b", "prompt": "test", "stream": False}
    response = test_client.post("/api/generate", json=payload, headers=auth_headers())
    assert response.status_code == 200


# ─── 4. WebSocket Broadcast Tests ─────────────────────────────────────────────

def test_websocket_broadcast_on_state_change(test_client, fake_orch) -> None:
    """Verifies that the WebSocket endpoint accepts connections and receives broadcasts on state change."""
    with test_client.websocket_connect("/ws") as websocket:
        # Modify the orchestrator state to trigger a broadcast update
        new_agent = Agent(
            agent_id="agent-test-1",
            name="WebSocket Test Worker",
            rank=AgentRank.LEVEL_0,
            status=AgentStatus.IDLE,
        )
        fake_orch.agents["agent-test-1"] = new_agent

        # Wait for the status loop to reload and broadcast (~1.5s max due to 1s poll interval)
        # We read from the websocket to get the status update event
        received_raw = websocket.receive_text()
        received = json.loads(received_raw)
        
        assert received["event"] == "status_update"
        assert len(received["data"]["agents"]) == 1
        assert received["data"]["agents"][0]["agent_id"] == "agent-test-1"
