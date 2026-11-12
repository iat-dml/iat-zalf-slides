"""Build IAT / ZALF PowerPoint decks on top of the institutional templates.

The helper owns the *frame* of the deck: the title slide, the banner on every
content slide, logos, slide numbers, the closing slide, language-dependent
labels, funder logos and the AI attribution. Everything inside the body area is
composed by the caller with python-pptx (or with the small text / picture /
source helpers below), so content stays free while the frame stays identical
from deck to deck.

    import sys; sys.path.insert(0, "<skill>/scripts")
    from pptx_deck import Deck

    deck = Deck(brand="iat", lang="en", audience="external")
    deck.title_slide("Soil moisture across three living labs",
                     subtitle="First season of sensor data",
                     authors=["Dr. A. Example", "B. Example"],
                     date="12.11.2026", event="IAT Statusseminar")
    s = deck.slide("Sensors were installed at 42 plots between March and May")
    deck.text(s, ["Loam sites: 18 plots", "Sandy sites: 24 plots"], bullets=True)
    deck.closing_slide(contact="a.example@zalf.de")
    deck.save("deck.pptx")

Requires python-pptx (pip install python-pptx). All measurements are inches on
the templates' 10 x 5.625 canvas.
"""
from __future__ import annotations

import copy
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

SKILL_DIR = Path(__file__).resolve().parent.parent
ASSETS = SKILL_DIR / "assets"

# Theme colours of the ZALF_PPT_2020 theme shared by both templates.
PALETTE = {
    "teal_dark": "356259",   # accent4 - banner / primary brand colour
    "green": "3AAE6C",       # accent3 - links, highlights
    "teal": "60ACAC",        # accent1
    "olive": "9DAE21",       # accent2
    "sage": "7E9862",        # accent6
    "sage_light": "91A878",  # lt2
    "forest": "252F2A",      # accent5
    "slate": "38463F",       # dk2
    "black": "000000",
    "gray": "6C6C6C",        # captions, sources, attribution
    "white": "FFFFFF",
}
# Order to use for data series in charts: distinguishable in greyscale too.
CHART_COLORS = ["356259", "9DAE21", "60ACAC", "7E9862", "252F2A", "3AAE6C"]

# Body area below the banner and above the slide number.
BODY = {"x": 0.24, "y": 1.16, "w": 9.50, "h": 3.75}

STRINGS = {
    "en": {
        "institution": "Leibniz Centre for Agricultural Landscape Research (ZALF)",
        "date": "Date:",
        "partners": "IAT partners:",
        "funded": "Funded by:",
        "thanks": "Thank you for your attention.",
        "contact": "Contact:",
        "ai_deck": "Presentation created with the assistance of Claude",
        "ai_image": "AI-generated image ({tool})",
        "source": "Source: ",
    },
    "de": {
        "institution": "Leibniz-Zentrum für Agrarlandschaftsforschung (ZALF) e. V.",
        "date": "Datum:",
        "partners": "IAT-Partner:",
        "funded": "Gefördert durch:",
        "thanks": "Vielen Dank für Ihre Aufmerksamkeit.",
        "contact": "Kontakt:",
        "ai_deck": "Präsentation mit Unterstützung von Claude erstellt",
        "ai_image": "KI-generiertes Bild ({tool})",
        "source": "Quelle: ",
    },
}

# Funder logos shown on the title slide of external decks: (file, x, y, w, h).
# Heights and rows follow the IAT template's own title slide; widths follow the
# logo files (federal ministry as renamed in 2025, current Hessen mark), with the
# row ending where the template's did.
FUNDERS = {
    "bmel": ("funders/bmel.png", 7.68, 4.86, 1.03, 0.48),
    "brandenburg": ("funders/brandenburg.png", 8.82, 4.80, 0.51, 0.54),
    "hessen": ("funders/hessen.png", 9.44, 4.84, 0.31, 0.50),
}
FUNDERS_BY_BRAND = {"iat": ["bmel", "brandenburg", "hessen"], "zalf": ["bmel", "brandenburg"]}


def _rgb(hex6: str) -> RGBColor:
    return RGBColor.from_string(hex6.upper().lstrip("#"))


class Deck:
    """A deck in one institutional design, language and audience."""

    def __init__(self, brand: str = "iat", lang: str = "en", audience: str = "internal",
                 ai_assisted: bool = True):
        brand, lang, audience = brand.lower(), lang.lower(), audience.lower()
        if brand not in ("iat", "zalf"):
            raise ValueError("brand must be 'iat' or 'zalf' (Zukunft Land is not available yet)")
        if lang not in STRINGS:
            raise ValueError("lang must be 'en' or 'de'")
        if audience not in ("internal", "external"):
            raise ValueError("audience must be 'internal' or 'external'")
        self.brand, self.lang, self.audience, self.ai_assisted = brand, lang, audience, ai_assisted
        self.s = STRINGS[lang]
        self.prs = Presentation(str(ASSETS / "pptx" / f"{brand}-template.pptx"))
        self._layouts = {l.name: l for m in self.prs.slide_masters for l in m.slide_layouts}
        self._template_slides = list(self.prs.slides)   # sample slides shipped in the template
        self._title_done = False
        self._localise_layouts()

    # ------------------------------------------------------------------ frame

    def title_slide(self, title: str, subtitle: str | None = None, authors=None,
                    date: str | None = None, event: str | None = None,
                    photo: str | None = None, photo_credit: str | None = None):
        """Fill the template's title slide. Call once, first.

        authors: a string or a list of names (optionally with role, e.g.
        "Dr. A. Example, Working Group Lead"). photo: optional image for the
        right half of the hero block; give photo_credit with it.
        """
        if isinstance(authors, str):
            authors = [authors]
        author_line = ", ".join(authors or [])
        when = " · ".join(x for x in (event, date) if x)
        slide = self._iat_title(title, subtitle, author_line, when, photo, photo_credit) \
            if self.brand == "iat" else \
            self._zalf_title(title, subtitle, author_line, date, event, photo, photo_credit)
        if self.audience == "external" and self.brand == "zalf":
            self._add_funders(slide)
        if self.ai_assisted:
            self._small(slide, self.s["ai_deck"], 0.24 if self.brand == "iat" else 0.47, 5.43, 5.0)
        self.prs.core_properties.title = title
        self.prs.core_properties.author = author_line
        self._title_done = True
        return slide

    def slide(self, title: str, layout: str = "title-only"):
        """Add a content slide with the title in the banner and return it.

        layout="title-only": empty body, compose freely inside BODY.
        layout="standard": the template's 'Standard slide' with five named
        placeholders, returned through placeholders(slide): headline, text,
        bullets, picture, caption. Remove the ones you do not fill with
        drop_empty_placeholders(slide).
        """
        self._require_title()
        if layout == "standard":
            name = "Standard slide"
        elif self.brand == "zalf":
            name = "Empty slide with header"
        else:
            name = "Titel und Inhalt"
        lay = self._layouts[name]
        slide = self.prs.slides.add_slide(lay)
        if layout != "standard" and self.brand == "iat":
            for ph in list(slide.placeholders):          # free composition: drop the body placeholder
                if ph.placeholder_format.idx == 1:
                    ph._element.getparent().remove(ph._element)
        slide.shapes.title.text_frame.text = title
        self._slide_number(slide, lay)
        self._iat_chrome(slide)
        return slide

    def closing_slide(self, contact: str | None = None, title: str | None = None):
        """Add the template's closing slide. contact: e.g. 'Dr. A. Example, a.example@zalf.de'."""
        self._require_title()
        lay = self._layouts["Finish slide"]
        slide = self.prs.slides.add_slide(lay)
        slide.shapes.title.text_frame.text = title or self.s["thanks"]
        for ph in list(slide.placeholders):
            idx = ph.placeholder_format.idx
            if idx == 14:                                # label; widened so "Kontakt:" fits on one line
                ph.text_frame.text = self.s["contact"] if contact else ""
                ph.left, ph.top, ph.width, ph.height = Inches(0.29), Inches(5.12), Inches(0.95), Inches(0.25)
            elif idx == 13:
                ph.text_frame.text = contact or ""
                ph.left, ph.top, ph.width, ph.height = Inches(1.28), Inches(5.12), Inches(7.0), Inches(0.25)
        self._iat_chrome(slide)
        return slide

    def save(self, path: str):
        self._require_title()
        for s in self._template_slides:                  # remove any untouched sample slides
            self._drop(s)
        self._template_slides = []
        self.prs.save(path)
        return path

    # ---------------------------------------------------------------- content

    def placeholders(self, slide) -> dict:
        """Named placeholders of a layout='standard' slide."""
        names = {21: "headline", 22: "text", 24: "bullets", 14: "picture", 23: "caption"}
        return {names[p.placeholder_format.idx]: p for p in slide.placeholders
                if p.placeholder_format.idx in names}

    def drop_empty_placeholders(self, slide):
        """Delete unfilled placeholders so no prompt text is left behind."""
        for ph in list(slide.placeholders):
            if ph.placeholder_format.idx in (0,):
                continue
            is_pic = ph.placeholder_format.type is not None and "PICTURE" in str(ph.placeholder_format.type)
            if is_pic or (ph.has_text_frame and not ph.text_frame.text.strip()
                          and "SLIDE_NUMBER" not in str(ph.placeholder_format.type)):
                ph._element.getparent().remove(ph._element)

    def text(self, slide, content, x=None, y=None, w=None, h=None, size=16, bold=False,
             color="black", bullets=False, align="left"):
        """Add a text box in the template's type. content: a string or a list of
        paragraphs. Body text is 16 pt in the templates; do not go below 12 pt."""
        x = BODY["x"] if x is None else x
        y = BODY["y"] if y is None else y
        w = BODY["w"] if w is None else w
        h = BODY["h"] if h is None else h
        tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        paras = [content] if isinstance(content, str) else list(content)
        for i, para in enumerate(paras):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER, "right": PP_ALIGN.RIGHT}[align]
            if i:
                p.space_before = Pt(size * 0.45)
            r = p.add_run()
            r.text = para
            r.font.size = Pt(size)
            r.font.bold = bold
            r.font.color.rgb = _rgb(PALETTE.get(color, color))
            if bullets:
                self._bullet(p, size)
        return tb

    def picture(self, slide, path, x, y, w=None, h=None, credit: str | None = None,
                ai_tool: str | None = None):
        """Add an image. credit: source / licence line shown beneath it.
        ai_tool: name of the image model if the image is AI-generated; the
        attribution is then added automatically beneath the image."""
        pic = slide.shapes.add_picture(str(path), Inches(x), Inches(y),
                                       Inches(w) if w else None, Inches(h) if h else None)
        parts = [p for p in (self.s["ai_image"].format(tool=ai_tool) if ai_tool else None, credit) if p]
        if parts:
            self.text(slide, " · ".join(parts), x, (pic.top + pic.height) / 914400 + 0.05,
                      pic.width / 914400, 0.22, size=9, color="gray")
        return pic

    def source(self, slide, text: str):
        """Source line for data or figures, bottom-left above the slide edge."""
        label = self.s["source"]
        return self.text(slide, text if text.startswith(label) else label + text,
                         BODY["x"], 5.12, 8.6, 0.22, size=9, color="gray")

    def table(self, slide, rows, x=None, y=None, w=None, col_widths=None, size=14, numeric=()):
        """Plain table in the template's style: no fills or banding, semibold
        header with a dark-teal rule, hairlines between rows. rows: list of
        row tuples, first row is the header. numeric: column indexes to
        right-align."""
        from pptx.oxml.ns import qn
        x = BODY["x"] if x is None else x
        y = BODY["y"] if y is None else y
        w = BODY["w"] if w is None else w
        n_rows, n_cols = len(rows), len(rows[0])
        row_h = size * 2.1 / 72
        gf = slide.shapes.add_table(n_rows, n_cols, Inches(x), Inches(y), Inches(w), Inches(row_h * n_rows))
        tbl = gf.table
        tblPr = tbl._tbl.tblPr
        for attr in ("bandRow", "firstRow"):
            tblPr.set(attr, "0")
        style = tblPr.find(qn("a:tableStyleId"))
        if style is not None:
            style.text = "{5940675A-B579-460E-94D1-54222C63F5DA}"   # "No Style, Table Grid"
        widths = col_widths or [w / n_cols] * n_cols
        for i, cw in enumerate(widths):
            tbl.columns[i].width = Inches(cw)
        for r, row in enumerate(rows):
            tbl.rows[r].height = Inches(row_h)
            for c, value in enumerate(row):
                cell = tbl.cell(r, c)
                cell.fill.background()
                cell.margin_left = Inches(0.02)
                cell.margin_right = Inches(0.12)
                tf = cell.text_frame
                tf.text = str(value)
                para = tf.paragraphs[0]
                para.alignment = PP_ALIGN.RIGHT if c in numeric else PP_ALIGN.LEFT
                run = para.runs[0] if para.runs else para.add_run()
                run.font.size = Pt(size)
                run.font.bold = (r == 0)
                run.font.color.rgb = _rgb(PALETTE["black"])
                tcPr = cell._tc.get_or_add_tcPr()
                for tag in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
                    for el in tcPr.findall(qn(tag)):
                        tcPr.remove(el)
                def line(tag, width_pt, hex6):
                    ln = tcPr.makeelement(qn(tag), {"w": str(int(width_pt * 12700)), "cap": "flat", "cmpd": "sng"})
                    if hex6 is None:
                        ln.append(ln.makeelement(qn("a:noFill"), {}))
                    else:
                        fill = ln.makeelement(qn("a:solidFill"), {})
                        fill.append(fill.makeelement(qn("a:srgbClr"), {"val": hex6}))
                        ln.append(fill)
                    return ln
                borders = [line("a:lnL", 0, None), line("a:lnR", 0, None), line("a:lnT", 0, None),
                           line("a:lnB", 1.5 if r == 0 else 0.5, PALETTE["teal_dark"] if r == 0 else "D9DDDB")]
                for b in borders:
                    tcPr.insert(borders.index(b), b)
        return gf

    def style_chart(self, chart, y_title: str | None = None, size=12):
        """Apply the palette and a quiet frame to a native python-pptx chart."""
        from pptx.enum.chart import XL_LEGEND_POSITION
        chart.has_title = False                             # the slide title says what the chart shows
        chart.font.size = Pt(size)
        chart.font.color.rgb = _rgb(PALETTE["black"])
        n_series = len(list(chart.plots[0].series))
        chart.has_legend = n_series > 1
        if chart.has_legend:
            chart.legend.position = XL_LEGEND_POSITION.BOTTOM
            chart.legend.include_in_layout = False
        try:
            chart.value_axis.has_major_gridlines = False
            chart.value_axis.format.line.color.rgb = _rgb("D9DDDB")
            chart.category_axis.format.line.color.rgb = _rgb("D9DDDB")
            if y_title:
                chart.value_axis.has_title = True
                chart.value_axis.axis_title.text_frame.text = y_title
                chart.value_axis.axis_title.text_frame.paragraphs[0].runs[0].font.size = Pt(size)
                chart.value_axis.axis_title.text_frame.paragraphs[0].runs[0].font.bold = False
        except (ValueError, AttributeError):
            pass                                             # pie and other axis-less charts
        for series, hex6 in zip(chart.plots[0].series, CHART_COLORS):
            is_line = "Line" in type(chart.plots[0]).__name__ or "XY" in type(chart.plots[0]).__name__
            if is_line:
                series.format.line.color.rgb = _rgb(hex6)
                series.format.line.width = Pt(2.25)
                series.marker.format.fill.solid()
                series.marker.format.fill.fore_color.rgb = _rgb(hex6)
                series.marker.format.line.color.rgb = _rgb(hex6)
                series.smooth = False
            else:
                series.format.fill.solid()
                series.format.fill.fore_color.rgb = _rgb(hex6)
        return chart

    def notes(self, slide, text: str):
        slide.notes_slide.notes_text_frame.text = text

    # -------------------------------------------------------------- internals

    def _require_title(self):
        if not self._title_done:
            raise RuntimeError("call title_slide() first")

    def _drop(self, slide):
        lst = self.prs.slides._sldIdLst
        for sld_id in list(lst):
            if self.prs.part.related_part(sld_id.rId) is slide.part:
                self.prs.part.drop_rel(sld_id.rId)
                lst.remove(sld_id)

    def _set_runs(self, shape, lines):
        """Replace a shape's text with [(text, pt or None), ...], one paragraph
        each, keeping the first paragraph's properties."""
        tf = shape.text_frame
        tf.clear()
        for i, (txt, size) in enumerate(lines):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            r = p.add_run()
            r.text = txt
            if size:
                r.font.size = Pt(size)
        return tf

    def _small(self, slide, text, x, y, w, size=6.5, color="gray", align="left"):
        return self.text(slide, text, x, y, w, 0.16, size=size, color=color, align=align)

    def _bullet(self, p, size):
        """The templates' own bullet: a small square in the theme's light sage."""
        from pptx.oxml.ns import qn
        pPr = p._p.get_or_add_pPr()
        pPr.set("marL", "177800")
        pPr.set("indent", "-177800")
        for tag in ("a:buClr", "a:buSzPct", "a:buFont", "a:buChar", "a:buNone", "a:buAutoNum"):
            for el in pPr.findall(qn(tag)):
                pPr.remove(el)
        clr = pPr.makeelement(qn("a:buClr"), {})
        clr.append(clr.makeelement(qn("a:schemeClr"), {"val": "bg2"}))
        pPr.append(clr)
        pPr.append(pPr.makeelement(qn("a:buSzPct"), {"val": "100000"}))
        pPr.append(pPr.makeelement(qn("a:buFont"), {"typeface": "Wingdings", "pitchFamily": "2", "charset": "2"}))
        pPr.append(pPr.makeelement(qn("a:buChar"), {"char": "\u00a7"}))

    def _slide_number(self, slide, layout):
        """python-pptx does not copy the slide-number placeholder; do it by hand."""
        for sh in layout.placeholders:
            if "SLIDE_NUMBER" in str(sh.placeholder_format.type):
                slide.shapes._spTree.append(copy.deepcopy(sh._element))
                return

    def _iat_chrome(self, slide):
        """IAT content slides carry the ZALF-IAT mark at the left of the banner,
        with the title moved clear of it (as on slide 2 of the IAT template)."""
        if self.brand != "iat":
            return
        slide.shapes.add_picture(str(ASSETS / "logos" / "zalf-iat-banner.png"),
                                 Inches(0.20), Inches(0.10), Inches(0.77), Inches(0.76))
        t = slide.shapes.title
        t.left, t.top, t.width, t.height = Inches(1.06), Inches(0.07), Inches(7.10), Inches(0.79)

    def _localise_layouts(self):
        """Static labels live on the layouts; switch them to the deck language."""
        swaps = {
            "Date:": self.s["date"], "Datum:": self.s["date"],
            STRINGS["en"]["institution"]: self.s["institution"],
            STRINGS["de"]["institution"]: self.s["institution"],
        }
        for lay in self._layouts.values():
            for sh in lay.shapes:
                if sh.is_placeholder or not sh.has_text_frame:
                    continue
                for p in sh.text_frame.paragraphs:
                    joined = "".join(r.text for r in p.runs).strip()
                    if joined in swaps and p.runs:
                        p.runs[0].text = swaps[joined]
                        for r in p.runs[1:]:
                            r.text = ""
                        if joined in (STRINGS["en"]["institution"], STRINGS["de"]["institution"]):
                            sh.width = Inches(7.6)       # keep the German name on one line
                        else:
                            sh.width = Inches(0.62)      # room for "Datum:"

    def _add_funders(self, slide, x_shift=0.0, label=True):
        if label:
            self._small(slide, self.s["funded"], 7.42 + x_shift, 4.62, 1.6)
        for key in FUNDERS_BY_BRAND[self.brand]:
            f, x, y, w, h = FUNDERS[key]
            slide.shapes.add_picture(str(ASSETS / "logos" / f), Inches(x + x_shift), Inches(y),
                                     Inches(w), Inches(h))

    def _hero_photo(self, slide, photo, credit, box):
        """Place a photo cropped to fill box=(x, y, w, h) and credit it."""
        x, y, w, h = box
        pic = slide.shapes.add_picture(str(photo), Inches(x), Inches(y), width=Inches(w))
        ratio = (pic.height / pic.width) / (h / w)
        if ratio > 1:                                    # too tall: crop top and bottom
            pic.crop_top = pic.crop_bottom = (1 - 1 / ratio) / 2
            pic.height = Inches(h)
        elif ratio < 1:                                  # too wide: crop the sides
            pic.height = Inches(h)
            pic.crop_left = pic.crop_right = (1 - ratio) / 2
            pic.width = Inches(w)
        if credit:
            self.text(slide, credit, x + 0.1, y + h - 0.26, w - 0.2, 0.2, size=9, color="white")
        return pic

    def _zalf_title(self, title, subtitle, author_line, date, event, photo, credit):
        keep = self._template_slides[1] if photo else self._template_slides[0]
        self._template_slides.remove(keep)
        for ph in keep.placeholders:
            idx = ph.placeholder_format.idx
            if idx == 12:
                self._set_runs(ph, [(title, None)])
            elif idx == 13:
                self._set_runs(ph, [(" · ".join(x for x in (author_line, event) if x), None)])
            elif idx == 11:
                self._set_runs(ph, [(date or "", None)])
                if self.lang == "de":                    # "Datum:" is wider than "Date:"
                    ph.left, ph.top, ph.width, ph.height = Inches(1.04), Inches(5.19), Inches(1.2), Inches(0.2)
        width = 4.53 if photo else 9.10
        if subtitle:
            self.text(keep, subtitle, 0.47, 3.02 if photo else 2.62, width, 0.6, size=14, color="white")
        for sh in list(keep.shapes):                     # the red "your picture goes here" box
            if not sh.is_placeholder and sh.has_text_frame and "picture goes here" in sh.text_frame.text:
                box = tuple(v / 914400 for v in (sh.left, sh.top, sh.width, sh.height))
                sh._element.getparent().remove(sh._element)
                self._hero_photo(keep, photo, credit, box)
        return keep

    def _iat_title(self, title, subtitle, author_line, when, photo, credit):
        keep = self._template_slides[0]
        self._template_slides.remove(keep)
        by_name = {sh.name: sh for sh in keep.shapes}
        lines = [(title, 20)] + ([(subtitle, 13)] if subtitle else [])
        tf = self._set_runs(by_name["Titel 12"], lines)
        if subtitle:
            tf.paragraphs[1].space_before = Pt(6)
        box = by_name["Textplatzhalter 13"]
        box.left, box.width, box.top, box.height = Inches(0.30), Inches(4.75), Inches(3.45), Inches(0.62)
        self._set_runs(box, [(t, s) for t, s in ((author_line, 12), (when, 11)) if t])
        stale = by_name.get("Rechteck 6")                # leftover caption hidden behind the footer
        if stale is not None:
            stale._element.getparent().remove(stale._element)
        if photo:                                        # swap the default aerial photo
            old, mark, cap = by_name["Grafik 21"], by_name["Grafik 1"], by_name["Rechteck 18"]
            geom = tuple(v / 914400 for v in (old.left, old.top, old.width, old.height))
            for sh in (old, mark, cap):
                sh._element.getparent().remove(sh._element)
            self._hero_photo(keep, photo, credit, geom)
        for sh in keep.shapes:                           # footer labels in the deck language
            if sh.has_text_frame and sh.text_frame.text.strip() == "IAT-Partner:":
                sh.text_frame.paragraphs[0].runs[0].text = self.s["partners"]
            elif sh.has_text_frame and sh.text_frame.text.strip() == "Gefördert durch:":
                sh.text_frame.paragraphs[0].runs[0].text = self.s["funded"]
        # The template embeds older funder logos. Drop them; external decks get
        # the files from assets/logos/funders/ under the template's own label.
        drop = ("Picture 2", "Picture 3", "Grafik 8")
        if self.audience == "internal":                  # funder logos only on external decks
            drop += ("Textfeld 9",)
        for name in drop:
            sh = by_name.get(name)
            if sh is not None:
                sh._element.getparent().remove(sh._element)
        if self.audience == "external":
            self._add_funders(keep, label=False)
        return keep
