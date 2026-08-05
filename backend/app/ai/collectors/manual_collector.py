from typing import List, Dict, Any
from app.ai.collectors.base import BaseCollector


class ManualCollector(BaseCollector):
    async def collect(self, params: Dict[str, Any]) -> List[Dict]:
        text = params.get("text", "")
        source = params.get("source", "manual")
        if not text:
            return []
        return self.normalize([{"text": text, "source": source}])

    def validate(self, raw_data: Any) -> bool:
        return isinstance(raw_data, list) and len(raw_data) > 0

    def normalize(self, raw_data: Any) -> List[Dict]:
        return [
            {
                "source": item.get("source", "manual"),
                "signal_type": "manual",
                "title": item.get("text", "")[:100],
                "text": item.get("text", ""),
                "url": "",
                "metrics": {},
                "metadata": {},
            }
            for item in raw_data
        ]
