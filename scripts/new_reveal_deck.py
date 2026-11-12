#!/usr/bin/env python3
"""Scaffold an IAT / ZALF reveal.js deck with the institutional frame in place.

  python new_reveal_deck.py --kind quarto --brand iat --lang en --audience external \
      --title "Soil moisture across three living labs" --subtitle "First season" \
      --author "Dr. A. Example" --author "B. Example" --date "12.11.2026" \
      --event "IAT Statusseminar" --out talks/soil-moisture

--kind quarto  writes <out>/slides.qmd and <out>/_extensions/zalf-iat/
               (render with: quarto render slides.qmd)
--kind plain   writes <out>/index.html, <out>/theme/ and <out>/vendor/reveal/
               (open index.html; no build step, works offline)

The script only writes the frame and the title slide. Add the content slides to
slides.qmd or index.html afterwards. It refuses to overwrite an existing deck
file unless --force is given.
"""
from __future__ import annotations

import argparse
import html
import shutil
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
REVEAL = SKILL_DIR / "assets" / "revealjs"
EXT = REVEAL / "_extensions" / "zalf-iat"


THANKS = {"en": "Thank you for your attention.", "de": "Vielen Dank für Ihre Aufmerksamkeit."}
CONTACT = {"en": "Contact:", "de": "Kontakt:"}


def yaml_str(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--kind", choices=["quarto", "plain"], required=True)
    ap.add_argument("--brand", choices=["iat", "zalf"], required=True)
    ap.add_argument("--lang", choices=["en", "de"], required=True)
    ap.add_argument("--audience", choices=["internal", "external"], required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--author", action="append", default=[], help="repeat for several authors")
    ap.add_argument("--date", default="")
    ap.add_argument("--event", default="")
    ap.add_argument("--contact", default="", help="contact line for the closing slide")
    ap.add_argument("--no-ai-note", action="store_true", help="omit the Claude attribution (only if no AI was involved)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    when = " · ".join(x for x in (a.event, a.date) if x)

    if a.kind == "quarto":
        target = out / "slides.qmd"
        if target.exists() and not a.force:
            print(f"{target} exists; use --force to overwrite", file=sys.stderr)
            return 1
        shutil.copytree(EXT, out / "_extensions" / "zalf-iat", dirs_exist_ok=True)
        fm = ["---", f"title: {yaml_str(a.title)}"]
        if a.subtitle:
            fm.append(f"subtitle: {yaml_str(a.subtitle)}")
        if a.author:
            fm.append("author:")
            fm += [f"  - {yaml_str(x)}" for x in a.author]
        fm += [
            f"lang: {a.lang}",
            "format:",
            "  zalf-iat-revealjs:",
            f"    deck-brand: {a.brand}",
            f"    deck-audience: {a.audience}",
            f"    ai-note: {'false' if a.no_ai_note else 'true'}",
            # deck-date is printed as written; Quarto would re-parse a `date:` such as 12.11.2026
            f"    deck-date: {yaml_str(when)}",
            "    embed-resources: false   # true gives one self-contained HTML file to send around",
            "---",
            "",
            "## Slide title stating the finding",
            "",
            "Body text.",
            "",
            "::: {.notes}",
            "Speaker notes.",
            ":::",
            "",
            "## " + THANKS[a.lang] + " {.zi-closing}",
            "",
            CONTACT[a.lang] + " " + (a.contact or "[TO CONFIRM: contact]"),
            "",
        ]
        target.write_text("\n".join(fm), encoding="utf-8")
        print(f"wrote {target}\nrender: quarto render {target}")
        return 0

    target = out / "index.html"
    if target.exists() and not a.force:
        print(f"{target} exists; use --force to overwrite", file=sys.stderr)
        return 1
    shutil.copytree(REVEAL / "plain" / "vendor", out / "vendor", dirs_exist_ok=True)
    theme = out / "theme"
    theme.mkdir(exist_ok=True)
    shutil.copy2(EXT / "zalf-iat.css", theme / "zalf-iat.css")
    shutil.copytree(EXT / "assets", theme / "assets", dirs_exist_ok=True)

    e = html.escape
    page = (REVEAL / "plain" / "index.template.html").read_text(encoding="utf-8")
    ai = "" if a.no_ai_note else (REVEAL / "plain" / "ai-note.html").read_text(encoding="utf-8").rstrip()
    subs = {
        "{{LANG}}": a.lang, "{{BRAND}}": a.brand, "{{AUDIENCE}}": a.audience,
        "{{TITLE}}": e(a.title), "{{AUTHORS}}": e(", ".join(a.author)),
        "{{SUBTITLE_BLOCK}}": f'      <p class="subtitle">{e(a.subtitle)}</p>' if a.subtitle else "",
        "{{DATE_BLOCK}}": f'      <p class="date">{e(when)}</p>' if when else "",
        "{{AI_BLOCK}}": ai, "{{CONTACT}}": e(a.contact or "[TO CONFIRM: contact]"),
    }
    for k, v in subs.items():
        page = page.replace(k, v)
    target.write_text(page, encoding="utf-8")
    print(f"wrote {target}\nopen it in a browser; S = speaker view, F = fullscreen, ?print-pdf for PDF")
    return 0


if __name__ == "__main__":
    sys.exit(main())
