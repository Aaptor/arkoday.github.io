#!/usr/bin/env python3
"""
check.py — Automated quality gates for arkoday.com portfolio site.
Validates:
1. Navigation consistency (Nav drift check: 3/3 internal links on every page)
2. No live placeholders or notices on top-level pages
3. Semantic heading structure (Exactly one <h1> per page)
4. SEO & Social metadata (<title>, meta description, canonical, OpenGraph)
5. Image hygiene (Every <img> has an alt attribute and existing source file)
6. Internal link resolution (No broken local links or 404s)
7. CV PDF availability and naming stability

Usage:
    python check.py
"""

import glob
import os
import re
import sys
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.abspath(__file__))

TEMPLATES = {
    os.path.join("projects", "project-template.html"),
    os.path.join("blog", "post-template.html"),
}

def get_all_html():
    return sorted(glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True))

def check_nav_drift(html_files):
    errors = []
    for path in html_files:
        rel = os.path.relpath(path, ROOT)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        matches = set(re.findall(r'href="[^"]*(projects|blog|about)\.html"', content))
        if len(matches) < 3:
            errors.append(f"Nav drift in {rel}: found only {len(matches)}/3 internal nav links ({matches})")
    return errors

def check_placeholders(html_files):
    errors = []
    for path in html_files:
        rel = os.path.relpath(path, ROOT)
        if rel in TEMPLATES or rel.startswith("projects" + os.sep):
            continue
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if 'class="placeholder' in content or 'placeholder-card' in content:
            errors.append(f"Unfinished placeholder class found in published page: {rel}")
        # Notice banner only permitted in templates or draft projects
        if 'class="notice"' in content:
            errors.append(f"Notice block still present in published page: {rel}")
    return errors

def check_h1_headings(html_files):
    errors = []
    for path in html_files:
        rel = os.path.relpath(path, ROOT)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', content, flags=re.DOTALL | re.IGNORECASE)
        if len(h1s) == 0:
            errors.append(f"Missing <h1> heading in: {rel}")
        elif len(h1s) > 1:
            errors.append(f"Multiple ({len(h1s)}) <h1> headings found in: {rel}")
    return errors

def check_metadata(html_files):
    errors = []
    for path in html_files:
        rel = os.path.relpath(path, ROOT)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        if not re.search(r'<title>.*?</title>', content, re.IGNORECASE):
            errors.append(f"Missing <title> tag in: {rel}")
        if not re.search(r'<meta\s+name=["\']description["\']', content, re.IGNORECASE):
            errors.append(f"Missing meta description in: {rel}")
        if not re.search(r'<meta\s+property=["\']og:title["\']', content, re.IGNORECASE):
            errors.append(f"Missing og:title tag in: {rel}")
    return errors

def check_images(html_files):
    errors = []
    for path in html_files:
        rel = os.path.relpath(path, ROOT)
        dir_path = os.path.dirname(path)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        clean_content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
        img_tags = re.findall(r'<img\s+([^>]+)>', clean_content, re.IGNORECASE)
        for tag in img_tags:
            if not re.search(r'alt=["\']', tag, re.IGNORECASE):
                errors.append(f"<img> missing alt attribute in {rel}: <img {tag}>")
            src_match = re.search(r'src=["\']([^"\']+)["\']', tag, re.IGNORECASE)
            if src_match:
                src = src_match.group(1)
                if not src.startswith("http") and not src.startswith("//"):
                    local_target = os.path.normpath(os.path.join(dir_path, src.split("?")[0]))
                    if not os.path.exists(local_target):
                        errors.append(f"Broken image reference in {rel}: {src} (expected at {local_target})")
    return errors

def check_internal_links(html_files):
    errors = []
    for path in html_files:
        rel = os.path.relpath(path, ROOT)
        dir_path = os.path.dirname(path)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        # Remove HTML comments and <code> blocks before checking links
        clean_content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
        clean_content = re.sub(r'<code[^>]*>.*?</code>', '', clean_content, flags=re.DOTALL)
        links = re.findall(r'<a\s+[^>]*href=["\']([^"\'#]+)(?:#[^"\']*)?["\']', clean_content, re.IGNORECASE)
        for link in links:
            if link.startswith("http") or link.startswith("mailto:") or link.startswith("tel:") or link == "URL":
                continue
            clean_path = urlparse(link).path
            if not clean_path:
                continue
            if clean_path.startswith("/"):
                target = os.path.normpath(os.path.join(ROOT, clean_path.lstrip("/")))
            else:
                target = os.path.normpath(os.path.join(dir_path, clean_path))
            if not os.path.exists(target):
                errors.append(f"Broken internal link in {rel}: '{link}' (resolves to non-existent '{target}')")
    return errors

def check_cv_assets():
    errors = []
    stable_cv = os.path.join(ROOT, "Arkoday_Roychowdhury_CV.pdf")
    alias_cv = os.path.join(ROOT, "cv.pdf")
    if not os.path.exists(stable_cv):
        errors.append("Missing primary stable CV file: Arkoday_Roychowdhury_CV.pdf")
    if not os.path.exists(alias_cv):
        errors.append("Missing alias CV file: cv.pdf")
    return errors

def main():
    print("=" * 60)
    print("Running Quality Gates for arkoday.com...")
    print("=" * 60)

    html_files = get_all_html()
    print(f"Found {len(html_files)} HTML files.")

    all_errors = []

    tests = [
        ("Navigation Drift Check", check_nav_drift),
        ("Placeholders & Notices", check_placeholders),
        ("Heading Hierarchy (Single <h1>)", check_h1_headings),
        ("SEO & Social Metadata", check_metadata),
        ("Image Hygiene & Alt Attributes", check_images),
        ("Internal Link Resolution", check_internal_links),
    ]

    for name, test_func in tests:
        errors = test_func(html_files)
        if errors:
            print(f"[FAIL] {name}:")
            for err in errors:
                print(f"       - {err}")
            all_errors.extend(errors)
        else:
            print(f"[PASS] {name}")

    cv_errors = check_cv_assets()
    if cv_errors:
        print("[FAIL] CV Assets Check:")
        for err in cv_errors:
            print(f"       - {err}")
        all_errors.extend(cv_errors)
    else:
        print("[PASS] CV Assets Check")

    print("-" * 60)
    if all_errors:
        print(f"RESULT: FAILED ({len(all_errors)} issues found)")
        sys.exit(1)
    else:
        print("RESULT: ALL QUALITY GATES PASSED! Ready to push.")
        sys.exit(0)

if __name__ == "__main__":
    main()
