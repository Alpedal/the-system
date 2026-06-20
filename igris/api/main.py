"""FastAPI entrypoint for Commander Igris."""

from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path


from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles


def create_app(data_dir: Path | str = Path("data"), orchestrator=None) -> FastAPI:
    """Create and configure the Igris API app."""
    from igris.api.routes import agents, gpu, health
    from igris.api.state import create_orchestrator

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if not hasattr(app.state, "orchestrator"):
            app.state.orchestrator = orchestrator or create_orchestrator(Path(data_dir))
        yield

    app = FastAPI(title="Commander Igris API", version="0.1.0", lifespan=lifespan)
    if orchestrator is not None:
        app.state.orchestrator = orchestrator

    app.include_router(health.router)
    app.include_router(agents.router)
    app.include_router(gpu.router)

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
