from app.ai.providers.base import BaseProvider
from app.ai.providers.mock import MockYouTubeProvider, MockRedditProvider, MockNewsProvider, MockTrendsProvider
from app.ai.providers.live import LiveYouTubeProvider, LiveRedditProvider, LiveNewsProvider, LiveTrendsProvider
from app.core.config import settings


class HybridProvider(BaseProvider):
    def __init__(self, mock: BaseProvider, live: BaseProvider):
        self.mock = mock
        self.live = live

    async def fetch(self, params):
        try:
            if await self.live.health_check():
                return await self.live.fetch(params)
        except Exception:
            pass
        return await self.mock.fetch(params)

    async def health_check(self) -> bool:
        return True


class ProviderFactory:
    @staticmethod
    def create_youtube() -> BaseProvider:
        mode = settings.PROVIDER_MODE
        if mode == "live":
            return LiveYouTubeProvider()
        elif mode == "hybrid":
            return HybridProvider(MockYouTubeProvider(), LiveYouTubeProvider())
        return MockYouTubeProvider()

    @staticmethod
    def create_reddit() -> BaseProvider:
        mode = settings.PROVIDER_MODE
        if mode == "live":
            return LiveRedditProvider()
        elif mode == "hybrid":
            return HybridProvider(MockRedditProvider(), LiveRedditProvider())
        return MockRedditProvider()

    @staticmethod
    def create_news() -> BaseProvider:
        mode = settings.PROVIDER_MODE
        if mode == "live":
            return LiveNewsProvider()
        elif mode == "hybrid":
            return HybridProvider(MockNewsProvider(), LiveNewsProvider())
        return MockNewsProvider()

    @staticmethod
    def create_trends() -> BaseProvider:
        mode = settings.PROVIDER_MODE
        if mode == "live":
            return LiveTrendsProvider()
        elif mode == "hybrid":
            return HybridProvider(MockTrendsProvider(), LiveTrendsProvider())
        return MockTrendsProvider()
