"""Agent status endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from igris.api.auth import require_api_token
from igris.api.state import get_orchestrator
from igris.core.orchestrator import IgrisOrchestrator


router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("")
def list_agents(
    _token: str = Depends(require_api_token),
    orchestrator: IgrisOrchestrator = Depends(get_orchestrator),
) -> list[dict]:
    """Return all tracked agents as API-safe JSON."""
    return [agent.model_dump(mode="json") for agent in orchestrator.agents.values()]


@router.get("/{agent_id}")
def get_agent(
    agent_id: str,
    _token: str = Depends(require_api_token),
    orchestrator: IgrisOrchestrator = Depends(get_orchestrator),
) -> dict:
    """Return one tracked agent."""
    from fastapi import HTTPException, status

    agent = orchestrator.agents.get(agent_id)
    if not agent:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="agent not found")
    return agent.model_dump(mode="json")
