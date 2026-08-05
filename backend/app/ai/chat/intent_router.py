from typing import Dict, List
import re


INTENTS = {
    "trend_analysis": {"keywords": ["trend", "trending", "hot", "popular", "rising", "growth", "momentum"], "tools": ["trends"]},
    "competitor_analysis": {"keywords": ["competitor", "rival", "compare", "vs", "channel", "subscriber"], "tools": ["competitors"]},
    "recommendation_request": {"keywords": ["recommend", "suggest", "idea", "what should", "content", "video"], "tools": ["recommendations"]},
    "revenue_prediction": {"keywords": ["revenue", "earn", "money", "income", "rpm", "ads"], "tools": ["revenue"]},
    "audience_analysis": {"keywords": ["audience", "viewer", "demographic", "who watches", "age", "country"], "tools": ["audience"]},
    "calendar_query": {"keywords": ["when", "best time", "publish", "schedule", "time"], "tools": ["calendar"]},
    "dashboard_summary": {"keywords": ["overview", "summary", "dashboard", "stats", "metrics"], "tools": ["dashboard"]},
    "video_analysis": {"keywords": ["video", "analyze", "performance", "views"], "tools": ["trends", "recommendations"]},
    "general_chat": {"keywords": [], "tools": []},
}


class IntentRouter:
    def parse(self, message: str) -> Dict:
        message_lower = message.lower()

        for intent_name, config in INTENTS.items():
            if intent_name == "general_chat":
                continue
            for keyword in config["keywords"]:
                if keyword in message_lower:
                    return {
                        "intent": intent_name,
                        "confidence": 0.85,
                        "tools": config["tools"],
                    }

        return {
            "intent": "general_chat",
            "confidence": 0.5,
            "tools": [],
        }
