from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.creator_memory import CreatorMemory
from app.models.profile import CreatorProfile
from app.models.video import Video


class MemoryRepository:
    async def get_all(self, user_id: str, db: AsyncSession) -> List[CreatorMemory]:
        result = await db.execute(
            select(CreatorMemory).where(CreatorMemory.user_id == user_id)
        )
        return result.scalars().all()

    async def get_by_category(self, user_id: str, category: str, db: AsyncSession) -> List[CreatorMemory]:
        result = await db.execute(
            select(CreatorMemory).where(
                CreatorMemory.user_id == user_id,
                CreatorMemory.category == category,
            )
        )
        return result.scalars().all()

    async def get_by_key(self, user_id: str, category: str, key: str, db: AsyncSession) -> Optional[CreatorMemory]:
        result = await db.execute(
            select(CreatorMemory).where(
                CreatorMemory.user_id == user_id,
                CreatorMemory.category == category,
                CreatorMemory.key == key,
            )
        )
        return result.scalar_one_or_none()

    async def upsert(self, user_id: str, category: str, key: str, value: dict, confidence: float, db: AsyncSession) -> CreatorMemory:
        existing = await self.get_by_key(user_id, category, key, db)
        if existing:
            existing.value = value
            existing.confidence = confidence
            return existing
        memory = CreatorMemory(
            user_id=user_id,
            category=category,
            key=key,
            value=value,
            confidence=confidence,
        )
        db.add(memory)
        await db.flush()
        return memory

    async def delete(self, user_id: str, category: str, key: str, db: AsyncSession) -> None:
        existing = await self.get_by_key(user_id, category, key, db)
        if existing:
            await db.delete(existing)
            await db.flush()

    async def get_profile(self, user_id: str, db: AsyncSession) -> Optional[CreatorProfile]:
        result = await db.execute(
            select(CreatorProfile).where(CreatorProfile.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_videos(self, user_id: str, db: AsyncSession) -> List[Video]:
        result = await db.execute(
            select(Video).where(Video.user_id == user_id)
        )
        return result.scalars().all()
