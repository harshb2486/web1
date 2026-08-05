from typing import Any, Optional
from pydantic import BaseModel
from datetime import datetime, timezone


class APIResponse(BaseModel):
    success: bool = True
    data: Any = None
    meta: dict = {}


def success_response(data: Any, meta: dict = None) -> dict:
    return {
        "success": True,
        "data": data,
        "meta": meta or {
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    }


def error_response(message: str, code: str = "error") -> dict:
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message,
        },
        "meta": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    }
