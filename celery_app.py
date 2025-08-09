from __future__ import annotations

from celery import Celery

from app.core.config import settings

celery = Celery(
    "atlas",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    task_acks_late=True,
    worker_prefetch_multiplier=1,
)


@celery.task(name="heartbeat")
def heartbeat() -> str:
    """heartbeat task"""
    return "ok"
