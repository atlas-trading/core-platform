from __future__ import annotations

from contextlib import asynccontextmanager

from dependency_injector.wiring import inject
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from prometheus_client import CONTENT_TYPE_LATEST, CollectorRegistry, Gauge, generate_latest
from starlette.responses import Response

from app.core.config import settings
from app.core.container import AppContainer
from app.core.logging import configure_structlog
from app.routers import health, marketdata, trading
from app.security.access import enforce_dashboard_access

templates = Jinja2Templates(directory="templates")


registry = CollectorRegistry()
cpu_gauge = Gauge("server_cpu_percent", "CPU percent", registry=registry)
mem_gauge = Gauge("server_memory_percent", "Memory percent", registry=registry)


@asynccontextmanager
async def lifespan(_: FastAPI):
    """애플리케이션 라이프사이클 관리."""
    configure_structlog(debug=settings.debug)
    container = AppContainer()
    app.container = container  # type: ignore[attr-defined]
    try:
        yield
    finally:
        ...


app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)
app.include_router(health.router)
app.include_router(trading.router)
app.include_router(marketdata.router)


@app.get("/", response_class=HTMLResponse)
@inject
async def dashboard(request: Request):
    """대시보드: 서버 상태 + 간단한 투자현황 placeholder."""
    enforce_dashboard_access(request, settings)
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "env": settings.environment,
            "title": settings.app_name,
        },
    )


@app.get("/metrics")
async def metrics():
    """프로메테우스 메트릭 엔드포인트."""
    try:
        import psutil

        cpu_gauge.set(psutil.cpu_percent())
        mem_gauge.set(psutil.virtual_memory().percent)
    except Exception:
        pass
    data = generate_latest(registry)
    return Response(data, media_type=CONTENT_TYPE_LATEST)


def run() -> None:
    """uvicorn 실행 엔트리포인트."""
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="debug" if settings.debug else "info",
    )
