import httpx
from typing import List, Dict, Any
from app.ai.providers.base import BaseProvider
from app.core.config import settings


class LiveRedditProvider(BaseProvider):
    BASE_URL = "https://oauth.reddit.com"

    async def health_check(self) -> bool:
        return bool(settings.REDDIT_CLIENT_ID and settings.REDDIT_CLIENT_SECRET)

    async def _get_token(self, client: httpx.AsyncClient) -> str:
        resp = await client.post(
            "https://www.reddit.com/api/v1/access_token",
            data={"grant_type": "client_credentials"},
            auth=(settings.REDDIT_CLIENT_ID, settings.REDDIT_CLIENT_SECRET),
        )
        resp.raise_for_status()
        return resp.json()["access_token"]

    async def fetch(self, params: Dict[str, Any]) -> List[Dict]:
        if not await self.health_check():
            return []
        query = params.get("query", "")
        subreddit = params.get("subreddit", "programming")
        async with httpx.AsyncClient(timeout=10) as client:
            token = await self._get_token(client)
            resp = await client.get(
                f"{self.BASE_URL}/r/{subreddit}/search.json",
                params={"q": query, "limit": params.get("max_results", 10), "sort": "relevance"},
                headers={"Authorization": f"Bearer {token}"},
            )
            resp.raise_for_status()
            data = resp.json()
            return [
                {
                    "title": post["data"]["title"],
                    "score": post["data"]["score"],
                    "comments": post["data"]["num_comments"],
                    "subreddit": post["data"]["subreddit"],
                    "created_utc": post["data"]["created_utc"],
                    "url": f"https://reddit.com{post['data']['permalink']}",
                }
                for post in data.get("data", {}).get("children", [])
            ]
