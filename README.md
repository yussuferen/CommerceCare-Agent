# 🤖 CommerceCareAI - Autonomous Telegram Support Agent

## 📌 Project Overview

A Python-based Telegram bot designed to automate customer support for e-commerce platforms. Utilizing a LangChain agent and a Retrieval-Augmented Generation (RAG) pipeline, the system answers general policy questions by querying local PDF documents. Additionally, it features custom tool-calling capabilities to read and update a local JSON database for automated order tracking and order cancellations.

---

## 📊 Dataset Overview

The agent processes two types of local data sources to resolve customer queries:
*   **Unstructured Data:** 4 PDF documents containing store policies, return/refund terms, and shipping FAQs (processed via RAG).
*   **Structured Data:** A local `orders.json` file acting as a mock database for order status checks and cancellation workflows.

---

## 🛠️ Tech Stack

| Component | Technology / Library |
| :--- | :--- |
| **Language** | Python 3.10+ |
| **LLM Engine** | `gemini-3.5-flash-lite` |
| **Embedding Model** | `gemini-embedding-2-preview` |
| **Agent Framework** | LangChain |
| **Vector Database** | ChromaDB |

---

## ⚙️ Indexing & Setup Data Flow
```text
  [ PDF Files ]
       |
       v
  [ PyPDFDirectoryLoader ]
       |
       v
    [ Chunk ]
       |
       |─────► [ Gemini Embedding API ] ─────► Generates vector for chunk text
       |     (gemini-embedding-2-preview)
       v
  [ ChromaDB ] ────────────────────► Stores Embedding Vectors
```
## 🔄 Agent Tool-Calling & RAG Data Flow
```text
                             [ Telegram Message ]
                                      |
                                      v
                             [ LangChain Agent ]
                           (gemini-3.5-flash-lite)
                                      |
           ┌──────────────────────┴──────────────────────────────┐
           |                          |                          |
           ▼                          ▼                          ▼
  [ rag_search_tool ]    [ get_order_status_tool ]    [ cancel_order_tool ]
           |                          |                          |
      (ChromaDB)                (orders.json)              (orders.json)
           |                          |                          |
           └─────────────────────────────────────────────────────┘
                                      |
                                      v
                                 [ Response ]
```
---

## 🚀 Quick Start

### 1. Prerequisites

    Ensure your development environment meets the following requirements:

    Python 3.10+ installed
    Git installed
    Google Gemini API Key
    Telegram Bot Token

### 2. Installation

    Clone the repository and install the dependencies:

    # Clone the repository
    git clone https://github.com/yussuferen/ecommerce-support-agent.git
    cd ecommerce-support-agent

    # Create a virtual environment
    python -m venv venv

    # Activate the virtual environment
    # On Linux/macOS:
    source venv/bin/activate
    # On Windows:
    venv\Scripts\activate

    # Install required dependencies
    pip install -r requirements.txt

### 3. Environment Configuration

    Create a .env file in the root directory of the project. 
    Pass your API keys inside the env:

    GEMINI_API_KEY=your_gemini_api_key_here
    TELEGRAM_TOKEN=your_telegram_bot_token_here

### 4. Running

    Execute the main application to start the Telegram bot:
    python app.py