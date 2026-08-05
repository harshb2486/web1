from typing import List, Dict, Any
from app.ai.collectors.base import BaseCollector
from app.ai.providers.factory import ProviderFactory


class NewsCollector(BaseCollector):
    def __init__(self):
        self.provider = ProviderFactory.create_news()

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
                "source": "news",
                "signal_type": "article",
                "title": item.get("title", ""),
                "text": item.get("snippet", ""),
                "url": item.get("url", ""),
                "metrics": {},
                "metadata": {
                    "source_name": item.get("source", ""),
                    "published_at": item.get("published_at", ""),
                },
            }
            for item in raw_data
        ]
