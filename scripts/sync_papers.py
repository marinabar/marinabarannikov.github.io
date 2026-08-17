#!/usr/bin/env python3
"""Import new papers from an RSS/Atom feed into content/en/papers/.

Run by .github/workflows/sync-papers.yaml on a schedule. Reads the feed URL
from data/papers_feed.yaml, skips entries that were already imported
(matched by their arxiv_id / feed id), and writes one markdown file per new
entry using the same front matter schema as the hand-written example papers
(see layouts/papers/summary.html). Papers don't get their own page — each
card in the Papers section links straight to its arXiv/PDF URL.

Stdlib only, except PyYAML for the small config file.
"""

import os
import re
import sys
import tempfile
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree

import yaml

ROOT = Path(__file__).resolve().parent.parent
PAPERS_DIR = ROOT / "content" / "en" / "papers"
CONFIG_PATH = ROOT / "data" / "papers_feed.yaml"

ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}


def load_config() -> dict:
    with CONFIG_PATH.open() as f:
        return yaml.safe_load(f)


def fetch_feed(url: str) -> bytes:
    req = urllib.request.Request(
        url, headers={"User-Agent": "marinabarannikov.github.io paper sync (contact via GitHub)"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def clean_text(text: str | None) -> str:
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def arxiv_id_from_entry_id(entry_id: str) -> str:
    # e.g. "http://arxiv.org/abs/2501.01234v2" -> "2501.01234"
    match = re.search(r"abs/([\w.\-]+?)(v\d+)?$", entry_id)
    return match.group(1) if match else entry_id


def parse_atom_entries(xml_bytes: bytes) -> list[dict]:
    root = ElementTree.fromstring(xml_bytes)
    entries = []
    for entry in root.findall("atom:entry", ATOM_NS):
        entry_id = clean_text(entry.findtext("atom:id", default="", namespaces=ATOM_NS))
        title = clean_text(entry.findtext("atom:title", default="", namespaces=ATOM_NS))
        summary = clean_text(entry.findtext("atom:summary", default="", namespaces=ATOM_NS))
        published = clean_text(entry.findtext("atom:published", default="", namespaces=ATOM_NS))
        authors = [
            clean_text(a.findtext("atom:name", default="", namespaces=ATOM_NS))
            for a in entry.findall("atom:author", ATOM_NS)
        ]
        authors = [a for a in authors if a]

        arxiv_id = arxiv_id_from_entry_id(entry_id)
        entries.append(
            {
                "id": arxiv_id,
                "title": title,
                "summary": summary,
                "authors": ", ".join(authors),
                "published": published,
                "arxiv_abs": f"https://arxiv.org/abs/{arxiv_id}",
                "arxiv_pdf": f"https://arxiv.org/pdf/{arxiv_id}",
            }
        )
    return entries


def existing_arxiv_ids() -> set[str]:
    ids = set()
    if not PAPERS_DIR.exists():
        return ids
    for md_file in PAPERS_DIR.glob("*.md"):
        text = md_file.read_text()
        match = re.search(r'arxiv_id:\s*"?([^"\n]+)"?', text)
        if match:
            ids.add(match.group(1).strip())
    return ids


def slugify(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return slug[:80] or "paper"


def yaml_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace('"', '\\"')


def parse_date(published: str) -> str:
    if not published:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")
    try:
        dt = datetime.strptime(published, "%Y-%m-%dT%H:%M:%SZ")
        return dt.strftime("%Y-%m-%dT%H:%M:%S+00:00")
    except ValueError:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")


def write_paper(entry: dict) -> Path:
    slug = slugify(entry["title"])
    path = PAPERS_DIR / f"{slug}.md"
    suffix = 2
    while path.exists():
        path = PAPERS_DIR / f"{slug}-{suffix}.md"
        suffix += 1

    front_matter = f"""---
title: "{yaml_escape(entry['title'])}"
date: {parse_date(entry['published'])}
build:
  render: false
  list: true
params:
  authors: "{yaml_escape(entry['authors'])}"
  venue: "arXiv preprint"
  arxiv_id: "{entry['id']}"
  links:
    arxiv: "{entry['arxiv_abs']}"
    pdf: "{entry['arxiv_pdf']}"
  image: ""

---

{entry['summary']}
"""
    path.write_text(front_matter)
    return path


def main() -> None:
    config = load_config()
    feed_url = config["feed_url"]
    max_new = int(config.get("max_new_entries", 5))

    print(f"Fetching feed: {feed_url}")
    xml_bytes = fetch_feed(feed_url)
    entries = parse_atom_entries(xml_bytes)
    print(f"Feed returned {len(entries)} entries")

    known_ids = existing_arxiv_ids()
    new_entries = [e for e in entries if e["id"] not in known_ids][:max_new]

    if not new_entries:
        print("No new papers to import.")
        return

    created = []
    for entry in new_entries:
        path = write_paper(entry)
        created.append(path)
        print(f"Created {path.relative_to(ROOT)} ({entry['id']})")

    # Emit paths for the workflow to use in the commit message. Written
    # outside the repo so it never gets picked up by `git add`.
    summary_dir = Path(os.environ.get("RUNNER_TEMP", tempfile.gettempdir()))
    summary_path = summary_dir / "sync_papers_summary.txt"
    summary_path.write_text("\n".join(str(p.relative_to(ROOT)) for p in created) + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        print(f"sync_papers.py failed: {exc}", file=sys.stderr)
        sys.exit(1)
