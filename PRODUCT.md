# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

**Primary (the market the site headlines):** companies with battery-powered LTE-M,
NB-IoT or 2G/3G devices **already deployed in the field** that flatten their batteries
well before the rated life, or drop off the network and reappear hours later. They have
no dedicated cellular expert in house. The pain is urgent, measurable, and often on a
deadline, because 2G/3G shutdowns are forcing migrations.

**Secondary (named on the site as a focus, not the headline):** energy and electrical
monitoring — solar and battery installers, EV-charger and heat-pump companies, energy
management startups, building operators. Companies that need to monitor something in
the field and have no electronics or firmware team of their own.

**Who actually reads the site:** CTOs, heads of hardware and embedded, firmware leads,
IoT product managers. Many are Swedish, Danish or German engineers reading English as a
second language. Procurement reads the footer and the company page.

## Product Purpose

Eldr Systems turns a remote measurement problem into a working, low-power, connected
device with a data backend — electronics, firmware, NB-IoT/LTE-M connectivity, cloud
and data analysis, delivered by three engineers in Budapest working across the EU.

The website's job is to convert a qualified technical reader into a **booked 20-minute
scoping call**. A named founder's email on our own domain is the secondary path; there
is no `info@`. Before either can happen the site has to clear a procurement bar — real
company details, real names, real numbers — because the buyer is committing a budget to
a three-person firm they have not met.

## Positioning

Five things a neighbouring consultancy could not truthfully copy in combination:

1. **End to end.** PCB, firmware, cellular connectivity, backend and data analysis in
   one small team — not coordinated across three vendors.
2. **Low-power cellular specifically.** NB-IoT and LTE-M, battery budgets, PSM and eDRX,
   poor coverage, OTA updates.
3. **Electrical competence near mains.** Voltage, current and power measured safely.
4. **Faults found in device data.** Anomaly detection, forecasting and fault detection
   on sensor time series. Always phrased "we find faults in your device data" — never
   "AI solutions".
5. **Trained in Scandinavia, based in Budapest.** Uppsala and Aalborg master's degrees,
   working English, Hungarian cost base. The Norse name is a nod to where the founders
   studied, not a claim to be Nordic. Budapest is stated openly; the cost base is a
   selling point, not something to hide.

Backend and ML appear only as parts of the end-to-end package, never as standalone
services. **What Eldr is not:** a web or app agency, an AI consultancy, or a large PCB
design house.

## Operating Context

Every engagement runs the same four steps: **call → scoping document → build with
weekly demos → handover.** The scoping document is fixed scope, fixed price, named
deliverables, and the client keeps it whether or not the build goes ahead. Handover is
source code, schematics, build instructions and documentation — no lock-in.

Weekly demos are working hardware and real data, not status reports.

The lead engagement is a two-week **Battery and Connectivity Audit**: the client ships
3–5 devices, week 1 is power traces and network tests, week 2 is analysis and fix
estimates, ending in a report and a one-hour walkthrough plus a 30-day follow-up call.
Total client effort is about two hours. Capacity is **two audits per month** — real
scarcity, stated plainly; never countdowns or manufactured urgency.

Contracts are in English. Working languages are English and Hungarian. Budapest, CET.

## Capabilities and Constraints

**Delivered across five layers:** sensor and PCB (measurement near mains) → firmware
(sleep budgets, power-saving modes, OTA) → NB-IoT / LTE-M (PSM and eDRX tuned per
operator and site) → cloud (ingest, storage, alerts, dashboard) → analytics (fault and
anomaly detection).

**The offer ladder was redesigned in September 2026** and the currently published
offers are stale. The launch set is the Audit featured, then Fix implementation, 2G/3G
migration sprint, and Field prototype in 6 weeks; Edge AI feasibility and Fleet care
are mentioned briefly; Fleet health for installers is **not published until validated**.
Full definitions, guarantees and figures: `docs/website-brief-2026-09.md` §6.

**Guarantees are real commitments, not marketing.** The Audit charges no fee if it
finds neither a 20%+ battery gain nor a connectivity fix, conditional on receiving the
agreed devices and information. Fix implementation continues at no extra cost until the
agreed gain is reached. The field prototype makes the next week free on a slipped
milestone. These must be reproduced accurately or not at all.

**Technical constraints the site must hold:**

- Ships no JavaScript to the browser. Node is a build-time dependency only.
- No third-party asset requests, no analytics, no cookies at launch. This is what keeps
  the footer's "No cookies." claim honest, and `scripts/check.sh` fails the build if a
  third-party request appears.
- Fonts self-hosted, subset to Latin **and Latin-Ext** — Latin-Ext carries the Hungarian
  **ő** and **ű**, so it is not optional.
- English across the whole site; a Hungarian version of at least the main page is
  committed. `/hu/` is configured and currently disabled. Every surface must stay
  translatable.
- Structure must grow into per-offer pages, case studies and a technical blog without a
  rebuild.
- Hungarian law requires registered seat, company registration number, tax number and
  EU VAT number in the footer once the Kft. is registered.
- Unset links render as visibly disabled controls, never as links to nowhere.

**Explicitly undecided — do not resolve silently:**

- **Whether prices are published.** Undecided. The Audit's €7,500 is carried as a
  bracketed placeholder for now, following the existing `€[...]` convention that
  `check.sh` reports. The indicative €15–50k ranges for the other offers are
  assumptions still being tested in conversations and are not publishable.
- **Tagline.** Provisionally *"Connected devices that stay connected."* — chosen because
  it names the buyer's actual failure without naming a technology. **Flagged for
  discussion; not settled.**
- **Hero framing**, build-led versus audit-led, remains open in the brief (§4).

## Brand Commitments

**Name:** written **Eldr Systems** — capital E, rest lowercase. Never "ELDR", never
"EldrSystems". Pronounced "EL-der"; spelled out on calls. *eldr* is Old Norse for fire.
Wordmark is lowercase **eldr** with **systems** set smaller in mono. Handle
`eldrsystems` everywhere; domain eldrsystems.com.

**The Keep** is always "The Keep by Eldr Systems" in public — an NB-IoT home monitoring
hub for accident prevention, presented as Eldr's own product and test bed, not a
separate business. **No flames anywhere near The Keep**: fire is the hazard it guards
against. No runes, no Viking imagery.

**Personality:** calm, precise, direct, quietly competent — *the engineers you'd trust
near mains voltage.* Specific over vague. Sober over flashy. Small and personal over
faceless. Honest about what is known over overclaiming seniority or scale.

**Voice rules:** numbers over adjectives; name the technology (NB-IoT, LTE-M, PSM,
eDRX, OTA); plain English and short sentences for second-language readers; experience
shown through specifics, not years; clear about scope, price and process; honest
scarcity only.

**Banned words:** revolutionary, cutting-edge, next-generation, game-changing,
AI-powered solutions, synergy, seamless, world-class, leverage (as a verb).

**Experience framing (decided):** a capable young team, said plainly. Scandinavian-
trained, Budapest-based, available. Not "senior specialists"; years of experience are
not claimed. Credibility comes from named specifics.

**The team is the product.** Three founders, real photos, one card each, descriptive
titles under a shared "Co-founder" role — Vencel Koczka (clients, cloud and data, the
contact person), Bence Schoblocher (firmware and connectivity), Boldizsar Karancsi
(electronics and production). **C-titles are deliberately not used.** Names are written
without Hungarian accents as supplied — do not "correct" them.

**Imagery: real photographs only** — our PCBs, power-profiler traces, a device in a real
distribution box, the three of us at the bench. Never stock smart-city glow, never AI
brains or robots. The SVGs in `graphics/` are placeholders that look deliberate, which
is a trap: they are easy to ship and never replace.

**Binding visual constraints** live in `eldr-systems-kit/BRAND.md` (colour tokens, the
one-ember-per-component rule, the display type width axis) and are not restated here.
Where `BRAND.md` and `docs/website-brief-2026-09.md` disagree on product truth, the
brief is newer and wins — except on typography, where Archivo is the resolved answer and
both documents need updating.

## Evidence on Hand

**Exists and is usable:**

- Three real founder photos and three specific bios (degrees, named former employers,
  named tools) — `data/team.yaml`, `assets/imgs/`.
- One published technical note with real substance: "What PSM actually negotiates, and
  why your battery estimate is wrong."
- A public build repository at github.com/eldr-systems, which the privacy page cites as
  verifiable proof of the no-tracking claim.
- The Keep as a genuine in-house NB-IoT device and test bed.
- Per-founder email addresses on the eldrsystems.com domain, recorded in `data/team.yaml`.

**Does not exist yet — must not be fabricated or implied:**

- **No customers, case studies, testimonials, logos or named references of any kind.**
- No demo video of The Keep. Planned, 2 minutes, YouTube `eldrsystems`.
- No real measurement for The Keep's average PSM current; the homepage carries `[X] µA`
  as a deliberate placeholder awaiting a bench measurement.
- No photographs of PCBs, power-profiler traces, or a device in a distribution box.
- Company registration incomplete: seat, registration number, tax number and EU VAT
  number are all unset. The company page states this openly rather than hiding it.
- Booking link unset. Site-wide email, LinkedIn company page and YouTube channel unset.
- No Hungarian copy written.
- The first planned proof piece is the audit of The Keep itself, with real traces.

## Product Principles

1. **Every claim traces to a measurement.** Numbers, not adjectives — and when the
   number does not exist yet, a visible placeholder rather than a plausible invention.
2. **Lead with the failure, not the capability.** The buyer arrives with devices dying
   in the field. Name their problem before describing what we can build.
3. **Fixed scope, fixed price, no lock-in.** Predictability is the product for a Nordic
   and German buyer. Source, schematics, scripts and documents go to the client.
4. **Three named engineers, not a faceless team.** Smallness is stated, not disguised;
   it is why the client talks to the person doing the work.
5. **The site proves its own claims.** No trackers, no third-party requests, a public
   repository and a build that fails when any of that slips. The medium is part of the
   argument.

## Accessibility & Inclusion

No formal standard is committed. The working requirement is that nothing ships broken:
real contrast, keyboard-reachable controls, sensible focus order, honest alt text, and
respect for reduced-motion preferences.

One product-specific inclusion fact does bind: **a large share of readers are engineers
reading English as a second language.** Short sentences, plain words and unambiguous
labels are a comprehension requirement here, not a style preference.
