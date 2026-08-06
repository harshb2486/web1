from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.ai.collectors.youtube_collector import YouTubeCollector
from app.ai.collectors.google_trends_collector import GoogleTrendsCollector
from app.ai.collectors.reddit_collector import RedditCollector
from app.ai.collectors.news_collector import NewsCollector
from app.ai.processors.keyword_processor import KeywordProcessor
from app.ai.processors.title_processor import TitleProcessor
from app.ai.processors.engagement_processor import EngagementProcessor
from app.ai.processors.performance_processor import PerformanceProcessor
from app.ai.processors.trend_processor import TrendProcessor
from app.ai.features.feature_engine import FeatureEngine
from app.ai.engines.trend_engine import TrendEngine
from app.ai.engines.competitor_engine import CompetitorEngine
from app.ai.engines.recommendation_engine import RecommendationEngine
from app.ai.engines.prediction_engine import PredictionEngine
from app.ai.notifications.detector import NotificationDetector, NotificationEmitter
from app.models.profile import CreatorProfile


class PipelineWorker:
    def __init__(self):
        self.youtube = YouTubeCollector()
        self.trends = GoogleTrendsCollector()
        self.reddit = RedditCollector()
        self.news = NewsCollector()
        self.keyword_proc = KeywordProcessor()
        self.title_proc = TitleProcessor()
        self.engagement_proc = EngagementProcessor()
        self.performance_proc = PerformanceProcessor()
        self.trend_proc = TrendProcessor()
        self.feature_engine = FeatureEngine()
        self.trend_engine = TrendEngine()
        self.competitor_engine = CompetitorEngine()
        self.recommendation_engine = RecommendationEngine()
        self.notification_detector = NotificationDetector()
        self.notification_emitter = NotificationEmitter()

    async def run_full_pipeline(self, user_id: str, db: AsyncSession, progress_callback=None) -> Dict:
        result = {}

        if progress_callback:
            await progress_callback(10)

        query = await self._get_user_query(user_id, db)
        raw_signals = await self._collect(user_id, db, query)
        result["signals_collected"] = len(raw_signals)

        if progress_callback:
            await progress_callback(30)

        processed = await self._process(raw_signals, db)
        result["signals_processed"] = len(processed)

        if progress_callback:
            await progress_callback(40)

        features = await self.feature_engine.compute_all(user_id, db)
        result["features_computed"] = True

        if progress_callback:
            await progress_callback(50)

        trends = await self.trend_engine.analyze(user_id, db)
        result["trends_found"] = len(trends)

        if progress_callback:
            await progress_callback(60)

        competitors = await self.competitor_engine.analyze(user_id, db)
        result["competitors_tracked"] = len(competitors)

        if progress_callback:
            await progress_callback(70)

        recommendations = await self.recommendation_engine.generate(user_id, db)
        result["recommendations_generated"] = len(recommendations)

        if progress_callback:
            await progress_callback(80)

        notifications = await self.notification_detector.detect(user_id, db)
        emitted = await self.notification_emitter.emit(user_id, notifications, db)
        result["notifications_created"] = len(emitted)

        if progress_callback:
            await progress_callback(100)

        return result

    async def _get_user_query(self, user_id: str, db: AsyncSession) -> str:
        result = await db.execute(select(CreatorProfile).where(CreatorProfile.user_id == user_id))
        profile = result.scalar_one_or_none()
        if profile and profile.niche:
            return profile.niche
        if profile and profile.channel_name:
            return profile.channel_name
        return "content creation"

    async def _collect(self, user_id: str, db: AsyncSession, query: str):
        signals = []
        for collector in [self.youtube, self.trends, self.reddit, self.news]:
            try:
                collected = await collector.collect({"query": query, "max_results": 5})
                stored = await collector.store(collected, user_id, db)
                signals.extend(stored)
            except Exception:
                pass
        return signals

    async def _process(self, signals, db):
        dicts = [
            {
                "id": s.id,
                "title": s.title,
                "text": s.text,
                "metrics": s.metrics,
                "source": s.source,
            }
            for s in signals
        ]
        processed = await self.keyword_proc.process(dicts)
        processed = await self.title_proc.process(processed)
        processed = await self.engagement_proc.process(processed)
        processed = await self.performance_proc.process(processed)
        processed = await self.trend_proc.process(processed)
        return processed
