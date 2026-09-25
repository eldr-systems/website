---
name: Eldr Systems
description: A calibrated instrument in bone and ink, with exactly one ember indicator lit.
colors:
  ink: "#14161A"
  bone: "#F4F1EA"
  ember: "#E2632B"
  ember-dark: "#C9551F"
  slate: "#5B6B7A"
  body: "#3A434C"
  muted: "#4E5A66"
  rule: "#C9C3B6"
  rule-dark: "#2B3036"
  on-ink: "#C9CFD5"
  muted-ink: "#9AA5AF"
typography:
  display:
    fontFamily: "Archivo, 'Helvetica Neue', Helvetica, Arial, sans-serif"
    fontSize: "clamp(2.5rem, 1.30rem + 4.92vw, 4.625rem)"
    fontWeight: 800
    lineHeight: 0.98
    letterSpacing: "-0.035em"
    fontVariation: "'wdth' 112"
  headline:
    fontFamily: "Archivo, 'Helvetica Neue', Helvetica, Arial, sans-serif"
    fontSize: "clamp(1.875rem, 1.28rem + 2.43vw, 2.75rem)"
    fontWeight: 800
    lineHeight: 1.05
    letterSpacing: "-0.03em"
    fontVariation: "'wdth' 112"
  title:
    fontFamily: "Archivo, 'Helvetica Neue', Helvetica, Arial, sans-serif"
    fontSize: "clamp(1.375rem, 1.10rem + 1.12vw, 1.75rem)"
    fontWeight: 800
    lineHeight: 1.05
    letterSpacing: "-0.02em"
    fontVariation: "'wdth' 108"
  cta:
    fontFamily: "Archivo, 'Helvetica Neue', Helvetica, Arial, sans-serif"
    fontSize: "clamp(2.75rem, 1.16rem + 6.51vw, 5rem)"
    fontWeight: 850
    lineHeight: 0.96
    letterSpacing: "-0.04em"
    fontVariation: "'wdth' 118"
  lead:
    fontFamily: "Archivo, 'Helvetica Neue', Helvetica, Arial, sans-serif"
    fontSize: "clamp(1.0625rem, 0.97rem + 0.38vw, 1.25rem)"
    fontWeight: 400
    lineHeight: 1.5
  body:
    fontFamily: "Archivo, 'Helvetica Neue', Helvetica, Arial, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.6
  small:
    fontFamily: "Archivo, 'Helvetica Neue', Helvetica, Arial, sans-serif"
    fontSize: "0.9375rem"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "'IBM Plex Mono', ui-monospace, Menlo, Consolas, monospace"
    fontSize: "0.8125rem"
    fontWeight: 400
    lineHeight: 1.8
rounded:
  none: "0"
  card: "26px"
  pill: "999px"
spacing:
  gutter: "clamp(1.25rem, 0.30rem + 3.90vw, 5rem)"
  section: "clamp(3.5rem, 2.36rem + 4.68vw, 5.5rem)"
  col-gap: "24px"
  spine: "clamp(3.75rem, 2.4rem + 5.4vw, 5rem)"
components:
  pill-ember:
    backgroundColor: "{colors.ember}"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "0.9rem 1.6rem"
    height: "48px"
  pill-ink:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.bone}"
    rounded: "{rounded.pill}"
    padding: "0.9rem 1.6rem"
    height: "48px"
  pill-outline:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "0.8rem 1.5rem"
    height: "48px"
  card-offer:
    backgroundColor: "{colors.bone}"
    textColor: "{colors.ink}"
    rounded: "{rounded.card}"
    padding: "2.25rem"
  card-offer-emphasised:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.on-ink}"
    rounded: "{rounded.card}"
    padding: "2.25rem"
  card-portrait:
    backgroundColor: "{colors.bone}"
    rounded: "{rounded.card}"
    width: "320px"
    height: "320px"
  spine-marker:
    backgroundColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    size: "12px"
  nav-link:
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.none}"
---

# Design System: Eldr Systems

## Overview

**Creative North Star: "The Calibrated Instrument"**

The system is built like the face of a precision measuring device. A bone faceplate, ink
markings machined into it, and exactly one ember indicator lit at a time. Nothing glows,
nothing floats, nothing is suggested — every edge is a real 2px border and every value
that came from a measurement is set in mono, the way a readout is. The reason ember is
rationed is not restraint for its own sake: an instrument with two lamps lit is an
instrument you cannot read.

The homepage is built on a **spine**: one continuous 2px ink rule running down a narrow
left rail, with each dated band hanging off it and a single marker riding it. The marker
lights ember as its band crosses mid-viewport and goes back to ink as it leaves, so the
accent is handed from one day to the next instead of being spent in several places at
once. That hand-off is the only motion in the system and the only thing that moves.

Density is generous rather than packed. Sections are full-width bands separated by
hairline-to-2px ink rules, and body copy is held to 34–44 characters so a reader working
in a second language never loses the line. The type does the shouting: Archivo at weight
800 with its **width axis** pushed to 112% and tracking pulled to −0.03em, which is what
makes headlines read as stamped rather than typed. Losing that width axis is the single
fastest way to turn this into a generic template.

The imagery stance is documentary, not decorative. Real photographs, real power-profiler
traces, real PCBs. Where a real asset does not exist yet, the system uses line diagrams
drawn in the same 1.5–2px ink stroke as everything else — deliberate-looking placeholders
that must eventually be replaced, never dressed up to pass as finished. Explicitly
rejected: stock smart-city glow, AI brains and robots, runes and Viking imagery, and any
flame anywhere near The Keep, since fire is the hazard it guards against.

**Key Characteristics:**

- Bone page, ink marks, and ember rationed across the whole viewport, not per component
- One continuous ink spine with a single travelling ember marker
- Zero shadows; depth is border weight and whole-surface inversion
- Archivo display type carried by width, not weight alone
- IBM Plex Mono reserved for measured values, labels and legal text
- 2px ink rules as the primary structural device
- Icons are single-colour ink; ember is an event, not a detail
- Two radii only: 26px cards and 999px pills

## Colors

A near-monochrome instrument palette — warm paper, cold black, one hot accent — with a
cool slate reserved exclusively for data.

### Primary

- **Ember** (`#E2632B`): The single lit indicator. Used for the logo dot, the primary
  call-to-action pill, the one emphasised bullet in a list, the device in the hero
  diagram, and the peak of a current trace. Never a fill, never a gradient, never a
  background for text at length.
- **Ember Deep** (`#C9551F`): The pressed and hover state of an ember pill. Exists only
  as a state; never used at rest.

### Secondary

- **Slate** (`#5B6B7A`): Data and diagrams only. Deliberately not a text colour and not a
  UI colour — it is the pencil used for a second series on a chart.

### Neutral

- **Ink** (`#14161A`): Body text at full contrast, every icon stroke, every border, and
  the dark surface an inverted section sits on.
- **Bone** (`#F4F1EA`): The page. Warm, slightly yellow paper — not white, and never
  substituted with white.
- **Body** (`#3A434C`): Running prose on bone. Softer than ink so that headings stay
  dominant without needing extra weight.
- **Muted** (`#4E5A66`): Mono labels and captions on bone.
- **Rule** (`#C9C3B6`): Hairline dividers on bone, for rows inside a section.
- **On Ink** (`#C9CFD5`): Running prose on an inverted ink surface.
- **Muted Ink** (`#9AA5AF`): Mono labels on an inverted ink surface.
- **Rule Dark** (`#2B3036`): Hairline dividers on an inverted ink surface.

### Named Rules

**The One Ember Rule.** Ember is rationed across the *viewport*, not per component. On
the homepage it is spent in exactly four places: the logo mark, the single audience
indicator dot, the booking pill, and the travelling spine marker — and the marker only
while its band is passing mid-screen. Everything else that could carry ember carries ink.
No CSS enforces the count; it has to be checked by eye, by scrolling the page and asking
how many lit points were visible at once.

**The Ink Icon Rule.** Icons render single-colour ink. The icon sprite ships an ember
detail in every symbol, and `--eldr-ember` is aliased to ink at `:root` to neutralise it,
because roughly twenty static ember marks on one scroll left the travelling marker
reading as the twenty-first dot rather than an event. A single component may re-declare
`--eldr-ember` locally to give one icon its ember back — deliberately, and never more
than one per screen.

**The Indicator Rule.** Ember marks a single point of attention: a dot, a peak, one
button, one bullet. It is never a surface, a gradient, a border on a large shape, or a
background behind body copy.

**The Reserved Slate Rule.** Slate appears in data and diagrams and nowhere else. Slate
text in running copy is a system violation, not a subtle choice.

## Typography

**Display Font:** Archivo variable (with Helvetica Neue, Helvetica, Arial fallbacks) —
weight axis 400–900, width axis 62–125%
**Body Font:** Archivo, same family
**Label/Mono Font:** IBM Plex Mono, weights 400 and 500 (with ui-monospace, Menlo,
Consolas fallbacks)

**Character:** A single grotesque doing all the talking, stretched wide and set tight at
display sizes so headlines read as machined into the page, with a technical monospace
carrying every number, unit and label. The pairing is engineering documentation, not
editorial — there is no serif anywhere and no second personality.

Both faces must render Hungarian **ő** and **ű**; the self-hosted subsets include
latin-ext specifically for this, and it is not optional.

### Hierarchy

- **Display** (800, `clamp(40px → 74px)`, line-height 0.98, tracking −0.035em, width 112%):
  The page's single h1. One per page.
- **Headline** (800, `clamp(30px → 44px)`, line-height 1.05, tracking −0.03em, width 112%):
  Section headings. The rhythm marker of the homepage.
- **Title** (800, `clamp(22px → 28px)`, line-height 1.05, tracking −0.02em, width 108%):
  Card headings, note titles, and h2s inside Markdown prose.
- **CTA** (850, `clamp(44px → 80px)`, line-height 0.96, tracking −0.04em, width 118%):
  The closing ask, and only the closing ask. The largest and widest type in the system —
  its job is to be the loudest thing on the page.
- **Lead** (400, `clamp(17px → 20px)`, line-height 1.5): The paragraph directly under the
  h1, held to ~34 characters per line.
- **Body** (400, 16px, line-height 1.6): Running prose, held to 34–44 characters in
  section intros and up to ~65 in long-form notes.
- **Small** (400, 15px, line-height 1.5): Secondary body — card lines, list detail,
  footnotes and navigation. One step below Body, never used for a primary paragraph.
- **Label** (mono 400, 13px, line-height 1.8): Eyebrows, durations, dates, table keys,
  the footer, and every legal value.

### Named Rules

**The Width Axis Rule.** Display type is Archivo with `font-stretch` set, not weight
alone. Always use the `display-xl` / `display-lg` / `display-md` / `display-cta`
utilities rather than writing type styles by hand — they exist precisely so a new section
cannot silently drop the width axis. All four also set `text-wrap: balance`, so a wide,
tightly tracked headline breaks into even lines instead of leaving one orphaned word.

**The Measured-Value Rule.** Any number that came from a measurement, a price, a
duration, a date or a registration document is set in IBM Plex Mono. Prose numbers stay
in Archivo. The mono face is how a reader tells a claim from a reading.

**The One Voice Rule.** There is no second typeface. A decorative or "friendlier" face
introduced anywhere in this system is a violation, not a variation.

## Layout

A single centred column capped at **1440px**, with a fluid gutter of
`clamp(20px → 80px)` and vertical section rhythm of `clamp(56px → 88px)`. Everything
lives inside that one container, including the header and footer, so the page reads as
one continuous instrument face rather than a stack of full-bleed bands.

Three grid patterns cover the whole site:

- **Dated band** — a two-column grid of `spine` width plus `1fr`, with a fluid
  `clamp(16px → 40px)` column gap. The left column is the spine rail; the right column
  holds the band's own content, usually a 12-column editorial split nested inside it.
  Used only by the five dated bands.

- **Editorial split** — a 12-column grid with a 24px column gap, used for sections with a
  statement on one side and content on the other. At `lg` (1024px) these resolve to a 6/6
  or a 5-column statement with content starting at column 7; below that everything
  collapses to a single full-width column.
- **Auto-fit card grid** — `repeat(auto-fit, minmax(Xpx, 1fr))` with a 24px column gap,
  where X is tuned per content type: 180px for the five layers, 220px for process steps,
  200px for the Keep's figures, 260px for notes on the proof band, 280px for offer cards
  on the offers index. The grid is never given a fixed column count, so adding a figure
  or an offer needs no template change. On the homepage this pattern is now the
  exception: the sections that once used it are ruled bands instead.

Section boundaries are structural: every top-level section carries a `border-top: 2px`
in ink. Rows *within* a section use a 1px `rule` hairline, with the first and last row of
a list promoted back to 2px ink to close the block.

Measure is controlled deliberately rather than left to the container: 14ch for the
closing CTA headline, 34ch for the hero lead, 38ch for captions, 44ch for section
intros.

### Named Rules

**The Ruled Section Rule.** Sections are separated by a 2px ink rule and nothing else —
no background change, no spacing-only break, no card wrapper. Inverted ink surfaces are a
card treatment, never a section treatment.

**The Spine Ends Rule.** The spine runs Day 0 → Week 1 → Week 2 → Day 14 → Day 44 and
stops. Everything below is context, not more clock, and carries no rail and no marker.
Extending the spine past the engagement dissolves the one thing it measures.

## Elevation & Depth

**Flat by default.** There is not one `box-shadow` in this system. Depth is expressed two
ways: **border weight** (2px ink for structure, 1px rule for subdivision) and **whole-
surface inversion** (a card flips to an ink background with `on-ink` prose and
`muted-ink` labels). An emphasised offer card is not raised — it is inverted.

A shadow must earn its way in. If genuinely floating UI ships later — a dropdown, a
modal over scrollable content — it defines its own named elevation token deliberately at
that point. What it may not do is sprinkle shadows onto components that are flat today.

### Named Rules

**The Flat-By-Default Rule.** Surfaces are flat. Before adding a shadow, name the element
that is physically floating above the page; if you cannot, the answer is a border or an
inversion.

**The Inversion-Is-Emphasis Rule.** The way to make a card louder is to flip it to ink,
not to lift it, tint it, or outline it in ember. When a card inverts, its icon strokes
invert with it via the `--eldr-ink` alias.

## Shapes

Two radii and no others: **26px** for cards, portraits and media blocks, and **999px**
for pills. Everything else is square — section rules, dividers, table rows, diagrams and
the logo's own 14.6% tile radius, which is a fixed proportion of the mark rather than a
member of the scale.

Borders carry the form language. The default is `2px solid ink` — heavy enough to read as
an edge rather than a hairline, which is what gives cards and outline pills their
machined quality. The 1px `rule` hairline is strictly for subdividing content inside an
already-bordered block.

The logo tile's corner radius is **74.7 on a 512 box (14.6%)** and must be preserved
proportionally at every size.

### Named Rules

**The Two-Radius Rule.** 26px or 999px. A value between them is a mistake, not a nuance.

## Components

Character: **machined and unambiguous.** Hard edges, real borders, obvious affordances.
Nothing is soft, nothing is merely suggested, and nothing clickable is ambiguous about
being clickable.

### Buttons (Pills)

- **Shape:** Fully rounded pill (999px), minimum height 48px, inline-flex and centred.
- **Primary (ember):** Ember background with ink text — never bone text on ember.
  Padding `0.9rem 1.6rem`, weight 700, 17px. This is the booking CTA and it is the one
  ember element in whatever section it appears in.
- **Solid (ink):** Ink background, bone text, same metrics. Used for the skip link.
- **Outline:** 2px ink border on transparent, padding `0.8rem 1.5rem` (1px tighter to
  compensate for the border). The secondary action, and the header's booking control.
- **Focus:** 3px ember outline at 3px offset, applied globally via `:focus-visible`. The
  focus ring is the one place ember appears without counting against the One Ember Rule.
- **Disabled:** see Disabled Control below.

### Cards

- **Corner style:** 26px.
- **Default:** Bone background, 2px ink border, 36px internal padding, contents in a
  vertical flow with 20px gaps and the description set to `grow` so the footer row aligns
  across a row of cards regardless of copy length.
- **Emphasised:** Ink background, `on-ink` prose, `muted-ink` labels, `rule-dark`
  dividers, and icons inverted via the `--eldr-ink` alias. No border change, no lift.
- **Footer row:** Divided from the body by a 1px hairline, with a mono value on the left
  and a text link on the right.

### Navigation

- **Header:** Logo lockup (inverse mark — bone tile, ink glyph, ember dot — at 44px, with
  `eldr` set at weight 850 / width 120% / tracking −0.035em beside `systems` in mono
  label). Links are 15px, weight 500, ink, with a fluid `clamp(1rem, 2vw, 2rem)` gap,
  wrapping rather than collapsing to a hamburger. The booking control is an outline pill.
- **Link default:** Colour inherited, no underline. **Hover:** underline at 4px offset.
  This applies site-wide; underline-on-hover is the only link affordance.
- **Footer:** Entirely mono at label size, `body` colour, above a 2px ink rule, using the
  original mark (ink tile, bone glyph) at 32px.

### Disabled Control

An unset URL renders as a non-interactive `<span>`, never an `<a>` to a bracketed
placeholder. Three behaviours define it:

- **It inherits the caller's class.** An unclassed caller (the footer's social links)
  stays plain inline text; it does not become a pill because it went dead.
- **An ember pill downgrades to an outline pill.** A dead control does not wear the
  page's primary accent. It keeps full contrast — it is not dimmed to an unreadable
  ghost.
- **The explanation sits outside the control.** A mono `[link pending]` in `muted` is a
  sibling of the control, not inside it, so it cannot break the pill's shape at phone
  width. `aria-disabled="true"` and a `title` carry the reason.

### Ruled Bands

The system's workhorse family, all built from the same hairline language rather than from
cards: rows separated by 1px `rule` hairlines, with the first and last row promoted to
2px ink to close the block. Four members ship:

- **Ruled list** — one label left, one mark right. The audience list (indicator dot
  right) and the "Where and how" definition list (mono key in `muted` left, mono value
  right).
- **Ruled sequence** — a mono ordinal (`01`–`05`) in `muted`, a semibold name, and a
  small-step line, on a 12-column baseline-aligned grid. The five layers.
- **Ruled roster** — a small square portrait at card radius with a 2px ink border, a
  name and mono role, and a small-step bio with an optional mono link. The team.
- **Ruled offer band** — a statement column on the left (title, summary, text link) and
  three rigid mono slots on the right, always in the same order: duration, price,
  guarantee. The slots are rigid on purpose; a reader compares down the column.
- **Spec table** — a mono definition list, key in `muted` left, value right, one row per
  fact. Opens on 2px ink and closes on 2px ink. The Day 0 band.

These deliberately replaced three card-grid sections. When a new section is a set of
comparable things, the default answer is a ruled band, not a card grid.

### The Spine (signature)

The defining structure of the homepage. A dated band is a two-column `band` grid whose
left column is a `spine-rail`: a 2px ink `border-right` with a mono unit label
(`DAY 0`, `WEEK 1`) set at 0.06em tracking beneath it. A 12px ink `spine-dot` sits at
`right: -7px` so it straddles the rule rather than hanging beside it. Consecutive bands
stack their rails into one continuous line down the page.

**The travelling ember.** A marker marked `data-rides` animates ink → ember → ink,
scaling 1 → 1.5 → 1, as its band crosses the middle of the viewport
(`animation-range: cover 42% cover 58%`). It is a CSS scroll-driven animation
(`animation-timeline: view()`) because the site ships no JavaScript, and it is wrapped in
both `@supports (animation-timeline: view())` and
`@media (prefers-reduced-motion: no-preference)`. The `@supports` guard is load-bearing,
not polish: without a timeline the same animation would fire once on load. Browsers
without support get a static ink marker, which is the honest fallback.

Day 0's marker does not ride. That band spends its ember on the booking pill, and two lit
points in one band is exactly what the ration forbids.

### Browser Surfaces

The parts the system did not draw still carry it. Selection is ember with ink text;
`scrollbar-color` is ink on bone; `caret-color` and `accent-color` are ember. Focus is a
3px ember outline at 3px offset, applied globally through `:focus-visible` — the one
place ember appears without counting against the ration, because it is transient and
user-summoned.

### Line Diagrams

Bespoke SVG drawn in the same language as the rest of the system: `1.5–2px` ink strokes,
`var(--color-ink)` rather than hardcoded hex so it inverts with its surface, dashed links
at `2 5` with round caps, and a single ember-filled shape as the subject. Labels are HTML
in normal flow beside the SVG, never `<text>` inside the viewBox, so they hold their
13px mono size at phone width instead of scaling with the drawing.

## Do's and Don'ts

### Do:

- **Do** use the `display-xl` / `display-lg` / `display-md` / `display-cta` utilities for
  all display type, so the width axis survives.
- **Do** set every measured value, price, duration, date and legal number in IBM Plex
  Mono.
- **Do** invert a card to ink when it needs emphasis.
- **Do** use `var(--color-ink)` in SVG strokes rather than `#14161A`, so icons follow the
  surface they sit on.
- **Do** count the lit ember points in a full viewport before shipping a section. More
  than one at rest means the ration is broken.
- **Do** build a comparison set as a ruled band before reaching for a card grid.
- **Do** wrap any scroll-driven animation in both `@supports (animation-timeline: view())`
  and a `prefers-reduced-motion` query.
- **Do** render an unset link as a visibly disabled control with `aria-disabled` — never
  an `href` to a bracketed placeholder.
- **Do** keep body measure between 34ch and 44ch in sections, and honour
  `prefers-reduced-motion`, which is already wired globally.
- **Do** leave placeholder assets obviously unfinished, and replace them with real photos
  and real traces.

### Don't:

- **Don't** let a second ember point be visible at rest anywhere in the viewport. This is
  the rule that holds the identity together, and it is measured across the screen, not
  per component.
- **Don't** give a sprite icon its ember back without deleting an ember elsewhere.
- **Don't** extend the spine past Day 44, or give a marker `data-rides` in a band that
  already spends its ember.
- **Don't** dim a disabled control to low contrast, or put its explanation inside the
  control.
- **Don't** set an uppercase mono kicker above a heading. The heading carries its own
  weight; a label above it is a crutch.
- **Don't** set display type with weight alone. Dropping `font-stretch` is the fastest
  route to a generic template.
- **Don't** add a `box-shadow` to a component that is flat today.
- **Don't** introduce a colour. The palette is closed; supporting greys already exist for
  every surface and state.
- **Don't** use slate for text or UI — it belongs to data and diagrams.
- **Don't** substitute white for bone, or bone for white.
- **Don't** use a corner radius between 26px and 999px.
- **Don't** add a second typeface, and don't put ember behind body copy.
- **Don't** ever place a flame near The Keep, or use runes, stock smart-city imagery, or
  generic AI visuals.
