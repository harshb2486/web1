from typing import Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.chat_message import ChatMessage
from app.ai.chat.pipeline import ChatPipeline
from app.ai.chat.schemas import ChatResponse


class ChatService:
    def __init__(self):
        self.pipeline = ChatPipeline()

    async def send_message(self, user_id: str, message: str, db: AsyncSession) -> ChatResponse:
        user_msg = ChatMessage(
            user_id=user_id,
            role="user",
            content=message,
        )
        db.add(user_msg)
        await db.flush()

        result = await self.pipeline.process(user_id, message, db)

        assistant_msg = ChatMessage(
            user_id=user_id,
            role="assistant",
            content=result.response,
            intent=result.intent,
        )
        db.add(assistant_msg)
        await db.flush()

        return result

    async def get_history(self, user_id: str, db: AsyncSession, limit: int = 50) -> List[Dict]:
        result = await db.execute(
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at.desc())
            .limit(limit)
        )
        messages = result.scalars().all()
        return [
            {
                "id": m.id,
                "role": m.role,
                "content": m.content,
                "intent": m.intent,
                "created_at": m.created_at.isoformat() if m.created_at else None,
            }
            for m in reversed(messages)
        ]
