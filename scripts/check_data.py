"""Check the JSON content files in data/ before the site is built.

Catches the mistakes that are easy to make when editing JSON by hand on GitHub:
a missing comma or quote, a missing required field, a malformed date, an unknown member role,
a research direction id that is duplicated, or an image path that does not exist.

Usage: python scripts/check_data.py      (exit code 1 and a list of problems if anything is wrong)
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
STATIC = ROOT / "static"
ROLES = {"postdoc", "phd", "mphil", "visiting", "uris", "fyp"}
problems = []
warnings = []


def load(name):
    path = DATA / name
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        problems.append(f"{name}: file is missing")
    except json.JSONDecodeError as e:
        problems.append(f"{name}: JSON syntax error at line {e.lineno}, column {e.colno}: {e.msg}")
    return None


def bilingual(value, where):
    if not isinstance(value, dict) or not str(value.get("en", "")).strip():
        problems.append(f"{where}: needs an object with at least an \"en\" text, e.g. {{\"en\": \"...\", \"zh\": \"...\"}}")


def image(path, where):
    if not path:
        return
    found = next((base / path for base in (ROOT / "assets", STATIC) if (base / path).is_file()), None)
    if not found:
        problems.append(f"{where}: image \"{path}\" not found under assets/ or static/")
    elif found.stat().st_size > 8 * 1024 * 1024:
        warnings.append(f"{where}: \"{path}\" is {found.stat().st_size // (1024 * 1024)} MB; "
                        "it still works, but compressing it first keeps the repository small")


site = load("site.json")
if site:
    for k in ("labName", "tagline", "summary"):
        bilingual(site.get(k), f"site.json → {k}")
    image(site.get("heroImage"), "site.json → heroImage")
    if not site.get("contact", {}).get("email"):
        problems.append("site.json → contact.email is required")

research = load("research.json")
if research:
    ids = []
    for i, d in enumerate(research.get("directions", [])):
        where = f"research.json → directions[{i}]"
        if not re.fullmatch(r"[a-z0-9-]+", str(d.get("id", ""))):
            problems.append(f"{where}: \"id\" must be lowercase letters, digits or hyphens (it becomes the page address)")
        ids.append(d.get("id"))
        for k in ("title", "summary", "intro"):
            bilingual(d.get(k), f"{where} → {k}")
        image(d.get("image"), f"{where} → image")
    for dup in {x for x in ids if ids.count(x) > 1}:
        problems.append(f"research.json: direction id \"{dup}\" is used more than once")

team = load("team.json")
if team:
    image((team.get("pi") or {}).get("photo"), "team.json → pi → photo")
    for group in ("members", "alumni"):
        for i, m in enumerate(team.get(group, [])):
            where = f"team.json → {group}[{i}] ({m.get('name', '?')})"
            if not m.get("name"):
                problems.append(f"{where}: \"name\" is required")
            if m.get("role") not in ROLES:
                problems.append(f"{where}: \"role\" must be one of {', '.join(sorted(ROLES))}")
            image(m.get("photo"), where)

pubs = load("publications.json")
if pubs is not None:
    for i, p in enumerate(pubs):
        where = f"publications.json → [{i}] ({str(p.get('title', '?'))[:50]})"
        for k in ("title", "journal", "year"):
            if not p.get(k):
                problems.append(f"{where}: \"{k}\" is required")
        authors = p.get("authors")
        if not isinstance(authors, list) or not authors:
            problems.append(f"{where}: \"authors\" must be a list, e.g. [\"Chen L\", \"Zhao Q\"]")
            continue
        complete = authors[-1].strip().lower() not in ("et al.", "et al")
        for key, pos_key, mark in (("corresponding", "correspondingPositions", "*"), ("equal", "equalPositions", "#")):
            if complete:
                for name in p.get(key, []):
                    n = authors.count(name)
                    if n != 1:
                        problems.append(
                            f"{where}: \"{key}\" name \"{name}\" matches {n} authors, so the {mark} mark "
                            f"{'goes nowhere' if n == 0 else 'is ambiguous'}; use \"{pos_key}\": [author numbers, starting from 1] instead"
                        )
            for pos in p.get(pos_key, []):
                if not isinstance(pos, int) or not 1 <= pos <= len(authors):
                    problems.append(f"{where}: \"{pos_key}\" value {pos!r} is not an author number between 1 and {len(authors)}")

news = load("news.json")
if news is not None:
    for i, n in enumerate(news):
        where = f"news.json → [{i}]"
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(n.get("date", ""))):
            problems.append(f"{where}: \"date\" must look like 2026-10-05")
        if not str(n.get("en", "")).strip():
            problems.append(f"{where}: \"en\" text is required")
        images = n.get("images", [])
        if not isinstance(images, list):
            problems.append(f"{where}: \"images\" must be a list, e.g. [\"images/news/2026-10-05-welcome.jpg\"]")
            continue
        for j, im in enumerate(images):
            src = im.get("src") if isinstance(im, dict) else im
            if not isinstance(src, str) or not src.strip():
                problems.append(f"{where} → images[{j}]: needs a path, either as a string or as \"src\"")
                continue
            found = next((base / src for base in (ROOT / "assets", STATIC) if (base / src).is_file()), None)
            if not found:
                problems.append(f"{where} → images[{j}]: \"{src}\" not found under assets/ or static/")
            elif found.stat().st_size > 8 * 1024 * 1024:
                warnings.append(f"{where} → images[{j}]: \"{src}\" is {found.stat().st_size // (1024 * 1024)} MB; "
                                "it still works, but compressing it first keeps the repository small")

load("join.json")

if (DATA / "gallery.json").exists():
    gallery = load("gallery.json")
    if gallery is not None:
        if not isinstance(gallery, list):
            problems.append("gallery.json: must be a list of pictures, e.g. [\"images/gallery/lab-life-01.jpg\"]")
        else:
            for i, g in enumerate(gallery):
                src = g.get("src") if isinstance(g, dict) else g
                if not isinstance(src, str) or not src.strip():
                    problems.append(f"gallery.json → [{i}]: needs a path, either as a string or as \"src\"")
                else:
                    image(src, f"gallery.json → [{i}]")

for w in warnings:
    print("Note: " + w)
if problems:
    print("Problems found in data/:")
    for p in problems:
        print("  - " + p)
    sys.exit(1)
print("data/ looks good.")
