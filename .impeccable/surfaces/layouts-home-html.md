---
version: 1
slug: "layouts-home-html"
primary_target: "layouts/home.html"
related_targets: ["content/_index.md","content/offers"]
---

## Scope and mode

The eldrsystems.com homepage and the offer detail pages it generates. Visitor mode:
**Persuade**. The notes collection stays **Read** and is out of this contract except for
the proof slot that links into it.

## Audience, job, action

A CTO, head of embedded or firmware lead whose battery-powered LTE-M / NB-IoT devices are
already failing in the field. Many read English as a second language. The action is a
booked 20-minute scoping call; a named founder's email is the secondary path.

## Proof and content

No customers, case studies or testimonials exist and none may be implied. The persuading
is done by the guarantee (no 20%+ battery gain or connectivity fix found, no fee), the
fixed price, the two-audits-a-month capacity, and The Keep audited in public with its own
traces. Placeholder figures stay visibly bracketed.

## Direction contract

**THESIS:** The page is the two weeks you are buying, dated Day 0 to Day 44. It refuses
the capability grid every engineering consultancy ships — hero, three equal service cards,
process strip, team row — because that arrangement sells a menu when the visitor arrived
with a failure and a deadline.

**OWN-WORLD:** Bone ground, ink rules, one ember. A dated mono spine runs the page's full
height and every band hangs off it. Emphasis tightens rule frequency rather than spending
a second accent; offers carry one rigid spec label — duration, price, capacity — in
identical slots; The Keep appears in four orthogonal views, never one photo. No shadows;
emphasis is inversion to ink.

**STORY:** The visitor understands their fleet is dying because nobody logged the timers
the network actually granted. They believe two weeks at a fixed fee settles it and that
the risk sits with us. They book Day 0.

**FIRST VIEWPORT:** Left seven columns: the failure set in display-xl (40→74px) with no
eyebrow above it, then a 34ch lead. Right five columns: one complete duty cycle drawn in 1.5px ink —
wake, transmit, active window, sleep — with the active window marked by tightened hatch
frequency, not colour. Directly below, full container width, the Day 0 band: a 2px ink
rule, "DAY 0 · 20 MINUTES" in mono at the left, the ember booking pill at the right. That
pill is the only ember above the fold.

**SIGNATURE INTERACTION:** The travelling ember. One ember marker rides the spine and is
handed from Day 0 to Week 1 to Day 14 to Day 44 as the reader scrolls, so the page
literally cannot hold two. Under `prefers-reduced-motion` it does not travel; it stays at
Day 0. Built with CSS scroll-driven animation inside an `@supports (animation-timeline:
view())` guard, because this site ships no JavaScript; unsupported browsers get the static
ember at Day 0. Motion grammar: nothing else on the page moves.

**FORM:** The Two-Week Clock — index 4 of 7 on the grounded structural list, dealt lead.
Seed key d0cc09fb.

**FINISH:** unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance

## Recorded deviations from the contract

- OWN-WORLD names the three rigid offer slots as duration / price / **capacity**.
  Capacity is real only for the Audit ("two audits a month"); no capacity figure
  exists for the other three offers in any source material, and a guarantee is a
  contractual claim that may not be invented. The slots ship as duration / price /
  **guarantee**, which is true for all three. Capacity survives in the Day 0 spec
  table where it is true. Accepted at finish review.
- FIRST VIEWPORT names the ember booking pill as the only ember above the fold.
  `bookingUrl` is unset, so every CTA renders as a full-contrast outline control
  with a `[link pending]` bracket and there is currently **no ember above the
  fold at all**. This is the honest rendering of an unprovisioned link, not a
  craft decision; setting the param restores the contract with no template edit.

## Unresolved

- Whether prices are published at all; the Audit's €7,500 rides as a bracketed placeholder.
- Tagline provisionally "Connected devices that stay connected."; flagged for discussion.
- The Keep's µA figure, demo video, and all real photography are still outstanding.
