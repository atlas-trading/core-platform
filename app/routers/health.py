from __future__ import annotations

import psutil
from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live")
async def live() -> dict[str, str]:
    """liveness check."""
    return {"status": "ok"}


@router.get("/ready")
async def ready() -> dict[str, object]:
    """readiness + server health summary."""
    vm = psutil.virtual_memory()
    cpu = psutil.cpu_percent(interval=None)
    return {
        "status": "ok",
        "cpu_percent": cpu,
        "memory_percent": vm.percent,
        "memory_total": vm.total,
        "memory_available": vm.available,
    }
