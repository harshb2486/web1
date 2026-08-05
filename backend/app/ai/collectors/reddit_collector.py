from typing import List, Dict, Any
from app.ai.collectors.base import BaseCollector
from app.ai.providers.factory import ProviderFactory


class RedditCollector(BaseCollector):
    def __init__(self):
        self.provider = ProviderFactory.create_reddit()

    async def collect(self, params: Dict[str, Any]) -> List[Dict]:
        raw = await self.provider.fetch(params)
        if not self.validate(raw):
            return []
        return self.normalize(raw)

    def validate(self, raw_data: Any) -> bool:
        return isinstance(raw_data, list) and len(raw_data) > 0

    def normalize(self, raw_data: Any) -> List[Dict]:
        return [
            {
                "source": "reddit",
                "signal_type": "post",
                "title": item.get("title", ""),
                "text": item.get("title", ""),
                "url": item.get("url", ""),
                "metrics": {
                    "score": item.get("score", 0),
                    "comments": item.get("comments", 0),
                },
                "metadata": {
                    "subreddit": item.get("subreddit", ""),
                    "created_utc": item.get("created_utc", ""),
                },
            }
            for item in raw_data
        ]
