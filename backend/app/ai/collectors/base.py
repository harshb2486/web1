from abc import ABC, abstractmethod
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.raw_signal import RawSignal


class BaseCollector(ABC):
    @abstractmethod
    async def collect(self, params: Dict[str, Any]) -> List[Dict]:
        ...

    @abstractmethod
    def validate(self, raw_data: Any) -> bool:
        ...

    @abstractmethod
    def normalize(self, raw_data: Any) -> List[Dict]:
        ...

    async def store(self, signals: List[Dict], user_id: str, db: AsyncSession) -> List[RawSignal]:
        stored = []
        for sig in signals:
            raw = RawSignal(
                user_id=user_id,
                source=sig.get("source", "unknown"),
                signal_type=sig.get("signal_type", "unknown"),
                title=sig.get("title", ""),
                text=sig.get("text", ""),
                url=sig.get("url", ""),
                metrics=sig.get("metrics", {}),
                metadata_=sig.get("metadata", {}),
            )
            db.add(raw)
            stored.append(raw)
        await db.flush()
        return stored
