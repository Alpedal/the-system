"""Tests for the Igris FastAPI control plane."""

from __future__ import annotations

from dataclasses import dataclass

from fastapi.testclient import TestClient

from igris.api.auth import DEFAULT_API_TOKEN
from igris.api.main import create_app
from igris.models.agent import Agent, AgentRank, AgentStatus


@dataclass
class FakeSnapshot:
    total_gb: float = 24.0
    used_gb: float = 12.0
    free_gb: float = 12.0
    utilization_pct: float = 42.0
    temperature_c: int = 57
    timestamp: float = 1.0


class FakeGPU:
    free_budget_gb = 1.8
    total_allocated_gb = 22.2

    def snapshot(self) -> FakeSnapshot:
        return FakeSnapshot()

    def check_oom_risk(self) -> dict:
        return {"risk": "low", "free_gb": 12.0, "action": "none"}


class FakeOrchestrator:
    def __init__(self) -> None:
        self.gpu = FakeGPU()
        self.agents = {
            "agent-python-001": Agent(
                agent_id="agent-python-001",
                name="Patch Worker",
                rank=AgentRank.B_RANK,
                status=AgentStatus.IDLE,
                tasks_completed=7,
                success_rate=0.86,
            )
        }
        self.tasks = {}
        self.loop_count = 3

    def observe(self) -> dict:
        return {
            "timestamp": "2026-06-20T00:00:00+00:00",
            "agents_total": len(self.agents),
            "agents_idle": 1,
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


def auth_headers() -> dict[str, str]:
    return {"Authorization": f"Bearer {DEFAULT_API_TOKEN}"}


def make_client() -> TestClient:
    return TestClient(create_app(orchestrator=FakeOrchestrator()))


def test_health_is_public() -> None:
    client = make_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["agents_total"] == 1


def test_agents_requires_token() -> None:
    client = make_client()
    response = client.get("/agents")
    assert response.status_code == 401


def test_agents_returns_tracked_agents() -> None:
    client = make_client()
    response = client.get("/agents", headers=auth_headers())
    assert response.status_code == 200
    assert response.json()[0]["agent_id"] == "agent-python-001"
    assert response.json()[0]["rank"] == "b_rank"


def test_get_agent_returns_404_for_unknown_agent() -> None:
    client = make_client()
    response = client.get("/agents/nope", headers=auth_headers())
    assert response.status_code == 404
    assert response.json()["detail"] == "agent not found"


def test_gpu_returns_snapshot_and_oom_risk() -> None:
    client = make_client()
    response = client.get("/gpu", headers=auth_headers())
    assert response.status_code == 200
    body = response.json()
    assert body["snapshot"]["total_gb"] == 24.0
    assert body["oom_risk"]["risk"] == "low"
    assert body["free_budget_gb"] == 1.8


def test_web_index_is_served() -> None:
    client = make_client()
    response = client.get("/")
    assert response.status_code == 200
    assert "Igris — Solo System" in response.text
