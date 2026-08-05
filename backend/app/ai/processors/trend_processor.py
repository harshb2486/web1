from typing import List, Dict
from app.ai.processors.base import BaseProcessor


class TrendProcessor(BaseProcessor):
    async def process(self, signals: List[Dict]) -> List[Dict]:
        for signal in signals:
            metrics = signal.get("metrics", {})
            growth = metrics.get("growth", 0)
            signal["trend_direction"] = self._calc_direction(growth)
            signal["trend_momentum"] = self._calc_momentum(growth)
        return signals

    def _calc_direction(self, growth: float) -> str:
        if growth > 5:
            return "up"
        elif growth < -5:
            return "down"
        return "stable"

    def _calc_momentum(self, growth: float) -> float:
        return min(max(growth / 10, -1.0), 1.0)
