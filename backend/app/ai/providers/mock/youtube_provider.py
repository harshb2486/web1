from typing import List, Dict, Any
from app.ai.providers.base import BaseProvider


class MockYouTubeProvider(BaseProvider):
    async def fetch(self, params: Dict[str, Any]) -> List[Dict]:
        query = params.get("query", "AI")
        return [
            {"title": f"Ultimate {query} Tutorial for Beginners", "views": 245000, "likes": 12000, "comments": 890, "published_at": "2026-01-15T10:00:00Z", "duration": "PT12M30S", "channel": "TechChannel", "thumbnail_url": None},
            {"title": f"Why {query} Changes Everything in 2026", "views": 189000, "likes": 9500, "comments": 650, "published_at": "2026-01-18T14:00:00Z", "duration": "PT8M45S", "channel": "DevInsights", "thumbnail_url": None},
            {"title": f"{query} vs Alternatives - Which One Wins?", "views": 312000, "likes": 15600, "comments": 1200, "published_at": "2026-01-20T18:00:00Z", "duration": "PT15M10S", "channel": "CodeReview", "thumbnail_url": None},
            {"title": f"I Built a Startup with {query} in 24 Hours", "views": 420000, "likes": 21000, "comments": 1800, "published_at": "2026-01-22T12:00:00Z", "duration": "PT20M00S", "channel": "BuildLogs", "thumbnail_url": None},
            {"title": f"The Dark Side of {query} Nobody Talks About", "views": 156000, "likes": 7800, "comments": 920, "published_at": "2026-01-25T16:00:00Z", "duration": "PT10M20S", "channel": "TechCritique", "thumbnail_url": None},
        ]
