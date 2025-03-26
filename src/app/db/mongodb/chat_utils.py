# src/app/db/mongodb/chat_utils.py

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from datetime import datetime, timezone
from src.app.core.logging_config import db_logger  

def serialize_messages(messages):
    """
    Convert LangChain messages into a JSON-serializable format.

    Args:
        messages (list): List of LangChain message objects.

    Returns:
        list: Serialized JSON messages.
    """
    try:
        db_logger.debug("Serializing chat messages...")

        serialized = [
            {
                "type": type(msg).__name__,  # 🔹 Store message type (SystemMessage, HumanMessage, AIMessage)
                "content": msg.content,
                "timestamp": datetime.now(timezone.utc).isoformat()  #  Store message timestamp
            }
            for msg in messages
        ]
        
        db_logger.debug("Chat messages successfully serialized.")
        return serialized

    except Exception as e:
        db_logger.error("Error serializing messages", exc_info=True)
        return []

def deserialize_messages(messages):
    """
    Convert stored JSON messages back into LangChain message objects.

    Args:
        messages (list): List of JSON messages from MongoDB.

    Returns:
        list: Deserialized LangChain message objects.
    """
    try:
        db_logger.debug("Deserializing chat messages...")

        message_mapping = {
            "SystemMessage": SystemMessage,
            "HumanMessage": HumanMessage,
            "AIMessage": AIMessage,
        }

        deserialized = [
            message_mapping[msg["type"]](content=msg["content"])
            for msg in messages
        ]

        db_logger.debug("Chat messages successfully deserialized.")
        return deserialized

    except Exception as e:
        db_logger.error("Error deserializing messages", exc_info=True)
        return []
