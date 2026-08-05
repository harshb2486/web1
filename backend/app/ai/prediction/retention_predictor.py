from app.ai.prediction.schemas import PredictionResult, PredictionRange


class RetentionPredictor:
    def predict(self, base_retention: float, avg_watch_time: float, video_length: float, competition_level: str) -> PredictionResult:
        comp_map = {"Low": 1.05, "Medium": 1.0, "High": 0.92}
        comp_mult = comp_map.get(competition_level, 1.0)

        watch_ratio = avg_watch_time / max(video_length, 1)
        retention = base_retention * comp_mult * (0.8 + watch_ratio * 0.4)
        retention = min(max(retention, 0.1), 0.95)

        low = max(retention * 0.8, 0.1)
        high = min(retention * 1.2, 0.98)

        confidence = 0.5 + (base_retention * 0.3)
        confidence = min(max(round(confidence, 2), 0.2), 0.85)
        risk = "low" if confidence >= 0.7 else "medium" if confidence >= 0.4 else "high"

        explanation = (
            f"Estimated retention of {retention:.1%} based on your baseline {base_retention:.1%}, "
            f"average watch time of {avg_watch_time:.0f}s, and competition level."
        )

        return PredictionResult(
            prediction=round(retention, 4),
            confidence=confidence,
            explanation=explanation,
            range=PredictionRange(min=round(low, 4), max=round(high, 4)),
            risk=risk,
        )

    def predict_watch_time(self, base_watch_time: float, video_length: float) -> PredictionResult:
        low = base_watch_time * 0.7
        high = min(base_watch_time * 1.4, video_length)
        mid = (low + high) / 2

        confidence = 0.6
        risk = "medium"

        explanation = f"Estimated watch time of {mid:.0f}s based on your average of {base_watch_time:.0f}s."

        return PredictionResult(
            prediction=round(mid),
            confidence=confidence,
            explanation=explanation,
            range=PredictionRange(min=round(low), max=round(high)),
            risk=risk,
        )
