# arkoday.com — Portfolio Architecture & Development Overview

This document provides a comprehensive overview of **[arkoday.com](https://www.arkoday.com)**: its design philosophy, architectural layout, the purpose of every code component, and a complete chronological summary of all improvements and features developed so far.

---

## 1. Project Purpose & Vision

The site serves as the digital portfolio, CV hub, and technical research blog for **Arkoday Roychowdhury**, a third-year Computer Science student at the **University of York** focusing on Machine Learning, Data Science, and biologically/organically inspired AI systems.

### Core Objectives
1. **Zero-Dependency Simplicity**: Built with clean, semantic HTML5, Vanilla CSS, and modular modern JavaScript. No heavy frontend frameworks, no bundlers, and zero build steps. Fast page load times and seamless hosting via GitHub Pages.
2. **Distinctive Editorial Tech Aesthetic**: Clean typography using **Space Grotesk**, smooth CSS transitions, subtle depth shadows, and an organic background particle system that reflects Arkoday's passion for biological AI.
3. **Flawless Dual-Theme Experience**: Full support for both a crisp Light Mode (soft lilac/slate with violet and azure accents) and an immersive Dark Mode (galactic dark navy with glowing cyan and purple highlights).
4. **Professional & Recruiter-Friendly**: Highlights practical experience (internships and industry work), core technical competencies, downloadable single-page CV, and deep-dive technical notes.

---

## 2. Codebase Architecture & File Purposes

```
arkoday.github.io/
├── index.html                   # Primary landing page (Hero, Featured Note, Experience, Technical Skills)
├── about.html                   # In-depth biography, full educational trajectory, college societies & badminton
├── projects.html                # Portfolio index of software & data engineering projects
├── blog.html                    # Technical writing, engineering notes, and research thoughts index
├── cv.html                      # Dedicated web CV viewer with responsive layout & direct download links
├── 404.html                     # Custom 404 error page maintaining site styling and quick navigation
├── cv.pdf                       # Standardized, single-page printable curriculum vitae
├── styles.css                   # Unified CSS design system (CSS variables, themes, grids, cards, responsive rules)
├── sitemap.xml                  # XML sitemap for SEO discovery and search indexing
├── robots.txt                   # Web crawler instructions
├── CNAME                        # Custom domain configuration pointing to www.arkoday.com
│
├── js/
│   ├── theme.js                 # Theme switcher: handles light/dark toggling and persists to localStorage
│   ├── reveal.js                # IntersectionObserver script for smooth scroll-triggered element animations
│   └── particles.js             # High-performance, zero-dependency HTML5 canvas organic particle constellation
│
├── blog/
│   ├── post-template.html       # Structural blueprint for generating new blog articles
│   └── why-my-first-cnn-overfit.html  # In-depth technical note on inductive biases, shortcuts, and vision architectures
│
├── projects/
│   ├── project-template.html    # Uniform template for engineering project case studies
│   ├── forex-trading-algorithm.html    # Case study: algorithmic trading model
│   └── personal-finance-apps.html      # Case study: financial analytics tooling
│
├── pages/
│   └── badminton.html           # Dedicated page for university sports, community tournaments, and gallery
│
├── images/
│   ├── profile.jpg              # High-resolution headshot in the Alps
│   ├── badminton.jpg            # Sports and tournament action photograph
│   └── og-image.png             # OpenGraph social card for link previews (1200x630)
│
├── new-post.py                  # CLI utility to scaffold, link, and register new blog articles
└── generate-cv.py               # Automation script to compile and format the single-page CV
```

### Detailed Component Roles

#### A. Global Stylesheet (`styles.css`)
- **CSS Custom Properties**: Central source of truth for color palettes, surface tones, typography scales, border radii, and timing functions.
- **Adaptive Themes**: Uses `[data-theme="dark"]` attribute overrides and respects system preferences via `@media (prefers-color-scheme: dark)`.
- **Layout Architecture**: Uses `.wrap-wide` (max-width: 1280px) and `.wrap` (max-width: 760px) to balance spacious desktop layouts with optimal reading line lengths.
- **Component Styling**: Reusable card styles (`.featured-note-card`, `.entry`, `.skill-group`, `.tags`, `.button`, `.nav-link`).

#### B. JavaScript Utilities (`js/`)
- **`js/particles.js`**:
  - Implements a custom 60 FPS organic particle network directly on `<canvas id="particle-canvas">`.
  - Dynamically adjusts particle count (46 on desktop, 24 on mobile) for near-zero CPU and memory usage.
  - Implements soft sinusoidal drift physics, inter-particle gradient line linking, and cursor repulsion with glowing threads.
  - Includes battery-saving features via `document.visibilityState` (pauses animation loop when tab is unfocused) and checks `prefers-reduced-motion`.
- **`js/theme.js`**:
  - Manages the theme toggle switch with accessible ARIA state.
  - Immediately updates both the DOM attribute and `localStorage` to avoid flash of unstyled content (FOUC).
- **`js/reveal.js`**:
  - Uses modern `IntersectionObserver` to trigger subtle `.reveal` fade-in effects as the user scrolls.

#### C. Content Creation Scripts (`new-post.py` & `generate-cv.py`)
- **`new-post.py`**:
  - Run via `python new-post.py "Your Title"`.
  - Automatically clones `blog/post-template.html`, injects current date, formats slugs, prepends the link to `blog.html`, and registers the URL inside `sitemap.xml`.
- **`generate-cv.py`**:
  - Compiles structured CV information and exports a clean single-page PDF with precise margin and font constraints.

---

## 3. What We Have Built & Refined (Chronological Evolution)

Here is a detailed breakdown of all the iterations and enhancements completed across the project:

### 1. Single-Page CV Optimization
- **Problem**: The original CV expanded over multiple pages with inconsistent layout density.
- **Solution**: Formatted a single-page condensed PDF (`cv.pdf`), standardizing section hierarchy (Education, Experience, Projects, Skills) so all vital qualifications fit cleanly on one page.
- **Web CV**: Updated `cv.html` with an embedded preview, quick-download button, and mobile-friendly responsive layout.

### 2. Profile Photo Depth & Aesthetics
- **Problem**: An earlier glowing ring around the hero profile image felt artificial and visually distracting.
- **Solution**: Removed the glow and implemented a layered, gentle drop-shadow effect (`rgba(15, 23, 42, 0.12)` in light mode, `rgba(0, 0, 0, 0.5)` in dark mode). This gives the circular image natural depth above the background particles.

### 3. Modern Typography Upgrade (Space Grotesk)
- **Problem**: Default system fonts lacked personality and modern tech identity.
- **Solution**: Integrated **Space Grotesk** across the entire site. Updated headings (`h1` through `h4`), navigation links, badges, action buttons, and body text. The geometric proportions enhance readability and create an authentic editorial tech feel.

### 4. Zero-Dependency Organic Particle Canvas
- **Problem**: Needed a dynamic, visually engaging visual touch without importing heavy external libraries.
- **Solution**: Created `js/particles.js` from scratch. Configured fixed background canvas positioning (`z-index: 0`), set foreground sections (`z-index: 1`) with translucent hero backdrops, and gave widgets solid card backgrounds so particles flow smoothly across negative space without obstructing text readability.

### 5. Information Architecture & Page Restructuring
- **Problem**: `index.html` was overcrowded with redundant education details, while `about.html` had duplicate content.
- **Solution**:
  - **Removed Education from `index.html`**: Streamlined the home page.
  - **Retained Full Educational History on `about.html`**: University of York BSc details (expected 2027, 2:1 trajectory, specific modules), WMG Academy A-Levels, and university societies/badminton are centralized on the About page.
  - **Shifted Experience and Skills**: Reorganized index sections so Experience becomes Section 3 and Technical Skills becomes Section 4.

### 6. Home Page "Featured Note" Showcase Card
- **Problem**: The home page lacked direct access to Arkoday's technical thought process and latest engineering writings.
- **Solution**:
  - Created a **Featured Note** showcase section placed directly underneath the hero and profile picture.
  - Designed `.featured-note-card` with an electric gradient top border, publication date, reading time estimate, topic badges, and dual direct links ("Read note" and "All notes →").

### 7. Authored & Published "Why My First CNN Overfit"
- **Problem**: The blog lacked authentic technical content showcasing machine learning problem-solving.
- **Solution**: Authored a complete technical article in `blog/why-my-first-cnn-overfit.html` covering:
  - Experiencing 98% training accuracy vs. 54.2% validation collapse.
  - Diagnosing shortcut learning using Class Activation Maps (CAM).
  - Mathematical analysis of effective receptive fields and kernel dilation.
  - The connection between CNN inductive bias and biological vision (primate ventral visual stream).
  - Full PyTorch diagnostic code block.
  - Added to `blog.html` and `sitemap.xml`.

### 8. Cache-Busting & Git Deployment Automation
- Updated cache-busting version query parameters (`styles.css?v=15`) across all 12 HTML templates to ensure instant styling updates in visitors' browsers.
- Automated git staging, committing, and pushing directly to GitHub (`origin/main`).

---

## 4. Current Home Page Structure (`index.html`)

The home page now follows an intentional flow designed for recruiters and collaborators:

1. **Section 1: Hero**
   - Headshot photo with soft shadow depth
   - Name, headline ("Third-year BSc Computer Science student at the University of York..."), and career interests (ML, data science, organic-inspired AI)
   - Primary action buttons: "View experience", "CV"
   - Social links: GitHub, LinkedIn, Email
2. **Section 2: Featured Note (Showcase)**
   - Highlights the latest published article: *"Why My First CNN Overfit"*
   - Includes tags, date, read time, excerpt, and quick links to the article and the notes archive
3. **Section 3: Experience**
   - Bluevia Health (Data Science Intern)
   - Network Rail (Work Experience Trainee)
   - Warwick Esports (Marketing & Production)
4. **Section 4: Technical Skills**
   - 5 structured categories: Programming Languages, Libraries & Frameworks, Methods, Tools & Platforms, Spoken Languages
   - Clear badge tags rendered on elevated surface cards

---

## 5. Summary of Key Files for Future Editing

| File | What to edit here |
|---|---|
| `index.html` | Hero introduction, featured note snippet, work history entries, skills list |
| `about.html` | Full bio, educational coursework, societies, sports, personal background |
| `projects.html` | Featured project cards and links to full case studies |
| `blog.html` | Reverse-chronological directory of published notes and articles |
| `cv.html` | Online CV presentation and PDF link target |
| `styles.css` | Color palette variables, spacing, typography, card animations, responsive media queries |
| `js/particles.js` | Particle count, speed, connection distance, colors, mouse interaction radius |
| `new-post.py` | Script to run when creating a new blog post |

---

*Last updated: September 2026*
