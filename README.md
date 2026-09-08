# arkoday.com

My portfolio site — a static site with no build step, served by GitHub Pages
from `main` at [www.arkoday.com](https://www.arkoday.com).

## Structure

```
index.html                       Home — hero, featured projects, skills, experience, contact
projects.html                    Projects index
projects/project-template.html   Blank template for a project write-up
blog.html                        Notes index
blog/post-template.html          Template a new post is generated from
new-post.py                      Creates a post, links it, updates the sitemap
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

## Adding a blog post

```bash
python new-post.py "Why my first CNN overfit"
```

That one command does three things:

1. Creates `blog/why-my-first-cnn-overfit.html` from `blog/post-template.html`,
   with the title, slug, date and metadata filled in.
2. Links it from the top of the list on `blog.html` (newest first), removing
   the "no posts yet" placeholder if it's still there.
3. Adds it to `sitemap.xml`.

Then open the new file, write the post inside `<section class="post-body">`,
and replace the placeholder summary in **both** the post and `blog.html`.
The template has a comment listing the markup you're likely to need.

The script never overwrites an existing post — re-run it after editing and it
stops rather than clobbering your work.

**If you stop posting**, remove the `Notes` link from the nav rather than
leaving a stale blog up. It appears once per page:

```bash
grep -rl '>Notes</a>' --include=*.html .
```

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
