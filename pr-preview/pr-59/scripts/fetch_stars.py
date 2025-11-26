#!/usr/bin/env python3
"""Fetch GitHub stars for component repos.

The result is attached to component
frontmatter so Jekyll can sort by `stars` at build time. Also emits
`assets/js/github-stars.json` for client-side fallback.

Run this in CI before `jekyll build` so the modified `_components/*.md`
files are read with `stars` present.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

import requests
import yaml

ROOT = Path(__file__).resolve().parents[1]
COMPONENTS_DIR = ROOT / "_components"
OUT_FILE = ROOT / "assets" / "js" / "github-stars.json"

GITHUB_API = "https://api.github.com/repos/{owner}/{repo}"
TOKEN = os.environ.get("GITHUB_TOKEN")


def parse_frontmatter_and_body(md_text: str) -> tuple[dict, str]:
    """Parse the frontmatter of a markdown file and return its values.

    Args:
        md_text (str): The markdown text to parse.

    Returns:
        tuple[dict, str]: The frontmatter values.
    """
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", md_text, re.DOTALL)
    if not m:
        return {}, md_text
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        fm = {}
    body = m.group(2)
    return fm, body


def repo_from_url(url: str | None) -> str | None:
    """Get the github repository ID from a github URL.

    Args:
        url (str | None): The URL to check.

    Returns:
        str | None: A repo identifier.
    """
    if not url:
        return None
    m = re.search(r"github\.com/([^/]+)/([^/]+)", url)
    if not m:
        return None
    owner = m.group(1)
    repo = m.group(2).rstrip(".git")
    return f"{owner}/{repo}"


def fetch_stars(owner_repo: str) -> int | None:
    """Load the stars of a github repository.

    Args:
        owner_repo (str): The owner/repo identifier.

    Returns:
        int | None: The star count, or None on failure.
    """
    owner, repo = owner_repo.split("/")
    url = GITHUB_API.format(owner=owner, repo=repo)
    headers = {"Accept": "application/vnd.github.v3+json"}
    if TOKEN:
        headers["Authorization"] = f"token {TOKEN}"
    try:
        r = requests.get(url, headers=headers, timeout=20)
    except requests.exceptions.RequestException as e:
        print(f"Warning: request failed for {owner_repo}: {e}")
        return None
    if r.status_code == 200:
        data = r.json()
        return data.get("stargazers_count")
    print(f"Warning: failed to fetch {owner_repo}: {r.status_code} {r.text}")
    return None


def main() -> None:
    """Load the stars of all components and store them into the frontmatter."""
    mapping: dict[str, int | None] = {}
    files = sorted(COMPONENTS_DIR.glob("*.md"))
    if not files:
        print("No component files found in _components/")
        sys.exit(0)

    # First pass: collect repos and fetch counts
    for f in files:
        text = f.read_text(encoding="utf-8")
        fm, _ = parse_frontmatter_and_body(text)
        links = fm.get("links") or {}
        gh = links.get("github")
        repo = repo_from_url(gh)
        if repo:
            stars = fetch_stars(repo)
            mapping[repo] = stars
            key = repo
        else:
            key = f.name
            mapping[key] = None
        print(f"Processed {f.name}: {key} -> {mapping.get(key)}")

    # Second pass: write 'stars' into frontmatter of each component file so
    # Jekyll can sort by it during the build.
    for f in files:
        text = f.read_text(encoding="utf-8")
        fm, body = parse_frontmatter_and_body(text)
        links = fm.get("links") or {}
        repo = repo_from_url(links.get("github"))
        stars = mapping.get(repo) if repo in mapping else None
        fm["stars"] = stars
        new_fm = yaml.safe_dump(fm, sort_keys=False).strip()
        new_text = f"---\n{new_fm}\n---\n{body}"
        f.write_text(new_text, encoding="utf-8")

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(mapping, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_FILE} with {len(mapping)} entries and updated component files")


if __name__ == "__main__":
    main()
