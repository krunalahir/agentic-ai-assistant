import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uuid
import os
import tempfile
import shutil
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel
from backend.langraph_database import workflow, retrive_all_thread
from langchain_core.messages import BaseMessage, HumanMessage
from rag.rag_tool import get_rag_system, is_rag_ready, initialize_rag_from_saved
import asyncio
from dotenv import load_dotenv
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    ToolMessage,
)

# Load environment variables from config folder
env_path = Path(__file__).parent.parent.parent / "config" / ".env"
load_dotenv(env_path)

app = FastAPI(title="Agentic AI Assistant API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Vector store path in data folder
VECTOR_STORE_PATH = str(Path(__file__).parent.parent.parent / "data" / "vector_store")

# Initialize RAG system from saved state if it exists
if os.path.exists(VECTOR_STORE_PATH):
    initialize_rag_from_saved(VECTOR_STORE_PATH)


class ChatRequest(BaseModel):
    message: str
    thread_id: str


class ChatResponse(BaseModel):
    response: str
    thread_id: str


class ThreadSummary(BaseModel):
    thread_id: str
    summary: str


class Message(BaseModel):
    role: str
    content: str


class ConversationResponse(BaseModel):
    messages: List[Message]


@app.get("/")
async def serve_index():
    """Serve the main HTML file"""
    return FileResponse("static/index.html")


@app.post("/api/thread", response_model=ThreadSummary)
async def create_thread():
    """Create a new chat thread"""
    thread_id = str(uuid.uuid4())
    return ThreadSummary(thread_id=thread_id, summary="New Chat")


@app.get("/api/thread", response_model=List[ThreadSummary])
async def get_all_threads():
    """Get all conversation threads"""
    try:
        threads = retrive_all_thread()
        thread_summaries = []
        
        for thread_id in threads:
            summary = get_thread_summary(thread_id)
            thread_summaries.append(ThreadSummary(thread_id=thread_id, summary=summary))
        
        return thread_summaries
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#@app.get("/api/thread/{thread_id}", response_model=ConversationResponse)
#async def get_thread_messages(thread_id: str):
    """Get messages for a specific thread"""
    try:
        messages = workflow.get_state(config={'configurable': {'thread_id': thread_id}}).values['messages']
        formatted_messages = []
        
        for message in messages:
            if isinstance(message, HumanMessage):
                role = 'user'
            else:
                role = 'assistant'
            
            content = message.content if hasattr(message, 'content') else str(message)
            formatted_messages.append(Message(role=role, content=content))
        
        return ConversationResponse(messages=formatted_messages)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/api/thread/{thread_id}", response_model=ConversationResponse)
async def get_thread_messages(thread_id: str):

    """Get only user-visible conversation."""
    try:
        state = workflow.get_state(
            config={"configurable": {"thread_id": thread_id}}
        )
        messages = state.values.get("messages", [])

        formatted_messages = []
        for message in messages:
            # User messages
            if isinstance(message, HumanMessage):
                # Hide internal worker reports
                if message.content.startswith("WORKER REPORT:"):
                    continue
                formatted_messages.append(
                    Message(
                        role="user",
                        content=message.content,
                    )

                )
            # Assistant messages

            elif isinstance(message, AIMessage):
                # Ignore AI messages that only call tools
                if getattr(message, "tool_calls", None):
                    continue
                if not message.content:
                    continue
                formatted_messages.append(
                    Message(
                        role="assistant",
                        content=message.content,
                    )
                )

            # Hide tool outputs
            elif isinstance(message, ToolMessage):
                continue
        return ConversationResponse(messages=formatted_messages)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a message and get AI response"""
    try:
        CONFIG = {'configurable': {'thread_id': request.thread_id}}
        
        # Use invoke instead of stream for more reliable response capturing
        result = workflow.invoke(
            {'messages': [HumanMessage(content=request.message)]},
            config=CONFIG
        )
        
        # The last message should be the AI's response
        messages = result.get('messages', [])
        ai_response = "I couldn't generate a response. Please try again."
        
        if messages:
            last_msg = messages[-1]
            if hasattr(last_msg, 'content'):
                ai_response = last_msg.content
            else:
                ai_response = str(last_msg)
        
        return ChatResponse(response=ai_response, thread_id=request.thread_id)
    except Exception as e:
        print(f"Error in /api/chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/rag/status")
async def get_rag_status():
    """Get RAG system status"""
    status = is_rag_ready()
    return {"ready": status}


@app.post("/api/rag/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a PDF document for RAG"""
    try:
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name

        # Initialize RAG system
        rag = get_rag_system()

        # Load and process document
        rag.load_documents(tmp_path)

        # Save vector store to data folder
        rag.save_vector_store(VECTOR_STORE_PATH)

        # Clean up temporary file
        os.unlink(tmp_path)
        
        return {"success": True, "message": f'Document "{file.filename}" processed successfully'}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_thread_summary(thread_id: str) -> str:
    """Generate a quick summary from the conversation without LLM overhead"""
    try:
        state = workflow.get_state(config={'configurable': {'thread_id': thread_id}})
        messages = state.values.get('messages', [])
        if messages:
            # Find the first user message
            for message in messages:
                if isinstance(message, HumanMessage):
                    content = message.content if hasattr(message, 'content') else str(message)
                    # Simple first 3-4 words for the sidebar
                    words = content.split()
                    summary = " ".join(words[:4])
                    if len(words) > 4:
                        summary += "..."
                    return summary
        return "New Chat"
    except Exception as e:
        return "New Chat"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
