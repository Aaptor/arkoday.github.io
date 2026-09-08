# arkoday.com

My portfolio site — a static site with no build step, served by GitHub Pages
from `main` at [www.arkoday.com](https://www.arkoday.com).

## Structure

```
index.html                       Home — hero, featured projects, skills, experience, contact
projects.html                    Projects index
projects/project-template.html   Blank template for a project write-up
about.html                       Longer bio, education, skills
cv.html                          CV (drop cv.pdf in the repo root and link it)
pages/badminton.html             Badminton photos
404.html                         Not-found page
styles.css                       All styling — light + dark via prefers-color-scheme
sitemap.xml, robots.txt          Search metadata
images/og-image.png              Social preview card (1200x630)
```

## Adding a project

1. Copy `projects/project-template.html` to `projects/<slug>.html`.
2. Fill in the six sections: header, problem, approach, results, what I'd do
   differently, stack. Keep the order — the point is that every write-up reads
   the same way.
3. Add a card for it in `projects.html`, and in the featured list in
   `index.html` if it's one of the top three.
4. Add the URL to `sitemap.xml`.

## Conventions

- Colours come from the CSS variables at the top of `styles.css`. Change them
  there, not inline. `--on-accent` is the text colour used on top of `--accent`
  (it flips in dark mode, where the accent is light).
- Anything not yet written uses the `.placeholder` / `.notice` classes, which
  render conspicuously on purpose. **Delete them as you fill things in** —
  they're meant to be visible so unfinished content is never mistaken for a
  real claim.
- Images: resize to ~1280px wide before committing, and set `width`/`height`
  attributes matching the real dimensions so the page doesn't reflow on load.

## Maintenance

Once a term: add whatever you built, delete whatever aged badly, update
`cv.pdf`, click every link, and bump the "last updated" line in each footer.
