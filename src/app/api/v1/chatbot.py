# app/api/v1/chatbot.py


from fastapi import APIRouter
from src.app.modules.chatbot.routes import router as chatbot_router  

router = APIRouter()

#  Include chatbot routes under `/api/v1/chatbot`
router.include_router(chatbot_router, tags=["Chatbot"])

