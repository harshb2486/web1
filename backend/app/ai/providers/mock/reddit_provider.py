from typing import List, Dict, Any
from app.ai.providers.base import BaseProvider


class MockRedditProvider(BaseProvider):
    async def fetch(self, params: Dict[str, Any]) -> List[Dict]:
        query = params.get("query", "AI")
        return [
            {"title": f"r/programming - What do you think about {query}?", "score": 2450, "comments": 380, "subreddit": "programming", "created_utc": "2026-01-20T08:00:00Z", "url": "https://reddit.com/example1"},
            {"title": f"r/webdev - {query} changed my workflow completely", "score": 1890, "comments": 245, "subreddit": "webdev", "created_utc": "2026-01-21T12:00:00Z", "url": "https://reddit.com/example2"},
            {"title": f"r/learnprogramming - Best {query} resources for beginners?", "score": 3200, "comments": 520, "subreddit": "learnprogramming", "created_utc": "2026-01-22T15:00:00Z", "url": "https://reddit.com/example3"},
            {"title": f"r/MachineLearning - {query} breakthrough paper released", "score": 4100, "comments": 680, "subreddit": "MachineLearning", "created_utc": "2026-01-23T09:00:00Z", "url": "https://reddit.com/example4"},
        ]
