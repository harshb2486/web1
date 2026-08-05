import httpx
from typing import List, Dict, Any
from app.ai.providers.base import BaseProvider
from app.core.config import settings


class LiveNewsProvider(BaseProvider):
    BASE_URL = "https://newsapi.org/v2"

    async def health_check(self) -> bool:
        return bool(settings.NEWS_API_KEY)

    async def fetch(self, params: Dict[str, Any]) -> List[Dict]:
        if not await self.health_check():
            return []
        query = params.get("query", "")
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(
                f"{self.BASE_URL}/everything",
                params={
                    "q": query,
                    "pageSize": params.get("max_results", 10),
                    "sortBy": "relevancy",
                    "apiKey": settings.NEWS_API_KEY,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            return [
                {
                    "title": article["title"],
                    "source": article["source"]["name"],
                    "published_at": article["publishedAt"],
                    "url": article["url"],
                    "snippet": article.get("description", ""),
                }
                for article in data.get("articles", [])
            ]
