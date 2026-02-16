# Updated: Dynamic Groq model support
from fastapi import FastAPI, UploadFile, File, HTTPException, Request, Depends
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

# Load environment variables from backend/.env (relative to this file)
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# Import our custom modules
from services.groq_service import GroqService
from services.pdf_processor import PDFProcessor
from services.web_search import WebSearchService
from services.vector_store import VectorStore
from services.rag_engine import RAGEngine
from services import course_manager
from services import quiz_manager
from services import auth_service
from services import reporting_service
from services import twofa_service
from services.security import (
    AuditLoggingMiddleware,
    RateLimitMiddleware,
    SecurityHeadersMiddleware,
    sanitize_string,
    sanitize_username,
    sanitize_email,
    can_access_document,
    get_request_log,
    get_security_stats,
)

app = FastAPI(title="Edu Assist Pro API", description="AI-powered corporate training platform with RAG capabilities")

# ─── Middleware stack (order matters: outermost first) ────────────────────────
# Security headers on every response
app.add_middleware(SecurityHeadersMiddleware)
# Rate limiting (before audit so 429s are fast)
app.add_middleware(RateLimitMiddleware)
# Audit logging for all /api/* requests
app.add_middleware(AuditLoggingMiddleware)

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

class EnrollRequest(BaseModel):
    user_id: str = "default_user"

class ModuleProgressRequest(BaseModel):
    user_id: str = "default_user"
    module_id: str
    course_id: str
    status: str = "completed"
    score: Optional[float] = None

class QuizSubmitRequest(BaseModel):
    user_id: str = "default_user"
    quiz_id: str
    answers: dict = {}
    time_spent_seconds: int = 0

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    name: str = ""
    role: str = "trainee"
    department: str = ""

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    department: Optional[str] = None
    is_active: Optional[bool] = None

class TwoFAVerifyRequest(BaseModel):
    temp_token: str
    challenge_id: str
    code: str

class TwoFASetupRequest(BaseModel):
    method: str = "authenticator"

class TwoFASendCodeRequest(BaseModel):
    temp_token: str
    method: str

# ─── Auth dependency ──────────────────────────────────────────────────────────

def get_current_user(request: Request) -> Optional[dict]:
    """Extract and verify JWT from Authorization header. Returns payload or None."""
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        token = auth[7:]
        payload = auth_service.verify_token(token)
        return payload
    return None

def require_auth(request: Request) -> dict:
    """Same as get_current_user but raises 401 if missing."""
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user

def require_role(*roles):
    """Returns a dependency that checks the user has one of the specified roles."""
    def checker(request: Request):
        user = require_auth(request)
        if user.get("role") not in roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return checker

# In-memory storage for sessions (in production, use a database)
chat_sessions = {}

@app.get("/")
async def root():
    # Redirect to the login page
    return RedirectResponse(url="/static/login.html")

@app.get("/health")
def health():
    """Simple health check endpoint"""
    return {"status": "ok", "message": "Edu Assist Pro API is running"}

@app.get("/api/health")
def api_health():
    """Alternative health check endpoint"""
    return {"status": "ok", "message": "Edu Assist Pro API is healthy"}

# Debug: Print registered routes
@app.on_event("startup")
async def startup_event():
    print("🚀 Edu Assist Pro API starting up...")
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
async def chat_endpoint(chat_request: ChatMessage, user=Depends(require_auth)):
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
async def upload_document(file: UploadFile = File(...), subject: str = "General", user=Depends(require_role("admin", "instructor"))):
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
async def list_documents(request: Request):
    """
    List all uploaded documents. Requires authentication.
    Admins/instructors see all; others see view-only metadata.
    """
    user = get_current_user(request)
    role = user.get("role", "trainee") if user else "trainee"

    if not can_access_document(role, "view"):
        raise HTTPException(status_code=403, detail="You do not have permission to view documents")

    try:
        documents = await vector_store.list_documents()
        return {"documents": documents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing documents: {str(e)}")

@app.delete("/api/documents/{document_id}")
async def delete_document(document_id: str, user=Depends(require_role("admin", "instructor"))):
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

# ─── COURSE & CURRICULUM ENDPOINTS ──────────────────────────────────────────

@app.get("/api/courses")
async def list_courses():
    """Return all available courses with module counts."""
    try:
        courses = course_manager.get_all_courses()
        return {"courses": courses}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching courses: {str(e)}")

@app.get("/api/courses/{course_id}")
async def get_course(course_id: str):
    """Return a single course with its modules."""
    try:
        course = course_manager.get_course(course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        return course
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching course: {str(e)}")

@app.post("/api/courses/{course_id}/enroll")
async def enroll_in_course(course_id: str, req: EnrollRequest, user=Depends(require_auth)):
    """Enroll a user in a course."""
    try:
        course = course_manager.get_course(course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        result = course_manager.enroll_user(req.user_id, course_id)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error enrolling: {str(e)}")

@app.get("/api/enrollments/{user_id}")
async def get_enrollments(user_id: str):
    """Get all course enrollments for a user."""
    try:
        enrollments = course_manager.get_user_enrollments(user_id)
        return {"enrollments": enrollments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching enrollments: {str(e)}")

@app.get("/api/enrollments/{user_id}/{course_id}")
async def get_enrollment(user_id: str, course_id: str):
    """Get enrollment status for a specific user + course."""
    try:
        enrollment = course_manager.get_enrollment(user_id, course_id)
        return {"enrollment": enrollment}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching enrollment: {str(e)}")

@app.post("/api/module-progress")
async def update_progress(req: ModuleProgressRequest, user=Depends(require_auth)):
    """Update a user's progress on a module."""
    try:
        result = course_manager.update_module_progress(
            user_id=req.user_id,
            module_id=req.module_id,
            course_id=req.course_id,
            status=req.status,
            score=req.score
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating progress: {str(e)}")

@app.get("/api/module-progress/{user_id}/{course_id}")
async def get_module_progress(user_id: str, course_id: str):
    """Get progress for all modules in a course for a user."""
    try:
        progress = course_manager.get_module_progress(user_id, course_id)
        return {"modules": progress}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching progress: {str(e)}")

# ─── ASSESSMENT / QUIZ ENDPOINTS ─────────────────────────────────────────────

@app.post("/api/quiz/generate/{course_id}")
async def generate_quiz(course_id: str, user=Depends(require_auth)):
    """Generate a quiz for a course using AI."""
    try:
        # Check if quiz already exists
        existing = quiz_manager.get_quiz_for_course(course_id)
        if existing:
            return existing

        # Get course info
        course = course_manager.get_course(course_id)
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        modules = course.get("modules", [])
        prompt = quiz_manager.build_quiz_prompt(course["title"], course["category"], modules)

        # Call Groq LLM to generate questions
        try:
            response_text = await groq_service.chat_completion(
                messages=[
                    {"role": "system", "content": "You are a corporate training quiz generator. Respond ONLY with valid JSON arrays."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=2048
            )
            questions = quiz_manager.parse_quiz_response(response_text)
        except Exception as e:
            print(f"LLM quiz generation failed: {e}, using fallback questions")
            questions = []

        if not questions:
            questions = quiz_manager.get_fallback_questions(course["title"], course["category"])

        result = quiz_manager.create_quiz_from_questions(course_id, course["title"], questions)
        # Return the full quiz
        return quiz_manager.get_quiz_by_id(result["quiz_id"])

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating quiz: {str(e)}")

@app.get("/api/quiz/{course_id}")
async def get_quiz(course_id: str):
    """Get the quiz for a course (without correct answers for the frontend)."""
    try:
        quiz = quiz_manager.get_quiz_for_course(course_id)
        if not quiz:
            raise HTTPException(status_code=404, detail="No quiz found for this course. Generate one first.")

        # Strip correct answers and explanations for the taking UI
        safe_questions = []
        for q in quiz.get("questions", []):
            safe_questions.append({
                "id": q["id"],
                "question_text": q["question_text"],
                "question_type": q["question_type"],
                "options": q["options"],
                "points": q["points"],
                "order_index": q["order_index"]
            })
        quiz["questions"] = safe_questions
        return quiz

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching quiz: {str(e)}")

@app.post("/api/quiz/submit")
async def submit_quiz(req: QuizSubmitRequest, user=Depends(require_auth)):
    """Submit quiz answers and get graded results."""
    try:
        result = quiz_manager.grade_quiz(
            quiz_id=req.quiz_id,
            user_id=req.user_id,
            answers=req.answers,
            time_spent=req.time_spent_seconds
        )
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error grading quiz: {str(e)}")

@app.get("/api/results/{user_id}")
async def get_results(user_id: str):
    """Get quiz result history for a user."""
    try:
        results = quiz_manager.get_user_results(user_id)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching results: {str(e)}")

@app.get("/api/certificates/{user_id}")
async def get_certificates(user_id: str):
    """Get all certificates for a user."""
    try:
        certs = quiz_manager.get_user_certificates(user_id)
        return {"certificates": certs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching certificates: {str(e)}")

@app.get("/api/certificate/{cert_id}")
async def get_certificate(cert_id: str):
    """Get a single certificate."""
    try:
        cert = quiz_manager.get_certificate(cert_id)
        if not cert:
            raise HTTPException(status_code=404, detail="Certificate not found")
        return cert
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching certificate: {str(e)}")

# ─── AUTHENTICATION & AUTHORIZATION ENDPOINTS ────────────────────────────────

@app.post("/api/auth/login")
async def auth_login(req: LoginRequest):
    """Authenticate user and return JWT + user profile, or require 2FA."""
    result = auth_service.login(req.username, req.password)
    if "error" in result:
        raise HTTPException(status_code=401, detail=result["error"])

    # Check if 2FA is enabled for this user
    user = result["user"]
    twofa_settings = twofa_service.get_user_2fa_settings(user["id"])

    if twofa_settings["is_enabled"]:
        # Issue a temporary token (not a full auth token)
        temp_token = twofa_service.create_temp_token(user["id"], user["username"], user["role"])
        # Create a challenge for the preferred method
        challenge = twofa_service.create_challenge(user["id"], twofa_settings["preferred_method"])

        return {
            "requires_2fa": True,
            "temp_token": temp_token,
            "challenge_id": challenge["challenge_id"],
            "method": twofa_settings["preferred_method"],
            "instructions": challenge["instructions"],
            "demo_hint": challenge.get("demo_hint", ""),
            "available_methods": twofa_service.get_available_methods(),
            "user_preview": {
                "username": user["username"],
                "name": user["name"],
            },
        }

    # No 2FA — return token directly
    return result

@app.post("/api/auth/register")
async def auth_register(req: RegisterRequest):
    """Register a new user account."""
    # Sanitize inputs
    clean_username = sanitize_username(req.username)
    clean_email = sanitize_email(req.email)
    clean_name = sanitize_string(req.name, max_length=100)
    clean_dept = sanitize_string(req.department, max_length=100)

    if not clean_username:
        raise HTTPException(status_code=400, detail="Invalid username. Use alphanumeric, dots, hyphens, underscores.")
    if not clean_email:
        raise HTTPException(status_code=400, detail="Invalid email address.")
    if len(req.password) < 3:
        raise HTTPException(status_code=400, detail="Password must be at least 3 characters.")

    result = auth_service.register_user(
        username=clean_username,
        email=clean_email,
        password=req.password,
        name=clean_name,
        role=req.role,
        department=clean_dept,
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# ─── TWO-FACTOR AUTHENTICATION ENDPOINTS ─────────────────────────────────────

@app.post("/api/auth/2fa/verify")
async def twofa_verify(req: TwoFAVerifyRequest):
    """Verify a 2FA code and return the real auth token."""
    # Validate the temp token
    payload = twofa_service.verify_temp_token(req.temp_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired 2FA session. Please login again.")

    # Verify the challenge code
    result = twofa_service.verify_challenge(req.challenge_id, req.code)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    # 2FA passed — issue a full auth token
    user_id = payload["sub"]
    username = payload["username"]
    role = payload["role"]
    token = auth_service.create_token(user_id, username, role)
    user = auth_service.get_user_safe(user_id)

    return {"token": token, "user": user}


@app.post("/api/auth/2fa/send-code")
async def twofa_send_code(req: TwoFASendCodeRequest):
    """Send / resend a 2FA code via a different method."""
    payload = twofa_service.verify_temp_token(req.temp_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired 2FA session. Please login again.")

    challenge = twofa_service.create_challenge(payload["sub"], req.method)
    return challenge


@app.get("/api/auth/2fa/methods")
async def twofa_methods():
    """Get available 2FA methods."""
    return {"methods": twofa_service.get_available_methods()}


@app.get("/api/auth/2fa/settings")
async def twofa_get_settings(user=Depends(require_auth)):
    """Get current user's 2FA settings."""
    settings = twofa_service.get_user_2fa_settings(user["sub"])
    return settings


@app.post("/api/auth/2fa/enable")
async def twofa_enable(req: TwoFASetupRequest, user=Depends(require_auth)):
    """Enable 2FA for the current user."""
    result = twofa_service.enable_2fa(user["sub"], req.method)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.post("/api/auth/2fa/disable")
async def twofa_disable(user=Depends(require_auth)):
    """Disable 2FA for the current user."""
    result = twofa_service.disable_2fa(user["sub"])
    return result


@app.get("/api/admin/2fa/stats")
async def admin_2fa_stats(user=Depends(require_role("admin", "manager"))):
    """Get 2FA adoption statistics (admin/manager only)."""
    return twofa_service.get_all_2fa_stats()


@app.post("/api/admin/2fa/enable/{user_id}")
async def admin_enable_user_2fa(user_id: str, req: TwoFASetupRequest, user=Depends(require_role("admin"))):
    """Admin: Enable 2FA for a specific user."""
    result = twofa_service.admin_enable_2fa_for_user(user_id, req.method)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@app.post("/api/admin/2fa/disable/{user_id}")
async def admin_disable_user_2fa(user_id: str, user=Depends(require_role("admin"))):
    """Admin: Disable 2FA for a specific user."""
    return twofa_service.admin_disable_2fa_for_user(user_id)


@app.get("/api/admin/2fa/status/{user_id}")
async def admin_get_user_2fa_status(user_id: str, user=Depends(require_role("admin", "manager"))):
    """Get 2FA settings for a specific user (admin/manager only)."""
    return twofa_service.get_user_2fa_settings(user_id)

@app.get("/api/auth/me")
async def auth_me(user=Depends(require_auth)):
    """Get the currently authenticated user profile."""
    profile = auth_service.get_user_safe(user["sub"])
    if "error" in profile:
        raise HTTPException(status_code=404, detail=profile["error"])
    return profile

@app.post("/api/auth/change-password")
async def auth_change_password(req: ChangePasswordRequest, user=Depends(require_auth)):
    """Change the current user's password."""
    result = auth_service.change_password(user["sub"], req.old_password, req.new_password)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

# ─── ADMIN USER MANAGEMENT ENDPOINTS ─────────────────────────────────────────

@app.get("/api/admin/users")
async def admin_list_users(role: Optional[str] = None, user=Depends(require_role("admin", "manager"))):
    """List all users (admin/manager only)."""
    users = auth_service.list_users(role)
    return {"users": users}

@app.get("/api/admin/users/{user_id}")
async def admin_get_user(user_id: str, user=Depends(require_role("admin", "manager"))):
    """Get a specific user profile (admin/manager only)."""
    profile = auth_service.get_user_safe(user_id)
    if "error" in profile:
        raise HTTPException(status_code=404, detail=profile["error"])
    return profile

@app.put("/api/admin/users/{user_id}")
async def admin_update_user(user_id: str, req: UpdateUserRequest, user=Depends(require_role("admin"))):
    """Update a user's profile (admin only)."""
    result = auth_service.update_user(user_id, **req.dict(exclude_none=True))
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.delete("/api/admin/users/{user_id}")
async def admin_deactivate_user(user_id: str, user=Depends(require_role("admin"))):
    """Deactivate a user (admin only). Soft delete."""
    return auth_service.delete_user(user_id)

@app.get("/api/admin/audit-log")
async def admin_audit_log(user_id: Optional[str] = None, limit: int = 50, user=Depends(require_role("admin"))):
    """View audit log entries (admin only)."""
    return {"log": auth_service.get_audit_log(user_id, limit)}

# ─── REPORTING & ANALYTICS ENDPOINTS ─────────────────────────────────────────

@app.get("/api/reports/team-overview")
async def report_team_overview(user=Depends(require_role("admin", "manager"))):
    """Team completion overview for managers/admins."""
    return reporting_service.get_team_overview()

@app.get("/api/reports/score-distribution")
async def report_score_distribution(user=Depends(require_role("admin", "manager"))):
    """Assessment score distribution across all users."""
    return reporting_service.get_score_distribution()

@app.get("/api/reports/compliance")
async def report_compliance(user=Depends(require_role("admin", "manager"))):
    """Compliance status for mandatory courses."""
    return reporting_service.get_compliance_report()

@app.get("/api/reports/export/team")
async def export_team(user=Depends(require_role("admin", "manager"))):
    """Export team overview as CSV."""
    from fastapi.responses import Response
    csv_data = reporting_service.export_team_csv()
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=team_overview.csv"}
    )

@app.get("/api/reports/export/scores")
async def export_scores(user=Depends(require_role("admin", "manager"))):
    """Export quiz scores as CSV."""
    from fastapi.responses import Response
    csv_data = reporting_service.export_scores_csv()
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=assessment_scores.csv"}
    )

@app.get("/api/reports/export/compliance")
async def export_compliance(user=Depends(require_role("admin", "manager"))):
    """Export compliance report as CSV."""
    from fastapi.responses import Response
    csv_data = reporting_service.export_compliance_csv()
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=compliance_report.csv"}
    )

# ─── SECURITY ADMIN ENDPOINTS ─────────────────────────────────────────────────

@app.get("/api/admin/security/stats")
async def admin_security_stats(user=Depends(require_role("admin"))):
    """Security statistics for today (admin only)."""
    return get_security_stats()

@app.get("/api/admin/security/request-log")
async def admin_request_log(
    limit: int = 100,
    method: Optional[str] = None,
    path: Optional[str] = None,
    user_id: Optional[str] = None,
    user=Depends(require_role("admin")),
):
    """Query request audit log (admin only)."""
    return {"log": get_request_log(limit=limit, method=method, path_contains=path, user_id=user_id)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
