#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pyyaml",
#     "requests",
# ]
# ///
"""Script for fetching GitHub star counts for components.

Read all Markdown files in _components/, extract `links.github` from YAML frontmatter,
query the GitHub REST API for stargazer counts using GITHUB_TOKEN (if available),
and write a JSON mapping to `assets/js/github-stars.json`.

This script is intended to be run from CI (GitHub Actions). It prints a short
summary and writes the JSON file. It does not commit — the workflow will do that.
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


def parse_frontmatter(md_text: str) -> dict:
    """Returns YAML frontmatter between leading '---' blocks."""
    m = re.match(r"^---\n(.*?)\n---\n", md_text, re.DOTALL)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        print(f"Failed to parse frontmatter: {e}")
        return {}


def repo_from_url(url: str) -> str | None:
    """Return extracted owner/repo from a GitHub URL."""
    if not url:
        return None
    m = re.search(r"github\.com/([^/]+)/([^/]+)", url)
    if not m:
        return None
    owner = m.group(1)
    repo = m.group(2).rstrip(".git")
    return f"{owner}/{repo}"


def fetch_stars(owner_repo: str) -> int | None:
    """Return GitHub stargazer count for a repo, or None on error."""
    owner, repo = owner_repo.split("/")
    url = GITHUB_API.format(owner=owner, repo=repo)
    headers = {"Accept": "application/vnd.github.v3+json"}
    if TOKEN:
        headers["Authorization"] = f"token {TOKEN}"
    r = requests.get(url, headers=headers, timeout=20)
    if r.status_code == 200:
        data = r.json()
        return data.get("stargazers_count")
    print(f"Warning: failed to fetch {owner_repo}: {r.status_code} {r.text}")
    return None


def main() -> None:
    """Main entry point."""
    mapping = {}
    files = sorted(COMPONENTS_DIR.glob("*.md"))
    if not files:
        print("No component files found in _components/")
        sys.exit(0)

    for f in files:
        text = f.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        links = fm.get("links") or {}
        gh = links.get("github")
        repo = repo_from_url(gh)
        if repo:
            stars = fetch_stars(repo)
            mapping[repo] = stars
            key = repo
        else:
            # If there's no links.github, skip but keep filename trackable
            key = f.name
            mapping[key] = None
        print(f"Processed {f.name}: {key} -> {mapping.get(key)}")

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(mapping, indent=2), encoding="utf-8")
    print(f"Wrote {OUT_FILE} with {len(mapping)} entries")


if __name__ == "__main__":
    main()
