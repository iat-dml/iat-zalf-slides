# Brands: IAT and ZALF

The Innovation Centre for Agricultural System Transformation (IAT) is part of the Leibniz
Centre for Agricultural Landscape Research (ZALF). Its slide design is ZALF's with a few
IAT-specific additions. The helper scripts apply everything below; this file is for choosing
a brand and for composing slide content that fits it.

## Which design

| Design | Use for |
|---|---|
| **IAT** | Work of the IAT: its projects, living labs, service working groups, partner universities |
| **ZALF** | Institute-wide topics, other ZALF research areas, committees and central services |
| **Zukunft Land** | IAT's public-facing platform for non-scientists. **Not available yet.** Tell the user, and offer IAT or ZALF. Do not improvise a Zukunft Land look from the logo. |

If a deck could be either, ask. Do not infer the brand from the repository name alone.

## What both designs share

- 16:9 canvas. PowerPoint: 10 × 5.625 in. reveal.js: 1280 × 720 px.
- **Title slide:** white header with the institution's name left and logo right, a green
  hero block carrying title, subtitle, authors and date in white, a white footer.
- **Content slides, PowerPoint:** a green banner across the top carrying the slide title in
  white, with the Leibniz Association and ZALF marks at its right end. White body. Slide
  number bottom right.
- **Content slides, reveal.js:** no banner, as in the existing IAT and ZALF reveal.js decks.
  The slide title is a dark-teal heading on white; the ZALF mark (IAT: ZALF-IAT mark) sits
  small in the bottom-right corner; slide number bottom left.
- **Closing slide:** PowerPoint: banner with the thanks line, contact line beneath.
  reveal.js: full-slide hero gradient with the thanks line and the contact line in white.
  Section dividers in reveal.js use the same gradient.
- Typeface Segoe UI (regular) and Segoe UI Semibold. No other typeface or weight.
- Left-aligned text throughout.

## Where they differ

| | IAT | ZALF |
|---|---|---|
| Title slide logo (header, right) | PowerPoint: ZALF mark, with the ZALF-IAT mark on the hero photo. reveal.js: ZALF-IAT mark | ZALF mark |
| Title slide footer | Partner row (Universität Kassel, Justus-Liebig-Universität Gießen, Hochschule Geisenheim University) and the Leibniz Association mark | Empty (date line in PowerPoint) |
| Content slides, PowerPoint | ZALF-IAT mark at the left of the banner, title moved clear of it | Title starts at the left edge |
| Corner mark, reveal.js | ZALF-IAT mark | ZALF mark |
| Funders on external decks | Federal ministry, Land Brandenburg, Land Hessen | Federal ministry, Land Brandenburg |

## Internal or external

- **External** (conferences, partners, funders, the public, anything published): the funder
  logos appear on the title slide under "Funded by:" / "Gefördert durch:".
- **Internal** (group meetings, status seminars, committees): no funder logos. IAT decks keep
  the partner row and the Leibniz mark.

If the user is unsure, a deck that will be shared outside ZALF or put online is external.

## Language

The frame's fixed wording follows the deck language. The helpers set it; listed here so the
same wording is used anywhere else it is needed.

| | English | German |
|---|---|---|
| Institution | Leibniz Centre for Agricultural Landscape Research (ZALF) | Leibniz-Zentrum für Agrarlandschaftsforschung (ZALF) e. V. |
| IAT, full name | Innovation Centre for Agricultural System Transformation (IAT) | Innovationszentrum für Agrarsystemtransformation (IAT) |
| Date label | Date: | Datum: |
| Partner label | IAT partners: | IAT-Partner: |
| Funder label | Funded by: | Gefördert durch: |
| Closing | Thank you for your attention. | Vielen Dank für Ihre Aufmerksamkeit. |
| Contact label | Contact: | Kontakt: |
| Deck attribution | Presentation created with the assistance of Claude | Präsentation mit Unterstützung von Claude erstellt |
| Image attribution | AI-generated image (tool) | KI-generiertes Bild (Tool) |
| Source label | Source: | Quelle: |

Dates are written DD.MM.YYYY in both languages, as in the templates.

## Colour

The two formats carry slightly different values for the same colours, because the PowerPoint
theme (`ZALF_PPT_2020`) and the Quarto brand files were defined separately. Use each
format's own values; do not mix them within a deck.

| Role | PowerPoint theme | reveal.js / Quarto | Use |
|---|---|---|---|
| Dark teal (primary) | `356259` | `#356259` | Emphasis, in-body headings, table header rules, first chart series |
| Banner / hero gradient | template artwork | `#326158` → `#39463E` | The frame only |
| Green | `3AAE6C` | `#46A84F` (ZALF green), `#36AE6C` | Large shapes and chart series. Not for small text: ZALF green on white is below 4.5:1, and on the dark gradient about 2.3:1. |
| Teal | `60ACAC` | `#80BDBD` | Chart series, tints |
| Olive | `9DAE21` | `#B1BE4D` | Chart series, a single highlight |
| Sage | `7E9862`, light `91A878` | `#657A4E`, light `#9EBC83` | Chart series; bullets use the light sage |
| Dark | `252F2A`, slate `38463F` | slate `#465555` | Chart series, secondary text |
| Text | `000000` | `#111111` | Body text |
| Grey | `6C6C6C` | `#6C6C6C` | Captions, sources, attribution |

IAT service colours, for content about the three service strata only: Support `#2D6A4F`,
Transfer `#458484`, Integration `#C18F59`. As text on white use the darker `#3E7777` and
`#906436` for Transfer and Integration; the fill colours do not reach 4.5:1.

How to use colour:

- Black text on white. Dark teal is the one emphasis colour.
- At most one further accent on a slide, and only where it separates something the audience
  must tell apart.
- Chart series in this order, which also separates in greyscale: dark teal, olive, teal,
  sage, near-black, green (`CHART_COLORS` in `pptx_deck.py`).
- White text only on the banner, hero, divider and closing gradient. White on ZALF green fails contrast.
- No tints, gradients or fills as decoration. See `anti-patterns.md`.

## Type sizes

| Element | PowerPoint | reveal.js |
|---|---|---|
| Slide title | 18 pt semibold in the banner, from the template | 38 px semibold, dark teal |
| In-body heading | 16 pt semibold | 28 px semibold, dark teal |
| Body text and bullets | 16 pt | 28 px |
| Small text, tables | 12 pt minimum | 22 px minimum |
| Captions | 12 pt (template); credits and sources 9 pt grey | 18 px; sources 16 px grey |

The PowerPoint canvas is 5.625 in. high, so 16 pt there reads like roughly 21 pt on a
7.5 in. slide. Do not enlarge it to "standard" sizes.

## Logos

All logo files are in `assets/logos/`. The frame places them; content slides get no
additional logos.

- Do not recolour, stretch, crop or add effects to any logo.
- White logo variants go on the green gradient only; colour variants on white only.
- Partner and funder logos keep the relative sizes the templates give them.
- Project or third-party logos a deck needs (a tool, a partner institution) go in the slide
  body at a modest size, never in the banner, the title area or the title-slide header.

The funder logos are:

| File | Funder |
|---|---|
| `bmel.png` | Federal Ministry of Agriculture, Food and Regional Identity (BMLEH; until 2025 the Federal Ministry of Food and Agriculture). English version. |
| `brandenburg.png` | Land Brandenburg, Ministry for Science, Research and Culture (MWFK) |
| `hessen.png` | Land Hessen |

The federal and Hessen files match the IAT PowerPoint template of November 2026 and the ZALF
poster template of July 2026. Ministries are
renamed from time to time; if the user says a logo is out of date, replace the file in
`assets/logos/funders/` (and in `assets/revealjs/_extensions/zalf-iat/assets/funders/`) and
keep the file name.
