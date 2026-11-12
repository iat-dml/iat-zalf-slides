# Building a PowerPoint deck

The institutional templates are in `assets/pptx/`. `scripts/pptx_deck.py` opens the right
one and builds the frame: title slide, banner, logos, slide numbers, closing slide, language
labels, funder logos, attribution. You compose the body of each slide.

Do not rebuild the frame with pptxgenjs or from a blank presentation, and do not edit the
templates' layouts. Decks that share one frame are what makes them consistent.

Requires `python-pptx` (`pip install python-pptx`).

## Build script

Write a short Python script next to the output and run it. Keep the script: the user can
re-run it after edits.

```python
import sys
sys.path.insert(0, "<path to this skill>/scripts")
from pptx_deck import Deck, BODY, PALETTE, CHART_COLORS

deck = Deck(brand="iat", lang="en", audience="external")     # brand: iat | zalf

deck.title_slide(
    "Soil moisture across three living labs",
    subtitle="First season of sensor data, March to October 2026",
    authors=["Dr. A. Example", "B. Example"],
    date="12.11.2026", event="IAT Statusseminar",
    # photo="field.jpg", photo_credit="Photo: A. Example / ZALF",   # optional
)

s = deck.slide("Sensors were installed at 42 plots between March and May")
deck.text(s, ["Loam sites: 18 plots, two depths",
              "Sandy sites: 24 plots, three depths"], bullets=True, w=4.6)
deck.picture(s, "map.png", x=5.2, y=1.2, w=4.5, credit="Map: ZALF, basemap © GeoBasis-DE")
deck.source(s, "Example et al. (2026)")
deck.notes(s, "What to say aloud.")

deck.closing_slide(contact="Dr. A. Example, a.example@zalf.de")
deck.save("soil-moisture.pptx")
```

## Helper reference

| Call | What it does |
|---|---|
| `Deck(brand, lang, audience, ai_assisted=True)` | Opens the template. `audience="external"` shows funder logos on the title slide. |
| `title_slide(title, subtitle, authors, date, event, photo, photo_credit)` | Fills the template's title slide. Call first, once. Adds the Claude attribution. |
| `slide(title, layout="title-only")` | Content slide with the title in the banner; returns the python-pptx slide. `layout="standard"` gives the template's placeholders (headline, text, bullets, picture, caption) via `placeholders(slide)`; call `drop_empty_placeholders(slide)` afterwards. |
| `text(slide, content, x, y, w, h, size=16, bold=False, color="black", bullets=False)` | Text box in the template's type. `content` is a string or a list of paragraphs. Defaults to the whole body area. `color` takes a `PALETTE` name or hex. |
| `picture(slide, path, x, y, w, h, credit, ai_tool)` | Image with a credit line beneath. Pass `ai_tool="..."` for an AI-generated image; the attribution is added in the deck language. |
| `table(slide, rows, x, y, w, col_widths, size=14, numeric=())` | Plain table; first row is the header; `numeric` lists right-aligned columns. |
| `style_chart(chart, y_title, size=12)` | Palette and quiet frame for a native python-pptx chart. |
| `source(slide, text)` | Source line bottom-left, prefixed "Source:" / "Quelle:". |
| `notes(slide, text)` | Speaker notes. |
| `closing_slide(contact, title=None)` | Template closing slide with the contact line. |
| `save(path)` | Removes the template's sample slides and writes the file. |

`deck.prs` is the underlying python-pptx `Presentation` for anything else.

## Body area

All measurements are inches. The body runs from `BODY["x"]` 0.24 to 9.74 and from
`BODY["y"]` 1.16 to 4.91. The banner occupies the top 0.93 in.; the slide number sits at the
bottom right, the source line at the bottom left. Keep content inside the body area and off
the banner.

Useful splits: text column 0.24 to 4.84 with a figure from 5.2 to 9.74; or a full-width
figure 9.5 in. wide and up to 3.6 in. high.

## Tables and charts

Use native tables and charts so colleagues can edit them.

```python
from pptx.util import Inches
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE

data = CategoryChartData()
data.categories = ["Apr", "May", "Jun", "Jul"]
data.add_series("Loam", (0.27, 0.24, 0.19, 0.15))
data.add_series("Sand", (0.18, 0.14, 0.09, 0.06))
gf = s.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, Inches(0.24), Inches(1.2),
                        Inches(5.6), Inches(3.5), data)
deck.style_chart(gf.chart, y_title="Volumetric water content (m³ m⁻³)")

deck.table(s, [("Site type", "Plots", "Depths"),
               ("Loam", "18", "2"),
               ("Sand", "24", "3")], x=6.1, y=1.3, w=3.6, numeric=(1, 2))
```

`style_chart` applies the palette in `CHART_COLORS` order, removes gridlines, puts the legend
at the bottom and sets 12 pt text. `table` gives a plain table: no fills or banding, a
semibold header with a dark-teal rule, hairlines between rows. Show only the rows and columns
the slide's point needs, and state units in the header or axis title.

Charts made elsewhere (R, Python) should use the palette in `brands.md`, a white background,
Segoe UI or Arial, and text large enough to read at slide size; insert them as PNG at 200 dpi
or more, or as SVG/EMF.

## Checking the result

1. `python <skill>/scripts/lint_deck.py deck.pptx`
2. Render and look at every slide. If LibreOffice is available:
   `soffice --headless --convert-to pdf deck.pptx` then `pdftoppm -png -r 80 deck.pdf slide`.
   LibreOffice substitutes another font for Segoe UI, so line breaks can differ slightly from
   PowerPoint; leave a little slack in text boxes rather than trusting an exact fit.
   If nothing can render the file, say so and ask the user to check the deck in PowerPoint.
3. Look for: text running past the body area or into the source line, a title wrapping to a
   third line, overlapping boxes, pictures over the banner, leftover prompt text.

If a general PowerPoint skill is available, its validation and rendering scripts can be used
for this step. Its design advice does not apply here; see `anti-patterns.md`.

## Editing an existing IAT or ZALF deck

Open it with python-pptx (`Presentation(path)`), add slides from its layouts, and keep to the
rules above. Do not run it through `Deck`, which starts from the empty template.
