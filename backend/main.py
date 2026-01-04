from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import ChatRequest, ChatResponse, PatientData
from graph import app as graph_app
from langchain_core.messages import HumanMessage
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Hospital Receptionist AI Backend is running"}

# In-memory storage for graph state (For demo purposes - production would use persistent Checkpointer)
# Since requirements asked for conversation keyed by session_id, we'll maintain state manually via the graph input/output 
# OR use a simple dictionary to hold the accumulated thread state if LangGraph checkpointer isn't set up (simplest for 'minimal' req).
session_store = {}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    session_id = request.session_id
    user_message = request.message

    # Retrieve existing state or initialize
    if session_id not in session_store:
        initial_state = {
            "messages": [],
            "patient_data": PatientData(),
            "ward": None,
            "missing_field": None,
            "is_complete": False,
            "db_written": False
        }
        session_store[session_id] = initial_state
    
    current_state = session_store[session_id]
    
    # Add user message to state
    current_state["messages"].append(HumanMessage(content=user_message))

    # Run Graph
    # We invoke with the current state. The graph will process and return the NEW state.
    # Note: For production, we'd use 'thread_id' in config, but passing full state works for simple stateless-server model.
    final_state = await graph_app.ainvoke(current_state)
    
    # Update store
    session_store[session_id] = final_state
    
    # Get last AI message
    last_message = final_state["messages"][-1]
    
    return ChatResponse(reply=last_message.content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
