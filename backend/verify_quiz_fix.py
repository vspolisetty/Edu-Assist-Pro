#!/usr/bin/env python3
"""Verify quiz fix worked"""
import sqlite3
import re
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'courses.db')

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
cursor.execute("SELECT content FROM modules WHERE title='Company Policies Overview'")
content = cursor.fetchone()[0]

# Check for remaining markers
checkmark = '\u2705'  # ✅
square = '\u2b1c'     # ⬜  
circle = '\u25cb'     # ○

print("Checking for old markers...")
if checkmark in content:
    # Count occurrences
    count = content.count(checkmark)
    print(f"  Still has {count} checkmark markers")
else:
    print("  No checkmark markers (good!)")
    
if square in content:
    count = content.count(square)
    print(f"  Still has {count} square markers")
else:
    print("  No square markers (good!)")

if circle in content:
    count = content.count(circle)
    print(f"  Still has {count} circle markers")  
else:
    print("  No circle markers (good!)")

print("\nChecking for interactive classes...")
if 'quiz-option' in content:
    count = content.count('quiz-option')
    print(f"  Has {count} quiz-option elements")
if 'data-correct="true"' in content:
    count = content.count('data-correct="true"')
    print(f"  Has {count} correct answer markers")
if 'data-correct="false"' in content:
    count = content.count('data-correct="false"')
    print(f"  Has {count} incorrect answer markers")

# Show sample
match = re.search(r'<li class="quiz-option"[^>]*>[^<]+</li>', content)
if match:
    print("\nSample quiz option HTML:")
    print(match.group(0))
    
conn.close()
