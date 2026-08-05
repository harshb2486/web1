from typing import Dict, List
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.resolver import DataSourceResolver


class ToolSelector:
    TOOLS = {
        "trends": "_fetch_trends",
        "competitors": "_fetch_competitors",
        "recommendations": "_fetch_recommendations",
        "revenue": "_fetch_revenue",
        "audience": "_fetch_audience",
        "calendar": "_fetch_calendar",
        "dashboard": "_fetch_dashboard",
    }

    async def execute(self, tools: List[str], user_id: str, db: AsyncSession) -> Dict:
        resolver = DataSourceResolver(db, user_id)
        context = {}

        for tool in tools:
            if tool in self.TOOLS:
                method = getattr(self, self.TOOLS[tool])
                context[tool] = await method(resolver)

        return context

    async def _fetch_trends(self, resolver: DataSourceResolver) -> List[Dict]:
        return await resolver.get_trends()

    async def _fetch_competitors(self, resolver: DataSourceResolver) -> List[Dict]:
        return await resolver.get_competitors()

    async def _fetch_recommendations(self, resolver: DataSourceResolver) -> List[Dict]:
        return await resolver.get_recommendations()

    async def _fetch_revenue(self, resolver: DataSourceResolver) -> Dict:
        from app.services.seed import MOCK_REVENUE_DATA
        return MOCK_REVENUE_DATA

    async def _fetch_audience(self, resolver: DataSourceResolver) -> Dict:
        from app.services.seed import MOCK_AUDIENCE_DATA
        return MOCK_AUDIENCE_DATA

    async def _fetch_calendar(self, resolver: DataSourceResolver) -> List[Dict]:
        return await resolver.get_calendar()

    async def _fetch_dashboard(self, resolver: DataSourceResolver) -> Dict:
        return {
            "totalViews": "1.2M",
            "revenue": "$3,240",
            "engagementRate": "7.8%",
            "subscribers": "284K",
        }
