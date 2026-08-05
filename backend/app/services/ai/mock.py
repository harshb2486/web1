from typing import List
from app.services.ai.base import TrendService, RecommendationService, PredictionService, CompetitorService


class MockTrendService(TrendService):
    async def get_trends(self, user_id: str) -> List[dict]:
        return [
            {"topic": "AI Agents", "growthDays": 18, "competition": "Medium", "fit": 88, "searchVolume": "+340%", "category": "Tech", "country": "Global", "direction": "up"},
            {"topic": "MCP Protocol", "growthDays": 12, "competition": "Low", "fit": 82, "searchVolume": "+520%", "category": "Tech", "country": "United States", "direction": "up"},
            {"topic": "Rust for Web Dev", "growthDays": 24, "competition": "Low", "fit": 74, "searchVolume": "+180%", "category": "Tech", "country": "Global", "direction": "up"},
            {"topic": "AI Video Generation", "growthDays": 15, "competition": "High", "fit": 79, "searchVolume": "+290%", "category": "Creative", "country": "India", "direction": "up"},
            {"topic": "No-Code SaaS", "growthDays": 21, "competition": "Medium", "fit": 71, "searchVolume": "+160%", "category": "Business", "country": "United States", "direction": "stable"},
            {"topic": "Local LLM Setup", "growthDays": 9, "competition": "Low", "fit": 85, "searchVolume": "+410%", "category": "Tech", "country": "Germany", "direction": "up"},
            {"topic": "GPT-5 Features", "growthDays": 6, "competition": "High", "fit": 90, "searchVolume": "+680%", "category": "AI", "country": "Global", "direction": "up"},
            {"topic": "TypeScript 6.0", "growthDays": 3, "competition": "Low", "fit": 86, "searchVolume": "+220%", "category": "Tech", "country": "Global", "direction": "up"},
            {"topic": "AI Coding Agents", "growthDays": 14, "competition": "Medium", "fit": 92, "searchVolume": "+390%", "category": "Tech", "country": "United States", "direction": "up"},
            {"topic": "Web Performance", "growthDays": 30, "competition": "Medium", "fit": 77, "searchVolume": "+95%", "category": "Tech", "country": "United Kingdom", "direction": "stable"},
            {"topic": "DevOps Automation", "growthDays": 20, "competition": "Low", "fit": 68, "searchVolume": "+130%", "category": "Tech", "country": "Canada", "direction": "up"},
            {"topic": "React Server Components", "growthDays": 16, "competition": "Medium", "fit": 84, "searchVolume": "+210%", "category": "Tech", "country": "Global", "direction": "up"},
        ]


class MockRecommendationService(RecommendationService):
    async def get_recommendations(self, user_id: str) -> List[dict]:
        return [
            {
                "topic": "AI Agents for Students",
                "confidence": 81,
                "evidence": [
                    "Search interest increasing for 12 consecutive days",
                    "Similar creators are not covering this specific angle yet",
                    "Your audience engages well with educational AI content",
                ],
                "expectedViews": {"low": 180000, "high": 240000},
                "expectedRevenue": {"low": 1200, "high": 1800},
                "risks": ["Competition may increase within 2 weeks as topic gains traction"],
                "similarContent": {"title": "AI Tools Every Student Needs", "views": 220000},
                "publishTime": "Tuesday 7:30 PM EST",
                "category": "Education",
                "potential": "high",
            },
            {
                "topic": "Build a SaaS in 24 Hours",
                "confidence": 76,
                "evidence": [
                    "SaaS content has 3x higher engagement than average on your channel",
                    "Similar video by Fireship got 1.2M views last month",
                    "Your tutorial format performs above channel average",
                ],
                "expectedViews": {"low": 150000, "high": 300000},
                "expectedRevenue": {"low": 1000, "high": 2200},
                "risks": ["High competition from established creators in this space"],
                "similarContent": {"title": "I Built a Startup in a Weekend", "views": 185000},
                "publishTime": "Thursday 8:00 PM EST",
                "category": "Business",
                "potential": "high",
            },
            {
                "topic": "Why Python Is Losing Developers",
                "confidence": 72,
                "evidence": [
                    "Rust and Go search volume up 45% year-over-year",
                    "Contrarian takes on your channel get 2x average comments",
                    "No major creator has covered this angle in the last 30 days",
                ],
                "expectedViews": {"low": 120000, "high": 200000},
                "expectedRevenue": {"low": 800, "high": 1500},
                "risks": ["May attract negative engagement from Python community"],
                "similarContent": {"title": "Is JavaScript Dying?", "views": 340000},
                "publishTime": "Tuesday 12:00 PM EST",
                "category": "Tech",
                "potential": "medium",
            },
            {
                "topic": "MCP Protocol Explained",
                "confidence": 85,
                "evidence": [
                    "MCP search volume up 520% in 30 days",
                    "Only 3 creators have covered this in depth",
                    "Your API/protocol content averages 1.8x your channel mean",
                ],
                "expectedViews": {"low": 200000, "high": 350000},
                "expectedRevenue": {"low": 1400, "high": 2500},
                "risks": ["Topic may be too niche for broad audience"],
                "similarContent": {"title": "REST vs GraphQL vs tRPC", "views": 290000},
                "publishTime": "Thursday 7:00 PM EST",
                "category": "Tech",
                "potential": "high",
            },
        ]


class MockPredictionService(PredictionService):
    async def predict_performance(self, user_id: str, topic: str) -> dict:
        return {"views": {"low": 100000, "high": 250000}, "revenue": {"low": 700, "high": 1800}}


class MockCompetitorService(CompetitorService):
    async def get_competitors(self, user_id: str) -> List[dict]:
        return [
            {"name": "Fireship", "subscribers": 2800000, "growthRate": 4.2, "overlap": 72, "engagement": 8.7, "lastVideo": "AI Agents in 100 Seconds", "lastVideoViews": 1800000, "trending": True},
            {"name": "Web Dev Simplified", "subscribers": 1500000, "growthRate": 2.1, "overlap": 68, "engagement": 6.4, "lastVideo": "Build a Full Stack App", "lastVideoViews": 420000, "trending": False},
            {"name": "Theo", "subscribers": 920000, "growthRate": 5.8, "overlap": 78, "engagement": 9.2, "lastVideo": "React Is Dead?", "lastVideoViews": 680000, "trending": True},
            {"name": "Jack Herrington", "subscribers": 480000, "growthRate": 3.4, "overlap": 81, "engagement": 7.8, "lastVideo": "TypeScript Tips You Need", "lastVideoViews": 245000, "trending": False},
            {"name": "ByteGrad", "subscribers": 340000, "growthRate": 6.1, "overlap": 75, "engagement": 8.9, "lastVideo": "Next.js 15 Changes Everything", "lastVideoViews": 310000, "trending": True},
            {"name": "Josh Tried Coding", "subscribers": 210000, "growthRate": 7.3, "overlap": 69, "engagement": 9.5, "lastVideo": "I Learned Rust in 30 Days", "lastVideoViews": 180000, "trending": True},
        ]
