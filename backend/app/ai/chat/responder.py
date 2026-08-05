from typing import Dict


class Responder:
    def generate(self, intent: str, context: str, tool_data: Dict, user_message: str) -> str:
        if intent == "trend_analysis":
            return self._respond_trends(tool_data)
        elif intent == "competitor_analysis":
            return self._respond_competitors(tool_data)
        elif intent == "recommendation_request":
            return self._respond_recommendations(tool_data)
        elif intent == "revenue_prediction":
            return self._respond_revenue(tool_data)
        elif intent == "audience_analysis":
            return self._respond_audience(tool_data)
        elif intent == "calendar_query":
            return self._respond_calendar(tool_data)
        elif intent == "dashboard_summary":
            return self._respond_dashboard(tool_data)
        else:
            return self._respond_general(user_message)

    def _respond_trends(self, data: Dict) -> str:
        trends = data.get("trends", [])
        if not trends:
            return "No trending data available yet. Run the pipeline to analyze trends."
        lines = ["Here are the current trends relevant to you:\n"]
        for t in trends[:5]:
            emoji = "📈" if t.get("direction") == "up" else "📉" if t.get("direction") == "down" else "➡️"
            lines.append(f"{emoji} **{t['topic']}** — {t['searchVolume']} growth, {t['competition']} competition, {t['fit']}% fit")
        lines.append(f"\nI found {len(trends)} trends. The top trend is **{trends[0]['topic']}** with {trends[0]['searchVolume']} search volume growth.")
        return "\n".join(lines)

    def _respond_competitors(self, data: Dict) -> str:
        comps = data.get("competitors", [])
        if not comps:
            return "No competitor data available. Run the pipeline to analyze competitors."
        lines = ["Here's your competitive landscape:\n"]
        for c in comps[:5]:
            trend = "🔥 Trending" if c.get("trending") else ""
            lines.append(f"• **{c['name']}** — {(c['subscribers']/1000000):.1f}M subs, +{c['growthRate']}% growth, {c['engagement']}% engagement {trend}")
        return "\n".join(lines)

    def _respond_recommendations(self, data: Dict) -> str:
        recs = data.get("recommendations", [])
        if not recs:
            return "No recommendations generated yet. Run the pipeline to get AI content ideas."
        lines = ["Here are your top AI-powered content recommendations:\n"]
        for r in recs[:3]:
            lines.append(f"**{r['topic']}** ({r['confidence']}% confidence)")
            lines.append(f"  Expected views: {r['expectedViews']['low']//1000}K–{r['expectedViews']['high']//1000}K")
            lines.append(f"  Category: {r['category']} | Potential: {r['potential']}")
            lines.append("")
        return "\n".join(lines)

    def _respond_revenue(self, data: Dict) -> str:
        return f"Your current monthly revenue is **${data.get('current', 0):,}**.\n\nBreakdown:\n• Ads: ${data.get('breakdown', {}).get('ads', 0):,}\n• Sponsorships: ${data.get('breakdown', {}).get('sponsorships', 0):,}\n• Affiliate: ${data.get('breakdown', {}).get('affiliate', 0):,}\n• Membership: ${data.get('breakdown', {}).get('membership', 0):,}"

    def _respond_audience(self, data: Dict) -> str:
        devices = ", ".join(f"{d['name']} ({d['percent']}%)" for d in data.get("devices", []))
        hours = ", ".join(data.get("peakHours", []))
        return (
            f"Your audience overview:\n"
            f"• Returning viewers: {data.get('returningViewers', 0)}%\n"
            f"• Avg watch time: {data.get('avgWatchTime', 'N/A')}\n"
            f"• Peak hours: {hours}\n"
            f"• Top devices: {devices}"
        )

    def _respond_calendar(self, data: Dict) -> str:
        if not data:
            return "No calendar data available."
        best = max(data, key=lambda x: x.get("score", 0))
        return f"Your best publish time is **{best['day']} at {best['time']}** (score: {best['score']}/100).\n\nReason: {best['reason']}"

    def _respond_dashboard(self, data: Dict) -> str:
        return f"Here's your dashboard overview:\n• Total Views: {data.get('totalViews', 'N/A')}\n• Revenue: {data.get('revenue', 'N/A')}\n• Engagement Rate: {data.get('engagementRate', 'N/A')}\n• Subscribers: {data.get('subscribers', 'N/A')}"

    def _respond_general(self, message: str) -> str:
        return "I can help you analyze trends, competitors, revenue, audience data, and generate content recommendations. Try asking about any of these topics!"
