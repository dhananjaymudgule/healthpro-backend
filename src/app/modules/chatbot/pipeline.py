# src/app/modules/chatbot/pipeline.py

from src.app.modules.chatbot.agents.chatbot_agent import ChatbotAgent
from src.app.modules.chatbot.agents.data_collection_agent import DataCollectionAgent
from src.app.db.repositories.patient_repository import get_patient_info
from src.app.core.logging_config import chatbot_logger 




class ChatbotPipeline:
    """
    Manages chatbot flow - decides whether to answer questions or collect patient info.
    """

    def __init__(self, user, db):
        self.user = user
        self.db = db
        self.chatbot_agent = ChatbotAgent(user)
        self.data_collection_agent = DataCollectionAgent(user, db)  #  Pass db

    async def route_message(self, session_id: str, message: str):  #  Accepts session_id
        """Routes message based on patient info availability."""
        user_id = str(self.user.id)

        # Step 1: Check patient info in the database
        patient_info = await get_patient_info(self.db, user_id)  #  Pass db

        if not patient_info:
            chatbot_logger.info(f"[Session: {session_id}] [User: {user_id}] No patient info found. Routing to DataCollectionAgent.")
            return await self.data_collection_agent.process_message(session_id, message)  #  Pass session_id

        chatbot_logger.info(f"[Session: {session_id}] [User: {user_id}] Patient info exists. Routing to ChatbotAgent for Q&A.")
        return await self.chatbot_agent.process_message(message)
