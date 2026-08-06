import os

try:
    from celery import Celery

    redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

    celery_app = Celery("creatoros")

    celery_app.config_from_object({
        "broker_url": redis_url,
        "result_backend": redis_url,
        "task_serializer": "json",
        "result_serializer": "json",
        "accept_content": ["json"],
        "timezone": "UTC",
        "enable_utc": True,
        "task_track_started": True,
        "task_acks_late": True,
        "worker_prefetch_multiplier": 1,
        "task_routes": {
            "app.workers.*": {"queue": "ai"},
        },
    })

    celery_app.autodiscover_tasks(["app.workers"])
except Exception:
    celery_app = None
