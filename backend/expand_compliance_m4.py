"""
Expand Module 4: Ethics & Code of Conduct (~25K chars target)
"""
import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), "courses.db")

CONTENT = """
<h2>Ethics & Code of Conduct</h2>

<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:20px 0;background:linear-gradient(135deg,#1a3a5c08,#1a3a5c03);border-radius:12px;padding:16px">
  <div style="text-align:center;padding:16px"><div style="font-size:32px">🎯</div><div style="font-size:1.5rem;font-weight:700;color:#1a3a5c">Integrity</div><div style="font-size:.8rem;color:#64748b">Foundation of Trust</div></div>
  <div style="text-align:center;padding:16px"><div style="font-size:32px">⚖️</div><div style="font-size:1.5rem;font-weight:700;color:#1a3a5c">Fairness</div><div style="font-size:.8rem;color:#64748b">Equal Treatment</div></div>
  <div style="text-align:center;padding:16px"><div style="font-size:32px">🔍</div><div style="font-size:1.5rem;font-weight:700;color:#1a3a5c">Transparency</div><div style="font-size:.8rem;color:#64748b">Open Communication</div></div>
  <div style="text-align:center;padding:16px"><div style="font-size:32px">🛡️</div><div style="font-size:1.5rem;font-weight:700;color:#1a3a5c">Accountability</div><div style="font-size:.8rem;color:#64748b">Own Your Actions</div></div>
</div>

<img src="https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=800&h=400&fit=crop" alt="Professional ethics and business integrity" style="width:100%;border-radius:12px;margin:20px 0;box-shadow:0 4px 12px rgba(0,0,0,0.1)">

<h3>🎯 Learning Objectives</h3>
<p>By the end of this module, you will be able to:</p>
<ul>
  <li>Articulate the company's ethical standards and their importance</li>
  <li>Identify conflicts of interest and understand disclosure requirements</li>
  <li>Apply the ethics decision-making framework to complex situations</li>
  <li>Navigate the whistleblower process with confidence</li>
  <li>Understand the consequences of ethical violations</li>
  <li>Build and maintain a culture of integrity in your team</li>
</ul>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>📚 Why Ethics Matter</h3>

<p>Ethics goes beyond following the law — it's about <strong>doing what's right even when no one is watching</strong>. Our reputation, built over decades, can be destroyed in a single headline. Every decision you make either strengthens or weakens our ethical foundation.</p>

<p>The business case for ethics is clear:</p>
<ul>
  <li><strong>Trust:</strong> Customers, partners, and employees trust ethical organizations</li>
  <li><strong>Reputation:</strong> Ethical companies attract better talent and business opportunities</li>
  <li><strong>Legal protection:</strong> Strong ethics programs reduce regulatory and legal risk</li>
  <li><strong>Long-term value:</strong> Ethical companies outperform in the long run</li>
  <li><strong>Employee engagement:</strong> People want to work for companies they're proud of</li>
</ul>

<div style="background:linear-gradient(135deg,#ef444408,#ef444403);border-left:4px solid #ef4444;padding:20px 24px;margin:24px 0;border-radius:0 10px 10px 0">
  <strong style="display:flex;align-items:center;gap:8px;margin-bottom:8px">⚠️ Real-World Consequences</strong>
  <div style="font-size:.92rem;line-height:1.7"><strong>Enron (2001):</strong> Accounting fraud led to $74 billion in shareholder losses and 20,000+ job losses. <strong>Volkswagen (2015):</strong> Emissions cheating resulted in $33 billion in fines and settlements. <strong>Wells Fargo (2016):</strong> Fake accounts scandal led to $3 billion in penalties and lasting brand damage. These weren't just corporate failures — individuals went to prison.</div>
</div>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>🏛️ The Four Pillars of Ethical Conduct</h3>

<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:20px;margin:24px 0">
  <div style="background:linear-gradient(135deg,#1a3a5c08,#1a3a5c02);border:1px solid #e2e8f0;padding:24px;border-radius:12px">
    <div style="font-size:36px;margin-bottom:12px">🎯</div>
    <h4 style="margin:0 0 12px 0;color:#1a3a5c">1. Honesty</h4>
    <p style="margin:0;font-size:.9rem;line-height:1.6;color:#475569">Be truthful in all communications and transactions. Never misrepresent facts, data, or capabilities to colleagues, clients, or stakeholders.</p>
    <ul style="margin:12px 0 0 0;padding-left:20px;font-size:.85rem;color:#64748b">
      <li>Report accurate data and results</li>
      <li>Acknowledge mistakes promptly</li>
      <li>Never exaggerate or omit material facts</li>
      <li>Be honest about what you know and don't know</li>
    </ul>
  </div>
  <div style="background:linear-gradient(135deg,#2c7a7b08,#2c7a7b02);border:1px solid #e2e8f0;padding:24px;border-radius:12px">
    <div style="font-size:36px;margin-bottom:12px">📋</div>
    <h4 style="margin:0 0 12px 0;color:#2c7a7b">2. Accountability</h4>
    <p style="margin:0;font-size:.9rem;line-height:1.6;color:#475569">Own your decisions and their consequences. Don't shift blame, make excuses, or hide problems. Accept responsibility and focus on solutions.</p>
    <ul style="margin:12px 0 0 0;padding-left:20px;font-size:.85rem;color:#64748b">
      <li>Take ownership of your work</li>
      <li>Follow through on commitments</li>
      <li>Admit errors and learn from them</li>
      <li>Hold yourself to the same standards as others</li>
    </ul>
  </div>
  <div style="background:linear-gradient(135deg,#7c3aed08,#7c3aed02);border:1px solid #e2e8f0;padding:24px;border-radius:12px">
    <div style="font-size:36px;margin-bottom:12px">⚖️</div>
    <h4 style="margin:0 0 12px 0;color:#7c3aed">3. Fairness</h4>
    <p style="margin:0;font-size:.9rem;line-height:1.6;color:#475569">Treat everyone equitably, without favoritism or bias. Apply the same standards to all, regardless of relationship, seniority, or personal feelings.</p>
    <ul style="margin:12px 0 0 0;padding-left:20px;font-size:.85rem;color:#64748b">
      <li>Make decisions based on merit</li>
      <li>Avoid conflicts of interest</li>
      <li>Don't play favorites</li>
      <li>Give credit where it's due</li>
    </ul>
  </div>
  <div style="background:linear-gradient(135deg,#16a34a08,#16a34a02);border:1px solid #e2e8f0;padding:24px;border-radius:12px">
    <div style="font-size:36px;margin-bottom:12px">🤝</div>
    <h4 style="margin:0 0 12px 0;color:#16a34a">4. Respect</h4>
    <p style="margin:0;font-size:.9rem;line-height:1.6;color:#475569">Value diversity and treat colleagues with dignity. Listen to understand, not just to respond. Create an environment where everyone feels valued.</p>
    <ul style="margin:12px 0 0 0;padding-left:20px;font-size:.85rem;color:#64748b">
      <li>Listen actively to others</li>
      <li>Respect different perspectives</li>
      <li>Communicate constructively</li>
      <li>Support colleagues' professional growth</li>
    </ul>
  </div>
</div>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>⚔️ Conflicts of Interest</h3>

<img src="https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=800&h=350&fit=crop" alt="Business decisions and ethics" style="width:100%;border-radius:12px;margin:20px 0;box-shadow:0 4px 12px rgba(0,0,0,0.1)">

<p>A conflict of interest occurs when your personal interests could influence — or appear to influence — your professional judgment. The key word is "could" — even the appearance of a conflict must be disclosed.</p>

<h4>Common Types of Conflicts</h4>

<table style="width:100%;border-collapse:collapse;margin:16px 0">
  <tr style="background:#f8fafc"><th style="padding:12px;text-align:left;border:1px solid #e2e8f0">Type</th><th style="padding:12px;text-align:left;border:1px solid #e2e8f0">Examples</th><th style="padding:12px;text-align:left;border:1px solid #e2e8f0">Required Action</th></tr>
  <tr><td style="padding:12px;border:1px solid #e2e8f0"><strong>💰 Financial</strong></td><td style="padding:12px;border:1px solid #e2e8f0">Owning stock in a vendor/competitor, receiving kickbacks</td><td style="padding:12px;border:1px solid #e2e8f0">Disclose and recuse from decisions</td></tr>
  <tr><td style="padding:12px;border:1px solid #e2e8f0"><strong>👨‍👩‍👧 Relationship</strong></td><td style="padding:12px;border:1px solid #e2e8f0">Hiring/supervising family members, romantic relationships with reports</td><td style="padding:12px;border:1px solid #e2e8f0">Disclose, restructure reporting lines</td></tr>
  <tr><td style="padding:12px;border:1px solid #e2e8f0"><strong>💼 Outside Employment</strong></td><td style="padding:12px;border:1px solid #e2e8f0">Working for competitors, consulting on company time</td><td style="padding:12px;border:1px solid #e2e8f0">Pre-approval required</td></tr>
  <tr><td style="padding:12px;border:1px solid #e2e8f0"><strong>🎁 Gifts & Entertainment</strong></td><td style="padding:12px;border:1px solid #e2e8f0">Accepting expensive gifts, luxury trips from vendors</td><td style="padding:12px;border:1px solid #e2e8f0">Follow Gift Policy limits</td></tr>
  <tr><td style="padding:12px;border:1px solid #e2e8f0"><strong>🏢 Board Positions</strong></td><td style="padding:12px;border:1px solid #e2e8f0">Serving on boards of related organizations</td><td style="padding:12px;border:1px solid #e2e8f0">Pre-approval from Ethics Committee</td></tr>
</table>

<div style="background:linear-gradient(135deg,#3b82f608,#3b82f603);border-left:4px solid #3b82f6;padding:20px 24px;margin:24px 0;border-radius:0 10px 10px 0">
  <strong style="display:flex;align-items:center;gap:8px;margin-bottom:8px">💡 Key Principle: Disclosure ≠ Wrongdoing</strong>
  <div style="font-size:.92rem;line-height:1.7">Disclosing a potential conflict doesn't mean you've done something wrong — it means you're being transparent. Many conflicts can be managed once disclosed. The problem isn't having a conflict; it's hiding one.</div>
</div>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>🧭 The Ethics Decision Framework</h3>

<p>When facing an ethical dilemma, use this framework to guide your decision:</p>

<div style="display:grid;grid-template-columns:1fr;gap:12px;margin:24px 0">
  <div style="background:#f8fafc;border-left:4px solid #1a3a5c;padding:16px 20px;border-radius:0 8px 8px 0">
    <strong style="color:#1a3a5c">1️⃣ Is it legal?</strong>
    <p style="margin:6px 0 0;font-size:.9rem">Does this action comply with all applicable laws and regulations?</p>
  </div>
  <div style="background:#f8fafc;border-left:4px solid #2c7a7b;padding:16px 20px;border-radius:0 8px 8px 0">
    <strong style="color:#2c7a7b">2️⃣ Does it align with our values?</strong>
    <p style="margin:6px 0 0;font-size:.9rem">Is it consistent with our Code of Conduct and company values?</p>
  </div>
  <div style="background:#f8fafc;border-left:4px solid #7c3aed;padding:16px 20px;border-radius:0 8px 8px 0">
    <strong style="color:#7c3aed">3️⃣ How would it look in the news?</strong>
    <p style="margin:6px 0 0;font-size:.9rem">Would you be comfortable if this decision were on the front page tomorrow?</p>
  </div>
  <div style="background:#f8fafc;border-left:4px solid #ea580c;padding:16px 20px;border-radius:0 8px 8px 0">
    <strong style="color:#ea580c">4️⃣ Would you tell your family?</strong>
    <p style="margin:6px 0 0;font-size:.9rem">Would you be proud to tell your family about this decision?</p>
  </div>
  <div style="background:#f8fafc;border-left:4px solid #16a34a;padding:16px 20px;border-radius:0 8px 8px 0">
    <strong style="color:#16a34a">5️⃣ Does it pass the "smell test"?</strong>
    <p style="margin:6px 0 0;font-size:.9rem">Does something feel wrong? Trust your instincts.</p>
  </div>
</div>

<p style="text-align:center;font-weight:600;font-size:1.1rem;color:#dc2626;margin:20px 0">If you answer "no" to ANY of these questions — STOP and seek guidance.</p>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>🛡️ Whistleblower Protections</h3>

<p>Employees who report unethical behavior, fraud, or violations in good faith are protected by:</p>

<ul style="line-height:2">
  <li><strong>Federal Laws:</strong> Sarbanes-Oxley, Dodd-Frank, False Claims Act provide legal protection</li>
  <li><strong>State Laws:</strong> Additional whistleblower protections vary by state</li>
  <li><strong>Company Policy:</strong> Our non-retaliation policy strictly prohibits adverse action against reporters</li>
  <li><strong>Anonymous Channels:</strong> Ethics Hotline and online portal allow anonymous reporting</li>
</ul>

<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:16px;margin:20px 0">
  <div style="background:#fff;border:2px solid #e2e8f0;padding:20px;border-radius:10px;text-align:center">
    <div style="font-size:28px;margin-bottom:8px">📞</div>
    <strong>Ethics Hotline</strong>
    <p style="font-size:.85rem;color:#64748b;margin:8px 0">1-800-ETHICS (24/7, anonymous)</p>
  </div>
  <div style="background:#fff;border:2px solid #e2e8f0;padding:20px;border-radius:10px;text-align:center">
    <div style="font-size:28px;margin-bottom:8px">🌐</div>
    <strong>Online Portal</strong>
    <p style="font-size:.85rem;color:#64748b;margin:8px 0">ethics.company.com (anonymous option)</p>
  </div>
</div>

<div style="background:linear-gradient(135deg,#22c55e08,#22c55e03);border:1px solid #22c55e40;padding:20px 24px;margin:24px 0;border-radius:12px">
  <strong style="display:flex;align-items:center;gap:8px;margin-bottom:10px">✅ What Happens After You Report</strong>
  <ol style="margin:0;padding-left:20px;font-size:.92rem;line-height:1.8">
    <li>Your report is received and logged by the Ethics & Compliance team</li>
    <li>An investigator is assigned within 48 hours</li>
    <li>You may be contacted for additional information (if not anonymous)</li>
    <li>The investigation is conducted confidentially</li>
    <li>Appropriate action is taken based on findings</li>
    <li>You're informed of the outcome (to the extent permitted)</li>
  </ol>
</div>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>🎭 Scenario-Based Exercises</h3>

<div style="background:#f1f5f9;border:1px solid #e2e8f0;padding:24px;margin:24px 0;border-radius:12px">
  <strong style="display:flex;align-items:center;gap:8px;margin-bottom:12px;font-size:1.1rem">🎯 Scenario 1: The Expense Report</strong>
  <p style="margin:12px 0;font-style:italic;background:#fff;padding:16px;border-radius:8px;border-left:4px solid #3b82f6">"You notice a colleague submitting expense reports for client dinners that you know didn't happen. When you casually mention it, they say 'Everyone does it — it's a perk of the job. The company has plenty of money.'"</p>
  <p style="margin:12px 0 8px;font-weight:600">What should you do?</p>
  <ul style="list-style:none;margin:0;padding:0">
    <li style="margin:6px 0;padding:10px 14px;background:#fff;border-radius:6px">⬜ A. Mind your own business — it's not your concern</li>
    <li style="margin:6px 0;padding:10px 14px;background:#fff;border-radius:6px">⬜ B. Confront them and demand they stop</li>
    <li style="margin:6px 0;padding:10px 14px;background:#fff;border-radius:6px">✅ C. Document what you observed and report through the Ethics Hotline</li>
    <li style="margin:6px 0;padding:10px 14px;background:#fff;border-radius:6px">⬜ D. Start submitting similar expenses since "everyone does it"</li>
  </ul>
  <details style="margin-top:16px">
    <summary style="cursor:pointer;color:#1a3a5c;font-weight:600;padding:8px;background:#e2e8f0;border-radius:6px">Show Answer & Explanation</summary>
    <div style="margin:12px 0;padding:16px;background:#fff;border-radius:8px;border-left:4px solid #22c55e">
      <p><strong>Correct Answer: C</strong></p>
      <p>This is expense fraud — a serious ethical and potentially criminal violation. "Everyone does it" is a rationalization, not a justification. Document what you know (dates, amounts if possible, the conversation) and report it. You don't need to confront them directly — that's the investigator's job.</p>
    </div>
  </details>
</div>

<div style="background:#f1f5f9;border:1px solid #e2e8f0;padding:24px;margin:24px 0;border-radius:12px">
  <strong style="display:flex;align-items:center;gap:8px;margin-bottom:12px;font-size:1.1rem">🎯 Scenario 2: The Family Business</strong>
  <p style="margin:12px 0;font-style:italic;background:#fff;padding:16px;border-radius:8px;border-left:4px solid #3b82f6">"Your brother-in-law owns a catering company. Your department is looking for a new catering vendor for company events. His prices are competitive and his quality is good. Can you recommend him?"</p>
  <p style="margin:12px 0 8px;font-weight:600">What should you do?</p>
  <ul style="list-style:none;margin:0;padding:0">
    <li style="margin:6px 0;padding:10px 14px;background:#fff;border-radius:6px">⬜ A. Recommend him — his prices are fair and you know the quality</li>
    <li style="margin:6px 0;padding:10px 14px;background:#fff;border-radius:6px">✅ B. Disclose the relationship and recuse yourself from the decision</li>
    <li style="margin:6px 0;padding:10px 14px;background:#fff;border-radius:6px">⬜ C. Don't mention the relationship since prices are competitive anyway</li>
    <li style="margin:6px 0;padding:10px 14px;background:#fff;border-radius:6px">⬜ D. Tell your brother-in-law to lower his prices so it looks even better</li>
  </ul>
  <details style="margin-top:16px">
    <summary style="cursor:pointer;color:#1a3a5c;font-weight:600;padding:8px;background:#e2e8f0;border-radius:6px">Show Answer & Explanation</summary>
    <div style="margin:12px 0;padding:16px;background:#fff;border-radius:8px;border-left:4px solid #22c55e">
      <p><strong>Correct Answer: B</strong></p>
      <p>This is a clear conflict of interest. Even if his prices are fair and quality is good, your involvement in recommending him creates the appearance of favoritism. Disclose the relationship to your manager and the Ethics Committee, and recuse yourself from the vendor selection process. The vendor can still be considered — just without your involvement.</p>
    </div>
  </details>
</div>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>💡 Key Takeaways</h3>

<div style="background:linear-gradient(135deg,#1a3a5c,#2c5282);color:white;padding:28px;border-radius:12px;margin:24px 0">
  <ul style="margin:0;padding-left:20px;line-height:2">
    <li>Ethics is about <strong>doing right even when no one is watching</strong></li>
    <li>The Four Pillars: <strong>Honesty, Accountability, Fairness, Respect</strong></li>
    <li><strong>Disclose conflicts of interest</strong> — transparency protects you</li>
    <li>Use the <strong>Ethics Decision Framework</strong> when facing dilemmas</li>
    <li><strong>Whistleblowers are protected</strong> — report concerns without fear</li>
    <li>Your reputation is your most valuable asset — <strong>protect it</strong></li>
  </ul>
</div>
"""

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute(
        "SELECT id FROM modules WHERE course_id = ? AND order_index = ?",
        ("course-compliance-101", 4),
    )
    row = cur.fetchone()
    if row:
        conn.execute("UPDATE modules SET content = ? WHERE id = ?", (CONTENT.strip(), row[0]))
        conn.commit()
        print(f"✅ Module 4 updated: {len(CONTENT)} chars")
    else:
        print("⚠️ Module not found")
    conn.close()

if __name__ == "__main__":
    main()
