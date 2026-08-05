from app.schemas.auth import (
    SignupRequest,
    LoginRequest,
    TokenResponse,
    RefreshRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)
from app.schemas.user import UserResponse, UpdateProfileRequest
from app.schemas.recommendation import RecommendationResponse
from app.schemas.trend import TrendResponse
from app.schemas.competitor import CompetitorResponse
from app.schemas.audience import AudienceResponse
from app.schemas.revenue import RevenueResponse
from app.schemas.sponsor import SponsorResponse
from app.schemas.calendar import CalendarSlotResponse
from app.schemas.notification import NotificationResponse
from app.schemas.dashboard import DashboardStatsResponse
from app.schemas.onboarding import OnboardingRequest
