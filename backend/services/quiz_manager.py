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

    return f"""You are a senior corporate training assessment designer creating professional certification-level exam questions. Generate exactly 10 comprehensive quiz questions for the course "{course_title}" in the "{category}" category.

Course modules and content:
{module_content}

REQUIREMENTS FOR HIGH-QUALITY QUESTIONS:

1. QUESTION LENGTH: Each question must be detailed and scenario-based when appropriate. Questions should be 2-4 sentences minimum, providing context or a real-world scenario that tests application of knowledge, not just memorization.

2. ANSWER OPTIONS: Each option (A, B, C, D) must be substantive (15-40 words each), plausible, and professionally worded. Avoid obviously wrong "joke" answers.

3. EXPLANATIONS: Each explanation should be 50-100 words, explaining WHY the correct answer is right and briefly why other options are incorrect.

4. QUESTION TYPES: Include scenario-based questions ("In this situation, what should you do..."), knowledge application questions, and policy interpretation questions.

Generate a JSON array of 10 questions. Each question must have:
- "question_text": A detailed question (2-4 sentences, scenario-based preferred)
- "question_type": Either "mcq" (multiple choice) or "true_false"
- "options": Array of 4 substantive options (15-40 words each) for mcq, or ["True", "False"] for true_false
- "correct_answer": The exact text of the correct option
- "explanation": Comprehensive explanation (50-100 words) of why this is correct

Mix 8 MCQ and 2 True/False questions. Make them challenging but fair, testing real understanding.

Respond ONLY with a valid JSON array, no other text. Example format:
[
  {{
    "question_text": "A vendor you've worked with for 3 years sends you a $150 gift basket during the holidays with a note thanking you for the partnership. According to company gift policy, what is the most appropriate course of action to take in this situation?",
    "question_type": "mcq",
    "options": [
      "Accept the gift with gratitude as it falls within the acceptable threshold and strengthens the business relationship with a valued partner",
      "Politely decline the gift, explaining that company policy prohibits accepting gifts over $50, and notify your supervisor within 5 business days",
      "Accept the gift but share it with your entire team to distribute the value and avoid any appearance of personal benefit from the vendor",
      "Accept the gift and report it to HR within 30 days as required by the annual gift disclosure policy for items over $100"
    ],
    "correct_answer": "Politely decline the gift, explaining that company policy prohibits accepting gifts over $50, and notify your supervisor within 5 business days",
    "explanation": "Company gift policy sets a $50 threshold for acceptable gifts from vendors or business partners. Gifts valued between $50-$200 must be disclosed to your supervisor within 5 business days, but gifts should be politely declined when feasible. The $150 value exceeds the acceptance threshold, and while sharing with a team doesn't change the policy violation, the correct action is disclosure and decline to maintain ethical boundaries and avoid any appearance of conflict of interest."
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
        25, 70, len(questions), now  # 25 minutes for comprehensive questions
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
    """Fallback questions if LLM fails - comprehensive professional questions."""
    
    # Course-specific comprehensive question banks
    QUESTION_BANKS = {
        "compliance": [
            {
                "question_text": "During a team meeting, your manager casually mentions that the company will be announcing a major acquisition next week. She says it's 'not public yet' but wanted to give the team a heads up. A colleague later asks if you'd recommend buying company stock given 'all the good news lately.' Based on insider trading regulations and company policy, what is the most appropriate response?",
                "question_type": "mcq",
                "options": [
                    "Share the acquisition information since your colleague is also an employee and has a right to know about company developments that affect their investment decisions",
                    "Politely decline to give investment advice and remind your colleague that employees should not trade on material non-public information, then report the manager's disclosure to compliance",
                    "Suggest waiting until after the announcement to buy stock, but don't explicitly mention the acquisition to avoid technically violating the policy",
                    "Recommend buying the stock since the information will be public soon anyway and your colleague would benefit from acting on publicly available market trends"
                ],
                "correct_answer": "Politely decline to give investment advice and remind your colleague that employees should not trade on material non-public information, then report the manager's disclosure to compliance",
                "explanation": "Insider trading regulations prohibit trading on material non-public information (MNPI). The acquisition news is clearly MNPI, and sharing it or encouraging someone to trade based on it is illegal under SEC regulations. Additionally, the manager's disclosure may have violated company policy on confidential information, which should be reported to compliance. The other options either compound the violation or create the appearance of impropriety even if technically avoiding explicit disclosure."
            },
            {
                "question_text": "You discover that a colleague in the procurement department has been accepting regular lunch invitations from a vendor who is currently bidding on a major contract. While company policy allows accepting meals valued under $75, you've noticed these lunches happen 2-3 times per week and the vendor always pays. What policy concern does this situation raise, and what action should you take?",
                "question_type": "mcq",
                "options": [
                    "No concern exists since each individual meal is under the $75 threshold, so the colleague is technically in compliance with the gift and entertainment policy",
                    "The pattern of frequent meals creates an appearance of impropriety and potential conflict of interest, which should be reported to your supervisor or the ethics hotline for review",
                    "Directly confront your colleague about the ethical implications and demand they stop accepting meals until the contract is awarded",
                    "Wait until the contract is awarded, then report the situation only if the vendor wins, since that would be the only scenario where actual harm occurred"
                ],
                "correct_answer": "The pattern of frequent meals creates an appearance of impropriety and potential conflict of interest, which should be reported to your supervisor or the ethics hotline for review",
                "explanation": "While individual meals may fall under policy thresholds, the cumulative pattern of 2-3 meals weekly from a vendor actively bidding on a contract creates a significant conflict of interest concern. Ethics policies typically address both actual conflicts and the 'appearance of impropriety.' The appropriate action is reporting through proper channels (supervisor or ethics hotline) rather than confronting the colleague directly or waiting to see the outcome. Compliance teams can investigate and determine appropriate action."
            },
            {
                "question_text": "A new data privacy regulation requires your company to implement 'data minimization' practices. Your department has been collecting extensive customer demographic information for years, much of which is never actually used in business operations. According to data privacy best practices and typical regulatory requirements, what does 'data minimization' require your department to do?",
                "question_type": "mcq",
                "options": [
                    "Continue collecting all current data fields but encrypt sensitive information more securely to protect it from unauthorized access",
                    "Stop collecting data that isn't necessary for specific, documented business purposes and establish retention schedules to delete data that's no longer needed",
                    "Archive older data to offline storage systems where it's less accessible but still available for potential future analysis needs",
                    "Anonymize all demographic data by removing names but keeping other identifiers so the data can still be used for analytics purposes"
                ],
                "correct_answer": "Stop collecting data that isn't necessary for specific, documented business purposes and establish retention schedules to delete data that's no longer needed",
                "explanation": "Data minimization is a core principle of regulations like GDPR and CCPA. It requires organizations to collect only data necessary for specific, legitimate purposes and to retain data only as long as needed. Simply encrypting or archiving data doesn't address minimization requirements. Anonymization is a separate concept that may complement minimization but doesn't fulfill the requirement to limit collection. The correct approach involves both limiting new collection and establishing retention schedules for existing data."
            },
            {
                "question_text": "Company policy requires all employees to complete annual compliance training by December 31st. It's December 15th and you notice several team members haven't started their training. As a team lead, you mention this in a meeting and one employee responds: 'I've been doing this job for 15 years and already know everything in that training. It's a waste of my time.' How should you respond to this situation?",
                "question_type": "mcq",
                "options": [
                    "Acknowledge their experience and offer to sign off on their training completion since they clearly already understand the material",
                    "Explain that annual training is mandatory regardless of experience level, as regulations and policies evolve, and offer to help them schedule time to complete it before the deadline",
                    "Escalate immediately to HR to document their non-compliance and potential insubordination before the deadline passes",
                    "Allow them to skip the training this year but make them commit to completing it next year when new content is added"
                ],
                "correct_answer": "Explain that annual training is mandatory regardless of experience level, as regulations and policies evolve, and offer to help them schedule time to complete it before the deadline",
                "explanation": "Compliance training requirements typically apply to all employees regardless of tenure or experience. Regulations change, policies are updated, and refresher training helps maintain awareness. Signing off falsely on training is fraudulent. While the concern should eventually be escalated if the employee refuses, the first approach should be education and support rather than immediate escalation. Allowing exceptions undermines the compliance program and creates legal liability."
            },
            {
                "question_text": "Employees who report potential policy violations or unethical behavior through the company's ethics hotline are protected from retaliation under whistleblower protection policies. This protection applies even if the reported concern ultimately turns out to be unfounded after investigation.",
                "question_type": "true_false",
                "options": ["True", "False"],
                "correct_answer": "True",
                "explanation": "Whistleblower protections cover good-faith reports regardless of whether the reported concern is ultimately substantiated. This is essential because employees might not have access to all information needed to fully evaluate a situation before reporting. The key requirement is that the report is made in good faith—meaning the reporter genuinely believes there may be a violation—not that the report must be proven correct. Protecting good-faith reporters encourages early reporting and helps organizations identify and address issues before they become larger problems."
            },
            {
                "question_text": "Your company uses a third-party cloud provider to store customer data. During a routine review, you discover the provider experienced a data breach three months ago but never notified your company. You only found out by reading a news article. According to data protection best practices and typical breach notification requirements, what should happen next?",
                "question_type": "mcq",
                "options": [
                    "Since the breach already happened months ago and affected the vendor's systems, not yours directly, no action is required on your company's part",
                    "Immediately notify your legal/compliance team, assess whether your customer data was affected, review vendor contracts for breach notification requirements, and potentially notify affected customers and regulators",
                    "Terminate the contract with the vendor immediately and migrate to a new provider before taking any other action to prevent future exposure",
                    "Wait to see if any customers complain about identity theft or fraud before determining whether notification is necessary"
                ],
                "correct_answer": "Immediately notify your legal/compliance team, assess whether your customer data was affected, review vendor contracts for breach notification requirements, and potentially notify affected customers and regulators",
                "explanation": "When a vendor breach potentially affects your customer data, your company maintains responsibility for notification under most data protection regulations (GDPR, CCPA, state breach notification laws). The priority is assessment and appropriate notification, not contract termination (which can be addressed after the immediate response). Waiting for customer complaints is inappropriate—regulations typically require proactive notification within specific timeframes. The vendor's failure to notify may also be a contract violation warranting legal review."
            },
            {
                "question_text": "A colleague asks to borrow your login credentials 'just for a few minutes' because they forgot their password and need to access a system urgently to meet a deadline. They promise to reset their password immediately afterward. Company IT security policy prohibits sharing credentials under any circumstances. What is the most appropriate response?",
                "question_type": "mcq",
                "options": [
                    "Help your colleague by sharing credentials just this once, since the policy exception is reasonable given the urgent business need and short timeframe",
                    "Decline to share credentials and offer to help your colleague contact IT support for an emergency password reset, or offer to complete the urgent task yourself if appropriate",
                    "Share credentials but immediately change your password afterward to minimize the security risk of temporary credential sharing",
                    "Share credentials but document the incident in an email to your manager to create a record that you acted in good faith to help a colleague"
                ],
                "correct_answer": "Decline to share credentials and offer to help your colleague contact IT support for an emergency password reset, or offer to complete the urgent task yourself if appropriate",
                "explanation": "Credential sharing policies exist without exceptions because any sharing creates security vulnerabilities and audit trail issues. If actions are taken using your credentials, you are accountable for them—even if someone else performed them. Most IT departments have emergency password reset procedures for exactly these situations. Documenting a policy violation doesn't make it acceptable. The appropriate response is finding an alternative solution while maintaining security policy compliance."
            },
            {
                "question_text": "During a vendor negotiation, the vendor's representative offers you a personal consulting opportunity on the side—work you'd do in your own time for a separate fee paid directly to you. The work isn't directly related to your current job but uses skills you developed at the company. According to typical conflict of interest policies, how should you handle this offer?",
                "question_type": "mcq",
                "options": [
                    "Accept the opportunity since it's personal work done on your own time and doesn't directly compete with your employer's business",
                    "Decline the offer immediately and disclose it to your supervisor, as accepting personal work from a vendor you do business with creates a conflict of interest regardless of when the work is performed",
                    "Accept the opportunity but recuse yourself from all future negotiations with this vendor to avoid any potential bias in business decisions",
                    "Negotiate a higher rate for the consulting work to compensate for any potential career risk, then decide based on whether the financial benefit outweighs the risk"
                ],
                "correct_answer": "Decline the offer immediately and disclose it to your supervisor, as accepting personal work from a vendor you do business with creates a conflict of interest regardless of when the work is performed",
                "explanation": "Accepting personal financial arrangements from vendors creates clear conflicts of interest. Even if you recuse yourself from negotiations, the relationship creates an appearance of impropriety and raises questions about whether previous or future decisions were influenced. Most corporate ethics policies require disclosure of such offers and prohibit accepting them. The fact that work is done on personal time or uses different skills doesn't eliminate the conflict created by receiving money from a business partner."
            },
            {
                "question_text": "The company's Code of Conduct applies only to full-time employees and does not extend to contractors, consultants, or temporary workers who are technically employed by staffing agencies.",
                "question_type": "true_false",
                "options": ["True", "False"],
                "correct_answer": "False",
                "explanation": "Most corporate Codes of Conduct explicitly extend to all individuals working on behalf of the company, including contractors, consultants, temporary workers, and often even business partners. This broad coverage is necessary because ethical violations by any worker can create legal liability, reputational damage, and workplace harm regardless of their employment classification. Staffing agencies typically require their workers to comply with client company policies as a condition of the assignment."
            },
            {
                "question_text": "You're reviewing expense reports for your team and notice a pattern: one employee consistently submits receipts from the same restaurant for 'client dinners' totaling $200-300 each, always on Friday evenings. You've never heard this employee mention these client meetings, and the 'client names' listed don't appear in your CRM system. Based on expense policy and your supervisory responsibilities, what should you do?",
                "question_type": "mcq",
                "options": [
                    "Approve the expenses since they have receipts attached and the amounts are within policy limits for client entertainment",
                    "Investigate further by asking the employee to provide more details about these client meetings, verify the client names, and if concerns remain, escalate to finance or HR for review",
                    "Deny all the expenses immediately and issue a written warning for potential fraud before conducting any investigation",
                    "Approve this month's expenses to avoid conflict but quietly start monitoring future submissions more closely before taking any action"
                ],
                "correct_answer": "Investigate further by asking the employee to provide more details about these client meetings, verify the client names, and if concerns remain, escalate to finance or HR for review",
                "explanation": "Red flags in expense reports (consistent patterns, unverifiable client names, timing that seems unusual for business purposes) warrant investigation before approval. As a supervisor, you have a duty to verify expense legitimacy. However, investigation should precede accusation—there may be legitimate explanations. Simply approving despite concerns fails your oversight responsibility, while immediate denial without investigation could be unfair if there's a reasonable explanation. The appropriate balance is gathering information before deciding on action."
            }
        ],
        "leadership": [
            {
                "question_text": "You're managing a high-performing team member who has recently started missing deadlines and producing lower-quality work. Other team members have mentioned they've noticed changes in this person's behavior—arriving late, seeming distracted, and being less communicative. As their manager, what is the most effective first step to address this performance change?",
                "question_type": "mcq",
                "options": [
                    "Document the performance issues and schedule a formal performance improvement plan meeting to clearly outline expectations and consequences",
                    "Schedule a private, supportive one-on-one conversation to understand if there are personal or work-related factors affecting their performance before determining next steps",
                    "Address the concerns publicly in a team meeting to set clear expectations and demonstrate that performance standards apply to everyone equally",
                    "Wait another month to see if the issues resolve themselves, as temporary performance dips are normal and often self-correct without intervention"
                ],
                "correct_answer": "Schedule a private, supportive one-on-one conversation to understand if there are personal or work-related factors affecting their performance before determining next steps",
                "explanation": "Sudden performance changes in previously high-performing employees often indicate underlying issues—personal challenges, burnout, workplace concerns, or health issues. Effective leadership requires understanding root causes before jumping to corrective action. A supportive private conversation shows you care about the employee as a person while gathering information needed to determine appropriate support. Formal PIPs may become necessary but shouldn't be the first response. Public discussion is inappropriate and potentially humiliating. Waiting risks allowing problems to worsen."
            },
            {
                "question_text": "Your organization is implementing a significant process change that will affect your team's daily work. You understand the business rationale, but you know several team members will resist because the change increases their short-term workload during the transition. According to change management best practices, what approach is most likely to result in successful adoption?",
                "question_type": "mcq",
                "options": [
                    "Announce the change via email with an implementation date, provide training materials, and expect compliance since it's a business decision from leadership",
                    "Involve team members early by explaining the 'why' behind the change, acknowledging the short-term challenges, soliciting their input on implementation, and providing ongoing support during transition",
                    "Implement the change without prior announcement to prevent resistance from building, then address concerns reactively as they arise",
                    "Delay the change until you can guarantee it won't increase anyone's workload, even if this means missing the business timeline"
                ],
                "correct_answer": "Involve team members early by explaining the 'why' behind the change, acknowledging the short-term challenges, soliciting their input on implementation, and providing ongoing support during transition",
                "explanation": "Research consistently shows that change adoption improves significantly when people understand the reasoning, have their concerns acknowledged, and participate in implementation planning. This approach addresses both rational (understanding the 'why') and emotional (feeling heard and supported) aspects of change acceptance. Top-down mandates often create compliance without commitment. Surprise changes generate mistrust. Indefinite delay to avoid any friction isn't realistic for business needs."
            },
            {
                "question_text": "During a team project, two of your direct reports have a significant disagreement about the approach to take. Both have valid points, and the conflict is starting to affect team morale and project progress. As their manager, what is the most effective way to handle this conflict?",
                "question_type": "mcq",
                "options": [
                    "Make the decision yourself to end the disagreement quickly and keep the project moving forward, then explain your reasoning to both parties",
                    "Meet with each person separately to understand their perspectives, then facilitate a joint discussion focused on project goals and help them find common ground or a hybrid solution",
                    "Let them work it out themselves since conflict resolution is a skill they need to develop, only intervening if it escalates to unprofessional behavior",
                    "Reassign one person to a different project to eliminate the source of conflict and ensure smoother team dynamics going forward"
                ],
                "correct_answer": "Meet with each person separately to understand their perspectives, then facilitate a joint discussion focused on project goals and help them find common ground or a hybrid solution",
                "explanation": "Effective conflict resolution involves understanding all perspectives before facilitating resolution. Individual conversations help you grasp each person's concerns without the pressure of the other party present. A facilitated joint discussion then allows collaborative problem-solving focused on shared goals rather than positional battles. Making decisions for them removes their ownership and learning opportunity. Ignoring the conflict allows it to fester. Reassignment avoids addressing the issue and may not be practical."
            },
            {
                "question_text": "Effective leaders should maintain consistent decision-making approaches regardless of circumstances. Adapting your leadership style to different situations or team members is a sign of inconsistency that undermines trust and credibility.",
                "question_type": "true_false",
                "options": ["True", "False"],
                "correct_answer": "False",
                "explanation": "Situational leadership theory, supported by decades of research, demonstrates that effective leaders adapt their approach based on team member development levels, task complexity, urgency, and other contextual factors. What remains consistent is the leader's values and commitment to their team—not their specific behaviors. A new employee learning a complex task needs more direction than an experienced expert working independently. Flexibility in approach, combined with consistency in principles, builds rather than undermines trust."
            },
            {
                "question_text": "You've recently been promoted to manage a team that includes someone who was also a candidate for your position. This person has more tenure with the company and deep technical expertise, but you were selected for your strategic thinking and cross-functional experience. The team member has been cooperative but somewhat reserved since your promotion. How should you approach this relationship?",
                "question_type": "mcq",
                "options": [
                    "Establish clear authority early by making several decisive decisions without their input to demonstrate why you were selected for the leadership role",
                    "Acknowledge their expertise and disappointment privately, express genuine interest in their perspective, and look for ways to leverage their strengths and include them in decisions where their expertise is valuable",
                    "Treat them exactly like every other team member to avoid any appearance of favoritism or special consideration",
                    "Proactively offer them a promotion to a different team to remove any awkwardness and allow them to advance their career elsewhere"
                ],
                "correct_answer": "Acknowledge their expertise and disappointment privately, express genuine interest in their perspective, and look for ways to leverage their strengths and include them in decisions where their expertise is valuable",
                "explanation": "Managing someone who competed for your role requires emotional intelligence and intentional relationship-building. Acknowledging the situation shows respect and self-awareness. Leveraging their expertise demonstrates you value what they bring and aren't threatened by their knowledge. This approach often converts potential resistance into strong partnership. Asserting dominance creates adversaries. Treating them 'exactly like others' ignores a unique dynamic that needs attention. Offering transfers assumes the relationship can't work and may not be their preference."
            },
            {
                "question_text": "A team member approaches you with an idea for improving a process. After listening, you realize their suggestion has a significant flaw that would actually make things worse. However, this employee rarely speaks up with ideas and you want to encourage more initiative. What is the most effective response?",
                "question_type": "mcq",
                "options": [
                    "Thank them enthusiastically and implement the idea anyway, since encouraging initiative is more important than this particular outcome",
                    "Point out the flaw directly so they learn from the experience and submit better ideas in the future",
                    "Thank them for bringing forward the idea, acknowledge what's good about their thinking, explain the specific concern you see, and invite them to think through how to address it—potentially leading to a better solution",
                    "Tell them you'll consider it and then quietly not implement it to avoid discouraging them with negative feedback"
                ],
                "correct_answer": "Thank them for bringing forward the idea, acknowledge what's good about their thinking, explain the specific concern you see, and invite them to think through how to address it—potentially leading to a better solution",
                "explanation": "Effective leadership balances encouraging initiative with developing critical thinking. Implementing flawed ideas undermines credibility and doesn't actually develop the employee. Direct criticism without acknowledgment discourages future contributions. Avoiding feedback through false acceptance is dishonest and prevents learning. The ideal approach recognizes effort, builds on what's good, shares your concern transparently, and engages them in problem-solving—treating them as a capable adult who can improve their idea."
            },
            {
                "question_text": "You manage a remote team across multiple time zones. One team member consistently participates less in video meetings—camera off, minimal verbal contribution, brief chat messages. Their individual work output remains strong. Is this a performance issue that needs to be addressed?",
                "question_type": "mcq",
                "options": [
                    "Yes, active meeting participation is essential for team collaboration and their behavior sets a poor example regardless of individual output",
                    "Not necessarily—have a private conversation to understand their perspective, as factors like introversion, time zone challenges, or cultural norms may explain the behavior, then assess whether the current pattern actually impacts team outcomes",
                    "No, if their work output is strong there's no reason to address how they participate in meetings since results are what matter",
                    "Yes, require camera-on participation as a non-negotiable team norm to ensure equitable expectations across all team members"
                ],
                "correct_answer": "Not necessarily—have a private conversation to understand their perspective, as factors like introversion, time zone challenges, or cultural norms may explain the behavior, then assess whether the current pattern actually impacts team outcomes",
                "explanation": "Effective remote leadership requires flexibility and understanding individual circumstances. Introverts may contribute better through written channels. Attending meetings at 3 AM in their time zone is exhausting. Some cultures consider extensive verbal participation inappropriate for junior members. Strong work output suggests engagement with job responsibilities. The appropriate first step is understanding rather than assuming the behavior is problematic. However, if the pattern genuinely impacts team dynamics or their own visibility/growth, it's worth addressing thoughtfully."
            },
            {
                "question_text": "Delegating important tasks to team members is primarily about freeing up the manager's time to focus on higher-priority work and strategic activities.",
                "question_type": "true_false",
                "options": ["True", "False"],
                "correct_answer": "False",
                "explanation": "While delegation does free manager time, this perspective misses the more important purpose: developing team members. Effective delegation is a primary vehicle for employee growth, skill-building, and career development. It shows trust, provides stretch opportunities, and builds bench strength for the organization. Managers who delegate only to lighten their own load miss opportunities to grow their people and often delegate only low-value tasks rather than meaningful development experiences."
            },
            {
                "question_text": "Your team has just completed a major project that was ultimately successful but had significant challenges along the way—missed intermediate deadlines, interpersonal conflicts, and last-minute scrambling. Now that it's done, what is the most valuable leadership action to take?",
                "question_type": "mcq",
                "options": [
                    "Celebrate the success and move on quickly to the next project while momentum and morale are high",
                    "Conduct a structured retrospective to identify what worked well and what could improve for future projects, documenting learnings and creating action items for process improvements",
                    "Meet individually with each team member to evaluate their personal performance during the project and document any issues for their performance reviews",
                    "Send a congratulatory email to the team and their senior leaders highlighting the successful outcome without mentioning the challenges"
                ],
                "correct_answer": "Conduct a structured retrospective to identify what worked well and what could improve for future projects, documenting learnings and creating action items for process improvements",
                "explanation": "Retrospectives transform experience into organizational learning. Celebrating success is important but insufficient—without structured reflection, the same problems will recur. The focus should be on process improvement (systems, communication, planning) rather than individual blame. Individual performance feedback is separate from project retrospectives. Sending congratulations without acknowledging challenges internally misses learning opportunities and may feel inauthentic to team members who experienced the difficulties."
            },
            {
                "question_text": "You need to deliver critical feedback to a team member about a presentation that did not go well with senior leadership. They seemed defensive when receiving minor feedback in the past. According to best practices for difficult feedback conversations, what approach is most likely to be effective?",
                "question_type": "mcq",
                "options": [
                    "Soften the message significantly to avoid triggering defensiveness, focusing primarily on positives with only minor mention of areas for improvement",
                    "Deliver the feedback directly but with specificity—describe observed behaviors and impacts rather than character judgments, show that you're invested in their success, and collaborate on improvement strategies",
                    "Send the feedback via email to give them time to process privately and avoid an emotional in-person reaction",
                    "Have a peer deliver the feedback instead since sometimes people accept constructive criticism better from colleagues than from managers"
                ],
                "correct_answer": "Deliver the feedback directly but with specificity—describe observed behaviors and impacts rather than character judgments, show that you're invested in their success, and collaborate on improvement strategies",
                "explanation": "Effective feedback requires psychological safety and clarity. Behavior-specific feedback ('In the presentation, when you...') is less threatening than character judgments ('You're not a good presenter'). Showing investment in their success reframes feedback as support rather than criticism. Collaboration on solutions gives them agency. Softening too much fails to communicate the message. Email avoids necessary dialogue. Peer feedback for performance issues undermines your role and may be inappropriate."
            }
        ],
        "technology": [
            {
                "question_text": "A phishing email arrives in your inbox appearing to be from your company's IT department. It warns that your password will expire in 24 hours and provides a link to 'update your credentials immediately.' The email address shows 'it-support@yourcompany-secure.com' (note the slight domain variation). What is the most appropriate action to take?",
                "question_type": "mcq",
                "options": [
                    "Click the link quickly since password expiration is time-sensitive, but be careful to verify the login page looks legitimate before entering credentials",
                    "Do not click the link, report the email as phishing using your email client's reporting feature or forward it to IT security, and if concerned about your actual password, navigate directly to known company systems to check or update it",
                    "Reply to the email asking if it's legitimate before taking any action on the link",
                    "Ignore the email since if it were really important, IT would call or send a calendar invite"
                ],
                "correct_answer": "Do not click the link, report the email as phishing using your email client's reporting feature or forward it to IT security, and if concerned about your actual password, navigate directly to known company systems to check or update it",
                "explanation": "The email shows classic phishing indicators: urgency, a slightly modified domain (yourcompany-secure.com vs yourcompany.com), and a request for credentials. Never click links in suspicious emails. Replying confirms your email is active and may get a convincing response. Ignoring without reporting allows the attack to potentially succeed against others. The correct approach is reporting (helps IT warn others and block the campaign) and verifying independently by going directly to known legitimate systems rather than through email links."
            },
            {
                "question_text": "You're working from a coffee shop and need to access sensitive company systems. The coffee shop offers free public WiFi. What is the most secure approach for accessing company resources in this situation?",
                "question_type": "mcq",
                "options": [
                    "Use the free WiFi but only access systems that don't require login credentials to minimize exposure of sensitive information",
                    "Connect to the company VPN before accessing any company systems, use HTTPS sites only, and avoid accessing highly sensitive data like financial systems or personal records while on public networks",
                    "Use the free WiFi since most company systems use encryption anyway, making additional precautions unnecessary",
                    "Ask the barista for the WiFi password to confirm it's the official network before connecting and proceeding normally"
                ],
                "correct_answer": "Connect to the company VPN before accessing any company systems, use HTTPS sites only, and avoid accessing highly sensitive data like financial systems or personal records while on public networks",
                "explanation": "Public WiFi networks are inherently insecure—even password-protected ones can be monitored by other connected users or spoofed by attackers ('evil twin' networks). VPNs encrypt your traffic, protecting it from interception. However, highly sensitive data should still be avoided on public networks as defense in depth. HTTPS provides additional transport encryption. Simply avoiding logins isn't practical for most work. Asking for a password doesn't verify network legitimacy—attackers create convincing fake networks."
            },
            {
                "question_text": "Your company recently implemented multi-factor authentication (MFA) for all systems. A colleague complains that entering codes from their authentication app is inconvenient and asks if they can just use SMS text messages instead since that's easier. Based on cybersecurity best practices, how should you respond?",
                "question_type": "mcq",
                "options": [
                    "Agree that SMS would be more convenient and suggest they request an exception from IT for SMS-based authentication",
                    "Explain that while SMS-based MFA is better than no MFA, authentication apps are significantly more secure because SMS can be intercepted through SIM swapping attacks, and the minor inconvenience provides meaningful security benefit",
                    "Tell them any form of MFA is equally secure since the important thing is having a second factor, not which type they use",
                    "Suggest they disable MFA entirely on systems that aren't business-critical to reduce daily friction"
                ],
                "correct_answer": "Explain that while SMS-based MFA is better than no MFA, authentication apps are significantly more secure because SMS can be intercepted through SIM swapping attacks, and the minor inconvenience provides meaningful security benefit",
                "explanation": "Not all MFA is created equal. SMS-based authentication is vulnerable to SIM swapping attacks where attackers convince mobile carriers to transfer a victim's phone number to a new SIM. Authentication apps generate time-based codes locally on your device, making them immune to this attack. While SMS MFA is still better than passwords alone, organizations implement app-based MFA specifically because of these security advantages. Disabling MFA for 'non-critical' systems creates potential access points for attackers."
            },
            {
                "question_text": "You receive a USB drive in the mail labeled 'Q3 Sales Incentive Program Details' with your company's logo on it. You weren't expecting this and don't recognize the sender's department listed on the package. What is the safest action to take?",
                "question_type": "mcq",
                "options": [
                    "Insert the USB drive into your computer to verify its contents and determine if it's legitimate before deciding how to respond",
                    "Do not insert the USB drive into any computer, report the suspicious package to IT security, and verify through known internal channels whether any such mailing was authorized",
                    "Insert the USB drive into a personal computer at home rather than your work computer to protect company systems while checking the contents",
                    "Forward the USB drive to a colleague in the Sales department since the label suggests it was probably meant for them"
                ],
                "correct_answer": "Do not insert the USB drive into any computer, report the suspicious package to IT security, and verify through known internal channels whether any such mailing was authorized",
                "explanation": "Malicious USB drives are a known attack vector ('USB drop attacks'). Attackers mail or leave USB drives that, when inserted, automatically install malware. Company branding can be easily faked. Never insert unknown USB devices into any computer—personal devices aren't 'safe' and can still be compromised and potentially connected to company networks later. Report suspicious items to security and verify through official channels. Don't assume it was a misdirected legitimate mailing without verification."
            },
            {
                "question_text": "Strong passwords should be changed every 30-60 days as a security best practice. The more frequently passwords are changed, the more secure your accounts will be.",
                "question_type": "true_false",
                "options": ["True", "False"],
                "correct_answer": "False",
                "explanation": "Modern security guidance from NIST (National Institute of Standards and Technology) actually recommends against frequent mandatory password changes. Research shows that forced frequent changes lead to predictable password patterns (adding numbers, slight variations) that are easier to crack. Instead, best practices now recommend using strong, unique passwords (ideally managed by a password manager), enabling MFA, and changing passwords only when there's indication of compromise. Length and complexity matter more than change frequency."
            },
            {
                "question_text": "You need to share a confidential document with an external business partner. The document contains sensitive financial projections that shouldn't be widely distributed. What is the most secure method for sharing this information?",
                "question_type": "mcq",
                "options": [
                    "Attach the document to an email since email is encrypted in transit and the partner will receive it directly",
                    "Use your company's approved secure file sharing platform with password protection, expiration dates, and the ability to revoke access if needed, then communicate the access method through a separate channel",
                    "Upload the document to a personal cloud storage account (like personal Google Drive) and share a link, since this avoids company email systems that might be monitored",
                    "Print the document and mail a physical copy to ensure no digital trail exists that could be hacked"
                ],
                "correct_answer": "Use your company's approved secure file sharing platform with password protection, expiration dates, and the ability to revoke access if needed, then communicate the access method through a separate channel",
                "explanation": "Enterprise file sharing platforms provide security controls that email attachments lack: access logging, expiration dates, download limits, and revocation capabilities. Email attachments create permanent copies that can't be recalled and may be forwarded. Personal cloud storage violates data handling policies and removes corporate security controls. Physical mail creates different security risks, can be lost, and isn't practical for business workflows. Sending access credentials through a different channel than the link provides additional security."
            },
            {
                "question_text": "Your company has implemented a Data Loss Prevention (DLP) system that flagged an email you tried to send to a client because it contained a spreadsheet with customer Social Security Numbers. You have a legitimate business need to share this data for a compliance audit. What is the appropriate next step?",
                "question_type": "mcq",
                "options": [
                    "Copy the data into a different format (like a PDF) to avoid triggering the DLP system and resend",
                    "Follow the DLP override process by requesting an exception through proper channels, providing business justification, and using approved secure methods for transmitting sensitive personal data",
                    "Send the email from your personal email account since DLP only monitors company systems",
                    "Remove the Social Security Numbers from the spreadsheet, send it, then call the client and read the numbers over the phone"
                ],
                "correct_answer": "Follow the DLP override process by requesting an exception through proper channels, providing business justification, and using approved secure methods for transmitting sensitive personal data",
                "explanation": "DLP systems exist to prevent accidental or intentional exposure of sensitive data. Circumventing them (format changes, personal email, splitting data across channels) violates their purpose and likely company policy. Legitimate business needs should be addressed through proper exception processes that provide documentation, ensure appropriate authorization, and may specify more secure transmission methods. SSNs are among the most sensitive personal data types; proper handling protections exist for good reason."
            },
            {
                "question_text": "You discover that a coworker has been using the same password for multiple company systems, including critical financial applications. They admit this when you notice them typing the same password repeatedly. According to security best practices, why is this practice dangerous even if the password itself is complex?",
                "question_type": "mcq",
                "options": [
                    "It makes their accounts slightly easier to hack if someone observes them typing, but the main risk is minimal with a complex password",
                    "Password reuse means that if any one system is compromised, attackers can use the same credentials to access all other systems where that password is used, potentially escalating a minor breach into a major incident",
                    "It's primarily a compliance violation rather than a real security risk, since complex passwords are difficult to crack regardless of reuse",
                    "The main problem is that IT systems can detect password reuse and may automatically lock accounts, causing inconvenience"
                ],
                "correct_answer": "Password reuse means that if any one system is compromised, attackers can use the same credentials to access all other systems where that password is used, potentially escalating a minor breach into a major incident",
                "explanation": "Password reuse is a critical vulnerability because breaches are inevitable—no system is 100% secure. When credentials are stolen from one system (even a less-secure third-party service), attackers immediately try those credentials on other valuable targets ('credential stuffing attacks'). A breach of a low-priority system becomes catastrophic if the same password opens financial systems. This is why password managers are recommended—they enable unique passwords for every system without requiring users to remember dozens of complex passwords."
            },
            {
                "question_text": "An employee's laptop is stolen from their car while they're at a restaurant. The laptop has full-disk encryption enabled and requires a password to boot. The employee reports the theft immediately. What is the primary security concern in this scenario?",
                "question_type": "mcq",
                "options": [
                    "The immediate concern is the data on the laptop, which is now accessible to whoever stole it regardless of encryption",
                    "The main concerns are the cost of replacing the laptop and the employee's lost productivity while waiting for a new device",
                    "While the encrypted disk should protect stored data, the stolen device should be reported to IT so any saved credentials, VPN configurations, or authentication certificates can be revoked or reset to prevent potential account access",
                    "Since full-disk encryption is enabled, there are no significant security concerns and the incident is primarily a property loss issue"
                ],
                "correct_answer": "While the encrypted disk should protect stored data, the stolen device should be reported to IT so any saved credentials, VPN configurations, or authentication certificates can be revoked or reset to prevent potential account access",
                "explanation": "Full-disk encryption significantly protects stored data—without the password, the drive contents are inaccessible. However, other security concerns remain: saved WiFi credentials, VPN configurations, browser-saved passwords, authentication certificates, and potentially cached session tokens could provide access to company resources. IT needs to revoke/reset these even though the disk encryption provides a strong first line of defense. The immediate reporting was exactly right; now credential rotation addresses residual risks."
            },
            {
                "question_text": "Artificial intelligence tools like ChatGPT and similar large language models can be safely used for drafting company documents, analyzing data, and improving productivity without any special precautions, since they're just sophisticated word processing tools.",
                "question_type": "true_false",
                "options": ["True", "False"],
                "correct_answer": "False",
                "explanation": "AI tools present several risks requiring precautions: Data entered into prompts may be used to train future models or stored on external servers, creating data privacy/confidentiality concerns. AI can generate incorrect information ('hallucinations') that appears authoritative. Output may incorporate copyrighted material. Many organizations have specific policies governing AI tool use, requiring approved enterprise versions, prohibiting sensitive data input, or requiring human review of outputs. Understanding your company's AI use policy is essential before using these tools for work."
            }
        ],
        "communication": [
            {
                "question_text": "You're preparing to deliver difficult news to your team: a project they've worked on for six months is being cancelled due to strategic prioritization changes from senior leadership. The team has invested significant effort and will likely be disappointed. According to communication best practices, what approach should you take when delivering this news?",
                "question_type": "mcq",
                "options": [
                    "Soften the news by emphasizing that the project 'may' be put on hold rather than cancelled, to reduce immediate emotional impact",
                    "Be direct and honest about the cancellation, acknowledge the team's hard work and likely disappointment, explain the business rationale as clearly as possible, and provide space for questions and reactions",
                    "Deliver the news via email to give team members time to process privately before any group discussion",
                    "Focus entirely on the positive opportunity to move to new projects rather than dwelling on the cancellation of the old one"
                ],
                "correct_answer": "Be direct and honest about the cancellation, acknowledge the team's hard work and likely disappointment, explain the business rationale as clearly as possible, and provide space for questions and reactions",
                "explanation": "Difficult news requires direct, honest communication that respects people's emotional responses. Softening creates false hope and erodes trust when the full truth emerges. Email avoids necessary human connection during difficult moments and prevents real-time support. Forced positivity invalidates legitimate feelings and can feel dismissive. Effective communication acknowledges reality, explains reasoning (even if the decision was made above you), and creates space for people to process and ask questions."
            },
            {
                "question_text": "You're in a meeting where a colleague presents an idea. You have concerns about the approach but notice several senior leaders seem enthusiastic. The meeting facilitator asks if anyone has questions or concerns. According to effective communication principles, what should you do?",
                "question_type": "mcq",
                "options": [
                    "Stay quiet during the meeting to avoid publicly contradicting senior leaders, then share your concerns privately with your manager afterward",
                    "Raise your concerns professionally and constructively, framing them as questions to explore ('Have we considered how this might affect X?') rather than direct opposition, contributing to better decision-making even if others seem aligned",
                    "Wait to see if anyone else raises concerns first, only speaking up if someone else breaks the ice",
                    "Express strong opposition immediately to ensure your disagreement is clearly on record before the decision moves forward"
                ],
                "correct_answer": "Raise your concerns professionally and constructively, framing them as questions to explore ('Have we considered how this might affect X?') rather than direct opposition, contributing to better decision-making even if others seem aligned",
                "explanation": "Healthy organizations value constructive dissent. Speaking up when you have legitimate concerns, even if it feels uncomfortable, contributes to better decisions and demonstrates professional courage. Framing concerns as exploratory questions invites discussion rather than creating adversarial dynamics. Staying silent allows potentially flawed decisions to proceed unchallenged. Strong opposition without diplomatic framing can seem aggressive and shut down dialogue. Contributing your perspective, even as the minority voice, is valuable."
            },
            {
                "question_text": "A colleague sends you an email that feels critical of your work. You feel defensive and want to respond immediately to correct what you perceive as unfair characterizations. What communication approach is most likely to lead to a productive outcome?",
                "question_type": "mcq",
                "options": [
                    "Respond immediately while the details are fresh, making sure to address each point they raised and clarify the facts",
                    "Take time to calm down, re-read the email to check whether it's as critical as it first seemed, consider their possible perspective, then either respond thoughtfully or suggest a direct conversation to resolve any misunderstanding",
                    "Forward the email to your manager to document the colleague's unprofessional communication",
                    "Reply all to ensure transparency and allow others to see your perspective and weigh in on who is correct"
                ],
                "correct_answer": "Take time to calm down, re-read the email to check whether it's as critical as it first seemed, consider their possible perspective, then either respond thoughtfully or suggest a direct conversation to resolve any misunderstanding",
                "explanation": "Emotional responses often misread tone in written communication—emails lack vocal cues and can seem harsher than intended. Immediate defensive responses tend to escalate conflict. Taking time allows emotional regulation and more objective re-reading. Often, messages seem less critical on second read. If genuine concerns remain, a direct conversation usually resolves misunderstandings faster than email exchanges. Escalating to managers or expanding the audience typically worsens relationships and isn't warranted for normal workplace friction."
            },
            {
                "question_text": "During a video conference with a global team spanning multiple time zones, you notice that one team member (joining at an inconvenient hour in their time zone) has their camera off and hasn't spoken. When you ask for their input, they give a very brief response. According to inclusive communication practices, how should you interpret and handle this situation?",
                "question_type": "mcq",
                "options": [
                    "Interpret the brief responses as disengagement and address it directly in the meeting by asking if they're paying attention",
                    "Recognize that time zone challenges, cultural differences in meeting participation styles, and camera fatigue may all contribute to their behavior; follow up individually after the meeting to ensure their input is captured and check if the meeting format works for them",
                    "Accept that some team members will be less engaged in global meetings and focus your attention on those who are actively participating",
                    "Require all team members to have cameras on during meetings to ensure equal participation standards regardless of time zone"
                ],
                "correct_answer": "Recognize that time zone challenges, cultural differences in meeting participation styles, and camera fatigue may all contribute to their behavior; follow up individually after the meeting to ensure their input is captured and check if the meeting format works for them",
                "explanation": "Inclusive leadership recognizes that equal participation looks different across contexts. Attending meetings at difficult hours is already significant effort. Some cultures consider brief, deferential responses appropriate in group settings. Camera fatigue is real. Rather than making assumptions or calling people out publicly, effective inclusion involves private follow-up that demonstrates you value their input and want to understand how to better include them. This may lead to insights about improving global meeting practices for everyone."
            },
            {
                "question_text": "The most effective communicators adjust their message based on their audience—using different language, emphasis, and level of detail depending on whether they're speaking to technical experts, senior executives, or front-line employees.",
                "question_type": "true_false",
                "options": ["True", "False"],
                "correct_answer": "True",
                "explanation": "Audience adaptation is a core communication skill. Technical experts need different depth and terminology than executives who need strategic context and business implications. Front-line employees may need different framing than corporate staff. Effective communicators maintain message consistency while adapting presentation. This isn't being inauthentic—it's being effective by recognizing that different audiences have different needs, knowledge bases, and concerns that affect how they receive information."
            },
            {
                "question_text": "Your manager asks you to send a project status update to senior leadership. The project has achieved its main milestones but has also encountered significant challenges that required creative problem-solving. How should you frame the communication?",
                "question_type": "mcq",
                "options": [
                    "Focus entirely on achievements and omit mention of challenges, since executives prefer positive updates and don't need to know about problems that were solved",
                    "Present a balanced view that highlights achievements, acknowledges challenges faced, explains how they were addressed, and notes any remaining risks—giving leadership an accurate picture while demonstrating professional problem-solving",
                    "Lead with all the challenges to demonstrate the difficulty of the work, then mention the achievements as evidence of the team's ability to overcome obstacles",
                    "Provide only raw data and metrics without interpretation, letting leadership draw their own conclusions about project status"
                ],
                "correct_answer": "Present a balanced view that highlights achievements, acknowledges challenges faced, explains how they were addressed, and notes any remaining risks—giving leadership an accurate picture while demonstrating professional problem-solving",
                "explanation": "Executive communication should be honest and complete while being strategically framed. Omitting challenges creates an inaccurate picture and may backfire if issues later emerge—damaging credibility. Leading with problems sets a negative tone. Raw data without context requires executives to do interpretive work. Balanced communication demonstrates professionalism: we achieved X, we faced Y challenges and handled them by Z, here's what to watch going forward. This approach is both honest and strategically smart."
            },
            {
                "question_text": "You receive feedback from a peer that your emails are often perceived as curt or unfriendly, although you don't intend them that way. You typically write brief, efficient emails to respect everyone's time. How should you approach improving your written communication?",
                "question_type": "mcq",
                "options": [
                    "Ignore the feedback since your intentions are good and people should interpret your emails based on your track record rather than individual messages",
                    "Experiment with small additions that soften tone without significantly increasing length—greetings, acknowledgments, and brief courteous phrases that signal warmth while remaining efficient",
                    "Start writing much longer, detailed emails with extensive pleasantries to ensure no one could possibly perceive them as curt",
                    "Switch to phone calls or video chats instead of email to avoid the problem of written tone being misinterpreted"
                ],
                "correct_answer": "Experiment with small additions that soften tone without significantly increasing length—greetings, acknowledgments, and brief courteous phrases that signal warmth while remaining efficient",
                "explanation": "Email lacks tone cues, making brief messages easy to misread as curt even when efficiency is the intent. Small adjustments—using names, adding brief warm phrases ('Thanks for the quick turnaround'), using greetings—significantly affect perception without undermining efficiency. Ignoring feedback means continuing to create unintended impressions. Overcompensating with lengthy emails trades one problem for another. Avoiding email entirely isn't practical. The goal is finding the balance between efficient and warm."
            },
            {
                "question_text": "Active listening involves primarily waiting silently while the other person speaks, then formulating your response once they've finished. The key to being a good listener is to say as little as possible.",
                "question_type": "true_false",
                "options": ["True", "False"],
                "correct_answer": "False",
                "explanation": "Active listening is far more than silent waiting—it involves engaged behaviors that demonstrate understanding and encourage elaboration: asking clarifying questions, paraphrasing to confirm understanding, acknowledging emotions, providing relevant responses that build on what was shared. Pure silence can actually signal disengagement or disinterest. Effective listeners participate in dialogue, showing they're processing and valuing what's being communicated while allowing appropriate space for the speaker."
            },
            {
                "question_text": "You need to communicate a complex policy change that affects different employee groups in different ways. Some employees will see benefits while others will face new restrictions. What communication approach best handles this complexity?",
                "question_type": "mcq",
                "options": [
                    "Send one company-wide communication with all details to ensure everyone receives the same information simultaneously",
                    "Create targeted communications for different affected groups, addressing their specific situations, concerns, and benefits, while ensuring message consistency across communications",
                    "Communicate only the general policy change and let managers handle explaining specific impacts to their teams",
                    "Start with the groups most positively affected to build momentum and positive word-of-mouth before reaching those who may be more resistant"
                ],
                "correct_answer": "Create targeted communications for different affected groups, addressing their specific situations, concerns, and benefits, while ensuring message consistency across communications",
                "explanation": "Complex changes affecting different groups differently benefit from tailored communications that address each audience's specific situation. One-size-fits-all messages often bury relevant details within irrelevant information. Delegating entirely to managers creates inconsistency and information gaps. Sequencing by predicted reaction can create perception of manipulation when those notified later learn others knew first. Consistent core messaging with audience-tailored framing and details is most effective."
            },
            {
                "question_text": "A colleague repeatedly interrupts you during team meetings, making it difficult to complete your thoughts. You've noticed this pattern over several meetings. How should you address this communication challenge?",
                "question_type": "mcq",
                "options": [
                    "Call out the behavior publicly in the next meeting when it happens: 'Please let me finish before you respond'",
                    "Have a private conversation with the colleague, describe the specific behavior you've observed without accusation, explain its impact on you, and work together on a solution",
                    "Stop attempting to contribute in meetings since the interruptions make participation too frustrating",
                    "Send an email to the meeting organizer requesting that they moderate the discussion more strictly"
                ],
                "correct_answer": "Have a private conversation with the colleague, describe the specific behavior you've observed without accusation, explain its impact on you, and work together on a solution",
                "explanation": "Pattern behaviors are best addressed directly but privately with the individual. Public callouts can embarrass and create defensive reactions. Private conversation allows honest discussion—the colleague may not realize they're interrupting or may have a different perspective on the interactions. Collaborative problem-solving ('How can we make sure we both get to share our thoughts?') is more effective than demands. Withdrawing from participation cedes important professional ground. Escalating to organizers before attempting direct communication skips important steps."
            }
        ]
    }
    
    # Determine which question bank to use based on category
    category_lower = category.lower()
    questions = []
    
    if "compliance" in category_lower or "policy" in category_lower or "ethics" in category_lower:
        questions = QUESTION_BANKS.get("compliance", [])
    elif "leader" in category_lower or "management" in category_lower:
        questions = QUESTION_BANKS.get("leadership", [])
    elif "tech" in category_lower or "security" in category_lower or "it" in category_lower or "cyber" in category_lower:
        questions = QUESTION_BANKS.get("technology", [])
    elif "communi" in category_lower or "soft skill" in category_lower or "present" in category_lower:
        questions = QUESTION_BANKS.get("communication", [])
    else:
        # Default to compliance questions
        questions = QUESTION_BANKS.get("compliance", [])
    
    # Return up to 10 questions
    return questions[:10]


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
