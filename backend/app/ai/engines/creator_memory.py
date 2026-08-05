from typing import Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.creator_memory import CreatorMemory


class CreatorMemoryStore:
    async def get_preferences(self, user_id: str, db: AsyncSession) -> Dict:
        result = await db.execute(
            select(CreatorMemory).where(CreatorMemory.user_id == user_id)
        )
        memories = result.scalars().all()
        prefs = {}
        for m in memories:
            if m.category not in prefs:
                prefs[m.category] = {}
            prefs[m.category][m.key] = {"value": m.value, "confidence": m.confidence}
        return prefs

    async def learn(self, user_id: str, category: str, key: str, value: Dict, db: AsyncSession, confidence: float = 0.5) -> None:
        result = await db.execute(
            select(CreatorMemory).where(
                CreatorMemory.user_id == user_id,
                CreatorMemory.category == category,
                CreatorMemory.key == key,
            )
        )
        existing = result.scalar_one_or_none()
        if existing:
            existing.value = value
            existing.confidence = confidence
        else:
            memory = CreatorMemory(
                user_id=user_id,
                category=category,
                key=key,
                value=value,
                confidence=confidence,
            )
            db.add(memory)
        await db.flush()

    async def get_preferred_categories(self, user_id: str, db: AsyncSession) -> List[str]:
        result = await db.execute(
            select(CreatorMemory).where(
                CreatorMemory.user_id == user_id,
                CreatorMemory.category == "category_performance",
            )
        )
        memories = result.scalars().all()
        return [m.key for m in sorted(memories, key=lambda x: x.confidence, reverse=True)]

    async def get_best_publish_times(self, user_id: str, db: AsyncSession) -> List[str]:
        result = await db.execute(
            select(CreatorMemory).where(
                CreatorMemory.user_id == user_id,
                CreatorMemory.category == "publish_time",
            )
        )
        memories = result.scalars().all()
        return [m.key for m in sorted(memories, key=lambda x: x.confidence, reverse=True)]
