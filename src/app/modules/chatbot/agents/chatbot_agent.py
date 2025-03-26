# src/app/modules/chatbot/agents/chatbot_agent.py

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from src.app.core.config import settings
from ..prompts.chatbot_prompts import SYSTEM_PROMPT
from ..tools.data_collection_tools import store_patient_info  
from src.app.core.logging_config import chatbot_logger  

# Initialize LLM (Google Gemini)
llm = ChatGoogleGenerativeAI(
    google_api_key=settings.GEMINI_API_KEY,
    model=settings.GEMINI_LLM_MODEL_NAME,
)

# Bind tools to LLM (Includes patient info collection)
llm_with_tools = llm.bind_tools([store_patient_info])

class ChatbotAgent:
    """
    Handles general health-related questions.
    """
    def __init__(self, user):
        self.llm = llm_with_tools
        self.chat_history = [SystemMessage(content=SYSTEM_PROMPT)]
        self.user = user  # Store user details

    async def process_message(self, message: str):
        """Processes user input and returns an AI response."""

        chatbot_logger.info(f"[User: {self.user.id}] Processing message: {message}")

        try:
            self.chat_history.append(HumanMessage(content=message))

            #  Inject user_id for tool execution
            user_id = str(self.user.id)

            #  Call AI model
            response = await self.llm.ainvoke(
                self.chat_history,
                additional_kwargs={"user_id": user_id}
            )

            # Store response in history
            self.chat_history.append(AIMessage(content=response.content))

            chatbot_logger.debug(f"[User: {self.user.id}] AI Response: {response.content}")
            return response.content

        except Exception as e:
            chatbot_logger.error(f"[User: {self.user.id}] Error processing message: {str(e)}", exc_info=True)
            return "An error occurred while processing your message."

#  Initialize chatbot agent
chatbot_agent = ChatbotAgent
