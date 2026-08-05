from typing import List, Dict, Any
from app.ai.providers.base import BaseProvider


class MockNewsProvider(BaseProvider):
    async def fetch(self, params: Dict[str, Any]) -> List[Dict]:
        query = params.get("query", "AI")
        return [
            {"title": f"TechCrunch: {query} Market Expected to Reach $50B by 2028", "source": "TechCrunch", "published_at": "2026-01-20T10:00:00Z", "url": "https://techcrunch.com/example1", "snippet": f"The {query} industry continues to grow rapidly..."},
            {"title": f"The Verge: How {query} Is Reshaping Developer Workflows", "source": "The Verge", "published_at": "2026-01-21T14:00:00Z", "url": "https://theverge.com/example2", "snippet": f"Developers are adopting {query} at unprecedented rates..."},
            {"title": f"Wired: The Complete Guide to {query} in 2026", "source": "Wired", "published_at": "2026-01-22T08:00:00Z", "url": "https://wired.com/example3", "snippet": f"Everything you need to know about {query}..."},
        ]
