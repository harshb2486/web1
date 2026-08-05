from app.ai.prediction.schemas import PredictionResult, PredictionRange


class CTRPredictor:
    def predict(self, base_ctr: float, trend_momentum: float, competition_level: str, thumbnail_quality: float = 0.5) -> PredictionResult:
        comp_map = {"Low": 1.1, "Medium": 1.0, "High": 0.85}
        comp_mult = comp_map.get(competition_level, 1.0)

        trend_mult = 0.9 + (trend_momentum * 0.2)
        thumb_mult = 0.8 + (thumbnail_quality * 0.4)

        ctr = base_ctr * trend_mult * comp_mult * thumb_mult
        ctr = min(max(ctr, 0.01), 0.25)

        low = max(ctr * 0.7, 0.01)
        high = min(ctr * 1.4, 0.30)

        confidence = 0.5 + (trend_momentum * 0.2) + (1.0 if competition_level == "Low" else 0.0)
        confidence = min(max(round(confidence, 2), 0.2), 0.9)
        risk = "low" if confidence >= 0.7 else "medium" if confidence >= 0.4 else "high"

        explanation = (
            f"Estimated CTR of {ctr:.1%} based on your baseline CTR of {base_ctr:.1%}, "
            f"adjusted for trend momentum and {competition_level.lower()} competition."
        )

        return PredictionResult(
            prediction=round(ctr, 4),
            confidence=confidence,
            explanation=explanation,
            range=PredictionRange(min=round(low, 4), max=round(high, 4)),
            risk=risk,
        )
