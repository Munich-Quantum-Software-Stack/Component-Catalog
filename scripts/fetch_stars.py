#!/usr/bin/env python3
"""
Read all Markdown files in _components/, extract `links.github` from YAML frontmatter,
query the GitHub REST API for stargazer counts using GITHUB_TOKEN (if available),
and write a JSON mapping to `assets/js/github-stars.json`.

This script is intended to be run from CI (GitHub Actions). It prints a short
summary and writes the JSON file. It does not commit — the workflow will do that.
"""
import os
import re
import sys
import json
from pathlib import Path

try:
    import requests
    import yaml
except Exception:
    print("Missing dependencies. Install with: pip install requests pyyaml", file=sys.stderr)
    raise

ROOT = Path(__file__).resolve().parents[1]
COMPONENTS_DIR = ROOT / "_components"
OUT_FILE = ROOT / "assets" / "js" / "github-stars.json"

GITHUB_API = "https://api.github.com/repos/{owner}/{repo}"
TOKEN = os.environ.get("GITHUB_TOKEN")

def parse_frontmatter(md_text):
    # Extract YAML frontmatter between leading '---' blocks
    m = re.match(r"^---\n(.*?)\n---\n", md_text, re.S)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except Exception as e:
        print(f"Failed to parse frontmatter: {e}")
        return {}

def repo_from_url(url):
    if not url:
        return None
    m = re.search(r"github\.com/([^/]+)/([^/]+)", url)
    if not m:
        return None
    owner = m.group(1)
    repo = m.group(2).rstrip(".git")
    return f"{owner}/{repo}"

def fetch_stars(owner_repo):
    owner, repo = owner_repo.split("/")
    url = GITHUB_API.format(owner=owner, repo=repo)
    headers = {"Accept": "application/vnd.github.v3+json"}
    if TOKEN:
        headers["Authorization"] = f"token {TOKEN}"
    r = requests.get(url, headers=headers, timeout=20)
    if r.status_code == 200:
        data = r.json()
        return data.get("stargazers_count")
    else:
        print(f"Warning: failed to fetch {owner_repo}: {r.status_code} {r.text}")
        return None

def main():
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
        key = None
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
