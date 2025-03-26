# src/app/modules/chatbot/tools/data_collection_tools.py

import json
from langchain_core.messages import ToolMessage
from langchain.tools import Tool
from langchain_core.tools import tool
from src.app.db.session import get_db
from src.app.db.repositories.patient_repository import create_patient, get_patient_info
from src.app.core.logging_config import db_logger  
from typing import Dict, List


@tool
async def store_patient_info(user_id: str, patient_data: dict):
    """
    LangChain tool to store or update patient information in the database.

    Args:
        user_id (str): The patient's user ID.
        patient_data (dict): Patient details (age, gender, BP, etc.).

    Returns:
        dict: Success message.
    """
    async with get_db() as db:
        try:
            db_logger.info(f"Storing patient info for user {user_id}")

            patient_record = await create_patient(db, user_id, patient_data)

            db_logger.debug(f"Successfully stored patient info for user {user_id}, patient_id={patient_record.id}")
            return {"success": True, "message": "Patient info stored successfully!", "patient_id": patient_record.id}

        except Exception as e:
            db_logger.error(f"Error storing patient info for user {user_id}: {str(e)}", exc_info=True)
            return {"success": False, "message": str(e)}


async def check_missing_patient_info(user_id: str):
    """
    Checks the database for missing patient details.

    Args:
        user_id (str): The patient's user ID.

    Returns:
        list: List of missing details.
    """
    async with get_db() as db:
        patient_info = await get_patient_info(db, user_id)

    if not patient_info:
        db_logger.warning(f"No patient info found for user {user_id}. Requesting full details.")
        return ["gender", "date_of_birth", "height_cm", "weight_kg", "sbp", "smoking_status", "diabetes_status", "total_cholesterol_level"]

    missing_fields = []
    required_fields = ["gender", "date_of_birth", "height_cm", "weight_kg", "sbp", "smoking_status", "diabetes_status", "total_cholesterol_level"]

    for field in required_fields:
        if not getattr(patient_info, field, None):
            missing_fields.append(field)

    if missing_fields:
        db_logger.info(f"User {user_id} is missing: {missing_fields}")
    else:
        db_logger.info(f"User {user_id} has all required health information.")

    return missing_fields


# List of available tools
TOOLS = [store_patient_info]

class BasicToolNode:
    """A node that runs tools requested in the last AIMessage."""

    def __init__(self, tools: List[Tool]) -> None:
        self.tools_by_name = {tool.name: tool for tool in tools}

    async def __call__(self, inputs: dict):
        """
        Executes tools requested in the last AI message.

        Args:
            inputs (dict): Contains a list of messages.

        Returns:
            dict: Messages containing tool execution results.
        """
        if not inputs.get("messages"):
            raise ValueError("No message found in input")

        message = inputs["messages"][-1]  # Get the last AI message
        outputs = []

        for tool_call in message.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            if tool_name not in self.tools_by_name:
                db_logger.error(f"Tool '{tool_name}' not found!")
                continue

            try:
                db_logger.info(f"Invoking tool: {tool_name} with args: {tool_args}")
                tool_result = await self.tools_by_name[tool_name].ainvoke(tool_args)
                
                outputs.append(
                    ToolMessage(
                        content=json.dumps(tool_result),
                        name=tool_name,
                        tool_call_id=tool_call["id"],
                    )
                )
                db_logger.debug(f"Tool {tool_name} executed successfully.")

            except Exception as e:
                db_logger.error(f"Error executing tool {tool_name}: {str(e)}", exc_info=True)
                outputs.append(
                    ToolMessage(
                        content=json.dumps({"error": str(e)}),
                        name=tool_name,
                        tool_call_id=tool_call["id"],
                    )
                )

        return {"messages": outputs}


# Initialize tool node
tool_node = BasicToolNode(tools=TOOLS)
