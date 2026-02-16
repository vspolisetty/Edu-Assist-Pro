"""
Expand module content with 3-5x more material — case studies, scenarios,
interactive exercises, knowledge checks, infographics, and deep-dive sections.
Run: python3 backend/expand_content.py
"""

import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), "courses.db")

# ── Helper: callout box ──
def callout(icon, title, body, color="#1a3a5c"):
    return f"""
<div style="background:linear-gradient(135deg,{color}08,{color}03);border-left:4px solid {color};padding:18px 22px;margin:24px 0;border-radius:0 8px 8px 0">
  <strong style="display:flex;align-items:center;gap:6px;margin-bottom:6px">{icon} {title}</strong>
  <div style="font-size:.9rem;line-height:1.6">{body}</div>
</div>"""

def scenario_box(scenario, options, answer_idx, explanation):
    opts = ""
    for i, o in enumerate(options):
        marker = "✅" if i == answer_idx else "⬜"
        opts += f"<li style='margin:4px 0'>{marker} {o}</li>"
    return f"""
<div style="background:var(--surface-hover,#f1f5f9);border:1px solid var(--border,#e2e8f0);padding:20px 24px;margin:24px 0;border-radius:10px">
  <strong style="display:flex;align-items:center;gap:6px;margin-bottom:8px">🎯 Scenario-Based Exercise</strong>
  <p style="margin:8px 0;font-style:italic">{scenario}</p>
  <p style="margin:10px 0 4px;font-weight:600">What would you do?</p>
  <ul style="list-style:none;margin:0;padding:0">{opts}</ul>
  <details style="margin-top:12px">
    <summary style="cursor:pointer;color:var(--primary,#1a3a5c);font-weight:600;font-size:.88rem">Show Answer & Explanation</summary>
    <p style="margin:8px 0;padding:10px;background:var(--bg,#f7f8fc);border-radius:6px;font-size:.88rem">{explanation}</p>
  </details>
</div>"""

def knowledge_check(question, options, answer_idx, explanation):
    opts = ""
    for i, o in enumerate(options):
        marker = "✅" if i == answer_idx else "○"
        opts += f"<li style='margin:4px 0'>{marker} {o}</li>"
    return f"""
<div style="background:linear-gradient(135deg,#22c55e08,#22c55e02);border:1px solid #22c55e40;padding:18px 22px;margin:20px 0;border-radius:10px">
  <strong style="display:flex;align-items:center;gap:6px;margin-bottom:8px">✅ Knowledge Check</strong>
  <p style="margin:6px 0;font-weight:500">{question}</p>
  <ul style="list-style:none;margin:8px 0;padding:0">{opts}</ul>
  <details style="margin-top:8px">
    <summary style="cursor:pointer;color:#22c55e;font-weight:600;font-size:.88rem">Reveal Answer</summary>
    <p style="margin:8px 0;padding:8px;background:#22c55e08;border-radius:6px;font-size:.88rem">{explanation}</p>
  </details>
</div>"""

def stat_box(stats):
    """stats: list of (icon, value, label)"""
    cards = ""
    for icon, val, label in stats:
        cards += f'<div style="text-align:center;padding:16px"><div style="font-size:28px;margin-bottom:4px">{icon}</div><div style="font-size:1.3rem;font-weight:700;color:var(--primary,#1a3a5c)">{val}</div><div style="font-size:.78rem;color:var(--text-secondary,#64748b)">{label}</div></div>'
    return f'<div style="display:grid;grid-template-columns:repeat({len(stats)},1fr);gap:8px;margin:20px 0;background:var(--surface-hover,#f1f5f9);border-radius:10px;overflow:hidden">{cards}</div>'


# ══════════════════════════════════════════════════════════════════════════
# EXPANDED CONTENT
# ══════════════════════════════════════════════════════════════════════════

CONTENT = {}

# ── Compliance 101 — Module 0: Company Policies ──
CONTENT[("course-compliance-101", 0)] = f"""
<h2>Company Policies Overview</h2>

{stat_box([("📋","50+","Active Policies"),("👥","100%","Employee Coverage"),("📅","Annual","Review Cycle"),("⚖️","Zero","Tolerance for Violations")])}

<h3>🎯 Learning Objectives</h3>
<ul>
  <li>Understand the purpose, scope, and structure of company policies</li>
  <li>Identify your responsibilities as an employee under each major policy</li>
  <li>Know where to find, reference, and report concerns about policies</li>
  <li>Apply policy knowledge to real-world workplace scenarios</li>
</ul>

<h3>Why Policies Matter</h3>
<p>Company policies are the backbone of a well-run organization. They exist to:</p>
<ul>
  <li><strong>Protect employees</strong> from unfair treatment, harassment, and unsafe conditions</li>
  <li><strong>Ensure legal compliance</strong> with federal, state, and local regulations</li>
  <li><strong>Create consistency</strong> so everyone is treated fairly regardless of role or location</li>
  <li><strong>Reduce liability</strong> for the organization and its employees</li>
  <li><strong>Set expectations</strong> so there are no surprises about what's acceptable</li>
</ul>

{callout("📌", "Did You Know?", "Companies with well-documented policies experience <strong>40% fewer employee disputes</strong> and <strong>60% faster resolution times</strong> when issues do arise.", "#2c7a7b")}

<h3>Code of Conduct: The Foundation</h3>
<p>Our Code of Conduct is the most important policy document. It sets the ethical and behavioral standards for every interaction — internal and external. Here are the pillars:</p>

<h4>1. Act with Integrity</h4>
<p>Integrity means being honest and transparent in all business dealings. This includes:</p>
<ul>
  <li>Accurately reporting work hours, expenses, and project status</li>
  <li>Never misrepresenting data, qualifications, or capabilities</li>
  <li>Honoring commitments to colleagues, clients, and partners</li>
  <li>Admitting mistakes promptly rather than trying to cover them up</li>
</ul>

<h4>2. Treat Others with Respect</h4>
<p>A respectful workplace is a productive workplace. This means:</p>
<ul>
  <li>Valuing diverse perspectives, backgrounds, and communication styles</li>
  <li>Listening actively before responding</li>
  <li>Addressing disagreements professionally, focusing on issues rather than people</li>
  <li>Never engaging in gossip, bullying, or exclusionary behavior</li>
</ul>

<h4>3. Protect Company Assets</h4>
<p>Company assets include physical property, intellectual property, data, and reputation:</p>
<ul>
  <li>Use company technology and equipment for authorized purposes only</li>
  <li>Safeguard confidential information — lock screens, shred documents, use encrypted communication</li>
  <li>Report lost or stolen equipment immediately to IT Security</li>
  <li>Don't share proprietary information with competitors or unauthorized third parties</li>
</ul>

<h4>4. Follow the Law</h4>
<p>Compliance with all applicable laws is non-negotiable. Key areas include:</p>
<ul>
  <li>Anti-bribery and anti-corruption laws (FCPA, UK Bribery Act)</li>
  <li>Securities regulations (insider trading prohibitions)</li>
  <li>Employment laws (wage and hour, discrimination, safety)</li>
  <li>Environmental regulations</li>
</ul>

{scenario_box(
    "Your manager asks you to 'adjust' some numbers in a client report to make the quarterly results look better. She says 'everyone does it' and it's not a big deal.",
    ["Do what your manager asks — she has more experience and probably knows best",
     "Refuse and report the request through the Ethics Hotline",
     "Adjust the numbers slightly — just enough to help but not enough to be noticed",
     "Ignore the request and hope she doesn't ask again"],
    1,
    "<strong>Correct: Refuse and report.</strong> Falsifying reports is a serious ethical and legal violation. Your manager's instruction does not override company policy or the law. Use the Ethics Hotline if you're uncomfortable reporting to your direct manager."
)}

<h3>Key Policies Every Employee Must Know</h3>

<table style="width:100%;border-collapse:collapse;margin:16px 0">
  <tr style="background:var(--surface-hover,#f0f0f0)"><th style="padding:10px 14px;text-align:left;border:1px solid var(--border,#ddd)">Policy</th><th style="padding:10px 14px;text-align:left;border:1px solid var(--border,#ddd)">What It Covers</th><th style="padding:10px 14px;text-align:left;border:1px solid var(--border,#ddd)">Key Points</th></tr>
  <tr><td style="padding:10px 14px;border:1px solid var(--border,#ddd)"><strong>Acceptable Use Policy</strong></td><td style="padding:10px 14px;border:1px solid var(--border,#ddd)">Technology, email, internet, social media</td><td style="padding:10px 14px;border:1px solid var(--border,#ddd)">No personal use of company devices for illegal activities; limited personal use is okay</td></tr>
  <tr><td style="padding:10px 14px;border:1px solid var(--border,#ddd)"><strong>Confidentiality Agreement</strong></td><td style="padding:10px 14px;border:1px solid var(--border,#ddd)">Trade secrets, client data, proprietary info</td><td style="padding:10px 14px;border:1px solid var(--border,#ddd)">Survives employment; breaches may result in legal action</td></tr>
  <tr><td style="padding:10px 14px;border:1px solid var(--border,#ddd)"><strong>Attendance & Punctuality</strong></td><td style="padding:10px 14px;border:1px solid var(--border,#ddd)">Work hours, time tracking, absences</td><td style="padding:10px 14px;border:1px solid var(--border,#ddd)">Notify supervisor before shift; 3 unexcused absences = disciplinary action</td></tr>
  <tr><td style="padding:10px 14px;border:1px solid var(--border,#ddd)"><strong>Conflict of Interest</strong></td><td style="padding:10px 14px;border:1px solid var(--border,#ddd)">Outside employment, investments, relationships</td><td style="padding:10px 14px;border:1px solid var(--border,#ddd)">Must disclose; doesn't mean you've done wrong — transparency matters</td></tr>
  <tr><td style="padding:10px 14px;border:1px solid var(--border,#ddd)"><strong>Travel & Expense</strong></td><td style="padding:10px 14px;border:1px solid var(--border,#ddd)">Business travel, reimbursements, per diem</td><td style="padding:10px 14px;border:1px solid var(--border,#ddd)">Pre-approval required; receipts over $25; economy class for flights under 6 hours</td></tr>
  <tr><td style="padding:10px 14px;border:1px solid var(--border,#ddd)"><strong>Social Media</strong></td><td style="padding:10px 14px;border:1px solid var(--border,#ddd)">Personal and professional social media</td><td style="padding:10px 14px;border:1px solid var(--border,#ddd)">Don't speak on behalf of company without authorization; disclose affiliation when relevant</td></tr>
</table>

<h3>📚 Deep Dive: The Gift & Entertainment Policy</h3>
<p>One of the most commonly misunderstood policies. Here are the rules:</p>
<ul>
  <li>You may <strong>accept</strong> gifts worth <strong>under $50</strong> from business partners (e.g., a branded pen, a book)</li>
  <li>Gifts worth <strong>$50-$200</strong> must be disclosed to your manager within 5 business days</li>
  <li>Gifts worth <strong>over $200</strong> must be declined or returned, and reported to the Ethics Committee</li>
  <li><strong>Cash or cash equivalents</strong> (gift cards) of any value must always be declined</li>
  <li><strong>Entertainment</strong> (meals, events) is acceptable if there's a legitimate business purpose and the other party is present</li>
  <li><strong>Government officials:</strong> Extra restrictions apply — consult Legal before offering or accepting anything</li>
</ul>

{callout("⚠️", "Common Mistake", "A vendor sends you a $100 gift basket during the holidays. Many employees assume it's fine because 'it's the holidays.' <strong>Wrong.</strong> You need to disclose it to your manager within 5 days because it exceeds $50.", "#ef4444")}

<h3>How to Report Concerns</h3>
<p>If you witness a policy violation or have concerns:</p>
<ol>
  <li><strong>Direct Supervisor:</strong> Your first option (unless they are involved in the issue)</li>
  <li><strong>HR Department:</strong> hr@company.com or schedule an in-person meeting</li>
  <li><strong>Ethics Hotline:</strong> Available 24/7, anonymous — call 1-800-ETHICS or visit ethics.company.com</li>
  <li><strong>Legal Department:</strong> For issues involving potential legal violations</li>
  <li><strong>Open Door Policy:</strong> You can escalate to any level of management</li>
</ol>

{callout("🛡️", "Retaliation Protection", "Retaliation against anyone who reports a concern in good faith is <strong>strictly prohibited</strong> and is itself a terminable offense. You are protected whether the report ultimately proves valid or not.", "#22c55e")}

{knowledge_check(
    "Which of the following is the correct action when you receive a $75 gift from a vendor?",
    ["Keep it quietly — it's under $100",
     "Disclose it to your manager within 5 business days",
     "Return it immediately and file an ethics report",
     "Share it with your team to avoid any personal benefit"],
    1,
    "Gifts between $50 and $200 must be disclosed to your manager within 5 business days. You don't need to return it, but transparency is required."
)}

<h3>Case Study: Policy in Action</h3>
<div style="background:var(--surface-hover,#f1f5f9);padding:20px 24px;border-radius:10px;margin:20px 0">
  <p><strong>The Situation:</strong> Sarah, a marketing manager, discovers that her team member Tom has been using his company laptop to run a freelance graphic design business during work hours. Tom argues that it doesn't affect his work performance.</p>
  <p><strong>The Policies Involved:</strong></p>
  <ul>
    <li><strong>Acceptable Use Policy:</strong> Company equipment is for company business</li>
    <li><strong>Conflict of Interest:</strong> Outside employment must be disclosed</li>
    <li><strong>Attendance & Punctuality:</strong> Full productivity expected during work hours</li>
  </ul>
  <p><strong>The Resolution:</strong> Sarah reported the situation to HR. Tom was counseled about the AUP violation and asked to disclose his freelance work under the Conflict of Interest policy. His freelance work was approved (it didn't compete with the company), but he was required to use personal equipment and personal time going forward.</p>
  <p><strong>The Lesson:</strong> The issue wasn't the freelance work itself — it was the lack of disclosure and misuse of company resources. Transparency would have prevented the entire situation.</p>
</div>

<h3>📝 Quick Reference: Where to Find Policies</h3>
<ul>
  <li><strong>Employee Handbook:</strong> Available on the HR Portal → Documents section</li>
  <li><strong>Policy Updates:</strong> Sent via email and posted on the intranet; acknowledgment required within 7 days</li>
  <li><strong>FAQ Section:</strong> Common questions answered at hr.company.com/policy-faq</li>
  <li><strong>HR Office Hours:</strong> Every Wednesday 2-4 PM for walk-in policy questions</li>
</ul>

<h3>💡 Key Takeaways</h3>
<ul>
  <li>Policies protect <strong>you</strong> — they're not just rules, they're your rights</li>
  <li>When in doubt, <strong>disclose</strong> — transparency is always the right choice</li>
  <li>Use the <strong>Ethics Hotline</strong> if you're uncomfortable reporting directly — it's anonymous and protected</li>
  <li>Review the <strong>Employee Handbook</strong> at least once a year, especially after updates</li>
  <li><strong>No policy is worth violating for short-term gain</strong> — the consequences always outweigh the benefits</li>
</ul>
"""

# ── Compliance 101 — Module 1: Data Privacy & GDPR ──
CONTENT[("course-compliance-101", 1)] = f"""
<h2>Data Privacy & GDPR</h2>

{stat_box([("🔒","€20M","Max GDPR Fine"),("📊","4%","Revenue Penalty"),("🌍","27+","EU Countries"),("⏱️","72h","Breach Notification")])}

<h3>🎯 Learning Objectives</h3>
<ul>
  <li>Understand the principles of data privacy and why it matters to every employee</li>
  <li>Learn the key provisions of GDPR and how they apply to your daily work</li>
  <li>Handle personal data responsibly across all channels and systems</li>
  <li>Recognize data breaches and know the reporting timeline</li>
</ul>

<h3>What Is Personal Data?</h3>
<p>Under GDPR, personal data is <strong>any information that can identify a living person</strong>, either directly or indirectly:</p>

<table style="width:100%;border-collapse:collapse;margin:16px 0">
  <tr style="background:var(--surface-hover,#f0f0f0)"><th style="padding:10px 14px;text-align:left;border:1px solid var(--border,#ddd)">Category</th><th style="padding:10px 14px;text-align:left;border:1px solid var(--border,#ddd)">Examples</th><th style="padding:10px 14px;text-align:left;border:1px solid var(--border,#ddd)">Sensitivity Level</th></tr>
  <tr><td style="padding:10px;border:1px solid var(--border,#ddd)">Basic Identity</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Name, email, phone number</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Standard</td></tr>
  <tr><td style="padding:10px;border:1px solid var(--border,#ddd)">Online Identifiers</td><td style="padding:10px;border:1px solid var(--border,#ddd)">IP address, cookies, device IDs</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Standard</td></tr>
  <tr><td style="padding:10px;border:1px solid var(--border,#ddd)">Financial</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Bank details, salary, credit score</td><td style="padding:10px;border:1px solid var(--border,#ddd)">High</td></tr>
  <tr><td style="padding:10px;border:1px solid var(--border,#ddd)">Health</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Medical records, insurance claims</td><td style="padding:10px;border:1px solid var(--border,#ddd)">🔴 Special Category</td></tr>
  <tr><td style="padding:10px;border:1px solid var(--border,#ddd)">Biometric</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Fingerprints, facial recognition</td><td style="padding:10px;border:1px solid var(--border,#ddd)">🔴 Special Category</td></tr>
  <tr><td style="padding:10px;border:1px solid var(--border,#ddd)">Political/Religious</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Political opinions, religious beliefs</td><td style="padding:10px;border:1px solid var(--border,#ddd)">🔴 Special Category</td></tr>
</table>

{callout("💡", "Key Insight", "Even data that seems harmless on its own can become personal data when combined. For example, a job title + department + office location might uniquely identify one person.", "#1a3a5c")}

<h3>The 7 GDPR Principles</h3>
<p>Every data processing activity must comply with these principles:</p>

<ol>
  <li><strong>Lawfulness, Fairness & Transparency:</strong> Have a legal basis for processing; be open about what you do with data</li>
  <li><strong>Purpose Limitation:</strong> Only collect data for specific, stated purposes — don't repurpose it without consent</li>
  <li><strong>Data Minimization:</strong> Collect only what you need — no "just in case" data hoarding</li>
  <li><strong>Accuracy:</strong> Keep data up to date; delete or correct inaccurate records promptly</li>
  <li><strong>Storage Limitation:</strong> Don't keep data longer than necessary — define and enforce retention periods</li>
  <li><strong>Integrity & Confidentiality:</strong> Protect data with appropriate technical and organizational measures</li>
  <li><strong>Accountability:</strong> Be able to demonstrate compliance — document your processes</li>
</ol>

<h3>The 6 Lawful Bases for Processing</h3>
<p>You need at least ONE of these to process personal data:</p>
<table style="width:100%;border-collapse:collapse;margin:16px 0">
  <tr style="background:var(--surface-hover,#f0f0f0)"><th style="padding:10px;border:1px solid var(--border,#ddd)">Basis</th><th style="padding:10px;border:1px solid var(--border,#ddd)">When to Use</th><th style="padding:10px;border:1px solid var(--border,#ddd)">Example</th></tr>
  <tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Consent</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Individual freely agrees</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Marketing emails opt-in</td></tr>
  <tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Contract</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Needed to fulfill a contract</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Processing employee payroll</td></tr>
  <tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Legal Obligation</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Required by law</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Tax reporting to government</td></tr>
  <tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Vital Interests</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Protect someone's life</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Emergency medical situation</td></tr>
  <tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Public Task</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Official authority/public interest</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Government agency processing</td></tr>
  <tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Legitimate Interest</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Business need, balanced with rights</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Fraud prevention analytics</td></tr>
</table>

<h3>Individual Rights Under GDPR</h3>
<p>Data subjects (the people whose data we process) have these rights:</p>
<ol>
  <li><strong>Right of Access (Article 15):</strong> "What data do you hold about me?" — Must respond within 30 days</li>
  <li><strong>Right to Rectification (Article 16):</strong> "Fix my incorrect data" — Correct it without undue delay</li>
  <li><strong>Right to Erasure (Article 17):</strong> "Delete my data" — Also known as the "Right to be Forgotten"</li>
  <li><strong>Right to Restrict Processing (Article 18):</strong> "Stop using my data but don't delete it"</li>
  <li><strong>Right to Data Portability (Article 20):</strong> "Give me my data in a portable format"</li>
  <li><strong>Right to Object (Article 21):</strong> "I don't want you to process my data for this purpose"</li>
  <li><strong>Rights Related to Automated Decision-Making (Article 22):</strong> "I want a human to review this automated decision"</li>
</ol>

{scenario_box(
    "A customer emails you saying: 'I want all my data deleted from your systems immediately.' You check and find their data is in the CRM, the billing system, and an old email thread.",
    ["Delete everything immediately from all systems",
     "Acknowledge the request, verify their identity, and forward to the Data Protection Officer within 24 hours",
     "Tell them you can't delete data that's needed for legal compliance",
     "Ignore it — they probably don't know about GDPR"],
    1,
    "<strong>Correct: Acknowledge and forward to the DPO.</strong> Erasure requests must be handled carefully. Some data (like tax records) may need to be retained for legal reasons. The DPO will determine what can be deleted and what must be kept, and respond within the 30-day deadline."
)}

<h3>Data Breach Response</h3>
<p>A data breach is any event where personal data is accidentally or unlawfully accessed, altered, disclosed, or destroyed.</p>

<h4>The 72-Hour Rule</h4>
<p>Under GDPR Article 33, <strong>the supervisory authority must be notified within 72 hours</strong> of becoming aware of a breach that poses a risk to individuals' rights. This means:</p>
<ol>
  <li><strong>Hour 0-1:</strong> You discover or suspect a breach → Report immediately to IT Security AND the DPO</li>
  <li><strong>Hour 1-24:</strong> Initial assessment — What data was affected? How many people? What's the risk?</li>
  <li><strong>Hour 24-48:</strong> Containment and documentation — Stop the breach, preserve evidence, document everything</li>
  <li><strong>Hour 48-72:</strong> Official notification to the supervisory authority (and affected individuals if high risk)</li>
</ol>

{callout("⚠️", "Real-World Impact", "<strong>British Airways</strong> was fined <strong>£20 million</strong> for a 2018 breach affecting 400,000 customers. The breach occurred because of insufficient security measures — something every employee can help prevent.", "#ef4444")}

<h3>Your Daily Data Privacy Checklist</h3>
<ul>
  <li>✅ Lock your screen when leaving your desk (<strong>Win+L</strong> or <strong>Ctrl+Cmd+Q</strong>)</li>
  <li>✅ Use encrypted email for sensitive information</li>
  <li>✅ Verify the recipient before sending data — double-check email addresses</li>
  <li>✅ Don't store personal data on USB drives or personal cloud storage</li>
  <li>✅ Shred physical documents containing personal data</li>
  <li>✅ Report any suspected breach to security@company.com within 1 hour</li>
  <li>✅ Review and clean up old files and emails containing personal data quarterly</li>
  <li>✅ Use "BCC" when emailing groups to protect email addresses</li>
</ul>

{knowledge_check(
    "Under GDPR, how quickly must a data breach be reported to the supervisory authority?",
    ["24 hours", "48 hours", "72 hours", "7 days"],
    2,
    "GDPR Article 33 requires notification to the supervisory authority within <strong>72 hours</strong> of becoming aware of a breach that poses a risk to individuals' rights."
)}

<h3>Case Study: The Accidental Email</h3>
<div style="background:var(--surface-hover,#f1f5f9);padding:20px 24px;border-radius:10px;margin:20px 0">
  <p><strong>The Situation:</strong> An HR coordinator was sending a spreadsheet of employee salaries to the Finance Director. She accidentally selected the wrong "Finance" group from the autocomplete — the spreadsheet went to all 200+ members of the Finance department instead of just the director.</p>
  <p><strong>What Happened:</strong></p>
  <ul>
    <li>The coordinator realized the mistake within 10 minutes</li>
    <li>She immediately reported it to the DPO and IT Security</li>
    <li>IT attempted to recall the email (successful for some but not all recipients)</li>
    <li>A notice was sent to all recipients asking them to delete the email unread</li>
    <li>The incident was logged as a data breach, though not reported externally due to low risk</li>
  </ul>
  <p><strong>The Lesson:</strong> Always double-check recipients before sending sensitive data. Use "Send with delay" settings in your email client. For highly sensitive documents, consider using a secure sharing link with access controls instead of attachments.</p>
</div>

<h3>💡 Key Takeaways</h3>
<ul>
  <li>Personal data is broader than you think — even IP addresses count</li>
  <li>You need a <strong>lawful basis</strong> before collecting or processing any personal data</li>
  <li>Data subjects have <strong>7 rights</strong> — and we must respond within <strong>30 days</strong></li>
  <li>Report breaches <strong>immediately</strong> — the 72-hour clock starts when you become aware</li>
  <li>When in doubt, treat data as personal and handle it with care</li>
</ul>
"""

# ── Security 101 — Module 0: Cybersecurity Fundamentals ──
CONTENT[("course-security-101", 0)] = f"""
<h2>Cybersecurity Fundamentals</h2>

{stat_box([("💰","$4.88M","Avg Breach Cost"),("📧","91%","Attacks Start with Email"),("⏱️","277","Days to Detect"),("👤","74%","Involve Human Error")])}

<h3>🎯 Learning Objectives</h3>
<ul>
  <li>Understand the current cyber threat landscape and its impact on businesses</li>
  <li>Master the CIA Triad — the foundation of all information security</li>
  <li>Identify the most common attack vectors and how they target employees</li>
  <li>Apply practical security habits to your daily work routine</li>
</ul>

<h3>The Current Threat Landscape</h3>
<p>Cybercrime is the <strong>fastest-growing criminal enterprise in the world</strong>. By 2025, cybercrime damages are projected to reach <strong>$10.5 trillion annually</strong> — more than the GDP of every country except the US and China.</p>

<h4>Top Threats to Organizations</h4>
<table style="width:100%;border-collapse:collapse;margin:16px 0">
  <tr style="background:var(--surface-hover,#f0f0f0)"><th style="padding:10px;border:1px solid var(--border,#ddd)">Threat</th><th style="padding:10px;border:1px solid var(--border,#ddd)">How It Works</th><th style="padding:10px;border:1px solid var(--border,#ddd)">Avg Cost</th><th style="padding:10px;border:1px solid var(--border,#ddd)">Prevention</th></tr>
  <tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Ransomware</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Encrypts your files; demands payment</td><td style="padding:10px;border:1px solid var(--border,#ddd)">$5.13M</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Backups, patching, awareness</td></tr>
  <tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Business Email Compromise</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Impersonates executives to trick employees</td><td style="padding:10px;border:1px solid var(--border,#ddd)">$4.89M</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Verification procedures, MFA</td></tr>
  <tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Supply Chain Attacks</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Compromises trusted vendors to access you</td><td style="padding:10px;border:1px solid var(--border,#ddd)">$4.63M</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Vendor assessment, monitoring</td></tr>
  <tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Insider Threats</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Employees (intentional or accidental)</td><td style="padding:10px;border:1px solid var(--border,#ddd)">$4.18M</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Access controls, monitoring, training</td></tr>
</table>

<h3>The CIA Triad — Security's Foundation</h3>
<p>Every security decision comes back to protecting these three properties:</p>

<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:20px 0">
  <div style="background:linear-gradient(135deg,#1a3a5c08,#1a3a5c03);border:1px solid var(--border,#e2e8f0);padding:20px;border-radius:10px;text-align:center">
    <div style="font-size:32px;margin-bottom:8px">🔒</div>
    <strong style="display:block;margin-bottom:6px">Confidentiality</strong>
    <p style="font-size:.84rem;color:var(--text-secondary,#64748b);margin:0">Only authorized people can access the data. Enforced through encryption, access controls, and authentication.</p>
  </div>
  <div style="background:linear-gradient(135deg,#2c7a7b08,#2c7a7b03);border:1px solid var(--border,#e2e8f0);padding:20px;border-radius:10px;text-align:center">
    <div style="font-size:32px;margin-bottom:8px">✅</div>
    <strong style="display:block;margin-bottom:6px">Integrity</strong>
    <p style="font-size:.84rem;color:var(--text-secondary,#64748b);margin:0">Data is accurate, complete, and hasn't been tampered with. Enforced through hashing, digital signatures, and audit trails.</p>
  </div>
  <div style="background:linear-gradient(135deg,#22c55e08,#22c55e03);border:1px solid var(--border,#e2e8f0);padding:20px;border-radius:10px;text-align:center">
    <div style="font-size:32px;margin-bottom:8px">⚡</div>
    <strong style="display:block;margin-bottom:6px">Availability</strong>
    <p style="font-size:.84rem;color:var(--text-secondary,#64748b);margin:0">Systems and data are accessible when needed. Enforced through redundancy, backups, and disaster recovery.</p>
  </div>
</div>

<h3>Understanding Attack Vectors</h3>
<p>An attack vector is the method or path an attacker uses to gain access. Here's how most attacks unfold:</p>

<h4>The Cyber Kill Chain</h4>
<p>Developed by Lockheed Martin, this framework shows the 7 stages of a cyberattack:</p>
<ol>
  <li><strong>Reconnaissance:</strong> Attacker researches the target (LinkedIn, company website, social media)</li>
  <li><strong>Weaponization:</strong> Creates a malicious payload (infected PDF, malware-laced link)</li>
  <li><strong>Delivery:</strong> Sends the weapon to the target (phishing email, compromised website)</li>
  <li><strong>Exploitation:</strong> The payload triggers — a vulnerability is exploited</li>
  <li><strong>Installation:</strong> Malware is installed on the target system</li>
  <li><strong>Command & Control:</strong> Attacker establishes remote access to the compromised system</li>
  <li><strong>Actions on Objectives:</strong> Data exfiltration, ransomware deployment, or lateral movement</li>
</ol>

{callout("🔑", "Your Role", "As an employee, you are the <strong>first line of defense</strong> — most attacks are stopped at Stage 3 (Delivery) or Stage 4 (Exploitation) by alert employees who recognize and report suspicious activity.", "#2c7a7b")}

{scenario_box(
    "You receive an email from what appears to be your CEO, urgently asking you to wire transfer $50,000 to a vendor 'before end of day.' The email address looks correct at first glance. You've never received such a request before.",
    ["Complete the transfer — the CEO wouldn't make this request if it wasn't urgent",
     "Reply to the email asking for confirmation",
     "Call the CEO directly on a known phone number to verify, and report the email to IT Security",
     "Forward the email to your manager and wait for instructions"],
    2,
    "<strong>Correct: Verify via a separate channel.</strong> This is a classic Business Email Compromise (BEC) attack. Never use the reply function (the attacker controls the email). Always verify unexpected financial requests through a separate, trusted channel (phone call, in-person). Report to IT Security regardless."
)}

<h3>🛡️ Your Daily Security Habits</h3>
<p>Security isn't just about technology — it's about behavior. These 10 habits will protect you and the organization:</p>

<ol>
  <li><strong>Lock your screen</strong> every time you leave your desk — even for 30 seconds</li>
  <li><strong>Use unique, strong passwords</strong> for every account — use a password manager</li>
  <li><strong>Enable MFA</strong> on every account that supports it</li>
  <li><strong>Verify before you trust</strong> — unexpected emails, calls, or messages need verification</li>
  <li><strong>Keep software updated</strong> — install patches within 48 hours of release</li>
  <li><strong>Don't plug in unknown USB drives</strong> — they could contain malware</li>
  <li><strong>Use the VPN</strong> when working remotely or on public Wi-Fi</li>
  <li><strong>Report suspicious activity</strong> immediately — even if you're not sure</li>
  <li><strong>Shred sensitive documents</strong> — dumpster diving is a real attack method</li>
  <li><strong>Think before you click</strong> — hover over links, verify senders, question urgency</li>
</ol>

{knowledge_check(
    "What percentage of cyberattacks involve human error as a contributing factor?",
    ["25%", "50%", "74%", "95%"],
    2,
    "According to the Verizon Data Breach Investigations Report, <strong>74%</strong> of all breaches involve the human element — including social engineering, errors, and misuse. This is why security awareness training is so critical."
)}

<h3>Case Study: The SolarWinds Attack</h3>
<div style="background:var(--surface-hover,#f1f5f9);padding:20px 24px;border-radius:10px;margin:20px 0">
  <p><strong>What happened:</strong> In 2020, hackers compromised SolarWinds' Orion software update mechanism. A trojanized update was distributed to ~18,000 organizations, including Fortune 500 companies and US government agencies.</p>
  <p><strong>Impact:</strong> The attackers had access to networks for <strong>9 months</strong> before detection. Affected organizations included Microsoft, Intel, the US Treasury, and the Department of Homeland Security.</p>
  <p><strong>Lessons:</strong></p>
  <ul>
    <li>Supply chain security is critical — trust but verify your vendors</li>
    <li>Monitoring and detection are as important as prevention</li>
    <li>Even the most sophisticated organizations can be compromised</li>
    <li>The average "dwell time" (time between breach and detection) is <strong>277 days</strong></li>
  </ul>
</div>

<h3>💡 Key Takeaways</h3>
<ul>
  <li>Cybersecurity is <strong>everyone's responsibility</strong> — not just IT's</li>
  <li>The CIA Triad (Confidentiality, Integrity, Availability) guides all security decisions</li>
  <li>Most attacks exploit <strong>human behavior</strong>, not technical vulnerabilities</li>
  <li>Your 10 daily security habits are more powerful than any firewall</li>
  <li>When in doubt, <strong>report it</strong> — there's no penalty for false alarms</li>
</ul>
"""


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    updated = 0

    for (course_id, order_index), html in CONTENT.items():
        cur = conn.execute(
            "SELECT id FROM modules WHERE course_id = ? AND order_index = ?",
            (course_id, order_index),
        )
        row = cur.fetchone()
        if row:
            conn.execute(
                "UPDATE modules SET content = ? WHERE id = ?",
                (html.strip(), row["id"]),
            )
            updated += 1
            print(f"  ✅ {course_id} / module {order_index}")
        else:
            print(f"  ⚠️  Not found: {course_id} / module {order_index}")

    conn.commit()
    conn.close()
    print(f"\nDone — expanded {updated} modules with deep content.")


if __name__ == "__main__":
    main()
