"""
Authentication & Authorization Service
- User registration with bcrypt-hashed passwords
- JWT token issue / verify
- Role-based access control (Admin, Instructor, Manager, Trainee)
"""

import os
import sqlite3
import uuid
from datetime import datetime, timedelta, timezone
from typing import Optional, List, Dict

import jwt
import bcrypt as _bcrypt


def _hash_password(password: str) -> str:
    return _bcrypt.hashpw(password.encode("utf-8"), _bcrypt.gensalt()).decode("utf-8")


def _check_password(password: str, hashed: str) -> bool:
    return _bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

# ─── Config ──────────────────────────────────────────────────────────────────

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "courses.db")
JWT_SECRET = os.getenv("JWT_SECRET", "edu-assist-pro-secret-change-in-prod-2026")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = 24

ROLES = ["admin", "instructor", "manager", "trainee"]
DEFAULT_ROLE = "trainee"


# ─── DB helpers ──────────────────────────────────────────────────────────────

def _conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def _init_tables():
    conn = _conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            TEXT PRIMARY KEY,
            username      TEXT UNIQUE NOT NULL,
            email         TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name          TEXT NOT NULL DEFAULT '',
            role          TEXT NOT NULL DEFAULT 'trainee',
            department    TEXT DEFAULT '',
            is_active     INTEGER NOT NULL DEFAULT 1,
            created_at    TEXT NOT NULL,
            updated_at    TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS audit_log (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    TEXT,
            action     TEXT NOT NULL,
            detail     TEXT DEFAULT '',
            ip_address TEXT DEFAULT '',
            created_at TEXT NOT NULL
        );
    """)
    # Seed a default admin if the table is empty
    existing = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if existing == 0:
        _seed_users(conn)
    conn.commit()
    conn.close()


def _seed_users(conn):
    """Create default admin + demo trainee."""
    now = datetime.now(timezone.utc).isoformat()
    users = [
        {
            "id": str(uuid.uuid4()),
            "username": "admin",
            "email": "admin@eduassistpro.com",
            "password_hash": _hash_password("admin123"),
            "name": "Administrator",
            "role": "admin",
            "department": "IT",
            "created_at": now,
            "updated_at": now,
        },
        {
            "id": str(uuid.uuid4()),
            "username": "test",
            "email": "demo@eduassistpro.com",
            "password_hash": _hash_password("test"),
            "name": "Demo Trainee",
            "role": "trainee",
            "department": "Engineering",
            "created_at": now,
            "updated_at": now,
        },
        {
            "id": str(uuid.uuid4()),
            "username": "manager",
            "email": "manager@eduassistpro.com",
            "password_hash": _hash_password("manager123"),
            "name": "Team Manager",
            "role": "manager",
            "department": "Operations",
            "created_at": now,
            "updated_at": now,
        },
    ]
    for u in users:
        conn.execute(
            """INSERT INTO users (id, username, email, password_hash, name, role, department, created_at, updated_at)
               VALUES (:id, :username, :email, :password_hash, :name, :role, :department, :created_at, :updated_at)""",
            u,
        )


# Run init on import
_init_tables()


# ─── Token helpers ───────────────────────────────────────────────────────────

def create_token(user_id: str, username: str, role: str) -> str:
    payload = {
        "sub": user_id,
        "username": username,
        "role": role,
        "exp": datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRE_HOURS),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_token(token: str) -> Optional[dict]:
    """Returns decoded payload or None if invalid / expired."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


# ─── Public API ──────────────────────────────────────────────────────────────

def register_user(
    username: str,
    email: str,
    password: str,
    name: str = "",
    role: str = DEFAULT_ROLE,
    department: str = "",
) -> dict:
    """Register a new user. Returns user dict (no password)."""
    if role not in ROLES:
        return {"error": f"Invalid role. Must be one of: {', '.join(ROLES)}"}

    conn = _conn()
    try:
        # Check uniqueness
        if conn.execute("SELECT 1 FROM users WHERE username=?", (username,)).fetchone():
            return {"error": "Username already taken"}
        if conn.execute("SELECT 1 FROM users WHERE email=?", (email,)).fetchone():
            return {"error": "Email already registered"}

        now = datetime.now(timezone.utc).isoformat()
        user_id = str(uuid.uuid4())
        conn.execute(
            """INSERT INTO users (id, username, email, password_hash, name, role, department, created_at, updated_at)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            (user_id, username, email, _hash_password(password), name or username, role, department, now, now),
        )
        _log(conn, user_id, "register", f"New {role} account created")
        conn.commit()
        return get_user_safe(user_id, conn)
    finally:
        conn.close()


def login(username: str, password: str) -> dict:
    """Authenticate and return { token, user } or { error }."""
    conn = _conn()
    try:
        row = conn.execute(
            "SELECT * FROM users WHERE username=? AND is_active=1", (username,)
        ).fetchone()
        if not row:
            return {"error": "Invalid username or password"}

        if not _check_password(password, row["password_hash"]):
            _log(conn, row["id"], "login_failed", "Bad password")
            conn.commit()
            return {"error": "Invalid username or password"}

        token = create_token(row["id"], row["username"], row["role"])
        _log(conn, row["id"], "login", "Successful login")
        conn.commit()

        user = _row_to_safe(row)
        return {"token": token, "user": user}
    finally:
        conn.close()


def get_user_safe(user_id: str, conn=None) -> dict:
    """Return user dict without password hash."""
    close = False
    if conn is None:
        conn = _conn()
        close = True
    try:
        row = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
        return _row_to_safe(row) if row else {"error": "User not found"}
    finally:
        if close:
            conn.close()


def get_user_by_username(username: str) -> Optional[dict]:
    conn = _conn()
    try:
        row = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        return _row_to_safe(row) if row else None
    finally:
        conn.close()


def list_users(role: Optional[str] = None) -> List[dict]:
    conn = _conn()
    try:
        if role:
            rows = conn.execute("SELECT * FROM users WHERE role=? ORDER BY created_at DESC", (role,)).fetchall()
        else:
            rows = conn.execute("SELECT * FROM users ORDER BY created_at DESC").fetchall()
        return [_row_to_safe(r) for r in rows]
    finally:
        conn.close()


def update_user(user_id: str, **kwargs) -> dict:
    """Update user fields (name, email, role, department, is_active)."""
    allowed = {"name", "email", "role", "department", "is_active"}
    updates = {k: v for k, v in kwargs.items() if k in allowed and v is not None}
    if not updates:
        return {"error": "No valid fields to update"}

    conn = _conn()
    try:
        updates["updated_at"] = datetime.now(timezone.utc).isoformat()
        set_clause = ", ".join(f"{k}=?" for k in updates)
        vals = list(updates.values()) + [user_id]
        conn.execute(f"UPDATE users SET {set_clause} WHERE id=?", vals)
        _log(conn, user_id, "update_user", f"Fields updated: {list(updates.keys())}")
        conn.commit()
        return get_user_safe(user_id, conn)
    finally:
        conn.close()


def change_password(user_id: str, old_password: str, new_password: str) -> dict:
    conn = _conn()
    try:
        row = conn.execute("SELECT password_hash FROM users WHERE id=?", (user_id,)).fetchone()
        if not row:
            return {"error": "User not found"}
        if not _check_password(old_password, row["password_hash"]):
            return {"error": "Current password is incorrect"}
        conn.execute(
            "UPDATE users SET password_hash=?, updated_at=? WHERE id=?",
            (_hash_password(new_password), datetime.now(timezone.utc).isoformat(), user_id),
        )
        _log(conn, user_id, "change_password", "Password changed")
        conn.commit()
        return {"message": "Password updated successfully"}
    finally:
        conn.close()


def delete_user(user_id: str) -> dict:
    conn = _conn()
    try:
        conn.execute("UPDATE users SET is_active=0, updated_at=? WHERE id=?",
                      (datetime.now(timezone.utc).isoformat(), user_id))
        _log(conn, user_id, "deactivate", "Account deactivated")
        conn.commit()
        return {"message": "User deactivated"}
    finally:
        conn.close()


def get_audit_log(user_id: Optional[str] = None, limit: int = 50) -> List[dict]:
    conn = _conn()
    try:
        if user_id:
            rows = conn.execute(
                "SELECT * FROM audit_log WHERE user_id=? ORDER BY created_at DESC LIMIT ?",
                (user_id, limit),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM audit_log ORDER BY created_at DESC LIMIT ?", (limit,)
            ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


# ─── Internal helpers ────────────────────────────────────────────────────────

def _row_to_safe(row) -> dict:
    return {
        "id": row["id"],
        "user_id": row["id"],
        "username": row["username"],
        "email": row["email"],
        "name": row["name"],
        "role": row["role"],
        "department": row["department"],
        "is_active": bool(row["is_active"]),
        "created_at": row["created_at"],
        "updated_at": row["updated_at"],
    }


def _log(conn, user_id: str, action: str, detail: str = "", ip: str = ""):
    conn.execute(
        "INSERT INTO audit_log (user_id, action, detail, ip_address, created_at) VALUES (?,?,?,?,?)",
        (user_id, action, detail, ip, datetime.now(timezone.utc).isoformat()),
    )
