"""
Expand Module 0: Company Policies Overview (~30K chars target)
"""
import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), "courses.db")

CONTENT = """
<h2>Company Policies Overview</h2>

<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:20px 0;background:linear-gradient(135deg,#1a3a5c08,#1a3a5c03);border-radius:12px;padding:16px">
  <div style="text-align:center;padding:16px"><div style="font-size:32px">📋</div><div style="font-size:1.5rem;font-weight:700;color:#1a3a5c">50+</div><div style="font-size:.8rem;color:#64748b">Active Policies</div></div>
  <div style="text-align:center;padding:16px"><div style="font-size:32px">👥</div><div style="font-size:1.5rem;font-weight:700;color:#1a3a5c">100%</div><div style="font-size:.8rem;color:#64748b">Employee Coverage</div></div>
  <div style="text-align:center;padding:16px"><div style="font-size:32px">📅</div><div style="font-size:1.5rem;font-weight:700;color:#1a3a5c">Annual</div><div style="font-size:.8rem;color:#64748b">Review Cycle</div></div>
  <div style="text-align:center;padding:16px"><div style="font-size:32px">⚖️</div><div style="font-size:1.5rem;font-weight:700;color:#1a3a5c">Zero</div><div style="font-size:.8rem;color:#64748b">Tolerance Policy</div></div>
</div>

<img src="https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=800&h=400&fit=crop" alt="Business documents and policies" style="width:100%;border-radius:12px;margin:20px 0;box-shadow:0 4px 12px rgba(0,0,0,0.1)">

<h3>🎯 Learning Objectives</h3>
<p>By the end of this module, you will be able to:</p>
<ul>
  <li>Understand the purpose, scope, and legal foundation of company policies</li>
  <li>Identify your specific responsibilities as an employee under each major policy category</li>
  <li>Navigate the policy documentation system and find answers quickly</li>
  <li>Apply policy knowledge to complex real-world workplace scenarios</li>
  <li>Recognize policy violations and understand reporting procedures</li>
  <li>Understand the consequences of non-compliance and how to avoid them</li>
</ul>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>📚 Introduction: Why Policies Matter</h3>

<p>Company policies are far more than bureaucratic paperwork — they are the <strong>living framework</strong> that defines how we operate as an organization. Think of policies as the "rules of the game" that ensure everyone plays fairly, safely, and ethically.</p>

<p>Without clear policies, organizations face:</p>
<ul>
  <li><strong>Legal exposure:</strong> Lawsuits, regulatory fines, and compliance failures</li>
  <li><strong>Inconsistent treatment:</strong> Favoritism, discrimination claims, and employee resentment</li>
  <li><strong>Operational chaos:</strong> Conflicting decisions, duplicated efforts, and wasted resources</li>
  <li><strong>Reputational damage:</strong> Public scandals, loss of customer trust, and brand erosion</li>
  <li><strong>Employee confusion:</strong> Unclear expectations leading to mistakes and poor performance</li>
</ul>

<div style="background:linear-gradient(135deg,#2c7a7b08,#2c7a7b03);border-left:4px solid #2c7a7b;padding:20px 24px;margin:24px 0;border-radius:0 10px 10px 0">
  <strong style="display:flex;align-items:center;gap:8px;margin-bottom:8px">📊 Research Insight</strong>
  <div style="font-size:.92rem;line-height:1.7">According to the Society for Human Resource Management (SHRM), organizations with comprehensive, well-communicated policies experience <strong>40% fewer employee disputes</strong>, <strong>60% faster issue resolution</strong>, and <strong>25% higher employee satisfaction scores</strong> compared to those with informal or poorly documented practices.</div>
</div>

<h3>The Legal Foundation of Workplace Policies</h3>

<p>Company policies don't exist in a vacuum — they are built upon a complex foundation of federal, state, and local laws. Understanding this foundation helps you appreciate why certain policies exist and why compliance is non-negotiable.</p>

<h4>Federal Laws That Shape Our Policies</h4>
<table style="width:100%;border-collapse:collapse;margin:16px 0">
  <tr style="background:#f8fafc"><th style="padding:12px 16px;text-align:left;border:1px solid #e2e8f0">Law</th><th style="padding:12px 16px;text-align:left;border:1px solid #e2e8f0">Year</th><th style="padding:12px 16px;text-align:left;border:1px solid #e2e8f0">Key Provisions</th><th style="padding:12px 16px;text-align:left;border:1px solid #e2e8f0">Related Policies</th></tr>
  <tr><td style="padding:12px 16px;border:1px solid #e2e8f0"><strong>Title VII (Civil Rights Act)</strong></td><td style="padding:12px 16px;border:1px solid #e2e8f0">1964</td><td style="padding:12px 16px;border:1px solid #e2e8f0">Prohibits discrimination based on race, color, religion, sex, national origin</td><td style="padding:12px 16px;border:1px solid #e2e8f0">EEO Policy, Anti-Harassment</td></tr>
  <tr><td style="padding:12px 16px;border:1px solid #e2e8f0"><strong>OSHA</strong></td><td style="padding:12px 16px;border:1px solid #e2e8f0">1970</td><td style="padding:12px 16px;border:1px solid #e2e8f0">Requires safe and healthful working conditions</td><td style="padding:12px 16px;border:1px solid #e2e8f0">Workplace Safety, Emergency Procedures</td></tr>
  <tr><td style="padding:12px 16px;border:1px solid #e2e8f0"><strong>ADA</strong></td><td style="padding:12px 16px;border:1px solid #e2e8f0">1990</td><td style="padding:12px 16px;border:1px solid #e2e8f0">Prohibits discrimination against individuals with disabilities</td><td style="padding:12px 16px;border:1px solid #e2e8f0">Accommodation Policy, Accessibility</td></tr>
  <tr><td style="padding:12px 16px;border:1px solid #e2e8f0"><strong>FMLA</strong></td><td style="padding:12px 16px;border:1px solid #e2e8f0">1993</td><td style="padding:12px 16px;border:1px solid #e2e8f0">Provides job-protected leave for family/medical reasons</td><td style="padding:12px 16px;border:1px solid #e2e8f0">Leave Policy, Time Off</td></tr>
  <tr><td style="padding:12px 16px;border:1px solid #e2e8f0"><strong>HIPAA</strong></td><td style="padding:12px 16px;border:1px solid #e2e8f0">1996</td><td style="padding:12px 16px;border:1px solid #e2e8f0">Protects health information privacy</td><td style="padding:12px 16px;border:1px solid #e2e8f0">Privacy Policy, Data Protection</td></tr>
  <tr><td style="padding:12px 16px;border:1px solid #e2e8f0"><strong>Sarbanes-Oxley</strong></td><td style="padding:12px 16px;border:1px solid #e2e8f0">2002</td><td style="padding:12px 16px;border:1px solid #e2e8f0">Financial reporting accuracy, whistleblower protection</td><td style="padding:12px 16px;border:1px solid #e2e8f0">Ethics Policy, Whistleblower Protection</td></tr>
</table>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>🏛️ Our Code of Conduct: The Foundation of Everything</h3>

<img src="https://images.unsplash.com/photo-1521791136064-7986c2920216?w=800&h=350&fit=crop" alt="Professional handshake representing integrity" style="width:100%;border-radius:12px;margin:20px 0;box-shadow:0 4px 12px rgba(0,0,0,0.1)">

<p>Our Code of Conduct is the cornerstone document that defines who we are as an organization. It establishes the ethical and behavioral standards that every employee — from entry-level to CEO — must uphold in every interaction, decision, and transaction.</p>

<h4>The Four Pillars of Our Code</h4>

<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:20px;margin:24px 0">
  <div style="background:linear-gradient(135deg,#1a3a5c08,#1a3a5c02);border:1px solid #e2e8f0;padding:24px;border-radius:12px">
    <div style="font-size:36px;margin-bottom:12px">🎯</div>
    <h4 style="margin:0 0 12px 0;color:#1a3a5c">1. Act with Integrity</h4>
    <p style="margin:0;font-size:.9rem;line-height:1.6;color:#475569">Integrity is doing the right thing even when no one is watching. It means being honest, transparent, and trustworthy in every business dealing, internal communication, and external interaction.</p>
    <ul style="margin:12px 0 0 0;padding-left:20px;font-size:.85rem;color:#64748b">
      <li>Accurately report work hours, expenses, and project status</li>
      <li>Never misrepresent data, qualifications, or capabilities</li>
      <li>Honor commitments to colleagues, clients, and partners</li>
      <li>Admit mistakes promptly rather than covering them up</li>
      <li>Avoid even the appearance of impropriety</li>
    </ul>
  </div>
  <div style="background:linear-gradient(135deg,#2c7a7b08,#2c7a7b02);border:1px solid #e2e8f0;padding:24px;border-radius:12px">
    <div style="font-size:36px;margin-bottom:12px">🤝</div>
    <h4 style="margin:0 0 12px 0;color:#2c7a7b">2. Treat Others with Respect</h4>
    <p style="margin:0;font-size:.9rem;line-height:1.6;color:#475569">A respectful workplace is a productive workplace. We value diversity of thought, background, and experience. We treat every person with dignity regardless of their role, seniority, or background.</p>
    <ul style="margin:12px 0 0 0;padding-left:20px;font-size:.85rem;color:#64748b">
      <li>Value diverse perspectives and communication styles</li>
      <li>Listen actively before responding</li>
      <li>Address disagreements professionally, not personally</li>
      <li>Never engage in gossip, bullying, or exclusion</li>
      <li>Celebrate others' successes genuinely</li>
    </ul>
  </div>
  <div style="background:linear-gradient(135deg,#7c3aed08,#7c3aed02);border:1px solid #e2e8f0;padding:24px;border-radius:12px">
    <div style="font-size:36px;margin-bottom:12px">🛡️</div>
    <h4 style="margin:0 0 12px 0;color:#7c3aed">3. Protect Company Assets</h4>
    <p style="margin:0;font-size:.9rem;line-height:1.6;color:#475569">Company assets include physical property, intellectual property, confidential data, financial resources, and our reputation. Every employee is a steward of these assets.</p>
    <ul style="margin:12px 0 0 0;padding-left:20px;font-size:.85rem;color:#64748b">
      <li>Use technology and equipment for authorized purposes</li>
      <li>Safeguard confidential information at all times</li>
      <li>Report lost or stolen equipment immediately</li>
      <li>Never share proprietary information externally</li>
      <li>Protect our brand and reputation in public</li>
    </ul>
  </div>
  <div style="background:linear-gradient(135deg,#dc262608,#dc262602);border:1px solid #e2e8f0;padding:24px;border-radius:12px">
    <div style="font-size:36px;margin-bottom:12px">⚖️</div>
    <h4 style="margin:0 0 12px 0;color:#dc2626">4. Follow the Law</h4>
    <p style="margin:0;font-size:.9rem;line-height:1.6;color:#475569">Compliance with all applicable laws is non-negotiable. This includes not just obvious laws but also regulations, industry standards, and contractual obligations that govern our operations.</p>
    <ul style="margin:12px 0 0 0;padding-left:20px;font-size:.85rem;color:#64748b">
      <li>Anti-bribery and anti-corruption compliance (FCPA, UK Bribery Act)</li>
      <li>Securities regulations and insider trading prohibitions</li>
      <li>Employment laws (wage, hour, discrimination, safety)</li>
      <li>Environmental and sustainability regulations</li>
      <li>Industry-specific compliance requirements</li>
    </ul>
  </div>
</div>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>📋 Key Policy Categories: A Comprehensive Overview</h3>

<p>Our policy framework is organized into eight major categories. Each category contains multiple specific policies that work together to create a complete governance structure.</p>

<h4>Category 1: Employment Policies</h4>
<div style="background:#f8fafc;border-radius:10px;padding:20px;margin:16px 0">
  <p>Employment policies govern the entire employee lifecycle from hiring to separation. They ensure fair, consistent treatment and legal compliance.</p>
  <table style="width:100%;border-collapse:collapse;margin:12px 0">
    <tr style="background:#e2e8f0"><th style="padding:10px 14px;text-align:left;border:1px solid #cbd5e1">Policy</th><th style="padding:10px 14px;text-align:left;border:1px solid #cbd5e1">Purpose</th><th style="padding:10px 14px;text-align:left;border:1px solid #cbd5e1">Key Points</th></tr>
    <tr><td style="padding:10px 14px;border:1px solid #cbd5e1">Equal Employment Opportunity</td><td style="padding:10px 14px;border:1px solid #cbd5e1">Prevents discrimination</td><td style="padding:10px 14px;border:1px solid #cbd5e1">Applies to all employment decisions</td></tr>
    <tr><td style="padding:10px 14px;border:1px solid #cbd5e1">At-Will Employment</td><td style="padding:10px 14px;border:1px solid #cbd5e1">Defines employment relationship</td><td style="padding:10px 14px;border:1px solid #cbd5e1">Either party can end relationship</td></tr>
    <tr><td style="padding:10px 14px;border:1px solid #cbd5e1">Background Checks</td><td style="padding:10px 14px;border:1px solid #cbd5e1">Ensures safe hiring</td><td style="padding:10px 14px;border:1px solid #cbd5e1">Conducted per FCRA requirements</td></tr>
    <tr><td style="padding:10px 14px;border:1px solid #cbd5e1">Probationary Period</td><td style="padding:10px 14px;border:1px solid #cbd5e1">Evaluates new hire fit</td><td style="padding:10px 14px;border:1px solid #cbd5e1">90 days with performance milestones</td></tr>
    <tr><td style="padding:10px 14px;border:1px solid #cbd5e1">Termination Procedures</td><td style="padding:10px 14px;border:1px solid #cbd5e1">Ensures fair separation</td><td style="padding:10px 14px;border:1px solid #cbd5e1">Documentation, exit interview, final pay</td></tr>
  </table>
</div>

<h4>Category 2: Conduct & Ethics Policies</h4>
<div style="background:#f8fafc;border-radius:10px;padding:20px;margin:16px 0">
  <p>Conduct policies define behavioral expectations and ethical standards that maintain our culture and reputation.</p>
  <table style="width:100%;border-collapse:collapse;margin:12px 0">
    <tr style="background:#e2e8f0"><th style="padding:10px 14px;text-align:left;border:1px solid #cbd5e1">Policy</th><th style="padding:10px 14px;text-align:left;border:1px solid #cbd5e1">Purpose</th><th style="padding:10px 14px;text-align:left;border:1px solid #cbd5e1">Key Points</th></tr>
    <tr><td style="padding:10px 14px;border:1px solid #cbd5e1">Code of Conduct</td><td style="padding:10px 14px;border:1px solid #cbd5e1">Sets ethical standards</td><td style="padding:10px 14px;border:1px solid #cbd5e1">Foundation for all behavior</td></tr>
    <tr><td style="padding:10px 14px;border:1px solid #cbd5e1">Anti-Harassment</td><td style="padding:10px 14px;border:1px solid #cbd5e1">Ensures safe workplace</td><td style="padding:10px 14px;border:1px solid #cbd5e1">Zero tolerance; multiple reporting channels</td></tr>
    <tr><td style="padding:10px 14px;border:1px solid #cbd5e1">Conflict of Interest</td><td style="padding:10px 14px;border:1px solid #cbd5e1">Protects objectivity</td><td style="padding:10px 14px;border:1px solid #cbd5e1">Disclosure required; management approved</td></tr>
    <tr><td style="padding:10px 14px;border:1px solid #cbd5e1">Gift & Entertainment</td><td style="padding:10px 14px;border:1px solid #cbd5e1">Prevents corruption</td><td style="padding:10px 14px;border:1px solid #cbd5e1">$50 limit; no cash equivalents</td></tr>
    <tr><td style="padding:10px 14px;border:1px solid #cbd5e1">Whistleblower Protection</td><td style="padding:10px 14px;border:1px solid #cbd5e1">Encourages reporting</td><td style="padding:10px 14px;border:1px solid #cbd5e1">Anonymity guaranteed; no retaliation</td></tr>
  </table>
</div>

<h4>Category 3: Workplace Safety Policies</h4>
<div style="background:#f8fafc;border-radius:10px;padding:20px;margin:16px 0">
  <p>Safety policies protect employees from physical harm and ensure compliance with OSHA and other safety regulations.</p>
  <table style="width:100%;border-collapse:collapse;margin:12px 0">
    <tr style="background:#e2e8f0"><th style="padding:10px 14px;text-align:left;border:1px solid #cbd5e1">Policy</th><th style="padding:10px 14px;text-align:left;border:1px solid #cbd5e1">Purpose</th><th style="padding:10px 14px;text-align:left;border:1px solid #cbd5e1">Key Points</th></tr>
    <tr><td style="padding:10px 14px;border:1px solid #cbd5e1">General Safety</td><td style="padding:10px 14px;border:1px solid #cbd5e1">Overall workplace safety</td><td style="padding:10px 14px;border:1px solid #cbd5e1">OSHA compliance; hazard reporting</td></tr>
    <tr><td style="padding:10px 14px;border:1px solid #cbd5e1">Emergency Procedures</td><td style="padding:10px 14px;border:1px solid #cbd5e1">Crisis response</td><td style="padding:10px 14px;border:1px solid #cbd5e1">Evacuation routes; assembly points</td></tr>
    <tr><td style="padding:10px 14px;border:1px solid #cbd5e1">Drug-Free Workplace</td><td style="padding:10px 14px;border:1px solid #cbd5e1">Ensures sobriety</td><td style="padding:10px 14px;border:1px solid #cbd5e1">Testing policy; EAP support</td></tr>
    <tr><td style="padding:10px 14px;border:1px solid #cbd5e1">Violence Prevention</td><td style="padding:10px 14px;border:1px solid #cbd5e1">Protects from threats</td><td style="padding:10px 14px;border:1px solid #cbd5e1">Zero tolerance; threat assessment</td></tr>
    <tr><td style="padding:10px 14px;border:1px solid #cbd5e1">Ergonomics</td><td style="padding:10px 14px;border:1px solid #cbd5e1">Prevents injury</td><td style="padding:10px 14px;border:1px solid #cbd5e1">Workstation setup; equipment requests</td></tr>
  </table>
</div>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>🎭 Scenario-Based Exercises</h3>

<div style="background:#f1f5f9;border:1px solid #e2e8f0;padding:24px;margin:24px 0;border-radius:12px">
  <strong style="display:flex;align-items:center;gap:8px;margin-bottom:12px;font-size:1.1rem">🎯 Scenario 1: The Manager's Request</strong>
  <p style="margin:12px 0;font-style:italic;background:#fff;padding:16px;border-radius:8px;border-left:4px solid #3b82f6">"Your manager asks you to 'adjust' some numbers in a client report to make the quarterly results look better. She says 'everyone does it' and it's not a big deal. The client won't know the difference."</p>
  <p style="margin:12px 0 8px;font-weight:600">What would you do?</p>
  <ul style="list-style:none;margin:0;padding:0">
    <li style="margin:6px 0;padding:10px 14px;background:#fff;border-radius:6px">⬜ A. Do what your manager asks — she has more experience and probably knows best</li>
    <li style="margin:6px 0;padding:10px 14px;background:#fff;border-radius:6px">✅ B. Refuse politely and report the request through the Ethics Hotline</li>
    <li style="margin:6px 0;padding:10px 14px;background:#fff;border-radius:6px">⬜ C. Adjust the numbers slightly — just enough to help but not enough to be noticed</li>
    <li style="margin:6px 0;padding:10px 14px;background:#fff;border-radius:6px">⬜ D. Ignore the request and hope she doesn't ask again</li>
  </ul>
  <details style="margin-top:16px">
    <summary style="cursor:pointer;color:#1a3a5c;font-weight:600;padding:8px;background:#e2e8f0;border-radius:6px">Show Answer & Explanation</summary>
    <div style="margin:12px 0;padding:16px;background:#fff;border-radius:8px;border-left:4px solid #22c55e">
      <p><strong>Correct Answer: B</strong></p>
      <p>Falsifying reports is a serious ethical and legal violation that could result in termination, civil liability, and even criminal charges. Your manager's instruction does not override company policy or the law. The phrase "everyone does it" is a classic rationalization that doesn't make the action right.</p>
      <p><strong>Why other answers are wrong:</strong></p>
      <ul>
        <li><strong>A:</strong> Experience doesn't justify unethical behavior. Senior employees are held to the same standards.</li>
        <li><strong>C:</strong> There's no such thing as "a little" fraud. Any falsification is a violation.</li>
        <li><strong>D:</strong> Ignoring unethical requests doesn't resolve the issue and may make you complicit.</li>
      </ul>
    </div>
  </details>
</div>

<div style="background:#f1f5f9;border:1px solid #e2e8f0;padding:24px;margin:24px 0;border-radius:12px">
  <strong style="display:flex;align-items:center;gap:8px;margin-bottom:12px;font-size:1.1rem">🎯 Scenario 2: The Gift Dilemma</strong>
  <p style="margin:12px 0;font-style:italic;background:#fff;padding:16px;border-radius:8px;border-left:4px solid #3b82f6">"A vendor you work with regularly sends you a $200 gift card to a nice restaurant 'as a thank you' for the business relationship. There's a handwritten note saying they hope you'll continue working together."</p>
  <p style="margin:12px 0 8px;font-weight:600">What would you do?</p>
  <ul style="list-style:none;margin:0;padding:0">
    <li style="margin:6px 0;padding:10px 14px;background:#fff;border-radius:6px">⬜ A. Accept it — it's just a thank you and doesn't affect your decisions</li>
    <li style="margin:6px 0;padding:10px 14px;background:#fff;border-radius:6px">⬜ B. Accept it but don't tell anyone</li>
    <li style="margin:6px 0;padding:10px 14px;background:#fff;border-radius:6px">✅ C. Politely decline and return the gift card, then notify your manager</li>
    <li style="margin:6px 0;padding:10px 14px;background:#fff;border-radius:6px">⬜ D. Accept it and share it with the team</li>
  </ul>
  <details style="margin-top:16px">
    <summary style="cursor:pointer;color:#1a3a5c;font-weight:600;padding:8px;background:#e2e8f0;border-radius:6px">Show Answer & Explanation</summary>
    <div style="margin:12px 0;padding:16px;background:#fff;border-radius:8px;border-left:4px solid #22c55e">
      <p><strong>Correct Answer: C</strong></p>
      <p>Our Gift & Entertainment Policy prohibits accepting cash or cash equivalents (including gift cards) of any value from business partners. This policy exists because cash-like gifts create the appearance of impropriety and potential conflicts of interest, even if your intentions are pure.</p>
      <p><strong>Key Policy Points:</strong></p>
      <ul>
        <li>Cash and gift cards must always be declined regardless of value</li>
        <li>Non-cash gifts over $50 must be disclosed to your manager</li>
        <li>Non-cash gifts over $200 must be returned or donated</li>
        <li>When in doubt, disclose — transparency protects you</li>
      </ul>
    </div>
  </details>
</div>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>📞 How to Report Policy Concerns</h3>

<img src="https://images.unsplash.com/photo-1556745757-8d76bdb6984b?w=800&h=350&fit=crop" alt="Professional help desk and support" style="width:100%;border-radius:12px;margin:20px 0;box-shadow:0 4px 12px rgba(0,0,0,0.1)">

<p>If you witness a policy violation or have concerns about potentially unethical behavior, you have multiple reporting channels available. <strong>You are protected from retaliation regardless of which channel you use.</strong></p>

<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:16px;margin:20px 0">
  <div style="background:#fff;border:2px solid #e2e8f0;padding:20px;border-radius:10px;text-align:center">
    <div style="font-size:32px;margin-bottom:8px">👤</div>
    <strong>Direct Supervisor</strong>
    <p style="font-size:.85rem;color:#64748b;margin:8px 0 0">First option for most concerns (unless they're involved)</p>
  </div>
  <div style="background:#fff;border:2px solid #e2e8f0;padding:20px;border-radius:10px;text-align:center">
    <div style="font-size:32px;margin-bottom:8px">🏢</div>
    <strong>HR Department</strong>
    <p style="font-size:.85rem;color:#64748b;margin:8px 0 0">hr@company.com or schedule in-person</p>
  </div>
  <div style="background:#fff;border:2px solid #e2e8f0;padding:20px;border-radius:10px;text-align:center">
    <div style="font-size:32px;margin-bottom:8px">📞</div>
    <strong>Ethics Hotline</strong>
    <p style="font-size:.85rem;color:#64748b;margin:8px 0 0">24/7 anonymous: 1-800-ETHICS</p>
  </div>
  <div style="background:#fff;border:2px solid #e2e8f0;padding:20px;border-radius:10px;text-align:center">
    <div style="font-size:32px;margin-bottom:8px">⚖️</div>
    <strong>Legal Department</strong>
    <p style="font-size:.85rem;color:#64748b;margin:8px 0 0">For potential legal violations</p>
  </div>
</div>

<div style="background:linear-gradient(135deg,#22c55e08,#22c55e03);border:1px solid #22c55e40;padding:20px 24px;margin:24px 0;border-radius:12px">
  <strong style="display:flex;align-items:center;gap:8px;margin-bottom:10px">🛡️ Retaliation Protection</strong>
  <p style="margin:0;font-size:.92rem;line-height:1.7">Retaliation against anyone who reports a concern in good faith is <strong>strictly prohibited</strong> and is itself a terminable offense. You are protected whether the report ultimately proves valid or not. Even if your concern turns out to be unfounded, you will not face consequences as long as you reported in good faith.</p>
</div>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>✅ Knowledge Checks</h3>

<div style="background:linear-gradient(135deg,#22c55e08,#22c55e02);border:1px solid #22c55e40;padding:20px 24px;margin:20px 0;border-radius:12px">
  <strong style="display:flex;align-items:center;gap:8px;margin-bottom:12px">✅ Knowledge Check 1</strong>
  <p style="margin:8px 0;font-weight:500">Under our Gift Policy, what is the maximum value of a non-cash gift you can accept from a vendor without disclosure?</p>
  <ul style="list-style:none;margin:12px 0;padding:0">
    <li style="margin:4px 0">○ A. $25</li>
    <li style="margin:4px 0">✅ B. $50</li>
    <li style="margin:4px 0">○ C. $100</li>
    <li style="margin:4px 0">○ D. $200</li>
  </ul>
  <details style="margin-top:12px">
    <summary style="cursor:pointer;color:#22c55e;font-weight:600">Reveal Answer</summary>
    <p style="margin:10px 0;padding:12px;background:#22c55e08;border-radius:8px">Gifts under $50 can be accepted without disclosure. Gifts $50-$200 must be disclosed to your manager within 5 business days. Gifts over $200 must be declined or returned.</p>
  </details>
</div>

<div style="background:linear-gradient(135deg,#22c55e08,#22c55e02);border:1px solid #22c55e40;padding:20px 24px;margin:20px 0;border-radius:12px">
  <strong style="display:flex;align-items:center;gap:8px;margin-bottom:12px">✅ Knowledge Check 2</strong>
  <p style="margin:8px 0;font-weight:500">Which of the following is NOT a valid reporting channel for ethics concerns?</p>
  <ul style="list-style:none;margin:12px 0;padding:0">
    <li style="margin:4px 0">○ A. Your direct supervisor</li>
    <li style="margin:4px 0">○ B. The anonymous Ethics Hotline</li>
    <li style="margin:4px 0">✅ C. Posting on social media</li>
    <li style="margin:4px 0">○ D. The HR Department</li>
  </ul>
  <details style="margin-top:12px">
    <summary style="cursor:pointer;color:#22c55e;font-weight:600">Reveal Answer</summary>
    <p style="margin:10px 0;padding:12px;background:#22c55e08;border-radius:8px">Social media is never an appropriate channel for reporting internal ethics concerns. It bypasses proper investigation procedures, may violate confidentiality policies, and could expose you and the company to legal liability.</p>
  </details>
</div>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>💡 Key Takeaways</h3>

<div style="background:linear-gradient(135deg,#1a3a5c,#2c5282);color:white;padding:28px;border-radius:12px;margin:24px 0">
  <ul style="margin:0;padding-left:20px;line-height:2">
    <li>Company policies <strong>protect you</strong> — they're not just rules, they're your rights and your shield</li>
    <li>When in doubt, <strong>disclose and ask</strong> — transparency is always the right choice</li>
    <li>Use the <strong>Ethics Hotline</strong> if you're uncomfortable reporting directly — it's anonymous and protected</li>
    <li>Review the <strong>Employee Handbook</strong> at least once a year, especially after updates</li>
    <li><strong>No policy is worth violating for short-term gain</strong> — the consequences always outweigh the benefits</li>
    <li>You are <strong>protected from retaliation</strong> when reporting concerns in good faith</li>
  </ul>
</div>

<h3>📚 Additional Resources</h3>
<ul>
  <li><strong>Employee Handbook:</strong> HR Portal → Documents → Employee Handbook</li>
  <li><strong>Policy Updates:</strong> Sent via email; acknowledgment required within 7 days</li>
  <li><strong>FAQ Section:</strong> hr.company.com/policy-faq</li>
  <li><strong>HR Office Hours:</strong> Every Wednesday 2-4 PM for walk-in questions</li>
  <li><strong>Ethics Training:</strong> Required annually via the Learning Management System</li>
</ul>
"""

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute(
        "SELECT id FROM modules WHERE course_id = ? AND order_index = ?",
        ("course-compliance-101", 0),
    )
    row = cur.fetchone()
    if row:
        conn.execute("UPDATE modules SET content = ? WHERE id = ?", (CONTENT.strip(), row[0]))
        conn.commit()
        print(f"✅ Module 0 updated: {len(CONTENT)} chars")
    else:
        print("⚠️ Module not found")
    conn.close()

if __name__ == "__main__":
    main()
