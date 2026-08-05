from typing import List, Dict, Any
from app.ai.providers.base import BaseProvider


class MockTrendsProvider(BaseProvider):
    async def fetch(self, params: Dict[str, Any]) -> List[Dict]:
        keywords = params.get("keywords", ["AI", "React", "Python"])
        results = []
        for kw in keywords:
            results.append({
                "keyword": kw,
                "values": [
                    {"date": "2026-01-01", "value": 45},
                    {"date": "2026-01-08", "value": 52},
                    {"date": "2026-01-15", "value": 68},
                    {"date": "2026-01-22", "value": 85},
                    {"date": "2026-01-29", "value": 92},
                ],
                "geo": params.get("geo", "US"),
                "related_queries": [f"{kw} tutorial", f"{kw} 2026", f"best {kw}"],
                "related_topics": [f"Technology", f"Programming"],
            })
        return results
