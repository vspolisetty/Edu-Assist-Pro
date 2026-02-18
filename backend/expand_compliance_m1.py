"""
Expand Module 1: Data Privacy & GDPR (~35K chars target)
"""
import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), "courses.db")

CONTENT = """
<h2>Data Privacy & GDPR Compliance</h2>

<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:20px 0;background:linear-gradient(135deg,#7c3aed08,#7c3aed03);border-radius:12px;padding:16px">
  <div style="text-align:center;padding:16px"><div style="font-size:32px">🔒</div><div style="font-size:1.5rem;font-weight:700;color:#7c3aed">€20M</div><div style="font-size:.8rem;color:#64748b">Max GDPR Fine</div></div>
  <div style="text-align:center;padding:16px"><div style="font-size:32px">📊</div><div style="font-size:1.5rem;font-weight:700;color:#7c3aed">4%</div><div style="font-size:.8rem;color:#64748b">Revenue Penalty</div></div>
  <div style="text-align:center;padding:16px"><div style="font-size:32px">🌍</div><div style="font-size:1.5rem;font-weight:700;color:#7c3aed">27+</div><div style="font-size:.8rem;color:#64748b">EU Countries</div></div>
  <div style="text-align:center;padding:16px"><div style="font-size:32px">⏱️</div><div style="font-size:1.5rem;font-weight:700;color:#7c3aed">72h</div><div style="font-size:.8rem;color:#64748b">Breach Notification</div></div>
</div>

<img src="https://images.unsplash.com/photo-1563986768609-322da13575f3?w=800&h=400&fit=crop" alt="Data privacy and security concept" style="width:100%;border-radius:12px;margin:20px 0;box-shadow:0 4px 12px rgba(0,0,0,0.1)">

<h3>🎯 Learning Objectives</h3>
<p>By the end of this module, you will be able to:</p>
<ul>
  <li>Define personal data and understand its various categories under GDPR</li>
  <li>Apply the 7 GDPR principles to your daily work activities</li>
  <li>Identify the 6 lawful bases for processing personal data</li>
  <li>Explain data subject rights and how to respond to requests</li>
  <li>Recognize data breaches and follow the 72-hour notification timeline</li>
  <li>Implement Privacy by Design in your projects and processes</li>
</ul>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>📚 What Is Data Privacy?</h3>

<p>Data privacy is the <strong>fundamental right of individuals to control how their personal information is collected, used, stored, and shared</strong>. In our increasingly digital world, personal data has become one of the most valuable commodities — and one of the most targeted by malicious actors.</p>

<p>Data privacy is not just about compliance — it's about:</p>
<ul>
  <li><strong>Trust:</strong> Customers share data because they trust us to protect it</li>
  <li><strong>Reputation:</strong> A single breach can destroy decades of brand building</li>
  <li><strong>Legal obligation:</strong> Non-compliance carries severe financial and criminal penalties</li>
  <li><strong>Ethical responsibility:</strong> We have a moral duty to protect people's information</li>
  <li><strong>Competitive advantage:</strong> Strong privacy practices differentiate us in the market</li>
</ul>

<div style="background:linear-gradient(135deg,#ef444408,#ef444403);border-left:4px solid #ef4444;padding:20px 24px;margin:24px 0;border-radius:0 10px 10px 0">
  <strong style="display:flex;align-items:center;gap:8px;margin-bottom:8px">⚠️ The Stakes Are Real</strong>
  <div style="font-size:.92rem;line-height:1.7">In 2023, <strong>Meta (Facebook)</strong> was fined <strong>€1.2 billion</strong> by the Irish Data Protection Commission — the largest GDPR fine ever issued. Amazon was fined €746 million, and WhatsApp €225 million. These aren't just headlines — they're warnings that regulators are serious about enforcement.</div>
</div>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>🔍 What Is Personal Data?</h3>

<p>Under GDPR, personal data is defined as <strong>any information that can identify a living person, either directly or indirectly</strong>. This definition is intentionally broad and includes much more than most people realize.</p>

<h4>Categories of Personal Data</h4>

<table style="width:100%;border-collapse:collapse;margin:16px 0">
  <tr style="background:#f8fafc"><th style="padding:12px 16px;text-align:left;border:1px solid #e2e8f0">Category</th><th style="padding:12px 16px;text-align:left;border:1px solid #e2e8f0">Examples</th><th style="padding:12px 16px;text-align:left;border:1px solid #e2e8f0">Sensitivity</th><th style="padding:12px 16px;text-align:left;border:1px solid #e2e8f0">Special Handling</th></tr>
  <tr><td style="padding:12px;border:1px solid #e2e8f0"><strong>Basic Identity</strong></td><td style="padding:12px;border:1px solid #e2e8f0">Name, email, phone, address, date of birth</td><td style="padding:12px;border:1px solid #e2e8f0">Standard</td><td style="padding:12px;border:1px solid #e2e8f0">Standard controls</td></tr>
  <tr><td style="padding:12px;border:1px solid #e2e8f0"><strong>Online Identifiers</strong></td><td style="padding:12px;border:1px solid #e2e8f0">IP address, cookies, device IDs, browser fingerprints</td><td style="padding:12px;border:1px solid #e2e8f0">Standard</td><td style="padding:12px;border:1px solid #e2e8f0">Cookie consent required</td></tr>
  <tr><td style="padding:12px;border:1px solid #e2e8f0"><strong>Financial</strong></td><td style="padding:12px;border:1px solid #e2e8f0">Bank details, salary, credit score, tax ID</td><td style="padding:12px;border:1px solid #e2e8f0">High</td><td style="padding:12px;border:1px solid #e2e8f0">Encryption required</td></tr>
  <tr><td style="padding:12px;border:1px solid #e2e8f0"><strong>Employment</strong></td><td style="padding:12px;border:1px solid #e2e8f0">CV, performance reviews, disciplinary records</td><td style="padding:12px;border:1px solid #e2e8f0">High</td><td style="padding:12px;border:1px solid #e2e8f0">Access restrictions</td></tr>
  <tr style="background:#fef2f2"><td style="padding:12px;border:1px solid #e2e8f0"><strong>🔴 Health Data</strong></td><td style="padding:12px;border:1px solid #e2e8f0">Medical records, prescriptions, insurance claims</td><td style="padding:12px;border:1px solid #e2e8f0">Special Category</td><td style="padding:12px;border:1px solid #e2e8f0">Explicit consent + extra safeguards</td></tr>
  <tr style="background:#fef2f2"><td style="padding:12px;border:1px solid #e2e8f0"><strong>🔴 Biometric</strong></td><td style="padding:12px;border:1px solid #e2e8f0">Fingerprints, facial recognition, voice patterns</td><td style="padding:12px;border:1px solid #e2e8f0">Special Category</td><td style="padding:12px;border:1px solid #e2e8f0">Explicit consent + extra safeguards</td></tr>
  <tr style="background:#fef2f2"><td style="padding:12px;border:1px solid #e2e8f0"><strong>🔴 Political/Religious</strong></td><td style="padding:12px;border:1px solid #e2e8f0">Political opinions, religious beliefs, union membership</td><td style="padding:12px;border:1px solid #e2e8f0">Special Category</td><td style="padding:12px;border:1px solid #e2e8f0">Generally prohibited</td></tr>
  <tr style="background:#fef2f2"><td style="padding:12px;border:1px solid #e2e8f0"><strong>🔴 Genetic</strong></td><td style="padding:12px;border:1px solid #e2e8f0">DNA analysis, genetic predispositions</td><td style="padding:12px;border:1px solid #e2e8f0">Special Category</td><td style="padding:12px;border:1px solid #e2e8f0">Explicit consent + extra safeguards</td></tr>
</table>

<div style="background:linear-gradient(135deg,#3b82f608,#3b82f603);border-left:4px solid #3b82f6;padding:20px 24px;margin:24px 0;border-radius:0 10px 10px 0">
  <strong style="display:flex;align-items:center;gap:8px;margin-bottom:8px">💡 Key Insight: Data Combination</strong>
  <div style="font-size:.92rem;line-height:1.7">Even data that seems harmless on its own can become personal data when combined. For example: <strong>Job title + Department + Office location</strong> might uniquely identify one person in the organization. This is called "indirect identification" and is covered by GDPR.</div>
</div>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>📜 The 7 GDPR Principles</h3>

<p>Every data processing activity must comply with these seven fundamental principles. Think of them as the "Seven Commandments" of data protection:</p>

<img src="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=350&fit=crop" alt="Legal documents and compliance" style="width:100%;border-radius:12px;margin:20px 0;box-shadow:0 4px 12px rgba(0,0,0,0.1)">

<div style="display:grid;grid-template-columns:1fr;gap:16px;margin:24px 0">
  <div style="background:#f8fafc;border-left:4px solid #1a3a5c;padding:20px 24px;border-radius:0 10px 10px 0">
    <strong style="font-size:1.1rem;color:#1a3a5c">1️⃣ Lawfulness, Fairness & Transparency</strong>
    <p style="margin:10px 0 0;line-height:1.7">You must have a valid legal basis for processing data. Be open and honest with people about what you do with their data. No hidden processing or deceptive practices.</p>
  </div>
  <div style="background:#f8fafc;border-left:4px solid #2c7a7b;padding:20px 24px;border-radius:0 10px 10px 0">
    <strong style="font-size:1.1rem;color:#2c7a7b">2️⃣ Purpose Limitation</strong>
    <p style="margin:10px 0 0;line-height:1.7">Only collect data for specific, stated purposes. Don't repurpose data without obtaining new consent or having another lawful basis. "Just in case" collection is not allowed.</p>
  </div>
  <div style="background:#f8fafc;border-left:4px solid #7c3aed;padding:20px 24px;border-radius:0 10px 10px 0">
    <strong style="font-size:1.1rem;color:#7c3aed">3️⃣ Data Minimization</strong>
    <p style="margin:10px 0 0;line-height:1.7">Collect only what you need — nothing more. Ask yourself: "Do I really need this field?" If the answer is "maybe someday," the answer is no.</p>
  </div>
  <div style="background:#f8fafc;border-left:4px solid #dc2626;padding:20px 24px;border-radius:0 10px 10px 0">
    <strong style="font-size:1.1rem;color:#dc2626">4️⃣ Accuracy</strong>
    <p style="margin:10px 0 0;line-height:1.7">Keep data up to date. Delete or correct inaccurate records promptly. Provide mechanisms for people to update their information.</p>
  </div>
  <div style="background:#f8fafc;border-left:4px solid #ea580c;padding:20px 24px;border-radius:0 10px 10px 0">
    <strong style="font-size:1.1rem;color:#ea580c">5️⃣ Storage Limitation</strong>
    <p style="margin:10px 0 0;line-height:1.7">Don't keep data longer than necessary. Define and enforce retention periods. When data is no longer needed, delete it securely.</p>
  </div>
  <div style="background:#f8fafc;border-left:4px solid #16a34a;padding:20px 24px;border-radius:0 10px 10px 0">
    <strong style="font-size:1.1rem;color:#16a34a">6️⃣ Integrity & Confidentiality</strong>
    <p style="margin:10px 0 0;line-height:1.7">Protect data with appropriate technical and organizational measures. This includes encryption, access controls, regular security testing, and employee training.</p>
  </div>
  <div style="background:#f8fafc;border-left:4px solid #0891b2;padding:20px 24px;border-radius:0 10px 10px 0">
    <strong style="font-size:1.1rem;color:#0891b2">7️⃣ Accountability</strong>
    <p style="margin:10px 0 0;line-height:1.7">Be able to demonstrate compliance. Document your processes, maintain records of processing activities, and conduct regular audits. "We think we're compliant" is not enough — prove it.</p>
  </div>
</div>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>⚖️ The 6 Lawful Bases for Processing</h3>

<p>Before processing any personal data, you must identify at least ONE lawful basis. Choosing the correct basis is critical because it affects the rights available to data subjects.</p>

<table style="width:100%;border-collapse:collapse;margin:16px 0">
  <tr style="background:#f8fafc"><th style="padding:12px;text-align:left;border:1px solid #e2e8f0">Lawful Basis</th><th style="padding:12px;text-align:left;border:1px solid #e2e8f0">When to Use</th><th style="padding:12px;text-align:left;border:1px solid #e2e8f0">Example</th><th style="padding:12px;text-align:left;border:1px solid #e2e8f0">Withdrawal Rights</th></tr>
  <tr><td style="padding:12px;border:1px solid #e2e8f0"><strong>1. Consent</strong></td><td style="padding:12px;border:1px solid #e2e8f0">Individual freely agrees</td><td style="padding:12px;border:1px solid #e2e8f0">Marketing email opt-in</td><td style="padding:12px;border:1px solid #e2e8f0">Can withdraw anytime</td></tr>
  <tr><td style="padding:12px;border:1px solid #e2e8f0"><strong>2. Contract</strong></td><td style="padding:12px;border:1px solid #e2e8f0">Needed to fulfill a contract</td><td style="padding:12px;border:1px solid #e2e8f0">Processing employee payroll</td><td style="padding:12px;border:1px solid #e2e8f0">Limited withdrawal</td></tr>
  <tr><td style="padding:12px;border:1px solid #e2e8f0"><strong>3. Legal Obligation</strong></td><td style="padding:12px;border:1px solid #e2e8f0">Required by law</td><td style="padding:12px;border:1px solid #e2e8f0">Tax reporting to government</td><td style="padding:12px;border:1px solid #e2e8f0">Cannot withdraw</td></tr>
  <tr><td style="padding:12px;border:1px solid #e2e8f0"><strong>4. Vital Interests</strong></td><td style="padding:12px;border:1px solid #e2e8f0">Protect someone's life</td><td style="padding:12px;border:1px solid #e2e8f0">Emergency medical situation</td><td style="padding:12px;border:1px solid #e2e8f0">Rarely applicable</td></tr>
  <tr><td style="padding:12px;border:1px solid #e2e8f0"><strong>5. Public Task</strong></td><td style="padding:12px;border:1px solid #e2e8f0">Official authority</td><td style="padding:12px;border:1px solid #e2e8f0">Government agency processing</td><td style="padding:12px;border:1px solid #e2e8f0">Can object</td></tr>
  <tr><td style="padding:12px;border:1px solid #e2e8f0"><strong>6. Legitimate Interest</strong></td><td style="padding:12px;border:1px solid #e2e8f0">Business need, balanced with rights</td><td style="padding:12px;border:1px solid #e2e8f0">Fraud prevention analytics</td><td style="padding:12px;border:1px solid #e2e8f0">Can object</td></tr>
</table>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>👤 Individual Rights Under GDPR</h3>

<p>Data subjects (the people whose data we process) have powerful rights under GDPR. We must respond to these requests within specific timeframes:</p>

<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:16px;margin:24px 0">
  <div style="background:#fff;border:2px solid #e2e8f0;padding:20px;border-radius:12px">
    <div style="font-size:28px;margin-bottom:8px">📋</div>
    <strong>Right of Access (Art. 15)</strong>
    <p style="font-size:.85rem;color:#64748b;margin:8px 0">"What data do you hold about me?"</p>
    <p style="font-size:.8rem;margin:0;padding:8px;background:#f8fafc;border-radius:6px"><strong>Response time:</strong> 30 days</p>
  </div>
  <div style="background:#fff;border:2px solid #e2e8f0;padding:20px;border-radius:12px">
    <div style="font-size:28px;margin-bottom:8px">✏️</div>
    <strong>Right to Rectification (Art. 16)</strong>
    <p style="font-size:.85rem;color:#64748b;margin:8px 0">"Fix my incorrect data"</p>
    <p style="font-size:.8rem;margin:0;padding:8px;background:#f8fafc;border-radius:6px"><strong>Response time:</strong> Without undue delay</p>
  </div>
  <div style="background:#fff;border:2px solid #e2e8f0;padding:20px;border-radius:12px">
    <div style="font-size:28px;margin-bottom:8px">🗑️</div>
    <strong>Right to Erasure (Art. 17)</strong>
    <p style="font-size:.85rem;color:#64748b;margin:8px 0">"Delete my data" (Right to be Forgotten)</p>
    <p style="font-size:.8rem;margin:0;padding:8px;background:#f8fafc;border-radius:6px"><strong>Response time:</strong> Without undue delay</p>
  </div>
  <div style="background:#fff;border:2px solid #e2e8f0;padding:20px;border-radius:12px">
    <div style="font-size:28px;margin-bottom:8px">⏸️</div>
    <strong>Right to Restrict (Art. 18)</strong>
    <p style="font-size:.85rem;color:#64748b;margin:8px 0">"Stop using my data but keep it"</p>
    <p style="font-size:.8rem;margin:0;padding:8px;background:#f8fafc;border-radius:6px"><strong>Response time:</strong> Without undue delay</p>
  </div>
  <div style="background:#fff;border:2px solid #e2e8f0;padding:20px;border-radius:12px">
    <div style="font-size:28px;margin-bottom:8px">📤</div>
    <strong>Right to Portability (Art. 20)</strong>
    <p style="font-size:.85rem;color:#64748b;margin:8px 0">"Give me my data in portable format"</p>
    <p style="font-size:.8rem;margin:0;padding:8px;background:#f8fafc;border-radius:6px"><strong>Response time:</strong> 30 days</p>
  </div>
  <div style="background:#fff;border:2px solid #e2e8f0;padding:20px;border-radius:12px">
    <div style="font-size:28px;margin-bottom:8px">🚫</div>
    <strong>Right to Object (Art. 21)</strong>
    <p style="font-size:.85rem;color:#64748b;margin:8px 0">"I don't want you to process my data"</p>
    <p style="font-size:.8rem;margin:0;padding:8px;background:#f8fafc;border-radius:6px"><strong>Response time:</strong> Without undue delay</p>
  </div>
</div>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>🚨 Data Breach Response</h3>

<img src="https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=800&h=350&fit=crop" alt="Cybersecurity breach alert" style="width:100%;border-radius:12px;margin:20px 0;box-shadow:0 4px 12px rgba(0,0,0,0.1)">

<p>A data breach is any event where personal data is accidentally or unlawfully accessed, altered, disclosed, or destroyed. Under GDPR Article 33, <strong>the supervisory authority must be notified within 72 hours</strong> of becoming aware of a breach that poses a risk to individuals' rights.</p>

<h4>The 72-Hour Timeline</h4>

<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:20px 0">
  <div style="background:linear-gradient(135deg,#ef4444,#dc2626);color:white;padding:20px;border-radius:12px;text-align:center">
    <div style="font-size:2rem;font-weight:700">0-1h</div>
    <div style="font-size:.85rem;margin-top:8px">Discover & Report to IT Security + DPO immediately</div>
  </div>
  <div style="background:linear-gradient(135deg,#f97316,#ea580c);color:white;padding:20px;border-radius:12px;text-align:center">
    <div style="font-size:2rem;font-weight:700">1-24h</div>
    <div style="font-size:.85rem;margin-top:8px">Initial assessment: What data? How many people? What risk?</div>
  </div>
  <div style="background:linear-gradient(135deg,#eab308,#ca8a04);color:white;padding:20px;border-radius:12px;text-align:center">
    <div style="font-size:2rem;font-weight:700">24-48h</div>
    <div style="font-size:.85rem;margin-top:8px">Containment & documentation; preserve evidence</div>
  </div>
  <div style="background:linear-gradient(135deg,#22c55e,#16a34a);color:white;padding:20px;border-radius:12px;text-align:center">
    <div style="font-size:2rem;font-weight:700">48-72h</div>
    <div style="font-size:.85rem;margin-top:8px">Official notification to supervisory authority</div>
  </div>
</div>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>🎭 Scenario-Based Exercise</h3>

<div style="background:#f1f5f9;border:1px solid #e2e8f0;padding:24px;margin:24px 0;border-radius:12px">
  <strong style="display:flex;align-items:center;gap:8px;margin-bottom:12px;font-size:1.1rem">🎯 Scenario: The Deletion Request</strong>
  <p style="margin:12px 0;font-style:italic;background:#fff;padding:16px;border-radius:8px;border-left:4px solid #3b82f6">"A customer emails you: 'I want all my data deleted from your systems immediately.' You check and find their data in the CRM, billing system, and old email threads."</p>
  <p style="margin:12px 0 8px;font-weight:600">What would you do?</p>
  <ul style="list-style:none;margin:0;padding:0">
    <li style="margin:6px 0;padding:10px 14px;background:#fff;border-radius:6px">⬜ A. Delete everything immediately from all systems</li>
    <li style="margin:6px 0;padding:10px 14px;background:#fff;border-radius:6px">✅ B. Acknowledge the request, verify identity, forward to DPO within 24 hours</li>
    <li style="margin:6px 0;padding:10px 14px;background:#fff;border-radius:6px">⬜ C. Tell them you can't delete data needed for legal compliance</li>
    <li style="margin:6px 0;padding:10px 14px;background:#fff;border-radius:6px">⬜ D. Ignore it — they probably don't understand GDPR</li>
  </ul>
  <details style="margin-top:16px">
    <summary style="cursor:pointer;color:#1a3a5c;font-weight:600;padding:8px;background:#e2e8f0;border-radius:6px">Show Answer & Explanation</summary>
    <div style="margin:12px 0;padding:16px;background:#fff;border-radius:8px;border-left:4px solid #22c55e">
      <p><strong>Correct: B. Acknowledge and forward to DPO.</strong></p>
      <p>Erasure requests must be handled carefully. Some data (like tax records) may need to be retained for legal reasons. The DPO will determine what can be deleted and respond within the 30-day deadline. You should acknowledge receipt to the customer, verify their identity, and immediately escalate to the DPO.</p>
    </div>
  </details>
</div>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>✅ Your Daily Data Privacy Checklist</h3>

<div style="background:#f8fafc;padding:24px;border-radius:12px;margin:20px 0">
  <ul style="margin:0;padding-left:0;list-style:none;line-height:2.2">
    <li>☑️ <strong>Lock your screen</strong> when leaving your desk (Win+L or Ctrl+Cmd+Q)</li>
    <li>☑️ <strong>Use encrypted email</strong> for sensitive information</li>
    <li>☑️ <strong>Verify the recipient</strong> before sending data — double-check email addresses</li>
    <li>☑️ <strong>Don't store personal data</strong> on USB drives or personal cloud storage</li>
    <li>☑️ <strong>Shred physical documents</strong> containing personal data</li>
    <li>☑️ <strong>Report suspected breaches</strong> to security@company.com within 1 hour</li>
    <li>☑️ <strong>Review and clean up</strong> old files containing personal data quarterly</li>
    <li>☑️ <strong>Use BCC</strong> when emailing groups to protect email addresses</li>
  </ul>
</div>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>💡 Key Takeaways</h3>

<div style="background:linear-gradient(135deg,#7c3aed,#6d28d9);color:white;padding:28px;border-radius:12px;margin:24px 0">
  <ul style="margin:0;padding-left:20px;line-height:2">
    <li>Personal data is <strong>broader than you think</strong> — even IP addresses count</li>
    <li>You need a <strong>lawful basis</strong> before collecting or processing any personal data</li>
    <li>Data subjects have <strong>7 powerful rights</strong> — respond within 30 days</li>
    <li>Report breaches <strong>immediately</strong> — the 72-hour clock starts when you become aware</li>
    <li>When in doubt, <strong>treat data as personal</strong> and handle with care</li>
    <li>Privacy is <strong>everyone's responsibility</strong>, not just the DPO's</li>
  </ul>
</div>
"""

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute(
        "SELECT id FROM modules WHERE course_id = ? AND order_index = ?",
        ("course-compliance-101", 1),
    )
    row = cur.fetchone()
    if row:
        conn.execute("UPDATE modules SET content = ? WHERE id = ?", (CONTENT.strip(), row[0]))
        conn.commit()
        print(f"✅ Module 1 updated: {len(CONTENT)} chars")
    else:
        print("⚠️ Module not found")
    conn.close()

if __name__ == "__main__":
    main()
