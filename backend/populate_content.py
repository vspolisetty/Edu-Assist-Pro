"""
Populate modules with rich, realistic learning content for demo.
Run once:  python3 backend/populate_content.py
"""

import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), "courses.db")

# ── Rich HTML content per module keyed by (course_id, order_index) ──────────

CONTENT = {

# ═══════════════════════════════════════════════════════════════════════════
# COMPLIANCE FUNDAMENTALS
# ═══════════════════════════════════════════════════════════════════════════
("course-compliance-101", 0): """
<h2>Company Policies Overview</h2>

<h3>🎯 Learning Objectives</h3>
<ul>
  <li>Understand the purpose and scope of company policies</li>
  <li>Identify your responsibilities as an employee</li>
  <li>Know where to find and reference policy documents</li>
</ul>

<h3>Introduction</h3>
<p>Company policies are the foundation of a well-organized, fair, and legally compliant workplace. They provide clear guidelines that help every employee understand what is expected and how to conduct business ethically and professionally.</p>

<h3>Code of Conduct</h3>
<p>Our Code of Conduct outlines the principles and standards that guide our behavior. Every employee, regardless of role or seniority, is expected to:</p>
<ul>
  <li><strong>Act with Integrity:</strong> Be honest and transparent in all business dealings.</li>
  <li><strong>Treat Others with Respect:</strong> Foster a collaborative, inclusive workplace free from discrimination.</li>
  <li><strong>Protect Company Assets:</strong> Use organizational resources responsibly and safeguard confidential information.</li>
  <li><strong>Follow the Law:</strong> Comply with all applicable local, state, federal, and international laws.</li>
</ul>

<h3>Employee Responsibilities</h3>
<p>As an employee, you are responsible for:</p>
<ol>
  <li><strong>Reading and understanding</strong> all relevant policies during onboarding and when updates are published.</li>
  <li><strong>Reporting violations</strong> through the proper channels (direct manager, HR, or the anonymous ethics hotline).</li>
  <li><strong>Attending required training</strong> sessions to stay current on compliance requirements.</li>
  <li><strong>Seeking clarification</strong> whenever you are unsure about a policy or procedure.</li>
</ol>

<h3>Key Policies to Know</h3>
<table style="width:100%;border-collapse:collapse;margin:12px 0">
  <tr style="background:#f0f0f0"><th style="padding:8px;text-align:left;border:1px solid #ddd">Policy</th><th style="padding:8px;text-align:left;border:1px solid #ddd">Summary</th></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">Acceptable Use Policy</td><td style="padding:8px;border:1px solid #ddd">Rules for using company technology, email, and internet.</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">Confidentiality Agreement</td><td style="padding:8px;border:1px solid #ddd">Protects trade secrets and proprietary data from unauthorized disclosure.</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">Attendance & Punctuality</td><td style="padding:8px;border:1px solid #ddd">Expectations for work hours, time tracking, and absences.</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">Conflict of Interest</td><td style="padding:8px;border:1px solid #ddd">Guidelines for disclosing and managing personal interests that may conflict with company interests.</td></tr>
</table>

<h3>💡 Key Takeaway</h3>
<p>Company policies are not just rules — they protect <strong>you</strong>, your colleagues, and the organization. When in doubt, consult the employee handbook or reach out to HR.</p>
""",

("course-compliance-101", 1): """
<h2>Data Privacy & GDPR</h2>

<h3>🎯 Learning Objectives</h3>
<ul>
  <li>Understand the principles of data privacy and why it matters</li>
  <li>Learn the key provisions of GDPR and how they apply to your role</li>
  <li>Know how to handle personal data responsibly</li>
</ul>

<h3>What Is Data Privacy?</h3>
<p>Data privacy refers to the right of individuals to control how their personal information is collected, used, stored, and shared. Organizations must handle data responsibly to maintain trust and comply with regulations.</p>

<h3>GDPR at a Glance</h3>
<p>The <strong>General Data Protection Regulation (GDPR)</strong> is a comprehensive data protection law that applies to any organization processing data of EU residents. Key principles include:</p>
<ul>
  <li><strong>Lawfulness, Fairness & Transparency:</strong> Personal data must be processed lawfully and transparently.</li>
  <li><strong>Purpose Limitation:</strong> Data should only be collected for specified, explicit, and legitimate purposes.</li>
  <li><strong>Data Minimization:</strong> Only collect data that is necessary for the stated purpose.</li>
  <li><strong>Accuracy:</strong> Keep personal data accurate and up to date.</li>
  <li><strong>Storage Limitation:</strong> Do not store data longer than necessary.</li>
  <li><strong>Integrity & Confidentiality:</strong> Protect data against unauthorized access, loss, or damage.</li>
</ul>

<h3>Individual Rights Under GDPR</h3>
<ol>
  <li><strong>Right to Access:</strong> Individuals can request a copy of their data.</li>
  <li><strong>Right to Rectification:</strong> Incorrect data must be corrected upon request.</li>
  <li><strong>Right to Erasure ("Right to be Forgotten"):</strong> Data can be deleted when no longer needed.</li>
  <li><strong>Right to Data Portability:</strong> Individuals can transfer their data between providers.</li>
  <li><strong>Right to Object:</strong> Individuals can object to certain types of processing.</li>
</ol>

<h3>Your Day-to-Day Responsibilities</h3>
<ul>
  <li>Always verify you have a lawful basis before collecting personal data.</li>
  <li>Use encryption and secure channels when transmitting sensitive information.</li>
  <li>Report any data breach to the Data Protection Officer within <strong>24 hours</strong>.</li>
  <li>Never share personal data with unauthorized third parties.</li>
  <li>Use the "Privacy by Design" approach when building new systems or processes.</li>
</ul>

<h3>⚠️ Consequences of Non-Compliance</h3>
<p>GDPR violations can result in fines of up to <strong>€20 million or 4% of global annual turnover</strong>, whichever is higher. Beyond financial penalties, breaches damage customer trust and organizational reputation.</p>

<h3>💡 Key Takeaway</h3>
<p>Data privacy is everyone's responsibility. Treat every piece of personal information as if it were your own.</p>
""",

("course-compliance-101", 2): """
<h2>Workplace Safety</h2>

<h3>🎯 Learning Objectives</h3>
<ul>
  <li>Identify common workplace hazards</li>
  <li>Know the emergency procedures and evacuation routes</li>
  <li>Understand reporting protocols for safety incidents</li>
</ul>

<h3>Why Workplace Safety Matters</h3>
<p>A safe workplace protects employees from injury, reduces absenteeism, and improves productivity. Under OSHA (Occupational Safety and Health Administration) regulations, every employer is required to provide a safe working environment.</p>

<h3>Common Workplace Hazards</h3>
<table style="width:100%;border-collapse:collapse;margin:12px 0">
  <tr style="background:#f0f0f0"><th style="padding:8px;text-align:left;border:1px solid #ddd">Hazard Type</th><th style="padding:8px;text-align:left;border:1px solid #ddd">Examples</th><th style="padding:8px;text-align:left;border:1px solid #ddd">Prevention</th></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">Ergonomic</td><td style="padding:8px;border:1px solid #ddd">Poor posture, repetitive strain</td><td style="padding:8px;border:1px solid #ddd">Adjustable desks, regular breaks</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">Slips & Falls</td><td style="padding:8px;border:1px solid #ddd">Wet floors, loose cables</td><td style="padding:8px;border:1px solid #ddd">Signage, cable management</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">Electrical</td><td style="padding:8px;border:1px solid #ddd">Faulty wiring, overloaded outlets</td><td style="padding:8px;border:1px solid #ddd">Regular inspections, surge protectors</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">Fire</td><td style="padding:8px;border:1px solid #ddd">Blocked exits, flammable materials</td><td style="padding:8px;border:1px solid #ddd">Fire drills, extinguisher access</td></tr>
</table>

<h3>Emergency Procedures</h3>
<ol>
  <li><strong>Stay Calm:</strong> Panic leads to poor decisions. Take a deep breath.</li>
  <li><strong>Alert Others:</strong> Activate the nearest fire alarm or call emergency services (dial the local emergency number).</li>
  <li><strong>Evacuate:</strong> Use the nearest exit. <strong>Never use elevators during a fire.</strong> Proceed to the designated assembly point.</li>
  <li><strong>Account for Everyone:</strong> Floor wardens will conduct headcounts at the assembly point.</li>
  <li><strong>Do Not Re-Enter:</strong> Wait for the "all clear" from emergency personnel.</li>
</ol>

<h3>Reporting Safety Incidents</h3>
<p>All incidents — even "near misses" — must be reported using the <strong>Incident Report Form</strong> within <strong>24 hours</strong>. Reports go to your direct supervisor and the Safety Committee. Anonymous reporting is also available through the safety hotline.</p>

<h3>💡 Key Takeaway</h3>
<p>Safety is a shared responsibility. If you see a hazard, report it immediately — you could prevent someone from getting hurt.</p>
""",

("course-compliance-101", 3): """
<h2>Anti-Harassment Training</h2>

<h3>🎯 Learning Objectives</h3>
<ul>
  <li>Define workplace harassment and its different forms</li>
  <li>Understand bystander responsibility</li>
  <li>Know how to report incidents safely and confidentially</li>
</ul>

<h3>What Is Workplace Harassment?</h3>
<p>Workplace harassment is any unwelcome conduct based on race, color, religion, sex, national origin, age, disability, or genetic information that creates a hostile, intimidating, or offensive work environment.</p>

<h3>Forms of Harassment</h3>
<ul>
  <li><strong>Verbal:</strong> Derogatory comments, slurs, unwelcome jokes, or intimidating language.</li>
  <li><strong>Physical:</strong> Unwanted touching, blocking movement, or physical intimidation.</li>
  <li><strong>Visual:</strong> Offensive images, emails, or gestures.</li>
  <li><strong>Cyber:</strong> Online bullying, threatening messages, or inappropriate social media behavior.</li>
  <li><strong>Quid Pro Quo:</strong> When employment decisions are conditioned on submission to unwelcome conduct.</li>
</ul>

<h3>The Bystander's Role</h3>
<p>If you witness harassment, you have the power to help:</p>
<ol>
  <li><strong>Intervene Safely:</strong> If you feel comfortable, speak up in the moment.</li>
  <li><strong>Support the Victim:</strong> Check on the person afterward and let them know you saw what happened.</li>
  <li><strong>Report It:</strong> File a report even if the affected person hasn't — you may not be the only witness.</li>
  <li><strong>Document:</strong> Write down what you saw, when, and who was involved.</li>
</ol>

<h3>How to Report</h3>
<ul>
  <li><strong>Direct Supervisor:</strong> Your first point of contact (unless they are involved).</li>
  <li><strong>HR Department:</strong> Available via email, phone, or in-person appointment.</li>
  <li><strong>Ethics Hotline:</strong> Anonymous, 24/7 reporting line.</li>
  <li><strong>Online Portal:</strong> Submit reports through the company's ethics & compliance portal.</li>
</ul>

<h3>Zero Tolerance Policy</h3>
<p>Our organization maintains a <strong>zero tolerance policy</strong> for harassment. All reports are investigated promptly, and retaliating against anyone who reports harassment is strictly prohibited and grounds for termination.</p>

<h3>💡 Key Takeaway</h3>
<p>Everyone deserves a respectful workplace. If you experience or witness harassment, speak up — the organization will protect you.</p>
""",

("course-compliance-101", 4): """
<h2>Ethics & Code of Conduct</h2>

<h3>🎯 Learning Objectives</h3>
<ul>
  <li>Understand the company's ethical standards</li>
  <li>Recognize conflicts of interest and how to disclose them</li>
  <li>Know whistleblower protections and how to use them</li>
</ul>

<h3>Our Ethical Standards</h3>
<p>Ethics goes beyond following the law — it's about doing what's right even when no one is watching. Our ethical framework is built on four pillars:</p>
<ol>
  <li><strong>Honesty:</strong> Be truthful in all communications and transactions.</li>
  <li><strong>Accountability:</strong> Own your decisions and their consequences.</li>
  <li><strong>Fairness:</strong> Treat everyone equitably, without favoritism or bias.</li>
  <li><strong>Respect:</strong> Value diversity and treat colleagues with dignity.</li>
</ol>

<h3>Conflicts of Interest</h3>
<p>A conflict of interest occurs when your personal interests could influence — or appear to influence — your professional judgment. Examples include:</p>
<ul>
  <li>Having a financial interest in a vendor or competitor</li>
  <li>Hiring or supervising a family member</li>
  <li>Accepting gifts worth more than $50 from business partners</li>
  <li>Using company resources for personal gain</li>
</ul>
<p><strong>What to do:</strong> Disclose any potential conflict to your manager or the Ethics Committee using the Conflict of Interest Disclosure Form. Disclosure does not automatically mean you've done something wrong — it means you're being transparent.</p>

<h3>Whistleblower Protections</h3>
<p>Employees who report unethical behavior, fraud, or violations in good faith are protected by:</p>
<ul>
  <li>Federal and state whistleblower protection laws</li>
  <li>Our internal non-retaliation policy</li>
  <li>Anonymous reporting channels (Ethics Hotline, online portal)</li>
</ul>
<p>Retaliation against whistleblowers is a <strong>terminable offense</strong> and may result in legal action against the retaliator.</p>

<h3>Real-World Scenario</h3>
<p><em>You notice a colleague submitting inflated expense reports. What should you do?</em></p>
<ol>
  <li>Do not confront them directly — this is not your role.</li>
  <li>Report it through the Ethics Hotline or to your manager.</li>
  <li>Document what you observed with dates and amounts.</li>
  <li>Trust the investigation process and maintain confidentiality.</li>
</ol>

<h3>💡 Key Takeaway</h3>
<p>Ethics is the foundation of trust. When you act ethically, you protect yourself, your colleagues, and the entire organization.</p>
""",

# ═══════════════════════════════════════════════════════════════════════════
# SECURITY AWARENESS TRAINING
# ═══════════════════════════════════════════════════════════════════════════
("course-security-101", 0): """
<h2>Cybersecurity Fundamentals</h2>

<h3>🎯 Learning Objectives</h3>
<ul>
  <li>Understand the current cyber threat landscape</li>
  <li>Learn the CIA Triad (Confidentiality, Integrity, Availability)</li>
  <li>Identify your role in organizational security</li>
</ul>

<h3>The Threat Landscape</h3>
<p>Cyberattacks are growing in frequency and sophistication. In 2024 alone, the average cost of a data breach reached <strong>$4.88 million</strong> (IBM). Common threats include:</p>
<ul>
  <li><strong>Ransomware:</strong> Malware that encrypts your files and demands payment for decryption.</li>
  <li><strong>Phishing:</strong> Deceptive emails or messages that trick you into revealing credentials.</li>
  <li><strong>Insider Threats:</strong> Intentional or accidental data exposure by employees.</li>
  <li><strong>Supply Chain Attacks:</strong> Compromising third-party software or services.</li>
  <li><strong>Zero-Day Exploits:</strong> Attacks on previously unknown vulnerabilities.</li>
</ul>

<h3>The CIA Triad</h3>
<p>The foundation of all information security:</p>
<table style="width:100%;border-collapse:collapse;margin:12px 0">
  <tr style="background:#f0f0f0"><th style="padding:8px;text-align:left;border:1px solid #ddd">Principle</th><th style="padding:8px;text-align:left;border:1px solid #ddd">Definition</th><th style="padding:8px;text-align:left;border:1px solid #ddd">Example</th></tr>
  <tr><td style="padding:8px;border:1px solid #ddd"><strong>Confidentiality</strong></td><td style="padding:8px;border:1px solid #ddd">Only authorized people can access data</td><td style="padding:8px;border:1px solid #ddd">Encryption, access controls</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd"><strong>Integrity</strong></td><td style="padding:8px;border:1px solid #ddd">Data is accurate and unaltered</td><td style="padding:8px;border:1px solid #ddd">Checksums, audit trails</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd"><strong>Availability</strong></td><td style="padding:8px;border:1px solid #ddd">Systems are accessible when needed</td><td style="padding:8px;border:1px solid #ddd">Backups, redundancy</td></tr>
</table>

<h3>Your Role in Security</h3>
<p>Every employee is a potential target — and a potential defender. You can protect the organization by:</p>
<ol>
  <li>Using strong, unique passwords and enabling MFA.</li>
  <li>Verifying unexpected requests for sensitive information.</li>
  <li>Keeping your devices and software up to date.</li>
  <li>Locking your workstation when you step away.</li>
  <li>Reporting any suspicious activity immediately.</li>
</ol>

<h3>💡 Key Takeaway</h3>
<p>Security is not just IT's job — it's everyone's responsibility. A single click on a phishing email can compromise the entire organization.</p>
""",

("course-security-101", 1): """
<h2>Phishing & Social Engineering</h2>

<h3>🎯 Learning Objectives</h3>
<ul>
  <li>Recognize phishing emails and social engineering tactics</li>
  <li>Apply the SLAM method to evaluate suspicious messages</li>
  <li>Know what to do when you receive a suspected phishing attempt</li>
</ul>

<h3>What Is Phishing?</h3>
<p>Phishing is a type of social engineering attack where attackers impersonate trusted entities to trick you into revealing sensitive information (passwords, credit card numbers, etc.) or clicking malicious links.</p>

<h3>Types of Phishing</h3>
<ul>
  <li><strong>Email Phishing:</strong> Mass emails that mimic legitimate organizations.</li>
  <li><strong>Spear Phishing:</strong> Targeted attacks personalized with your name, role, or company info.</li>
  <li><strong>Whaling:</strong> Attacks targeting executives and senior management.</li>
  <li><strong>Smishing:</strong> Phishing via SMS text messages.</li>
  <li><strong>Vishing:</strong> Phone-based phishing calls.</li>
</ul>

<h3>The SLAM Method</h3>
<p>Use <strong>SLAM</strong> to evaluate every unexpected email:</p>
<table style="width:100%;border-collapse:collapse;margin:12px 0">
  <tr style="background:#f0f0f0"><th style="padding:8px;border:1px solid #ddd">Letter</th><th style="padding:8px;border:1px solid #ddd">Check</th><th style="padding:8px;border:1px solid #ddd">What to Look For</th></tr>
  <tr><td style="padding:8px;border:1px solid #ddd"><strong>S</strong></td><td style="padding:8px;border:1px solid #ddd">Sender</td><td style="padding:8px;border:1px solid #ddd">Is the email address slightly misspelled? (e.g., support@g00gle.com)</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd"><strong>L</strong></td><td style="padding:8px;border:1px solid #ddd">Links</td><td style="padding:8px;border:1px solid #ddd">Hover over links — does the URL match the expected destination?</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd"><strong>A</strong></td><td style="padding:8px;border:1px solid #ddd">Attachments</td><td style="padding:8px;border:1px solid #ddd">Were you expecting an attachment? Is the file type suspicious (.exe, .zip)?</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd"><strong>M</strong></td><td style="padding:8px;border:1px solid #ddd">Message</td><td style="padding:8px;border:1px solid #ddd">Urgency, spelling errors, generic greetings ("Dear Customer").</td></tr>
</table>

<h3>Red Flags to Watch For</h3>
<ul>
  <li>🚩 Urgent language: "Your account will be suspended in 24 hours!"</li>
  <li>🚩 Requests for credentials or payment information via email</li>
  <li>🚩 Mismatched sender name and email address</li>
  <li>🚩 Links that go to unfamiliar domains</li>
  <li>🚩 Unexpected attachments, especially .exe, .zip, or macro-enabled docs</li>
</ul>

<h3>What to Do If You Suspect Phishing</h3>
<ol>
  <li><strong>Don't click</strong> any links or download attachments.</li>
  <li><strong>Don't reply</strong> to the message.</li>
  <li><strong>Report it</strong> using the "Report Phishing" button in your email client or forward it to security@company.com.</li>
  <li><strong>Delete</strong> the message after reporting.</li>
  <li>If you already clicked — <strong>change your password immediately</strong> and contact IT Security.</li>
</ol>

<h3>💡 Key Takeaway</h3>
<p>When in doubt, don't click. Take 10 seconds to verify — it could save the company millions.</p>
""",

("course-security-101", 2): """
<h2>Password & Access Management</h2>

<h3>🎯 Learning Objectives</h3>
<ul>
  <li>Create strong, memorable passwords</li>
  <li>Understand and use Multi-Factor Authentication (MFA)</li>
  <li>Follow the Principle of Least Privilege</li>
</ul>

<h3>Password Best Practices</h3>
<p>Passwords remain the most common form of authentication. Follow these rules:</p>
<ul>
  <li><strong>Length Over Complexity:</strong> A 16-character passphrase ("correct-horse-battery-staple") is stronger than "P@$$w0rd!"</li>
  <li><strong>Unique Per Account:</strong> Never reuse passwords across different services.</li>
  <li><strong>Use a Password Manager:</strong> Tools like Bitwarden, 1Password, or LastPass generate and store complex passwords securely.</li>
  <li><strong>Never Share Passwords:</strong> Not with colleagues, not with IT support, not with your manager.</li>
</ul>

<h3>Multi-Factor Authentication (MFA)</h3>
<p>MFA adds an extra layer of security by requiring two or more verification factors:</p>
<table style="width:100%;border-collapse:collapse;margin:12px 0">
  <tr style="background:#f0f0f0"><th style="padding:8px;border:1px solid #ddd">Factor</th><th style="padding:8px;border:1px solid #ddd">Type</th><th style="padding:8px;border:1px solid #ddd">Example</th></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">Something You Know</td><td style="padding:8px;border:1px solid #ddd">Knowledge</td><td style="padding:8px;border:1px solid #ddd">Password, PIN</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">Something You Have</td><td style="padding:8px;border:1px solid #ddd">Possession</td><td style="padding:8px;border:1px solid #ddd">Phone, hardware token</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">Something You Are</td><td style="padding:8px;border:1px solid #ddd">Biometric</td><td style="padding:8px;border:1px solid #ddd">Fingerprint, face recognition</td></tr>
</table>
<p><strong>Always enable MFA</strong> on all accounts that support it, especially email, VPN, and cloud services.</p>

<h3>Principle of Least Privilege</h3>
<p>Users should only have access to the resources they need to do their job — nothing more. This limits the blast radius if an account is compromised.</p>
<ul>
  <li>Request only the access you need.</li>
  <li>Review your access permissions quarterly.</li>
  <li>Report any access you have that you don't need.</li>
  <li>When changing roles, ensure old access is revoked.</li>
</ul>

<h3>💡 Key Takeaway</h3>
<p>Your password is the key to the kingdom. Make it strong, make it unique, and add MFA as your second lock.</p>
""",

("course-security-101", 3): """
<h2>Incident Reporting</h2>

<h3>🎯 Learning Objectives</h3>
<ul>
  <li>Identify what constitutes a security incident</li>
  <li>Follow the proper incident reporting process</li>
  <li>Understand the incident response lifecycle</li>
</ul>

<h3>What Is a Security Incident?</h3>
<p>A security incident is any event that compromises the confidentiality, integrity, or availability of information or systems. Examples include:</p>
<ul>
  <li>Unauthorized access to systems or data</li>
  <li>Lost or stolen devices (laptops, phones, USB drives)</li>
  <li>Malware infection or ransomware attack</li>
  <li>Accidental data exposure (e.g., sending sensitive data to the wrong person)</li>
  <li>Suspicious login attempts or account lockouts</li>
  <li>Physical security breaches (tailgating, unauthorized building access)</li>
</ul>

<h3>Incident Reporting Process</h3>
<ol>
  <li><strong>Identify:</strong> Recognize that something unusual is happening.</li>
  <li><strong>Contain:</strong> If possible, disconnect the affected device from the network. Do NOT try to "fix" it yourself.</li>
  <li><strong>Report:</strong> Contact IT Security immediately:
    <ul>
      <li>📧 security@company.com</li>
      <li>📞 Security Hotline: ext. 7000</li>
      <li>🖥️ ServiceNow Incident Portal</li>
    </ul>
  </li>
  <li><strong>Document:</strong> Record what happened, when, and any actions you took.</li>
  <li><strong>Cooperate:</strong> Work with the incident response team during investigation.</li>
</ol>

<h3>Incident Response Lifecycle</h3>
<p>The security team follows the NIST Incident Response Framework:</p>
<ol>
  <li><strong>Preparation:</strong> Having tools, processes, and training in place.</li>
  <li><strong>Detection & Analysis:</strong> Identifying and assessing the scope of the incident.</li>
  <li><strong>Containment, Eradication & Recovery:</strong> Stopping the attack, removing the threat, and restoring services.</li>
  <li><strong>Post-Incident Activity:</strong> Lessons learned, process improvements, and documentation.</li>
</ol>

<h3>⚠️ Common Mistakes</h3>
<ul>
  <li>Delaying the report hoping the problem will "go away"</li>
  <li>Trying to investigate or fix the issue on your own</li>
  <li>Turning off the affected machine (this destroys forensic evidence)</li>
  <li>Not reporting "minor" incidents (they may be part of a larger attack)</li>
</ul>

<h3>💡 Key Takeaway</h3>
<p>Speed matters. The sooner you report an incident, the faster the team can contain it and limit damage. There is <strong>no penalty</strong> for reporting a false alarm — only for not reporting at all.</p>
""",

# ═══════════════════════════════════════════════════════════════════════════
# LEADERSHIP DEVELOPMENT PROGRAM
# ═══════════════════════════════════════════════════════════════════════════
("course-leadership-201", 0): """
<h2>Team Management Essentials</h2>

<h3>🎯 Learning Objectives</h3>
<ul>
  <li>Set clear, measurable team goals using the SMART framework</li>
  <li>Master the art of effective delegation</li>
  <li>Build and sustain high-performance teams</li>
</ul>

<h3>Setting SMART Goals</h3>
<p>Effective leaders set goals that are:</p>
<ul>
  <li><strong>Specific:</strong> "Increase customer satisfaction score" → "Increase NPS from 45 to 60"</li>
  <li><strong>Measurable:</strong> Define metrics to track progress.</li>
  <li><strong>Achievable:</strong> Challenging but realistic given resources.</li>
  <li><strong>Relevant:</strong> Aligned with team and organizational objectives.</li>
  <li><strong>Time-Bound:</strong> Set a clear deadline.</li>
</ul>

<h3>Effective Delegation</h3>
<p>Delegation is not about offloading work — it's about empowering your team:</p>
<ol>
  <li><strong>Match tasks to strengths:</strong> Assign work to team members whose skills align with the task.</li>
  <li><strong>Be clear about expectations:</strong> Define the desired outcome, deadline, and any constraints.</li>
  <li><strong>Provide resources and authority:</strong> Give them what they need to succeed.</li>
  <li><strong>Check in, don't check up:</strong> Monitor progress without micromanaging.</li>
  <li><strong>Recognize and celebrate:</strong> Acknowledge good work publicly.</li>
</ol>

<h3>Building High-Performance Teams</h3>
<p>According to Patrick Lencioni's model, high-performance teams have:</p>
<ul>
  <li><strong>Trust:</strong> Team members are vulnerable and honest with each other.</li>
  <li><strong>Healthy Conflict:</strong> Constructive debate around ideas, not personal attacks.</li>
  <li><strong>Commitment:</strong> Once a decision is made, everyone commits — even dissenters.</li>
  <li><strong>Accountability:</strong> Team members hold each other accountable.</li>
  <li><strong>Results Focus:</strong> Collective goals take priority over individual agendas.</li>
</ul>

<h3>💡 Key Takeaway</h3>
<p>Great managers don't create followers — they develop leaders. Invest in your team's growth, and the results will follow.</p>
""",

("course-leadership-201", 1): """
<h2>Communication & Feedback</h2>

<h3>🎯 Learning Objectives</h3>
<ul>
  <li>Apply effective communication frameworks</li>
  <li>Give and receive constructive feedback using the SBI model</li>
  <li>Adapt your communication style to different audiences</li>
</ul>

<h3>The Communication Framework</h3>
<p>Effective leadership communication follows the <strong>3 C's</strong>:</p>
<ol>
  <li><strong>Clear:</strong> Use simple, direct language. Avoid jargon when possible.</li>
  <li><strong>Concise:</strong> Get to the point. Respect your audience's time.</li>
  <li><strong>Consistent:</strong> Ensure your message aligns across channels and over time.</li>
</ol>

<h3>Active Listening</h3>
<p>Communication is not just about speaking — it's about listening. Active listening involves:</p>
<ul>
  <li>Making eye contact and giving your full attention</li>
  <li>Paraphrasing what you heard to confirm understanding</li>
  <li>Asking open-ended questions to explore ideas</li>
  <li>Avoiding interrupting or formulating your response while the other person is speaking</li>
</ul>

<h3>The SBI Feedback Model</h3>
<p>Use <strong>Situation → Behavior → Impact</strong> for both positive and constructive feedback:</p>
<table style="width:100%;border-collapse:collapse;margin:12px 0">
  <tr style="background:#f0f0f0"><th style="padding:8px;border:1px solid #ddd">Step</th><th style="padding:8px;border:1px solid #ddd">Example (Constructive)</th><th style="padding:8px;border:1px solid #ddd">Example (Positive)</th></tr>
  <tr><td style="padding:8px;border:1px solid #ddd"><strong>Situation</strong></td><td style="padding:8px;border:1px solid #ddd">"In yesterday's client meeting…"</td><td style="padding:8px;border:1px solid #ddd">"During the quarterly review…"</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd"><strong>Behavior</strong></td><td style="padding:8px;border:1px solid #ddd">"you interrupted the client twice."</td><td style="padding:8px;border:1px solid #ddd">"you presented the data clearly and answered every question."</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd"><strong>Impact</strong></td><td style="padding:8px;border:1px solid #ddd">"It made them feel unheard and may affect our relationship."</td><td style="padding:8px;border:1px solid #ddd">"The client was impressed and approved the next phase."</td></tr>
</table>

<h3>💡 Key Takeaway</h3>
<p>Feedback is a gift — when delivered well, it accelerates growth. When received well, it shows maturity and commitment to improvement.</p>
""",

("course-leadership-201", 2): """
<h2>Conflict Resolution</h2>

<h3>🎯 Learning Objectives</h3>
<ul>
  <li>Identify the root causes of workplace conflict</li>
  <li>Apply the Thomas-Kilmann conflict resolution styles</li>
  <li>Mediate disputes effectively as a leader</li>
</ul>

<h3>Common Causes of Workplace Conflict</h3>
<ul>
  <li><strong>Miscommunication:</strong> Unclear expectations or assumptions.</li>
  <li><strong>Resource Scarcity:</strong> Competition for budget, headcount, or tools.</li>
  <li><strong>Personality Clashes:</strong> Different working styles or values.</li>
  <li><strong>Role Ambiguity:</strong> Overlapping responsibilities or unclear ownership.</li>
  <li><strong>Unequal Treatment:</strong> Perceived favoritism or unfairness.</li>
</ul>

<h3>Thomas-Kilmann Conflict Modes</h3>
<table style="width:100%;border-collapse:collapse;margin:12px 0">
  <tr style="background:#f0f0f0"><th style="padding:8px;border:1px solid #ddd">Style</th><th style="padding:8px;border:1px solid #ddd">When to Use</th></tr>
  <tr><td style="padding:8px;border:1px solid #ddd"><strong>Competing</strong></td><td style="padding:8px;border:1px solid #ddd">Emergency decisions; when you're certain you're right.</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd"><strong>Collaborating</strong></td><td style="padding:8px;border:1px solid #ddd">Important issues where both parties' concerns matter.</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd"><strong>Compromising</strong></td><td style="padding:8px;border:1px solid #ddd">When a quick, mutually acceptable solution is needed.</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd"><strong>Avoiding</strong></td><td style="padding:8px;border:1px solid #ddd">Trivial issues or when emotions are too high.</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd"><strong>Accommodating</strong></td><td style="padding:8px;border:1px solid #ddd">When the relationship is more important than the issue.</td></tr>
</table>

<h3>Mediation Steps</h3>
<ol>
  <li><strong>Separate the parties</strong> and speak to each individually.</li>
  <li><strong>Identify the issue</strong> — focus on interests, not positions.</li>
  <li><strong>Bring them together</strong> in a neutral setting.</li>
  <li><strong>Establish ground rules:</strong> No interrupting, focus on solutions.</li>
  <li><strong>Facilitate dialogue</strong> and guide toward a mutually acceptable outcome.</li>
  <li><strong>Document the agreement</strong> and schedule a follow-up.</li>
</ol>

<h3>💡 Key Takeaway</h3>
<p>Conflict isn't the enemy — unmanaged conflict is. Address issues early, listen to all sides, and focus on solutions rather than blame.</p>
""",

("course-leadership-201", 3): """
<h2>Strategic Thinking</h2>

<h3>🎯 Learning Objectives</h3>
<ul>
  <li>Think beyond day-to-day tasks to see the big picture</li>
  <li>Use decision-making frameworks to evaluate options</li>
  <li>Align team activities with organizational strategy</li>
</ul>

<h3>What Is Strategic Thinking?</h3>
<p>Strategic thinking is the ability to anticipate trends, see the big picture, and make decisions that position your team and organization for long-term success. It's about asking: <em>"Where do we need to be in 1, 3, and 5 years — and how do we get there?"</em></p>

<h3>The SWOT Framework</h3>
<table style="width:100%;border-collapse:collapse;margin:12px 0">
  <tr><td style="padding:12px;border:1px solid #ddd;background:#e8f5e9"><strong>Strengths</strong><br>What do we do well? What advantages do we have?</td><td style="padding:12px;border:1px solid #ddd;background:#fff3e0"><strong>Weaknesses</strong><br>Where can we improve? What gaps exist?</td></tr>
  <tr><td style="padding:12px;border:1px solid #ddd;background:#e3f2fd"><strong>Opportunities</strong><br>What trends can we capitalize on? What markets are growing?</td><td style="padding:12px;border:1px solid #ddd;background:#ffebee"><strong>Threats</strong><br>What competitors or risks could hurt us?</td></tr>
</table>

<h3>Decision-Making Frameworks</h3>
<ul>
  <li><strong>Eisenhower Matrix:</strong> Prioritize tasks by urgency and importance.</li>
  <li><strong>Cost-Benefit Analysis:</strong> Weigh the expected costs vs. benefits of each option.</li>
  <li><strong>RACI Matrix:</strong> Clarify who is Responsible, Accountable, Consulted, and Informed for each decision.</li>
  <li><strong>Pre-Mortem:</strong> Before executing, imagine the plan has failed — what went wrong? Use this to identify risks proactively.</li>
</ul>

<h3>Aligning Team Goals with Strategy</h3>
<p>Use the <strong>OKR (Objectives and Key Results)</strong> framework:</p>
<ul>
  <li><strong>Objective:</strong> A qualitative goal (e.g., "Become the market leader in customer satisfaction")</li>
  <li><strong>Key Results:</strong> Measurable outcomes (e.g., "Achieve NPS of 70+", "Reduce response time to &lt;2 hours")</li>
</ul>

<h3>💡 Key Takeaway</h3>
<p>Strategy without execution is a dream. Execution without strategy is chaos. Effective leaders connect the two.</p>
""",

("course-leadership-201", 4): """
<h2>Change Management</h2>

<h3>🎯 Learning Objectives</h3>
<ul>
  <li>Understand why change initiatives fail</li>
  <li>Apply Kotter's 8-Step Change Model</li>
  <li>Lead your team through transitions effectively</li>
</ul>

<h3>Why Change Fails</h3>
<p>Research shows that <strong>70% of change initiatives fail</strong>. Common reasons include:</p>
<ul>
  <li>Lack of clear vision or urgency</li>
  <li>Insufficient leadership support</li>
  <li>Poor communication about the "why"</li>
  <li>Resistance from employees who feel unheard</li>
  <li>Declaring victory too early</li>
</ul>

<h3>Kotter's 8-Step Model</h3>
<ol>
  <li><strong>Create Urgency:</strong> Help others see why change is needed <em>now</em>.</li>
  <li><strong>Build a Coalition:</strong> Assemble a team of influential supporters.</li>
  <li><strong>Form a Vision:</strong> Develop a clear, compelling vision of the future state.</li>
  <li><strong>Communicate the Vision:</strong> Share it frequently through multiple channels.</li>
  <li><strong>Empower Action:</strong> Remove barriers and give people the tools to act.</li>
  <li><strong>Create Quick Wins:</strong> Show progress early to build momentum.</li>
  <li><strong>Build on Change:</strong> Use each success to drive the next improvement.</li>
  <li><strong>Anchor in Culture:</strong> Make the change part of "how we do things here."</li>
</ol>

<h3>Managing Resistance</h3>
<p>Resistance is natural. Address it by:</p>
<ul>
  <li><strong>Listening:</strong> Understand their concerns before responding.</li>
  <li><strong>Involving:</strong> Give people a role in shaping the change.</li>
  <li><strong>Supporting:</strong> Provide training, resources, and emotional support.</li>
  <li><strong>Acknowledging:</strong> Recognize that change is hard and validate feelings.</li>
</ul>

<h3>💡 Key Takeaway</h3>
<p>People don't resist change — they resist being changed. Involve them in the process, and they'll become your biggest advocates.</p>
""",

("course-leadership-201", 5): """
<h2>Mentoring & Coaching</h2>

<h3>🎯 Learning Objectives</h3>
<ul>
  <li>Distinguish between mentoring and coaching</li>
  <li>Use the GROW coaching model</li>
  <li>Create a development plan for your team members</li>
</ul>

<h3>Mentoring vs. Coaching</h3>
<table style="width:100%;border-collapse:collapse;margin:12px 0">
  <tr style="background:#f0f0f0"><th style="padding:8px;border:1px solid #ddd">Aspect</th><th style="padding:8px;border:1px solid #ddd">Mentoring</th><th style="padding:8px;border:1px solid #ddd">Coaching</th></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">Focus</td><td style="padding:8px;border:1px solid #ddd">Long-term career development</td><td style="padding:8px;border:1px solid #ddd">Specific skills or performance goals</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">Relationship</td><td style="padding:8px;border:1px solid #ddd">Senior → Junior</td><td style="padding:8px;border:1px solid #ddd">Manager → Team Member</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">Duration</td><td style="padding:8px;border:1px solid #ddd">Months to years</td><td style="padding:8px;border:1px solid #ddd">Weeks to months</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">Approach</td><td style="padding:8px;border:1px solid #ddd">Sharing experience and advice</td><td style="padding:8px;border:1px solid #ddd">Asking questions and guiding discovery</td></tr>
</table>

<h3>The GROW Model</h3>
<p>A simple but powerful coaching framework:</p>
<ol>
  <li><strong>Goal:</strong> "What do you want to achieve?" Define a clear, specific goal.</li>
  <li><strong>Reality:</strong> "Where are you now?" Assess the current situation honestly.</li>
  <li><strong>Options:</strong> "What could you do?" Brainstorm possible actions without judging.</li>
  <li><strong>Will:</strong> "What will you do?" Commit to specific actions with deadlines.</li>
</ol>

<h3>Creating Individual Development Plans</h3>
<p>An effective IDP includes:</p>
<ul>
  <li><strong>Current Skills Assessment:</strong> Where is the person today?</li>
  <li><strong>Career Aspirations:</strong> Where do they want to go?</li>
  <li><strong>Skill Gaps:</strong> What needs to be developed?</li>
  <li><strong>Action Items:</strong> Specific learning activities, projects, or experiences.</li>
  <li><strong>Timeline & Checkpoints:</strong> Regular review dates to track progress.</li>
</ul>

<h3>💡 Key Takeaway</h3>
<p>The best leaders develop other leaders. Investing time in mentoring and coaching is the highest-ROI activity you can do as a manager.</p>
""",

# ═══════════════════════════════════════════════════════════════════════════
# TECHNICAL SKILLS ONBOARDING
# ═══════════════════════════════════════════════════════════════════════════
("course-technical-101", 0): """
<h2>Tools & Systems Overview</h2>

<h3>🎯 Learning Objectives</h3>
<ul>
  <li>Navigate the company's core software tools</li>
  <li>Understand how systems integrate with each other</li>
  <li>Set up your workstation for maximum productivity</li>
</ul>

<h3>Our Technology Stack</h3>
<table style="width:100%;border-collapse:collapse;margin:12px 0">
  <tr style="background:#f0f0f0"><th style="padding:8px;border:1px solid #ddd">Category</th><th style="padding:8px;border:1px solid #ddd">Tool</th><th style="padding:8px;border:1px solid #ddd">Purpose</th></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">Communication</td><td style="padding:8px;border:1px solid #ddd">Microsoft Teams / Slack</td><td style="padding:8px;border:1px solid #ddd">Messaging, video calls, channels</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">Email</td><td style="padding:8px;border:1px solid #ddd">Outlook / Gmail</td><td style="padding:8px;border:1px solid #ddd">Formal communication, calendar</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">Project Management</td><td style="padding:8px;border:1px solid #ddd">Jira / Asana</td><td style="padding:8px;border:1px solid #ddd">Task tracking, sprint planning</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">CRM</td><td style="padding:8px;border:1px solid #ddd">Salesforce</td><td style="padding:8px;border:1px solid #ddd">Customer relationship management</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">Document Storage</td><td style="padding:8px;border:1px solid #ddd">SharePoint / Google Drive</td><td style="padding:8px;border:1px solid #ddd">File storage and collaboration</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">HR Portal</td><td style="padding:8px;border:1px solid #ddd">Workday / BambooHR</td><td style="padding:8px;border:1px solid #ddd">Time off, benefits, payroll</td></tr>
</table>

<h3>Getting Set Up</h3>
<ol>
  <li><strong>Credentials:</strong> You'll receive login credentials via your onboarding email. Change default passwords immediately.</li>
  <li><strong>MFA Enrollment:</strong> Set up Multi-Factor Authentication on all accounts (see Security Awareness Training).</li>
  <li><strong>VPN Access:</strong> Install and configure the VPN client for remote access.</li>
  <li><strong>Software Installation:</strong> Use the Software Center / Self-Service portal to install approved applications.</li>
  <li><strong>Bookmarks:</strong> Save quick links to the intranet, knowledge base, and IT support portal.</li>
</ol>

<h3>Integration Map</h3>
<p>Our systems are interconnected: CRM data flows into reporting dashboards, project management integrates with version control, and HR systems sync with the payroll provider. Understanding these connections helps you see how your work fits into the bigger picture.</p>

<h3>💡 Key Takeaway</h3>
<p>Don't try to learn everything at once. Focus on the tools you'll use daily, and explore others as needed. The IT Help Desk is always available for support.</p>
""",

("course-technical-101", 1): """
<h2>Process Documentation</h2>

<h3>🎯 Learning Objectives</h3>
<ul>
  <li>Write clear, maintainable Standard Operating Procedures (SOPs)</li>
  <li>Use templates and version control for documentation</li>
  <li>Understand the document review and approval process</li>
</ul>

<h3>Why Documentation Matters</h3>
<p>Good documentation reduces errors, speeds up onboarding, ensures consistency, and protects the organization's knowledge from being lost when employees leave.</p>

<h3>Writing Effective SOPs</h3>
<p>Every SOP should include:</p>
<ol>
  <li><strong>Purpose:</strong> Why does this process exist?</li>
  <li><strong>Scope:</strong> Who does it apply to?</li>
  <li><strong>Step-by-Step Instructions:</strong> Numbered, action-oriented steps with screenshots where applicable.</li>
  <li><strong>Roles & Responsibilities:</strong> Who does what?</li>
  <li><strong>Exceptions:</strong> What to do when the standard process doesn't apply.</li>
  <li><strong>Version History:</strong> Track changes over time.</li>
</ol>

<h3>Best Practices</h3>
<ul>
  <li>Use <strong>active voice</strong> and simple language.</li>
  <li>Include <strong>visuals</strong> (screenshots, flowcharts, diagrams) wherever possible.</li>
  <li>Store documents in the <strong>central knowledge base</strong>, not personal drives.</li>
  <li>Review and update SOPs at least <strong>annually</strong> or when processes change.</li>
  <li>Use <strong>version numbers</strong> (v1.0, v1.1, v2.0) to track revisions.</li>
</ul>

<h3>💡 Key Takeaway</h3>
<p>If a process isn't documented, it doesn't exist. Write it down, keep it updated, and make it accessible.</p>
""",

("course-technical-101", 2): """
<h2>Quality Standards</h2>

<h3>🎯 Learning Objectives</h3>
<ul>
  <li>Understand ISO 9001 and quality management principles</li>
  <li>Apply continuous improvement methodologies</li>
  <li>Use quality metrics to track and improve performance</li>
</ul>

<h3>ISO 9001 Overview</h3>
<p>ISO 9001 is the international standard for Quality Management Systems (QMS). It's based on seven principles:</p>
<ol>
  <li>Customer Focus</li>
  <li>Leadership</li>
  <li>Engagement of People</li>
  <li>Process Approach</li>
  <li>Improvement</li>
  <li>Evidence-Based Decision Making</li>
  <li>Relationship Management</li>
</ol>

<h3>Continuous Improvement: PDCA Cycle</h3>
<p>The <strong>Plan-Do-Check-Act</strong> cycle is the engine of continuous improvement:</p>
<ul>
  <li><strong>Plan:</strong> Identify the problem and develop a solution.</li>
  <li><strong>Do:</strong> Implement the solution on a small scale.</li>
  <li><strong>Check:</strong> Measure the results — did it work?</li>
  <li><strong>Act:</strong> If successful, standardize. If not, revise and repeat.</li>
</ul>

<h3>Key Quality Metrics</h3>
<table style="width:100%;border-collapse:collapse;margin:12px 0">
  <tr style="background:#f0f0f0"><th style="padding:8px;border:1px solid #ddd">Metric</th><th style="padding:8px;border:1px solid #ddd">What It Measures</th><th style="padding:8px;border:1px solid #ddd">Target</th></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">Defect Rate</td><td style="padding:8px;border:1px solid #ddd">Errors per unit of output</td><td style="padding:8px;border:1px solid #ddd">&lt; 1%</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">First Pass Yield</td><td style="padding:8px;border:1px solid #ddd">% of work done right the first time</td><td style="padding:8px;border:1px solid #ddd">&gt; 95%</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">Customer Satisfaction</td><td style="padding:8px;border:1px solid #ddd">Survey scores from clients</td><td style="padding:8px;border:1px solid #ddd">&gt; 4.5/5</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">On-Time Delivery</td><td style="padding:8px;border:1px solid #ddd">% of deliverables meeting deadlines</td><td style="padding:8px;border:1px solid #ddd">&gt; 98%</td></tr>
</table>

<h3>💡 Key Takeaway</h3>
<p>Quality is not a department — it's a habit. Every process you touch is an opportunity to improve.</p>
""",

("course-technical-101", 3): """
<h2>Project Management Basics</h2>

<h3>🎯 Learning Objectives</h3>
<ul>
  <li>Understand Agile methodology and Scrum framework</li>
  <li>Use project management tools effectively</li>
  <li>Track progress and communicate status to stakeholders</li>
</ul>

<h3>Agile Methodology</h3>
<p>Agile is an iterative approach to project management that delivers work in small, usable increments called <strong>sprints</strong> (typically 1-4 weeks). Key principles:</p>
<ul>
  <li>Individuals and interactions over processes and tools</li>
  <li>Working software over comprehensive documentation</li>
  <li>Customer collaboration over contract negotiation</li>
  <li>Responding to change over following a plan</li>
</ul>

<h3>Scrum Framework</h3>
<table style="width:100%;border-collapse:collapse;margin:12px 0">
  <tr style="background:#f0f0f0"><th style="padding:8px;border:1px solid #ddd">Ceremony</th><th style="padding:8px;border:1px solid #ddd">Purpose</th><th style="padding:8px;border:1px solid #ddd">Frequency</th></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">Sprint Planning</td><td style="padding:8px;border:1px solid #ddd">Decide what to build in the sprint</td><td style="padding:8px;border:1px solid #ddd">Start of sprint</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">Daily Standup</td><td style="padding:8px;border:1px solid #ddd">Share progress and blockers (15 min)</td><td style="padding:8px;border:1px solid #ddd">Daily</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">Sprint Review</td><td style="padding:8px;border:1px solid #ddd">Demo completed work to stakeholders</td><td style="padding:8px;border:1px solid #ddd">End of sprint</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">Retrospective</td><td style="padding:8px;border:1px solid #ddd">Reflect: What went well? What to improve?</td><td style="padding:8px;border:1px solid #ddd">End of sprint</td></tr>
</table>

<h3>Using Project Management Tools</h3>
<p>Whether you use Jira, Asana, or Trello, follow these best practices:</p>
<ol>
  <li>Break work into <strong>small, actionable tasks</strong> (< 1 day of work each).</li>
  <li>Use <strong>clear titles</strong> that describe the deliverable (e.g., "Create login form validation").</li>
  <li>Assign <strong>owners and due dates</strong> to every task.</li>
  <li>Update task status <strong>daily</strong>.</li>
  <li>Use labels and filters to organize work by priority, type, or component.</li>
</ol>

<h3>💡 Key Takeaway</h3>
<p>A project plan is a living document. Update it regularly, communicate proactively, and don't be afraid to adjust when reality changes.</p>
""",

("course-technical-101", 4): """
<h2>Troubleshooting & Support</h2>

<h3>🎯 Learning Objectives</h3>
<ul>
  <li>Follow a systematic troubleshooting methodology</li>
  <li>Know when and how to escalate issues</li>
  <li>Use the knowledge base effectively</li>
</ul>

<h3>The Troubleshooting Methodology</h3>
<ol>
  <li><strong>Identify the Problem:</strong> What exactly is happening? When did it start? Who is affected?</li>
  <li><strong>Gather Information:</strong> Check error messages, logs, recent changes, and similar past incidents.</li>
  <li><strong>Develop a Theory:</strong> Based on the symptoms, what's the most likely cause?</li>
  <li><strong>Test the Theory:</strong> Make one change at a time and observe the result.</li>
  <li><strong>Implement the Fix:</strong> Apply the solution and verify it resolves the issue.</li>
  <li><strong>Document:</strong> Record the problem, root cause, and solution for future reference.</li>
</ol>

<h3>Escalation Matrix</h3>
<table style="width:100%;border-collapse:collapse;margin:12px 0">
  <tr style="background:#f0f0f0"><th style="padding:8px;border:1px solid #ddd">Level</th><th style="padding:8px;border:1px solid #ddd">Who</th><th style="padding:8px;border:1px solid #ddd">When</th></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">Level 1</td><td style="padding:8px;border:1px solid #ddd">Self-Service / Knowledge Base</td><td style="padding:8px;border:1px solid #ddd">First 15 minutes</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">Level 2</td><td style="padding:8px;border:1px solid #ddd">IT Help Desk</td><td style="padding:8px;border:1px solid #ddd">After self-service fails</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">Level 3</td><td style="padding:8px;border:1px solid #ddd">Specialist Team</td><td style="padding:8px;border:1px solid #ddd">Complex or system-wide issues</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">Level 4</td><td style="padding:8px;border:1px solid #ddd">Vendor / External Support</td><td style="padding:8px;border:1px solid #ddd">Vendor-specific product issues</td></tr>
</table>

<h3>Using the Knowledge Base</h3>
<ul>
  <li><strong>Search first:</strong> Before creating a ticket, search the KB — the answer may already exist.</li>
  <li><strong>Use keywords:</strong> Search for error codes, tool names, or symptoms.</li>
  <li><strong>Contribute:</strong> If you solve a new problem, write a KB article so others can benefit.</li>
</ul>

<h3>💡 Key Takeaway</h3>
<p>Systematic troubleshooting saves time and reduces frustration. Follow the methodology, document your findings, and don't hesitate to escalate when needed.</p>
""",

# ═══════════════════════════════════════════════════════════════════════════
# HR & BENEFITS ORIENTATION
# ═══════════════════════════════════════════════════════════════════════════
("course-hr-101", 0): """
<h2>Employee Benefits Overview</h2>

<h3>🎯 Learning Objectives</h3>
<ul>
  <li>Understand your health insurance options and enrollment process</li>
  <li>Learn about retirement plans and company matching</li>
  <li>Discover additional perks and benefits available to you</li>
</ul>

<h3>Health Insurance Plans</h3>
<table style="width:100%;border-collapse:collapse;margin:12px 0">
  <tr style="background:#f0f0f0"><th style="padding:8px;border:1px solid #ddd">Plan</th><th style="padding:8px;border:1px solid #ddd">Monthly Premium</th><th style="padding:8px;border:1px solid #ddd">Deductible</th><th style="padding:8px;border:1px solid #ddd">Best For</th></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">PPO Basic</td><td style="padding:8px;border:1px solid #ddd">$120/mo</td><td style="padding:8px;border:1px solid #ddd">$1,500</td><td style="padding:8px;border:1px solid #ddd">Healthy individuals, lower premiums</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">PPO Plus</td><td style="padding:8px;border:1px solid #ddd">$250/mo</td><td style="padding:8px;border:1px solid #ddd">$750</td><td style="padding:8px;border:1px solid #ddd">Families, frequent doctor visits</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">HDHP + HSA</td><td style="padding:8px;border:1px solid #ddd">$85/mo</td><td style="padding:8px;border:1px solid #ddd">$3,000</td><td style="padding:8px;border:1px solid #ddd">Low utilization, tax savings</td></tr>
</table>
<p>Open enrollment happens each November. You can also make changes during qualifying life events (marriage, birth, etc.).</p>

<h3>Retirement Plans</h3>
<ul>
  <li><strong>401(k):</strong> The company matches <strong>100% of the first 4%</strong> of your salary that you contribute.</li>
  <li><strong>Vesting Schedule:</strong> You are fully vested after 3 years of service.</li>
  <li><strong>Investment Options:</strong> Choose from target-date funds, index funds, and self-directed accounts.</li>
  <li><strong>Roth 401(k):</strong> Also available for after-tax contributions.</li>
</ul>

<h3>Additional Benefits</h3>
<ul>
  <li>🦷 <strong>Dental & Vision:</strong> Included with all health plans at no extra cost.</li>
  <li>🧠 <strong>Mental Health:</strong> Free access to an Employee Assistance Program (EAP) with 12 counseling sessions/year.</li>
  <li>🏋️ <strong>Wellness:</strong> $500 annual wellness stipend for gym, fitness classes, or equipment.</li>
  <li>📚 <strong>Education:</strong> $5,000/year tuition reimbursement for approved programs.</li>
  <li>🚌 <strong>Commuter:</strong> Pre-tax transit and parking benefits.</li>
</ul>

<h3>💡 Key Takeaway</h3>
<p>Take full advantage of your benefits — especially the 401(k) match. It's essentially free money toward your retirement.</p>
""",

("course-hr-101", 1): """
<h2>Time Off & Leave Policies</h2>

<h3>🎯 Learning Objectives</h3>
<ul>
  <li>Understand PTO accrual and usage policies</li>
  <li>Know the different types of leave available</li>
  <li>Follow the proper time-off request process</li>
</ul>

<h3>Paid Time Off (PTO)</h3>
<table style="width:100%;border-collapse:collapse;margin:12px 0">
  <tr style="background:#f0f0f0"><th style="padding:8px;border:1px solid #ddd">Tenure</th><th style="padding:8px;border:1px solid #ddd">Annual PTO</th><th style="padding:8px;border:1px solid #ddd">Accrual Rate</th></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">0-2 years</td><td style="padding:8px;border:1px solid #ddd">15 days</td><td style="padding:8px;border:1px solid #ddd">1.25 days/month</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">3-5 years</td><td style="padding:8px;border:1px solid #ddd">20 days</td><td style="padding:8px;border:1px solid #ddd">1.67 days/month</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">5+ years</td><td style="padding:8px;border:1px solid #ddd">25 days</td><td style="padding:8px;border:1px solid #ddd">2.08 days/month</td></tr>
</table>
<p>PTO can be carried over up to <strong>5 days</strong> into the next year. Unused days beyond 5 are forfeited.</p>

<h3>Types of Leave</h3>
<ul>
  <li><strong>Sick Leave:</strong> 10 days/year for illness, medical appointments, or caring for a family member.</li>
  <li><strong>Parental Leave:</strong> 12 weeks paid (birthing parent) / 6 weeks paid (non-birthing parent).</li>
  <li><strong>Bereavement:</strong> Up to 5 days for immediate family; 3 days for extended family.</li>
  <li><strong>Jury Duty:</strong> Paid leave for the duration of service.</li>
  <li><strong>Remote Work:</strong> Up to 3 days/week with manager approval.</li>
  <li><strong>Sabbatical:</strong> 4 weeks paid after 7 years of continuous service.</li>
</ul>

<h3>Requesting Time Off</h3>
<ol>
  <li>Submit your request through the <strong>HR Portal</strong> at least 2 weeks in advance for planned absences.</li>
  <li>For urgent/sick leave, notify your manager directly and submit the request within 24 hours.</li>
  <li>Your manager will approve or discuss alternative dates within 3 business days.</li>
  <li>Long absences (3+ weeks) require HR approval in addition to manager approval.</li>
</ol>

<h3>💡 Key Takeaway</h3>
<p>Use your time off! Rest and recovery are essential for sustained high performance. Plan ahead and communicate with your team.</p>
""",

("course-hr-101", 2): """
<h2>Professional Development</h2>

<h3>🎯 Learning Objectives</h3>
<ul>
  <li>Understand the company's investment in your growth</li>
  <li>Access training resources and development programs</li>
  <li>Create a personal career development plan</li>
</ul>

<h3>Our Commitment to Growth</h3>
<p>We believe that investing in our employees is investing in our future. Every team member has access to:</p>

<h3>Training & Education Budget</h3>
<ul>
  <li><strong>$5,000/year</strong> tuition reimbursement for degree programs, certifications, and courses.</li>
  <li><strong>$1,500/year</strong> conference and workshop budget.</li>
  <li><strong>Unlimited access</strong> to our online learning platform (LinkedIn Learning, Coursera, Udemy for Business).</li>
  <li><strong>Internal lunch-and-learns</strong> hosted monthly by subject matter experts.</li>
</ul>

<h3>Career Paths</h3>
<p>We offer two career tracks:</p>
<table style="width:100%;border-collapse:collapse;margin:12px 0">
  <tr style="background:#f0f0f0"><th style="padding:8px;border:1px solid #ddd">Management Track</th><th style="padding:8px;border:1px solid #ddd">Individual Contributor Track</th></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">Team Lead → Manager → Senior Manager → Director → VP</td><td style="padding:8px;border:1px solid #ddd">Specialist → Senior → Staff → Principal → Fellow</td></tr>
</table>
<p>Both tracks are equally valued and compensated. You choose the path that matches your interests and strengths.</p>

<h3>Creating Your Development Plan</h3>
<ol>
  <li><strong>Self-Assessment:</strong> What are your strengths? What skills do you want to develop?</li>
  <li><strong>Career Goals:</strong> Where do you want to be in 1 year? 3 years? 5 years?</li>
  <li><strong>Action Items:</strong> Courses, certifications, stretch assignments, mentoring.</li>
  <li><strong>Review with Manager:</strong> Discuss your plan in your next 1-on-1.</li>
  <li><strong>Track Progress:</strong> Review quarterly and adjust as needed.</li>
</ol>

<h3>💡 Key Takeaway</h3>
<p>Your career is in your hands. Use the resources available, be proactive about learning, and don't hesitate to ask for new challenges.</p>
""",

("course-hr-101", 3): """
<h2>Workplace Culture</h2>

<h3>🎯 Learning Objectives</h3>
<ul>
  <li>Understand and embody our core values</li>
  <li>Champion diversity, equity, and inclusion</li>
  <li>Participate in team-building and community initiatives</li>
</ul>

<h3>Our Core Values</h3>
<ol>
  <li><strong>Innovation:</strong> We encourage creative thinking and are not afraid to fail forward.</li>
  <li><strong>Integrity:</strong> We do the right thing, even when no one is watching.</li>
  <li><strong>Collaboration:</strong> We achieve more together than we ever could alone.</li>
  <li><strong>Excellence:</strong> We hold ourselves to the highest standards in everything we do.</li>
  <li><strong>Empathy:</strong> We listen first, judge less, and support always.</li>
</ol>

<h3>Diversity, Equity & Inclusion (DEI)</h3>
<p>We are committed to building a workplace where everyone feels valued and included:</p>
<ul>
  <li><strong>Employee Resource Groups (ERGs):</strong> Join groups for women, LGBTQ+, veterans, parents, and more.</li>
  <li><strong>Inclusive Hiring:</strong> Structured interviews and diverse hiring panels reduce bias.</li>
  <li><strong>Pay Equity:</strong> Annual reviews ensure fair compensation across demographics.</li>
  <li><strong>Accessibility:</strong> Our offices and digital tools are designed to be accessible to all.</li>
  <li><strong>Unconscious Bias Training:</strong> Required annually for all people managers.</li>
</ul>

<h3>Getting Involved</h3>
<ul>
  <li>🎉 <strong>Social Events:</strong> Monthly happy hours, holiday parties, team outings.</li>
  <li>🤝 <strong>Volunteering:</strong> 2 paid volunteer days per year for the charity of your choice.</li>
  <li>💡 <strong>Innovation Days:</strong> Quarterly hackathons to work on creative projects.</li>
  <li>🏃 <strong>Wellness Challenges:</strong> Step challenges, meditation groups, and fitness classes.</li>
</ul>

<h3>💡 Key Takeaway</h3>
<p>Culture isn't just posters on the wall — it's how we treat each other every day. Be the culture you want to see.</p>
""",

# ═══════════════════════════════════════════════════════════════════════════
# CUSTOMER RELATIONS EXCELLENCE
# ═══════════════════════════════════════════════════════════════════════════
("course-customer-201", 0): """
<h2>Client Communication Standards</h2>

<h3>🎯 Learning Objectives</h3>
<ul>
  <li>Apply professional communication standards across all channels</li>
  <li>Structure emails and messages for maximum clarity</li>
  <li>Handle difficult communications with grace</li>
</ul>

<h3>Communication Channels</h3>
<table style="width:100%;border-collapse:collapse;margin:12px 0">
  <tr style="background:#f0f0f0"><th style="padding:8px;border:1px solid #ddd">Channel</th><th style="padding:8px;border:1px solid #ddd">Best For</th><th style="padding:8px;border:1px solid #ddd">Response Time</th></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">Email</td><td style="padding:8px;border:1px solid #ddd">Formal requests, documentation, follow-ups</td><td style="padding:8px;border:1px solid #ddd">Within 4 business hours</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">Phone</td><td style="padding:8px;border:1px solid #ddd">Urgent issues, complex discussions</td><td style="padding:8px;border:1px solid #ddd">Answer within 3 rings</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">Video Call</td><td style="padding:8px;border:1px solid #ddd">Presentations, relationship building</td><td style="padding:8px;border:1px solid #ddd">Scheduled in advance</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd">Chat</td><td style="padding:8px;border:1px solid #ddd">Quick questions, informal updates</td><td style="padding:8px;border:1px solid #ddd">Within 30 minutes</td></tr>
</table>

<h3>Email Best Practices</h3>
<ol>
  <li><strong>Subject Line:</strong> Be specific — "Q3 Budget Review — Action Needed by Friday"</li>
  <li><strong>Greeting:</strong> Always professional — "Dear [Name]" or "Hi [Name]"</li>
  <li><strong>Body:</strong> Lead with the ask or key point. Use bullet points for clarity.</li>
  <li><strong>Closing:</strong> Include clear next steps and deadlines.</li>
  <li><strong>Signature:</strong> Use your company signature with title and contact info.</li>
</ol>

<h3>Handling Difficult Communications</h3>
<ul>
  <li><strong>Stay Professional:</strong> Never respond emotionally, even if the client is upset.</li>
  <li><strong>Acknowledge:</strong> "I understand your frustration, and I'm here to help."</li>
  <li><strong>Focus on Solutions:</strong> Redirect the conversation toward resolution.</li>
  <li><strong>Escalate When Needed:</strong> If you can't resolve it, bring in your manager — not as a failure, but as a resource.</li>
</ul>

<h3>💡 Key Takeaway</h3>
<p>Every communication is a reflection of our brand. Be prompt, be professional, and always put the client first.</p>
""",

("course-customer-201", 1): """
<h2>Service Level Agreements</h2>

<h3>🎯 Learning Objectives</h3>
<ul>
  <li>Understand what SLAs are and why they matter</li>
  <li>Know our standard SLA tiers and response commitments</li>
  <li>Monitor and report on SLA compliance</li>
</ul>

<h3>What Is an SLA?</h3>
<p>A <strong>Service Level Agreement</strong> is a contract between our organization and the client that defines the expected level of service, including response times, resolution times, and quality standards.</p>

<h3>Our SLA Tiers</h3>
<table style="width:100%;border-collapse:collapse;margin:12px 0">
  <tr style="background:#f0f0f0"><th style="padding:8px;border:1px solid #ddd">Priority</th><th style="padding:8px;border:1px solid #ddd">Description</th><th style="padding:8px;border:1px solid #ddd">Response Time</th><th style="padding:8px;border:1px solid #ddd">Resolution Time</th></tr>
  <tr><td style="padding:8px;border:1px solid #ddd;background:#ffebee"><strong>P1 - Critical</strong></td><td style="padding:8px;border:1px solid #ddd">Service down, revenue impact</td><td style="padding:8px;border:1px solid #ddd">15 minutes</td><td style="padding:8px;border:1px solid #ddd">4 hours</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd;background:#fff3e0"><strong>P2 - High</strong></td><td style="padding:8px;border:1px solid #ddd">Major feature broken, workaround exists</td><td style="padding:8px;border:1px solid #ddd">1 hour</td><td style="padding:8px;border:1px solid #ddd">8 hours</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd;background:#e3f2fd"><strong>P3 - Medium</strong></td><td style="padding:8px;border:1px solid #ddd">Minor issue, no business impact</td><td style="padding:8px;border:1px solid #ddd">4 hours</td><td style="padding:8px;border:1px solid #ddd">48 hours</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd"><strong>P4 - Low</strong></td><td style="padding:8px;border:1px solid #ddd">Cosmetic, enhancement request</td><td style="padding:8px;border:1px solid #ddd">1 business day</td><td style="padding:8px;border:1px solid #ddd">5 business days</td></tr>
</table>

<h3>SLA Compliance</h3>
<p>Our target is <strong>99.5% SLA compliance</strong> across all tiers. SLA breaches trigger:</p>
<ul>
  <li>Automatic escalation to the team lead</li>
  <li>Root cause analysis within 24 hours</li>
  <li>Client notification and remediation plan</li>
  <li>Service credits for Enterprise clients per contract terms</li>
</ul>

<h3>Your Role</h3>
<ul>
  <li>Acknowledge client requests promptly — even if you can't resolve immediately.</li>
  <li>Accurately categorize priority levels.</li>
  <li>Update the ticket with progress notes at regular intervals.</li>
  <li>Escalate before an SLA breach, not after.</li>
</ul>

<h3>💡 Key Takeaway</h3>
<p>SLAs are promises to our clients. Meeting them builds trust; breaking them erodes it. Own your response times.</p>
""",

("course-customer-201", 2): """
<h2>Handling Complaints</h2>

<h3>🎯 Learning Objectives</h3>
<ul>
  <li>Apply de-escalation techniques to defuse tense situations</li>
  <li>Turn complaints into opportunities for improvement</li>
  <li>Follow the complaint resolution framework</li>
</ul>

<h3>Why Complaints Are Valuable</h3>
<p>For every customer who complains, there are <strong>26 who remain silent</strong> and may never come back. Complaints are a gift — they tell you exactly where to improve.</p>

<h3>The HEARD Framework</h3>
<p>Use the <strong>HEARD</strong> method to resolve complaints effectively:</p>
<ol>
  <li><strong>H — Hear:</strong> Let the customer speak without interrupting. Take notes.</li>
  <li><strong>E — Empathize:</strong> "I completely understand why that would be frustrating."</li>
  <li><strong>A — Apologize:</strong> "I'm sorry you've had this experience." (Not "I'm sorry you feel that way.")</li>
  <li><strong>R — Resolve:</strong> Offer a concrete solution. Give options when possible.</li>
  <li><strong>D — Diagnose:</strong> After resolution, identify the root cause to prevent recurrence.</li>
</ol>

<h3>De-Escalation Techniques</h3>
<ul>
  <li><strong>Lower your voice</strong> — matching their volume escalates the situation.</li>
  <li><strong>Use their name</strong> — it personalizes the interaction.</li>
  <li><strong>Avoid "but"</strong> — replace with "and" ("I hear you, and here's what I can do…").</li>
  <li><strong>Focus on what you CAN do</strong>, not what you can't.</li>
  <li><strong>Set boundaries calmly</strong> — "I want to help you, and I need us to have a respectful conversation to do that."</li>
</ul>

<h3>When to Escalate</h3>
<ul>
  <li>The customer requests a manager</li>
  <li>The issue exceeds your authority to resolve</li>
  <li>The complaint involves a safety or legal concern</li>
  <li>Multiple complaints about the same issue are received</li>
</ul>

<h3>💡 Key Takeaway</h3>
<p>A well-handled complaint can create a more loyal customer than one who never had a problem in the first place.</p>
""",

("course-customer-201", 3): """
<h2>Account Management</h2>

<h3>🎯 Learning Objectives</h3>
<ul>
  <li>Build and maintain long-term client relationships</li>
  <li>Conduct effective account reviews</li>
  <li>Identify upsell and cross-sell opportunities</li>
</ul>

<h3>The Account Manager's Role</h3>
<p>As an account manager, you are the <strong>bridge between the client and the company</strong>. Your responsibilities include:</p>
<ul>
  <li>Being the primary point of contact for assigned accounts</li>
  <li>Understanding the client's business goals and challenges</li>
  <li>Ensuring service delivery meets or exceeds expectations</li>
  <li>Identifying growth opportunities and renewals</li>
</ul>

<h3>Conducting Quarterly Business Reviews (QBRs)</h3>
<ol>
  <li><strong>Prepare:</strong> Gather usage data, support metrics, and satisfaction scores.</li>
  <li><strong>Review Performance:</strong> Share SLA compliance, key metrics, and achievements.</li>
  <li><strong>Discuss Challenges:</strong> Proactively address any concerns or open issues.</li>
  <li><strong>Align on Goals:</strong> Understand their evolving needs for the next quarter.</li>
  <li><strong>Present Opportunities:</strong> Introduce relevant new features, services, or upgrades.</li>
  <li><strong>Follow Up:</strong> Send a written summary with action items within 48 hours.</li>
</ol>

<h3>Client Health Score</h3>
<table style="width:100%;border-collapse:collapse;margin:12px 0">
  <tr style="background:#f0f0f0"><th style="padding:8px;border:1px solid #ddd">Score</th><th style="padding:8px;border:1px solid #ddd">Health</th><th style="padding:8px;border:1px solid #ddd">Action</th></tr>
  <tr><td style="padding:8px;border:1px solid #ddd;background:#e8f5e9">80-100</td><td style="padding:8px;border:1px solid #ddd">🟢 Healthy</td><td style="padding:8px;border:1px solid #ddd">Nurture and grow</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd;background:#fff3e0">50-79</td><td style="padding:8px;border:1px solid #ddd">🟡 At Risk</td><td style="padding:8px;border:1px solid #ddd">Increase touchpoints, address concerns</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd;background:#ffebee">0-49</td><td style="padding:8px;border:1px solid #ddd">🔴 Critical</td><td style="padding:8px;border:1px solid #ddd">Executive-level intervention, recovery plan</td></tr>
</table>

<h3>💡 Key Takeaway</h3>
<p>Retention is more valuable than acquisition. A well-managed account becomes a reference, a referral source, and a long-term revenue stream.</p>
""",

("course-customer-201", 4): """
<h2>Negotiation Skills</h2>

<h3>🎯 Learning Objectives</h3>
<ul>
  <li>Prepare effectively for negotiations</li>
  <li>Apply win-win negotiation strategies</li>
  <li>Close deals confidently and professionally</li>
</ul>

<h3>Preparation Is Everything</h3>
<p>80% of negotiation success happens before the conversation. Prepare by:</p>
<ol>
  <li><strong>Know Your BATNA:</strong> Best Alternative To a Negotiated Agreement — what will you do if this deal falls through?</li>
  <li><strong>Research the Other Side:</strong> Understand their priorities, constraints, and decision-making process.</li>
  <li><strong>Set Your Range:</strong> Define your ideal outcome, acceptable range, and walk-away point.</li>
  <li><strong>Anticipate Objections:</strong> Prepare responses to likely concerns or pushback.</li>
</ol>

<h3>Win-Win Strategies</h3>
<ul>
  <li><strong>Focus on Interests, Not Positions:</strong> "I need a lower price" is a position. "I need to stay within budget" is an interest — and there may be creative ways to address it.</li>
  <li><strong>Create Value:</strong> Look for trades — "If we extend the contract term, can we include premium support at no extra cost?"</li>
  <li><strong>Use Silence:</strong> After making an offer, be comfortable with silence. Let the other side respond.</li>
  <li><strong>Anchor High (or Low):</strong> The first number on the table often anchors the entire negotiation.</li>
  <li><strong>Bundle and Unbundle:</strong> Package items together for perceived value, or separate them to isolate concessions.</li>
</ul>

<h3>Closing Techniques</h3>
<table style="width:100%;border-collapse:collapse;margin:12px 0">
  <tr style="background:#f0f0f0"><th style="padding:8px;border:1px solid #ddd">Technique</th><th style="padding:8px;border:1px solid #ddd">Example</th></tr>
  <tr><td style="padding:8px;border:1px solid #ddd"><strong>Summary Close</strong></td><td style="padding:8px;border:1px solid #ddd">"So to recap, we've agreed on X, Y, and Z. Shall we proceed?"</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd"><strong>Assumptive Close</strong></td><td style="padding:8px;border:1px solid #ddd">"When would you like implementation to start?"</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd"><strong>Urgency Close</strong></td><td style="padding:8px;border:1px solid #ddd">"This pricing is available through the end of the quarter."</td></tr>
  <tr><td style="padding:8px;border:1px solid #ddd"><strong>Trial Close</strong></td><td style="padding:8px;border:1px solid #ddd">"If we can address that concern, would you be ready to move forward?"</td></tr>
</table>

<h3>💡 Key Takeaway</h3>
<p>The best negotiators aren't the toughest — they're the most prepared. Focus on creating value for both sides, and the deal will follow.</p>
""",

}

# ── Main ────────────────────────────────────────────────────────────────────

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
    print(f"\nDone — updated {updated} modules with rich content.")


if __name__ == "__main__":
    main()
