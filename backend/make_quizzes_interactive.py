#!/usr/bin/env python3
"""
Make all knowledge check quizzes interactive by:
1. Replacing ✅ markers with data-correct attributes
2. Wrapping quizzes in proper interactive quiz containers
"""
import sqlite3
import re
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'courses.db')

def transform_content(content: str) -> str:
    """Transform knowledge check HTML to be interactive."""
    if not content:
        return content
    
    # Pattern to find quiz option list items with ✅ markers (correct answers)
    # Example: <li style="...">✅ B. $50</li>
    def replace_correct_option(match):
        full_match = match.group(0)
        # Extract the style if present
        style_match = re.search(r'style="([^"]*)"', full_match)
        style = style_match.group(1) if style_match else "margin:4px 0"
        
        # Extract the text content (remove ✅ and whitespace)
        text_match = re.search(r'>✅\s*(.*?)</li>', full_match, re.DOTALL)
        if text_match:
            text = text_match.group(1).strip()
            return f'<li class="quiz-option" data-correct="true" style="{style}">{text}</li>'
        return full_match
    
    # Pattern to find quiz option list items without ✅ (incorrect answers)
    def replace_incorrect_option(match):
        full_match = match.group(0)
        # Skip if already has quiz-option class or data-correct
        if 'quiz-option' in full_match or 'data-correct' in full_match:
            return full_match
        # Skip if has ✅ (will be handled by correct option replacer)
        if '✅' in full_match:
            return full_match
        
        # Extract the style if present
        style_match = re.search(r'style="([^"]*)"', full_match)
        style = style_match.group(1) if style_match else "margin:4px 0"
        
        # Extract the text content
        text_match = re.search(r'>([A-D]\.\s.*?)</li>', full_match, re.DOTALL)
        if text_match:
            text = text_match.group(1).strip()
            return f'<li class="quiz-option" data-correct="false" style="{style}">{text}</li>'
        return full_match
    
    # First, replace correct options (those with ✅)
    content = re.sub(
        r'<li[^>]*>✅\s*[A-D]\.[^<]*</li>',
        replace_correct_option,
        content
    )
    
    # Then, find and replace incorrect options in quiz contexts
    # Look for list items that follow a Knowledge Check heading
    # Pattern: li items that have A. B. C. D. format within quiz sections
    
    # Find all quiz sections and transform their options
    def transform_quiz_section(match):
        section = match.group(0)
        # Replace any remaining non-quiz-option li items with A. B. C. D. format
        def add_quiz_class(li_match):
            li = li_match.group(0)
            if 'quiz-option' in li:
                return li
            style_match = re.search(r'style="([^"]*)"', li)
            style = style_match.group(1) if style_match else "margin:4px 0"
            text_match = re.search(r'>([A-D]\.\s*[^<]+)</li>', li)
            if text_match:
                text = text_match.group(1).strip()
                return f'<li class="quiz-option" data-correct="false" style="{style}">{text}</li>'
            return li
        
        section = re.sub(r'<li[^>]*>[A-D]\.[^<]*</li>', add_quiz_class, section)
        return section
    
    # Transform sections that contain "Knowledge Check" or "Scenario"
    content = re.sub(
        r'<div[^>]*>(?:(?!</div>).)*Knowledge Check(?:(?!</div>).)*</div>',
        transform_quiz_section,
        content,
        flags=re.DOTALL | re.IGNORECASE
    )
    
    # Also handle scenario exercises with questions
    content = re.sub(
        r'<div[^>]*>(?:(?!</div>).)*Scenario(?:(?!</div>).)*</div>',
        transform_quiz_section,
        content,
        flags=re.DOTALL | re.IGNORECASE
    )
    
    # Wrap UL elements containing quiz-option items in a quiz-container
    def wrap_quiz_ul(match):
        ul_content = match.group(0)
        if 'quiz-container' not in ul_content:
            # Add wrapper class to the ul
            ul_content = ul_content.replace('<ul', '<ul class="quiz-container"', 1)
        return ul_content
    
    content = re.sub(
        r'<ul[^>]*>(?:(?!</ul>).)*quiz-option(?:(?!</ul>).)*</ul>',
        wrap_quiz_ul,
        content,
        flags=re.DOTALL
    )
    
    # Remove any remaining ✅ from option text (cleanup)
    content = re.sub(r'(quiz-option[^>]*>)✅\s*', r'\1', content)
    
    # Hide "Correct Answer:" text by wrapping it
    content = re.sub(
        r'<p><strong>(Correct Answer:[^<]*)</strong></p>',
        r'<p class="quiz-answer-reveal" style="display:none"><strong>\1</strong></p>',
        content
    )
    
    return content

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Get all modules
    cursor.execute("SELECT id, title, content FROM modules WHERE content IS NOT NULL")
    modules = cursor.fetchall()
    
    updated = 0
    for mod_id, title, content in modules:
        if not content:
            continue
        
        # Check if this module has knowledge checks
        if 'Knowledge Check' in content or '✅' in content:
            new_content = transform_content(content)
            
            if new_content != content:
                cursor.execute(
                    "UPDATE modules SET content = ? WHERE id = ?",
                    (new_content, mod_id)
                )
                updated += 1
                print(f"✅ Updated: {title}")
    
    conn.commit()
    conn.close()
    print(f"\n🎯 Total modules updated: {updated}")

if __name__ == "__main__":
    main()
