"""
Rubber Soul Beta - Backend API Server
FastAPI server with Claude API integration
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, List
import os
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic
import uuid
from datetime import datetime

# Load environment variables from project root
# Get the project root (parent of backend directory)
project_root = Path(__file__).parent.parent
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)

# Also try loading from current directory (for flexibility)
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Rubber Soul Beta API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Claude client
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
if not anthropic_api_key:
    raise ValueError(
        f"ANTHROPIC_API_KEY not found in environment variables. "
        f"Checked .env file at: {env_path}. "
        f"Make sure .env file exists in project root with ANTHROPIC_API_KEY=your_key"
    )

# Verify API key is loaded (show first 10 chars for debugging)
print(f"✅ Loaded API key from .env (starts with: {anthropic_api_key[:10]}...)")
print(f"✅ .env file location: {env_path}")

client = Anthropic(api_key=anthropic_api_key)

# Claude model configuration
# Try these model names in order if one fails:
# - claude-3-5-sonnet-20240620 (most recent)
# - claude-3-opus-20240229 (most capable)
# - claude-3-sonnet-20240229 (older but stable)
# - claude-3-haiku-20240307 (fastest)
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20240620")
FALLBACK_MODELS = [
    "claude-3-5-sonnet-20240620",
    "claude-3-opus-20240229", 
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307"
]

# In-memory storage (use database in production)
conversations: Dict[str, Dict] = {}
sessions: Dict[str, Dict] = {}


# Pydantic models
class ConversationCreate(BaseModel):
    pass


class MessageSend(BaseModel):
    conversation_id: str
    content: str
    ai_mode: str = "claude"


class ConversationResponse(BaseModel):
    conversation_id: str
    success: bool


class MessageResponse(BaseModel):
    success: bool
    assistant_message: str
    conversation_id: str


# Load Rubber Soul system prompt
def load_rubber_soul_prompt() -> str:
    """Load the Rubber Soul Beta system prompt"""
    # Try multiple paths
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "..", "RUBBERSOUL-BETA.txt"),
        os.path.join(os.path.dirname(__file__), "..", "RUBBERSOUL-BETA.txt"),
        "RUBBERSOUL-BETA.txt",
        "../RUBBERSOUL-BETA.txt"
    ]
    
    for path in possible_paths:
        try:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    return f.read()
        except Exception:
            continue
    
    # Fallback if file not found
    return """RUBBER SOUL BETA – The Trust Architecture Engine
AI-Assisted. Human-Souled.
Refined over 7M+ impressions, 16 craft dimensions, 14 trust patterns.
Created by Stephen Klein | Curiouser.AI"""


RUBBER_SOUL_SYSTEM_PROMPT = load_rubber_soul_prompt()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Rubber Soul Beta API"}


@app.post("/api/conversations/create", response_model=ConversationResponse)
async def create_conversation():
    """Create a new conversation"""
    conversation_id = str(uuid.uuid4())
    
    conversations[conversation_id] = {
        "id": conversation_id,
        "created_at": datetime.now().isoformat(),
        "messages": [],
        "session": {
            "platform": None,
            "mode": None,
            "topic": None,
            "angle": None,
            "hook": None,
            "intensity": 2,
            "footnotes": "ON",
            "draft_version": 0
        }
    }
    
    return ConversationResponse(
        conversation_id=conversation_id,
        success=True
    )


@app.post("/api/messages/send", response_model=MessageResponse)
async def send_message(message: MessageSend):
    """Send a message and get AI response"""
    
    if message.conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    conversation = conversations[message.conversation_id]
    
    # Add user message to conversation
    conversation["messages"].append({
        "role": "user",
        "content": message.content,
        "timestamp": datetime.now().isoformat()
    })
    
    # Prepare messages for Claude
    messages = []
    for msg in conversation["messages"]:
        messages.append({
            "role": msg["role"],
            "content": msg["content"]
        })
    
    # Try the configured model first, then fallback models
    models_to_try = [CLAUDE_MODEL] + [m for m in FALLBACK_MODELS if m != CLAUDE_MODEL]
    last_error = None
    
    for model_name in models_to_try:
        try:
            # Call Claude API
            response = client.messages.create(
                model=model_name,
                max_tokens=4096,
                system=RUBBER_SOUL_SYSTEM_PROMPT,
                messages=messages
            )
            
            assistant_message = response.content[0].text
            
            # Add assistant message to conversation
            conversation["messages"].append({
                "role": "assistant",
                "content": assistant_message,
                "timestamp": datetime.now().isoformat()
            })
            
            return MessageResponse(
                success=True,
                assistant_message=assistant_message,
                conversation_id=message.conversation_id
            )
        
        except Exception as e:
            last_error = e
            error_str = str(e)
            # If it's a 404 (model not found), try next model
            if "404" in error_str or "not_found" in error_str.lower():
                continue
            # For other errors, raise immediately
            else:
                raise HTTPException(status_code=500, detail=f"Error calling Claude API: {str(e)}")
    
    # If all models failed with 404
    raise HTTPException(
        status_code=500, 
        detail=f"Error calling Claude API: All models failed. Last error: {str(last_error)}. "
               f"Please check your API key has access to Claude models. "
               f"Tried models: {', '.join(models_to_try)}"
    )


@app.get("/api/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get conversation history"""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return conversations[conversation_id]


@app.get("/api/conversations/{conversation_id}/session")
async def get_session(conversation_id: str):
    """Get session state"""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return conversations[conversation_id]["session"]


@app.put("/api/conversations/{conversation_id}/session")
async def update_session(conversation_id: str, session_data: Dict):
    """Update session state"""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    conversations[conversation_id]["session"].update(session_data)
    return {"success": True, "session": conversations[conversation_id]["session"]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

