"""
Quiz Manager — AI-generated quizzes, grading, results storage, and certificate generation.
Uses Groq LLM to generate quiz questions from course content.
"""

import sqlite3
import os
import json
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any


DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "courses.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_quiz_tables():
    """Create quiz-related tables."""
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS quizzes (
            id TEXT PRIMARY KEY,
            course_id TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            time_limit_minutes INTEGER DEFAULT 15,
            passing_score REAL DEFAULT 70,
            question_count INTEGER DEFAULT 10,
            created_at TEXT NOT NULL,
            FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS quiz_questions (
            id TEXT PRIMARY KEY,
            quiz_id TEXT NOT NULL,
            question_text TEXT NOT NULL,
            question_type TEXT DEFAULT 'mcq',
            options TEXT DEFAULT '[]',
            correct_answer TEXT NOT NULL,
            explanation TEXT,
            points REAL DEFAULT 1,
            order_index INTEGER DEFAULT 0,
            FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS quiz_attempts (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            quiz_id TEXT NOT NULL,
            course_id TEXT NOT NULL,
            answers TEXT DEFAULT '{}',
            score REAL,
            total_points REAL,
            percentage REAL,
            passed INTEGER DEFAULT 0,
            started_at TEXT NOT NULL,
            completed_at TEXT,
            time_spent_seconds INTEGER DEFAULT 0,
            FOREIGN KEY (quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS certificates (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            course_id TEXT NOT NULL,
            quiz_attempt_id TEXT,
            course_title TEXT NOT NULL,
            user_name TEXT NOT NULL,
            score REAL,
            issued_at TEXT NOT NULL,
            FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
        );
    """)
    conn.commit()
    conn.close()


# ─── Quiz Generation ─────────────────────────────────────────────────────────

def build_quiz_prompt(course_title: str, category: str, modules: List[Dict]) -> str:
    """Build the prompt for the LLM to generate quiz questions."""
    module_content = "\n".join([
        f"- {m['title']}: {m.get('description', '')} {m.get('content', '')}"
        for m in modules
    ])

    return f"""You are a corporate training assessment designer. Generate exactly 10 quiz questions for the course "{course_title}" in the "{category}" category.

Course modules and content:
{module_content}

Generate a JSON array of 10 questions. Each question must have:
- "question_text": The question
- "question_type": Either "mcq" (multiple choice) or "true_false"
- "options": Array of 4 options for mcq, or ["True", "False"] for true_false
- "correct_answer": The exact text of the correct option
- "explanation": Brief explanation of why this is correct

Mix 8 MCQ and 2 True/False questions. Make them professional and relevant to corporate training.

Respond ONLY with a valid JSON array, no other text. Example format:
[
  {{
    "question_text": "What is the primary purpose of GDPR?",
    "question_type": "mcq",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_answer": "Option A",
    "explanation": "GDPR was designed to..."
  }}
]"""


def parse_quiz_response(response_text: str) -> List[Dict]:
    """Parse the LLM response into quiz questions."""
    # Try to extract JSON from the response
    text = response_text.strip()

    # Find JSON array in response
    start = text.find('[')
    end = text.rfind(']')
    if start != -1 and end != -1:
        text = text[start:end + 1]

    try:
        questions = json.loads(text)
        if isinstance(questions, list):
            return questions
    except json.JSONDecodeError:
        pass

    # Fallback: return empty if parsing fails
    return []


def create_quiz_from_questions(course_id: str, course_title: str, questions: List[Dict]) -> Dict:
    """Store generated quiz and questions in the database."""
    conn = get_db()
    quiz_id = f"quiz-{uuid.uuid4().hex[:8]}"
    now = datetime.now().isoformat()

    conn.execute("""
        INSERT INTO quizzes (id, course_id, title, description, time_limit_minutes, passing_score, question_count, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        quiz_id, course_id,
        f"{course_title} Assessment",
        f"Test your knowledge of {course_title}",
        15, 70, len(questions), now
    ))

    for idx, q in enumerate(questions):
        q_id = f"qq-{uuid.uuid4().hex[:8]}"
        conn.execute("""
            INSERT INTO quiz_questions (id, quiz_id, question_text, question_type, options, correct_answer, explanation, points, order_index)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            q_id, quiz_id,
            q.get("question_text", ""),
            q.get("question_type", "mcq"),
            json.dumps(q.get("options", [])),
            q.get("correct_answer", ""),
            q.get("explanation", ""),
            1, idx
        ))

    conn.commit()
    conn.close()
    return {"quiz_id": quiz_id, "question_count": len(questions)}


def get_fallback_questions(course_title: str, category: str) -> List[Dict]:
    """Fallback questions if LLM fails."""
    return [
        {
            "question_text": f"What is the primary objective of {course_title}?",
            "question_type": "mcq",
            "options": [
                f"To understand {category} fundamentals",
                "To pass the time",
                "To learn cooking skills",
                "None of the above"
            ],
            "correct_answer": f"To understand {category} fundamentals",
            "explanation": f"The course focuses on {category} fundamentals."
        },
        {
            "question_text": f"Is {course_title} important for organizational success?",
            "question_type": "true_false",
            "options": ["True", "False"],
            "correct_answer": "True",
            "explanation": f"{course_title} is essential for organizational compliance and growth."
        },
        {
            "question_text": f"Which best describes the scope of {category}?",
            "question_type": "mcq",
            "options": [
                f"Company-wide {category} policies and procedures",
                "Personal hobbies",
                "Sports statistics",
                "Weather forecasting"
            ],
            "correct_answer": f"Company-wide {category} policies and procedures",
            "explanation": f"{category} covers organizational policies and best practices."
        },
        {
            "question_text": f"Training in {category} is optional and not recommended.",
            "question_type": "true_false",
            "options": ["True", "False"],
            "correct_answer": "False",
            "explanation": f"{category} training is highly recommended for all employees."
        },
        {
            "question_text": f"What should you do after completing {course_title}?",
            "question_type": "mcq",
            "options": [
                "Apply the learned concepts in your daily work",
                "Forget everything immediately",
                "Ignore the guidelines",
                "Delete the training materials"
            ],
            "correct_answer": "Apply the learned concepts in your daily work",
            "explanation": "Training is most effective when applied to real work situations."
        },
    ]


# ─── Quiz CRUD ────────────────────────────────────────────────────────────────

def get_quiz_for_course(course_id: str) -> Optional[Dict]:
    """Get the most recent quiz for a course."""
    conn = get_db()
    quiz = conn.execute(
        "SELECT * FROM quizzes WHERE course_id = ? ORDER BY created_at DESC LIMIT 1",
        (course_id,)
    ).fetchone()
    if not quiz:
        conn.close()
        return None

    result = dict(quiz)
    questions = conn.execute(
        "SELECT * FROM quiz_questions WHERE quiz_id = ? ORDER BY order_index",
        (quiz["id"],)
    ).fetchall()
    result["questions"] = []
    for q in questions:
        qd = dict(q)
        qd["options"] = json.loads(qd["options"])
        result["questions"].append(qd)

    conn.close()
    return result


def get_quiz_by_id(quiz_id: str) -> Optional[Dict]:
    """Get a quiz by ID with questions."""
    conn = get_db()
    quiz = conn.execute("SELECT * FROM quizzes WHERE id = ?", (quiz_id,)).fetchone()
    if not quiz:
        conn.close()
        return None
    result = dict(quiz)
    questions = conn.execute(
        "SELECT * FROM quiz_questions WHERE quiz_id = ? ORDER BY order_index",
        (quiz_id,)
    ).fetchall()
    result["questions"] = []
    for q in questions:
        qd = dict(q)
        qd["options"] = json.loads(qd["options"])
        result["questions"].append(qd)
    conn.close()
    return result


# ─── Grading ──────────────────────────────────────────────────────────────────

def grade_quiz(quiz_id: str, user_id: str, answers: Dict[str, str], time_spent: int = 0) -> Dict:
    """Grade a quiz attempt and store results."""
    conn = get_db()
    questions = conn.execute(
        "SELECT * FROM quiz_questions WHERE quiz_id = ? ORDER BY order_index",
        (quiz_id,)
    ).fetchall()

    quiz = conn.execute("SELECT * FROM quizzes WHERE id = ?", (quiz_id,)).fetchone()
    if not quiz:
        conn.close()
        return {"error": "Quiz not found"}

    total_points = 0
    earned_points = 0
    results = []

    for q in questions:
        total_points += q["points"]
        user_answer = answers.get(q["id"], "")
        is_correct = user_answer.strip().lower() == q["correct_answer"].strip().lower()
        if is_correct:
            earned_points += q["points"]
        results.append({
            "question_id": q["id"],
            "user_answer": user_answer,
            "correct_answer": q["correct_answer"],
            "is_correct": is_correct,
            "explanation": q["explanation"],
            "points": q["points"] if is_correct else 0
        })

    percentage = (earned_points / total_points * 100) if total_points > 0 else 0
    passed = percentage >= quiz["passing_score"]

    attempt_id = f"att-{uuid.uuid4().hex[:8]}"
    now = datetime.now().isoformat()

    conn.execute("""
        INSERT INTO quiz_attempts (id, user_id, quiz_id, course_id, answers, score, total_points, percentage, passed, started_at, completed_at, time_spent_seconds)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        attempt_id, user_id, quiz_id, quiz["course_id"],
        json.dumps(answers), earned_points, total_points,
        round(percentage, 1), 1 if passed else 0,
        now, now, time_spent
    ))

    # If passed, generate certificate
    certificate = None
    if passed:
        certificate = _generate_certificate(conn, user_id, quiz["course_id"], attempt_id, percentage)

    conn.commit()
    conn.close()

    return {
        "attempt_id": attempt_id,
        "score": earned_points,
        "total_points": total_points,
        "percentage": round(percentage, 1),
        "passed": passed,
        "passing_score": quiz["passing_score"],
        "results": results,
        "certificate": certificate,
        "time_spent_seconds": time_spent
    }


def _generate_certificate(conn, user_id: str, course_id: str, attempt_id: str, score: float) -> Dict:
    """Generate a certificate for passing a quiz."""
    course = conn.execute("SELECT title FROM courses WHERE id = ?", (course_id,)).fetchone()
    cert_id = f"cert-{uuid.uuid4().hex[:8]}"
    now = datetime.now().isoformat()

    conn.execute("""
        INSERT INTO certificates (id, user_id, course_id, quiz_attempt_id, course_title, user_name, score, issued_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        cert_id, user_id, course_id, attempt_id,
        course["title"] if course else "Unknown Course",
        user_id, round(score, 1), now
    ))

    return {
        "certificate_id": cert_id,
        "course_title": course["title"] if course else "Unknown",
        "score": round(score, 1),
        "issued_at": now
    }


# ─── Results & History ────────────────────────────────────────────────────────

def get_user_results(user_id: str) -> List[Dict]:
    """Get all quiz attempt results for a user."""
    conn = get_db()
    rows = conn.execute("""
        SELECT qa.*, q.title as quiz_title, c.title as course_title, c.category, c.icon
        FROM quiz_attempts qa
        JOIN quizzes q ON q.id = qa.quiz_id
        JOIN courses c ON c.id = qa.course_id
        WHERE qa.user_id = ?
        ORDER BY qa.completed_at DESC
    """, (user_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_user_certificates(user_id: str) -> List[Dict]:
    """Get all certificates for a user."""
    conn = get_db()
    rows = conn.execute("""
        SELECT * FROM certificates WHERE user_id = ? ORDER BY issued_at DESC
    """, (user_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_certificate(cert_id: str) -> Optional[Dict]:
    """Get a single certificate by ID."""
    conn = get_db()
    row = conn.execute("SELECT * FROM certificates WHERE id = ?", (cert_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


# Initialize tables on import
init_quiz_tables()
