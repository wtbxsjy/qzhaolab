"""Complete and extend data/publications.json using Crossref metadata.

What it does
- For every entry with a DOI whose author list ends in "et al." (or is empty), fetch the full
  author list from Crossref, in "Family Initials" form (for example "Zhao Q", "Wang HW").
- For entries whose title ends in "…" (truncated), replace the title with Crossref's.
- Optionally add a new paper by DOI (--add), with its topics and corresponding authors.

Usage
    python scripts/update_publications.py
    python scripts/update_publications.py --add 10.1021/jasms.1c00076 --topics peptidein,immunopeptides --corresponding "Zhao Q"

Needs: Python 3.9+ and internet access to api.crossref.org (no extra packages).
"""
import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path


DATA = Path(__file__).resolve().parent.parent / "data" / "publications.json"
UA = "QZhaoLabWebsite/1.0 (https://github.com/wtbxsjy/qzhaolab)"


def fetch(doi):
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/")
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)["message"]


def initials(given):
    parts = re.split(r"[\s\-\.]+", given.strip())
    return "".join(p[0].upper() for p in parts if p)


def author_names(msg):
    out = []
    for a in msg.get("author", []):
        if "family" in a:
            fam = a["family"].strip()
            ini = initials(a.get("given", ""))
            out.append(f"{fam} {ini}".strip())
        elif "name" in a:
            out.append(a["name"].strip())
    return out


def clean(text):
    text = re.sub(r"<[^>]+>", "", text or "")
    return re.sub(r"\s+", " ", text).strip()


def entry_from(msg):
    year = (msg.get("issued", {}).get("date-parts") or [[None]])[0][0]
    e = {
        "title": clean((msg.get("title") or [""])[0]),
        "authors": author_names(msg),
        "journal": clean((msg.get("container-title") or [""])[0]),
        "year": year,
    }
    vol, issue, page = msg.get("volume"), msg.get("issue"), msg.get("page")
    if vol:
        e["volume"] = f"{vol}({issue})" if issue else str(vol)
    if page:
        e["pages"] = page.replace("-", "–")
    e["doi"] = msg.get("DOI", "").lower()
    return e


def needs_authors(p):
    a = p.get("authors") or []
    return not a or a[-1].strip().lower() in ("et al.", "et al", "…", "...")


def split_list(s):
    return [x.strip() for x in (s or "").split(",") if x.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--add", default="", help="DOI of a new paper to add")
    ap.add_argument("--topics", default="", help="comma-separated topics for the new paper")
    ap.add_argument("--corresponding", default="", help="comma-separated corresponding authors for the new paper")
    args = ap.parse_args()

    pubs = json.loads(DATA.read_text(encoding="utf-8")) or []
    changed = 0

    for p in pubs:
        doi = p.get("doi")
        if not doi or not (needs_authors(p) or str(p.get("title", "")).endswith("…")):
            continue
        try:
            msg = fetch(doi)
        except Exception as exc:  # keep going; one bad DOI should not stop the rest
            print(f"skip {doi}: {exc}", file=sys.stderr)
            continue
        fresh = entry_from(msg)
        if needs_authors(p) and fresh["authors"]:
            p["authors"] = fresh["authors"]
        if str(p.get("title", "")).endswith("…") and fresh["title"]:
            p["title"] = fresh["title"]
        for k in ("volume", "pages"):
            if k not in p and k in fresh:
                p[k] = fresh[k]
        changed += 1
        print(f"updated {doi}")
        time.sleep(0.2)

    new_doi = args.add.strip().removeprefix("https://doi.org/").lower()
    if new_doi:
        if any(str(p.get("doi", "")).lower() == new_doi for p in pubs):
            print(f"{new_doi} is already in the list")
        else:
            e = entry_from(fetch(new_doi))
            if split_list(args.corresponding):
                e["corresponding"] = split_list(args.corresponding)
            if split_list(args.topics):
                e["topics"] = split_list(args.topics)
            pubs.append(e)
            changed += 1
            print(f"added {new_doi}: {e['title']}")

    pubs.sort(key=lambda p: int(p.get("year") or 0), reverse=True)
    if changed:
        DATA.write_text(json.dumps(pubs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{changed} entr{'y' if changed == 1 else 'ies'} changed")


if __name__ == "__main__":
    main()
