# Building a reveal.js deck

Two routes share one theme (`zalf-iat.css`), so they look the same. The title slide matches
the PowerPoint templates. Content slides do not carry the PowerPoint banner: they follow the
existing IAT and ZALF reveal.js decks, with a dark-teal heading on white and a small corner
mark (see `brands.md`).

| Route | Choose when | Output |
|---|---|---|
| **Quarto** (`--kind quarto`) | The project already uses Quarto, the deck has code-generated figures, or the user asks for it | `slides.qmd`, rendered with `quarto render` |
| **Plain reveal.js** (`--kind plain`) | No Quarto available, the deck needs custom HTML or animation, or it must run from a folder with no build step | `index.html` with reveal.js 5.1 vendored; works offline |

If the user said only "revealJS", check for `_quarto.yml` or `.qmd` files in the project: use
Quarto if they are there, otherwise ask.

## Start the deck

```bash
python <skill>/scripts/new_reveal_deck.py --kind quarto --brand iat --lang en \
    --audience external --title "..." --subtitle "..." \
    --author "Dr. A. Example" --author "B. Example" \
    --date "12.11.2026" --event "IAT Statusseminar" --out talks/my-talk
```

This writes the frame, the title slide, one content slide and the closing slide. Do not
hand-write the title slide or copy one from another deck. `--contact` fills the contact line
on the closing slide; without it the script writes `[TO CONFIRM: contact]`.

Quarto front matter written by the script:

```yaml
format:
  zalf-iat-revealjs:
    deck-brand: iat            # iat | zalf
    deck-audience: external    # internal | external
    ai-note: true              # leave true
    deck-date: "IAT Statusseminar · 12.11.2026"   # printed as written
    # title-image: field.jpg                 # optional photo in the hero block
    # title-image-credit: "Photo: ZALF"
```

Use `deck-date`, not `date`: Quarto re-parses `date` and turns 12.11.2026 into 11 December.

The extension lives in `_extensions/zalf-iat/` next to the `.qmd`. Asset paths are relative
to the document, so keep the `.qmd` beside `_extensions/`. Inside a Quarto website project,
or to send the deck as one file, set `embed-resources: true`.

## Writing slides

| Need | Quarto | Plain reveal.js |
|---|---|---|
| Content slide; the heading is the slide title | `## Title` | `<section><h2>Title</h2> ... </section>` |
| Section divider (green, full slide) | `# Section name` and an optional line of text | `<section class="zi-divider"><h1>Section name</h1></section>` |
| Two columns | `:::: {.columns}` with `::: {.column width="50%"}` | a two-column CSS grid in a `<div style="display:grid;grid-template-columns:1fr 1fr;gap:40px">` |
| In-body heading | `### Heading` | `<h3>` |
| Source line, bottom left | `::: {.source}` Source: ... `:::` | `<p class="source">Source: ...</p>` |
| Figure with credit | `![Alt text](fig.png)` then `[Photo: ...]{.credit}` | `<figure><img ...><figcaption>...</figcaption></figure>` |
| Full-canvas slide without padding or corner mark | `## {.zi-plain}` | `<section class="zi-plain">` |
| Smaller text (22 px floor) | `[...]{.small}` or `::: {.small}` | `class="small"` |
| Right-aligned numbers in a table | Markdown column alignment | `class="num"` on `td` / `th` |
| Speaker notes | `::: {.notes}` | `<aside class="notes">` |
| Closing slide (gradient, white text) | `## Thank you for your attention. {.zi-closing}` plus the contact line; already in the starter | `<section class="zi-closing">`; already in the starter |

The theme provides type sizes, bullets, tables, figures, links and code. Write content in
those; do not restyle them per slide.

### Custom styling

Some decks need a layout the theme does not have. Put the rules in a `deck.css` next to the
deck (Quarto: `css: [deck.css]` under the format; plain: one more `<link>` after the theme),
and keep to these limits:

- Use the theme's custom properties (`--zi-teal-dark`, `--zi-gray`, `--zi-tint`, ...), not new
  colours or fonts.
- No `text-transform: uppercase`, wide letter-spacing, single-edge borders, pills, shadows or
  gradients. `lint_deck.py` reads CSS files passed to it and flags these.
- Do not restyle the slide title, corner mark, title slide, dividers or closing slide.

### Figures and AI-generated images

Code-generated figures use the palette from `brands.md`, a white background and text sized
for a slide. Every AI-generated image gets a credit line naming it as such, in the deck
language: `AI-generated image (tool)` / `KI-generiertes Bild (Tool)`. Photos and third-party
figures get their source and licence in the same place.

## Checking the result

1. `python <skill>/scripts/lint_deck.py slides.qmd` (or `index.html`), adding any `deck.css`.
2. Render (`quarto render slides.qmd`) and look at the slides. If a headless browser is
   available (for example Playwright), screenshot each slide at 1280 × 720; otherwise open
   the file, or ask the user to. Check: titles that wrap past two lines, text
   running off the bottom or into the source line, images overflowing, the right brand and
   funder logos on the title slide.
3. PDF: open with `?print-pdf` appended to the URL and print from the browser.

## Speaker keys

Arrows or space to advance, `S` speaker view, `F` fullscreen, `Esc` overview.
