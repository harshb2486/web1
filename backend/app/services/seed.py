from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.recommendation import Recommendation
from app.models.trend import Trend
from app.models.competitor import Competitor
from app.models.notification import Notification
from app.models.calendar_event import CalendarEvent


MOCK_AUDIENCE_DATA = {
    "age": [
        {"range": "13-17", "percent": 8},
        {"range": "18-24", "percent": 42},
        {"range": "25-34", "percent": 35},
        {"range": "35-44", "percent": 11},
        {"range": "45+", "percent": 4},
    ],
    "countries": [
        {"name": "India", "percent": 38},
        {"name": "United States", "percent": 22},
        {"name": "United Kingdom", "percent": 12},
        {"name": "Germany", "percent": 8},
        {"name": "Canada", "percent": 6},
        {"name": "Others", "percent": 14},
    ],
    "devices": [
        {"name": "Mobile", "percent": 58},
        {"name": "Desktop", "percent": 38},
        {"name": "Tablet", "percent": 4},
    ],
    "returningViewers": 67,
    "avgWatchTime": "6.4 min",
    "peakHours": ["7 PM", "9 PM", "12 PM"],
    "insight": "Your 18-24 audience grows 3x faster than other age groups. Educational AI content performs best with this segment.",
}

MOCK_REVENUE_DATA = {
    "current": 3240,
    "breakdown": {"ads": 1944, "sponsorships": 972, "affiliate": 194, "membership": 130},
    "monthly": [
        {"month": "Jan", "revenue": 2800, "ads": 1680, "sponsors": 840},
        {"month": "Feb", "revenue": 2950, "ads": 1770, "sponsors": 885},
        {"month": "Mar", "revenue": 3100, "ads": 1860, "sponsors": 930},
        {"month": "Apr", "revenue": 3240, "ads": 1944, "sponsors": 972},
    ],
    "chartData": [
        {"month": "May", "revenue": 2100},
        {"month": "Jun", "revenue": 2400},
        {"month": "Jul", "revenue": 2200},
        {"month": "Aug", "revenue": 2800},
        {"month": "Sep", "revenue": 2600},
        {"month": "Oct", "revenue": 2950},
        {"month": "Nov", "revenue": 3100},
        {"month": "Dec", "revenue": 3000},
        {"month": "Jan", "revenue": 2800},
        {"month": "Feb", "revenue": 2950},
        {"month": "Mar", "revenue": 3100},
        {"month": "Apr", "revenue": 3240},
    ],
}

MOCK_SPONSORS = [
    {"name": "Notion", "category": "Productivity", "fit": 94, "estimatedPrice": "$2,500", "responseProb": 78, "status": "proposal"},
    {"name": "Vercel", "category": "Developer Tools", "fit": 91, "estimatedPrice": "$3,200", "responseProb": 82, "status": "contacted"},
    {"name": "Linear", "category": "Project Management", "fit": 87, "estimatedPrice": "$1,800", "responseProb": 71, "status": "lead"},
    {"name": "Supabase", "category": "Backend", "fit": 89, "estimatedPrice": "$2,800", "responseProb": 75, "status": "contract"},
    {"name": "Raycast", "category": "Productivity", "fit": 86, "estimatedPrice": "$1,500", "responseProb": 73, "status": "paid"},
]


async def seed_user_data(db: AsyncSession, user_id: str) -> None:
    existing = await db.execute(select(Recommendation).where(Recommendation.user_id == user_id))
    if existing.first():
        return

    recommendations = [
        Recommendation(user_id=user_id, topic="AI Agents for Students", confidence=81, evidence=["Search interest increasing for 12 consecutive days", "Similar creators are not covering this specific angle yet", "Your audience engages well with educational AI content"], expected_views_low=180000, expected_views_high=240000, expected_revenue_low=1200, expected_revenue_high=1800, risks=["Competition may increase within 2 weeks as topic gains traction"], similar_content_title="AI Tools Every Student Needs", similar_content_views=220000, publish_time="Tuesday 7:30 PM EST", category="Education", potential="high"),
        Recommendation(user_id=user_id, topic="Build a SaaS in 24 Hours", confidence=76, evidence=["SaaS content has 3x higher engagement than average on your channel", "Similar video by Fireship got 1.2M views last month", "Your tutorial format performs above channel average"], expected_views_low=150000, expected_views_high=300000, expected_revenue_low=1000, expected_revenue_high=2200, risks=["High competition from established creators in this space"], similar_content_title="I Built a Startup in a Weekend", similar_content_views=185000, publish_time="Thursday 8:00 PM EST", category="Business", potential="high"),
        Recommendation(user_id=user_id, topic="Why Python Is Losing Developers", confidence=72, evidence=["Rust and Go search volume up 45% year-over-year", "Contrarian takes on your channel get 2x average comments", "No major creator has covered this angle in the last 30 days"], expected_views_low=120000, expected_views_high=200000, expected_revenue_low=800, expected_revenue_high=1500, risks=["May attract negative engagement from Python community"], similar_content_title="Is JavaScript Dying?", similar_content_views=340000, publish_time="Tuesday 12:00 PM EST", category="Tech", potential="medium"),
        Recommendation(user_id=user_id, topic="MCP Protocol Explained", confidence=85, evidence=["MCP search volume up 520% in 30 days", "Only 3 creators have covered this in depth", "Your API/protocol content averages 1.8x your channel mean"], expected_views_low=200000, expected_views_high=350000, expected_revenue_low=1400, expected_revenue_high=2500, risks=["Topic may be too niche for broad audience"], similar_content_title="REST vs GraphQL vs tRPC", similar_content_views=290000, publish_time="Thursday 7:00 PM EST", category="Tech", potential="high"),
    ]
    db.add_all(recommendations)

    trends = [
        Trend(user_id=user_id, topic="AI Agents", growth_days=18, competition="Medium", fit=88, search_volume="+340%", category="Tech", country="Global", direction="up"),
        Trend(user_id=user_id, topic="MCP Protocol", growth_days=12, competition="Low", fit=82, search_volume="+520%", category="Tech", country="United States", direction="up"),
        Trend(user_id=user_id, topic="Rust for Web Dev", growth_days=24, competition="Low", fit=74, search_volume="+180%", category="Tech", country="Global", direction="up"),
        Trend(user_id=user_id, topic="AI Video Generation", growth_days=15, competition="High", fit=79, search_volume="+290%", category="Creative", country="India", direction="up"),
        Trend(user_id=user_id, topic="No-Code SaaS", growth_days=21, competition="Medium", fit=71, search_volume="+160%", category="Business", country="United States", direction="stable"),
        Trend(user_id=user_id, topic="Local LLM Setup", growth_days=9, competition="Low", fit=85, search_volume="+410%", category="Tech", country="Germany", direction="up"),
        Trend(user_id=user_id, topic="GPT-5 Features", growth_days=6, competition="High", fit=90, search_volume="+680%", category="AI", country="Global", direction="up"),
        Trend(user_id=user_id, topic="TypeScript 6.0", growth_days=3, competition="Low", fit=86, search_volume="+220%", category="Tech", country="Global", direction="up"),
        Trend(user_id=user_id, topic="AI Coding Agents", growth_days=14, competition="Medium", fit=92, search_volume="+390%", category="Tech", country="United States", direction="up"),
        Trend(user_id=user_id, topic="Web Performance", growth_days=30, competition="Medium", fit=77, search_volume="+95%", category="Tech", country="United Kingdom", direction="stable"),
        Trend(user_id=user_id, topic="DevOps Automation", growth_days=20, competition="Low", fit=68, search_volume="+130%", category="Tech", country="Canada", direction="up"),
        Trend(user_id=user_id, topic="React Server Components", growth_days=16, competition="Medium", fit=84, search_volume="+210%", category="Tech", country="Global", direction="up"),
    ]
    db.add_all(trends)

    competitors = [
        Competitor(user_id=user_id, name="Fireship", subscriber_count=2800000, growth_rate=4.2, overlap=72, engagement_rate=8.7, last_video_title="AI Agents in 100 Seconds", last_video_views=1800000, is_trending=True),
        Competitor(user_id=user_id, name="Web Dev Simplified", subscriber_count=1500000, growth_rate=2.1, overlap=68, engagement_rate=6.4, last_video_title="Build a Full Stack App", last_video_views=420000, is_trending=False),
        Competitor(user_id=user_id, name="Theo", subscriber_count=920000, growth_rate=5.8, overlap=78, engagement_rate=9.2, last_video_title="React Is Dead?", last_video_views=680000, is_trending=True),
        Competitor(user_id=user_id, name="Jack Herrington", subscriber_count=480000, growth_rate=3.4, overlap=81, engagement_rate=7.8, last_video_title="TypeScript Tips You Need", last_video_views=245000, is_trending=False),
        Competitor(user_id=user_id, name="ByteGrad", subscriber_count=340000, growth_rate=6.1, overlap=75, engagement_rate=8.9, last_video_title="Next.js 15 Changes Everything", last_video_views=310000, is_trending=True),
        Competitor(user_id=user_id, name="Josh Tried Coding", subscriber_count=210000, growth_rate=7.3, overlap=69, engagement_rate=9.5, last_video_title="I Learned Rust in 30 Days", last_video_views=180000, is_trending=True),
    ]
    db.add_all(competitors)

    notifications = [
        Notification(user_id=user_id, title="Trend detected", message="AI Agents trending with +340% search volume", type="info", is_read=False),
        Notification(user_id=user_id, title="Competitor alert", message="Theo published a new video with 680K views", type="info", is_read=False),
        Notification(user_id=user_id, title="Revenue milestone", message="You've earned $3,240 this month", type="success", is_read=True),
        Notification(user_id=user_id, title="Sponsor response", message="Notion responded to your pitch", type="success", is_read=True),
    ]
    db.add_all(notifications)

    calendar_events = [
        CalendarEvent(user_id=user_id, day="Monday", time="12:00 PM", score=72, reason="Lunch break audience peak", type="good"),
        CalendarEvent(user_id=user_id, day="Tuesday", time="7:30 PM", score=94, reason="Highest engagement window for your audience", type="recommended"),
        CalendarEvent(user_id=user_id, day="Tuesday", time="12:00 PM", score=68, reason="Secondary peak", type="okay"),
        CalendarEvent(user_id=user_id, day="Wednesday", time="9:00 PM", score=81, reason="Evening scroll traffic", type="good"),
        CalendarEvent(user_id=user_id, day="Thursday", time="8:00 PM", score=88, reason="Pre-weekend content consumption peak", type="recommended"),
        CalendarEvent(user_id=user_id, day="Friday", time="12:00 PM", score=65, reason="Lower engagement, but less competition", type="okay"),
        CalendarEvent(user_id=user_id, day="Saturday", time="10:00 AM", score=70, reason="Weekend morning browse", type="good"),
        CalendarEvent(user_id=user_id, day="Sunday", time="7:00 PM", score=76, reason="Sunday evening prep for the week", type="good"),
    ]
    db.add_all(calendar_events)
