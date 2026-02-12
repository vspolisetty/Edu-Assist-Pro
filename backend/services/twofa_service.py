"""
Two-Factor Authentication (2FA) Service
========================================
Supports multiple verification methods:
  - authenticator  (TOTP app like Google Authenticator)
  - sms            (OTP sent to registered phone)
  - hardware_key   (USB security key / FIDO2)
  - contact_admin  (Admin-issued one-time code)

For DEMO purposes the valid code is always 123456.
In production, replace with real TOTP / SMS / FIDO2 integrations.
"""

import os
import sqlite3
import uuid
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional, List, Dict

import jwt

# ─── Config ──────────────────────────────────────────────────────────────────

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "courses.db")
JWT_SECRET = os.getenv("JWT_SECRET", "edu-assist-pro-secret-change-in-prod-2026")
JWT_ALGORITHM = "HS256"

# Demo code – in production this would be generated per-request
DEMO_CODE = "123456"

# Temp token lifespan (minutes) – user must complete 2FA within this window
TEMP_TOKEN_EXPIRE_MINUTES = 10

# Available 2FA methods
AVAILABLE_METHODS = [
    {
        "id": "authenticator",
        "label": "Authenticator App",
        "description": "Use Google Authenticator, Microsoft Authenticator, or similar app",
        "icon": "phonelink_lock",
        "instructions": "Open your authenticator app and enter the 6-digit code displayed.",
    },
    {
        "id": "sms",
        "label": "OTP to Phone",
        "description": "Receive a one-time code via SMS to your registered phone",
        "icon": "sms",
        "instructions": "A 6-digit code has been sent to your registered phone number ending in ****.",
    },
    {
        "id": "hardware_key",
        "label": "Hardware Security Key",
        "description": "Use a USB security key (YubiKey, Titan, etc.)",
        "icon": "usb",
        "instructions": "Insert your hardware security key and enter the generated code.",
    },
    {
        "id": "contact_admin",
        "label": "Contact Admin",
        "description": "Request a verification code from your system administrator",
        "icon": "support_agent",
        "instructions": "Contact your administrator to receive a one-time verification code.",
    },
]


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
        CREATE TABLE IF NOT EXISTS twofa_settings (
            user_id          TEXT PRIMARY KEY,
            is_enabled       INTEGER NOT NULL DEFAULT 0,
            preferred_method TEXT NOT NULL DEFAULT 'authenticator',
            phone_last4      TEXT DEFAULT '',
            totp_secret      TEXT DEFAULT '',
            hardware_key_id  TEXT DEFAULT '',
            backup_codes     TEXT DEFAULT '',
            updated_at       TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS twofa_challenges (
            id          TEXT PRIMARY KEY,
            user_id     TEXT NOT NULL,
            method      TEXT NOT NULL,
            code        TEXT NOT NULL,
            is_used     INTEGER NOT NULL DEFAULT 0,
            expires_at  TEXT NOT NULL,
            created_at  TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)
    conn.commit()
    conn.close()


# Run init on import
_init_tables()


# ─── Temporary token (pre-2FA) ──────────────────────────────────────────────

def create_temp_token(user_id: str, username: str, role: str) -> str:
    """Create a short-lived token that only authorises the 2FA verification step."""
    payload = {
        "sub": user_id,
        "username": username,
        "role": role,
        "purpose": "2fa",  # marks this as a pre-2FA token
        "exp": datetime.now(timezone.utc) + timedelta(minutes=TEMP_TOKEN_EXPIRE_MINUTES),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_temp_token(token: str) -> Optional[dict]:
    """Verify a temp 2FA token. Returns payload only if purpose == '2fa'."""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if payload.get("purpose") != "2fa":
            return None
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


# ─── 2FA Settings Management ────────────────────────────────────────────────

def get_user_2fa_settings(user_id: str) -> dict:
    """Get 2FA settings for a user. Returns defaults if none exist."""
    conn = _conn()
    try:
        row = conn.execute("SELECT * FROM twofa_settings WHERE user_id=?", (user_id,)).fetchone()
        if row:
            return {
                "user_id": row["user_id"],
                "is_enabled": bool(row["is_enabled"]),
                "preferred_method": row["preferred_method"],
                "phone_last4": row["phone_last4"],
                "has_totp": bool(row["totp_secret"]),
                "has_hardware_key": bool(row["hardware_key_id"]),
                "has_backup_codes": bool(row["backup_codes"]),
                "updated_at": row["updated_at"],
            }
        return {
            "user_id": user_id,
            "is_enabled": False,
            "preferred_method": "authenticator",
            "phone_last4": "",
            "has_totp": False,
            "has_hardware_key": False,
            "has_backup_codes": False,
            "updated_at": None,
        }
    finally:
        conn.close()


def enable_2fa(user_id: str, method: str = "authenticator") -> dict:
    """Enable 2FA for a user with the specified preferred method."""
    valid_methods = [m["id"] for m in AVAILABLE_METHODS]
    if method not in valid_methods:
        return {"error": f"Invalid method. Must be one of: {', '.join(valid_methods)}"}

    conn = _conn()
    try:
        now = datetime.now(timezone.utc).isoformat()
        # Generate demo secrets based on method
        totp_secret = f"DEMO-TOTP-{uuid.uuid4().hex[:16].upper()}" if method == "authenticator" else ""
        phone_last4 = "1234" if method == "sms" else ""
        hardware_key_id = f"HW-{uuid.uuid4().hex[:8].upper()}" if method == "hardware_key" else ""

        # Generate backup codes
        backup_codes = ",".join([f"{secrets.randbelow(900000) + 100000}" for _ in range(8)])

        conn.execute("""
            INSERT INTO twofa_settings (user_id, is_enabled, preferred_method, phone_last4, totp_secret, hardware_key_id, backup_codes, updated_at)
            VALUES (?, 1, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                is_enabled=1,
                preferred_method=excluded.preferred_method,
                phone_last4=excluded.phone_last4,
                totp_secret=CASE WHEN excluded.totp_secret != '' THEN excluded.totp_secret ELSE twofa_settings.totp_secret END,
                hardware_key_id=CASE WHEN excluded.hardware_key_id != '' THEN excluded.hardware_key_id ELSE twofa_settings.hardware_key_id END,
                backup_codes=excluded.backup_codes,
                updated_at=excluded.updated_at
        """, (user_id, method, phone_last4, totp_secret, hardware_key_id, backup_codes, now))
        conn.commit()

        return {
            "message": "2FA enabled successfully",
            "method": method,
            "backup_codes": backup_codes.split(","),
            "totp_secret": totp_secret if method == "authenticator" else None,
            "phone_last4": phone_last4 if method == "sms" else None,
            "hardware_key_id": hardware_key_id if method == "hardware_key" else None,
        }
    finally:
        conn.close()


def disable_2fa(user_id: str) -> dict:
    """Disable 2FA for a user."""
    conn = _conn()
    try:
        now = datetime.now(timezone.utc).isoformat()
        conn.execute("""
            UPDATE twofa_settings SET is_enabled=0, updated_at=? WHERE user_id=?
        """, (now, user_id))
        conn.commit()
        return {"message": "2FA disabled successfully"}
    finally:
        conn.close()


def update_preferred_method(user_id: str, method: str) -> dict:
    """Update the user's preferred 2FA method."""
    valid_methods = [m["id"] for m in AVAILABLE_METHODS]
    if method not in valid_methods:
        return {"error": f"Invalid method. Must be one of: {', '.join(valid_methods)}"}

    conn = _conn()
    try:
        now = datetime.now(timezone.utc).isoformat()
        conn.execute("""
            UPDATE twofa_settings SET preferred_method=?, updated_at=? WHERE user_id=?
        """, (method, now, user_id))
        conn.commit()
        return {"message": f"Preferred method updated to {method}"}
    finally:
        conn.close()


# ─── Challenge / Verification ───────────────────────────────────────────────

def create_challenge(user_id: str, method: str) -> dict:
    """
    Create a 2FA challenge (send code).
    In DEMO mode, the code is always 123456.
    In production, this would:
      - authenticator: not needed (user reads from app)
      - sms: call SMS gateway to send OTP
      - hardware_key: initiate WebAuthn challenge
      - contact_admin: notify admin via email/chat
    """
    challenge_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(minutes=5)

    conn = _conn()
    try:
        # Invalidate any existing unused challenges for this user
        conn.execute("""
            UPDATE twofa_challenges SET is_used=1
            WHERE user_id=? AND is_used=0
        """, (user_id,))

        conn.execute("""
            INSERT INTO twofa_challenges (id, user_id, method, code, is_used, expires_at, created_at)
            VALUES (?, ?, ?, ?, 0, ?, ?)
        """, (challenge_id, user_id, method, DEMO_CODE, expires_at.isoformat(), now.isoformat()))
        conn.commit()

        # Get method info
        method_info = next((m for m in AVAILABLE_METHODS if m["id"] == method), AVAILABLE_METHODS[0])

        return {
            "challenge_id": challenge_id,
            "method": method,
            "instructions": method_info["instructions"],
            "expires_in_seconds": 300,
            # In demo mode we hint at the code
            "demo_hint": "For demo purposes, the code is 123456",
        }
    finally:
        conn.close()


def verify_challenge(challenge_id: str, code: str) -> dict:
    """
    Verify a 2FA challenge code.
    Returns { success: True } or { error: "..." }.
    """
    conn = _conn()
    try:
        row = conn.execute("""
            SELECT * FROM twofa_challenges
            WHERE id=? AND is_used=0
        """, (challenge_id,)).fetchone()

        if not row:
            return {"error": "Invalid or expired verification code"}

        # Check expiry
        expires_at = datetime.fromisoformat(row["expires_at"])
        if datetime.now(timezone.utc) > expires_at:
            conn.execute("UPDATE twofa_challenges SET is_used=1 WHERE id=?", (challenge_id,))
            conn.commit()
            return {"error": "Verification code has expired. Please request a new one."}

        # Check code (demo: always 123456)
        if code != row["code"]:
            return {"error": "Invalid verification code. Please try again."}

        # Mark as used
        conn.execute("UPDATE twofa_challenges SET is_used=1 WHERE id=?", (challenge_id,))
        conn.commit()

        return {"success": True, "user_id": row["user_id"]}
    finally:
        conn.close()


# ─── Admin helpers ───────────────────────────────────────────────────────────

def get_all_2fa_stats() -> dict:
    """Get 2FA adoption statistics for admin dashboard."""
    conn = _conn()
    try:
        total_users = conn.execute("SELECT COUNT(*) FROM users WHERE is_active=1").fetchone()[0]
        enabled_count = conn.execute("SELECT COUNT(*) FROM twofa_settings WHERE is_enabled=1").fetchone()[0]

        method_counts = {}
        rows = conn.execute("""
            SELECT preferred_method, COUNT(*) as cnt
            FROM twofa_settings WHERE is_enabled=1
            GROUP BY preferred_method
        """).fetchall()
        for r in rows:
            method_counts[r["preferred_method"]] = r["cnt"]

        recent_challenges = conn.execute("""
            SELECT COUNT(*) FROM twofa_challenges
            WHERE created_at >= datetime('now', '-24 hours')
        """).fetchone()[0]

        return {
            "total_users": total_users,
            "enabled_count": enabled_count,
            "disabled_count": total_users - enabled_count,
            "adoption_rate": round((enabled_count / max(total_users, 1)) * 100, 1),
            "method_breakdown": method_counts,
            "challenges_last_24h": recent_challenges,
        }
    finally:
        conn.close()


def admin_enable_2fa_for_user(user_id: str, method: str = "authenticator") -> dict:
    """Admin can enable 2FA for any user."""
    return enable_2fa(user_id, method)


def admin_disable_2fa_for_user(user_id: str) -> dict:
    """Admin can disable 2FA for any user."""
    return disable_2fa(user_id)


def get_available_methods() -> List[dict]:
    """Return list of available 2FA methods."""
    return AVAILABLE_METHODS
