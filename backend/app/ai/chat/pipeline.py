from typing import Dict, List
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.chat.intent_router import IntentRouter
from app.ai.chat.entity_extractor import EntityExtractor
from app.ai.chat.context_formatter import ContextFormatter
from app.ai.chat.llm_client import LLMClient
from app.ai.chat.schemas import ChatResponse
from app.ai.memory.service import MemoryService
from app.ai.engines.trend_engine import TrendEngine
from app.ai.engines.recommendation_engine import RecommendationEngine
from app.ai.features.feature_engine import FeatureEngine
from app.ai.resolver import DataSourceResolver
from app.models.profile import CreatorProfile
from app.models.video import Video
from sqlalchemy import select


class ChatPipeline:
    def __init__(self):
        self.intent_router = IntentRouter()
        self.entity_extractor = EntityExtractor()
        self.context_formatter = ContextFormatter()
        self.llm_client = LLMClient()
        self.memory_service = MemoryService()

    async def process(self, user_id: str, message: str, db: AsyncSession) -> ChatResponse:
        parsed = self.intent_router.parse(message)
        entities = self.entity_extractor.extract(message)
        intent = parsed["intent"]

        memory = await self.memory_service.get_full_memory(user_id, db)
        profile = await self._get_profile(user_id, db)
        features = await self._get_features(user_id, db)
        resolver = DataSourceResolver(db, user_id)
        trends = await resolver.get_trends()
        recommendations = await resolver.get_recommendations()
        videos = await self._get_videos(user_id, db)

        creator_ctx = self.context_formatter.format_creator_context(
            profile.__dict__ if profile else {},
            features.__dict__ if features else {},
        )
        analytics_ctx = self.context_formatter.format_analytics(
            features.__dict__ if features else {},
            [{"views": v.views} for v in videos] if videos else [],
        )
        trends_ctx = self.context_formatter.format_trends(trends)
        recs_ctx = self.context_formatter.format_recommendations(recommendations)
        memory_ctx = self.context_formatter.format_memory(memory.__dict__)

        full_context = self.context_formatter.compose_full_context(
            creator_ctx, analytics_ctx, trends_ctx, recs_ctx, memory_ctx
        )

        from app.ai.prompts.loader import PromptLoader
        loader = PromptLoader()
        prompt = loader.render(
            "chat.txt",
            creator_context=creator_ctx,
            analytics_context=analytics_ctx,
            trends_context=trends_ctx,
            recommendations_context=recs_ctx,
            memory_context=memory_ctx,
            question=message,
        )

        response_text = await self.llm_client.generate(prompt)

        sources = []
        if trends:
            sources.append("trends")
        if recommendations:
            sources.append("recommendations")
        if features:
            sources.append("analytics")
        if memory.all_memories:
            sources.append("memory")

        return ChatResponse(
            response=response_text,
            intent=intent,
            confidence=parsed["confidence"],
            sources_used=sources,
        )

    async def _get_profile(self, user_id: str, db: AsyncSession):
        result = await db.execute(select(CreatorProfile).where(CreatorProfile.user_id == user_id))
        return result.scalar_one_or_none()

    async def _get_features(self, user_id: str, db: AsyncSession):
        from app.models.feature_vector import FeatureVector
        result = await db.execute(select(FeatureVector).where(FeatureVector.user_id == user_id))
        return result.scalar_one_or_none()

    async def _get_videos(self, user_id: str, db: AsyncSession):
        result = await db.execute(select(Video).where(Video.user_id == user_id))
        return result.scalars().all()
