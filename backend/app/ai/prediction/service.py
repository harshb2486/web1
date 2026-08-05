from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.prediction.repository import PredictionRepository
from app.ai.prediction.view_predictor import ViewPredictor
from app.ai.prediction.ctr_predictor import CTRPredictor
from app.ai.prediction.revenue_predictor import RevenuePredictor
from app.ai.prediction.retention_predictor import RetentionPredictor
from app.ai.prediction.schemas import ViewPrediction, RevenuePrediction, RetentionPrediction, SimulateResponse


class PredictionService:
    def __init__(self):
        self.repo = PredictionRepository()
        self.view_pred = ViewPredictor()
        self.ctr_pred = CTRPredictor()
        self.revenue_pred = RevenuePredictor()
        self.retention_pred = RetentionPredictor()

    async def predict_video(self, topic: str, trend_data: Dict, user_id: str, db: AsyncSession) -> ViewPrediction:
        videos = await self.repo.get_videos(user_id, db)
        features = await self.repo.get_features(user_id, db)
        profile = await self.repo.get_profile(user_id, db)

        avg_views = self.repo.calc_avg_views(videos)
        momentum = trend_data.get("raw_momentum", 0.5)
        competition = trend_data.get("competition", "Medium")
        fit = trend_data.get("fit", 50)

        base_ctr = features.ctr if features else 0.065
        base_retention = features.retention_rate if features else 0.45
        base_watch_time = features.avg_watch_time if features else 384

        views = self.view_pred.predict(avg_views, momentum, competition, fit)
        ctr = self.ctr_pred.predict(base_ctr, momentum, competition)
        retention = self.retention_pred.predict(base_retention, base_watch_time, 600, competition)

        return ViewPrediction(views=views, ctr=ctr, retention=retention)

    async def predict_revenue(self, views_low: int, views_high: int, user_id: str, db: AsyncSession) -> RevenuePrediction:
        videos = await self.repo.get_videos(user_id, db)
        rpm = self.repo.calc_avg_revenue(videos)
        return self.revenue_pred.predict(views_low, views_high, rpm)

    async def simulate(self, topic: str, user_id: str, db: AsyncSession) -> SimulateResponse:
        trend_data = {"raw_momentum": 0.7, "competition": "Medium", "fit": 70}
        view_pred = await self.predict_video(topic, trend_data, user_id, db)
        rev_pred = await self.predict_revenue(
            view_pred.views.range.min, view_pred.views.range.max, user_id, db
        )
        return SimulateResponse(
            topic=topic,
            views=view_pred.views,
            ctr=view_pred.ctr,
            retention=view_pred.retention,
            revenue=rev_pred,
        )
