# src/app/modules/chatbot/agents/data_collection_agent.py

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from ..tools.data_collection_tools import store_patient_info, check_missing_patient_info
from ..prompts.data_collection_prompts import SYSTEM_PROMPT
from src.app.db.repositories.patient_repository import get_patient_info
from src.app.core.logging_config import chatbot_logger  


class DataCollectionAgent:
    """
    Handles collection and storage of patient health information.
    """

    def __init__(self, user, db):
        self.user = user
        self.db = db
        self.chat_history = [SystemMessage(content=SYSTEM_PROMPT)]

    async def process_message(self, session_id: str, message: str):  # Accepts session_id
        """Processes user input for patient information collection."""

        user_id = str(self.user.id)
        chatbot_logger.info(f"[Session: {session_id}] [User: {user_id}] Processing data collection message: {message}")

        # Step 1: Check existing patient info
        patient_info = await get_patient_info(self.db, user_id)  #  Pass db

        if patient_info:
            chatbot_logger.info(f"[Session: {session_id}] [User: {user_id}] Patient info exists. Checking for missing fields...")
            missing_fields = check_missing_patient_info(patient_info)

            if not missing_fields:
                chatbot_logger.info(f"[Session: {session_id}] [User: {user_id}] All health details are complete.")
                return "Your health details are already complete. How else can I assist you?"

            chatbot_logger.info(f"[Session: {session_id}] [User: {user_id}] Missing fields detected: {missing_fields}")
            return f"I see some details are missing: {', '.join(missing_fields)}. Can you provide them?"

        # Step 2: If no data exists, ask for full details
        chatbot_logger.info(f"[Session: {session_id}] [User: {user_id}] No patient info found. Requesting full details.")
        return "I don't have your health details yet. Can you provide your gender, age, height, weight, and health conditions?"
