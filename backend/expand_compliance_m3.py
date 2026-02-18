"""
Expand Module 3: Anti-Harassment Training (~25K chars target)
"""
import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), "courses.db")

CONTENT = """
<h2>Anti-Harassment Training</h2>

<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:20px 0;background:linear-gradient(135deg,#dc262608,#dc262603);border-radius:12px;padding:16px">
  <div style="text-align:center;padding:16px"><div style="font-size:32px">⚖️</div><div style="font-size:1.5rem;font-weight:700;color:#dc2626">1 in 3</div><div style="font-size:.8rem;color:#64748b">Workers Experience Harassment</div></div>
  <div style="text-align:center;padding:16px"><div style="font-size:32px">🔇</div><div style="font-size:1.5rem;font-weight:700;color:#dc2626">75%</div><div style="font-size:.8rem;color:#64748b">Go Unreported</div></div>
  <div style="text-align:center;padding:16px"><div style="font-size:32px">💰</div><div style="font-size:1.5rem;font-weight:700;color:#dc2626">$1B+</div><div style="font-size:.8rem;color:#64748b">Annual EEOC Settlements</div></div>
  <div style="text-align:center;padding:16px"><div style="font-size:32px">🚫</div><div style="font-size:1.5rem;font-weight:700;color:#dc2626">Zero</div><div style="font-size:.8rem;color:#64748b">Tolerance Policy</div></div>
</div>

<img src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=800&h=400&fit=crop" alt="Diverse professional workplace team" style="width:100%;border-radius:12px;margin:20px 0;box-shadow:0 4px 12px rgba(0,0,0,0.1)">

<h3>🎯 Learning Objectives</h3>
<p>By the end of this module, you will be able to:</p>
<ul>
  <li>Define workplace harassment and identify its various forms</li>
  <li>Recognize subtle and overt harassment behaviors</li>
  <li>Understand the legal framework that protects employees</li>
  <li>Apply bystander intervention techniques safely and effectively</li>
  <li>Report incidents through appropriate channels with confidence</li>
  <li>Support colleagues who have experienced harassment</li>
</ul>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>📚 What Is Workplace Harassment?</h3>

<p>Workplace harassment is <strong>any unwelcome conduct based on protected characteristics</strong> that creates a hostile, intimidating, offensive, or abusive work environment. It can come from supervisors, coworkers, clients, vendors, or anyone in the workplace.</p>

<p>Harassment becomes illegal when:</p>
<ul>
  <li>Enduring the offensive conduct becomes a condition of continued employment, OR</li>
  <li>The conduct is severe or pervasive enough to create a work environment that a reasonable person would consider intimidating, hostile, or abusive</li>
</ul>

<div style="background:linear-gradient(135deg,#dc262608,#dc262603);border-left:4px solid #dc2626;padding:20px 24px;margin:24px 0;border-radius:0 10px 10px 0">
  <strong style="display:flex;align-items:center;gap:8px;margin-bottom:8px">⚖️ Legal Protected Classes</strong>
  <div style="font-size:.92rem;line-height:1.7">Under federal law (Title VII, ADA, ADEA), harassment is prohibited based on: <strong>Race, Color, Religion, Sex (including pregnancy, gender identity, sexual orientation), National Origin, Age (40+), Disability, Genetic Information</strong>. Many states add additional protections including marital status, military status, and political affiliation.</div>
</div>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>🔍 Types of Workplace Harassment</h3>

<h4>Understanding the Two Legal Categories</h4>

<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:20px;margin:24px 0">
  <div style="background:linear-gradient(135deg,#ef444408,#ef444402);border:2px solid #fca5a5;padding:24px;border-radius:12px">
    <div style="font-size:36px;margin-bottom:12px">⚠️</div>
    <h4 style="margin:0 0 12px 0;color:#dc2626">Quid Pro Quo</h4>
    <p style="margin:0;font-size:.9rem;line-height:1.6;color:#475569">"This for that" — When employment decisions (hiring, promotion, raises) are conditioned on submission to unwelcome conduct, typically of a sexual nature.</p>
    <ul style="margin:12px 0 0 0;padding-left:20px;font-size:.85rem;color:#64748b">
      <li>"I'll give you a promotion if you go out with me"</li>
      <li>"You'll get the best shifts if you're nice to me"</li>
      <li>Implied threats for rejecting advances</li>
    </ul>
  </div>
  <div style="background:linear-gradient(135deg,#f9731608,#f9731602);border:2px solid #fdba74;padding:24px;border-radius:12px">
    <div style="font-size:36px;margin-bottom:12px">🌪️</div>
    <h4 style="margin:0 0 12px 0;color:#ea580c">Hostile Work Environment</h4>
    <p style="margin:0;font-size:.9rem;line-height:1.6;color:#475569">Conduct that is severe or pervasive enough to create an intimidating, hostile, or offensive work environment that interferes with work performance.</p>
    <ul style="margin:12px 0 0 0;padding-left:20px;font-size:.85rem;color:#64748b">
      <li>Repeated offensive jokes or comments</li>
      <li>Displaying offensive images or materials</li>
      <li>Persistent unwelcome attention</li>
      <li>Physical intimidation or threats</li>
    </ul>
  </div>
</div>

<h4>Forms of Harassment</h4>

<table style="width:100%;border-collapse:collapse;margin:16px 0">
  <tr style="background:#f8fafc"><th style="padding:12px;text-align:left;border:1px solid #e2e8f0">Form</th><th style="padding:12px;text-align:left;border:1px solid #e2e8f0">Examples</th><th style="padding:12px;text-align:left;border:1px solid #e2e8f0">Impact</th></tr>
  <tr><td style="padding:12px;border:1px solid #e2e8f0"><strong>💬 Verbal</strong></td><td style="padding:12px;border:1px solid #e2e8f0">Slurs, insults, threats, offensive jokes, unwelcome comments about appearance</td><td style="padding:12px;border:1px solid #e2e8f0">Emotional distress, anxiety, fear</td></tr>
  <tr><td style="padding:12px;border:1px solid #e2e8f0"><strong>✋ Physical</strong></td><td style="padding:12px;border:1px solid #e2e8f0">Unwanted touching, blocking movement, physical intimidation, assault</td><td style="padding:12px;border:1px solid #e2e8f0">Physical harm, trauma, fear</td></tr>
  <tr><td style="padding:12px;border:1px solid #e2e8f0"><strong>👁️ Visual</strong></td><td style="padding:12px;border:1px solid #e2e8f0">Offensive images, gestures, staring, displaying inappropriate materials</td><td style="padding:12px;border:1px solid #e2e8f0">Discomfort, humiliation</td></tr>
  <tr><td style="padding:12px;border:1px solid #e2e8f0"><strong>💻 Digital/Cyber</strong></td><td style="padding:12px;border:1px solid #e2e8f0">Offensive emails/texts, social media harassment, inappropriate messages</td><td style="padding:12px;border:1px solid #e2e8f0">24/7 exposure, documentation trail</td></tr>
  <tr><td style="padding:12px;border:1px solid #e2e8f0"><strong>🚫 Exclusionary</strong></td><td style="padding:12px;border:1px solid #e2e8f0">Deliberately excluding from meetings, social events, information, opportunities</td><td style="padding:12px;border:1px solid #e2e8f0">Isolation, career damage</td></tr>
</table>

<img src="https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=800&h=350&fit=crop" alt="Professional workplace communication" style="width:100%;border-radius:12px;margin:20px 0;box-shadow:0 4px 12px rgba(0,0,0,0.1)">

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>🚩 Recognizing Harassment: Red Flags</h3>

<p>Harassment isn't always obvious. Here are warning signs to watch for:</p>

<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:16px;margin:24px 0">
  <div style="background:#fef2f2;padding:20px;border-radius:10px">
    <strong style="color:#dc2626">🔴 Obvious Red Flags</strong>
    <ul style="margin:12px 0 0;padding-left:20px;font-size:.9rem;line-height:1.8">
      <li>Explicit sexual comments or propositions</li>
      <li>Racial slurs or ethnic jokes</li>
      <li>Unwanted physical contact</li>
      <li>Threats or intimidation</li>
      <li>Displaying pornographic material</li>
      <li>Mocking someone's disability</li>
    </ul>
  </div>
  <div style="background:#fef3c7;padding:20px;border-radius:10px">
    <strong style="color:#d97706">🟡 Subtle Warning Signs</strong>
    <ul style="margin:12px 0 0;padding-left:20px;font-size:.9rem;line-height:1.8">
      <li>Repeatedly commenting on appearance</li>
      <li>"Joking" that makes someone uncomfortable</li>
      <li>Standing too close or invading personal space</li>
      <li>Consistently interrupting certain people</li>
      <li>Assigning demeaning tasks to specific groups</li>
      <li>Backhanded compliments ("You're smart for a...")</li>
    </ul>
  </div>
</div>

<div style="background:linear-gradient(135deg,#3b82f608,#3b82f603);border-left:4px solid #3b82f6;padding:20px 24px;margin:24px 0;border-radius:0 10px 10px 0">
  <strong style="display:flex;align-items:center;gap:8px;margin-bottom:8px">💡 The "Reasonable Person" Standard</strong>
  <div style="font-size:.92rem;line-height:1.7">Courts use the "reasonable person" standard: Would a reasonable person in the same situation find the conduct offensive or hostile? This is an objective standard — the harasser's intent ("I was just joking") doesn't matter if the impact creates a hostile environment.</div>
</div>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>👀 The Bystander's Role</h3>

<p>If you witness harassment, you have the power — and responsibility — to help. Bystander intervention can stop harassment and support targets.</p>

<h4>The 5 D's of Bystander Intervention</h4>

<div style="display:grid;grid-template-columns:1fr;gap:12px;margin:24px 0">
  <div style="background:#f8fafc;border-left:4px solid #16a34a;padding:16px 20px;border-radius:0 8px 8px 0">
    <strong style="color:#16a34a">1. DIRECT</strong>
    <p style="margin:6px 0 0;font-size:.9rem">Intervene directly by addressing the harasser: "That's not appropriate" or "Please stop."</p>
    <p style="margin:4px 0 0;font-size:.8rem;color:#64748b">⚠️ Only use when safe — don't put yourself at risk</p>
  </div>
  <div style="background:#f8fafc;border-left:4px solid #2563eb;padding:16px 20px;border-radius:0 8px 8px 0">
    <strong style="color:#2563eb">2. DISTRACT</strong>
    <p style="margin:6px 0 0;font-size:.9rem">Create a distraction to interrupt the situation: "Hey, can you help me with something?" or spill something nearby.</p>
    <p style="margin:4px 0 0;font-size:.8rem;color:#64748b">✅ Subtle and effective in many situations</p>
  </div>
  <div style="background:#f8fafc;border-left:4px solid #7c3aed;padding:16px 20px;border-radius:0 8px 8px 0">
    <strong style="color:#7c3aed">3. DELEGATE</strong>
    <p style="margin:6px 0 0;font-size:.9rem">Get help from someone else — a manager, HR, security, or another colleague.</p>
    <p style="margin:4px 0 0;font-size:.8rem;color:#64748b">✅ Good when you don't feel comfortable intervening directly</p>
  </div>
  <div style="background:#f8fafc;border-left:4px solid #ea580c;padding:16px 20px;border-radius:0 8px 8px 0">
    <strong style="color:#ea580c">4. DELAY</strong>
    <p style="margin:6px 0 0;font-size:.9rem">Check in with the target afterward: "Are you okay? I saw what happened. Can I help you report it?"</p>
    <p style="margin:4px 0 0;font-size:.8rem;color:#64748b">✅ Shows support even when immediate intervention isn't possible</p>
  </div>
  <div style="background:#f8fafc;border-left:4px solid #dc2626;padding:16px 20px;border-radius:0 8px 8px 0">
    <strong style="color:#dc2626">5. DOCUMENT</strong>
    <p style="margin:6px 0 0;font-size:.9rem">Write down what you witnessed: date, time, location, people involved, exact words used.</p>
    <p style="margin:4px 0 0;font-size:.8rem;color:#64748b">✅ Your notes can support a formal complaint</p>
  </div>
</div>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>📢 How to Report Harassment</h3>

<p>You have multiple options for reporting harassment. All reports are taken seriously, investigated promptly, and kept as confidential as possible.</p>

<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:16px;margin:20px 0">
  <div style="background:#fff;border:2px solid #e2e8f0;padding:20px;border-radius:10px">
    <div style="font-size:28px;margin-bottom:8px">👤</div>
    <strong>Direct Supervisor</strong>
    <p style="font-size:.85rem;color:#64748b;margin:8px 0">Your first option (unless they're involved)</p>
  </div>
  <div style="background:#fff;border:2px solid #e2e8f0;padding:20px;border-radius:10px">
    <div style="font-size:28px;margin-bottom:8px">🏢</div>
    <strong>HR Department</strong>
    <p style="font-size:.85rem;color:#64748b;margin:8px 0">hr@company.com or in-person</p>
  </div>
  <div style="background:#fff;border:2px solid #e2e8f0;padding:20px;border-radius:10px">
    <div style="font-size:28px;margin-bottom:8px">📞</div>
    <strong>Ethics Hotline</strong>
    <p style="font-size:.85rem;color:#64748b;margin:8px 0">24/7 anonymous: 1-800-ETHICS</p>
  </div>
  <div style="background:#fff;border:2px solid #e2e8f0;padding:20px;border-radius:10px">
    <div style="font-size:28px;margin-bottom:8px">🌐</div>
    <strong>Online Portal</strong>
    <p style="font-size:.85rem;color:#64748b;margin:8px 0">ethics.company.com</p>
  </div>
</div>

<div style="background:linear-gradient(135deg,#22c55e08,#22c55e03);border:1px solid #22c55e40;padding:20px 24px;margin:24px 0;border-radius:12px">
  <strong style="display:flex;align-items:center;gap:8px;margin-bottom:10px">🛡️ Zero Tolerance for Retaliation</strong>
  <p style="margin:0;font-size:.92rem;line-height:1.7">Retaliation against anyone who reports harassment in good faith is <strong>strictly prohibited</strong> and is a terminable offense. This includes negative changes to job assignments, performance reviews, schedules, or any other adverse action. If you experience retaliation, report it immediately.</p>
</div>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>🎭 Scenario-Based Exercise</h3>

<div style="background:#f1f5f9;border:1px solid #e2e8f0;padding:24px;margin:24px 0;border-radius:12px">
  <strong style="display:flex;align-items:center;gap:8px;margin-bottom:12px;font-size:1.1rem">🎯 Scenario: The "Harmless" Jokes</strong>
  <p style="margin:12px 0;font-style:italic;background:#fff;padding:16px;border-radius:8px;border-left:4px solid #3b82f6">"Your team lead frequently makes jokes about a colleague's accent, saying things like 'Can anyone translate what Maria just said?' The jokes always get a laugh from some team members, but Maria looks uncomfortable. The team lead says it's 'all in good fun.'"</p>
  <p style="margin:12px 0 8px;font-weight:600">Is this harassment? What should you do?</p>
  <ul style="list-style:none;margin:0;padding:0">
    <li style="margin:6px 0;padding:10px 14px;background:#fff;border-radius:6px">⬜ A. It's just jokes — let it go</li>
    <li style="margin:6px 0;padding:10px 14px;background:#fff;border-radius:6px">⬜ B. Wait and see if Maria reports it herself</li>
    <li style="margin:6px 0;padding:10px 14px;background:#fff;border-radius:6px">✅ C. Speak privately to the team lead, check on Maria, and report if it continues</li>
    <li style="margin:6px 0;padding:10px 14px;background:#fff;border-radius:6px">⬜ D. Publicly confront the team lead in the next meeting</li>
  </ul>
  <details style="margin-top:16px">
    <summary style="cursor:pointer;color:#1a3a5c;font-weight:600;padding:8px;background:#e2e8f0;border-radius:6px">Show Answer & Explanation</summary>
    <div style="margin:12px 0;padding:16px;background:#fff;border-radius:8px;border-left:4px solid #22c55e">
      <p><strong>Correct Answer: C</strong></p>
      <p>Yes, this IS harassment. Repeated jokes targeting someone's national origin create a hostile environment, regardless of intent. The fact that Maria looks uncomfortable shows impact. Use the 5 D's: You might directly speak to the team lead privately ("Hey, I've noticed those jokes make Maria uncomfortable"), check on Maria afterward (Delay), and report to HR if it continues (Delegate).</p>
    </div>
  </details>
</div>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>💡 Key Takeaways</h3>

<div style="background:linear-gradient(135deg,#dc2626,#b91c1c);color:white;padding:28px;border-radius:12px;margin:24px 0">
  <ul style="margin:0;padding-left:20px;line-height:2">
    <li>Harassment is about <strong>impact, not intent</strong> — "I was just joking" is not a defense</li>
    <li>Everyone deserves a <strong>respectful workplace</strong> — speak up when you see problems</li>
    <li>Use the <strong>5 D's</strong> of bystander intervention: Direct, Distract, Delegate, Delay, Document</li>
    <li>Report through <strong>multiple channels</strong> — the Ethics Hotline is anonymous</li>
    <li><strong>Retaliation is prohibited</strong> — you are protected when you report in good faith</li>
    <li><strong>Support each other</strong> — a simple "Are you okay?" can make a huge difference</li>
  </ul>
</div>
"""

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute(
        "SELECT id FROM modules WHERE course_id = ? AND order_index = ?",
        ("course-compliance-101", 3),
    )
    row = cur.fetchone()
    if row:
        conn.execute("UPDATE modules SET content = ? WHERE id = ?", (CONTENT.strip(), row[0]))
        conn.commit()
        print(f"✅ Module 3 updated: {len(CONTENT)} chars")
    else:
        print("⚠️ Module not found")
    conn.close()

if __name__ == "__main__":
    main()
