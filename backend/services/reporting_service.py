"""
Reporting Service — Analytics and reporting for managers/admins.
Provides team overviews, score distributions, compliance stats, and CSV export.
"""

import sqlite3
import os
import csv
import io
from datetime import datetime
from typing import Optional, List, Dict, Any


DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "courses.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ─── Team Completion Overview ─────────────────────────────────────────────────

def get_team_overview() -> Dict[str, Any]:
    """
    Returns an overview of all users' training progress:
    - Total users, courses, enrollments, completions
    - Per-user summary (courses enrolled, completed, avg score)
    """
    conn = get_db()
    cur = conn.cursor()

    # Total counts
    total_users = cur.execute("SELECT COUNT(*) FROM users WHERE is_active = 1").fetchone()[0]
    total_courses = cur.execute("SELECT COUNT(*) FROM courses").fetchone()[0]
    total_enrollments = cur.execute("SELECT COUNT(*) FROM enrollments").fetchone()[0]
    total_completions = cur.execute(
        "SELECT COUNT(*) FROM enrollments WHERE status = 'completed'"
    ).fetchone()[0]

    # Per-user summaries
    rows = cur.execute("""
        SELECT
            u.id,
            u.username,
            u.name,
            u.department,
            u.role,
            COUNT(DISTINCT e.course_id) AS enrolled,
            COUNT(DISTINCT CASE WHEN e.status = 'completed' THEN e.course_id END) AS completed,
            ROUND(AVG(CASE WHEN qa.score IS NOT NULL THEN qa.score END), 1) AS avg_score,
            MAX(qa.completed_at) AS last_activity
        FROM users u
        LEFT JOIN enrollments e ON u.id = e.user_id
        LEFT JOIN quiz_attempts qa ON u.id = qa.user_id
        WHERE u.is_active = 1
        GROUP BY u.id
        ORDER BY u.name
    """).fetchall()

    members = []
    for r in rows:
        members.append({
            "user_id": r["id"],
            "username": r["username"],
            "name": r["name"] or r["username"],
            "department": r["department"] or "—",
            "role": r["role"],
            "enrolled": r["enrolled"] or 0,
            "completed": r["completed"] or 0,
            "avg_score": r["avg_score"] or 0,
            "last_activity": r["last_activity"] or "—",
            "completion_rate": round((r["completed"] / r["enrolled"] * 100) if r["enrolled"] else 0, 1),
        })

    conn.close()
    return {
        "total_users": total_users,
        "total_courses": total_courses,
        "total_enrollments": total_enrollments,
        "total_completions": total_completions,
        "completion_rate": round((total_completions / total_enrollments * 100) if total_enrollments else 0, 1),
        "members": members,
    }


# ─── Assessment Score Distribution ───────────────────────────────────────────

def get_score_distribution() -> Dict[str, Any]:
    """
    Returns score distribution across all quiz attempts:
    - Histogram buckets (0-10, 10-20, ..., 90-100)
    - Per-course average scores
    - Pass/fail rates
    """
    conn = get_db()
    cur = conn.cursor()

    # All scores
    scores = cur.execute("""
        SELECT qa.score, qa.passed, COALESCE(c.title, qa.course_id) AS course_title
        FROM quiz_attempts qa
        LEFT JOIN courses c ON qa.course_id = c.id
        ORDER BY qa.completed_at DESC
    """).fetchall()

    # Histogram: 10-point buckets
    buckets = {f"{i*10}-{i*10+10}": 0 for i in range(10)}
    pass_count = 0
    fail_count = 0

    for s in scores:
        score = s["score"] or 0
        bucket_idx = min(int(score // 10), 9)
        key = f"{bucket_idx*10}-{bucket_idx*10+10}"
        buckets[key] += 1
        if s["passed"]:
            pass_count += 1
        else:
            fail_count += 1

    # Per-course averages
    course_scores = cur.execute("""
        SELECT
            COALESCE(c.title, qa.course_id) AS course_title,
            COUNT(*) AS attempts,
            ROUND(AVG(qa.score), 1) AS avg_score,
            ROUND(MIN(qa.score), 1) AS min_score,
            ROUND(MAX(qa.score), 1) AS max_score,
            SUM(CASE WHEN qa.passed THEN 1 ELSE 0 END) AS passed_count
        FROM quiz_attempts qa
        LEFT JOIN courses c ON qa.course_id = c.id
        GROUP BY qa.course_id
        ORDER BY avg_score DESC
    """).fetchall()

    per_course = []
    for row in course_scores:
        per_course.append({
            "course": row["course_title"],
            "attempts": row["attempts"],
            "avg_score": row["avg_score"] or 0,
            "min_score": row["min_score"] or 0,
            "max_score": row["max_score"] or 0,
            "pass_rate": round((row["passed_count"] / row["attempts"] * 100) if row["attempts"] else 0, 1),
        })

    conn.close()
    return {
        "total_attempts": len(scores),
        "pass_count": pass_count,
        "fail_count": fail_count,
        "pass_rate": round((pass_count / len(scores) * 100) if scores else 0, 1),
        "distribution": buckets,
        "per_course": per_course,
    }


# ─── Compliance Status ──────────────────────────────────────────────────────

def get_compliance_report() -> Dict[str, Any]:
    """
    Shows mandatory course completion status per user.
    Mandatory = courses where is_mandatory = 1.
    """
    conn = get_db()
    cur = conn.cursor()

    mandatory_courses = cur.execute(
        "SELECT id, title FROM courses WHERE is_mandatory = 1"
    ).fetchall()

    if not mandatory_courses:
        # If no mandatory flag column, treat all courses as trackable
        mandatory_courses = cur.execute("SELECT id, title FROM courses").fetchall()

    active_users = cur.execute(
        "SELECT id, username, name, department FROM users WHERE is_active = 1"
    ).fetchall()

    compliance = []
    total_compliant = 0

    for user in active_users:
        user_courses = []
        all_complete = True
        for mc in mandatory_courses:
            enrollment = cur.execute(
                "SELECT status, progress FROM enrollments WHERE user_id = ? AND course_id = ?",
                (user["id"], mc["id"])
            ).fetchone()

            status = "not_enrolled"
            progress = 0
            if enrollment:
                status = enrollment["status"]
                progress = enrollment["progress"] or 0

            if status != "completed":
                all_complete = False

            user_courses.append({
                "course_id": mc["id"],
                "course_title": mc["title"],
                "status": status,
                "progress": progress,
            })

        if all_complete and len(mandatory_courses) > 0:
            total_compliant += 1

        compliance.append({
            "user_id": user["id"],
            "username": user["username"],
            "name": user["name"] or user["username"],
            "department": user["department"] or "—",
            "courses": user_courses,
            "compliant": all_complete and len(mandatory_courses) > 0,
        })

    conn.close()
    return {
        "mandatory_course_count": len(mandatory_courses),
        "total_users": len(active_users),
        "compliant_users": total_compliant,
        "compliance_rate": round((total_compliant / len(active_users) * 100) if active_users else 0, 1),
        "users": compliance,
    }


# ─── CSV Export ──────────────────────────────────────────────────────────────

def export_team_csv() -> str:
    """Export team overview as CSV string."""
    data = get_team_overview()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Name", "Username", "Department", "Role", "Enrolled", "Completed", "Completion %", "Avg Score", "Last Activity"])
    for m in data["members"]:
        writer.writerow([
            m["name"], m["username"], m["department"], m["role"],
            m["enrolled"], m["completed"], m["completion_rate"],
            m["avg_score"], m["last_activity"]
        ])
    return output.getvalue()


def export_scores_csv() -> str:
    """Export all quiz attempt scores as CSV string."""
    conn = get_db()
    cur = conn.cursor()
    rows = cur.execute("""
        SELECT
            u.name, u.username, u.department,
            COALESCE(c.title, qa.course_id) AS course_title,
            qa.score, qa.percentage,
            qa.passed, qa.time_spent_seconds, qa.completed_at
        FROM quiz_attempts qa
        LEFT JOIN users u ON qa.user_id = u.id
        LEFT JOIN courses c ON qa.course_id = c.id
        ORDER BY qa.completed_at DESC
    """).fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Name", "Username", "Department", "Course", "Score", "Percentage", "Passed", "Time (sec)", "Date"])
    for r in rows:
        writer.writerow([
            r["name"] or r["username"] or "—",
            r["username"] or "—",
            r["department"] or "—",
            r["course_title"],
            r["score"], r["percentage"],
            "Yes" if r["passed"] else "No",
            r["time_spent_seconds"],
            r["completed_at"],
        ])
    return output.getvalue()


def export_compliance_csv() -> str:
    """Export compliance report as CSV string."""
    data = get_compliance_report()
    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    course_titles = [c["course_title"] for c in data["users"][0]["courses"]] if data["users"] else []
    writer.writerow(["Name", "Username", "Department", "Compliant"] + course_titles)

    for u in data["users"]:
        row = [u["name"], u["username"], u["department"], "Yes" if u["compliant"] else "No"]
        for c in u["courses"]:
            row.append(f'{c["status"]} ({c["progress"]}%)')
        writer.writerow(row)

    return output.getvalue()
