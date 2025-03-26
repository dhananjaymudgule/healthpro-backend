# Chatbot

```
src/
├── app/
│   ├── modules/
│   │   ├── chatbot/             # New chatbot module
│   │   │   ├── __init__.py
│   │   │   ├── routes.py         # API endpoints for chatbot
│   │   │   ├── services.py       # Business logic for chatbot
│   │   │   ├── schemas.py        # Pydantic models for request validation
│   │   │   ├── langchain/        # LangChain & LangGraph specific logic
│   │   │   │   ├── __init__.py
│   │   │   │   ├── graph.py       # LangGraph structure & execution
│   │   │   │   ├── tools.py       # Tool implementations
│   │   │   │   ├── memory.py      # Chat memory management
│   │   │   │   ├── prompts.py     # System prompts and user instructions
│   │   │   │   ├── agents.py      # LangChain agents
│   │   │   ├── dependencies.py   # Any required dependencies

```

### Explanation:
- `routes.py` → Defines API endpoints to interact with the chatbot.
- `services.py` → Contains business logic, handles processing.
- `dependencies.py` → Manages required dependencies (e.g., database connection, authentication).
- `schemas.py` → Defines request/response schemas using Pydantic.
- `langchain/` → Contains core logic for LangChain & LangGraph.
  - `agents.py` → Defines different agents.
  - `chains.py` → Manages LangChain chains.
  - `memory.py` → Implements memory for conversation context.
  - `prompts.py` → Stores chatbot prompts.
  - `graph.py` → Manages the LangGraph workflow.

