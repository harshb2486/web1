from typing import List, Dict
from app.ai.processors.base import BaseProcessor


class PerformanceProcessor(BaseProcessor):
    async def process(self, signals: List[Dict]) -> List[Dict]:
        for signal in signals:
            metrics = signal.get("metrics", {})
            signal["performance_percentile"] = self._calc_performance(metrics)
        return signals

    def _calc_performance(self, metrics: Dict) -> int:
        views = metrics.get("views", 0)
        if views > 1000000:
            return 95
        elif views > 500000:
            return 85
        elif views > 100000:
            return 70
        elif views > 50000:
            return 55
        elif views > 10000:
            return 40
        elif views > 1000:
            return 25
        return 10
