import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from tools import rag_search_tool, get_order_status_tool, cancel_order_tool

LLM_MODEL = "gemini-3.5-flash-lite"

llm = ChatGoogleGenerativeAI(
    model=LLM_MODEL,
    temperature=0,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

tools = [rag_search_tool, get_order_status_tool, cancel_order_tool]

system_prompt = """You are CommerceCareAI, an intelligent customer support AI assistant for an e-commerce platform.
Your primary language of communication is English. Always respond politely, concisely, and professionally in English.

Follow these execution guidelines strictly:
1. For general inquiries, store policies, return/refund rules, warranty, shipping terms, or FAQ questions, use the `rag_search_tool`.
2. For specific order status or tracking inquiries (e.g., ORD-1001, ORD-1002), use the `get_order_status_tool`.
3. For order cancellation requests, use the `cancel_order_tool`.
4. If `cancel_order_tool` fails because the order status is already 'Dispatched / In Transit', use `rag_search_tool` to check the policy for in-transit orders and instruct the user on what to do.
5. Never hallucinate policies or order details. Rely strictly on tool outputs."""

memory = MemorySaver()

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt,
    checkpointer=memory
)

def run_agent(user_input,thread_id="default_user"):
    config = {"configurable": {"thread_id": thread_id}}

    try:
        response = agent.invoke({"messages": [{"role": "user", "content": user_input}]},config=config)
    except Exception as e:
        print(f"ERROR: {e}")
        return "Internal Error"
        
    raw_content = response["messages"][-1].content
    
    if isinstance(raw_content, list):
        texts = [item["text"] for item in raw_content if "text" in item]
        return "".join(texts)
        
    return str(raw_content)