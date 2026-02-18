#!/usr/bin/env python3
"""
Fix all in-module quizzes/scenarios to be truly interactive.
Removes ✅ and ⬜ markers and converts to proper quiz-option format.
"""
import sqlite3
import re
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'courses.db')

def transform_content(content: str) -> str:
    """Transform in-module quizzes to be interactive without showing answers."""
    if not content:
        return content
    
    # Pattern 1: Replace ✅ markers (correct answers) with quiz-option data-correct="true"
    # e.g., <li ...>✅ B. Answer text</li> -> <li class="quiz-option" data-correct="true" ...>B. Answer text</li>
    def replace_correct_li(match):
        full = match.group(0)
        # Extract style if present
        style_match = re.search(r'style="([^"]*)"', full)
        style = style_match.group(1) if style_match else "margin:6px 0;padding:10px 14px;background:#fff;border-radius:6px"
        # Extract the answer text (remove ✅ and whitespace)
        text_match = re.search(r'>✅\s*([A-D]\..*?)</li>', full, re.DOTALL)
        if text_match:
            text = text_match.group(1).strip()
            return f'<li class="quiz-option" data-correct="true" style="{style}">{text}</li>'
        return full
    
    # Pattern 2: Replace ⬜ markers (wrong answers) with quiz-option data-correct="false"
    def replace_wrong_li(match):
        full = match.group(0)
        style_match = re.search(r'style="([^"]*)"', full)
        style = style_match.group(1) if style_match else "margin:6px 0;padding:10px 14px;background:#fff;border-radius:6px"
        text_match = re.search(r'>⬜\s*([A-D]\..*?)</li>', full, re.DOTALL)
        if text_match:
            text = text_match.group(1).strip()
            return f'<li class="quiz-option" data-correct="false" style="{style}">{text}</li>'
        return full
    
    # Pattern 3: Replace ○ markers (knowledge check wrong answers)
    def replace_circle_li(match):
        full = match.group(0)
        style_match = re.search(r'style="([^"]*)"', full)
        style = style_match.group(1) if style_match else "margin:4px 0"
        text_match = re.search(r'>○\s*([A-D]\..*?)</li>', full, re.DOTALL)
        if text_match:
            text = text_match.group(1).strip()
            return f'<li class="quiz-option" data-correct="false" style="{style}">{text}</li>'
        return full
    
    # Pattern 4: Handle knowledge check ✅ markers (different format)
    def replace_kc_correct(match):
        full = match.group(0)
        style_match = re.search(r'style="([^"]*)"', full)
        style = style_match.group(1) if style_match else "margin:4px 0"
        # Match both ✅ A. and just ✅ B. patterns
        text_match = re.search(r'>✅\s*([A-D]\..*?)</li>', full, re.DOTALL)
        if text_match:
            text = text_match.group(1).strip()
            return f'<li class="quiz-option" data-correct="true" style="{style}">{text}</li>'
        return full
    
    # Apply all transformations
    # First: ✅ markers (correct answers)
    content = re.sub(r'<li[^>]*>✅\s*[A-D]\.[^<]*</li>', replace_correct_li, content)
    
    # Second: ⬜ markers (wrong answers)  
    content = re.sub(r'<li[^>]*>⬜\s*[A-D]\.[^<]*</li>', replace_wrong_li, content)
    
    # Third: ○ markers (knowledge check wrong)
    content = re.sub(r'<li[^>]*>○\s*[A-D]\.[^<]*</li>', replace_circle_li, content)
    
    # Add quiz-container class to parent ULs that contain quiz-option items
    # This is a simpler approach - just mark the ULs
    def wrap_quiz_ul(match):
        ul_html = match.group(0)
        if 'quiz-container' not in ul_html:
            ul_html = ul_html.replace('<ul', '<ul class="quiz-container"', 1)
        return ul_html
    
    content = re.sub(
        r'<ul[^>]*>(?:(?!</ul>).)*quiz-option(?:(?!</ul>).)*</ul>',
        wrap_quiz_ul,
        content,
        flags=re.DOTALL
    )
    
    return content

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all modules with content
    cursor.execute("SELECT id, title, content FROM modules WHERE content IS NOT NULL")
    modules = cursor.fetchall()
    
    updated = 0
    for mod_id, title, content in modules:
        if not content:
            continue
        
        # Check if this module has quiz markers to fix
        if '✅' in content or '⬜' in content or '○' in content:
            new_content = transform_content(content)
            
            if new_content != content:
                cursor.execute(
                    "UPDATE modules SET content = ? WHERE id = ?",
                    (new_content, mod_id)
                )
                updated += 1
                print(f"✅ Fixed: {title}")
    
    conn.commit()
    conn.close()
    print(f"\n🎯 Total modules fixed: {updated}")
    print("📝 In-module quizzes are now interactive (answers hidden until clicked)")

if __name__ == "__main__":
    main()
