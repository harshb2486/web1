from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.recommendations import router as recommendations_router
from app.api.v1.trends import router as trends_router
from app.api.v1.competitors import router as competitors_router
from app.api.v1.audience import router as audience_router
from app.api.v1.revenue import router as revenue_router
from app.api.v1.sponsors import router as sponsors_router
from app.api.v1.calendar import router as calendar_router
from app.api.v1.notifications import router as notifications_router
from app.api.v1.onboarding import router as onboarding_router
from app.api.v1.ai import router as ai_router
from app.api.v1.chat import router as chat_router
from app.api.v1.predictions import router as predictions_router
from app.api.v1.opportunities import router as opportunities_router
from app.api.v1.analyze import router as analyze_router
from app.api.v1.generate_plan import router as generate_plan_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(dashboard_router)
api_router.include_router(recommendations_router)
api_router.include_router(trends_router)
api_router.include_router(competitors_router)
api_router.include_router(audience_router)
api_router.include_router(revenue_router)
api_router.include_router(sponsors_router)
api_router.include_router(calendar_router)
api_router.include_router(notifications_router)
api_router.include_router(onboarding_router)
api_router.include_router(ai_router)
api_router.include_router(chat_router)
api_router.include_router(predictions_router)
api_router.include_router(opportunities_router)
api_router.include_router(analyze_router)
api_router.include_router(generate_plan_router)
