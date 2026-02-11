# Updated: Dynamic Groq model support
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import asyncio
from typing import List, Optional
import json
import uuid
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import our custom modules
from services.groq_service import GroqService
from services.pdf_processor import PDFProcessor
from services.web_search import WebSearchService
from services.vector_store import VectorStore
from services.rag_engine import RAGEngine

app = FastAPI(title="Edu Assist API", description="AI-powered educational chatbot with RAG capabilities")

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (your existing frontend)
import os
from fastapi.responses import RedirectResponse
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
print(f"Static directory: {static_dir}")
print(f"Static directory exists: {os.path.exists(static_dir)}")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Initialize services
groq_service = GroqService()
pdf_processor = PDFProcessor()
web_search = WebSearchService()
vector_store = VectorStore()
rag_engine = RAGEngine(groq_service, vector_store, web_search)

# Pydantic models for request/response
class SourceInfo(BaseModel):
    type: str
    source: str
    url: Optional[str] = None

class ChatMessage(BaseModel):
    message: str
    subject: Optional[str] = None
    topic: Optional[str] = None
    eli5_mode: Optional[bool] = False
    session_id: Optional[str] = None
    conversation_history: Optional[List[dict]] = []

class ChatResponse(BaseModel):
    response: str
    sources: List[SourceInfo] = []  # Use proper source model
    session_id: str
    timestamp: str

class DocumentUpload(BaseModel):
    filename: str
    subject: Optional[str] = None

# In-memory storage for sessions (in production, use a database)
chat_sessions = {}

@app.get("/")
async def root():
    # Redirect to the login page
    return RedirectResponse(url="/static/login.html")

@app.get("/health")
def health():
    """Simple health check endpoint"""
    return {"status": "ok", "message": "Edu Assist API is running"}

@app.get("/api/health")
def api_health():
    """Alternative health check endpoint"""
    return {"status": "ok", "message": "Edu Assist API is healthy"}

# Debug: Print registered routes
@app.on_event("startup")
async def startup_event():
    print("🚀 Edu Assist API starting up...")
    print("📋 Registered routes:")
    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path_regex'):
            methods = getattr(route, 'methods', [])
            path = getattr(route, 'path', 'unknown')
            print(f"   {list(methods) if methods else 'ALL'} {path}")
    print("✅ Startup complete!")

@app.get("/api/test")
async def test_rag():
    """Test endpoint to verify RAG system is working"""
    try:
        # Test with a simple query
        test_response = await rag_engine.get_response(
            query="What is mathematics?",
            subject="Math",
            eli5_mode=False,
            chat_history=[]
        )
        return {
            "status": "success",
            "message": "RAG system is working",
            "test_response": test_response["response"][:100] + "..." if len(test_response["response"]) > 100 else test_response["response"],
            "sources_count": len(test_response.get("sources", []))
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"RAG system error: {str(e)}"
        }

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(chat_request: ChatMessage):
    """
    Main chat endpoint that handles user messages and returns AI responses
    """
    try:
        # Generate session ID if not provided
        session_id = chat_request.session_id or str(uuid.uuid4())
        
        # Initialize session if new
        if session_id not in chat_sessions:
            chat_sessions[session_id] = {
                "messages": [],
                "subject": chat_request.subject or "General",
                "created_at": datetime.now().isoformat()
            }
        
        # Add user message to session
        chat_sessions[session_id]["messages"].append({
            "role": "user",
            "content": chat_request.message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Get AI response using RAG engine
        response_data = await rag_engine.get_response(
            query=chat_request.message,
            subject=chat_request.subject,
            eli5_mode=chat_request.eli5_mode or False,
            chat_history=chat_sessions[session_id]["messages"][-10:]  # Last 10 messages for context
        )
        
        # Convert sources to SourceInfo objects
        sources = []
        for source_dict in response_data.get("sources", []):
            sources.append(SourceInfo(
                type=source_dict.get("type", "unknown"),
                source=source_dict.get("source", ""),
                url=source_dict.get("url")
            ))
        
        # Add AI response to session
        chat_sessions[session_id]["messages"].append({
            "role": "assistant",
            "content": response_data["response"],
            "sources": response_data.get("sources", []),
            "timestamp": datetime.now().isoformat()
        })
        
        return ChatResponse(
            response=response_data["response"],
            sources=sources,  # Use converted SourceInfo objects
            session_id=session_id,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        print(f"Chat endpoint error: {str(e)}")  # Debug logging
        # Return a more helpful error response instead of raising HTTP exception
        return ChatResponse(
            response=f"I'm having technical difficulties right now. Error: {str(e)}. Please try asking a simpler question.",
            sources=[],
            session_id=session_id or "error",
            timestamp=datetime.now().isoformat()
        )

@app.post("/api/upload-document")
async def upload_document(file: UploadFile = File(...), subject: str = "General"):
    """
    Upload and process PDF documents for the knowledge base
    """
    try:
        if not file.filename or not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Save uploaded file temporarily
        temp_file_path = f"temp_{uuid.uuid4()}_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Process PDF and extract chunks
        chunks = await pdf_processor.process_pdf(temp_file_path, subject)
        
        # Store chunks in vector database
        document_id = await vector_store.store_document_chunks(
            chunks=chunks,
            filename=file.filename or "unknown.pdf",
            subject=subject
        )
        
        # Clean up temporary file
        os.remove(temp_file_path)
        
        return {
            "message": f"Successfully processed {file.filename}",
            "document_id": document_id,
            "chunks_count": len(chunks),
            "subject": subject
        }
        
    except Exception as e:
        # Clean up temp file if it exists
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")

@app.get("/api/documents")
async def list_documents():
    """
    List all uploaded documents
    """
    try:
        documents = await vector_store.list_documents()
        return {"documents": documents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing documents: {str(e)}")

@app.delete("/api/documents/{document_id}")
async def delete_document(document_id: str):
    """
    Delete a document and its chunks from the knowledge base
    """
    try:
        success = await vector_store.delete_document(document_id)
        if success:
            return {"message": "Document deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Document not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting document: {str(e)}")

@app.get("/api/chat-history/{session_id}")
async def get_chat_history(session_id: str):
    """
    Get chat history for a specific session
    """
    if session_id not in chat_sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return chat_sessions[session_id]

@app.get("/api/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "services": {
            "groq": await groq_service.health_check(),
            "vector_store": await vector_store.health_check(),
            "web_search": await web_search.health_check()
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
