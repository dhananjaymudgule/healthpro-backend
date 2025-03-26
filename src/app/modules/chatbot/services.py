# src/app/modules/chatbot/services.py

from src.app.modules.chatbot.pipeline import ChatbotPipeline
from src.app.db.mongodb.chat_repository import save_chat, get_chat_history
from src.app.core.logging_config import chatbot_logger  


class ChatService:
    def __init__(self, user, db):
        self.user = user
        self.db = db
        self.chatbot_pipeline = ChatbotPipeline(user, db)  #  Instantiate pipeline

    async def handle_message(self, session_id: str, message: str):
        """Routes user message through chatbot pipeline and saves chat history."""
        user_id = str(self.user.id)
        chatbot_logger.info(f"[Session: {session_id}] User {user_id} sent a message: {message}")

        try:
            #  Pass session_id to route_message
            ai_response = await self.chatbot_pipeline.route_message(session_id, message)

            #  Retrieve chat history from MongoDB
            chat_history = await get_chat_history(user_id, session_id)

            #  Append user & AI messages
            chat_history.append({"role": "user", "content": message})
            chat_history.append({"role": "assistant", "content": ai_response})

            #  Save updated chat history
            await save_chat(user_id, session_id, chat_history)

            chatbot_logger.info(f"[Session: {session_id}] AI Response: {ai_response}")
            return ai_response

        except Exception as e:
            chatbot_logger.error(f"[Session: {session_id}] Error: {str(e)}", exc_info=True)
            return "An error occurred while processing your message."
