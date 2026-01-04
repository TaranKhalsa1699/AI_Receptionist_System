from typing import TypedDict, Annotated, List, Optional
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY
from models import PatientData, WebhookPayload
from database import persist_patient_data
from utils import trigger_webhook
import logging

# Initialize LLM (Used for more complex extraction if needed later, but sticking to deterministic logic for now)
llm = ChatOpenAI(api_key=OPENAI_API_KEY, model="gpt-4o", temperature=0)

# Define State
class State(TypedDict):
    messages: List[BaseMessage]
    patient_data: PatientData
    ward: Optional[str]
    missing_field: Optional[str]
    is_complete: bool
    db_written: bool

# --- Node Logic ---

def start_node(state: State):
    """
    Entry point. Doesn't do much interpretation, just passes through.
    """
    return state

def router_node(state: State):
    """
    Classifies the ward based on the initial query if ward is not set.
    """
    if state.get("ward"):
        return state

    messages = state["messages"]
    last_message = messages[-1].content.lower()

    # Deterministic Keyword Routing
    keywords = {
        "emergency": ["pain", "bleeding", "unconscious", "accident", "severe", "stroke", "heart attack", "broken", "trauma", "heart", "chest", "collapse"],
        "mental_health": ["anxiety", "depression", "panic", "suicide", "self-harm", "sad", "hopeless", "stress", "mental"],
        # General captures everything else (stomach, routine, mild issues)
    }

    ward = "general" # Default
    
    # Check strict matches
    found = False
    for w, kws in keywords.items():
        if any(k in last_message for k in kws):
            ward = w
            found = True
            break
    
    # FIX: Persist the initial query so we don't ask for it again
    patient_data = state.get("patient_data", PatientData())
    if not patient_data.query:
        patient_data.query = messages[-1].content

    return {"ward": ward, "patient_data": patient_data}

def collection_node(state: State):
    """
    Collects Name -> Age -> Query (if missing).
    """
    messages = state["messages"]
    patient_data = state.get("patient_data", PatientData())
    
    # Check for missing fields in strict order
    if not patient_data.name:
        current_missing = "name"
    elif patient_data.age is None:
        current_missing = "age"
    elif not patient_data.query:
        current_missing = "query"
    else:
        current_missing = None
    
    # If we were waiting for a specific field, try to extract it from the last message
    # (Skip if this is the very first turn and we just routed)
    last_message = messages[-1].content
    previous_missing = state.get("missing_field")

    if previous_missing:
        try:
            if previous_missing == "name":
                # Assume message is name
                patient_data.name = last_message
            
            elif previous_missing == "age":
                # Extract number
                import re
                match = re.search(r"\d+", last_message)
                if match:
                    patient_data.age = int(match.group())

            elif previous_missing == "query":
                patient_data.query = last_message
                
        except ValueError:
             # Validation failed, will ask again
             pass

    # Re-evaluate missing fields after potential update
    final_missing = None
    reply = ""

    if not patient_data.name:
        final_missing = "name"
        # Context-aware greeting if this is the start of the conversation (and we already caught the query)
        if patient_data.query and len(messages) <= 1:
             reply = "Hello. I have noted your symptoms. To proceed with registration, could you please provide the patient's full name?"
        elif len(messages) <= 1:
             reply = "Hello. Welcome to the hospital reception. To begin, could you please provide the patient's full name?"
        else:
             reply = "Could you please provide the patient's full name?"

    elif patient_data.age is None:
        final_missing = "age"
        reply = "Thank you. Now, could you please provide the patient's age?"
        
    elif not patient_data.query:
        final_missing = "query"
        reply = "Thank you. Could you briefly describe the main symptoms or reason for the visit?"
    else:
        # All complete
        # Check if the user is just saying thanks (post-completion)
        last_message_lower = messages[-1].content.lower()
        gratitude_phrases = ["thank", "thanks", "thx", "cool", "ok", "okay", "bye"]
        if any(phrase in last_message_lower for phrase in gratitude_phrases):
             return {"patient_data": patient_data, "is_complete": True, "missing_field": None, "messages": [AIMessage(content="You are welcome. Please proceed to the assigned ward.")]}

        ward_display_map = {
            "general": "General Ward",
            "emergency": "Emergency Ward",
            "mental_health": "Mental Health Ward"
        }
        ward_name = ward_display_map.get(state["ward"], "General Ward")
        
        reply = (
            f"Registration complete.\n"
            f"Patient {patient_data.name}, age {patient_data.age}, has been assigned to the {ward_name}.\n"
            f"Please proceed to the {ward_name} or wait for further assistance."
        )
        return {"patient_data": patient_data, "is_complete": True, "missing_field": None, "messages": [AIMessage(content=reply)]}

    return {"patient_data": patient_data, "missing_field": final_missing, "messages": [AIMessage(content=reply)]}

async def finalize_node(state: State):
    """
    Persist data and trigger webhook.
    """
    if state.get("is_complete") and not state.get("db_written"):
        
        payload = WebhookPayload(
            patient_name=state["patient_data"].name,
            patient_age=state["patient_data"].age,
            patient_query=state["patient_data"].query,
            ward=state["ward"]
        )

        # 1. Persist to DB
        success_db = persist_patient_data(payload)
        
        # 2. Trigger Webhook
        if success_db:
             await trigger_webhook(payload)
             return {"db_written": True}
    
    return state


# --- Graph Construction ---
workflow = StateGraph(State)

workflow.add_node("start", start_node)
workflow.add_node("router", router_node)
workflow.add_node("collection", collection_node)
workflow.add_node("finalize", finalize_node)

workflow.set_entry_point("start")

workflow.add_edge("start", "router")
workflow.add_edge("router", "collection")

# After collection node, check if complete
def check_complete(state: State):
    if state.get("is_complete"):
        return "finalize"
    return END

workflow.add_conditional_edges("collection", check_complete)
workflow.add_edge("finalize", END)

app = workflow.compile()
