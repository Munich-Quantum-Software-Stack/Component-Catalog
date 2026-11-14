#!/usr/bin/env python3
"""Remove the `stars` key from YAML frontmatter of all `_components/*.md` files.

Intended to be used as a pre-commit hook (e.g. via pre-commit). The script
edits files in-place only when necessary and prints a short summary.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMPONENTS_DIR = ROOT / "_components"


def strip_stars_from_text(text: str) -> tuple[str, bool]:
    """Remove the stars entry from a frontmatter.

    Args:
        text (str): The frontmatter text to reformat.

    Returns:
        tuple[str, bool]: The parsed YAML entries.
    """
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not m:
        return text, False
    fm_raw, body = m.group(1), m.group(2)

    # Edit raw frontmatter lines to remove any 'stars:' entry while preserving
    # all other formatting (leading spaces, quoting, list styles).
    lines = fm_raw.splitlines(keepends=True)
    pattern = re.compile(r"^\s*stars\s*:\s*.*$")
    new_lines = [ln for ln in lines if not pattern.match(ln.rstrip("\r\n"))]

    if len(new_lines) == len(lines):
        # nothing removed
        return text, False

    # Reconstruct frontmatter preserving original line endings/layout
    new_fm_raw = "".join(new_lines).rstrip("\n\r")
    new_text = f"---\n{new_fm_raw}\n---\n{body}"
    return new_text, True


def main() -> int:
    """Main entry point.

    Returns:
        int: 1 if files were modified, otherwise 0.
    """
    md_files = sorted(COMPONENTS_DIR.glob("*.md"))
    changed = []
    for p in md_files:
        text = p.read_text(encoding="utf-8")
        new_text, modified = strip_stars_from_text(text)
        if modified:
            p.write_text(new_text, encoding="utf-8")
            changed.append(str(p))

    if changed:
        print("Removed 'stars' from frontmatter in:")
        for c in changed:
            print(" - ", c)
        # Exit non-zero to make pre-commit fail and let user re-run commit/inspect
        return 1

    print("No 'stars' keys found in component frontmatter.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
