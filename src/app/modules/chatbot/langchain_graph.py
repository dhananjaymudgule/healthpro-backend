# src/app/modules/chatbot/langchain_graph.py

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict
from typing import Annotated
from .pipeline import get_chatbot_pipeline
from src.app.core.logging_config import chatbot_logger  

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

# Chatbot node
async def chatbot(state: State):
    """Processes user input through the AI model."""
    chatbot_logger.info("Processing chatbot response...")

    try:
        user = state["user"]
        chatbot_pipeline = get_chatbot_pipeline(user)

        ai_response = await chatbot_pipeline.route_message(state["messages"][-1].content)  
        chatbot_logger.debug(f"AI Response: {ai_response}")

        return {"messages": [{"role": "assistant", "content": ai_response}]}

    except Exception as e:
        chatbot_logger.error(f"Error in chatbot node: {str(e)}", exc_info=True)
        return {"messages": [{"role": "system", "content": "An error occurred."}]}

graph_builder.add_node("chatbot", chatbot)

# Define flow edges
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# Compile the graph
graph = graph_builder.compile()
