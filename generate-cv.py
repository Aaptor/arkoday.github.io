"""
Generate Arkoday Roychowdhury's 1-Page CV PDF
Uses headless Chrome to render an exact A4 single-page vector PDF.
Run: python generate-cv.py
"""

import os
import subprocess
import pypdf

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Arkoday Roychowdhury — Curriculum Vitae</title>
  <style>
    @page {
      size: A4 portrait;
      margin: 12mm 14mm 12mm 14mm;
    }
    *, *::before, *::after {
      box-sizing: border-box;
    }
    html, body {
      margin: 0;
      padding: 0;
      background: #ffffff;
      color: #1a1a24;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      font-size: 8.8pt;
      line-height: 1.34;
      -webkit-font-smoothing: antialiased;
    }
    
    /* Header */
    .header {
      text-align: center;
      margin-bottom: 8px;
      padding-bottom: 2px;
    }
    .name {
      font-size: 18.5pt;
      font-weight: 700;
      letter-spacing: -0.3px;
      color: #0f172a;
      margin: 0 0 4px 0;
    }
    .contact-line {
      font-size: 8.5pt;
      color: #475569;
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }
    .contact-line a {
      color: #2563eb;
      text-decoration: none;
    }
    .contact-line a:hover {
      text-decoration: underline;
    }
    .contact-line .sep {
      color: #94a3b8;
    }
    
    /* Summary / Bio */
    .summary {
      font-size: 8.6pt;
      color: #334155;
      text-align: justify;
      margin: 0 0 9px 0;
      line-height: 1.36;
    }
    
    /* Sections */
    .section {
      margin-bottom: 8px;
    }
    .section:last-of-type {
      margin-bottom: 0;
    }
    .section-title {
      font-size: 9pt;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: #0f172a;
      border-bottom: 1.2px solid #cbd5e1;
      padding-bottom: 2px;
      margin: 0 0 5px 0;
    }
    
    /* Skills */
    .skills-grid {
      display: flex;
      flex-direction: column;
      gap: 2.5px;
      font-size: 8.5pt;
    }
    .skill-row {
      display: flex;
      line-height: 1.32;
    }
    .skill-label {
      font-weight: 600;
      color: #1e293b;
      min-width: 148px;
      flex-shrink: 0;
    }
    .skill-val {
      color: #334155;
    }
    
    /* Entries */
    .entry {
      margin-bottom: 6px;
    }
    .entry:last-child {
      margin-bottom: 0;
    }
    .entry-header {
      display: flex;
      justify-content: space-between;
      align-items: baseline;
      font-size: 8.8pt;
    }
    .entry-title {
      font-weight: 700;
      color: #0f172a;
    }
    .entry-role {
      font-weight: 500;
      color: #2563eb;
    }
    .entry-date {
      font-size: 8.3pt;
      color: #64748b;
      font-weight: 500;
      white-space: nowrap;
    }
    
    /* Bullets */
    ul.bullets {
      margin: 2.5px 0 0 0;
      padding-left: 15px;
      list-style-type: disc;
    }
    ul.bullets li {
      margin-bottom: 2px;
      color: #334155;
      font-size: 8.5pt;
      line-height: 1.32;
    }
    ul.bullets li:last-child {
      margin-bottom: 0;
    }
    .takeaway {
      margin-top: 2px;
      font-size: 8.4pt;
      color: #334155;
      padding-left: 15px;
      line-height: 1.32;
    }
    .takeaway-label {
      font-weight: 600;
      color: #1e293b;
      font-style: italic;
    }
    
    /* Projects / Compact list */
    ul.compact-list {
      margin: 2.5px 0 0 0;
      padding-left: 15px;
      list-style-type: disc;
    }
    ul.compact-list li {
      margin-bottom: 2.5px;
      color: #334155;
      font-size: 8.5pt;
      line-height: 1.32;
    }
    ul.compact-list li:last-child {
      margin-bottom: 0;
    }
    ul.compact-list strong {
      color: #0f172a;
    }
  </style>
</head>
<body>

  <!-- Header -->
  <header class="header">
    <h1 class="name">Arkoday Roychowdhury</h1>
    <div class="contact-line">
      <a href="mailto:arkoday8@gmail.com">arkoday8@gmail.com</a>
      <span class="sep">·</span>
      <a href="https://www.linkedin.com/in/arkoday-roychowdhury-810749230" target="_blank">linkedin.com/in/arkoday-roychowdhury-810749230</a>
      <span class="sep">·</span>
      <a href="https://github.com/Aaptor" target="_blank">github.com/Aaptor</a>
      <span class="sep">·</span>
      <a href="https://www.arkoday.com" target="_blank">arkoday.com</a>
    </div>
  </header>

  <!-- Summary -->
  <p class="summary">
    Computer Science undergraduate at the University of York with practical data science experience in healthcare — most recently building patient cohorts and cross-venue outcome analyses at Bluevia Health. An early hands-on engineering education pushed me towards the applied side of technology, and towards machine learning and robotics.
  </p>

  <!-- Technical Skills -->
  <section class="section">
    <div class="section-title">Technical Skills</div>
    <div class="skills-grid">
      <div class="skill-row">
        <span class="skill-label">Programming languages</span>
        <span class="skill-val">Python, Java, SQL, C, Bash, Assembly</span>
      </div>
      <div class="skill-row">
        <span class="skill-label">Libraries and frameworks</span>
        <span class="skill-val">pandas, NumPy, scikit-learn, PyTorch, Matplotlib, Tkinter</span>
      </div>
      <div class="skill-row">
        <span class="skill-label">Methods</span>
        <span class="skill-val">data cleaning, statistical analysis, hypothesis testing, regression, decision trees, K-Means, CNNs</span>
      </div>
      <div class="skill-row">
        <span class="skill-label">Computer science</span>
        <span class="skill-val">data structures and algorithms, complexity analysis, concurrency and parallel programming, computer architecture, operating systems, TCP/IP networking, test-driven development</span>
      </div>
      <div class="skill-row">
        <span class="skill-label">Tools and platforms</span>
        <span class="skill-val">Git and GitHub, Jupyter, Gemini CLI, MCP Platform, SQLite, Excel</span>
      </div>
      <div class="skill-row">
        <span class="skill-label">Operating systems</span>
        <span class="skill-val">Windows, macOS, Linux (Ubuntu)</span>
      </div>
      <div class="skill-row">
        <span class="skill-label">Spoken languages</span>
        <span class="skill-val">English and Bengali (fluent); French (intermediate); Hindi (basic understanding)</span>
      </div>
    </div>
  </section>

  <!-- Experience -->
  <section class="section">
    <div class="section-title">Experience</div>
    
    <div class="entry">
      <div class="entry-header">
        <span class="entry-title">Bluevia Health <span class="entry-role">— Data Science Intern, Remote</span></span>
        <span class="entry-date">Apr – Jul 2026</span>
      </div>
      <ul class="bullets">
        <li>Worked on a venue-of-care analysis building towards interpretable risk stratification, extracting and analysing patient data from the MCP Platform using Gemini CLI.</li>
        <li>Built cohorts covering inpatient and outpatient populations as well as specific surgical procedures, then enriched their encounters by layering data such as medications and labs accessed through the platform.</li>
        <li>Produced statistical analyses of cross-venue outcomes including length of stay and readmission, and cleaned and prepared the data for export in accordance with patient privacy guidelines.</li>
      </ul>
      <div class="takeaway">
        <span class="takeaway-label">Took away:</span> an end-to-end view of clinical data work, and confidence using an LLM command-line tool as a real analysis instrument.
      </div>
    </div>

    <div class="entry">
      <div class="entry-header">
        <span class="entry-title">Network Rail <span class="entry-role">— Engineering Challenge, Team Lead</span></span>
        <span class="entry-date">Mar – Apr 2022</span>
      </div>
      <ul class="bullets">
        <li>Led a team of 10 across two challenges: redesigning London Euston station and the railway route from London Euston to Birmingham New Street.</li>
        <li>Combined technical design with business-case planning under cost and efficiency constraints; the proposed route was projected to increase profits by 3–4% through price discrimination.</li>
      </ul>
      <div class="takeaway">
        <span class="takeaway-label">Took away:</span> my first experience of leading a team to a deadline under commercial as well as technical constraints.
      </div>
    </div>

    <div class="entry">
      <div class="entry-header">
        <span class="entry-title">University of Warwick Esports <span class="entry-role">— Marketing and Production</span></span>
        <span class="entry-date">Apr 2022</span>
      </div>
      <ul class="bullets">
        <li>Created a promotional video and a promotion strategy for an esports tournament that was later broadcast to hundreds of viewers, using Canva and Pixlr for graphics and DaVinci Resolve for editing.</li>
      </ul>
      <div class="takeaway">
        <span class="takeaway-label">Took away:</span> how to shape content around a specific audience and a fixed date, plus practical production skills.
      </div>
    </div>
  </section>

  <!-- Projects and Technical Development -->
  <section class="section">
    <div class="section-title">Projects and Technical Development</div>
    <ul class="compact-list">
      <li><strong>Forex trading algorithm</strong> — built for the Morgan Stanley programming challenge, 2024; a first exercise in turning a strategy into testable code.</li>
      <li><strong>Personal finance applications</strong> — an expense tracker and finance dashboard built for my own use at university, 2024.</li>
      <li><strong>MIT OpenCourseWare</strong> — completed “Introduction to Computer Science and Programming Using Python”, 2024.</li>
      <li><strong>CNC Machining</strong> — programmed and operated a CNC lathe at WMG Academy for Young Engineers, 2021.</li>
    </ul>
  </section>

  <!-- Education -->
  <section class="section">
    <div class="section-title">Education</div>
    
    <div class="entry">
      <div class="entry-header">
        <span class="entry-title">University of York <span class="entry-role">— BSc Computer Science</span></span>
        <span class="entry-date">Expected 2027</span>
      </div>
      <ul class="bullets">
        <li>On track for a 2:1 based on second-year module results.</li>
        <li><strong>Relevant modules:</strong> Introduction to Data Science; Intelligent Systems (Machine Learning and Optimisation); Object Oriented Data Structures and Algorithms; Operating Systems, Security and Networking; Advanced Computer Systems.</li>
      </ul>
    </div>

    <div class="entry">
      <div class="entry-header">
        <span class="entry-title">WMG Academy for Young Engineers, Coventry <span class="entry-role">— A-levels</span></span>
        <span class="entry-date">2024</span>
      </div>
      <ul class="bullets">
        <li>Mathematics (A), Physics (B), Economics (B), Further Mathematics (C)</li>
      </ul>
    </div>
  </section>

  <!-- Leadership, Awards and Interests -->
  <section class="section" style="margin-bottom: 0;">
    <div class="section-title">Leadership, Awards and Interests</div>
    <ul class="compact-list">
      <li><strong>University of York Badminton Club</strong> — B team player in my second year, competing in league fixtures alongside a full academic workload.</li>
      <li><strong>National Citizen Service, Westhorpe Farm, Marlow</strong> — raised over £1,080 for the Coventry food bank with my group, the highest total in that summer’s programme, through outdoor and problem-solving work with people I had never met, July – August 2022.</li>
      <li><strong>CIMA Business Management, April 2022</strong> — awarded “Outstanding performance”.</li>
      <li><strong>Other interests</strong> — Chess and weightlifting outside of badminton.</li>
    </ul>
  </section>

</body>
</html>
"""

def main():
    root = os.path.dirname(os.path.abspath(__file__))
    html_path = os.path.join(root, "cv_source.html")
    pdf_out1 = os.path.join(root, "Arkoday_Roychowdhury_CV.pdf")
    pdf_out2 = os.path.join(root, "cv.pdf")
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(HTML_TEMPLATE)
        
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    browser = next((p for p in chrome_paths if os.path.exists(p)), None)
    if not browser:
        print("Error: No Chrome or Edge browser executable found.")
        return
        
    url = "file:///" + html_path.replace("\\", "/")
    cmd = [
        browser,
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        f"--print-to-pdf={pdf_out1}",
        "--no-pdf-header-footer",
        url
    ]
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("PDF generation error:", res.stderr)
        return
        
    import shutil
    shutil.copyfile(pdf_out1, pdf_out2)
    
    # Verify page count
    r = pypdf.PdfReader(pdf_out1)
    print(f"Generated {pdf_out1} (pages: {len(r.pages)})")
    print(f"Copied to {pdf_out2}")
    if os.path.exists(html_path):
        os.remove(html_path)

if __name__ == "__main__":
    main()
