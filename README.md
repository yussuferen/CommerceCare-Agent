# CommerceCare-Agent

A Telegram bot that automates e-commerce customer support using **LangChain**, **LangGraph**, and **Gemini API**.
It combines a RAG pipeline for answering policy questions with custom tools to check order statuses and process cancellations.

---

## Tech Stack

- **LLM & Embeddings:** Gemini API
- **Vector DB:** ChromaDB
- **Agent Framework:** LangChain / LangGraph

---
## Data Flow
```mermaid
graph TD
    MSG[Telegram Message] --> AGENT[LangChain Agent / Gemini API]

    %% Agent Tool Calling Branches
    AGENT -->|Policy Questions| RAG[rag_search_tool]
    AGENT -->|Check Status| STATUS[get_order_status_tool]
    AGENT -->|Cancel Order| CANCEL[cancel_order_tool]

    %% Final Response
    RAG --> RESP([Telegram Response])
    STATUS --> RESP
    CANCEL --> RESP
```
---

## Quick Start

### 1. Prerequisites

    Ensure:
    
    Python 3.10+ installed
    Git installed
    Google Gemini API Key
    Telegram Bot Token

### 2. Installation

    git clone https://github.com/yussuferen/CommerceCare-Agent.git
    cd CommerceCare-Agent
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

### 3. Environment Configuration

    Create a .env file in the root directory.

    # Required Credentials
    GEMINI_API_KEY=<gemini_api_key>
    TELEGRAM_TOKEN=<telegram_token>

    # Optional: LangSmith
    LANGSMITH_TRACING=true
    LANGSMITH_ENDPOINT=<langsmith_end_point>
    LANGSMITH_API_KEY=<langsmith_api_key>
    LANGSMITH_PROJECT=<project_name>

### 4. Running

    python app.py