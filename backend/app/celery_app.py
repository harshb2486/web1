from celery import Celery
from app.core.config import settings

celery_app = Celery("creatoros")

celery_app.config_from_object({
    "broker_url": settings.REDIS_URL,
    "result_backend": settings.REDIS_URL,
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
    "beat_schedule": {
        "check-notifications": {
            "task": "app.workers.notification.check_notifications",
            "schedule": 900.0,
        },
        "cleanup-old-data": {
            "task": "app.workers.cleanup.cleanup_old_data",
            "schedule": 86400.0,
        },
    },
})

celery_app.autodiscover_tasks(["app.workers"])
