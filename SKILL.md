---
name: iat-zalf-slides
description: Create slide decks in the institutional design of the Innovation Centre for Agricultural System Transformation (IAT) or the Leibniz Centre for Agricultural Landscape Research (ZALF), as PowerPoint (.pptx), Quarto revealjs or plain reveal.js, in English or German, with a scientific tone and without the usual signs of machine-made slides. Use this skill whenever someone at IAT or ZALF asks for slides, a presentation, a talk, a deck, a Vortrag, Folien or a Präsentation, including status seminar talks, committee and working-group updates, conference talks and anything for Zukunft Land, and whenever a request mentions IAT, ZALF, the DML working group, living labs / Reallabore or an iat-dml repository together with slides, even if no format or branding is named. Also use it to restyle or extend an existing IAT or ZALF deck. It takes precedence over general presentation and PowerPoint skills for these decks.
---

# IAT and ZALF slide decks

This skill produces decks that look and read as if one careful colleague made all of them:
the same institutional frame every time, content written the way a scientist presents, and
none of the stock devices that mark slides as generated.

The frame (title slide, banner or heading, logos, closing slide, labels, attribution) is built by the
scripts in `scripts/` from the institutions' own templates. Never draw it by hand. Your work
is the content: what the deck argues, what goes on each slide, and how it is worded.

## Workflow

### 1. Ask what is needed

Before writing anything, establish the items below. Ask for all missing ones in a single
round, using the environment's question tool if there is one (multiple choice for the first
four), otherwise a short list. Skip anything the user has already stated. Do not guess the
design or the audience: both change what appears on the title slide.

| Ask | Options |
|---|---|
| Institutional design | IAT · ZALF (Zukunft Land is planned but not available; say so and offer these two) |
| Language | English · German |
| Audience | Internal · External (external decks carry the funders' logos on the title slide) |
| Format | PowerPoint (.pptx) · Quarto revealjs · plain reveal.js |
| Title and subtitle | free text; offer a suggestion if the user has none |
| Author names | as they should appear, with academic titles if wanted |

Also useful if not evident: the occasion and date, how long the talk is, and who will be in
the room. Ask only if the answer would change the deck.

`references/brands.md` explains which design fits which work and what internal and external
mean, if the user is unsure.

### 2. Gather the project's context

Run `python scripts/find_context.py <project dir>`. It lists `CONTEXT.md`, `README.md`,
glossaries, Quarto and brand configuration, and bibliography files from the working
directory up to the repository root. Read `CONTEXT.md` and `README.md` and whatever else the
deck needs. They hold the project's aims, facts and vocabulary; use its terms, not synonyms.

If a skill with background on the IAT and its glossary is available (for example one named
`iat-background` or `iat-glossary`), consult it for institutional facts and preferred terms.
If it is not, do not fill the gap from general knowledge: use the context files and ask the
user for anything missing.

Content comes from the user's material. Never supply a number, citation, name, date or
result that is not in it. Where the deck needs something that is missing, write
`[TO CONFIRM: ...]` in place and report every such marker at the end.

### 3. Agree an outline

Draft the deck as a list: one line per slide with its title and what it will show (text,
which figure, which table). Titles state what the slide shows; see `references/writing.md`.
Size the deck to the talk, about one slide per one and a half to two minutes.

Show the outline and wait for agreement before building, unless the user asked for a finished
deck in one go or the deck is very short. Changing an outline is cheap; rebuilding slides is
not.

### 4. Build

Read the reference for the chosen format, then build:

- **PowerPoint:** `references/pptx.md`. Write a short Python script using
  `scripts/pptx_deck.py`.
- **Quarto revealjs or plain reveal.js:** `references/revealjs.md`. Start the deck with
  `scripts/new_reveal_deck.py`, then add slides.

Before composing slides, read `references/anti-patterns.md` and `references/writing.md`. The
short version:

- Every element carries content. No eyebrows, accent lines, edge-striped cards, icon circles,
  pills, oversized statistic callouts or filler imagery.
- The frame is the only decoration. White body, black text, dark teal for emphasis, Segoe UI.
- Sentence-case titles that state the finding. No slogans, no management vocabulary, no
  "not just X but Y", no em-dash chains.
- One point per slide; detail goes in the speaker notes.
- Real figures, photos and maps from the project, each with its source. If there is none, the
  slide has no image.

A slide with one sentence and one figure is finished. Do not add elements to fill space.

### 5. Attribute AI involvement

- The title slide carries "Presentation created with the assistance of Claude" (German:
  "Präsentation mit Unterstützung von Claude erstellt"). The scripts add it; leave it in.
- Every AI-generated image carries its own credit naming the tool: pass `ai_tool=` to
  `deck.picture()` in PowerPoint, or add the credit line described in
  `references/revealjs.md`. This applies to images the user supplies as AI-generated as well
  as any you generate.
- Photos, maps and third-party figures carry their source and licence in the same place.

### 6. Check, then hand over

1. Run `python scripts/lint_deck.py <deck file>`. Fix every FAIL. Read each WARN and fix it
   or decide it is justified (a proper name in capitals, a genuine "Topic: specification"
   title).
2. Render the deck and look at every slide, as described in the format reference. Fix
   overflow, overlap and titles that wrap past two lines. If nothing in the environment can
   render it, say so plainly.
3. Read the slides once more against `references/anti-patterns.md`; the linter only catches
   the mechanical items.
4. Hand over the file with a short note: design, language, audience and format used; any
   `[TO CONFIRM]` markers; anything you could not verify, such as rendering in PowerPoint
   itself.

## Files

| Path | Purpose |
|---|---|
| `references/brands.md` | IAT and ZALF designs, internal and external, colour, type, logos, fixed wording in both languages |
| `references/writing.md` | Titles, body text, English and German conventions, deck structure |
| `references/anti-patterns.md` | What to avoid in text and design, why, and what to do instead |
| `references/pptx.md` | Building with `pptx_deck.py`; tables, charts, checking |
| `references/revealjs.md` | Quarto and plain reveal.js; markup conventions, custom CSS limits, checking |
| `scripts/find_context.py` | Lists project context files |
| `scripts/pptx_deck.py` | Builds the PowerPoint frame from the templates |
| `scripts/new_reveal_deck.py` | Scaffolds a Quarto or plain reveal.js deck with the frame |
| `scripts/lint_deck.py` | Checks a deck against the anti-pattern list |
| `assets/pptx/` | The IAT and ZALF PowerPoint templates |
| `assets/revealjs/` | The `zalf-iat` Quarto extension, the shared theme and a plain reveal.js starter |
| `assets/logos/`, `assets/brand/` | Logo files and the `_brand.yml` definitions |
