"""
Security Hardening Module
- Audit logging middleware (every request → audit_log)
- Rate limiting (login/register brute-force protection)
- Security headers middleware
- Input sanitization helpers
- Document access control per role
"""

import os
import re
import time
import sqlite3
import html
from collections import defaultdict
from datetime import datetime, timezone
from typing import Optional

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

# ─── Config ──────────────────────────────────────────────────────────────────

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "courses.db")

# Rate-limit settings (per IP)
RATE_LIMIT_WINDOW = 60        # seconds
LOGIN_MAX_ATTEMPTS = 10       # max login attempts per window
REGISTER_MAX_ATTEMPTS = 5     # max register attempts per window
GENERAL_MAX_REQUESTS = 200    # max total requests per window

# Paths that should be audit-logged (regex patterns)
AUDIT_PATHS = re.compile(r"^/api/")

# Paths exempt from rate limiting (static assets, health)
RATE_EXEMPT = re.compile(r"^/(static|health|favicon)")

# ─── DB helpers ──────────────────────────────────────────────────────────────

def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def _ensure_tables():
    """Ensure audit tables exist with the right schema."""
    conn = _conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS request_log (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            method     TEXT NOT NULL,
            path       TEXT NOT NULL,
            status     INTEGER DEFAULT 0,
            user_id    TEXT DEFAULT '',
            username   TEXT DEFAULT '',
            role       TEXT DEFAULT '',
            ip_address TEXT DEFAULT '',
            user_agent TEXT DEFAULT '',
            duration_ms REAL DEFAULT 0,
            created_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_request_log_created ON request_log(created_at);
        CREATE INDEX IF NOT EXISTS idx_request_log_user    ON request_log(user_id);
    """)
    conn.commit()
    conn.close()


_ensure_tables()


# ─── Rate Limiter (in-memory, per-IP) ────────────────────────────────────────

class RateLimiter:
    """Simple sliding-window rate limiter keyed by IP address."""

    def __init__(self):
        # { ip: [(timestamp, path_bucket), ...] }
        self._hits: dict[str, list] = defaultdict(list)

    def _cleanup(self, ip: str):
        cutoff = time.time() - RATE_LIMIT_WINDOW
        self._hits[ip] = [h for h in self._hits[ip] if h[0] > cutoff]

    def check(self, ip: str, path: str) -> Optional[str]:
        """
        Returns an error message if rate limited, else None.
        """
        self._cleanup(ip)
        hits = self._hits[ip]

        # Count by bucket
        login_count = sum(1 for _, p in hits if p == "login")
        register_count = sum(1 for _, p in hits if p == "register")
        total_count = len(hits)

        # Determine bucket for this request
        bucket = "general"
        if "/api/auth/login" in path:
            bucket = "login"
            if login_count >= LOGIN_MAX_ATTEMPTS:
                return f"Too many login attempts. Try again in {RATE_LIMIT_WINDOW}s."
        elif "/api/auth/register" in path:
            bucket = "register"
            if register_count >= REGISTER_MAX_ATTEMPTS:
                return f"Too many registration attempts. Try again in {RATE_LIMIT_WINDOW}s."

        if total_count >= GENERAL_MAX_REQUESTS:
            return f"Rate limit exceeded ({GENERAL_MAX_REQUESTS} req/{RATE_LIMIT_WINDOW}s)."

        # Record this hit
        self._hits[ip].append((time.time(), bucket))
        return None


_rate_limiter = RateLimiter()


# ─── Audit Logging Middleware ─────────────────────────────────────────────────

class AuditLoggingMiddleware(BaseHTTPMiddleware):
    """
    Logs every /api/* request to the request_log table.
    Records: method, path, response status, user info (from JWT), IP, UA, duration.
    """

    async def dispatch(self, request: Request, call_next):
        start = time.time()
        path = request.url.path

        # Skip non-API and static requests
        if not AUDIT_PATHS.match(path):
            return await call_next(request)

        # Extract user info from JWT if present
        user_id = ""
        username = ""
        role = ""
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            try:
                import jwt as _jwt
                token = auth_header[7:]
                secret = os.getenv("JWT_SECRET", "edu-assist-pro-secret-change-in-prod-2026")
                payload = _jwt.decode(token, secret, algorithms=["HS256"])
                user_id = payload.get("sub", "")
                username = payload.get("username", "")
                role = payload.get("role", "")
            except Exception:
                pass

        # Call the actual endpoint
        response = await call_next(request)
        duration_ms = (time.time() - start) * 1000

        # Async-safe: write log in a non-blocking way
        ip = request.client.host if request.client else ""
        ua = request.headers.get("User-Agent", "")[:200]

        try:
            conn = _conn()
            conn.execute(
                """INSERT INTO request_log
                   (method, path, status, user_id, username, role, ip_address, user_agent, duration_ms, created_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (
                    request.method,
                    path,
                    response.status_code,
                    user_id,
                    username,
                    role,
                    ip,
                    ua,
                    round(duration_ms, 2),
                    datetime.now(timezone.utc).isoformat(),
                ),
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[audit-log] Error writing request log: {e}")

        return response


# ─── Rate Limiting Middleware ─────────────────────────────────────────────────

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Applies rate limiting per IP.  Returns 429 if limit exceeded.
    """

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Skip static assets and health checks
        if RATE_EXEMPT.match(path):
            return await call_next(request)

        ip = request.client.host if request.client else "unknown"
        error = _rate_limiter.check(ip, path)
        if error:
            return JSONResponse(
                status_code=429,
                content={"detail": error},
                headers={"Retry-After": str(RATE_LIMIT_WINDOW)},
            )

        return await call_next(request)


# ─── Security Headers Middleware ──────────────────────────────────────────────

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Adds standard security headers to every response.
    """

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Prevent MIME-type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"
        # Prevent clickjacking
        response.headers["X-Frame-Options"] = "DENY"
        # XSS protection (legacy browsers)
        response.headers["X-XSS-Protection"] = "1; mode=block"
        # Referrer policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        # Permissions policy
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        # Strict transport (when behind HTTPS proxy)
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        # Cache control for API responses
        if request.url.path.startswith("/api/"):
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
            response.headers["Pragma"] = "no-cache"

        return response


# ─── Input Sanitization ──────────────────────────────────────────────────────

def sanitize_string(value: str, max_length: int = 500) -> str:
    """
    Sanitize a user-provided string:
    - Strip leading/trailing whitespace
    - Escape HTML entities (prevent stored XSS)
    - Truncate to max_length
    """
    if not isinstance(value, str):
        return ""
    value = value.strip()
    value = html.escape(value, quote=True)
    return value[:max_length]


def sanitize_username(value: str) -> str:
    """Only allow alphanumeric, underscores, hyphens, dots."""
    value = value.strip()[:50]
    return re.sub(r"[^a-zA-Z0-9._-]", "", value)


def sanitize_email(value: str) -> str:
    """Basic email format validation + sanitization."""
    value = value.strip().lower()[:254]
    if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value):
        return ""  # invalid
    return value


# ─── Document Access Control ─────────────────────────────────────────────────

# Define who can access what
DOCUMENT_ACCESS = {
    "admin": ["*"],           # full access
    "instructor": ["*"],      # full access
    "manager": ["view"],      # read-only
    "trainee": ["view"],      # read-only
}


def can_access_document(role: str, action: str) -> bool:
    """
    Check if a role has permission for a document action.
    Actions: 'view', 'upload', 'delete'
    """
    allowed = DOCUMENT_ACCESS.get(role, [])
    return "*" in allowed or action in allowed


# ─── Request Log Query (for admin panel) ─────────────────────────────────────

def get_request_log(
    limit: int = 100,
    method: Optional[str] = None,
    path_contains: Optional[str] = None,
    user_id: Optional[str] = None,
) -> list:
    """Query the request_log for the admin panel."""
    conn = _conn()
    try:
        query = "SELECT * FROM request_log WHERE 1=1"
        params = []
        if method:
            query += " AND method=?"
            params.append(method.upper())
        if path_contains:
            query += " AND path LIKE ?"
            params.append(f"%{path_contains}%")
        if user_id:
            query += " AND user_id=?"
            params.append(user_id)
        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)
        rows = conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_security_stats() -> dict:
    """
    Return security-relevant stats for the admin dashboard.
    """
    conn = _conn()
    try:
        # Total requests today
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        total_today = conn.execute(
            "SELECT COUNT(*) FROM request_log WHERE created_at >= ?", (today,)
        ).fetchone()[0]

        # Failed auth attempts (401s on login)
        failed_logins = conn.execute(
            "SELECT COUNT(*) FROM request_log WHERE path LIKE '%/auth/login%' AND status=401 AND created_at >= ?",
            (today,),
        ).fetchone()[0]

        # 403 Forbidden (unauthorized access attempts)
        forbidden_count = conn.execute(
            "SELECT COUNT(*) FROM request_log WHERE status=403 AND created_at >= ?",
            (today,),
        ).fetchone()[0]

        # 429 Rate limited
        rate_limited = conn.execute(
            "SELECT COUNT(*) FROM request_log WHERE status=429 AND created_at >= ?",
            (today,),
        ).fetchone()[0]

        # Unique IPs today
        unique_ips = conn.execute(
            "SELECT COUNT(DISTINCT ip_address) FROM request_log WHERE created_at >= ?",
            (today,),
        ).fetchone()[0]

        # Average response time
        avg_ms = conn.execute(
            "SELECT AVG(duration_ms) FROM request_log WHERE created_at >= ?",
            (today,),
        ).fetchone()[0] or 0

        return {
            "total_requests_today": total_today,
            "failed_logins_today": failed_logins,
            "forbidden_attempts_today": forbidden_count,
            "rate_limited_today": rate_limited,
            "unique_ips_today": unique_ips,
            "avg_response_ms": round(avg_ms, 1),
        }
    finally:
        conn.close()
