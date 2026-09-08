#!/usr/bin/env python3
"""Create a new blog post.

    python new-post.py "Why my first CNN overfit"

Creates blog/<slug>.html from blog/post-template.html, links it from the top
of the list on blog.html, and adds it to sitemap.xml. Then you just write.

Nothing is overwritten: if the post already exists the script stops and tells
you. Re-running after an edit is safe -- it will refuse rather than clobber.
"""

import datetime
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEMPLATE = ROOT / "blog" / "post-template.html"
INDEX = ROOT / "blog.html"
SITEMAP = ROOT / "sitemap.xml"
SITE = "https://www.arkoday.com"


def slugify(title):
    s = title.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def main():
    if len(sys.argv) < 2 or not sys.argv[1].strip():
        sys.exit('Usage: python new-post.py "Your post title"')

    title = sys.argv[1].strip()
    slug = slugify(title)
    if not slug:
        sys.exit("Could not make a URL slug from that title.")

    today = datetime.date.today()
    iso = today.isoformat()
    pretty = today.strftime("%d %B %Y").lstrip("0")
    summary = "A one-line summary of this post."

    post_path = ROOT / "blog" / f"{slug}.html"
    if post_path.exists():
        sys.exit(f"{post_path.relative_to(ROOT)} already exists - not overwriting.")

    # --- 1. Create the post from the template -----------------------------
    body = TEMPLATE.read_text(encoding="utf-8")
    for key, value in (
        ("{{TITLE}}", html.escape(title)),
        ("{{SLUG}}", slug),
        ("{{ISODATE}}", iso),
        ("{{DATE}}", pretty),
        ("{{SUMMARY}}", html.escape(summary)),
    ):
        body = body.replace(key, value)
    post_path.write_text(body, encoding="utf-8", newline="\n")

    # --- 2. Link it from blog.html, newest first --------------------------
    index = INDEX.read_text(encoding="utf-8")
    entry = (
        '          <li class="post-item">\n'
        f'            <a href="./blog/{slug}.html">{html.escape(title)}</a>\n'
        f'            <p class="post-meta"><time datetime="{iso}">{pretty}</time></p>\n'
        f'            <p class="muted small">{html.escape(summary)}</p>\n'
        "          </li>\n"
    )
    # drop the "no posts yet" placeholder once there is a real post
    index = re.sub(
        r'          <li class="post-item post-empty">.*?</li>\n',
        "",
        index,
        flags=re.S,
    )
    marker = "          <!-- posts:start -->\n"
    if marker not in index:
        sys.exit("Could not find the posts:start marker in blog.html.")
    index = index.replace(marker, marker + entry, 1)
    INDEX.write_text(index, encoding="utf-8", newline="\n")

    # --- 3. Add it to the sitemap -----------------------------------------
    sitemap = SITEMAP.read_text(encoding="utf-8")
    url_block = (
        "  <url>\n"
        f"    <loc>{SITE}/blog/{slug}.html</loc>\n"
        f"    <lastmod>{iso}</lastmod>\n"
        "    <priority>0.6</priority>\n"
        "  </url>\n"
    )
    if f"/blog/{slug}.html" not in sitemap:
        sitemap = sitemap.replace("</urlset>", url_block + "</urlset>")
        SITEMAP.write_text(sitemap, encoding="utf-8", newline="\n")

    print(f"Created  blog/{slug}.html")
    print("Linked   blog.html")
    print("Added    sitemap.xml")
    print()
    print("Next: write the post, and replace the placeholder summary in both")
    print(f"      blog/{slug}.html and blog.html.")


if __name__ == "__main__":
    main()
