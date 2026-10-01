# Product

<!-- impeccable:product-schema 1 -->

> **Direction reset, 2026-10-01.** The three founders agreed a new direction: Eldr
> Systems is an end-to-end engineering service company for industry. This file is the
> source of truth. `docs/website-brief-2026-09.md` and the Battery and Connectivity
> Audit offer it describes are superseded and kept only as history.

## Platform

web

## Users

**Who we sell to:** industrial companies that need something measured, connected and
shown on a screen, and have no electronics, firmware or cloud team that covers the
whole chain. Not only NB-IoT or sensor companies: manufacturers, maintenance and
service companies, energy and grid operators, building operators.

**Who actually reads the site:** mostly people we contacted cold, on LinkedIn or by
email, who click through to check us before replying. CTOs, heads of engineering,
operations and maintenance managers, product managers. Many read English as a second
language. They give the site about a minute. Procurement reads the footer and the
company page.

## Product Purpose

The site has one job: turn a cold reader into a **reply or a booked 20-minute call**.
In that minute it has to make three points, in this order:

1. **This team can build my whole thing**, from the circuit board to the dashboard.
2. **They are real and competent**: named people, named backgrounds, real work.
3. **Talking to them is easy and low-risk.**

Everything on the page supports one of those three or is cut.

## Positioning

**End to end, in house.** Electronics, firmware, connectivity, cloud and dashboards,
built by one team. The client gets one contract and one team, not three vendors and
the gaps between them.

**A capable young team.** Never written as the word "young". It shows through:
real faces, fast replies, short turnarounds stated as commitments, direct access to the
engineer doing the work, and a modern stack named openly. Credibility comes from named
specifics: Ericsson, Keysight, Samsung SDI, Uppsala, Aalborg, BME.

**What Eldr is not:** a web or app agency, an AI consultancy, or a large design house.

## Operating Context

The founders run Eldr alongside their day jobs for now. **The site never mentions day
jobs or part-time work**, and never promises what that cannot support (24/7 support,
large teams, very short deadlines on large builds). It does promise what we can keep:
a reply within one working day, and a named owner for every layer.

Every engagement runs the same steps: **call → scoping → build with regular demos →
handover.** Handover is source code, schematics, build instructions and documentation,
with no lock-in. Contracts in English. Working languages English and Hungarian.
Budapest, CET.

## Offer

**No prices on the website.** Engagements are described by type and quoted per project:

- **Feasibility and scoping:** can it be built, how, and what will it cost.
- **Prototype:** a working device reporting to a working dashboard.
- **Product development:** from prototype to small-series production.
- **Take over or extend:** one layer of an existing system, or a device someone else
  built.

## Proof

**The Keep by Eldr Systems is the flagship.** An NB-IoT home monitoring hub for
accident prevention, built entirely in house: board, firmware, NB-IoT link, backend,
dashboard. Three units go into the field in November 2026. Its data is currently viewed
in an internal Grafana dashboard.

**Live plot (planned).** The homepage shows live data from The Keep (battery voltage
over time first; temperature and last check-in after), fetched from a dedicated public
endpoint on The Keep's backend. Rules:

- A separate, read-only endpoint returning pre-aggregated data (e.g. hourly averages,
  last 7–30 days), CORS-limited to our domain and cached. Never the Grafana data source
  or the internal API.
- The devices are in real homes: data is delayed by a few hours, devices are labelled
  "Device A/B/C", no locations, and owners consent in writing.
- Drawn in our own brand (small chart library or hand-rolled SVG), not a Grafana iframe.
- If the endpoint is down, the last snapshot is shown with "last updated …".
- This will be the site's first JavaScript. It must be served from our own domain and
  call only our own domain, so the footer's "no third-party requests" stays true.

Until the endpoint exists, the site carries a clearly marked placeholder chart.

**Past work.** Shown as project cards alongside The Keep, anonymised (no employer or
client names). Working list, details to be written:

- Machine maintenance CRM system
- Machine condition monitoring
- Grid data collection and analysis

Each card says the problem in one line and tags which layers it covered. Real client
case studies and testimonials replace or join these as contracts land.

## Brand Commitments

**Name:** written **Eldr Systems**: capital E, rest lowercase. Never "ELDR", never
"EldrSystems". Pronounced "EL-der". *eldr* is Old Norse for fire. Wordmark is lowercase
**eldr** with **systems** set smaller in mono. Handle `eldrsystems` everywhere; domain
eldrsystems.com.

**The Keep** is always "The Keep by Eldr Systems" in public: our own product and proof
of our end-to-end work, not a separate business. **No flames anywhere near The Keep**:
fire is the hazard it guards against. No runes, no Viking imagery.

**Personality:** confident, direct, precise, energetic. Specific over vague. Small and
personal over faceless. Ambitious about what we can build, honest about what we have
done.

**Voice rules:** numbers over adjectives; name the technology; plain English and short
sentences for second-language readers; experience shown through specifics, not years.

**Banned words:** revolutionary, cutting-edge, next-generation, game-changing,
AI-powered solutions, synergy, seamless, world-class, leverage (as a verb).

**The team.** Three founders, real photos, shared "Co-founder" role with descriptive
titles: Vencel Koczka (clients, cloud and data, the contact person), Bence Schoblocher
(firmware and connectivity), Boldizsar Karancsi (electronics and production). No
C-titles. Names without Hungarian accents, as supplied. Do not "correct" them.

**Imagery: real photographs only.** Our boards, The Keep, the bench, the three of us.
Never stock, never AI brains or robots.

**Binding visual constraints** live in `DESIGN.md` and `eldr-systems-kit/BRAND.md`
(colour tokens, one ember element per component, the Archivo width axis).

## Technical Constraints

- No third-party asset requests, no analytics, no cookies. `scripts/check.sh` fails the
  build if a third-party request appears.
- No JavaScript until the live plot; then only that, first-party.
- Fonts self-hosted, Latin and Latin-Ext (Hungarian ő and ű).
- English across the site; `/hu/` configured and disabled. Keep every surface
  translatable.
- Hungarian law requires registered seat, registration number, tax number and EU VAT
  number in the footer once the Kft. is registered.
- Unset links render as visibly disabled controls, never as links to nowhere.
- Missing content is a **visible bracketed placeholder**, never a plausible invention.
  `scripts/check.sh` lists every outstanding one.

## Evidence on Hand

**Exists:** three founder photos and bios; one technical note (PSM timers); The Keep as
a working device with a Grafana dashboard; the public site repository.

**Does not exist yet, must not be fabricated:** customers, testimonials or logos;
photos of boards and The Keep; the public data endpoint; write-ups of the three past
projects; company registration details; booking link.

## Accessibility & Inclusion

Nothing ships broken: real contrast, keyboard-reachable controls, sensible focus order,
honest alt text, reduced-motion respected. Many readers use English as a second
language, so short sentences and unambiguous labels are a requirement.
