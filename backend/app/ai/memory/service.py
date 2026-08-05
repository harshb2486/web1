from typing import Dict, List
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.memory.repository import MemoryRepository
from app.ai.memory.schemas import (
    MemoryResponse, CreatorProfileMemory, Preferences,
    LearningHistory, SuccessfulTopic, FailedTopic, MemoryEntry,
)


class MemoryService:
    def __init__(self):
        self.repo = MemoryRepository()

    async def get_full_memory(self, user_id: str, db: AsyncSession) -> MemoryResponse:
        memories = await self.repo.get_all(user_id, db)
        profile = await self.repo.get_profile(user_id, db)

        grouped = {}
        for m in memories:
            if m.category not in grouped:
                grouped[m.category] = []
            grouped[m.category].append(MemoryEntry(
                id=m.id,
                category=m.category,
                key=m.key,
                value=m.value,
                confidence=m.confidence,
                updated_at=m.updated_at,
            ))

        creator_profile = CreatorProfileMemory(
            niche=profile.niche if profile else None,
            subscriber_count=profile.subscriber_count if profile else None,
        )

        categories = [m.key for m in grouped.get("category_performance", [])]
        publish_times = [m.key for m in grouped.get("publish_time", [])]
        topics_to_avoid = [m.key for m in grouped.get("failed_topics", [])]

        successful = [
            SuccessfulTopic(
                topic=m.key,
                score=m.value.get("score", 0),
                evidence=m.value.get("evidence", ""),
                learned_at=m.updated_at,
            )
            for m in grouped.get("successful_topics", [])
        ]
        failed = [
            FailedTopic(
                topic=m.key,
                score=m.value.get("score", 0),
                reason=m.value.get("reason", ""),
                learned_at=m.updated_at,
            )
            for m in grouped.get("failed_topics", [])
        ]

        return MemoryResponse(
            creator_profile=creator_profile,
            preferences=Preferences(
                categories=categories,
                publish_times=publish_times,
                topics_to_avoid=topics_to_avoid,
            ),
            learning_history=LearningHistory(
                successful_topics=successful,
                failed_topics=failed,
            ),
            all_memories=grouped,
        )

    async def learn(self, user_id: str, category: str, key: str, value: Dict, db: AsyncSession, confidence: float = 0.5) -> None:
        await self.repo.upsert(user_id, category, key, value, confidence, db)

    async def update_from_trends(self, user_id: str, trends: List[Dict], db: AsyncSession) -> None:
        for t in trends:
            fit = t.get("fit", 50)
            topic = t.get("topic", "")
            if fit >= 80:
                await self.repo.upsert(
                    user_id, "successful_topics", topic,
                    {"score": fit, "evidence": f"Trend fit {fit}%, volume {t.get('searchVolume', 'N/A')}"},
                    confidence=min(fit / 100, 0.95), db=db,
                )
            elif fit <= 40:
                await self.repo.upsert(
                    user_id, "failed_topics", topic,
                    {"score": fit, "reason": f"Low trend fit ({fit}%)"},
                    confidence=min((100 - fit) / 100, 0.9), db=db,
                )

    async def update_from_recommendations(self, user_id: str, recommendations: List[Dict], db: AsyncSession) -> None:
        for r in recommendations:
            category = r.get("category", "")
            confidence = r.get("confidence", 50) / 100
            if category:
                await self.repo.upsert(
                    user_id, "category_performance", category,
                    {"avg_confidence": confidence, "count": 1},
                    confidence=confidence, db=db,
                )

    async def update_from_videos(self, user_id: str, db: AsyncSession) -> None:
        videos = await self.repo.get_videos(user_id, db)
        if not videos:
            return

        total_views = sum(v.views for v in videos)
        avg_views = total_views // len(videos) if videos else 0
        avg_revenue = sum(v.revenue for v in videos) / len(videos) if videos else 0

        await self.repo.upsert(
            user_id, "channel_stats", "avg_views",
            {"value": avg_views}, confidence=0.9, db=db,
        )
        await self.repo.upsert(
            user_id, "channel_stats", "avg_revenue",
            {"value": round(avg_revenue, 2)}, confidence=0.9, db=db,
        )

    async def auto_update(self, user_id: str, trigger: str, data: Dict, db: AsyncSession) -> None:
        if trigger == "trend_analysis":
            await self.update_from_trends(user_id, data.get("trends", []), db)
        elif trigger == "recommendation_generation":
            await self.update_from_recommendations(user_id, data.get("recommendations", []), db)
        elif trigger == "pipeline_run":
            await self.update_from_videos(user_id, db)
