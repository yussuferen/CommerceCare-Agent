import json
import os
from langchain_core.tools import tool
from vectorstore import get_vector_db

ORDERS_JSON_PATH = "docs/json/orders.json"

vectorstore = get_vector_db()

@tool
def rag_search_tool(query):
    """
    Use this tool to search for company policies, return and refund terms, 
    warranty coverage, shipping fees, delivery timeframes, and general customer support FAQs.
    """
    docs = vectorstore.similarity_search(query, k=3)
    
    if not docs:
        return "No relevant policy or information found."
    
    results = [f"[SearchResult {i+1}]: {doc.page_content}" for i, doc in enumerate(docs)]
    return "\n\n".join(results)


@tool
def get_order_status_tool(order_id):
    """
    Use this tool when the user inquires about the status, tracking code, or details of a specific order ID (ORD-1001, ORD-1002..).
    """
    if not os.path.exists(ORDERS_JSON_PATH):
        return "Order database file not found."
    
    with open(ORDERS_JSON_PATH, "r", encoding="utf-8") as f:
        orders = json.load(f)
    
    for order in orders:
        if order["order_id"].upper() == order_id.upper():
            return json.dumps(order, ensure_ascii=False, indent=2)
            
    return f"Order ID {order_id} was not found in the system. Please verify the order number."


@tool
def cancel_order_tool(order_id):
    """
    Use this tool when a customer explicitly requests to cancel an order. 
    Only orders with status 'Preparing in Warehouse' or 'Order Processing' can be automatically cancelled.
    """
    if not os.path.exists(ORDERS_JSON_PATH):
        return "Order database file not found."
    
    with open(ORDERS_JSON_PATH, "r", encoding="utf-8") as f:
        orders = json.load(f)
    
    for order in orders:
        if order["order_id"].upper() == order_id.upper():
            current_status = order["status"]
            
            if current_status in ["Preparing in Warehouse", "Order Processing"]:
                order["status"] = "Cancelled"
                with open(ORDERS_JSON_PATH, "w", encoding="utf-8") as wf:
                    json.dump(orders, wf, ensure_ascii=False, indent=2)
                
                return f"SUCCESS: Order {order_id} has been successfully CANCELLED. A full refund has been triggered to the original payment method."
            else:
                return (
                    f"SYSTEM ERROR / CANCELLATION FAILED: Order {order_id} has current status '{current_status}'. "
                    "Automated system cancellation is only permitted while the order status is 'Preparing in Warehouse' or 'Order Processing'."
                )
                
    return f"Order ID {order_id} was not found in the database."