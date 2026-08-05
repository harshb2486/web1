from typing import Dict, List
from sqlalchemy.ext.asyncio import AsyncSession


class ContextFormatter:
    def format_creator_context(self, profile: Dict, features: Dict) -> str:
        lines = []
        if profile:
            lines.append(f"Creator: {profile.get('name', 'Unknown')}")
            lines.append(f"Niche: {profile.get('niche', 'Unknown')}")
            lines.append(f"Subscribers: {profile.get('subscriber_count', 0):,}")
        if features:
            lines.append(f"CTR: {features.get('ctr', 0):.1%}")
            lines.append(f"Avg Watch Time: {features.get('avg_watch_time', 0):.0f}s")
            lines.append(f"Retention: {features.get('retention_rate', 0):.1%}")
            lines.append(f"Engagement: {features.get('engagement_score', 0):.1f}")
        return "\n".join(lines) if lines else "No creator data available."

    def format_analytics(self, features: Dict, videos: List[Dict]) -> str:
        lines = []
        if features:
            lines.append(f"Upload Frequency: {features.get('upload_frequency', 0):.1f}/week")
            lines.append(f"View Velocity: {features.get('view_velocity', 0):.0f} views/day")
            lines.append(f"Growth: {features.get('growth_pct', 0):.1f}%")
        if videos:
            avg_views = sum(v.get("views", 0) for v in videos) / len(videos) if videos else 0
            lines.append(f"Avg Views: {avg_views:,.0f}")
            lines.append(f"Total Videos: {len(videos)}")
        return "\n".join(lines) if lines else "No analytics data available."

    def format_trends(self, trends: List[Dict]) -> str:
        if not trends:
            return "No trend data available."
        lines = [f"Top {len(trends)} trending topics:"]
        for t in trends[:5]:
            direction = "↑" if t.get("direction") == "up" else "↓" if t.get("direction") == "down" else "→"
            lines.append(
                f"- {t.get('topic', 'Unknown')} {direction} "
                f"(Fit: {t.get('fit', 0)}%, Volume: {t.get('searchVolume', 'N/A')})"
            )
        return "\n".join(lines)

    def format_recommendations(self, recs: List[Dict]) -> str:
        if not recs:
            return "No recommendations available."
        lines = [f"Top {len(recs)} recommendations:"]
        for r in recs[:3]:
            lines.append(
                f"- {r.get('topic', 'Unknown')} "
                f"(Confidence: {r.get('confidence', 0)}%, "
                f"Potential: {r.get('potential', 'unknown')})"
            )
        return "\n".join(lines)

    def format_memory(self, memory: Dict) -> str:
        if not memory:
            return "No memory data available."
        lines = []
        prefs = memory.get("preferences", {})
        if prefs.get("categories"):
            lines.append(f"Preferred Categories: {', '.join(prefs['categories'][:3])}")
        if prefs.get("publish_times"):
            lines.append(f"Best Publish Times: {', '.join(prefs['publish_times'][:2])}")
        learning = memory.get("learning_history", {})
        if learning.get("successful_topics"):
            successful = [t.get("topic") for t in learning["successful_topics"][:3]]
            lines.append(f"Successful Topics: {', '.join(successful)}")
        return "\n".join(lines) if lines else "No memory data available."

    def compose_full_context(
        self,
        creator_context: str,
        analytics_context: str,
        trends_context: str,
        recommendations_context: str,
        memory_context: str,
    ) -> str:
        return (
            f"=== Creator Profile ===\n{creator_context}\n\n"
            f"=== Analytics ===\n{analytics_context}\n\n"
            f"=== Current Trends ===\n{trends_context}\n\n"
            f"=== Recommendations ===\n{recommendations_context}\n\n"
            f"=== Learned Preferences ===\n{memory_context}"
        )
