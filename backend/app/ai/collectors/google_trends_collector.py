from typing import List, Dict, Any
from app.ai.collectors.base import BaseCollector
from app.ai.providers.factory import ProviderFactory


class GoogleTrendsCollector(BaseCollector):
    def __init__(self):
        self.provider = ProviderFactory.create_trends()

    async def collect(self, params: Dict[str, Any]) -> List[Dict]:
        raw = await self.provider.fetch(params)
        if not self.validate(raw):
            return []
        return self.normalize(raw)

    def validate(self, raw_data: Any) -> bool:
        return isinstance(raw_data, list) and len(raw_data) > 0

    def normalize(self, raw_data: Any) -> List[Dict]:
        results = []
        for item in raw_data:
            keyword = item.get("keyword", "")
            values = item.get("values", [])
            if values:
                latest = values[-1].get("value", 0)
                previous = values[-2].get("value", 0) if len(values) > 1 else latest
                growth = latest - previous
                results.append({
                    "source": "google_trends",
                    "signal_type": "search",
                    "title": keyword,
                    "text": f"Trending keyword: {keyword}",
                    "url": "",
                    "metrics": {
                        "search_volume": latest,
                        "growth": growth,
                        "values": values,
                    },
                    "metadata": {
                        "geo": item.get("geo", "US"),
                        "related_queries": item.get("related_queries", []),
                        "related_topics": item.get("related_topics", []),
                    },
                })
        return results
