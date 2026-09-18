# Eldr Systems website — design

**Date:** 2026-09-18
**Status:** approved pending review
**Repo:** `git@github.com:eldr-systems/website.git`
**Domain:** eldrsystems.com (DNS on Cloudflare), hosted on GitHub Pages

---

## Goal

Turn `eldr-systems-kit/` — a finished single-file homepage plus tokens, logos, icons and
graphics — into a maintainable multi-page site that the three founders can edit and that
grows into a case-study site without a rebuild.

## Decisions taken

| Decision | Choice | Reason |
|---|---|---|
| Generator | Hugo (extended) | Single binary, fast, mature multilingual support for the later `/hu/` |
| Scope | Full site: homepage, offer detail pages, notes collection | The "Details →" links and the Notes nav item are already in the design |
| Hungarian | Structure now, content later | Routes configured, nav link hidden until copy exists |
| Fonts | Self-hosted, subset | No third-party request, so "No cookies." stays honest for EU visitors |
| CSS | Tailwind v4, CSS-first config | Chosen by the team; brand invariants pinned in `@theme` (see below) |
| Analytics | None at launch | Zero third-party scripts; Plausible is a one-line change later |
| Typeface | Archivo | The design uses it; `BRAND.md` says IBM Plex Sans. Resolved in favour of Archivo — the brand file needs updating, not the site |

## Toolchain

- **Hugo extended 0.166**, installed per-project via `mise` so all three founders get the
  same version from `mise.toml`.
- **Tailwind v4** via npm, invoked through Hugo's `css.TailwindCSS` pipe. Node is a
  build-time dependency only — nothing ships to the browser.
- Build is one command: `hugo`. Dev is `hugo server`.

## Brand invariants

The parts of this design that are easiest to lose have no stock Tailwind utilities.
They are defined once and referenced everywhere, never written as arbitrary values:

- Display type: `font-stretch: 112%`, `letter-spacing: -0.03em`, `font-weight: 800`.
  Losing the width axis is, per `BRAND.md`, the fastest way to make this look generic.
- The fluid `clamp()` scale from `tokens.css` (hero, h2, h3, cta, lead) becomes
  `@theme` font-size tokens.
- Colour tokens ink/bone/ember/slate plus the six derived greys.
- **One ember element per component, never two.** Not enforceable in CSS; called out in
  a comment at the top of `main.css` and in the README.

## Repo layout

```
hugo.toml                  baseURL, menus, languages, params
mise.toml                  pins hugo-extended
package.json               tailwindcss + @tailwindcss/cli only
assets/
  css/main.css             @import "tailwindcss"; @theme tokens; @utility rules
  css/fonts.css            @font-face
  fonts/*.woff2            Archivo variable + IBM Plex Mono, Latin + Latin-Ext
content/
  _index.md                homepage section copy in front matter
  offers/_index.md
  offers/poc-sprint.md
  offers/battery-connectivity.md
  offers/device-analytics.md
  notes/_index.md
  notes/*.md
  privacy.md
  company.md
data/
  layers.yaml              five layers
  audience.yaml            who it's for
  team.yaml                three founders
  process.yaml             how we work, four steps
layouts/
  baseof.html  home.html  list.html  single.html
  _partials/head.html  header.html  footer.html  icon.html  sprite.html
  _partials/sections/*.html
  offers/  notes/
static/
  logo/  graphics/  CNAME  robots.txt
.github/workflows/deploy.yml
```

Hugo 0.146 dropped `layouts/_default/`; this uses the current flat template layout with
`_partials/`.

## Content model

**Rule: anything the team might edit lives in `content/` or `data/`, never in a template.**

- Offer cards on the homepage read from `content/offers/`. Adding an offer is one
  Markdown file and it appears on the homepage *and* gets a detail page.
- Team members read from `data/team.yaml`.
- The Proof section pulls the three newest `content/notes/` entries, so it fills itself
  as write-ups are published.
- All bracketed placeholders are consolidated into `hugo.toml` params, in one place.

## Routes

| Route | Template | Notes |
|---|---|---|
| `/` | `home.html` | Eleven sections |
| `/offers/` | `list.html` | Index of the three offers |
| `/offers/{slug}/` | `offers/single.html` | Makes the existing "Details →" links real |
| `/notes/` | `notes/list.html` | Write-ups index |
| `/notes/{slug}/` | `notes/single.html` | |
| `/privacy/`, `/company/` | `single.html` | Makes the existing footer links resolve |
| `/hu/` | — | Configured in `hugo.toml`, `disabled = true`. Nav link hidden until copy lands |
| `/404.html` | `404.html` | Uses `graphics/404.svg` |

## Homepage sections

Seven ported from `page/index.html`, four new. In order:

1. Header
2. Hero
3. Five layers
4. Who it's for
5. Offers
6. **How we work** *(new)* — call → scoping document → build with weekly demos →
   handover with docs and source. Uses `graphics/how-we-work-four-steps.svg`.
7. The Keep
8. **Proof** *(new)* — three newest notes.
9. **Team** *(new)* — three cards from `data/team.yaml`, `portrait-placeholder.svg`
   until real photos exist. Per the kit, this matters most for a three-person firm.
10. **Where and how** *(new)* — Budapest, EU-wide, CET, English and Hungarian,
    contracts in English. Mono-set.
11. Closing CTA + footer

The ported sections keep their bespoke arc-and-ember-dot SVGs — those are the design,
not generic icons. The 32-icon sprite is inlined once per page and referenced with
`<use href="#eldr-name">`; its symbols use `var(--eldr-ink, #14161A)` so they follow
the tokens.

### Nav fixes

`page/index.html` has `id="work"` on the five-layers section, `id="notes"` on The Keep's
stat block, and `id="team"` on the closing CTA. All three nav links currently land in the
wrong place. Nav is rebuilt against real section IDs, with Notes pointing at `/notes/`.

## Known values

```
Founders (titles deliberately unset — pending team discussion):
  Vencel Koczka        co-founder, roleA   vencel@eldrsystems.com
  Bence Schoblocher    co-founder, roleB   bence@eldrsystems.com
  Boldizsar Karancsi   co-founder, roleC   boldizsar@eldrsystems.com

Phone:   +36 30 123 1234        (dummy, to be replaced)
GitHub:  https://github.com/eldr-systems
LinkedIn: https://www.linkedin.com/   (placeholder — no company page yet)
YouTube:  placeholder
Email addresses are not yet provisioned.
```

Names are written without Hungarian accents, as given. This is deliberate, not an
encoding failure — do not "correct" them later.

## Confirmed placeholder decisions

- **Prices stay bracketed** — `from €[6,000]`, `from €[3,000]`, `from €[3,500]`,
  exactly as the kit has them. The show-or-drop question is deferred, not answered.
- **Booking link stays a placeholder** — no scheduling account exists yet. It renders as
  a visibly disabled control rather than a live link to nowhere (see below).
- **Domain and Cloudflare setup happen after the site builds**, walked through step by
  step at that point.

## Placeholder discipline

Every unresolved value lives in one `[params.placeholders]` block in `hugo.toml`. A Hugo
template check emits a build warning naming each one still unfilled, so the site cannot
quietly go live claiming a price nobody set or a mailbox nobody created.

**Unset links must not render as broken links.** `page/index.html` currently has
`href="[BOOKING LINK]"` in three places, which a browser resolves as a relative path and
serves a 404. Instead, a `booking_cta` partial takes the URL from params and:

- if set → renders a normal `<a>` pill;
- if empty → renders a visually identical `<span>` with `aria-disabled="true"` and no
  href, so nothing is clickable and nothing 404s.

Filling in `booking_url` later turns all three into live links with no template edits.
The same pattern covers the LinkedIn, YouTube and email placeholders.

Still open at time of writing: booking link, the three prices, `[X] µA`, the demo video,
Kft. registration details (seat, reg. no., tax no., EU VAT), LinkedIn, YouTube, real
photos, and the measured `[X] kB` footer figure.

## Deployment

GitHub Actions builds and publishes to GitHub Pages on push to `main`. The workflow pins
the Hugo version to match `mise.toml`. `static/CNAME` carries `eldrsystems.com`.

Because the repo is `eldr-systems/website` rather than `eldr-systems.github.io`, the
custom domain is what keeps paths at the root; `baseURL` is `https://eldrsystems.com/`.

## Non-goals

- No JavaScript framework. No client-side JS at all unless a specific feature needs it.
- No CMS. Markdown in the repo is the CMS.
- No dark mode — the brand is bone-on-ink by design, one surface.
- No blog comments, no newsletter, no search.
- Hungarian copy is out of scope for this build.
