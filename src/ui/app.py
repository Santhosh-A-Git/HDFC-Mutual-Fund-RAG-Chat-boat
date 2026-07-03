import sys
import os
# pyrefly: ignore [missing-import]
from fastapi import FastAPI, HTTPException
# pyrefly: ignore [missing-import]
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Ensure we can import from src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.rag.intent import classify_intent, get_refusal_message
from src.rag.engine import ask_question

app = FastAPI(title="HDFC Mutual Fund Assistant API")

# Configure CORS for Vercel Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace "*" with your Vercel URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
        
    try:
        # 1. Classify Intent
        intent = classify_intent(query)
        
        # 2. Route based on intent
        if intent == "ADVISORY":
            answer = get_refusal_message()
        else:
            answer = ask_question(query)
            
        return ChatResponse(response=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "HDFC Mutual Fund Assistant API is running!"}

if __name__ == "__main__":
    # pyrefly: ignore [missing-import]
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
