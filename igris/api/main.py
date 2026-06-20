"""FastAPI entrypoint for Commander Igris."""

from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

import httpx
from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from igris.api.middleware.rate_limit import RateLimitMiddleware


def create_app(data_dir: Path | str = Path("data"), orchestrator=None) -> FastAPI:
    """Create and configure the Igris API app."""
    from igris.api.routes import agents, gpu, health, chat
    from igris.api.state import create_orchestrator
    from igris.api.ws import router as ws_router, start_broadcast_worker, stop_broadcast_worker
    from igris.api.routes.chat import OLLAMA_BASE

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if not hasattr(app.state, "orchestrator"):
            app.state.orchestrator = orchestrator or create_orchestrator(Path(data_dir))
        
        # Set up shared AsyncClient for proxying Ollama requests
        app.state.http_client = httpx.AsyncClient(base_url=OLLAMA_BASE, timeout=300)
        
        # Start background WebSocket status broadcaster
        start_broadcast_worker(app)
        
        yield
        
        # Shutdown HTTP client
        await app.state.http_client.aclose()
        
        # Stop background WebSocket status broadcaster
        stop_broadcast_worker()

    app = FastAPI(title="Commander Igris API", version="0.1.0", lifespan=lifespan)
    if orchestrator is not None:
        app.state.orchestrator = orchestrator

    # Register middlewares
    app.add_middleware(RateLimitMiddleware)

    # Register routers
    app.include_router(health.router)
    app.include_router(agents.router)
    app.include_router(gpu.router)
    app.include_router(chat.router)
    app.include_router(ws_router)

    web_dir = Path(__file__).resolve().parents[1] / "web"
    if web_dir.exists():
        app.mount("/assets", StaticFiles(directory=web_dir), name="assets")

        @app.get("/", include_in_schema=False)
        def web_index() -> FileResponse:
            return FileResponse(web_dir / "index.html")

        @app.get("/web", include_in_schema=False)
        def web_redirect() -> RedirectResponse:
            return RedirectResponse(url="/", status_code=307)

    return app


app = create_app()
