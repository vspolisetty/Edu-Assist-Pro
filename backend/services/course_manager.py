"""
Course Manager — Data models and persistence for the course/curriculum system.
Stores courses, modules, sections, and enrollment data in SQLite.
"""

import sqlite3
import os
import json
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any


DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "courses.db")


def get_db():
    """Get a database connection with row_factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Initialize the courses database with tables and seed data."""
    conn = get_db()
    cur = conn.cursor()

    # --- Tables ---
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS courses (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT,
            category TEXT NOT NULL,
            icon TEXT DEFAULT '📋',
            duration_hours REAL DEFAULT 0,
            difficulty TEXT DEFAULT 'Beginner',
            prerequisites TEXT DEFAULT '[]',
            is_mandatory INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS modules (
            id TEXT PRIMARY KEY,
            course_id TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            order_index INTEGER DEFAULT 0,
            duration_minutes INTEGER DEFAULT 30,
            content TEXT DEFAULT '',
            FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS enrollments (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            course_id TEXT NOT NULL,
            status TEXT DEFAULT 'enrolled',
            enrolled_at TEXT NOT NULL,
            completed_at TEXT,
            progress REAL DEFAULT 0,
            FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS module_progress (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            module_id TEXT NOT NULL,
            course_id TEXT NOT NULL,
            status TEXT DEFAULT 'not_started',
            started_at TEXT,
            completed_at TEXT,
            score REAL,
            FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE,
            FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
        );
    """)

    # --- Seed data (only if no courses exist) ---
    existing = cur.execute("SELECT COUNT(*) FROM courses").fetchone()[0]
    if existing == 0:
        _seed_courses(cur)

    conn.commit()
    conn.close()


def _seed_courses(cur):
    """Insert default corporate training courses."""
    now = datetime.now().isoformat()
    courses = [
        {
            "id": "course-compliance-101",
            "title": "Compliance Fundamentals",
            "description": "Learn essential compliance policies, data privacy regulations, and workplace ethics required for all employees.",
            "category": "Compliance",
            "icon": "📋",
            "duration_hours": 4,
            "difficulty": "Beginner",
            "is_mandatory": 1,
            "modules": [
                ("Company Policies Overview", "Understanding the core company policies, code of conduct, and employee responsibilities.", 30, "Welcome to Compliance Fundamentals. This module covers company policies..."),
                ("Data Privacy & GDPR", "Learn about GDPR principles, data processing consent, and handling personal data.", 45, "Data privacy is critical in modern organizations..."),
                ("Workplace Safety", "Emergency procedures, hazard identification, and safety protocols.", 30, "Workplace safety is everyone's responsibility..."),
                ("Anti-Harassment Training", "Understanding, preventing, and reporting workplace harassment.", 45, "Creating a respectful and inclusive workplace is essential..."),
                ("Ethics & Code of Conduct", "Business ethics, conflicts of interest, and whistleblower protections.", 30, "Ethical behavior is the foundation of our organization..."),
            ]
        },
        {
            "id": "course-security-101",
            "title": "Security Awareness Training",
            "description": "Protect organizational data and systems by learning cybersecurity best practices, phishing prevention, and incident reporting.",
            "category": "Security",
            "icon": "🔒",
            "duration_hours": 3,
            "difficulty": "Beginner",
            "is_mandatory": 1,
            "modules": [
                ("Cybersecurity Fundamentals", "Overview of the threat landscape and your role in security.", 30, "Cybersecurity is not just IT's job..."),
                ("Phishing & Social Engineering", "Identify and avoid phishing emails, social engineering attacks.", 45, "Phishing is the #1 attack vector..."),
                ("Password & Access Management", "Strong passwords, MFA, and managing system access securely.", 30, "Passwords are your first line of defense..."),
                ("Incident Reporting", "How to identify, report, and respond to security incidents.", 30, "When you see something suspicious, report it immediately..."),
            ]
        },
        {
            "id": "course-leadership-201",
            "title": "Leadership Development Program",
            "description": "Develop key leadership skills including team management, communication, conflict resolution, and strategic thinking.",
            "category": "Leadership",
            "icon": "👥",
            "duration_hours": 6,
            "difficulty": "Intermediate",
            "is_mandatory": 0,
            "modules": [
                ("Team Management Essentials", "Setting goals, delegating effectively, and building high-performance teams.", 45, "Great leaders build great teams..."),
                ("Communication & Feedback", "Effective communication strategies and giving/receiving constructive feedback.", 45, "Communication is the most important leadership skill..."),
                ("Conflict Resolution", "Mediation techniques and handling difficult workplace situations.", 40, "Conflict is inevitable; how you handle it defines you..."),
                ("Strategic Thinking", "Long-term planning, decision-making frameworks, and organizational alignment.", 45, "Strategy is about making choices..."),
                ("Change Management", "Leading teams through organizational change and transformation.", 40, "Change is the only constant in business..."),
                ("Mentoring & Coaching", "Developing your team's talent through mentoring and coaching.", 35, "The best leaders develop other leaders..."),
            ]
        },
        {
            "id": "course-technical-101",
            "title": "Technical Skills Onboarding",
            "description": "Get up to speed on company tools, systems, processes, and quality standards for your role.",
            "category": "Technical",
            "icon": "⚙️",
            "duration_hours": 5,
            "difficulty": "Beginner",
            "is_mandatory": 0,
            "modules": [
                ("Tools & Systems Overview", "Introduction to company software, CRM, ERP, and collaboration tools.", 45, "Our technology stack includes..."),
                ("Process Documentation", "How to create, update, and follow Standard Operating Procedures.", 40, "Good documentation saves time and reduces errors..."),
                ("Quality Standards", "Understanding ISO standards, quality metrics, and continuous improvement.", 45, "Quality is not an act, it is a habit..."),
                ("Project Management Basics", "Agile methodology, task management, and project tracking.", 45, "Every project needs a plan..."),
                ("Troubleshooting & Support", "Common issues, escalation procedures, and knowledge base usage.", 35, "When things go wrong, follow these steps..."),
            ]
        },
        {
            "id": "course-hr-101",
            "title": "HR & Benefits Orientation",
            "description": "Understand employee benefits, time-off policies, professional development opportunities, and workplace culture.",
            "category": "HR & Benefits",
            "icon": "📄",
            "duration_hours": 2,
            "difficulty": "Beginner",
            "is_mandatory": 1,
            "modules": [
                ("Employee Benefits Overview", "Health insurance, retirement plans, and other employee benefits.", 30, "Your benefits package includes..."),
                ("Time Off & Leave Policies", "Vacation, sick leave, parental leave, and remote work guidelines.", 25, "Work-life balance is important..."),
                ("Professional Development", "Training budgets, conference attendance, and career growth.", 25, "We invest in your growth..."),
                ("Workplace Culture", "Our values, diversity & inclusion, and team-building.", 20, "Culture is what happens when no one is watching..."),
            ]
        },
        {
            "id": "course-customer-201",
            "title": "Customer Relations Excellence",
            "description": "Master client communication, service standards, complaint handling, and relationship management skills.",
            "category": "Customer Service",
            "icon": "🤝",
            "duration_hours": 4,
            "difficulty": "Intermediate",
            "is_mandatory": 0,
            "modules": [
                ("Client Communication Standards", "Professional communication across email, phone, and meetings.", 40, "Every interaction is an opportunity..."),
                ("Service Level Agreements", "Understanding SLAs, response times, and quality expectations.", 35, "SLAs set mutual expectations..."),
                ("Handling Complaints", "De-escalation techniques and turning complaints into opportunities.", 40, "A complaint is a gift..."),
                ("Account Management", "Building long-term client relationships and managing accounts.", 35, "Retention is more valuable than acquisition..."),
                ("Negotiation Skills", "Win-win negotiation strategies and closing techniques.", 40, "Negotiation is about understanding needs..."),
            ]
        },
    ]

    for course in courses:
        cur.execute("""
            INSERT INTO courses (id, title, description, category, icon, duration_hours, difficulty, prerequisites, is_mandatory, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            course["id"], course["title"], course["description"],
            course["category"], course["icon"], course["duration_hours"],
            course["difficulty"], "[]", course["is_mandatory"], now, now
        ))

        for idx, (mod_title, mod_desc, mod_dur, mod_content) in enumerate(course["modules"]):
            cur.execute("""
                INSERT INTO modules (id, course_id, title, description, order_index, duration_minutes, content)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                f"mod-{uuid.uuid4().hex[:8]}", course["id"],
                mod_title, mod_desc, idx, mod_dur, mod_content
            ))


# ─── CRUD Functions ──────────────────────────────────────────────────────────

def get_all_courses() -> List[Dict]:
    """Return all courses with module counts."""
    conn = get_db()
    rows = conn.execute("""
        SELECT c.*, COUNT(m.id) as module_count
        FROM courses c
        LEFT JOIN modules m ON m.course_id = c.id
        GROUP BY c.id
        ORDER BY c.is_mandatory DESC, c.title
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_course(course_id: str) -> Optional[Dict]:
    """Return a single course with its modules."""
    conn = get_db()
    course = conn.execute("SELECT * FROM courses WHERE id = ?", (course_id,)).fetchone()
    if not course:
        conn.close()
        return None
    result = dict(course)
    modules = conn.execute(
        "SELECT * FROM modules WHERE course_id = ? ORDER BY order_index", (course_id,)
    ).fetchall()
    result["modules"] = [dict(m) for m in modules]
    conn.close()
    return result


def get_enrollment(user_id: str, course_id: str) -> Optional[Dict]:
    """Get enrollment status for a user + course."""
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM enrollments WHERE user_id = ? AND course_id = ?",
        (user_id, course_id)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def enroll_user(user_id: str, course_id: str) -> Dict:
    """Enroll a user in a course."""
    conn = get_db()
    enrollment_id = f"enr-{uuid.uuid4().hex[:8]}"
    now = datetime.now().isoformat()
    conn.execute("""
        INSERT OR IGNORE INTO enrollments (id, user_id, course_id, status, enrolled_at, progress)
        VALUES (?, ?, ?, 'enrolled', ?, 0)
    """, (enrollment_id, user_id, course_id, now))
    conn.commit()
    conn.close()
    return {"enrollment_id": enrollment_id, "status": "enrolled"}


def get_user_enrollments(user_id: str) -> List[Dict]:
    """Get all courses a user is enrolled in, with progress."""
    conn = get_db()
    rows = conn.execute("""
        SELECT e.*, c.title, c.category, c.icon, c.duration_hours, c.difficulty,
               (SELECT COUNT(*) FROM modules WHERE course_id = c.id) as total_modules,
               (SELECT COUNT(*) FROM module_progress
                WHERE user_id = e.user_id AND course_id = c.id AND status = 'completed') as completed_modules
        FROM enrollments e
        JOIN courses c ON c.id = e.course_id
        WHERE e.user_id = ?
        ORDER BY e.enrolled_at DESC
    """, (user_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_module_progress(user_id: str, module_id: str, course_id: str, status: str, score: float = None) -> Dict:
    """Update progress on a specific module."""
    conn = get_db()
    now = datetime.now().isoformat()
    prog_id = f"prog-{uuid.uuid4().hex[:8]}"

    # Upsert module progress
    existing = conn.execute(
        "SELECT id FROM module_progress WHERE user_id = ? AND module_id = ?",
        (user_id, module_id)
    ).fetchone()

    if existing:
        conn.execute("""
            UPDATE module_progress SET status = ?, completed_at = ?, score = ?
            WHERE user_id = ? AND module_id = ?
        """, (status, now if status == "completed" else None, score, user_id, module_id))
    else:
        conn.execute("""
            INSERT INTO module_progress (id, user_id, module_id, course_id, status, started_at, completed_at, score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (prog_id, user_id, module_id, course_id, status, now, now if status == "completed" else None, score))

    # Recalculate overall enrollment progress
    total = conn.execute("SELECT COUNT(*) FROM modules WHERE course_id = ?", (course_id,)).fetchone()[0]
    completed = conn.execute(
        "SELECT COUNT(*) FROM module_progress WHERE user_id = ? AND course_id = ? AND status = 'completed'",
        (user_id, course_id)
    ).fetchone()[0]
    progress = (completed / total * 100) if total > 0 else 0

    enrollment_status = "completed" if progress >= 100 else "in_progress"
    conn.execute("""
        UPDATE enrollments SET progress = ?, status = ?, completed_at = ?
        WHERE user_id = ? AND course_id = ?
    """, (progress, enrollment_status, now if enrollment_status == "completed" else None, user_id, course_id))

    conn.commit()
    conn.close()
    return {"progress": progress, "status": enrollment_status}


def get_module_progress(user_id: str, course_id: str) -> List[Dict]:
    """Get progress for all modules in a course for a user."""
    conn = get_db()
    rows = conn.execute("""
        SELECT m.*, mp.status as progress_status, mp.completed_at, mp.score
        FROM modules m
        LEFT JOIN module_progress mp ON mp.module_id = m.id AND mp.user_id = ?
        WHERE m.course_id = ?
        ORDER BY m.order_index
    """, (user_id, course_id)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# Initialize DB on import
init_db()
