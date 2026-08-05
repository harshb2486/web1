from app.services.ai.base import TrendService, RecommendationService, PredictionService, CompetitorService
from app.services.ai.mock import MockTrendService, MockRecommendationService, MockPredictionService, MockCompetitorService

trend_service: TrendService = MockTrendService()
recommendation_service: RecommendationService = MockRecommendationService()
prediction_service: PredictionService = MockPredictionService()
competitor_service: CompetitorService = MockCompetitorService()
