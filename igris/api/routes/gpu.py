"""GPU telemetry endpoints."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass

from fastapi import APIRouter, Depends

from igris.api.auth import require_api_token
from igris.api.state import get_gpu_manager


router = APIRouter(prefix="/gpu", tags=["gpu"])


@router.get("")
def gpu_status(_token: str = Depends(require_api_token), gpu=Depends(get_gpu_manager)) -> dict:
    """Return current GPU telemetry and OOM recommendation."""
    snap = gpu.snapshot()
    snapshot = asdict(snap) if is_dataclass(snap) else dict(snap)
    return {
        "snapshot": snapshot,
        "oom_risk": gpu.check_oom_risk(),
        "free_budget_gb": gpu.free_budget_gb,
        "total_allocated_gb": gpu.total_allocated_gb,
    }
