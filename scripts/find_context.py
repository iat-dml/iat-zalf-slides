#!/usr/bin/env python3
"""List project context files a slide deck should draw on.

  python find_context.py [start_dir]

Walks up from start_dir to the repository root (the first directory holding
.git, or four levels at most) and two levels down, and prints every context
file found with its size and first heading. Read the relevant ones before
outlining the deck; they hold the project's own terms, aims and facts.
"""
from __future__ import annotations

import sys
from pathlib import Path

NAMES = ["CONTEXT.md", "README.md", "CLAUDE.md", "AGENTS.md", "GLOSSARY.md", "glossary.md",
         "_quarto.yml", "_brand.yml", "CITATION.cff", "DESCRIPTION"]
GLOBS = ["*.bib", "docs/*.md", "context/*.md", "notes/*.md"]
SKIP = {".git", "node_modules", "_site", "_extensions", ".quarto", "renv", "venv", ".venv", "vendor", "__pycache__"}


def first_heading(p: Path) -> str:
    try:
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines()[:40]:
            s = line.strip().lstrip("\ufeff")
            if s.startswith("#"):
                return s.lstrip("# ").strip()[:80]
            if s.lower().startswith("title:"):
                return s[6:].strip().strip("\"'")[:80]
    except OSError:
        pass
    return ""


def main() -> int:
    start = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    ups, d = [start], start
    for _ in range(4):
        if (d / ".git").exists() or d.parent == d:
            break
        d = d.parent
        ups.append(d)
    root = ups[-1]
    found: dict[Path, None] = {}
    for d in ups:
        for n in NAMES:
            if (d / n).is_file():
                found[d / n] = None
        for g in GLOBS:
            for p in sorted(d.glob(g)):
                found[p] = None
    for p in sorted(start.rglob("*")):
        rel = p.relative_to(start).parts
        if len(rel) > 3 or any(part in SKIP for part in rel):
            continue
        if p.is_file() and p.name in ("CONTEXT.md", "README.md", "GLOSSARY.md", "glossary.md"):
            found[p] = None
    print(f"start: {start}\nroot:  {root}\n")
    if not found:
        print("No context files found. Ask the user for source material (paper, report, notes, data).")
        return 0
    for p in found:
        kb = p.stat().st_size / 1024
        print(f"{kb:7.1f} kB  {p}   {first_heading(p)}")
    print("\nRead CONTEXT.md and README.md first; open the others only if the deck needs them.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
