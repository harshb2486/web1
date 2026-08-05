from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.prediction.schemas import PredictionResult, PredictionRange


class ViewPredictor:
    def predict(self, avg_views: int, trend_momentum: float, competition_level: str, niche_fit: float) -> PredictionResult:
        comp_map = {"Low": 1.15, "Medium": 1.0, "High": 0.8}
        comp_mult = comp_map.get(competition_level, 1.0)

        trend_mult = 0.8 + (trend_momentum * 0.6)
        fit_mult = 0.7 + (niche_fit / 100 * 0.6)

        base = avg_views * trend_mult * comp_mult * fit_mult
        low = base * 0.6
        high = base * 1.4

        confidence = self._calc_confidence(trend_momentum, niche_fit, competition_level)
        risk = self._calc_risk(confidence)

        explanation = (
            f"Based on your average of {avg_views:,} views, "
            f"adjusted for {competition_level.lower()} competition ({comp_mult:.2f}x), "
            f"trend momentum ({trend_momentum:.2f}), and niche fit ({int(niche_fit)}%)."
        )

        return PredictionResult(
            prediction=round(base),
            confidence=confidence,
            explanation=explanation,
            range=PredictionRange(min=round(low), max=round(high)),
            risk=risk,
        )

    def _calc_confidence(self, momentum: float, niche_fit: float, competition: str) -> float:
        base = 0.5
        base += momentum * 0.2
        base += (niche_fit / 100) * 0.2
        if competition == "Low":
            base += 0.1
        elif competition == "High":
            base -= 0.1
        return min(max(round(base, 2), 0.1), 0.95)

    def _calc_risk(self, confidence: float) -> str:
        if confidence >= 0.7:
            return "low"
        elif confidence >= 0.4:
            return "medium"
        return "high"
