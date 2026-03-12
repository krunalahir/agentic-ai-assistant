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
from rag.rag_tool import get_rag_system, is_rag_ready
import asyncio
from dotenv import load_dotenv

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


@app.get("/api/thread/{thread_id}", response_model=ConversationResponse)
async def get_thread_messages(thread_id: str):
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


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a message and get AI response"""
    try:
        CONFIG = {'configurable': {'thread_id': request.thread_id}}
        
        # Stream AI response
        response_chunks = []
        for message_chunks, metadata in workflow.stream(
            {'messages': [HumanMessage(content=request.message)]},
            config=CONFIG,
            stream_mode='messages'
        ):
            if hasattr(message_chunks, 'content'):
                response_chunks.append(message_chunks.content)
        
        ai_response = "".join(response_chunks)
        
        return ChatResponse(response=ai_response, thread_id=request.thread_id)
    except Exception as e:
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
    """Generate a meaningful summary from the conversation"""
    try:
        messages = workflow.get_state(config={'configurable': {'thread_id': thread_id}}).values['messages']
        if messages:
            # Find the first user message
            for message in messages:
                if isinstance(message, HumanMessage):
                    content = message.content if hasattr(message, 'content') else str(message)
                    # Use LLM to generate a meaningful summary
                    from langchain_mistralai.chat_models import ChatMistralAI
                    llm = ChatMistralAI(model="mistral-small-latest", api_key=os.getenv("MISTRAL_API_KEY"))
                    prompt = f"Create a concise 2-3 word title for this conversation topic: '{content}'. Return only the title, no quotes or explanation."
                    response = llm.invoke(prompt)
                    summary = response.content.strip().strip('"').strip("'")
                    # Limit to 3 words max
                    words = summary.split()[:3]
                    return ' '.join(words)
        return "New Chat"
    except Exception as e:
        try:
            messages = workflow.get_state(config={'configurable': {'thread_id': thread_id}}).values['messages']
            if messages:
                for message in messages:
                    if isinstance(message, HumanMessage):
                        content = message.content if hasattr(message, 'content') else str(message)
                        words = content.split()[:3]
                        return ' '.join(words) + ('...' if len(content.split()) > 3 else '')
        except:
            pass
        return "New Chat"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
