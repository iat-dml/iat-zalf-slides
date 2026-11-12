# Anti-patterns: what makes a deck read as machine-made

Audiences at a research institute recognise generated slides quickly, and once they do they
discount the content. The patterns below are the common tells. Each entry says what to do
instead, because the aim is a deck that a careful colleague could have made by hand, and
removing a tell without replacing it leaves a hole.

Two rules cover most cases:

1. **Every element on a slide carries content.** A shape, line, icon, colour or label that
   could be deleted without the audience losing information should be deleted.
2. **The institutional frame is the only decoration.** The title slide, the banner (PowerPoint) or
   heading and corner mark (reveal.js), the closing slide and the logos come from the
   template. Nothing else on a slide is there for looks.

`scripts/lint_deck.py` checks the mechanical items in this list. It cannot check the ones
that need judgement, so read the deck against this file as well.

## Contents

- [Text](#text)
- [Layout and shapes](#layout-and-shapes)
- [Colour, type and imagery](#colour-type-and-imagery)
- [Structure of the deck](#structure-of-the-deck)
- [Where this differs from general slide advice](#where-this-differs-from-general-slide-advice)

## Text

| Pattern | Why it fails | Instead |
|---|---|---|
| All-caps eyebrow above the title ("OUR APPROACH", "KEY RESULT", "WHO AM I") | Says nothing the title does not; the letter-spaced caps label is the most recognisable tell there is | Delete it. If the section matters, it has a divider slide. |
| Slogan titles: "From data to decisions", "Beyond the pilot", "Unlocking X", "The road ahead", "Why this matters", "X, reimagined" | Management-speak rhythm with no claim in it | State what the slide shows: "Soil moisture fell below wilting point at 9 of 24 sandy plots in July" |
| "Label: clever phrase" titles ("Living labs: where science meets practice") | The colon formula signals a tagline | One plain clause. Colons are fine for genuine "Topic: specification" titles such as "Study area: Märkisch-Oderland". |
| Question titles that tease ("So what did we find?") | Withholds the finding | Give the answer as the title |
| Topic-label titles on result slides ("Results", "Overview", "Challenges") | The audience has to work out the point | An assertion. Topic labels are fine on dividers and on genuinely descriptive slides ("Study sites", "Methods"). |
| Stock vocabulary: leverage, unlock, empower, seamless, robust (outside statistics), holistic, synergy, journey, deep dive, game-changer, cutting-edge, pivotal, foster, delve, tapestry, landscape (as metaphor; the literal agricultural landscape is of course fine) | Filler that a scientist would not write | The specific verb or noun: "use", "combine", "reduces", "covers" |
| German equivalents: ganzheitlich, nahtlos, Synergien, zukunftsweisend, innovativ, Mehrwert, Leuchtturmprojekt, Gamechanger, Deep Dive, spannend | Same | Concrete statement of what is done or found |
| "Not just X, but Y" / "It's not X, it's Y" / "nicht nur ..., sondern auch ..." | Rhetorical contrast with an invented opponent | Say Y |
| Reflexive groups of three ("faster, cheaper, better") | Rhythm in place of content | List what is actually the case, however many items that is |
| Em dashes as the default connector | Strong statistical tell in generated English | Comma, colon, full stop, or two sentences. German: Halbgeviertstrich with spaces, used sparingly. |
| Title Case In Every Heading | Not the institute's style and not German usage | Sentence case. Proper names keep their capitals. |
| Bullets that restate the title, or that are all the same length and shape | Padding | Cut. A slide with one sentence and one figure is complete. |
| Bold lead-in on every bullet ("**Scalability:** the system scales") | Template-fill pattern | Bold only for the one term the audience must not miss |
| "Key takeaways" slide that repeats the slide titles | Adds nothing | A closing slide that says what follows: open questions, next steps, what is needed from the audience |
| Hedge stacks ("may potentially help to possibly improve") and universal claims ("revolutionises", "transforms") | Both misstate the evidence | One hedge matched to the evidence, or the number with its uncertainty |
| Emoji as bullets or markers; arrows and check marks as decoration | Not the register of a research institute | Words |
| Invented or unsourced numbers, citations, quotes | A fabricated figure in a scientific deck is a serious error, not a style issue | Use only numbers from the source material. Mark gaps `[TO CONFIRM]` and list them for the user. |
| Meta-commentary on the slide ("This slide shows ...", "As we can see ...") | Belongs in the spoken talk | Put it in the speaker notes |

## Layout and shapes

| Pattern | Why it fails | Instead |
|---|---|---|
| Rounded rectangle "cards" with one coloured edge | The single-edge accent stripe is the best-known visual tell | Plain text on the slide. If items must be grouped, use spacing or a light tint (`F3F5F4`) with square corners and no border. |
| Accent line under the title, rules between sections, thin bars along a slide edge | Decoration; the frame already separates title and body | Whitespace |
| Three or four equal boxes as the default layout | Forces content into a grid it does not have | Let the content decide: one figure, a figure with a short text column, a table, a single sentence |
| The same layout on every slide; or a different "creative" layout on every slide | Both look generated | A small set used for a reason: text, figure plus text, full-width figure, table, divider |
| Icons in coloured circles beside each point | Generic icons carry no information | No icon. Use a real figure, photo, map or diagram where there is one. |
| Oversized "stat callout" numbers (72 pt "42%") without n, unit, uncertainty or source | Marketing device; strips the context a scientist needs | Put the number in a sentence or a chart, with unit, n and source |
| Pills, badges, chips, tags | Decorative labelling | Plain text |
| Floating geometric shapes, corner blobs, dot grids, arbitrary diagonal lines | No data purpose | Nothing |
| Drop shadows, glow, glass effects, gradients on content elements | Dated and decorative | Flat fills. The banner, hero, divider and closing gradients are the template's and stay. |
| Decorative timeline or "process flow" of chevrons for things that are not a process | Imposes false sequence | A list, or a real diagram if the sequence is real |
| Numbered circles (1, 2, 3) on items with no order | False structure | An unordered list |
| Centred body text | Hard to read; default of generated layouts | Left-aligned text; the template is left-aligned throughout |
| Text shrunk until it fits | Unreadable from the back of the room | Cut words, or split the slide. Body text stays at 16 pt in PowerPoint (28 px in reveal.js); never below 12 pt (22 px). |
| Extra logos, footers or page furniture on content slides | The frame already carries the institutional marks | Leave the frame alone |

## Colour, type and imagery

| Pattern | Why it fails | Instead |
|---|---|---|
| Colours outside the palette, or every palette colour used at once | Off-brand; rainbow slides | Dark teal for emphasis and headings, black text, one accent where needed. See `brands.md`. |
| Cream or beige backgrounds, italic serif headings | The current default look of generated decks | White background, Segoe UI, as in the templates |
| A second typeface, or weights other than regular and semibold | Off-template | Segoe UI and Segoe UI Semibold only |
| Colour as the only carrier of meaning in charts | Fails in greyscale print and for colour-blind viewers | Direct labels; `CHART_COLORS` order, which separates in greyscale |
| Stock photography or generated imagery as filler | Adds nothing and misleads about the study | Real photos, maps and figures from the project, credited. If there is none, no image. |
| AI-generated images without attribution | Violates the attribution rule of this skill | Caption every one: "AI-generated image (tool)" / "KI-generiertes Bild (Tool)" |
| Chart junk: 3-D, gridlines everywhere, legends far from the data, default Office colours | Obscures the result | Label directly, remove gridlines that are not read, state the unit on the axis |
| Screenshots of tables | Unreadable and not editable | A real table with only the rows and columns the point needs |

## Structure of the deck

- **Agenda slide in a short talk.** Under roughly fifteen minutes it costs a minute and tells
  the audience nothing. Use one only for long or multi-part sessions.
- **"About us" and mission slides before the content.** Start with the question or the
  result. Institutional background goes last or stays out.
- **One slide per bullet of the source document.** A deck is not a document cut into pages;
  decide what the talk argues and build that.
- **Padding to a round number of slides.** Size the deck to the time: about one slide per
  one and a half to two minutes.
- **A closing slide of thanks only.** The templates' closing slide carries the contact line;
  the slide before it should say what happens next.

## Where this differs from general slide advice

General-purpose slide guidance (including the built-in PowerPoint skill, if it is loaded
alongside this one) recommends several things this skill rules out. Where they conflict,
this file wins, because the institutional design and the scientific audience are fixed:

- "Every slide needs a visual element": no. A slide with one clear sentence is fine.
- "Pick a bold palette for the topic": no. The palette is the brand's.
- Icons in coloured circles, large stat callouts, card grids: no, see above.
- "Titles 36 pt and larger": no. Titles use the template's size (the banner in PowerPoint, the theme's heading in reveal.js).
- Building the frame with pptxgenjs from scratch: no. The frame comes from the templates via
  `scripts/pptx_deck.py`.

Their tooling for rendering, validating and inspecting files is still useful and can be used.
