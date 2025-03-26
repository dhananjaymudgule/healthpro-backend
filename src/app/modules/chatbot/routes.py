# src/app/modules/chatbot/routes.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.modules.chatbot.schemas import ChatRequest, ChatResponse
from src.app.modules.chatbot.services import ChatService
from src.app.modules.users.dependencies import get_current_user
from src.app.core.logging_config import chatbot_logger  
from src.app.db.session import get_db

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, user=Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    """Handles chat messages by routing them through ChatService."""
    chatbot_logger.info(f"[Session: {request.session_id}] Received message: {request.message}")

    try:
        chat_service = ChatService(user, db)  # Initialize ChatService
        response = await chat_service.handle_message(request.session_id, request.message)
        return {"response": response}

    except Exception as e:
        chatbot_logger.error(f"[Session: {request.session_id}] Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="An error occurred while processing your message.")
