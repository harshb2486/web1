from app.ai.prediction.schemas import PredictionResult, PredictionRange, RevenuePrediction


class RevenuePredictor:
    def predict(self, views_low: int, views_high: int, rpm: float = 3.5) -> RevenuePrediction:
        rev_low = (views_low / 1000) * rpm * 0.7
        rev_high = (views_high / 1000) * rpm * 1.3
        rev_mid = (rev_low + rev_high) / 2

        confidence = 0.6
        risk = "medium"

        explanation = (
            f"Revenue estimated at ${rev_mid:,.0f} based on "
            f"{views_low:,}–{views_high:,} views and ${rpm:.2f} RPM."
        )

        revenue = PredictionResult(
            prediction=round(rev_mid, 2),
            confidence=confidence,
            explanation=explanation,
            range=PredictionRange(min=round(rev_low, 2), max=round(rev_high, 2)),
            risk=risk,
        )

        return RevenuePrediction(
            revenue=revenue,
            rpm_range=PredictionRange(min=rpm * 0.7, max=rpm * 1.3),
        )
