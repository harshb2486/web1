from typing import List, Dict, Any
from app.ai.providers.base import BaseProvider


class LiveTrendsProvider(BaseProvider):
    async def health_check(self) -> bool:
        return False

    async def fetch(self, params: Dict[str, Any]) -> List[Dict]:
        return []
