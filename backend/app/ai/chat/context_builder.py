from typing import Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.chat_message import ChatMessage
from app.models.profile import CreatorProfile


class ContextBuilder:
    async def build(self, user_id: str, intent: str, tool_data: Dict, db: AsyncSession) -> str:
        profile = await self._get_profile(user_id, db)
        chat_history = await self._get_history(user_id, db, limit=5)

        context_parts = []

        if profile:
            context_parts.append(f"Creator: {profile.name}, Channel: {profile.channel_name}, Niche: {profile.niche}, Subscribers: {profile.subscriber_count}")

        if chat_history:
            context_parts.append("Recent conversation:")
            for msg in chat_history[-3:]:
                context_parts.append(f"  {msg.role}: {msg.content[:200]}")

        for tool_name, data in tool_data.items():
            if data:
                context_parts.append(f"\n{tool_name.upper()} DATA:")
                if isinstance(data, list):
                    for item in data[:5]:
                        if isinstance(item, dict):
                            context_parts.append(f"  - {item.get('topic', item.get('name', str(item)[:100]))}")
                elif isinstance(data, dict):
                    for k, v in list(data.items())[:5]:
                        context_parts.append(f"  {k}: {v}")

        return "\n".join(context_parts)

    async def _get_profile(self, user_id: str, db: AsyncSession):
        r = await db.execute(select(CreatorProfile).where(CreatorProfile.user_id == user_id))
        return r.scalar_one_or_none()

    async def _get_history(self, user_id: str, db: AsyncSession, limit: int = 5):
        r = await db.execute(
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at.desc())
            .limit(limit)
        )
        return list(reversed(r.scalars().all()))
