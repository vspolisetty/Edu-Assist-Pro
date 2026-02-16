"""
Expand ALL 29 modules with 3-5x more content.
Each module gets: case studies, scenarios, knowledge checks, stat cards,
callout boxes, deep-dive sections, and practical exercises.
Run: python3 backend/expand_all_content.py
"""
import sqlite3, os, textwrap

DB = os.path.join(os.path.dirname(__file__), "courses.db")

# ─── Helpers ───
def cb(icon, title, body, c="#1a3a5c"):
    return f'<div style="background:linear-gradient(135deg,{c}08,{c}03);border-left:4px solid {c};padding:18px 22px;margin:24px 0;border-radius:0 8px 8px 0"><strong style="display:flex;align-items:center;gap:6px;margin-bottom:6px">{icon} {title}</strong><div style="font-size:.9rem;line-height:1.6">{body}</div></div>'

def sb(scenario, opts, ans, exp):
    ol=""
    for i,o in enumerate(opts):
        m="✅" if i==ans else "⬜"
        ol+=f"<li style='margin:4px 0'>{m} {o}</li>"
    return f'<div style="background:var(--surface-hover,#f1f5f9);border:1px solid var(--border,#e2e8f0);padding:20px 24px;margin:24px 0;border-radius:10px"><strong style="display:flex;align-items:center;gap:6px;margin-bottom:8px">🎯 Scenario-Based Exercise</strong><p style="margin:8px 0;font-style:italic">{scenario}</p><p style="margin:10px 0 4px;font-weight:600">What would you do?</p><ul style="list-style:none;margin:0;padding:0">{ol}</ul><details style="margin-top:12px"><summary style="cursor:pointer;color:var(--primary,#1a3a5c);font-weight:600;font-size:.88rem">Show Answer &amp; Explanation</summary><p style="margin:8px 0;padding:10px;background:var(--bg,#f7f8fc);border-radius:6px;font-size:.88rem">{exp}</p></details></div>'

def kc(q, opts, ans, exp):
    ol=""
    for i,o in enumerate(opts):
        m="✅" if i==ans else "○"
        ol+=f"<li style='margin:4px 0'>{m} {o}</li>"
    return f'<div style="background:linear-gradient(135deg,#22c55e08,#22c55e02);border:1px solid #22c55e40;padding:18px 22px;margin:20px 0;border-radius:10px"><strong style="display:flex;align-items:center;gap:6px;margin-bottom:8px">✅ Knowledge Check</strong><p style="margin:6px 0;font-weight:500">{q}</p><ul style="list-style:none;margin:8px 0;padding:0">{ol}</ul><details style="margin-top:8px"><summary style="cursor:pointer;color:#22c55e;font-weight:600;font-size:.88rem">Reveal Answer</summary><p style="margin:8px 0;padding:8px;background:#22c55e08;border-radius:6px;font-size:.88rem">{exp}</p></details></div>'

def stats(items):
    n=len(items)
    c=""
    for ic,v,l in items:
        c+=f'<div style="text-align:center;padding:16px"><div style="font-size:28px;margin-bottom:4px">{ic}</div><div style="font-size:1.3rem;font-weight:700;color:var(--primary,#1a3a5c)">{v}</div><div style="font-size:.78rem;color:var(--text-secondary,#64748b)">{l}</div></div>'
    return f'<div style="display:grid;grid-template-columns:repeat({n},1fr);gap:8px;margin:20px 0;background:var(--surface-hover,#f1f5f9);border-radius:10px;overflow:hidden">{c}</div>'

def case(title, situation, impact, lessons):
    ll = "".join(f"<li>{l}</li>" for l in lessons)
    return f'<div style="background:var(--surface-hover,#f1f5f9);padding:20px 24px;border-radius:10px;margin:20px 0"><h4 style="margin:0 0 10px">📖 Case Study: {title}</h4><p><strong>Situation:</strong> {situation}</p><p><strong>Impact:</strong> {impact}</p><p style="font-weight:600;margin:12px 0 6px">Lessons Learned:</p><ul>{ll}</ul></div>'


# ═══════════════════════════════════════════════════════════════
# ALL CONTENT — keyed by (course_id, order_index)
# ═══════════════════════════════════════════════════════════════
C = {}

# ────────────────────────────────────────────────────────────
# COURSE: COMPLIANCE 101
# ────────────────────────────────────────────────────────────

C[("course-compliance-101",0)] = f"""
<h2>Company Policies Overview</h2>
{stats([("📋","50+","Active Policies"),("👥","100%","Employee Coverage"),("📅","Annual","Review Cycle"),("⚖️","Zero","Tolerance")])}

<h3>🎯 Learning Objectives</h3>
<ul><li>Understand the purpose, scope, and structure of company policies</li><li>Identify your responsibilities under each major policy area</li><li>Know where to find, reference, and report concerns about policies</li><li>Apply policy knowledge to real-world workplace scenarios</li></ul>

<h3>Why Policies Matter</h3>
<p>Company policies are the backbone of a well-run organization. They exist to <strong>protect employees</strong> from unfair treatment, <strong>ensure legal compliance</strong>, <strong>create consistency</strong>, <strong>reduce liability</strong>, and <strong>set clear expectations</strong>.</p>
{cb("📌","Did You Know?","Companies with well-documented policies experience <strong>40% fewer employee disputes</strong> and <strong>60% faster resolution times</strong>.","#2c7a7b")}

<h3>Code of Conduct: The Foundation</h3>
<h4>1. Act with Integrity</h4>
<p>Integrity means honesty and transparency in all business dealings: accurately reporting hours and expenses, never misrepresenting data, honoring commitments, and admitting mistakes promptly.</p>
<h4>2. Treat Others with Respect</h4>
<p>Value diverse perspectives, listen actively, address disagreements professionally (focus on issues not people), and never engage in gossip, bullying, or exclusionary behavior.</p>
<h4>3. Protect Company Assets</h4>
<p>Use company technology for authorized purposes only. Safeguard confidential information — lock screens, shred documents, use encrypted communication. Report lost or stolen equipment immediately.</p>
<h4>4. Follow the Law</h4>
<p>Compliance with all applicable laws is non-negotiable: anti-bribery (FCPA, UK Bribery Act), securities regulations, employment laws, and environmental regulations.</p>

{sb("Your manager asks you to 'adjust' some numbers in a client report to make quarterly results look better. She says 'everyone does it.'",["Do what your manager asks","Refuse and report through the Ethics Hotline","Adjust the numbers slightly","Ignore the request and hope she doesn't ask again"],1,"<strong>Correct: Refuse and report.</strong> Falsifying reports is a serious ethical and legal violation. Your manager's instruction doesn't override policy or law. Use the Ethics Hotline if uncomfortable reporting directly.")}

<h3>Key Policies Every Employee Must Know</h3>
<table style="width:100%;border-collapse:collapse;margin:16px 0"><tr style="background:var(--surface-hover,#f0f0f0)"><th style="padding:10px 14px;text-align:left;border:1px solid var(--border,#ddd)">Policy</th><th style="padding:10px 14px;text-align:left;border:1px solid var(--border,#ddd)">What It Covers</th><th style="padding:10px 14px;text-align:left;border:1px solid var(--border,#ddd)">Key Points</th></tr>
<tr><td style="padding:10px 14px;border:1px solid var(--border,#ddd)"><strong>Acceptable Use</strong></td><td style="padding:10px 14px;border:1px solid var(--border,#ddd)">Technology, email, internet, social media</td><td style="padding:10px 14px;border:1px solid var(--border,#ddd)">No illegal use; limited personal use OK</td></tr>
<tr><td style="padding:10px 14px;border:1px solid var(--border,#ddd)"><strong>Confidentiality</strong></td><td style="padding:10px 14px;border:1px solid var(--border,#ddd)">Trade secrets, client data, proprietary info</td><td style="padding:10px 14px;border:1px solid var(--border,#ddd)">Survives employment; breaches → legal action</td></tr>
<tr><td style="padding:10px 14px;border:1px solid var(--border,#ddd)"><strong>Attendance</strong></td><td style="padding:10px 14px;border:1px solid var(--border,#ddd)">Work hours, time tracking, absences</td><td style="padding:10px 14px;border:1px solid var(--border,#ddd)">Notify supervisor; 3 unexcused = disciplinary</td></tr>
<tr><td style="padding:10px 14px;border:1px solid var(--border,#ddd)"><strong>Conflict of Interest</strong></td><td style="padding:10px 14px;border:1px solid var(--border,#ddd)">Outside employment, investments</td><td style="padding:10px 14px;border:1px solid var(--border,#ddd)">Must disclose; transparency matters</td></tr>
<tr><td style="padding:10px 14px;border:1px solid var(--border,#ddd)"><strong>Travel &amp; Expense</strong></td><td style="padding:10px 14px;border:1px solid var(--border,#ddd)">Business travel, reimbursements</td><td style="padding:10px 14px;border:1px solid var(--border,#ddd)">Pre-approval; receipts over $25</td></tr>
<tr><td style="padding:10px 14px;border:1px solid var(--border,#ddd)"><strong>Social Media</strong></td><td style="padding:10px 14px;border:1px solid var(--border,#ddd)">Personal &amp; professional accounts</td><td style="padding:10px 14px;border:1px solid var(--border,#ddd)">Don't speak for company without authorization</td></tr></table>

<h3>📚 Deep Dive: Gift &amp; Entertainment Policy</h3>
<ul><li>Accept gifts <strong>under $50</strong> freely</li><li><strong>$50–$200</strong>: disclose to manager within 5 days</li><li><strong>Over $200</strong>: decline or return, report to Ethics Committee</li><li><strong>Cash/gift cards</strong> of any value: always decline</li><li><strong>Government officials:</strong> consult Legal first</li></ul>
{cb("⚠️","Common Mistake","A vendor sends a $100 gift basket during holidays. Many assume it's fine because 'it's the holidays.' <strong>Wrong.</strong> Disclose to your manager within 5 days since it exceeds $50.","#ef4444")}

<h3>How to Report Concerns</h3>
<ol><li><strong>Direct Supervisor</strong> (unless involved in the issue)</li><li><strong>HR Department:</strong> hr@company.com or in-person</li><li><strong>Ethics Hotline:</strong> 24/7, anonymous — 1-800-ETHICS</li><li><strong>Legal Department:</strong> for potential legal violations</li><li><strong>Open Door Policy:</strong> escalate to any management level</li></ol>
{cb("🛡️","Retaliation Protection","Retaliation against anyone who reports in good faith is <strong>strictly prohibited</strong> and is itself a terminable offense.","#22c55e")}

{kc("Which action is correct when you receive a $75 gift from a vendor?",["Keep it quietly","Disclose to your manager within 5 business days","Return it immediately","Share it with your team"],1,"Gifts between $50–$200 must be disclosed to your manager within 5 business days. You don't need to return it, but transparency is required.")}

{case("The Freelance Designer","Sarah discovers team member Tom uses his company laptop for a personal freelance business during work hours. Tom argues it doesn't affect performance.","Three policies were violated: Acceptable Use, Conflict of Interest, and Attendance. Tom was counseled and required to use personal equipment/time.",["Transparency would have prevented the situation entirely","The issue was lack of disclosure and misuse of resources"])}

<h3>📝 Where to Find Policies</h3>
<ul><li><strong>Employee Handbook:</strong> HR Portal → Documents</li><li><strong>Policy Updates:</strong> Email + intranet; acknowledgment within 7 days</li><li><strong>FAQ:</strong> hr.company.com/policy-faq</li><li><strong>HR Office Hours:</strong> Wednesdays 2-4 PM</li></ul>

<h3>💡 Key Takeaways</h3>
<ul><li>Policies protect <strong>you</strong> — they're your rights, not just rules</li><li>When in doubt, <strong>disclose</strong> — transparency is always right</li><li>Use the <strong>Ethics Hotline</strong> for anonymous reporting</li><li>Review the <strong>Employee Handbook</strong> at least annually</li><li><strong>No policy violation is worth short-term gain</strong></li></ul>
"""

C[("course-compliance-101",1)] = f"""
<h2>Data Privacy &amp; GDPR</h2>
{stats([("🔒","€20M","Max GDPR Fine"),("📊","4%","Revenue Penalty"),("🌍","27+","EU Countries"),("⏱️","72h","Breach Notification")])}

<h3>🎯 Learning Objectives</h3>
<ul><li>Understand data privacy principles and why they matter</li><li>Learn key GDPR provisions and how they apply daily</li><li>Handle personal data responsibly across all channels</li><li>Recognize data breaches and know the reporting timeline</li></ul>

<h3>What Is Personal Data?</h3>
<p>Under GDPR, personal data is <strong>any information that can identify a living person</strong>:</p>
<table style="width:100%;border-collapse:collapse;margin:16px 0"><tr style="background:var(--surface-hover,#f0f0f0)"><th style="padding:10px;text-align:left;border:1px solid var(--border,#ddd)">Category</th><th style="padding:10px;text-align:left;border:1px solid var(--border,#ddd)">Examples</th><th style="padding:10px;text-align:left;border:1px solid var(--border,#ddd)">Sensitivity</th></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)">Basic Identity</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Name, email, phone</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Standard</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)">Online Identifiers</td><td style="padding:10px;border:1px solid var(--border,#ddd)">IP address, cookies, device IDs</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Standard</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)">Financial</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Bank details, salary, credit score</td><td style="padding:10px;border:1px solid var(--border,#ddd)">High</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)">Health</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Medical records, insurance</td><td style="padding:10px;border:1px solid var(--border,#ddd)">🔴 Special Category</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)">Biometric</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Fingerprints, facial recognition</td><td style="padding:10px;border:1px solid var(--border,#ddd)">🔴 Special Category</td></tr></table>
{cb("💡","Key Insight","Even harmless-seeming data can become personal when combined. A job title + department + office location might uniquely identify one person.")}

<h3>The 7 GDPR Principles</h3>
<ol><li><strong>Lawfulness, Fairness &amp; Transparency</strong></li><li><strong>Purpose Limitation</strong></li><li><strong>Data Minimization</strong> — collect only what you need</li><li><strong>Accuracy</strong> — keep data up to date</li><li><strong>Storage Limitation</strong> — define retention periods</li><li><strong>Integrity &amp; Confidentiality</strong> — protect with tech measures</li><li><strong>Accountability</strong> — document your compliance</li></ol>

<h3>The 6 Lawful Bases for Processing</h3>
<table style="width:100%;border-collapse:collapse;margin:16px 0"><tr style="background:var(--surface-hover,#f0f0f0)"><th style="padding:10px;border:1px solid var(--border,#ddd)">Basis</th><th style="padding:10px;border:1px solid var(--border,#ddd)">When to Use</th><th style="padding:10px;border:1px solid var(--border,#ddd)">Example</th></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Consent</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Individual freely agrees</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Marketing opt-in</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Contract</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Needed for a contract</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Employee payroll</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Legal Obligation</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Required by law</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Tax reporting</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Vital Interests</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Protect someone's life</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Emergency medical</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Public Task</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Official authority</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Government agency</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Legitimate Interest</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Business need, balanced</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Fraud prevention</td></tr></table>

<h3>Individual Rights Under GDPR</h3>
<ol><li><strong>Right of Access (Art.15):</strong> "What data do you hold?" — respond within 30 days</li><li><strong>Right to Rectification (Art.16):</strong> Correct inaccurate data without delay</li><li><strong>Right to Erasure (Art.17):</strong> "Right to be Forgotten"</li><li><strong>Right to Restrict Processing (Art.18)</strong></li><li><strong>Right to Data Portability (Art.20)</strong></li><li><strong>Right to Object (Art.21)</strong></li><li><strong>Automated Decision-Making (Art.22):</strong> Right to human review</li></ol>

{sb("A customer emails: 'Delete all my data from your systems immediately.' Their data is in CRM, billing, and an old email thread.",["Delete everything immediately","Acknowledge, verify identity, forward to the DPO within 24 hours","Tell them you can't delete legally required data","Ignore it"],1,"<strong>Correct: Acknowledge and forward to DPO.</strong> Some data (tax records) may need retention. The DPO determines what can be deleted and responds within the 30-day deadline.")}

<h3>Data Breach Response: The 72-Hour Rule</h3>
<p>Under GDPR Article 33, the supervisory authority must be notified <strong>within 72 hours</strong>:</p>
<ol><li><strong>Hour 0-1:</strong> Discover/suspect → report to IT Security AND DPO</li><li><strong>Hour 1-24:</strong> Assessment — what data, how many people, what risk?</li><li><strong>Hour 24-48:</strong> Containment, preserve evidence, document</li><li><strong>Hour 48-72:</strong> Official notification to authority (and individuals if high risk)</li></ol>
{cb("⚠️","Real-World Impact","<strong>British Airways</strong> was fined <strong>£20 million</strong> for a 2018 breach affecting 400,000 customers — due to insufficient security measures.","#ef4444")}

<h3>Your Daily Data Privacy Checklist</h3>
<ul><li>✅ Lock your screen when leaving (<strong>Win+L</strong> or <strong>Ctrl+Cmd+Q</strong>)</li><li>✅ Use encrypted email for sensitive info</li><li>✅ Double-check recipients before sending data</li><li>✅ No personal data on USB drives or personal cloud</li><li>✅ Shred physical documents with personal data</li><li>✅ Report suspected breaches to security@company.com within 1 hour</li><li>✅ Clean up old files quarterly</li><li>✅ Use "BCC" for group emails</li></ul>

{kc("Under GDPR, how quickly must a data breach be reported to the supervisory authority?",["24 hours","48 hours","72 hours","7 days"],2,"GDPR Article 33 requires notification within <strong>72 hours</strong> of becoming aware of a risk-posing breach.")}

{case("The Accidental Email","An HR coordinator sent a salary spreadsheet to all 200+ Finance members instead of just the director.","IT attempted email recall; a notice was sent to delete the email. Logged as a data breach but not reported externally (low risk).",["Always double-check recipients before sending sensitive data","Use 'Send with delay' settings in email","For sensitive documents, use secure sharing links with access controls"])}

<h3>💡 Key Takeaways</h3>
<ul><li>Personal data is broader than you think — IP addresses count</li><li>You need a <strong>lawful basis</strong> before processing any personal data</li><li>Data subjects have <strong>7 rights</strong> — respond within <strong>30 days</strong></li><li>Report breaches <strong>immediately</strong> — the 72-hour clock starts when you become aware</li><li>When in doubt, treat data as personal and handle with care</li></ul>
"""

C[("course-compliance-101",2)] = f"""
<h2>Workplace Safety</h2>
{stats([("🏥","2.8M","Workplace Injuries/yr"),("💰","$167B","Annual Cost"),("📉","5%","YoY Improvement"),("🎯","Zero","Target Incidents")])}

<h3>🎯 Learning Objectives</h3>
<ul><li>Identify common workplace hazards across office and field environments</li><li>Master emergency procedures and evacuation protocols</li><li>Understand OSHA requirements and employer obligations</li><li>Apply safety principles to your daily routine</li></ul>

<h3>Why Workplace Safety Matters</h3>
<p>Under <strong>OSHA</strong> regulations, every employer must provide a safe working environment. But safety isn't just about compliance — it's about protecting people you work with every day.</p>

<h3>Common Workplace Hazards</h3>
<table style="width:100%;border-collapse:collapse;margin:16px 0"><tr style="background:var(--surface-hover,#f0f0f0)"><th style="padding:10px;border:1px solid var(--border,#ddd)">Hazard</th><th style="padding:10px;border:1px solid var(--border,#ddd)">Examples</th><th style="padding:10px;border:1px solid var(--border,#ddd)">Prevention</th></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Ergonomic</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Poor posture, repetitive strain, eye strain</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Adjustable desks, 20-20-20 rule, breaks</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Slips &amp; Falls</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Wet floors, loose cables, uneven surfaces</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Signage, cable management, non-slip mats</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Electrical</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Faulty wiring, overloaded outlets</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Regular inspections, surge protectors</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Fire</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Blocked exits, flammable materials</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Fire drills, extinguisher access</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Psychological</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Stress, burnout, workplace violence</td><td style="padding:10px;border:1px solid var(--border,#ddd)">EAP, mental health days, training</td></tr></table>

<h3>The 20-20-20 Rule for Screen Workers</h3>
<p>Every <strong>20 minutes</strong>, look at something <strong>20 feet</strong> away for <strong>20 seconds</strong>. This simple practice reduces eye strain by 60%.</p>

<h3>Emergency Procedures — Step by Step</h3>
<ol><li><strong>Stay Calm</strong> — panic leads to poor decisions</li><li><strong>Alert Others</strong> — activate fire alarm or call emergency services</li><li><strong>Evacuate</strong> — use nearest exit; <strong>never use elevators during fire</strong></li><li><strong>Account for Everyone</strong> — floor wardens conduct headcounts at assembly point</li><li><strong>Do Not Re-Enter</strong> — wait for "all clear" from emergency personnel</li></ol>

{sb("You notice a small electrical spark from a power strip under your colleague's desk. The power strip looks old and has 6 devices plugged in.",["Ignore it — it was just a small spark","Unplug the power strip immediately and report it to Facilities","Move to a different desk and tell your colleague","Post about it on the team chat"],1,"<strong>Correct: Unplug immediately and report.</strong> Electrical sparks indicate an overloaded or faulty power strip — a fire hazard. Remove the source of danger, then report to Facilities for replacement.")}

<h3>Ergonomic Workstation Setup</h3>
<ul><li><strong>Monitor:</strong> top of screen at eye level, arm's length away</li><li><strong>Chair:</strong> feet flat on floor, knees at 90°, lumbar support</li><li><strong>Keyboard:</strong> wrists straight, elbows at 90°, shoulders relaxed</li><li><strong>Lighting:</strong> no glare on screen, adequate ambient light</li><li><strong>Breaks:</strong> stand and stretch every 30-60 minutes</li></ul>

{cb("📊","Statistics","Workers who follow ergonomic guidelines experience <strong>60% fewer musculoskeletal disorders</strong> and report <strong>25% higher productivity</strong>.","#2c7a7b")}

<h3>Reporting Safety Incidents</h3>
<p>All incidents — even "near misses" — must be reported using the <strong>Incident Report Form</strong> within <strong>24 hours</strong>. Reports go to your supervisor and the Safety Committee. Anonymous reporting is available via the safety hotline.</p>

{kc("What should you do if you witness a 'near miss' (an incident that almost caused injury)?",["Nothing — no one was hurt","Report it within 24 hours using the Incident Report Form","Tell your coworker to be more careful","Wait until your next team meeting to mention it"],1,"ALL incidents including near misses must be reported within 24 hours. Near misses are valuable learning opportunities that can prevent actual injuries.")}

<h3>💡 Key Takeaways</h3>
<ul><li>Safety is a <strong>shared responsibility</strong> — see something, say something</li><li>Know your <strong>evacuation route</strong> and assembly point</li><li>Follow the <strong>20-20-20 rule</strong> for eye health</li><li>Report <strong>all incidents</strong> including near misses within 24 hours</li><li>Good ergonomics = better health AND better productivity</li></ul>
"""

C[("course-compliance-101",3)] = f"""
<h2>Anti-Harassment Training</h2>
{stats([("🚫","Zero","Tolerance Policy"),("📞","24/7","Ethics Hotline"),("🛡️","100%","Retaliation Protection"),("📋","72h","Investigation Start")])}

<h3>🎯 Learning Objectives</h3>
<ul><li>Define workplace harassment and its different forms</li><li>Understand the legal framework (Title VII, state laws)</li><li>Know bystander responsibility and intervention techniques</li><li>Master the reporting process and understand protections</li></ul>

<h3>What Is Workplace Harassment?</h3>
<p>Any <strong>unwelcome conduct</strong> based on race, color, religion, sex, national origin, age, disability, or genetic information that creates a hostile, intimidating, or offensive work environment.</p>

<h3>Forms of Harassment</h3>
<ul><li><strong>Verbal:</strong> Derogatory comments, slurs, unwelcome jokes, intimidating language</li><li><strong>Physical:</strong> Unwanted touching, blocking movement, physical intimidation</li><li><strong>Visual:</strong> Offensive images, emails, gestures</li><li><strong>Cyber:</strong> Online bullying, threatening messages, inappropriate social media</li><li><strong>Quid Pro Quo:</strong> Employment decisions conditioned on submission to unwelcome conduct</li><li><strong>Hostile Environment:</strong> Pervasive behavior that interferes with work ability</li></ul>
{cb("⚠️","Important","Harassment doesn't require intent. Even well-meaning comments can constitute harassment if they are <strong>unwelcome</strong> and create a hostile environment for the recipient.","#ef4444")}

<h3>The Bystander's Role — The 5 D's</h3>
<ol><li><strong>Direct:</strong> Confront the behavior directly ("That's not appropriate")</li><li><strong>Distract:</strong> Interrupt the situation ("Hey, did you see the email about the meeting?")</li><li><strong>Delegate:</strong> Get someone with authority to intervene</li><li><strong>Document:</strong> Write down what happened (who, what, when, where)</li><li><strong>Delay:</strong> Check on the person afterward ("Are you OK? I saw what happened")</li></ol>

{sb("During a team lunch, a colleague repeatedly makes jokes about another teammate's accent, despite the teammate looking visibly uncomfortable. Others laugh nervously.",["Laugh along — it's just jokes","Wait and talk to the joke-teller privately later","Use the 'Distract' technique — change the subject immediately, then check on the teammate afterward","Report it to HR the next day without saying anything now"],2,"<strong>Best approach: Distract then follow up.</strong> Changing the subject immediately stops the behavior. Then check on the affected colleague (Delay/Document). If the behavior continues, escalate to HR. Using multiple D's is often the most effective approach.")}

<h3>How to Report</h3>
<ul><li><strong>Direct Supervisor</strong> (unless involved)</li><li><strong>HR Department:</strong> email, phone, or in-person</li><li><strong>Ethics Hotline:</strong> anonymous, 24/7</li><li><strong>Online Portal:</strong> ethics.company.com</li></ul>

<h3>What Happens After You Report</h3>
<ol><li><strong>Acknowledgment:</strong> HR confirms receipt within 24 hours</li><li><strong>Investigation begins:</strong> within 72 hours — interviews, evidence review</li><li><strong>Interim measures:</strong> separation of parties if needed</li><li><strong>Resolution:</strong> findings and corrective action (typically within 30 days)</li><li><strong>Follow-up:</strong> HR checks in with the reporter to ensure no retaliation</li></ol>

{kc("Which of the following is TRUE about workplace harassment?",["It only counts if the harasser intends to offend","A single severe incident can constitute harassment","It only applies to interactions between supervisors and subordinates","You must confront the harasser directly before reporting"],1,"A single severe incident CAN constitute harassment. Intent is not required — what matters is whether the conduct is unwelcome and creates a hostile environment. Anyone can harass anyone regardless of hierarchy.")}

<h3>💡 Key Takeaways</h3>
<ul><li>Everyone deserves a respectful workplace</li><li>Harassment doesn't require <strong>intent</strong> — impact matters</li><li>Use the <strong>5 D's</strong> as a bystander</li><li>Reports are <strong>protected</strong> — retaliation is a terminable offense</li><li>When in doubt, <strong>report</strong> — HR will investigate</li></ul>
"""

C[("course-compliance-101",4)] = f"""
<h2>Ethics &amp; Code of Conduct</h2>
{stats([("🏛️","4 Pillars","Ethical Framework"),("📋","100%","Disclosure Rate Target"),("🔒","Anonymous","Reporting Available"),("⚖️","Federal","Whistleblower Protection")])}

<h3>🎯 Learning Objectives</h3>
<ul><li>Understand the company's ethical standards and their practical application</li><li>Recognize and properly disclose conflicts of interest</li><li>Know whistleblower protections and how to use them</li><li>Apply ethical decision-making frameworks to real scenarios</li></ul>

<h3>The Four Ethical Pillars</h3>
<ol><li><strong>Honesty:</strong> Be truthful in all communications and transactions</li><li><strong>Accountability:</strong> Own your decisions and their consequences</li><li><strong>Fairness:</strong> Treat everyone equitably, without favoritism or bias</li><li><strong>Respect:</strong> Value diversity and treat colleagues with dignity</li></ol>

<h3>The Ethics Decision Framework</h3>
<p>When facing an ethical dilemma, ask yourself these 5 questions:</p>
<ol><li>Is it <strong>legal</strong>?</li><li>Does it comply with <strong>company policy</strong>?</li><li>Would I be comfortable if it were <strong>reported in the news</strong>?</li><li>Would I be proud to tell my <strong>family</strong> about this decision?</li><li>Does it treat all parties <strong>fairly</strong>?</li></ol>
<p>If the answer to ANY of these is "no" or "I'm not sure," <strong>stop and seek guidance</strong>.</p>

<h3>Conflicts of Interest</h3>
<p>A conflict occurs when personal interests could influence — or appear to influence — professional judgment:</p>
<ul><li>Financial interest in a vendor or competitor</li><li>Hiring or supervising a family member</li><li>Accepting gifts over $50 from business partners</li><li>Using company resources for personal gain</li><li>Having a romantic relationship with someone in your reporting chain</li></ul>
{cb("💡","Remember","Disclosure ≠ wrongdoing. Disclosing a potential conflict shows <strong>transparency</strong> and allows the company to manage it appropriately.")}

{sb("You're on the vendor selection committee. Your spouse works for one of the vendors being evaluated. No one on the committee knows about the relationship.",["Say nothing — your spouse works in a different department","Disclose the relationship to the committee chair and recuse yourself from the decision","Vote for a different vendor to avoid any appearance of bias","Mention it casually but continue participating"],1,"<strong>Correct: Disclose and recuse.</strong> Even if you'd be objective, the <em>appearance</em> of a conflict undermines trust. Disclosure and recusal protects you, the committee, and the integrity of the process.")}

<h3>Whistleblower Protections</h3>
<p>Employees who report in good faith are protected by:</p>
<ul><li>Federal and state whistleblower protection laws (Sarbanes-Oxley, Dodd-Frank)</li><li>Internal non-retaliation policy</li><li>Anonymous reporting channels</li></ul>
<p><strong>Retaliation</strong> (termination, demotion, exclusion, reduced hours) against whistleblowers is a <strong>terminable offense</strong> and may result in legal action.</p>

{kc("What is the FIRST thing you should do when you identify a potential conflict of interest?",["Resolve it yourself","Disclose it using the Conflict of Interest Disclosure Form","Ask a colleague for advice","Wait to see if it becomes an actual problem"],1,"Always disclose FIRST. The Ethics Committee or your manager will determine if action is needed. Waiting until a conflict becomes a problem is far worse than proactive disclosure.")}

<h3>💡 Key Takeaways</h3>
<ul><li>Ethics goes beyond the law — it's doing right <strong>when no one is watching</strong></li><li>Use the <strong>5-question framework</strong> for ethical decisions</li><li><strong>Disclose</strong> potential conflicts immediately — disclosure ≠ wrongdoing</li><li>Whistleblower protections are <strong>real and enforced</strong></li><li>When in doubt, <strong>ask</strong> — Ethics Committee is here to help</li></ul>
"""

# ────────────────────────────────────────────────────────────
# COURSE: SECURITY 101
# ────────────────────────────────────────────────────────────

C[("course-security-101",0)] = f"""
<h2>Cybersecurity Fundamentals</h2>
{stats([("💰","$4.88M","Avg Breach Cost"),("📧","91%","Attacks via Email"),("⏱️","277","Days to Detect"),("👤","74%","Human Error")])}

<h3>🎯 Learning Objectives</h3>
<ul><li>Understand the current cyber threat landscape</li><li>Master the CIA Triad — the foundation of information security</li><li>Identify the most common attack vectors</li><li>Apply practical security habits to your daily routine</li></ul>

<h3>The CIA Triad</h3>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:20px 0">
<div style="background:linear-gradient(135deg,#1a3a5c08,#1a3a5c03);border:1px solid var(--border,#e2e8f0);padding:20px;border-radius:10px;text-align:center"><div style="font-size:32px;margin-bottom:8px">🔒</div><strong>Confidentiality</strong><p style="font-size:.84rem;color:var(--text-secondary,#64748b);margin:4px 0 0">Only authorized people can access data. Enforced through encryption, access controls, authentication.</p></div>
<div style="background:linear-gradient(135deg,#2c7a7b08,#2c7a7b03);border:1px solid var(--border,#e2e8f0);padding:20px;border-radius:10px;text-align:center"><div style="font-size:32px;margin-bottom:8px">✅</div><strong>Integrity</strong><p style="font-size:.84rem;color:var(--text-secondary,#64748b);margin:4px 0 0">Data is accurate and untampered. Enforced through hashing, digital signatures, audit trails.</p></div>
<div style="background:linear-gradient(135deg,#22c55e08,#22c55e03);border:1px solid var(--border,#e2e8f0);padding:20px;border-radius:10px;text-align:center"><div style="font-size:32px;margin-bottom:8px">⚡</div><strong>Availability</strong><p style="font-size:.84rem;color:var(--text-secondary,#64748b);margin:4px 0 0">Systems accessible when needed. Enforced through redundancy, backups, disaster recovery.</p></div>
</div>

<h3>The Cyber Kill Chain</h3>
<ol><li><strong>Reconnaissance:</strong> Attacker researches target (LinkedIn, social media)</li><li><strong>Weaponization:</strong> Creates malicious payload</li><li><strong>Delivery:</strong> Sends weapon (phishing email, compromised site)</li><li><strong>Exploitation:</strong> Vulnerability exploited</li><li><strong>Installation:</strong> Malware installed</li><li><strong>Command &amp; Control:</strong> Remote access established</li><li><strong>Actions on Objectives:</strong> Data theft, ransomware, lateral movement</li></ol>
{cb("🔑","Your Role","You are the <strong>first line of defense</strong>. Most attacks are stopped at Stage 3 (Delivery) or 4 (Exploitation) by alert employees.","#2c7a7b")}

<h3>Top Threats</h3>
<table style="width:100%;border-collapse:collapse;margin:16px 0"><tr style="background:var(--surface-hover,#f0f0f0)"><th style="padding:10px;border:1px solid var(--border,#ddd)">Threat</th><th style="padding:10px;border:1px solid var(--border,#ddd)">How It Works</th><th style="padding:10px;border:1px solid var(--border,#ddd)">Avg Cost</th></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Ransomware</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Encrypts files; demands payment</td><td style="padding:10px;border:1px solid var(--border,#ddd)">$5.13M</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Business Email Compromise</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Impersonates executives</td><td style="padding:10px;border:1px solid var(--border,#ddd)">$4.89M</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Supply Chain</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Compromises trusted vendors</td><td style="padding:10px;border:1px solid var(--border,#ddd)">$4.63M</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Insider Threats</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Employees (intentional or accidental)</td><td style="padding:10px;border:1px solid var(--border,#ddd)">$4.18M</td></tr></table>

{sb("You receive an email from your 'CEO' urgently requesting a $50,000 wire transfer to a vendor 'before end of day.' You've never received such a request.",["Complete the transfer — the CEO wouldn't ask if it wasn't urgent","Reply to the email asking for confirmation","Call the CEO on a known phone number to verify, and report to IT Security","Forward to your manager and wait"],2,"<strong>Correct: Verify via separate channel.</strong> This is a classic BEC attack. Never use the reply function. Always verify unexpected financial requests via phone. Report to IT Security regardless.")}

<h3>🛡️ 10 Daily Security Habits</h3>
<ol><li>Lock your screen every time you leave your desk</li><li>Use unique, strong passwords — use a password manager</li><li>Enable MFA on every account</li><li>Verify before you trust — check unexpected emails</li><li>Keep software updated within 48 hours</li><li>Don't plug in unknown USB drives</li><li>Use the VPN on public Wi-Fi</li><li>Report suspicious activity immediately</li><li>Shred sensitive documents</li><li>Think before you click — hover over links first</li></ol>

{kc("What percentage of cyberattacks involve human error?",["25%","50%","74%","95%"],2,"According to the Verizon DBIR, <strong>74%</strong> of all breaches involve the human element — social engineering, errors, and misuse.")}

<h3>💡 Key Takeaways</h3>
<ul><li>Cybersecurity is <strong>everyone's responsibility</strong></li><li>CIA Triad: Confidentiality, Integrity, Availability</li><li>Most attacks exploit <strong>human behavior</strong>, not technical vulnerabilities</li><li>Your 10 daily habits are more powerful than any firewall</li><li>When in doubt, <strong>report it</strong> — no penalty for false alarms</li></ul>
"""

C[("course-security-101",1)] = f"""
<h2>Phishing &amp; Social Engineering</h2>
{stats([("📧","3.4B","Phishing Emails/Day"),("💰","$17,700","Lost Every Minute"),("🎭","98%","of Attacks Are Social Eng."),("👁️","6s","To Spot a Fake")])}

<h3>🎯 Learning Objectives</h3>
<ul><li>Identify the different types of phishing attacks</li><li>Recognize social engineering tactics and manipulation techniques</li><li>Apply the SLAM method to evaluate suspicious messages</li><li>Know what to do when you suspect a phishing attempt</li></ul>

<h3>Types of Phishing</h3>
<table style="width:100%;border-collapse:collapse;margin:16px 0"><tr style="background:var(--surface-hover,#f0f0f0)"><th style="padding:10px;border:1px solid var(--border,#ddd)">Type</th><th style="padding:10px;border:1px solid var(--border,#ddd)">Description</th><th style="padding:10px;border:1px solid var(--border,#ddd)">Example</th></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Email Phishing</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Mass emails mimicking trusted sources</td><td style="padding:10px;border:1px solid var(--border,#ddd)">"Your account has been compromised"</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Spear Phishing</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Targeted at specific individuals</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Email referencing your actual projects</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Whaling</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Targets executives (C-suite)</td><td style="padding:10px;border:1px solid var(--border,#ddd)">"Board meeting agenda attached"</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Smishing</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">SMS/text-based phishing</td><td style="padding:10px;border:1px solid var(--border,#ddd)">"Your package delivery failed"</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Vishing</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Voice-based phishing (phone calls)</td><td style="padding:10px;border:1px solid var(--border,#ddd)">"This is IT support, we need your password"</td></tr></table>

<h3>The SLAM Method</h3>
<p>Use SLAM to evaluate every email:</p>
<ul><li><strong>S — Sender:</strong> Do you know them? Is the address slightly misspelled?</li><li><strong>L — Links:</strong> Hover before clicking. Does the URL match the displayed text?</li><li><strong>A — Attachments:</strong> Were you expecting a file? Is the extension suspicious (.exe, .scr)?</li><li><strong>M — Message:</strong> Is there urgency, threats, or too-good-to-be-true offers?</li></ul>

<h3>Social Engineering Tactics</h3>
<ul><li><strong>Authority:</strong> "I'm the CEO and I need this done NOW"</li><li><strong>Urgency:</strong> "Your account will be locked in 1 hour"</li><li><strong>Scarcity:</strong> "Only 2 spots left — register now"</li><li><strong>Social Proof:</strong> "Everyone in your department has already completed this"</li><li><strong>Reciprocity:</strong> "I helped you last week, now I need a small favor"</li><li><strong>Likability:</strong> Building rapport before making the request</li></ul>

{sb("You get an email from 'IT Support' saying your password expires today and to click a link to reset it. The email has the company logo and looks official.",["Click the link — it looks legitimate and time-sensitive","Check the sender's email address carefully, hover over the link, and if suspicious, report to IT Security","Reply asking if it's legitimate","Ignore it and hope nothing happens"],1,"<strong>Correct: Use SLAM.</strong> Check the sender (is it actually from IT?), hover over the link (does it go to company.com?), and if anything seems off, report it. Legitimate IT will never ask you to click a link to reset a password via email.")}

{kc("Which social engineering tactic is being used: 'Act now — this offer expires in 10 minutes!'?",["Authority","Urgency","Social Proof","Reciprocity"],1,"This is <strong>Urgency</strong> — creating artificial time pressure to prevent careful thinking.")}

<h3>What To Do When You Suspect Phishing</h3>
<ol><li><strong>Don't click</strong> any links or download attachments</li><li><strong>Don't reply</strong> to the message</li><li><strong>Report it:</strong> Forward to phishing@company.com or use the "Report Phishing" button</li><li><strong>Delete</strong> the message after reporting</li><li>If you already clicked, <strong>disconnect from network</strong> and call IT Security immediately</li></ol>

<h3>💡 Key Takeaways</h3>
<ul><li>Phishing is the <strong>#1 attack vector</strong> — 3.4 billion attempts per day</li><li>Use the <strong>SLAM method</strong> on every email</li><li>When in doubt, <strong>report it</strong> — better safe than sorry</li><li>If you clicked, <strong>disconnect and call IT</strong> immediately</li></ul>
"""

C[("course-security-101",2)] = f"""
<h2>Password &amp; Access Management</h2>
{stats([("🔐","81%","Breaches via Weak Passwords"),("⏱️","<1s","To Crack '123456'"),("🛡️","99.9%","Attacks Blocked by MFA"),("📊","13","Avg Passwords per Person")])}

<h3>🎯 Learning Objectives</h3>
<ul><li>Create strong, memorable passwords</li><li>Understand Multi-Factor Authentication (MFA) and why it matters</li><li>Apply the Principle of Least Privilege to access management</li><li>Use password managers effectively</li></ul>

<h3>What Makes a Strong Password?</h3>
<table style="width:100%;border-collapse:collapse;margin:16px 0"><tr style="background:var(--surface-hover,#f0f0f0)"><th style="padding:10px;border:1px solid var(--border,#ddd)">Password</th><th style="padding:10px;border:1px solid var(--border,#ddd)">Crack Time</th><th style="padding:10px;border:1px solid var(--border,#ddd)">Rating</th></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)">password123</td><td style="padding:10px;border:1px solid var(--border,#ddd)">&lt;1 second</td><td style="padding:10px;border:1px solid var(--border,#ddd)">🔴 Terrible</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)">Tr0ub4dor&3</td><td style="padding:10px;border:1px solid var(--border,#ddd)">~3 days</td><td style="padding:10px;border:1px solid var(--border,#ddd)">🟡 Weak</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)">correct-horse-battery-staple</td><td style="padding:10px;border:1px solid var(--border,#ddd)">~550 years</td><td style="padding:10px;border:1px solid var(--border,#ddd)">🟢 Strong</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)">kG#9mP!qL2@vN8&dR</td><td style="padding:10px;border:1px solid var(--border,#ddd)">~billions of years</td><td style="padding:10px;border:1px solid var(--border,#ddd)">🟢 Excellent</td></tr></table>

<h3>The Passphrase Method</h3>
<p>Use 4+ random words with modifiers: <strong>correct-horse-battery-staple</strong>. Longer is better — each word adds exponential complexity. Easy to remember, hard to crack.</p>

<h3>Multi-Factor Authentication (MFA)</h3>
<p>MFA requires two or more of:</p>
<ul><li><strong>Something you know:</strong> password, PIN</li><li><strong>Something you have:</strong> phone, hardware key, smart card</li><li><strong>Something you are:</strong> fingerprint, face, voice</li></ul>
{cb("📊","MFA Effectiveness","Microsoft reports that MFA blocks <strong>99.9%</strong> of automated attacks. It's the single most impactful security measure you can enable.","#22c55e")}

<h3>Principle of Least Privilege</h3>
<p>Users should only have access to the resources they <strong>need for their current role</strong> — nothing more. This limits damage if an account is compromised.</p>

{sb("A colleague who recently transferred departments asks you to share your login credentials so they can access a system they need for a project while waiting for their own access.",["Share your credentials temporarily","Politely decline and suggest they request access through IT","Log in for them and let them use your session","Give them your password but change it afterward"],1,"<strong>Correct: Decline and redirect to IT.</strong> Never share credentials. Each person must have their own access for accountability and security.")}

{kc("What does MFA protect against?",["All cyberattacks","Password-based attacks (even if your password is stolen)","Physical theft of devices","Social engineering"],1,"MFA protects against <strong>password-based attacks</strong>. Even if an attacker steals your password, they can't log in without the second factor.")}

<h3>💡 Key Takeaways</h3>
<ul><li>Use <strong>passphrases</strong> (4+ random words) — longer = stronger</li><li>Enable <strong>MFA everywhere</strong> — it blocks 99.9% of automated attacks</li><li><strong>Never share credentials</strong> — each person needs their own access</li><li>Use a <strong>password manager</strong> for unique passwords per account</li><li>Apply <strong>Least Privilege</strong> — request only the access you need</li></ul>
"""

C[("course-security-101",3)] = f"""
<h2>Incident Reporting</h2>
{stats([("⏱️","<1h","Report Deadline"),("📊","56%","Incidents Unreported"),("💰","$1.12M","Cost Savings with Fast Response"),("🎯","30min","Avg Containment Improvement")])}

<h3>🎯 Learning Objectives</h3>
<ul><li>Recognize what constitutes a security incident</li><li>Know the step-by-step reporting process</li><li>Understand the incident response lifecycle</li><li>Apply proper evidence preservation techniques</li></ul>

<h3>What Is a Security Incident?</h3>
<p>Any event that threatens the confidentiality, integrity, or availability of information or systems:</p>
<ul><li>Suspected phishing email (even if you didn't click)</li><li>Lost or stolen device (laptop, phone, USB)</li><li>Unauthorized access to systems or data</li><li>Malware infection or unusual system behavior</li><li>Accidental disclosure of confidential information</li><li>Physical security breach (tailgating, unauthorized entry)</li></ul>

<h3>The Reporting Process</h3>
<ol><li><strong>Recognize:</strong> Something seems wrong — trust your instincts</li><li><strong>Preserve:</strong> Don't turn off the computer or delete evidence</li><li><strong>Report:</strong> Contact IT Security within 1 hour — security@company.com or ext. 5555</li><li><strong>Document:</strong> Write down what happened, when, and what you observed</li><li><strong>Cooperate:</strong> Work with the incident response team</li></ol>
{cb("⚠️","Critical","<strong>56% of security incidents go unreported</strong> because employees worry about blame. There is NO punishment for reporting in good faith — even if it turns out to be a false alarm.","#ef4444")}

<h3>NIST Incident Response Lifecycle</h3>
<ol><li><strong>Preparation:</strong> Having policies, tools, and training in place</li><li><strong>Detection &amp; Analysis:</strong> Identifying and assessing the incident</li><li><strong>Containment, Eradication &amp; Recovery:</strong> Stopping the threat and restoring systems</li><li><strong>Post-Incident Activity:</strong> Lessons learned, process improvements</li></ol>

{sb("You notice your computer is running unusually slow and a program you don't recognize is running. What do you do?",["Restart the computer to fix the slowness","Try to uninstall the unknown program yourself","Disconnect from the network and call IT Security immediately","Ignore it — computers are slow sometimes"],2,"<strong>Correct: Disconnect and call IT.</strong> Unknown programs could be malware. Disconnecting prevents it from spreading. Don't restart (destroys evidence) or try to fix it yourself.")}

{kc("Why should you NOT turn off a potentially compromised computer?",["It wastes electricity","It could destroy forensic evidence in memory","The malware might resist being shut down","It takes too long to reboot"],1,"Turning off a computer can destroy <strong>forensic evidence in volatile memory (RAM)</strong> that incident responders need to understand the attack.")}

<h3>💡 Key Takeaways</h3>
<ul><li><strong>Report within 1 hour</strong> — speed saves money and limits damage</li><li>There's <strong>no punishment</strong> for reporting in good faith</li><li><strong>Don't try to fix it yourself</strong> — preserve evidence for the team</li><li>Document <strong>what, when, who, where</strong></li><li>Your report could prevent a much larger breach</li></ul>
"""

# ────────────────────────────────────────────────────────────
# COURSE: CUSTOMER SERVICE 201
# ────────────────────────────────────────────────────────────

C[("course-customer-201",0)] = f"""
<h2>Client Communication Standards</h2>
{stats([("📞","<4h","Response Time Target"),("⭐","95%","Client Satisfaction Goal"),("📧","3-5-3","Email Rule"),("🤝","100%","Professional Standard")])}

<h3>🎯 Learning Objectives</h3>
<ul><li>Master professional communication across all channels</li><li>Apply the 3-5-3 email framework for effective messages</li><li>Handle difficult conversations with confidence</li><li>Adapt communication style to different client types</li></ul>

<h3>The Communication Pyramid</h3>
<p>Effective client communication follows a hierarchy: <strong>Clarity → Empathy → Professionalism → Speed</strong>. Always prioritize being clear and empathetic over being fast.</p>

<h3>The 3-5-3 Email Framework</h3>
<ul><li><strong>3 seconds:</strong> Subject line must convey the purpose immediately</li><li><strong>5 sentences:</strong> Body should be 5 sentences or fewer for routine emails</li><li><strong>3 elements:</strong> Every email needs: Context → Action → Timeline</li></ul>
{cb("📧","Example","<strong>Subject:</strong> Invoice #4521 — Payment Confirmation Needed by Friday<br><strong>Body:</strong> Hi Sarah, Thank you for sending Invoice #4521. Our accounting team has reviewed it and found a discrepancy in line item 3. Could you please verify the quantity (we show 50 units, invoice says 55)? We'd appreciate a response by Friday so we can process payment on schedule. Best regards, [Name]","#2c7a7b")}

<h3>Channel Selection Guide</h3>
<table style="width:100%;border-collapse:collapse;margin:16px 0"><tr style="background:var(--surface-hover,#f0f0f0)"><th style="padding:10px;border:1px solid var(--border,#ddd)">Situation</th><th style="padding:10px;border:1px solid var(--border,#ddd)">Best Channel</th><th style="padding:10px;border:1px solid var(--border,#ddd)">Why</th></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)">Complex discussion</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Video call</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Visual cues, real-time Q&A</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)">Quick question</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Chat/IM</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Fast, informal, low-interruption</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)">Formal request</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Email</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Documentation trail, professional</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)">Sensitive/bad news</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Phone/in-person</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Empathy, tone control</td></tr></table>

{sb("A client sends an angry email: 'This is unacceptable! We've been waiting 3 weeks for delivery and nobody has bothered to update us. I'm considering switching providers.'",["Reply immediately with 'I understand your frustration' and a detailed timeline","Call the client within 1 hour to acknowledge, apologize, and provide a concrete resolution plan","Send a formal email CC'ing your manager to show escalation","Wait until you have all the facts before responding"],1,"<strong>Best approach: Call immediately.</strong> Angry clients need to feel heard. A phone call shows urgency and empathy. Acknowledge the problem, apologize sincerely, provide a concrete resolution plan with dates.")}

{kc("What is the correct priority order in the Communication Pyramid?",["Speed → Clarity → Empathy → Professionalism","Clarity → Empathy → Professionalism → Speed","Professionalism → Speed → Clarity → Empathy","Empathy → Speed → Professionalism → Clarity"],1,"Always prioritize being <strong>clear and empathetic</strong> over being fast.")}

<h3>💡 Key Takeaways</h3>
<ul><li>Use the <strong>3-5-3 framework</strong> for effective emails</li><li>Choose the <strong>right channel</strong> for the situation</li><li>Respond to client issues within <strong>4 hours</strong></li><li>For angry clients: <strong>call, don't email</strong></li><li>Clarity and empathy always come before speed</li></ul>
"""

C[("course-customer-201",1)] = f"""
<h2>Service Level Agreements (SLAs)</h2>
{stats([("📋","100%","SLA Compliance Target"),("⏱️","99.9%","Uptime Standard"),("📊","Monthly","Review Cadence"),("💰","$$$","Penalty Avoidance")])}

<h3>🎯 Learning Objectives</h3>
<ul><li>Understand what SLAs are and why they matter</li><li>Know the key components of an effective SLA</li><li>Monitor and report on SLA compliance</li><li>Handle SLA breaches professionally</li></ul>

<h3>What Is an SLA?</h3>
<p>A Service Level Agreement is a <strong>formal contract</strong> that defines the expected level of service between a provider and a client. It sets measurable targets, responsibilities, and consequences for non-compliance.</p>

<h3>Key SLA Components</h3>
<table style="width:100%;border-collapse:collapse;margin:16px 0"><tr style="background:var(--surface-hover,#f0f0f0)"><th style="padding:10px;border:1px solid var(--border,#ddd)">Component</th><th style="padding:10px;border:1px solid var(--border,#ddd)">Description</th><th style="padding:10px;border:1px solid var(--border,#ddd)">Example</th></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Response Time</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">How quickly you acknowledge</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Critical: 15min, High: 1hr</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Resolution Time</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">How quickly you resolve</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Critical: 4hr, High: 8hr</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Uptime</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Service availability</td><td style="padding:10px;border:1px solid var(--border,#ddd)">99.9% = 8.7hr downtime/yr</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Penalties</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Consequences for breach</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Service credits, fee reduction</td></tr></table>

{cb("📊","The Nines of Uptime","99% = 3.65 days downtime/year. 99.9% = 8.77 hours. 99.99% = 52.6 minutes. 99.999% = 5.26 minutes. Each additional nine is exponentially harder to achieve.","#1a3a5c")}

{sb("A client reports a critical system outage at 2:00 PM. Your SLA requires a 15-minute response and 4-hour resolution. At 2:10 PM, you've acknowledged the issue. At 5:30 PM, the issue is still unresolved.",["You're fine — you responded within 15 minutes","You've breached the SLA — resolution was due by 6:00 PM","You've breached both response and resolution SLAs","Contact the client with an update and revised timeline before the 6:00 PM deadline"],3,"<strong>Best action: Proactive communication.</strong> You met the response SLA but are at risk of breaching resolution. Contact the client BEFORE the deadline with an honest update and revised timeline. Proactive communication builds trust even during failures.")}

{kc("What does 99.9% uptime allow for per year?",["Zero downtime","52.6 minutes","8.77 hours","3.65 days"],2,"99.9% uptime allows for approximately <strong>8.77 hours</strong> of downtime per year.")}

<h3>💡 Key Takeaways</h3>
<ul><li>SLAs are <strong>contractual commitments</strong> — take them seriously</li><li>Know your <strong>response and resolution times</strong> by priority level</li><li>Proactive communication <strong>before</strong> a breach builds trust</li><li>Track and review SLA metrics <strong>monthly</strong></li></ul>
"""

C[("course-customer-201",2)] = f"""
<h2>Handling Complaints</h2>
{stats([("🔄","70%","Retention if Resolved"),("95%","Retention","If Resolved Quickly"),("😡","→😊","Goal: Detractor to Promoter"),("📝","HEARD","Framework")])}

<h3>🎯 Learning Objectives</h3>
<ul><li>Apply the HEARD framework for complaint resolution</li><li>Turn unhappy clients into loyal advocates</li><li>De-escalate emotional situations effectively</li><li>Document and learn from complaints</li></ul>

<h3>The HEARD Framework</h3>
<ol><li><strong>H — Hear:</strong> Listen fully without interrupting. Let them vent.</li><li><strong>E — Empathize:</strong> "I understand how frustrating that must be."</li><li><strong>A — Apologize:</strong> Sincerely. "I'm sorry this happened."</li><li><strong>R — Resolve:</strong> Propose a concrete solution with timeline.</li><li><strong>D — Diagnose:</strong> Find root cause to prevent recurrence.</li></ol>

{cb("📊","Statistics","<strong>70%</strong> of unhappy customers will do business again if you resolve their complaint. <strong>95%</strong> will return if resolved quickly. Complaints are <strong>opportunities</strong>.","#22c55e")}

<h3>De-escalation Techniques</h3>
<ul><li><strong>Lower your voice</strong> — calm is contagious</li><li><strong>Use the client's name</strong> — personalizes the interaction</li><li><strong>Acknowledge first, solve second</strong> — they need to feel heard before accepting solutions</li><li><strong>Avoid "but"</strong> — use "and" instead ("I understand your concern, AND here's what I can do...")</li><li><strong>Offer choices</strong> — gives the client a sense of control</li></ul>

{sb("A long-term client calls, furious: 'This is the THIRD time this month your system has gone down. My team can't work. I want to speak to someone in charge RIGHT NOW.'",["Transfer them to your manager immediately","Say 'I understand' and use the HEARD framework: hear them out, empathize, apologize, propose a specific resolution, then escalate if needed","Tell them the system is working fine on your end","Offer a discount immediately to calm them down"],1,"<strong>Use HEARD first.</strong> The client needs to feel heard before any transfer or solution. Listen, empathize, apologize, then propose a resolution. Only escalate if they specifically insist or the resolution needs approval you can't give.")}

{kc("In the HEARD framework, what does the 'D' stand for?",["Deliver","Document","Diagnose","Discuss"],2,"D = <strong>Diagnose</strong>. After resolving the complaint, find the root cause to prevent it from happening again.")}

<h3>💡 Key Takeaways</h3>
<ul><li>Complaints are <strong>opportunities</strong> to build loyalty</li><li>Use the <strong>HEARD framework</strong> every time</li><li><strong>Acknowledge before solving</strong> — emotions first, solutions second</li><li>Resolve quickly — <strong>95% retention</strong> when resolved fast</li></ul>
"""

C[("course-customer-201",3)] = f"""
<h2>Account Management</h2>
{stats([("📈","20%","Upsell Opportunity"),("🤝","Quarterly","Business Reviews"),("📊","NPS","Key Metric"),("💰","5-25x","Cheaper to Retain vs Acquire")])}

<h3>🎯 Learning Objectives</h3>
<ul><li>Understand the account manager's role and responsibilities</li><li>Conduct effective Quarterly Business Reviews (QBRs)</li><li>Identify expansion and upsell opportunities</li><li>Build lasting client relationships</li></ul>

<h3>The Account Manager's Mission</h3>
<p>Your job isn't just to manage — it's to be a <strong>trusted advisor</strong>. The best account managers understand the client's business as well as the client does.</p>

<h3>The QBR Framework</h3>
<ol><li><strong>Review:</strong> Performance metrics, SLA compliance, support tickets</li><li><strong>Roadmap:</strong> What's coming — new features, improvements, changes</li><li><strong>Feedback:</strong> What's working? What's not? What do they need?</li><li><strong>Strategy:</strong> Align on goals for the next quarter</li></ol>

{cb("💰","Revenue Impact","It costs <strong>5-25x more</strong> to acquire a new customer than to retain an existing one. Existing customers are also <strong>50% more likely</strong> to try new products and spend <strong>31% more</strong>.","#2c7a7b")}

{sb("During a QBR, your client mentions their team has grown from 50 to 150 people and they're struggling with onboarding new users on your platform.",["Note it down and follow up later","Immediately discuss your Enterprise tier which includes dedicated onboarding support and additional user licenses","Say 'That's great that you're growing!' and move to the next agenda item","Send them a pricing document after the meeting"],1,"<strong>Best approach: Discuss the Enterprise tier now.</strong> The client has expressed a pain point that aligns with a solution you offer. This is a natural, value-driven upsell — not pushy sales.")}

{kc("How much more does it cost to acquire a new customer compared to retaining an existing one?",["2x","5-25x","50x","100x"],1,"It costs <strong>5-25x more</strong> to acquire a new customer than retain an existing one.")}

<h3>💡 Key Takeaways</h3>
<ul><li>Be a <strong>trusted advisor</strong>, not just a vendor</li><li>Conduct <strong>QBRs quarterly</strong> with a structured agenda</li><li>Listen for <strong>pain points</strong> that align with solutions you offer</li><li>Retention is <strong>5-25x cheaper</strong> than acquisition</li></ul>
"""

C[("course-customer-201",4)] = f"""
<h2>Negotiation Skills</h2>
{stats([("🤝","Win-Win","Target Outcome"),("📋","BATNA","Key Concept"),("🎯","80%","Prep vs 20% Execution"),("💡","ZOPA","Zone of Possible Agreement")])}

<h3>🎯 Learning Objectives</h3>
<ul><li>Understand negotiation principles and psychology</li><li>Master the BATNA framework</li><li>Apply win-win negotiation strategies</li><li>Handle common negotiation tactics</li></ul>

<h3>Key Negotiation Concepts</h3>
<ul><li><strong>BATNA:</strong> Best Alternative To Negotiated Agreement — your backup plan</li><li><strong>ZOPA:</strong> Zone Of Possible Agreement — the range where both parties can agree</li><li><strong>Reservation Price:</strong> Your absolute walk-away point</li><li><strong>Anchoring:</strong> The first number sets the frame for the negotiation</li></ul>

<h3>The 5-Step Negotiation Process</h3>
<ol><li><strong>Prepare:</strong> Know your BATNA, research the other party, set objectives</li><li><strong>Open:</strong> Build rapport, set the agenda, establish ground rules</li><li><strong>Explore:</strong> Ask questions, listen actively, understand their needs</li><li><strong>Bargain:</strong> Make offers, trade concessions, create value</li><li><strong>Close:</strong> Summarize, confirm details, document the agreement</li></ol>

{cb("📊","The 80/20 Rule","<strong>80% of negotiation success comes from preparation.</strong> Know your numbers, your limits, and your alternatives before you sit down at the table.","#1a3a5c")}

{sb("A client wants a 30% discount on their annual renewal. Your approved discount limit is 15%. They say a competitor offered them a similar product at 25% less.",["Agree to 30% to keep the client","Offer your maximum 15% and hold firm","Explore what additional value you can provide instead of pure discount — perhaps additional users, premium support, or extended terms at 15% off","Tell them to go with the competitor"],2,"<strong>Best: Expand the pie.</strong> Instead of competing purely on price, find creative value additions. Often, the client's real need isn't the lowest price — it's the best value.")}

{kc("What does BATNA stand for?",["Best Agreement Through Negotiation Analysis","Best Alternative To Negotiated Agreement","Basic Approach To Negotiation Alignment","Business Alliance Through Negotiation Approach"],1,"BATNA = <strong>Best Alternative To Negotiated Agreement</strong> — your backup plan if the negotiation fails.")}

<h3>💡 Key Takeaways</h3>
<ul><li><strong>80% preparation, 20% execution</strong></li><li>Always know your <strong>BATNA</strong> before negotiating</li><li>Aim for <strong>win-win</strong> — expand the pie before splitting it</li><li>Listen more than you talk — <strong>ask questions</strong> to understand needs</li></ul>
"""

# ────────────────────────────────────────────────────────────
# COURSE: HR 101
# ────────────────────────────────────────────────────────────

C[("course-hr-101",0)] = f"""
<h2>Employee Benefits Overview</h2>
{stats([("🏥","3 Plans","Health Insurance"),("💰","6%","401(k) Match"),("📅","25+","PTO Days"),("🎓","$5,000","Tuition Reimbursement")])}

<h3>🎯 Learning Objectives</h3>
<ul><li>Understand all benefit categories available to you</li><li>Know enrollment periods and eligibility</li><li>Make informed decisions about benefit selections</li><li>Access benefits resources and support</li></ul>

<h3>Health Insurance Plans</h3>
<table style="width:100%;border-collapse:collapse;margin:16px 0"><tr style="background:var(--surface-hover,#f0f0f0)"><th style="padding:10px;border:1px solid var(--border,#ddd)">Plan</th><th style="padding:10px;border:1px solid var(--border,#ddd)">Monthly Premium</th><th style="padding:10px;border:1px solid var(--border,#ddd)">Deductible</th><th style="padding:10px;border:1px solid var(--border,#ddd)">Best For</th></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>HMO Basic</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">$150</td><td style="padding:10px;border:1px solid var(--border,#ddd)">$2,000</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Healthy individuals, low utilization</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>PPO Standard</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">$300</td><td style="padding:10px;border:1px solid var(--border,#ddd)">$1,000</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Moderate utilization, want flexibility</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>PPO Premium</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">$450</td><td style="padding:10px;border:1px solid var(--border,#ddd)">$500</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Families, frequent medical needs</td></tr></table>

<h3>Retirement Benefits</h3>
<p>The company matches your 401(k) contributions up to <strong>6% of your salary</strong>. That's free money!</p>
{cb("💰","Example","If you earn $60,000 and contribute 6% ($3,600/year), the company adds another $3,600. Over 30 years at 7% return, that match alone becomes <strong>~$340,000</strong>.","#22c55e")}

<h3>Additional Benefits</h3>
<ul><li><strong>Dental &amp; Vision:</strong> Company-paid basic coverage</li><li><strong>Life Insurance:</strong> 2x salary (company-paid), up to 5x (voluntary)</li><li><strong>EAP:</strong> 10 free counseling sessions per year</li><li><strong>Tuition Reimbursement:</strong> $5,000/year for approved programs</li><li><strong>Wellness Program:</strong> $500 annual gym reimbursement</li><li><strong>Commuter Benefits:</strong> Pre-tax transit/parking</li></ul>

{kc("What's the maximum 401(k) company match?",["3% of salary","4% of salary","6% of salary","10% of salary"],2,"The company matches up to <strong>6%</strong> of your salary. Contribute at least 6% to get the full match.")}

<h3>💡 Key Takeaways</h3>
<ul><li>Contribute at least <strong>6%</strong> to 401(k) to get the full match</li><li>Open enrollment is in <strong>November</strong> — changes take effect January 1</li><li>Use the <strong>EAP</strong> — 10 free sessions, completely confidential</li><li>Questions? Contact HR Benefits at benefits@company.com</li></ul>
"""

C[("course-hr-101",1)] = f"""
<h2>Time Off &amp; Leave Policies</h2>
{stats([("📅","15-25","PTO Days/Year"),("🏥","12 Weeks","FMLA Leave"),("👶","16 Weeks","Parental Leave"),("🎉","11","Company Holidays")])}

<h3>🎯 Learning Objectives</h3>
<ul><li>Understand PTO accrual, usage, and rollover policies</li><li>Know the different leave types and eligibility</li><li>Navigate FMLA and parental leave processes</li><li>Plan time off effectively</li></ul>

<h3>PTO Accrual Schedule</h3>
<table style="width:100%;border-collapse:collapse;margin:16px 0"><tr style="background:var(--surface-hover,#f0f0f0)"><th style="padding:10px;border:1px solid var(--border,#ddd)">Tenure</th><th style="padding:10px;border:1px solid var(--border,#ddd)">Annual PTO</th><th style="padding:10px;border:1px solid var(--border,#ddd)">Monthly Accrual</th></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)">0-2 years</td><td style="padding:10px;border:1px solid var(--border,#ddd)">15 days</td><td style="padding:10px;border:1px solid var(--border,#ddd)">1.25 days</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)">3-5 years</td><td style="padding:10px;border:1px solid var(--border,#ddd)">20 days</td><td style="padding:10px;border:1px solid var(--border,#ddd)">1.67 days</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)">6+ years</td><td style="padding:10px;border:1px solid var(--border,#ddd)">25 days</td><td style="padding:10px;border:1px solid var(--border,#ddd)">2.08 days</td></tr></table>

<h3>Leave Types</h3>
<ul><li><strong>PTO:</strong> Vacation, personal time, mental health days</li><li><strong>Sick Leave:</strong> Separate bank of 10 days/year</li><li><strong>FMLA:</strong> 12 weeks unpaid for qualifying medical/family events</li><li><strong>Parental Leave:</strong> 16 weeks paid (birth, adoption, foster placement)</li><li><strong>Bereavement:</strong> 5 days for immediate family, 3 for extended</li><li><strong>Jury Duty:</strong> Full pay during service</li></ul>

{sb("You've been with the company for 3 years. You want to take 3 weeks off for an international trip. You currently have 12 PTO days available.",["Request all 3 weeks as PTO — you'll go negative and earn it back","Request 12 days PTO and 3 days unpaid leave with manager approval","Take the trip and figure out the PTO later","Cancel the trip — you don't have enough days"],1,"<strong>Best approach: Combine PTO + unpaid leave.</strong> Use your 12 available days as PTO and request 3 additional unpaid days. Discuss with your manager in advance — most will accommodate with enough notice.")}

{kc("How many days of PTO does an employee with 4 years of tenure accrue per year?",["15 days","20 days","25 days","30 days"],1,"Employees with 3-5 years of tenure accrue <strong>20 days</strong> of PTO per year.")}

<h3>💡 Key Takeaways</h3>
<ul><li>PTO increases with tenure — <strong>15 → 20 → 25</strong> days</li><li>Up to <strong>5 days</strong> roll over to next year</li><li>Request time off <strong>2+ weeks</strong> in advance for best approval odds</li><li>Use your PTO — research shows it improves <strong>productivity and retention</strong></li></ul>
"""

C[("course-hr-101",2)] = f"""
<h2>Professional Development</h2>
{stats([("🎓","$5,000","Annual Tuition Reimbursement"),("📚","Unlimited","Learning Platform Access"),("🤝","Mentorship","Program Available"),("📈","IDP","Individual Development Plan")])}

<h3>🎯 Learning Objectives</h3>
<ul><li>Create an effective Individual Development Plan (IDP)</li><li>Leverage company learning resources and tuition reimbursement</li><li>Build a career growth roadmap</li><li>Find and engage with mentors</li></ul>

<h3>The IDP Framework</h3>
<ol><li><strong>Self-Assessment:</strong> Where are you now? Strengths, gaps, interests</li><li><strong>Goal Setting:</strong> Where do you want to be in 1 year? 3 years? 5 years?</li><li><strong>Action Plan:</strong> What specific steps will get you there?</li><li><strong>Resources:</strong> What learning, mentoring, or experience do you need?</li><li><strong>Review:</strong> Quarterly check-ins with your manager</li></ol>

<h3>Available Development Resources</h3>
<ul><li><strong>Learning Platform:</strong> 10,000+ courses on LinkedIn Learning, Coursera, and internal content</li><li><strong>Tuition Reimbursement:</strong> $5,000/year for approved degree or certification programs</li><li><strong>Conference Budget:</strong> 1 industry conference per year (up to $2,000)</li><li><strong>Mentorship Program:</strong> Matched with senior leaders — 6-month cycles</li><li><strong>Internal Mobility:</strong> Rotate into different departments for 3-6 month assignments</li><li><strong>Certification Support:</strong> Exam fees + study materials for relevant certifications</li></ul>

{cb("📈","Career Insight","Employees who have an IDP and meet with their manager quarterly about development are <strong>3.5x more likely</strong> to be promoted within 2 years.","#2c7a7b")}

{kc("What is the annual tuition reimbursement amount?",["$2,000","$3,500","$5,000","$10,000"],2,"The company provides <strong>$5,000 per year</strong> in tuition reimbursement for approved programs.")}

<h3>💡 Key Takeaways</h3>
<ul><li>Create your <strong>IDP</strong> — it's the roadmap to your career goals</li><li>Take advantage of <strong>$5,000 tuition reimbursement</strong></li><li>Review your development plan <strong>quarterly</strong> with your manager</li><li>Apply for the <strong>Mentorship Program</strong> — it's competitive but transformative</li></ul>
"""

C[("course-hr-101",3)] = f"""
<h2>Workplace Culture</h2>
{stats([("🏆","Great Place","to Work Certified"),("📊","87%","Employee Engagement"),("🌍","DEI","Core Value"),("💬","Weekly","Team Check-ins")])}

<h3>🎯 Learning Objectives</h3>
<ul><li>Understand our core values and how they shape daily work</li><li>Contribute positively to team culture and belonging</li><li>Navigate DEI (Diversity, Equity &amp; Inclusion) principles</li><li>Practice effective collaboration across teams</li></ul>

<h3>Our Core Values</h3>
<ol><li><strong>Integrity:</strong> We do the right thing, even when it's hard</li><li><strong>Innovation:</strong> We embrace change and creative problem-solving</li><li><strong>Inclusion:</strong> Everyone belongs, every voice matters</li><li><strong>Impact:</strong> We measure success by the difference we make</li><li><strong>Collaboration:</strong> We achieve more together than apart</li></ol>

<h3>Building Inclusive Teams</h3>
<ul><li><strong>Assume positive intent</strong> — give colleagues the benefit of the doubt</li><li><strong>Amplify others' ideas</strong> — "I'd like to build on what Sarah said..."</li><li><strong>Make space</strong> for quieter voices in meetings</li><li><strong>Challenge bias</strong> respectfully when you see it</li><li><strong>Celebrate differences</strong> — cultural events, heritage months, ERGs</li></ul>

{cb("📊","Research Shows","Teams with high psychological safety are <strong>76% more engaged</strong>, <strong>50% more productive</strong>, and <strong>57% more likely</strong> to collaborate across departments. —Google's Project Aristotle","#2c7a7b")}

{sb("In a team meeting, you notice a newer colleague keeps trying to share an idea but gets talked over by more senior team members. What do you do?",["Nothing — they'll learn to speak up with time","Wait for a pause and say 'I noticed Alex had something to share — Alex, would you like to continue?'","Talk to them privately after the meeting","Send a message to the team about meeting etiquette later"],1,"<strong>Best: Create space in the moment.</strong> Redirecting attention shows allyship and creates psychological safety. Follow up privately too, but the real impact happens in the moment.")}

{kc("According to Google's Project Aristotle, what is the #1 factor in high-performing teams?",["Individual talent","Psychological safety","Strong leadership","Clear goals"],1,"<strong>Psychological safety</strong> — the belief that you won't be punished for making mistakes or speaking up — is the #1 factor.")}

<h3>💡 Key Takeaways</h3>
<ul><li>Culture is built through <strong>daily actions</strong>, not mission statements</li><li><strong>Psychological safety</strong> is the foundation of high-performing teams</li><li><strong>Amplify others</strong> — inclusion is an active practice</li><li>Join an <strong>Employee Resource Group (ERG)</strong> to connect and contribute</li></ul>
"""

# ────────────────────────────────────────────────────────────
# COURSE: LEADERSHIP 201
# ────────────────────────────────────────────────────────────

C[("course-leadership-201",0)] = f"""
<h2>Team Management Essentials</h2>
{stats([("👥","Span","5-9 Direct Reports"),("📋","1:1s","Weekly"),("🎯","OKRs","Quarterly"),("📊","360°","Annual Feedback")])}

<h3>🎯 Learning Objectives</h3>
<ul><li>Understand core team management responsibilities</li><li>Run effective 1:1 meetings</li><li>Set and track OKRs (Objectives and Key Results)</li><li>Build high-performing teams</li></ul>

<h3>The Manager's Three Jobs</h3>
<ol><li><strong>Direction:</strong> Set clear goals and priorities</li><li><strong>Support:</strong> Remove obstacles and provide resources</li><li><strong>Development:</strong> Help each person grow professionally</li></ol>

<h3>The Effective 1:1 Meeting</h3>
<p>Weekly 30-minute meetings are the most important tool in your management toolkit:</p>
<ul><li><strong>10 min — Their agenda:</strong> What's on their mind? Challenges?</li><li><strong>10 min — Your agenda:</strong> Feedback, updates, priorities</li><li><strong>10 min — Development:</strong> Career goals, learning, growth</li></ul>
{cb("📊","Impact","Managers who hold weekly 1:1s have teams that are <strong>2.8x more engaged</strong> than those who don't. —Gallup","#2c7a7b")}

{sb("One of your direct reports consistently delivers great work but is quiet in team meetings and never volunteers for presentations. Their annual review is coming up.",["Mention it as an area for improvement in their review","Ask them privately if they'd like support with public speaking — offer coaching or a Toastmasters membership","Ignore it — their work quality speaks for itself","Require them to present at the next team meeting to build confidence"],1,"<strong>Best: Private conversation + support.</strong> Not everyone is comfortable with public speaking. Ask what THEY want, and offer support. Don't force it or penalize quiet contributions.")}

{kc("How much more engaged are teams when managers hold weekly 1:1s?",["1.5x","2.8x","4x","5.5x"],1,"Teams with weekly 1:1 meetings are <strong>2.8x more engaged</strong>.")}

<h3>💡 Key Takeaways</h3>
<ul><li>Direction + Support + Development = Great Management</li><li><strong>Weekly 1:1s</strong> are non-negotiable</li><li>Set <strong>OKRs quarterly</strong> — measurable, ambitious, aligned</li><li>Adapt your style to each person's needs</li></ul>
"""

C[("course-leadership-201",1)] = f"""
<h2>Communication &amp; Feedback</h2>
{stats([("📣","70%","of Errors from Bad Communication"),("📋","SBI","Feedback Model"),("⏱️","48h","Feedback Window"),("🔄","Continuous","Not Just Annual")])}

<h3>🎯 Learning Objectives</h3>
<ul><li>Master the SBI (Situation-Behavior-Impact) feedback model</li><li>Give both positive and constructive feedback effectively</li><li>Create a feedback-rich team culture</li><li>Handle difficult feedback conversations</li></ul>

<h3>The SBI Feedback Model</h3>
<ol><li><strong>Situation:</strong> "During yesterday's client presentation..."</li><li><strong>Behavior:</strong> "...you spoke over the client twice when they were asking questions..."</li><li><strong>Impact:</strong> "...which made the client feel unheard and they mentioned it to me afterward."</li></ol>
{cb("📧","SBI Example — Positive","<strong>S:</strong> 'In last week's sprint review...' <strong>B:</strong> '...you prepared a demo that clearly showed the new feature's value proposition...' <strong>I:</strong> '...which helped the stakeholders approve the feature for production ahead of schedule.'","#22c55e")}

<h3>The 48-Hour Rule</h3>
<p>Give feedback within <strong>48 hours</strong> of the event. After that, the details fade and the impact diminishes.</p>

<h3>Receiving Feedback Gracefully</h3>
<ol><li><strong>Listen</strong> without interrupting</li><li><strong>Thank</strong> the person for sharing</li><li><strong>Ask clarifying questions</strong> if needed</li><li><strong>Reflect</strong> before responding</li><li><strong>Follow up</strong> on actions you committed to</li></ol>

{sb("A team member's work quality has declined over the past month. You suspect personal issues may be involved.",["Give direct feedback about the quality decline and set a performance improvement plan","Have a private, caring conversation: 'I've noticed a change and I want to check in — how are you doing?' Then discuss performance separately","Ignore it and hope it improves","Ask their coworkers if they know what's going on"],1,"<strong>Best: Check in first, then address performance.</strong> Lead with empathy. There may be personal circumstances affecting them. Show care, then separately discuss the work impact and create a supportive plan.")}

{kc("What does SBI stand for?",["Structure-Build-Implement","Situation-Behavior-Impact","Summary-Background-Insight","Start-Bridge-Improve"],1,"SBI = <strong>Situation-Behavior-Impact</strong>. The most effective and objective feedback model.")}

<h3>💡 Key Takeaways</h3>
<ul><li>Use <strong>SBI</strong> for all feedback — it keeps it objective</li><li>Give feedback within <strong>48 hours</strong></li><li><strong>5:1 ratio</strong> — aim for 5 positive observations for every 1 constructive</li><li>Create a culture where feedback is <strong>expected and welcomed</strong></li></ul>
"""

C[("course-leadership-201",2)] = f"""
<h2>Conflict Resolution</h2>
{stats([("⚡","85%","of Employees Experience Conflict"),("⏱️","2.8h","Per Week on Conflict"),("💰","$359B","Annual Cost (US)"),("🤝","DESC","Resolution Framework")])}

<h3>🎯 Learning Objectives</h3>
<ul><li>Understand the sources and types of workplace conflict</li><li>Apply the DESC framework for resolution</li><li>Know when to mediate and when to escalate</li><li>Turn conflict into productive outcomes</li></ul>

<h3>The DESC Framework</h3>
<ol><li><strong>D — Describe:</strong> State the specific situation objectively</li><li><strong>E — Express:</strong> Share how it affects you/the team</li><li><strong>S — Specify:</strong> Request specific changes</li><li><strong>C — Consequences:</strong> Explain the positive outcomes of resolution</li></ol>

<h3>The 5 Conflict Styles</h3>
<table style="width:100%;border-collapse:collapse;margin:16px 0"><tr style="background:var(--surface-hover,#f0f0f0)"><th style="padding:10px;border:1px solid var(--border,#ddd)">Style</th><th style="padding:10px;border:1px solid var(--border,#ddd)">When to Use</th></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Collaborating</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Both parties' concerns are important; time allows</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Compromising</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Moderate importance; need quick resolution</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Accommodating</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Issue matters more to the other person</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Competing</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Emergency decisions; non-negotiable values</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Avoiding</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Trivial issue; emotions need cooling</td></tr></table>

{sb("Two senior team members are in a heated disagreement about the project approach. One wants Agile, the other Waterfall. The tension is affecting the whole team.",["Let them work it out themselves","Use DESC: bring them together, have each describe their position, facilitate a discussion focused on project goals (not personal preferences), and guide them toward a hybrid approach","Pick one approach and make them follow it","Escalate to your VP immediately"],1,"<strong>Best: Facilitate with DESC.</strong> Bring both to a private meeting. Have each describe their reasoning. Focus on shared project goals. A hybrid approach often emerges that incorporates the best of both.")}

{kc("On average, how many hours per week do employees spend dealing with conflict?",["0.5 hours","1.5 hours","2.8 hours","4.5 hours"],2,"Employees spend an average of <strong>2.8 hours per week</strong> dealing with workplace conflict.")}

<h3>💡 Key Takeaways</h3>
<ul><li>Conflict is <strong>normal and can be productive</strong> if managed well</li><li>Use <strong>DESC</strong> for structured resolution</li><li>Choose the right <strong>conflict style</strong> for the situation</li><li>Address conflict <strong>early</strong> — it rarely resolves on its own</li></ul>
"""

C[("course-leadership-201",3)] = f"""
<h2>Strategic Thinking</h2>
{stats([("🎯","SWOT","Analysis Framework"),("📊","5 Forces","Competitive Analysis"),("🗺️","Strategy","Canvas"),("📈","OKRs","Execution Framework")])}

<h3>🎯 Learning Objectives</h3>
<ul><li>Apply strategic analysis frameworks (SWOT, Porter's 5 Forces)</li><li>Translate strategy into actionable plans</li><li>Think long-term while managing short-term priorities</li><li>Communicate strategy effectively to your team</li></ul>

<h3>SWOT Analysis</h3>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:20px 0">
<div style="background:#22c55e15;padding:16px;border-radius:8px"><strong>💪 Strengths</strong><p style="font-size:.85rem;margin:4px 0 0">Internal advantages. What do we do well? What resources do we have?</p></div>
<div style="background:#ef444415;padding:16px;border-radius:8px"><strong>⚠️ Weaknesses</strong><p style="font-size:.85rem;margin:4px 0 0">Internal limitations. What could we improve? Where do we lack resources?</p></div>
<div style="background:#3b82f615;padding:16px;border-radius:8px"><strong>🚀 Opportunities</strong><p style="font-size:.85rem;margin:4px 0 0">External possibilities. Market trends? Unmet needs? New technologies?</p></div>
<div style="background:#f59e0b15;padding:16px;border-radius:8px"><strong>🔥 Threats</strong><p style="font-size:.85rem;margin:4px 0 0">External risks. Competition? Regulation? Economic shifts?</p></div>
</div>

<h3>From Strategy to Execution</h3>
<ol><li><strong>Vision:</strong> Where do we want to be? (3-5 year horizon)</li><li><strong>Strategy:</strong> How will we get there? (annual plan)</li><li><strong>Objectives:</strong> What specific goals? (quarterly OKRs)</li><li><strong>Initiatives:</strong> What projects/actions? (monthly sprints)</li><li><strong>Metrics:</strong> How do we measure progress? (weekly tracking)</li></ol>

{cb("🎯","Strategy vs Tactics","<strong>Strategy</strong> is deciding WHAT to do and WHY. <strong>Tactics</strong> are HOW to do it. Leaders must spend time on strategy before diving into tactics. A perfectly executed wrong strategy still fails.","#1a3a5c")}

{kc("In a SWOT analysis, which quadrant represents external factors you can leverage?",["Strengths","Weaknesses","Opportunities","Threats"],2,"<strong>Opportunities</strong> are external factors that you can leverage for advantage.")}

<h3>💡 Key Takeaways</h3>
<ul><li>Use <strong>SWOT</strong> regularly — at least quarterly</li><li>Strategy is about <strong>choices</strong> — what you say NO to matters as much as what you say yes to</li><li>Translate strategy to execution: <strong>Vision → Strategy → OKRs → Initiatives → Metrics</strong></li><li>Communicate the WHY, not just the WHAT</li></ul>
"""

C[("course-leadership-201",4)] = f"""
<h2>Change Management</h2>
{stats([("📊","70%","Change Initiatives Fail"),("🧠","ADKAR","Model"),("⏱️","3-6mo","Typical Transition"),("🤝","Champions","Key to Success")])}

<h3>🎯 Learning Objectives</h3>
<ul><li>Understand why change initiatives fail and how to prevent it</li><li>Apply the ADKAR model for individual change</li><li>Lead teams through uncertainty and resistance</li><li>Measure and sustain change success</li></ul>

<h3>The ADKAR Model</h3>
<ol><li><strong>A — Awareness:</strong> WHY is the change needed?</li><li><strong>D — Desire:</strong> Build WANT to participate and support</li><li><strong>K — Knowledge:</strong> HOW to change (training, information)</li><li><strong>A — Ability:</strong> CAN they actually do it? (skills, tools)</li><li><strong>R — Reinforcement:</strong> SUSTAIN the change (rewards, accountability)</li></ol>

<h3>The Change Curve (Kübler-Ross Adaptation)</h3>
<p>People move through emotional stages during change:</p>
<ol><li><strong>Shock/Denial:</strong> "This won't really happen"</li><li><strong>Frustration/Anger:</strong> "Why are they doing this?"</li><li><strong>Depression/Confusion:</strong> "I don't know if I can do this"</li><li><strong>Experiment:</strong> "Let me try the new way"</li><li><strong>Integration:</strong> "This is actually better"</li></ol>
{cb("📊","Key Statistic","<strong>70% of change initiatives fail</strong>, primarily due to employee resistance and inadequate management support. The #1 predictor of success? Active, visible leadership sponsorship.","#ef4444")}

{sb("Your company is migrating to a new project management tool. Half your team is enthusiastic, but the other half is resistant, saying 'the old tool worked fine.'",["Force everyone to switch immediately — rip off the bandaid","Use ADKAR: explain WHY (awareness), show benefits relevant to THEM (desire), provide training (knowledge), offer hands-on practice (ability), and celebrate early wins (reinforcement)","Let the resistant half keep using the old tool","Send an email explaining the change and hope they adapt"],1,"<strong>Best: Apply ADKAR systematically.</strong> Resistance usually comes from lack of awareness or desire. Address each stage for each person. Champions from the enthusiastic half can help peers through the transition.")}

{kc("What is the #1 predictor of change initiative success?",["Budget allocation","Timeline","Active, visible leadership sponsorship","Technology quality"],2,"The #1 predictor is <strong>active, visible leadership sponsorship</strong>. When leaders visibly support and model the change, teams follow.")}

<h3>💡 Key Takeaways</h3>
<ul><li><strong>70% of changes fail</strong> — be intentional, not hopeful</li><li>Use <strong>ADKAR</strong> for every individual: Awareness → Desire → Knowledge → Ability → Reinforcement</li><li>People go through <strong>emotional stages</strong> — meet them where they are</li><li><strong>Leadership sponsorship</strong> is the #1 success factor</li></ul>
"""

C[("course-leadership-201",5)] = f"""
<h2>Mentoring &amp; Coaching</h2>
{stats([("🤝","Mentoring","Long-term Development"),("🎯","Coaching","Performance-focused"),("📈","5x","More Likely to Be Promoted"),("💬","GROW","Coaching Model")])}

<h3>🎯 Learning Objectives</h3>
<ul><li>Understand the difference between mentoring and coaching</li><li>Apply the GROW coaching model</li><li>Be an effective mentor and mentee</li><li>Build a culture of continuous development</li></ul>

<h3>Mentoring vs Coaching</h3>
<table style="width:100%;border-collapse:collapse;margin:16px 0"><tr style="background:var(--surface-hover,#f0f0f0)"><th style="padding:10px;border:1px solid var(--border,#ddd)">Aspect</th><th style="padding:10px;border:1px solid var(--border,#ddd)">Mentoring</th><th style="padding:10px;border:1px solid var(--border,#ddd)">Coaching</th></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)">Focus</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Career/life development</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Specific skill/performance</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)">Duration</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Months to years</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Weeks to months</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)">Approach</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Sharing experience, advising</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Asking questions, guiding discovery</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)">Relationship</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Usually outside reporting line</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Often manager or specialist</td></tr></table>

<h3>The GROW Coaching Model</h3>
<ol><li><strong>G — Goal:</strong> "What do you want to achieve?"</li><li><strong>R — Reality:</strong> "Where are you now? What's happening?"</li><li><strong>O — Options:</strong> "What could you do? What else?"</li><li><strong>W — Will:</strong> "What WILL you do? By when?"</li></ol>

{cb("📈","Impact","Employees with mentors are <strong>5x more likely</strong> to be promoted and report <strong>higher job satisfaction</strong>. Mentors also benefit — 97% say mentoring makes them better leaders.","#22c55e")}

{sb("A junior team member asks you: 'I want to become a team lead someday. What should I do?'",["Tell them exactly what steps to take based on your experience","Use the GROW model: ask about their specific goal (G), explore their current skills (R), brainstorm options together (O), and commit to next steps (W)","Say 'Just keep doing good work and it'll happen'","Send them to the mentorship program and leave it at that"],1,"<strong>Best: Use GROW.</strong> Coaching helps them discover their own path. Ask questions: 'What does being a team lead mean to you?' (G), 'What leadership experience do you have?' (R), 'What skills could you develop?' (O), 'What's one thing you'll start this week?' (W)")}

{kc("In the GROW model, what does the 'W' stand for?",["Work","Way forward","Will","Wisdom"],2,"W = <strong>Will</strong> — what will the person commit to doing, and by when?")}

<h3>💡 Key Takeaways</h3>
<ul><li><strong>Mentoring</strong> = long-term development; <strong>Coaching</strong> = specific performance</li><li>Use <strong>GROW</strong> for coaching conversations</li><li>Employees with mentors are <strong>5x more likely to be promoted</strong></li><li>Ask questions more than you give answers — help them discover their path</li></ul>
"""

# ────────────────────────────────────────────────────────────
# COURSE: TECHNICAL 101
# ────────────────────────────────────────────────────────────

C[("course-technical-101",0)] = f"""
<h2>Tools &amp; Systems Overview</h2>
{stats([("🔧","12+","Core Tools"),("☁️","Cloud","First"),("🔐","SSO","Single Sign-On"),("📊","Dashboard","Central Hub")])}

<h3>🎯 Learning Objectives</h3>
<ul><li>Navigate the company's core technology stack</li><li>Understand how systems integrate and share data</li><li>Use SSO and access management effectively</li><li>Know who to contact for each system</li></ul>

<h3>Core Technology Stack</h3>
<table style="width:100%;border-collapse:collapse;margin:16px 0"><tr style="background:var(--surface-hover,#f0f0f0)"><th style="padding:10px;border:1px solid var(--border,#ddd)">Category</th><th style="padding:10px;border:1px solid var(--border,#ddd)">Tool</th><th style="padding:10px;border:1px solid var(--border,#ddd)">Purpose</th><th style="padding:10px;border:1px solid var(--border,#ddd)">Access</th></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)">Communication</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Microsoft Teams</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Chat, video, calls</td><td style="padding:10px;border:1px solid var(--border,#ddd)">All employees</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)">Email</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Outlook</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Email, calendar</td><td style="padding:10px;border:1px solid var(--border,#ddd)">All employees</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)">Projects</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Jira / Asana</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Task management</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Team-based</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)">Documents</td><td style="padding:10px;border:1px solid var(--border,#ddd)">SharePoint/Confluence</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Documentation</td><td style="padding:10px;border:1px solid var(--border,#ddd)">All employees</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)">CRM</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Salesforce</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Client management</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Sales/CS roles</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)">HR</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Workday</td><td style="padding:10px;border:1px solid var(--border,#ddd)">HR self-service</td><td style="padding:10px;border:1px solid var(--border,#ddd)">All employees</td></tr></table>

<h3>Single Sign-On (SSO)</h3>
<p>All company tools use SSO — one login for everything. Your SSO credentials are your company email and password. Enable <strong>MFA</strong> for added security (required for all employees).</p>

{sb("You need access to a CRM system for a new project, but when you try to log in, you get 'Access Denied.'",["Ask a colleague to share their login","Submit an access request through the IT Service Portal, specifying the system, your role, and business justification","Email the CRM admin directly","Try different password combinations"],1,"<strong>Correct: Use the IT Service Portal.</strong> Access requests need proper authorization and documentation. The portal routes your request to the right approver and creates an audit trail.")}

{kc("What is the correct process for requesting access to a new tool?",["Ask a colleague for credentials","Submit request through IT Service Portal","Email IT directly","Ask your manager to request for you"],0,"Always use the <strong>IT Service Portal</strong> — it ensures proper authorization, documentation, and audit trail.")}

<h3>💡 Key Takeaways</h3>
<ul><li>Use <strong>SSO + MFA</strong> for all company systems</li><li>Request access through the <strong>IT Service Portal</strong></li><li><strong>Never share credentials</strong> — each person needs their own access</li><li>Bookmark the <strong>IT Support Knowledge Base</strong> for self-service help</li></ul>
"""

C[("course-technical-101",1)] = f"""
<h2>Process Documentation</h2>
{stats([("📝","SOP","Standard Operating Procedure"),("📊","60%","of Knowledge is Undocumented"),("🔄","Quarterly","Review Cycle"),("👥","Bus Factor","Minimum 2")])}

<h3>🎯 Learning Objectives</h3>
<ul><li>Create clear, maintainable process documentation</li><li>Understand the SOP format and when to use it</li><li>Address the "bus factor" problem through documentation</li><li>Keep documentation current and useful</li></ul>

<h3>Why Document Processes?</h3>
<ul><li><strong>Knowledge preservation:</strong> 60% of critical knowledge lives only in people's heads</li><li><strong>Consistency:</strong> Everyone follows the same steps</li><li><strong>Onboarding:</strong> New team members can self-serve</li><li><strong>Bus factor:</strong> If someone leaves, the knowledge stays</li></ul>

<h3>The SOP Template</h3>
<ol><li><strong>Title &amp; Purpose:</strong> What process, why it matters</li><li><strong>Scope:</strong> Who does this, when, how often</li><li><strong>Prerequisites:</strong> What's needed before starting</li><li><strong>Steps:</strong> Numbered, clear, screenshot-supported</li><li><strong>Expected Outcomes:</strong> What success looks like</li><li><strong>Troubleshooting:</strong> Common issues and fixes</li><li><strong>Owner &amp; Review Date:</strong> Who maintains it, when it's next reviewed</li></ol>

{cb("📊","The Bus Factor","The 'bus factor' is the minimum number of people who need to be unavailable before a process fails. If it's 1, you have a critical risk. Every key process should have a bus factor of <strong>at least 2</strong>.","#ef4444")}

{kc("What is the recommended review cycle for process documentation?",["Monthly","Quarterly","Annually","Only when something breaks"],1,"Process documentation should be reviewed <strong>quarterly</strong> to ensure accuracy and relevance.")}

<h3>💡 Key Takeaways</h3>
<ul><li>If it's important, <strong>document it</strong></li><li>Use the <strong>SOP template</strong> for consistency</li><li>Review documentation <strong>quarterly</strong></li><li>Every critical process needs a <strong>bus factor ≥ 2</strong></li></ul>
"""

C[("course-technical-101",2)] = f"""
<h2>Quality Standards</h2>
{stats([("⭐","ISO 9001","Quality Framework"),("📊","Six Sigma","Methodology"),("🎯","99.99%","Defect-Free Target"),("🔄","PDCA","Improvement Cycle")])}

<h3>🎯 Learning Objectives</h3>
<ul><li>Understand quality management principles</li><li>Apply the PDCA cycle for continuous improvement</li><li>Know our quality standards and how to measure them</li><li>Identify and report quality issues</li></ul>

<h3>The PDCA Cycle</h3>
<ol><li><strong>Plan:</strong> Identify the issue, analyze root cause, design a solution</li><li><strong>Do:</strong> Implement the solution on a small scale (pilot)</li><li><strong>Check:</strong> Measure results — did it work?</li><li><strong>Act:</strong> If yes, standardize and scale. If no, revise and repeat.</li></ol>

<h3>Quality Metrics We Track</h3>
<table style="width:100%;border-collapse:collapse;margin:16px 0"><tr style="background:var(--surface-hover,#f0f0f0)"><th style="padding:10px;border:1px solid var(--border,#ddd)">Metric</th><th style="padding:10px;border:1px solid var(--border,#ddd)">Target</th><th style="padding:10px;border:1px solid var(--border,#ddd)">How Measured</th></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)">Defect Rate</td><td style="padding:10px;border:1px solid var(--border,#ddd)">&lt;0.01%</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Defects per 1000 deliverables</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)">First Pass Yield</td><td style="padding:10px;border:1px solid var(--border,#ddd)">&gt;95%</td><td style="padding:10px;border:1px solid var(--border,#ddd)">% completed correctly first time</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)">Customer Satisfaction</td><td style="padding:10px;border:1px solid var(--border,#ddd)">&gt;4.5/5</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Post-delivery survey</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)">On-Time Delivery</td><td style="padding:10px;border:1px solid var(--border,#ddd)">&gt;98%</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Delivery vs committed date</td></tr></table>

{cb("🎯","The Cost of Quality","Fixing a defect after delivery costs <strong>10-100x more</strong> than finding it during development. That's why quality is built in from the start, not inspected at the end.","#ef4444")}

{kc("In the PDCA cycle, what should you do if the 'Check' phase shows your solution didn't work?",["Abandon the project","Go back to Plan and revise your approach","Implement it anyway at full scale","Blame the team"],1,"If Check shows failure, go back to <strong>Plan</strong>. PDCA is a cycle — iterate until you find what works.")}

<h3>💡 Key Takeaways</h3>
<ul><li>Quality is <strong>everyone's job</strong>, not just QA's</li><li>Use <strong>PDCA</strong> for continuous improvement</li><li>Catching defects early saves <strong>10-100x</strong></li><li>Report quality issues immediately — early detection is key</li></ul>
"""

C[("course-technical-101",3)] = f"""
<h2>Project Management Basics</h2>
{stats([("📋","Agile","Primary Methodology"),("📊","Kanban","Visual Management"),("⏱️","2 Weeks","Sprint Length"),("🎯","SMART","Goals Framework")])}

<h3>🎯 Learning Objectives</h3>
<ul><li>Understand Agile vs Waterfall methodologies</li><li>Run effective sprint ceremonies</li><li>Set SMART goals for projects</li><li>Use Kanban boards for visual task management</li></ul>

<h3>Agile vs Waterfall</h3>
<table style="width:100%;border-collapse:collapse;margin:16px 0"><tr style="background:var(--surface-hover,#f0f0f0)"><th style="padding:10px;border:1px solid var(--border,#ddd)">Aspect</th><th style="padding:10px;border:1px solid var(--border,#ddd)">Agile</th><th style="padding:10px;border:1px solid var(--border,#ddd)">Waterfall</th></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)">Approach</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Iterative, flexible</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Sequential, planned</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)">Delivery</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Incremental (every sprint)</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Big bang (end of project)</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)">Changes</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Welcome at any point</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Costly and difficult</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)">Best For</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Complex, evolving requirements</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Well-defined, stable requirements</td></tr></table>

<h3>SMART Goals</h3>
<ul><li><strong>S — Specific:</strong> Clear, unambiguous</li><li><strong>M — Measurable:</strong> Quantifiable success criteria</li><li><strong>A — Achievable:</strong> Realistic given resources</li><li><strong>R — Relevant:</strong> Aligned with business objectives</li><li><strong>T — Time-bound:</strong> Has a deadline</li></ul>

{cb("📧","SMART Example","❌ 'Improve customer satisfaction'<br>✅ 'Increase NPS score from 42 to 55 by Q3 2026 through implementation of automated follow-up surveys and a dedicated customer success team.'","#22c55e")}

<h3>Sprint Ceremonies</h3>
<ol><li><strong>Sprint Planning:</strong> What will we accomplish this sprint? (2 hours)</li><li><strong>Daily Standup:</strong> What did I do? What will I do? Any blockers? (15 min)</li><li><strong>Sprint Review:</strong> Demo the work to stakeholders (1 hour)</li><li><strong>Sprint Retrospective:</strong> What went well? What to improve? (1 hour)</li></ol>

{kc("What does the 'T' in SMART goals stand for?",["Trackable","Team-based","Time-bound","Transparent"],2,"T = <strong>Time-bound</strong>. Every goal needs a deadline.")}

<h3>💡 Key Takeaways</h3>
<ul><li>Use <strong>Agile</strong> for complex, evolving projects</li><li>Set <strong>SMART goals</strong> for every project and sprint</li><li>All 4 <strong>sprint ceremonies</strong> matter — don't skip the retro!</li><li>Visualize work on a <strong>Kanban board</strong></li></ul>
"""

C[("course-technical-101",4)] = f"""
<h2>Troubleshooting &amp; Support</h2>
{stats([("🔧","5 Whys","Root Cause Method"),("📋","Tier 1-3","Support Levels"),("⏱️","MTTR","Mean Time to Resolve"),("📊","Knowledge","Base First")])}

<h3>🎯 Learning Objectives</h3>
<ul><li>Apply systematic troubleshooting methodologies</li><li>Use the 5 Whys technique for root cause analysis</li><li>Understand the tiered support model</li><li>Document solutions for future reference</li></ul>

<h3>The Troubleshooting Framework</h3>
<ol><li><strong>Identify:</strong> What exactly is the problem? When did it start?</li><li><strong>Reproduce:</strong> Can you make it happen again consistently?</li><li><strong>Isolate:</strong> What changed? What's different from when it worked?</li><li><strong>Fix:</strong> Apply the solution</li><li><strong>Verify:</strong> Confirm the fix works and doesn't break anything else</li><li><strong>Document:</strong> Record the problem, root cause, and solution</li></ol>

<h3>The 5 Whys Technique</h3>
<p>Keep asking "Why?" until you reach the root cause:</p>
<ol><li><strong>Why</strong> did the server go down? → Because it ran out of memory</li><li><strong>Why</strong> did it run out of memory? → Because the log files grew too large</li><li><strong>Why</strong> did the logs grow too large? → Because log rotation wasn't configured</li><li><strong>Why</strong> wasn't log rotation configured? → Because it wasn't in the setup checklist</li><li><strong>Why</strong> wasn't it in the checklist? → Because the checklist was last updated 2 years ago</li></ol>
<p><strong>Root cause:</strong> Outdated setup checklist. <strong>Fix:</strong> Update checklist + quarterly reviews.</p>

<h3>Tiered Support Model</h3>
<table style="width:100%;border-collapse:collapse;margin:16px 0"><tr style="background:var(--surface-hover,#f0f0f0)"><th style="padding:10px;border:1px solid var(--border,#ddd)">Tier</th><th style="padding:10px;border:1px solid var(--border,#ddd)">Handles</th><th style="padding:10px;border:1px solid var(--border,#ddd)">Response Time</th></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Tier 1 (Help Desk)</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Basic issues, password resets, FAQs</td><td style="padding:10px;border:1px solid var(--border,#ddd)">1 hour</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Tier 2 (Technical)</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Complex issues, configuration, integration</td><td style="padding:10px;border:1px solid var(--border,#ddd)">4 hours</td></tr>
<tr><td style="padding:10px;border:1px solid var(--border,#ddd)"><strong>Tier 3 (Engineering)</strong></td><td style="padding:10px;border:1px solid var(--border,#ddd)">Code bugs, infrastructure, architecture</td><td style="padding:10px;border:1px solid var(--border,#ddd)">Same day</td></tr></table>

{sb("A user reports: 'The application is slow.' No other details.",["Tell them to restart their computer","Ask structured questions: When did it start? Which specific actions are slow? Is it just them or others too? What changed recently?","Escalate to Tier 3 immediately","Tell them it's probably their internet connection"],1,"<strong>Best: Ask structured questions.</strong> 'Slow' is a symptom, not a diagnosis. Gather specific details: when, what, who, what changed. Most issues can be resolved with good questioning before any technical investigation.")}

{kc("In the 5 Whys technique, what is the typical result?",["A list of 5 different problems","A root cause that's often systemic, not surface-level","Five different solutions to try","A blame assignment"],1,"The 5 Whys typically reveals a <strong>systemic root cause</strong> (process, documentation, training) rather than the surface-level symptom.")}

<h3>💡 Key Takeaways</h3>
<ul><li>Follow the <strong>6-step troubleshooting framework</strong></li><li>Use <strong>5 Whys</strong> to find the real root cause</li><li><strong>Document every solution</strong> — your fix helps the next person</li><li>Check the <strong>Knowledge Base first</strong> — it might already be solved</li></ul>
"""


# ═══════════════════════════════════════════════════════════════
# WRITE TO DATABASE
# ═══════════════════════════════════════════════════════════════

def main():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    updated = 0

    for (cid, oi), html in C.items():
        cur = conn.execute(
            "SELECT id FROM modules WHERE course_id = ? AND order_index = ?",
            (cid, oi),
        )
        row = cur.fetchone()
        if row:
            conn.execute("UPDATE modules SET content = ? WHERE id = ?",
                         (html.strip(), row["id"]))
            updated += 1
            print(f"  ✅ {cid} / module {oi}")
        else:
            print(f"  ⚠️  Not found: {cid} / module {oi}")

    conn.commit()
    conn.close()
    print(f"\n🎉 Done — expanded {updated} modules with deep content.")


if __name__ == "__main__":
    main()
