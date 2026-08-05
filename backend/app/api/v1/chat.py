from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.ai.chat.service import ChatService
from app.api.v1.response import success_response

router = APIRouter(tags=["chat"])
chat_service = ChatService()


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
async def send_message(
    data: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await chat_service.send_message(current_user.id, data.message, db)
    return success_response(result.model_dump())


@router.get("/chat/history")
async def get_chat_history(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    history = await chat_service.get_history(current_user.id, db)
    return success_response(history)
