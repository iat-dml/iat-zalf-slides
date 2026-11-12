# iat-zalf-slides

A Claude skill for making slide decks in the institutional design of the Innovation Centre
for Agricultural System Transformation (IAT) and the Leibniz Centre for Agricultural
Landscape Research (ZALF): PowerPoint, Quarto revealjs or plain reveal.js, in English or
German.

Status: version 0.1, first draft. See [Open points](#open-points).

## What it does

When asked for slides, Claude

1. asks for the design (IAT or ZALF), language, audience (internal or external), format,
   title, subtitle and authors;
2. looks for project context files (`CONTEXT.md`, `README.md`, glossaries);
3. agrees an outline;
4. builds the deck on the institutional frame, using the scripts in `scripts/`;
5. adds the attribution "Presentation created with the assistance of Claude" to the title
   slide and a credit to every AI-generated image;
6. checks the result against a list of machine-made-slide patterns
   (`references/anti-patterns.md`, `scripts/lint_deck.py`).

External decks carry the funders' logos on the title slide. Zukunft Land is not supported
yet.

## Install

**Claude Code.** Clone into a skills directory; the folder name must be `iat-zalf-slides`.

```
# for all your projects
git clone https://github.com/<org>/iat-zalf-slides %USERPROFILE%\.claude\skills\iat-zalf-slides

# or for one repository, shared with everyone who clones it
git clone https://github.com/<org>/iat-zalf-slides .claude/skills/iat-zalf-slides
```

If the repository lives elsewhere (for example `C:\git\iat-zalf-slides`), a symlink from the
skills directory to it works as well.

**Claude apps.** Upload the packaged `iat-zalf-slides.skill` file under Settings, where
skills are managed.

Requirements on the machine that builds decks: Python 3.9 or later with `python-pptx` for
PowerPoint; Quarto 1.4 or later for the Quarto route; nothing for plain reveal.js.

## Layout

```
SKILL.md                      the instructions Claude follows
references/                   brands, writing, anti-patterns, per-format guides
scripts/pptx_deck.py          builds the PowerPoint frame from the templates
scripts/new_reveal_deck.py    scaffolds a Quarto or plain reveal.js deck
scripts/lint_deck.py          checks a deck against the anti-pattern list
scripts/find_context.py       lists project context files
assets/pptx/                  IAT and ZALF PowerPoint templates
assets/revealjs/              zalf-iat Quarto extension, shared theme, plain starter
assets/logos/, assets/brand/  logos and _brand.yml definitions
evals/                        test prompts with expected outcomes
```

## Using the scripts by hand

```
python scripts/new_reveal_deck.py --kind quarto --brand iat --lang en --audience external ^
    --title "My talk" --author "A. Example" --date "12.11.2026" --out talks/my-talk
python scripts/lint_deck.py talks/my-talk/slides.qmd
```

`scripts/pptx_deck.py` is a module; see `references/pptx.md` for an example build script.

## Sources

| In this repository | Taken from |
|---|---|
| `assets/pptx/iat-template.pptx`, `zalf-template.pptx` | `iat-dml/templates` (`IAT-template-powerpoint.pptx`, `zalf-template-powerpoint-slides.pptx`) |
| `assets/revealjs/_extensions/zalf-iat/` | title slide derived from `iat-dml/templates/iat-revealjs` 1.0.0 (hero artwork unchanged); content, divider and closing slides follow the IAT-ZALF skin of the existing reveal.js decks (`zalf-rdm-system`, `iat-data-policy`) |
| `assets/brand/` | `iat-dml/iat-brand-yml`; `zalf-internal-typst` in `iat-dml/templates` |
| `assets/logos/` | extracted from the PowerPoint templates; `funders/bmel.png` and `funders/hessen.png` from `templates/zalf-poster-typst` (identical to those in the November 2026 IAT PowerPoint template) |
| `assets/revealjs/plain/vendor/reveal/` | reveal.js 5.1.0, MIT licence, © Hakim El Hattab |

When a template changes upstream, replace the file here under the same name. The title-slide
markup exists twice (`_extensions/zalf-iat/title-slide.html` for Quarto and
`plain/index.template.html`); change both together.

## Open points

- **Brandenburg funder.** The federal ministry (now BMLEH) and Hessen logos were updated in
  November 2026 to match the newest IAT PowerPoint template and the ZALF poster template.
  For Brandenburg the two disagree: the slide templates show the Ministry for Science,
  Research and Culture, the poster the Ministry for Agriculture, Environment and Climate
  Protection. The skill keeps the former until confirmed. German-language versions of the
  federal logo exist in the new IAT template but are not used yet. See `REVIEW.md`.
- **Funders per design.** IAT external: federal ministry, Brandenburg, Hessen. ZALF external:
  federal ministry, Brandenburg. The IAT data-policy deck (internal audience) shows the
  funders, which contradicts "internal decks show no funder logos". Undecided.
- **Colours.** The PowerPoint theme (`ZALF_PPT_2020`) and the `_brand.yml` files give
  slightly different values for the same colours. Each format uses its own; the existing
  reveal.js decks use the `_brand.yml` values, which supports this.
- **New IAT PowerPoint template.** `C:\git\templates\iat-powerpoint-template.pptx` (12 Nov
  2026, uncommitted) restructures the layouts. `scripts/pptx_deck.py` still uses the
  previous template; adopting the new one needs script changes. See `REVIEW.md`.
- **Closing slide.** The ZALF lockup on the PowerPoint closing slide is English only. The
  new IAT template has a German IAT lockup.
- **Zukunft Land.** Not implemented. The only brand file found locally is a white
  `logo-zukunft-land.png` in `templates/zalf-poster-typst`.
- **IAT background and glossary.** `SKILL.md` refers to a future skill; update the name there
  once it exists.

## Licence

Copyright © 2026 Leibniz Centre for Agricultural Landscape Research (ZALF) e. V.

The code and documentation in this repository are released under the MIT licence
(see `LICENSE`), with the exceptions below.

**Third-party code.** `assets/revealjs/plain/vendor/reveal/` contains reveal.js 5.1.0,
© 2011–2024 Hakim El Hattab, under the MIT licence (see the `LICENSE` file there).

**Not covered by this licence.** The logos in `assets/logos/` and
`assets/revealjs/_extensions/zalf-iat/assets/` (ZALF, ZALF-IAT, Leibniz Association,
Universität Kassel, Justus-Liebig-Universität Gießen, Hochschule Geisenheim University,
the Federal Ministry of Agriculture, Food and Regional Identity, Land Brandenburg and
Land Hessen), the PowerPoint templates in `assets/pptx/`, and the title-slide artwork
(`title-background-block.png`) are trademarks, official emblems or copyrighted works of
their owners. They are included only so that decks made by these institutions follow
their corporate design. No rights to them are granted. Do not use them for any other purpose.
