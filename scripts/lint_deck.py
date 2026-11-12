#!/usr/bin/env python3
"""Check a finished deck against the IAT / ZALF anti-pattern list.

  python lint_deck.py deck.pptx
  python lint_deck.py slides.qmd [extra.css ...]
  python lint_deck.py index.html css/deck.css

Reports findings per slide. FAIL lines are things the skill rules out; WARN
lines need a look and may be fine. Exit status is 1 if any FAIL is reported.
The linter catches the mechanical tells only. It cannot judge whether a slide
says anything, so it supplements reading the deck, it does not replace it.
See references/anti-patterns.md for the reasoning behind each check.
"""
from __future__ import annotations

import html as htmllib
import re
import sys
from pathlib import Path

ACRONYM_OK = re.compile(r"^(?:[A-ZÄÖÜ0-9]{2,6}|[A-Z][a-z]?[A-Z0-9]+)s?$")   # ZALF, IAT, FAIR, DMP, CO2, pH ...

PHRASES = [
    # English
    r"\bleverag\w+", r"\bunlock\w*", r"\bempower\w*", r"\bseamless\w*", r"\bholistic\w*", r"\bsynerg\w+",
    r"\bgame[- ]chang\w+", r"\bcutting[- ]edge\b", r"\bstate[- ]of[- ]the[- ]art\b", r"\bdeep dive\b",
    r"\bjourney\b", r"\blandscape of\b", r"\bdelve\w*", r"\btapestry\b", r"\bparadigm shift\b",
    r"\bat the heart of\b", r"\bin today'?s\b", r"\bfast[- ]paced\b", r"\bever[- ]evolving\b",
    r"\bit'?s (?:important|worth) (?:to note|noting)\b", r"\bat a glance\b", r"\bkey takeaways?\b",
    r"\bthe road ahead\b", r"\bnext[- ]level\b", r"\bsupercharg\w+", r"\brevolutioni[sz]\w+",
    r"\btransformative\b", r"\bgroundbreaking\b", r"\bpivotal\b", r"\bfoster(?:s|ing)?\b", r"\bunderscor\w+",
    r"\bnot (?:just|only|merely)\b[^.?!\n]{0,60}\bbut\b", r"\bmore than just\b",
    r"\bwhy (?:it|this) matters\b", r"\blet'?s (?:dive|explore|unpack)\b",
    # German
    r"\bganzheitlich\w*", r"\bnahtlos\w*", r"\bSynergie\w*", r"\bzukunftsweisend\w*", r"\bwegweisend\w*",
    r"\binnovativ\w*", r"\bGamechanger\b", r"\bDeep Dive\b", r"\bMehrwert\w*", r"\bLeuchtturm\w*",
    r"\bnicht nur\b[^.?!\n]{0,60}\bsondern auch\b", r"\bauf einen Blick\b", r"\bKey Takeaways?\b",
    r"\bin der heutigen\b", r"\bschnelllebig\w*", r"\bSpannend\w*\b", r"\bReise\b",
]
PHRASE_RE = re.compile("|".join(PHRASES), re.IGNORECASE)
TITLE_FORMULA = [
    (re.compile(r"^(?:from|von)\b.+\b(?:to|zu[mr]?)\b", re.I), "'From X to Y' title"),
    (re.compile(r"^(?:beyond|jenseits)\b", re.I), "'Beyond X' title"),
    (re.compile(r"^(?:unlocking|rethinking|reimagining|introducing|meet)\b", re.I), "slogan-style opener"),
    (re.compile(r"^(?:the|der|die|das) (?:big picture|bottom line|challenge|opportunity|vision)\b", re.I), "generic label title"),
    (re.compile(r"\?$"), "question as title (state the answer instead)"),
    (re.compile(r"^[^:]{3,40}: .{3,}$"), "'Label: phrase' title (check it is not a slogan)"),
]
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B50\u2B06\u2705\u274C]")
STOP = {"a", "an", "and", "as", "at", "but", "by", "for", "in", "of", "on", "or", "the", "to", "vs", "via", "with", "from", "per"}


def caps_run(text: str) -> str | None:
    """Return a run of two or more shouted words (not acronyms), if any."""
    words = re.findall(r"[A-Za-zÄÖÜäöüß][A-Za-zÄÖÜäöüß\-]*", text)
    run: list[str] = []
    for w in words:
        if len(w) >= 3 and w.upper() == w and not (ACRONYM_OK.match(w) and len(w) <= 5):
            run.append(w)
            if len(run) >= 2:
                return " ".join(run)
        elif not (w.upper() == w):
            run = []
    one = [w for w in words if len(w) >= 7 and w.upper() == w]
    return one[0] if one and len(words) <= 4 else None


def title_case(text: str) -> bool:
    words = [w for w in re.findall(r"[A-Za-z][A-Za-z\-']*", text)]
    body = [w for w in words[1:] if w.lower() not in STOP and not ACRONYM_OK.match(w)]
    return len(words) >= 4 and len(body) >= 3 and sum(w[0].isupper() for w in body) / len(body) >= 0.8


class Report:
    def __init__(self):
        self.items: list[tuple[str, str, str]] = []

    def add(self, level: str, where: str, msg: str):
        self.items.append((level, where, msg))

    def text_checks(self, where: str, text: str, lang: str, is_title: bool = False):
        t = " ".join(text.split())
        if not t:
            return
        # "[TO CONFIRM: ...]" is the skill's own marker for missing facts, not slide text.
        c = caps_run(re.sub(r"\[\s*TO CONFIRM\b[^\]]*\]", " ", t))
        if c:
            self.add("FAIL", where, f"all-caps text: '{c}'")
        for m in PHRASE_RE.finditer(t):
            self.add("FAIL", where, f"stock phrase: '{m.group(0)}'")
        if "\u2014" in t:
            self.add("WARN", where, "em dash; use a comma, colon or full stop (German: Halbgeviertstrich with spaces)")
        if EMOJI.search(t):
            self.add("FAIL", where, "emoji")
        if is_title:
            if lang == "en" and title_case(t):
                self.add("WARN", where, f"Title Case heading; use sentence case unless it is a proper name: '{t[:60]}'")
            for rx, label in TITLE_FORMULA:
                if rx.search(t):
                    self.add("WARN", where, f"{label}: '{t[:60]}'")
            if len(t.split()) <= 2 and not ACRONYM_OK.match(t.replace(" ", "")):
                self.add("WARN", where, f"topic label as title; say what the slide shows: '{t}'")

    def finish(self) -> int:
        fails = sum(1 for l, _, _ in self.items if l == "FAIL")
        for level, where, msg in self.items:
            print(f"{level}  {where}: {msg}")
        print(f"\n{fails} FAIL, {len(self.items) - fails} WARN")
        return 1 if fails else 0


# ----------------------------------------------------------------------- pptx

def lint_pptx(path: Path, rep: Report):
    from pptx import Presentation
    from pptx.enum.shapes import MSO_SHAPE_TYPE
    from pptx.util import Pt

    prs = Presentation(str(path))
    lang = "de" if any("Datum:" in (sh.text_frame.text if sh.has_text_frame else "")
                       for l in prs.slide_layouts for sh in l.shapes) else "en"
    first_text = ""
    for n, slide in enumerate(prs.slides, 1):
        where = f"slide {n}"
        rounded = bars = 0
        words = 0
        for sh in slide.shapes:
            w, h = (sh.width or 0) / 914400, (sh.height or 0) / 914400
            if sh.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE:
                kind = str(getattr(sh, "auto_shape_type", ""))
                if "ROUNDED" in kind:
                    rounded += 1
                if (0 < w < 0.09 and h > 0.3) or (0 < h < 0.09 and w > 0.3):
                    bars += 1
            if not sh.has_text_frame:
                continue
            is_title = sh.is_placeholder and "TITLE" in str(sh.placeholder_format.type)
            txt = sh.text_frame.text
            if n == 1:
                first_text += " " + txt
            if n == 1 or (n == len(prs.slides) and is_title):
                rep.text_checks(where, txt, lang)            # template wording on title / closing slide
            else:
                rep.text_checks(where, txt, lang, is_title)
            words += len(txt.split())
            for p in sh.text_frame.paragraphs:
                for r in p.runs:
                    if r.font.size is not None and r.font.size < Pt(12) and r.text.strip() and n > 1 \
                            and r.font.size > Pt(9.5):
                        rep.add("WARN", where, f"text below 12 pt ({r.font.size.pt:g} pt): '{r.text[:40]}'")
                    if r.font.name and "segoe" not in r.font.name.lower() and not r.font.name.startswith("+"):
                        rep.add("FAIL", where, f"font outside the template: {r.font.name}")
        if rounded >= 3:
            rep.add("WARN", where, f"{rounded} rounded rectangles; check for a card grid")
        if bars:
            rep.add("FAIL", where, f"{bars} thin bar shape(s); accent stripes and title underlines are out")
        if words > 90 and n > 1:
            rep.add("WARN", where, f"{words} words; split the slide or move detail to the notes")
    if "Claude" not in first_text:
        rep.add("FAIL", "slide 1", "AI attribution missing ('... assistance of Claude')")


# ----------------------------------------------------------------- html / qmd

CSS_CHECKS = [
    (re.compile(r"text-transform\s*:\s*uppercase", re.I), "FAIL", "text-transform: uppercase"),
    (re.compile(r"letter-spacing\s*:\s*0?\.(?:0[5-9]|[1-9])\d*em", re.I), "WARN", "wide letter-spacing (eyebrow styling)"),
    (re.compile(r"border-(?:left|right|top)\s*:\s*[2-9]px\s+solid", re.I), "WARN", "single-edge border (accent stripe on a card)"),
    (re.compile(r"border-radius\s*:\s*(?:9999px|[2-9]\d\d?px|50%)", re.I), "WARN", "pill / circle shape; check it is not decoration"),
    (re.compile(r"box-shadow\s*:(?!\s*none)", re.I), "WARN", "box-shadow"),
    (re.compile(r"(?:linear|radial)-gradient\(", re.I), "WARN", "gradient outside the theme"),
    (re.compile(r"font-family\s*:\s*[\"']?(?!var\(|inherit|Segoe|system-ui|Cascadia|Consolas|ui-monospace|monospace)[A-Za-z]", re.I),
     "WARN", "font-family other than the theme's"),
    (re.compile(r"font-style\s*:\s*italic[^}]*font-family[^}]*serif", re.I | re.S), "FAIL", "italic serif flourish"),
]


def lint_css(where: str, css: str, rep: Report):
    for rx, level, label in CSS_CHECKS:
        hits = rx.findall(css)
        if hits:
            rep.add(level, where, f"{label} ({len(hits)}x)")


def lint_html(path: Path, rep: Report):
    raw = path.read_text(encoding="utf-8", errors="replace")
    lang = "de" if re.search(r'<html[^>]*lang="de', raw) else "en"
    for i, css in enumerate(re.findall(r"<style[^>]*>(.*?)</style>", raw, re.S), 1):
        lint_css(f"{path.name} <style> {i}", css, rep)
    lint_css(f"{path.name} inline styles", " ".join(re.findall(r'style="([^"]*)"', raw)), rep)
    body = re.sub(r"<(script|style)\b.*?</\1>", " ", raw, flags=re.S)
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.S)
    sections = re.findall(r"<section\b[^>]*>(.*?)</section>", body, re.S) or [body]
    for n, sec in enumerate(sections, 1):
        sec = re.sub(r'<span class="l-(?:de|en)">.*?</span>', " ", sec, flags=re.S) if n == 1 else sec
        sec = re.sub(r"<aside\b.*?</aside>", " ", sec, flags=re.S)
        where = f"slide {n}"
        for h in re.findall(r"<h[12]\b[^>]*>(.*?)</h[12]>", sec, re.S):
            t = htmllib.unescape(re.sub(r"<[^>]+>", " ", h))
            if n > 1:
                rep.text_checks(where, t, lang, is_title=True)
        if re.search(r'class="[^"]*\b(?:eyebrow|kicker|overline|pill|badge|chip|tag)\b', sec):
            rep.add("FAIL", where, "eyebrow / pill / badge element")
        rest = htmllib.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<h[12]\b.*?</h[12]>", " ", sec, flags=re.S)))
        rep.text_checks(where, rest, lang)
        if len(rest.split()) > 110 and n > 1:
            rep.add("WARN", where, f"{len(rest.split())} words; split the slide or move detail to the notes")
    if "Claude" not in (sections[0] if sections else ""):
        rep.add("FAIL", "slide 1", "AI attribution missing ('... assistance of Claude')")


def lint_qmd(path: Path, rep: Report):
    raw = path.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\n(.*?)\n---\n", raw, re.S)
    front, body = (m.group(1), raw[m.end():]) if m else ("", raw)
    lang = "de" if re.search(r"^lang:\s*de", front, re.M) else "en"
    if re.search(r"ai-note:\s*false", front):
        rep.add("FAIL", "front matter", "ai-note is false; the Claude attribution is required")
    lint_css(f"{path.name} inline styles", " ".join(re.findall(r'style="([^"]*)"', body)), rep)
    body = re.sub(r"```\{?=?(?:css|html)\}?.*?```", lambda mm: (lint_css(f"{path.name} raw block", mm.group(0), rep) or ""), body, flags=re.S)
    body = re.sub(r":::\s*\{\.notes\}.*?:::", " ", body, flags=re.S)
    n = 1
    chunks = re.split(r"^(#{1,2} .*)$", body, flags=re.M)
    for i in range(1, len(chunks), 2):
        n += 1
        where = f"slide {n}"
        title = re.sub(r"\{.*?\}\s*$", "", chunks[i].lstrip("# ")).strip()
        rep.text_checks(where, title, lang, is_title=True)
        text = re.sub(r"[#*_`>|:\-]{1,}", " ", re.sub(r"\{[^}]*\}", " ", chunks[i + 1]))
        rep.text_checks(where, text, lang)
        if re.search(r"\.(?:eyebrow|kicker|overline|pill|badge|chip)\b", chunks[i + 1]):
            rep.add("FAIL", where, "eyebrow / pill / badge element")
        if len(text.split()) > 110:
            rep.add("WARN", where, f"{len(text.split())} words; split the slide or move detail to the notes")


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    rep = Report()
    for arg in sys.argv[1:]:
        p = Path(arg)
        ext = p.suffix.lower()
        if ext == ".pptx":
            lint_pptx(p, rep)
        elif ext in (".html", ".htm"):
            lint_html(p, rep)
        elif ext in (".qmd", ".md"):
            lint_qmd(p, rep)
        elif p.name == "zalf-iat.css":
            continue                                         # the theme itself
        elif ext in (".css", ".scss"):
            lint_css(p.name, p.read_text(encoding="utf-8", errors="replace"), rep)
        else:
            print(f"skipped {p} (unsupported type)")
    return rep.finish()


if __name__ == "__main__":
    sys.exit(main())
