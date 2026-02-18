#!/usr/bin/env python3
"""
Clear existing quizzes to force regeneration with improved comprehensive questions.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "courses.db")

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Count existing quizzes
    cursor.execute("SELECT COUNT(*) FROM quizzes")
    quiz_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM quiz_questions")
    question_count = cursor.fetchone()[0]
    
    print(f"Found {quiz_count} quizzes with {question_count} questions")
    
    # Delete all quiz data (will regenerate with new comprehensive questions)
    cursor.execute("DELETE FROM quiz_questions")
    cursor.execute("DELETE FROM quizzes")
    
    conn.commit()
    conn.close()
    
    print(f"✅ Cleared {quiz_count} quizzes and {question_count} questions")
    print("🔄 Quizzes will regenerate with comprehensive questions when users access assessments")

if __name__ == "__main__":
    main()
