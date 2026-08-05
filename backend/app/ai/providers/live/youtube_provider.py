import httpx
from typing import List, Dict, Any
from app.ai.providers.base import BaseProvider
from app.core.config import settings


class LiveYouTubeProvider(BaseProvider):
    BASE_URL = "https://www.googleapis.com/youtube/v3"

    async def health_check(self) -> bool:
        return bool(settings.YOUTUBE_API_KEY)

    async def fetch(self, params: Dict[str, Any]) -> List[Dict]:
        if not settings.YOUTUBE_API_KEY:
            return []
        query = params.get("query", "")
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(
                f"{self.BASE_URL}/search",
                params={
                    "part": "snippet",
                    "q": query,
                    "type": "video",
                    "maxResults": params.get("max_results", 10),
                    "order": "viewCount",
                    "key": settings.YOUTUBE_API_KEY,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            return [
                {
                    "title": item["snippet"]["title"],
                    "views": 0,
                    "likes": 0,
                    "comments": 0,
                    "published_at": item["snippet"]["publishedAt"],
                    "duration": "",
                    "channel": item["snippet"]["channelTitle"],
                    "thumbnail_url": item["snippet"]["thumbnails"]["high"]["url"],
                    "video_id": item["id"]["videoId"],
                }
                for item in data.get("items", [])
            ]
