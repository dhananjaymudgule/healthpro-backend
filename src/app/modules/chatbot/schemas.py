# src/app/modules/chatbot/schemas.py

from pydantic import BaseModel


class ChatRequest(BaseModel):
    session_id: str  
    message: str

class ChatResponse(BaseModel):
    response: str