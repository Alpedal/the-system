"""
Ollama Proxy — FastAPI-app som proxar anrop till Ollama.

Proxar:
  POST /api/generate (med streaming)
  GET  /api/tags

Kör med:  uv run python main.py
"""

import json
import os
import sys
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse

OLLAMA_BASE = os.environ.get("OLLAMA_BASE", "http://localhost:11434")
HOST = os.environ.get("PROXY_HOST", "0.0.0.0")
PORT = int(os.environ.get("PROXY_PORT", "8080"))

client: httpx.AsyncClient | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global client
    client = httpx.AsyncClient(base_url=OLLAMA_BASE, timeout=300)
    # Ping Ollama on startup
    try:
        r = await client.get("/api/tags")
        print(f"[proxy] Ollama reachable at {OLLAMA_BASE} (status={r.status_code})", flush=True)
    except Exception as e:
        print(f"[proxy] Ollama NOT reachable at {OLLAMA_BASE}: {e}", flush=True)
        print(f"[proxy] Proxy will still start, but requests will fail until Ollama is up.", flush=True)
    yield
    await client.aclose()


app = FastAPI(title="Ollama Proxy", lifespan=lifespan)


@app.get("/")
async def root():
    return {"service": "ollama-proxy", "ollama": OLLAMA_BASE, "status": "running"}


@app.get("/api/tags")
async def proxy_tags():
    """Proxy GET /api/tags to Ollama."""
    try:
        resp = await client.get("/api/tags")
        return JSONResponse(content=resp.json(), status_code=resp.status_code)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=502)


@app.post("/api/generate")
async def proxy_generate(request: Request):
    """Proxy POST /api/generate to Ollama with streaming support.

    Accepts JSON body with the same fields as Ollama's /api/generate:
      model, prompt, stream (bool), options, etc.

    If stream=true (or default), returns a StreamingResponse that forwards
    Ollama's SSE chunks as they arrive.
    If stream=false, returns the complete JSON response.
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(content={"error": "invalid JSON body"}, status_code=400)

    is_stream = body.get("stream", True)

    # Quick connectivity check before attempting streaming
    try:
        await client.get("/api/tags")
    except Exception:
        return JSONResponse(
            content={"error": f"Ollama not reachable at {OLLAMA_BASE}"},
            status_code=502,
        )

    if not is_stream:
        # Non-streaming: just forward and return
        try:
            resp = await client.post("/api/generate", json=body)
            return JSONResponse(content=resp.json(), status_code=resp.status_code)
        except Exception as e:
            return JSONResponse(content={"error": str(e)}, status_code=502)

    # Streaming: forward chunks as they arrive
    async def _stream():
        try:
            async with client.stream("POST", "/api/generate", json=body) as resp:
                async for chunk in resp.aiter_bytes():
                    yield chunk
        except Exception as e:
            yield json.dumps({"error": str(e)}).encode()

    return StreamingResponse(
        _stream(),
        media_type="application/x-ndjson",
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT, log_level="info")
