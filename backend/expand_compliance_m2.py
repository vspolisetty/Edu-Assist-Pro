"""
Expand Module 2: Workplace Safety (~25K chars target)
"""
import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), "courses.db")

CONTENT = """
<h2>Workplace Safety</h2>

<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:20px 0;background:linear-gradient(135deg,#16a34a08,#16a34a03);border-radius:12px;padding:16px">
  <div style="text-align:center;padding:16px"><div style="font-size:32px">🏥</div><div style="font-size:1.5rem;font-weight:700;color:#16a34a">2.8M</div><div style="font-size:.8rem;color:#64748b">Workplace Injuries/Year</div></div>
  <div style="text-align:center;padding:16px"><div style="font-size:32px">💰</div><div style="font-size:1.5rem;font-weight:700;color:#16a34a">$170B</div><div style="font-size:.8rem;color:#64748b">Annual Cost to Business</div></div>
  <div style="text-align:center;padding:16px"><div style="font-size:32px">📉</div><div style="font-size:1.5rem;font-weight:700;color:#16a34a">5,190</div><div style="font-size:.8rem;color:#64748b">Fatal Injuries (2021)</div></div>
  <div style="text-align:center;padding:16px"><div style="font-size:32px">✅</div><div style="font-size:1.5rem;font-weight:700;color:#16a34a">95%</div><div style="font-size:.8rem;color:#64748b">Are Preventable</div></div>
</div>

<img src="https://images.unsplash.com/photo-1504307651254-35680f356dfd?w=800&h=400&fit=crop" alt="Workplace safety equipment and hard hats" style="width:100%;border-radius:12px;margin:20px 0;box-shadow:0 4px 12px rgba(0,0,0,0.1)">

<h3>🎯 Learning Objectives</h3>
<p>By the end of this module, you will be able to:</p>
<ul>
  <li>Identify common workplace hazards across different work environments</li>
  <li>Apply the hierarchy of hazard controls to eliminate or reduce risks</li>
  <li>Execute emergency procedures including evacuation and shelter-in-place</li>
  <li>Report safety incidents and near-misses using proper protocols</li>
  <li>Maintain ergonomic workstations to prevent repetitive strain injuries</li>
  <li>Understand OSHA regulations and your rights as an employee</li>
</ul>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>📚 Why Workplace Safety Matters</h3>

<p>A safe workplace is not just a legal requirement — it's a <strong>moral imperative and a business necessity</strong>. Every day, approximately 12 workers die on the job in the United States, and thousands more suffer preventable injuries.</p>

<p>The impact of workplace injuries extends far beyond the individual:</p>
<ul>
  <li><strong>Human cost:</strong> Pain, disability, trauma for workers and families</li>
  <li><strong>Financial cost:</strong> Medical expenses, lost wages, workers' compensation</li>
  <li><strong>Business cost:</strong> Lost productivity, training replacements, equipment damage</li>
  <li><strong>Legal cost:</strong> OSHA fines, lawsuits, regulatory scrutiny</li>
  <li><strong>Cultural cost:</strong> Decreased morale, fear, high turnover</li>
</ul>

<div style="background:linear-gradient(135deg,#16a34a08,#16a34a03);border-left:4px solid #16a34a;padding:20px 24px;margin:24px 0;border-radius:0 10px 10px 0">
  <strong style="display:flex;align-items:center;gap:8px;margin-bottom:8px">💡 The Business Case for Safety</strong>
  <div style="font-size:.92rem;line-height:1.7">According to OSHA, businesses spend approximately <strong>$1 billion per week</strong> on workers' compensation costs alone. Studies show that for every $1 invested in workplace safety programs, companies see a return of <strong>$4-$6</strong> in reduced injuries, lower insurance premiums, and improved productivity.</div>
</div>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>⚠️ Common Workplace Hazards</h3>

<p>Hazards exist in every work environment — from traditional offices to manufacturing floors. Understanding and recognizing hazards is the first step in preventing injuries.</p>

<h4>The Six Categories of Workplace Hazards</h4>

<table style="width:100%;border-collapse:collapse;margin:16px 0">
  <tr style="background:#f8fafc"><th style="padding:12px;text-align:left;border:1px solid #e2e8f0">Category</th><th style="padding:12px;text-align:left;border:1px solid #e2e8f0">Examples</th><th style="padding:12px;text-align:left;border:1px solid #e2e8f0">Prevention</th><th style="padding:12px;text-align:left;border:1px solid #e2e8f0">Industries Most Affected</th></tr>
  <tr><td style="padding:12px;border:1px solid #e2e8f0"><strong>🔧 Physical</strong></td><td style="padding:12px;border:1px solid #e2e8f0">Slips, falls, machinery, noise, temperature</td><td style="padding:12px;border:1px solid #e2e8f0">Guards, PPE, signage, training</td><td style="padding:12px;border:1px solid #e2e8f0">Construction, Manufacturing</td></tr>
  <tr><td style="padding:12px;border:1px solid #e2e8f0"><strong>⚗️ Chemical</strong></td><td style="padding:12px;border:1px solid #e2e8f0">Toxic substances, fumes, corrosives</td><td style="padding:12px;border:1px solid #e2e8f0">Ventilation, SDS sheets, PPE</td><td style="padding:12px;border:1px solid #e2e8f0">Healthcare, Labs, Cleaning</td></tr>
  <tr><td style="padding:12px;border:1px solid #e2e8f0"><strong>🦠 Biological</strong></td><td style="padding:12px;border:1px solid #e2e8f0">Viruses, bacteria, mold, insects</td><td style="padding:12px;border:1px solid #e2e8f0">Hygiene protocols, vaccines, PPE</td><td style="padding:12px;border:1px solid #e2e8f0">Healthcare, Agriculture</td></tr>
  <tr><td style="padding:12px;border:1px solid #e2e8f0"><strong>💺 Ergonomic</strong></td><td style="padding:12px;border:1px solid #e2e8f0">Poor posture, repetitive motion, lifting</td><td style="padding:12px;border:1px solid #e2e8f0">Adjustable equipment, breaks, training</td><td style="padding:12px;border:1px solid #e2e8f0">Office, Warehouse, Healthcare</td></tr>
  <tr><td style="padding:12px;border:1px solid #e2e8f0"><strong>😰 Psychosocial</strong></td><td style="padding:12px;border:1px solid #e2e8f0">Stress, violence, harassment, workload</td><td style="padding:12px;border:1px solid #e2e8f0">Policies, EAP, workload management</td><td style="padding:12px;border:1px solid #e2e8f0">All industries</td></tr>
  <tr><td style="padding:12px;border:1px solid #e2e8f0"><strong>⚡ Electrical</strong></td><td style="padding:12px;border:1px solid #e2e8f0">Faulty wiring, overloaded circuits, exposed wires</td><td style="padding:12px;border:1px solid #e2e8f0">Inspections, lockout/tagout, training</td><td style="padding:12px;border:1px solid #e2e8f0">Construction, Maintenance</td></tr>
</table>

<img src="https://images.unsplash.com/photo-1581092921461-eab62e97a780?w=800&h=350&fit=crop" alt="Safety signage and workplace safety symbols" style="width:100%;border-radius:12px;margin:20px 0;box-shadow:0 4px 12px rgba(0,0,0,0.1)">

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>🔺 The Hierarchy of Hazard Controls</h3>

<p>When addressing hazards, NIOSH (National Institute for Occupational Safety and Health) recommends following the Hierarchy of Controls — from most effective to least effective:</p>

<div style="margin:24px 0">
  <div style="background:#16a34a;color:white;padding:20px;border-radius:12px 12px 0 0;text-align:center">
    <strong style="font-size:1.2rem">1. ELIMINATION</strong>
    <p style="margin:8px 0 0;font-size:.9rem">Physically remove the hazard completely</p>
    <p style="margin:4px 0 0;font-size:.8rem;opacity:.9">Example: Automate a dangerous manual process</p>
  </div>
  <div style="background:#22c55e;color:white;padding:20px;text-align:center">
    <strong style="font-size:1.1rem">2. SUBSTITUTION</strong>
    <p style="margin:8px 0 0;font-size:.9rem">Replace the hazard with something safer</p>
    <p style="margin:4px 0 0;font-size:.8rem;opacity:.9">Example: Use a less toxic chemical</p>
  </div>
  <div style="background:#84cc16;color:white;padding:20px;text-align:center">
    <strong style="font-size:1.1rem">3. ENGINEERING CONTROLS</strong>
    <p style="margin:8px 0 0;font-size:.9rem">Isolate people from the hazard</p>
    <p style="margin:4px 0 0;font-size:.8rem;opacity:.9">Example: Install machine guards, ventilation systems</p>
  </div>
  <div style="background:#eab308;color:white;padding:20px;text-align:center">
    <strong style="font-size:1.1rem">4. ADMINISTRATIVE CONTROLS</strong>
    <p style="margin:8px 0 0;font-size:.9rem">Change the way people work</p>
    <p style="margin:4px 0 0;font-size:.8rem;opacity:.9">Example: Job rotation, training, warning signs</p>
  </div>
  <div style="background:#f97316;color:white;padding:20px;border-radius:0 0 12px 12px;text-align:center">
    <strong style="font-size:1.1rem">5. PPE (Personal Protective Equipment)</strong>
    <p style="margin:8px 0 0;font-size:.9rem">Protect the worker with equipment</p>
    <p style="margin:4px 0 0;font-size:.8rem;opacity:.9">Example: Safety glasses, gloves, hard hats (LAST RESORT)</p>
  </div>
</div>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>🚨 Emergency Procedures</h3>

<p>Every employee must know how to respond to emergencies. Familiarize yourself with these procedures BEFORE an emergency occurs.</p>

<h4>Fire Emergency Procedure: R.A.C.E.</h4>

<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:20px 0">
  <div style="background:#ef4444;color:white;padding:20px;border-radius:12px;text-align:center">
    <div style="font-size:2.5rem;font-weight:700">R</div>
    <strong>RESCUE</strong>
    <p style="font-size:.8rem;margin:8px 0 0">Remove anyone in immediate danger (only if safe to do so)</p>
  </div>
  <div style="background:#f97316;color:white;padding:20px;border-radius:12px;text-align:center">
    <div style="font-size:2.5rem;font-weight:700">A</div>
    <strong>ALARM</strong>
    <p style="font-size:.8rem;margin:8px 0 0">Pull the fire alarm and call emergency services</p>
  </div>
  <div style="background:#eab308;color:white;padding:20px;border-radius:12px;text-align:center">
    <div style="font-size:2.5rem;font-weight:700">C</div>
    <strong>CONFINE</strong>
    <p style="font-size:.8rem;margin:8px 0 0">Close doors to prevent fire spread</p>
  </div>
  <div style="background:#16a34a;color:white;padding:20px;border-radius:12px;text-align:center">
    <div style="font-size:2.5rem;font-weight:700">E</div>
    <strong>EVACUATE</strong>
    <p style="font-size:.8rem;margin:8px 0 0">Exit via nearest safe route to assembly point</p>
  </div>
</div>

<h4>Evacuation Guidelines</h4>
<ol style="line-height:2">
  <li><strong>Stay Calm:</strong> Panic leads to poor decisions. Take a deep breath.</li>
  <li><strong>Leave Immediately:</strong> Do not gather personal belongings</li>
  <li><strong>Use Stairs Only:</strong> NEVER use elevators during emergencies</li>
  <li><strong>Assist Others:</strong> Help those with disabilities if safe to do so</li>
  <li><strong>Proceed to Assembly Point:</strong> Go to designated meeting location</li>
  <li><strong>Report In:</strong> Floor wardens conduct headcount</li>
  <li><strong>Do Not Re-Enter:</strong> Wait for official "all clear"</li>
</ol>

<div style="background:linear-gradient(135deg,#ef444408,#ef444403);border-left:4px solid #ef4444;padding:20px 24px;margin:24px 0;border-radius:0 10px 10px 0">
  <strong style="display:flex;align-items:center;gap:8px;margin-bottom:8px">🔥 Know Your Exit Routes</strong>
  <div style="font-size:.92rem;line-height:1.7">Take time TODAY to identify: (1) The two nearest exits from your workstation, (2) The location of fire extinguishers, (3) Your floor's assembly point, (4) Who your floor warden is. This knowledge could save your life.</div>
</div>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>💺 Ergonomics: Preventing Office Injuries</h3>

<img src="https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=800&h=350&fit=crop" alt="Ergonomic office workstation setup" style="width:100%;border-radius:12px;margin:20px 0;box-shadow:0 4px 12px rgba(0,0,0,0.1)">

<p>Musculoskeletal disorders (MSDs) account for nearly <strong>30% of all worker injuries</strong>. Proper ergonomics can prevent these painful, often chronic conditions.</p>

<h4>The Ideal Workstation Setup</h4>

<div style="background:#f8fafc;padding:24px;border-radius:12px;margin:20px 0">
  <ul style="margin:0;padding-left:20px;line-height:2.2">
    <li><strong>Monitor:</strong> Top of screen at or slightly below eye level, arm's length away</li>
    <li><strong>Chair:</strong> Feet flat on floor, knees at 90°, back supported</li>
    <li><strong>Keyboard:</strong> Elbows at 90°, wrists straight (not bent)</li>
    <li><strong>Mouse:</strong> Close to keyboard, same level, move from elbow not wrist</li>
    <li><strong>Lighting:</strong> No glare on screen, adequate task lighting</li>
    <li><strong>Breaks:</strong> Follow 20-20-20 rule (every 20 min, look 20 feet away for 20 sec)</li>
  </ul>
</div>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>📝 Incident Reporting</h3>

<p>ALL incidents — including near-misses — must be reported within <strong>24 hours</strong>. Reporting helps us identify patterns and prevent future injuries.</p>

<h4>What Must Be Reported</h4>
<ul>
  <li>✅ Any injury requiring first aid or medical attention</li>
  <li>✅ Near-misses (incidents that could have caused injury)</li>
  <li>✅ Unsafe conditions (broken equipment, spills, hazards)</li>
  <li>✅ Property damage</li>
  <li>✅ Safety concerns raised by employees</li>
</ul>

<h4>How to Report</h4>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin:20px 0">
  <div style="background:#fff;border:2px solid #e2e8f0;padding:20px;border-radius:10px;text-align:center">
    <div style="font-size:32px;margin-bottom:8px">📱</div>
    <strong>Incident Hotline</strong>
    <p style="font-size:.85rem;color:#64748b;margin:8px 0 0">ext. 5555 (24/7)</p>
  </div>
  <div style="background:#fff;border:2px solid #e2e8f0;padding:20px;border-radius:10px;text-align:center">
    <div style="font-size:32px;margin-bottom:8px">📝</div>
    <strong>Online Form</strong>
    <p style="font-size:.85rem;color:#64748b;margin:8px 0 0">safety.company.com/report</p>
  </div>
  <div style="background:#fff;border:2px solid #e2e8f0;padding:20px;border-radius:10px;text-align:center">
    <div style="font-size:32px;margin-bottom:8px">👤</div>
    <strong>Direct Supervisor</strong>
    <p style="font-size:.85rem;color:#64748b;margin:8px 0 0">For immediate concerns</p>
  </div>
</div>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>🎭 Scenario-Based Exercise</h3>

<div style="background:#f1f5f9;border:1px solid #e2e8f0;padding:24px;margin:24px 0;border-radius:12px">
  <strong style="display:flex;align-items:center;gap:8px;margin-bottom:12px;font-size:1.1rem">🎯 Scenario: The Wet Floor</strong>
  <p style="margin:12px 0;font-style:italic;background:#fff;padding:16px;border-radius:8px;border-left:4px solid #3b82f6">"You're walking to a meeting and notice a water leak has created a puddle in the hallway. There's no sign or barrier, and people are walking through it."</p>
  <p style="margin:12px 0 8px;font-weight:600">What would you do?</p>
  <ul style="list-style:none;margin:0;padding:0">
    <li style="margin:6px 0;padding:10px 14px;background:#fff;border-radius:6px">⬜ A. Walk around it and continue to your meeting</li>
    <li style="margin:6px 0;padding:10px 14px;background:#fff;border-radius:6px">⬜ B. Wait for someone else to report it</li>
    <li style="margin:6px 0;padding:10px 14px;background:#fff;border-radius:6px">✅ C. Warn others, place a makeshift barrier if possible, and report immediately</li>
    <li style="margin:6px 0;padding:10px 14px;background:#fff;border-radius:6px">⬜ D. Email facilities when you get back to your desk</li>
  </ul>
  <details style="margin-top:16px">
    <summary style="cursor:pointer;color:#1a3a5c;font-weight:600;padding:8px;background:#e2e8f0;border-radius:6px">Show Answer & Explanation</summary>
    <div style="margin:12px 0;padding:16px;background:#fff;border-radius:8px;border-left:4px solid #22c55e">
      <p><strong>Correct Answer: C</strong></p>
      <p>Safety is everyone's responsibility. Take immediate action to prevent injury: verbally warn passersby, place a chair or other object to mark the hazard, and call the safety hotline immediately. The meeting can wait — someone could slip and fall while you're sitting in your meeting.</p>
    </div>
  </details>
</div>

<hr style="margin:30px 0;border:none;border-top:2px solid #e2e8f0">

<h3>💡 Key Takeaways</h3>

<div style="background:linear-gradient(135deg,#16a34a,#15803d);color:white;padding:28px;border-radius:12px;margin:24px 0">
  <ul style="margin:0;padding-left:20px;line-height:2">
    <li>Safety is <strong>everyone's responsibility</strong> — not just the safety team's</li>
    <li>If you see a hazard, <strong>report it immediately</strong> — you could prevent an injury</li>
    <li><strong>Know your emergency procedures</strong> and exit routes before you need them</li>
    <li>Use the <strong>hierarchy of controls</strong> — PPE is always the last resort</li>
    <li>Report ALL incidents, including <strong>near-misses</strong> — they reveal hidden hazards</li>
    <li><strong>Ergonomics matter</strong> — small adjustments prevent big injuries</li>
  </ul>
</div>
"""

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.execute(
        "SELECT id FROM modules WHERE course_id = ? AND order_index = ?",
        ("course-compliance-101", 2),
    )
    row = cur.fetchone()
    if row:
        conn.execute("UPDATE modules SET content = ? WHERE id = ?", (CONTENT.strip(), row[0]))
        conn.commit()
        print(f"✅ Module 2 updated: {len(CONTENT)} chars")
    else:
        print("⚠️ Module not found")
    conn.close()

if __name__ == "__main__":
    main()
