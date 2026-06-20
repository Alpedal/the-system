"""Ollama chat and generate proxy routes."""

from __future__ import annotations

import json
import logging
import yaml
from pathlib import Path
from typing import Any

import httpx
from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.responses import StreamingResponse, JSONResponse

from igris.api.auth import require_api_token
from igris.api.queue import gpu_lock

router = APIRouter(tags=["chat"])

logger = logging.getLogger("igris.api.chat")


def load_ollama_endpoint() -> str:
    """Load Ollama base URL from igris.yaml, or fall back to default."""
    config_path = Path(__file__).resolve().parents[2] / "config" / "igris.yaml"
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
                if config and "inference" in config and "ollama_endpoint" in config["inference"]:
                    return config["inference"]["ollama_endpoint"]
        except Exception as e:
            logger.warning(f"Failed to parse config file: {e}")
    return "http://localhost:11434"


OLLAMA_BASE = load_ollama_endpoint()


async def get_http_client(request: Request) -> httpx.AsyncClient:
    """Dependency to retrieve or create an HTTP client targeting Ollama."""
    if hasattr(request.app.state, "http_client"):
        return request.app.state.http_client
    # Fallback client if not managed by lifespan
    return httpx.AsyncClient(base_url=OLLAMA_BASE, timeout=300)


@router.post("/chat")
@router.post("/api/generate")
async def proxy_ollama(
    request: Request,
    _token: str = Depends(require_api_token),
    client: httpx.AsyncClient = Depends(get_http_client),
):
    """Proxy requests to Ollama with streaming and queue lock serialization.

    Queues requests using `gpu_lock` to ensure only one request uses the GPU at a time.
    """
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="invalid JSON body")

    # Map path directly
    path = request.url.path
    if path == "/chat":
        # Map generic /chat to Ollama's /api/chat
        target_path = "/api/chat"
    else:
        target_path = path

    is_stream = body.get("stream", True)

    # Check connection to Ollama before acquiring lock/streaming
    try:
        await client.get("/api/tags")
    except Exception:
        raise HTTPException(
            status_code=502,
            detail=f"Ollama not reachable at {OLLAMA_BASE}",
        )

    # Acquire the lock to serialize GPU work
    async with gpu_lock:
        if not is_stream:
            # Non-streaming
            try:
                resp = await client.post(target_path, json=body)
                return JSONResponse(content=resp.json(), status_code=resp.status_code)
            except Exception as e:
                raise HTTPException(status_code=502, detail=f"Ollama error: {e}")

        # Streaming response
        async def _stream():
            try:
                async with client.stream("POST", target_path, json=body) as resp:
                    async for chunk in resp.aiter_bytes():
                        yield chunk
            except Exception as e:
                yield json.dumps({"error": str(e)}).encode()

        return StreamingResponse(
            _stream(),
            media_type="application/x-ndjson",
        )
