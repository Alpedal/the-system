"""Shared API state and dependency factories."""

from __future__ import annotations

from pathlib import Path

from fastapi import Request

from igris.core.orchestrator import IgrisOrchestrator


def create_orchestrator(data_dir: Path | str = Path("data")) -> IgrisOrchestrator:
    """Create the orchestrator used by API routes."""
    return IgrisOrchestrator(data_dir=Path(data_dir))


def get_orchestrator(request: Request) -> IgrisOrchestrator:
    """Return the app-scoped orchestrator instance."""
    return request.app.state.orchestrator


def get_gpu_manager(request: Request):
    """Return the GPU manager from the app-scoped orchestrator."""
    return request.app.state.orchestrator.gpu
