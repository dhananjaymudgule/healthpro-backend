# src/app/db/mongodb/chat_repository.py

from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
from src.app.core.config import settings
from src.app.db.mongodb.chat_utils import serialize_messages, deserialize_messages  
from src.app.core.logging_config import db_logger  

# 🔹 Initialize MongoDB Client
client = AsyncIOMotorClient(settings.MONGO_DB_URI)
db = client.healthpro_db
chat_collection = db.chats  # Collection for chat history

async def save_chat(user_id: str, session_id: str, chat_history: list):
    """
    Save chat history in MongoDB for a specific user session.
    
    Args:
        user_id (str): The unique user identifier.
        session_id (str): The session identifier.
        chat_history (list): List of chat messages.
    """
    serialized_messages = serialize_messages(chat_history)

    chat_data = {
        "user_id": user_id,  #  Store user-wise chat history
        "session_id": session_id,  #  Store session-wise chat history
        "messages": serialized_messages,
        "timestamp": datetime.now(timezone.utc),
    }

    try:
        db_logger.info(f"Saving chat for user {user_id}, session {session_id}")
        
        await chat_collection.update_one(
            {"user_id": user_id, "session_id": session_id},  # 🔹 Query by both user & session
            {"$set": chat_data},
            upsert=True,
        )
        
        db_logger.debug(f"Chat successfully saved for session {session_id}")

    except Exception as e:
        db_logger.error(f"Error saving chat for session {session_id}: {str(e)}", exc_info=True)

async def get_chat_history(user_id: str, session_id: str):
    """
    Retrieve chat history for a specific user session.
    
    Args:
        user_id (str): The unique user identifier.
        session_id (str): The session identifier.

    Returns:
        list: Deserialized chat messages.
    """
    try:
        db_logger.info(f"Retrieving chat history for user {user_id}, session {session_id}")

        chat_data = await chat_collection.find_one({"user_id": user_id, "session_id": session_id})
        if chat_data and "messages" in chat_data:
            db_logger.debug(f"Chat history retrieved for session {session_id}")
            return deserialize_messages(chat_data["messages"])  #  Convert JSON back to LangChain messages
        
        db_logger.warning(f"No chat history found for session {session_id}")
    
    except Exception as e:
        db_logger.error(f"Error retrieving chat history for session {session_id}: {str(e)}", exc_info=True)

    return []
