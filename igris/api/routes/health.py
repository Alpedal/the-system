"""Health endpoint for the Igris API."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from igris.api.auth import require_api_token
from igris.api.state import get_orchestrator
from igris.core.orchestrator import IgrisOrchestrator


router = APIRouter(tags=["health"])


@router.get("/health")
def health(orchestrator: IgrisOrchestrator = Depends(get_orchestrator)) -> dict:
    """Return basic liveness and loop state."""
    obs = orchestrator.observe()
    return {
        "status": "ok",
        "loop_count": obs["loop_count"],
        "agents_total": obs["agents_total"],
        "pending_tasks": obs["pending_tasks"],
        "oom_risk": obs["oom_risk"]["risk"],
    }


@router.get("/health/private")
def private_health(
    _token: str = Depends(require_api_token),
    orchestrator: IgrisOrchestrator = Depends(get_orchestrator),
) -> dict:
    """Return authenticated health details."""
    obs = orchestrator.observe()
    return {"status": "ok", "observation": obs}
