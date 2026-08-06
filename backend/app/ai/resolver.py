from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.models.trend import Trend
from app.models.recommendation import Recommendation
from app.models.competitor import Competitor
from app.models.notification import Notification
from app.models.calendar_event import CalendarEvent


class DataSourceResolver:
    def __init__(self, db: AsyncSession, user_id: str):
        self.db = db
        self.user_id = user_id
        self.mode = settings.APP_MODE

    async def get_trends(self) -> List[Dict]:
        if self.mode == "demo":
            return self._demo_trends()
        real = await self._get_computed_trends()
        if real:
            return real
        if self.mode == "hybrid":
            return self._demo_trends()
        return []

    async def get_recommendations(self) -> List[Dict]:
        if self.mode == "demo":
            return self._demo_recommendations()
        real = await self._get_computed_recommendations()
        if real:
            return real
        if self.mode == "hybrid":
            return self._demo_recommendations()
        return []

    async def get_competitors(self) -> List[Dict]:
        if self.mode == "demo":
            return self._demo_competitors()
        real = await self._get_computed_competitors()
        if real:
            return real
        if self.mode == "hybrid":
            return self._demo_competitors()
        return []

    async def get_notifications(self) -> List[Dict]:
        if self.mode == "demo":
            return self._demo_notifications()
        result = await self.db.execute(
            select(Notification).where(Notification.user_id == self.user_id)
        )
        return [self._notif_to_dict(n) for n in result.scalars().all()]

    async def get_calendar(self) -> List[Dict]:
        if self.mode == "demo":
            return self._demo_calendar()
        result = await self.db.execute(
            select(CalendarEvent).where(CalendarEvent.user_id == self.user_id)
        )
        return [self._cal_to_dict(e) for e in result.scalars().all()]

    async def _get_computed_trends(self) -> List[Dict]:
        result = await self.db.execute(
            select(Trend).where(Trend.user_id == self.user_id)
        )
        trends = result.scalars().all()
        return [self._trend_to_dict(t) for t in trends]

    async def _get_computed_recommendations(self) -> List[Dict]:
        result = await self.db.execute(
            select(Recommendation).where(Recommendation.user_id == self.user_id)
        )
        recs = result.scalars().all()
        return [self._rec_to_dict(r) for r in recs]

    async def _get_computed_competitors(self) -> List[Dict]:
        result = await self.db.execute(
            select(Competitor).where(Competitor.user_id == self.user_id)
        )
        comps = result.scalars().all()
        return [self._comp_to_dict(c) for c in comps]

    def _demo_trends(self) -> List[Dict]:
        return [
            {"id": "t1", "topic": "AI Content Creation Tools", "growthDays": 14, "competition": "Medium", "fit": 85, "searchVolume": "+120%", "category": "Technology", "country": "US", "direction": "up"},
            {"id": "t2", "topic": "Creator Economy Monetization", "growthDays": 7, "competition": "High", "fit": 72, "searchVolume": "+85%", "category": "Business", "country": "US", "direction": "up"},
            {"id": "t3", "topic": "Short-form Video Algorithm", "growthDays": 21, "competition": "Low", "fit": 90, "searchVolume": "+150%", "category": "Social Media", "country": "US", "direction": "up"},
            {"id": "t4", "topic": "Podcast Growth Hacking", "growthDays": 30, "competition": "Medium", "fit": 65, "searchVolume": "+60%", "category": "Media", "country": "US", "direction": "stable"},
            {"id": "t5", "topic": "YouTube SEO Strategies", "growthDays": 10, "competition": "High", "fit": 95, "searchVolume": "+220%", "category": "Marketing", "country": "US", "direction": "up"},
        ]

    def _demo_recommendations(self) -> List[Dict]:
        return [
            {"id": "r1", "topic": "AI Tools for Content Creators", "confidence": 92, "evidence": ["High search volume with low competition", "Growing 45% week-over-week"], "expectedViews": {"low": 50000, "high": 150000}, "expectedRevenue": {"low": 150, "high": 450}, "risks": ["Saturated topic in general"], "similarContent": {"title": "10 AI Tools Every Creator Needs", "views": 850000}, "publishTime": "Tuesday 7:00 PM", "category": "Technology", "potential": "high"},
            {"id": "r2", "topic": "Behind the Scenes: My Content Creation Process", "confidence": 88, "evidence": ["Authenticity-focused content performs well", "Average 2.5x engagement"], "expectedViews": {"low": 30000, "high": 80000}, "expectedRevenue": {"low": 90, "high": 240}, "risks": ["May not appeal to new viewers"], "similarContent": {"title": "A Day in My Life as a Creator", "views": 420000}, "publishTime": "Saturday 10:00 AM", "category": "Lifestyle", "potential": "medium"},
            {"id": "r3", "topic": "Revenue Breakdown: How I Make Money Online", "confidence": 85, "evidence": ["Transparency content drives high watch time", "Your audience values financial education"], "expectedViews": {"low": 40000, "high": 120000}, "expectedRevenue": {"low": 120, "high": 360}, "risks": ["Competitive space"], "similarContent": {"title": "I Made $10K in 30 Days", "views": 1200000}, "publishTime": "Wednesday 4:00 PM", "category": "Business", "potential": "high"},
        ]

    def _demo_competitors(self) -> List[Dict]:
        return [
            {"id": "c1", "name": "CreatorTech Hub", "subscribers": 285000, "growthRate": 12.5, "overlap": 78, "engagement": 4.2, "lastVideo": "AI Changed How I Create", "lastVideoViews": 125000, "trending": True},
            {"id": "c2", "name": "Digital Nomad Academy", "subscribers": 156000, "growthRate": 8.3, "overlap": 45, "engagement": 3.8, "lastVideo": "Passive Income for Creators", "lastVideoViews": 89000, "trending": False},
            {"id": "c3", "name": "Content Strategy Lab", "subscribers": 420000, "growthRate": 15.2, "overlap": 62, "engagement": 5.1, "lastVideo": "Viral Content Formula", "lastVideoViews": 340000, "trending": True},
            {"id": "c4", "name": "YouTube Growth Secrets", "subscribers": 89000, "growthRate": 22.1, "overlap": 35, "engagement": 6.2, "lastVideo": "How I Got 1M Subs", "lastVideoViews": 560000, "trending": True},
        ]

    def _demo_notifications(self) -> List[Dict]:
        return [
            {"id": "n1", "title": "Trending Opportunity", "message": "AI Content Creation is trending up 45%. Create content now to capitalize.", "type": "trend", "time": "2 hours ago", "read": False},
            {"id": "n2", "title": "Competitor Alert", "message": "CreatorTech Hub published a video with 2x your average views.", "type": "competitor", "time": "5 hours ago", "read": False},
            {"id": "n3", "title": "Revenue Milestone", "message": "You've earned $1,250 this month. Up 15% from last month!", "type": "revenue", "time": "1 day ago", "read": True},
            {"id": "n4", "title": "Optimal Upload Window", "message": "Based on your analytics, Tuesday 2PM EST is your best upload time.", "type": "suggestion", "time": "1 day ago", "read": True},
        ]

    def _demo_calendar(self) -> List[Dict]:
        return [
            {"id": "ev1", "day": "Tuesday", "time": "2:00 PM", "score": 95, "reason": "Peak audience activity + low competition window", "type": "optimal"},
            {"id": "ev2", "day": "Thursday", "time": "6:00 PM", "score": 82, "reason": "High engagement period for tech content", "type": "good"},
            {"id": "ev3", "day": "Saturday", "time": "10:00 AM", "score": 78, "reason": "Weekend browsing spike + tutorial content performs well", "type": "good"},
            {"id": "ev4", "day": "Sunday", "time": "3:00 PM", "score": 65, "reason": "Moderate traffic, lower competition", "type": "fair"},
        ]

    @staticmethod
    def _trend_to_dict(t: Trend) -> Dict:
        return {"id": t.id, "topic": t.topic, "growthDays": t.growth_days, "competition": t.competition, "fit": t.fit, "searchVolume": t.search_volume, "category": t.category, "country": t.country, "direction": t.direction}

    @staticmethod
    def _rec_to_dict(r: Recommendation) -> Dict:
        return {"id": r.id, "topic": r.topic, "confidence": r.confidence, "evidence": r.evidence, "expectedViews": {"low": r.expected_views_low, "high": r.expected_views_high}, "expectedRevenue": {"low": r.expected_revenue_low, "high": r.expected_revenue_high}, "risks": r.risks, "similarContent": {"title": r.similar_content_title, "views": r.similar_content_views}, "publishTime": r.publish_time, "category": r.category, "potential": r.potential}

    @staticmethod
    def _comp_to_dict(c: Competitor) -> Dict:
        return {"id": c.id, "name": c.name, "subscribers": c.subscriber_count, "growthRate": c.growth_rate, "overlap": c.overlap, "engagement": c.engagement_rate, "lastVideo": c.last_video_title, "lastVideoViews": c.last_video_views, "trending": c.is_trending}

    @staticmethod
    def _notif_to_dict(n: Notification) -> Dict:
        return {"id": n.id, "title": n.title, "message": n.message, "type": n.type, "time": "2 min ago" if not n.is_read else "3 hours ago", "read": n.is_read}

    @staticmethod
    def _cal_to_dict(e: CalendarEvent) -> Dict:
        return {"id": e.id, "day": e.day, "time": e.time, "score": e.score, "reason": e.reason, "type": e.type}
