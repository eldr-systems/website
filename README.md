# eldrsystems.com

The Eldr Systems website. Hugo + Tailwind v4, deployed to GitHub Pages.

Built from `eldr-systems-kit/`, which is the design work and stays in the repo as the
source of record.

## Running it locally

```bash
mise install    # installs the pinned Hugo (0.166.0, extended)
npm install     # installs Tailwind
hugo server     # http://localhost:1313
```

Node is a build-time dependency only. The site ships no JavaScript.

## Checking a change

```bash
./scripts/check.sh
```

Builds the site and asserts on the output:

- no bracketed placeholder ever lands in an `href` or `src`
- no third-party asset request — this is what keeps the footer claim honest
- the Archivo width axis survives into the compiled CSS
- every homepage nav anchor has a target
- fonts are served from our own domain

It also lists which placeholders are still unfilled. Those are warnings, not failures —
the site stays buildable while they are outstanding. Run it before pushing. CI runs the
same script, so a build that breaks any of the above cannot deploy.

## Editing content

| To change | Edit |
|---|---|
| Homepage headline, lead, The Keep figure | `content/_index.md` |
| An offer, or add a new one | `content/offers/*.md` |
| Publish a note | `content/notes/*.md` — new file, set `date` |
| Five layers, audience list, process steps, team | `data/*.yaml` |
| Booking link, email, social links, company details | `hugo.toml`, under `[params]` |

Adding an offer file makes it appear on the homepage **and** generates its detail page.
Publishing a note makes it appear in the homepage Proof section automatically.

Unset links degrade safely: an empty `bookingUrl` renders a visibly disabled control
rather than a link to nowhere. Fill the param and all three CTAs become live with no
template edits.

## Regenerating the fonts

Only needed if a font is added or a subset changes:

```bash
curl -A "Mozilla/5.0 ... Chrome/131.0" \
  "https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=IBM+Plex+Mono:wght@400;500&display=swap" \
  -o /tmp/gf.css
# keep only the latin and latin-ext blocks, download the woff2 files into
# assets/fonts/, then:
python3 scripts/build-fonts.py /tmp/gf-latin.css
```

`latin-ext` is required: it carries the Hungarian **ő** and **ű**.

## Regenerating the OG image

`static/graphics/og-image.png` is rendered from the SVG. A PNG is required because
LinkedIn, Slack and Facebook all reject an SVG `og:image`.

```bash
rsvg-convert -w 1200 -h 630 static/graphics/og-image-1200x630.svg -o static/graphics/og-image.png
```

The source SVG uses live text, so Archivo must be installed locally for this to render
correctly — see the note in `eldr-systems-kit/README.md`.

## Brand rules the code cannot enforce

- **One ember element per component, never two.** Ember is rationed; that is why the
  design holds together.
- **The ember logo tile appears exactly once**, at the closing CTA.
- Display type needs its width axis (`font-stretch: 112%`), not weight alone. Use the
  `display-xl` / `display-lg` / `display-md` / `display-cta` utilities rather than
  writing type styles by hand.
- Numbers over adjectives. Banned: revolutionary, cutting-edge, next-generation,
  game-changing, seamless, world-class, leverage as a verb.
- Real photos only. The SVGs in `graphics/` are placeholders that look deliberate —
  which is a trap, because it is easy to ship and never replace them.

Full rules: `eldr-systems-kit/BRAND.md`.

## Still to do before launch

`./scripts/check.sh` prints the list on every run. Currently outstanding:

| Item | Owner |
|---|---|
| Booking link (`bookingUrl` in `hugo.toml`) | Vencel |
| Offer prices — fill in or drop entirely | Vencel |
| Email addresses, once provisioned | Vencel |
| LinkedIn company page, YouTube channel | Vencel |
| Kft. registration: seat, reg. no., tax no., EU VAT | after registration |
| The Keep's `[X] µA` figure, from a real measurement | Bence |
| The Keep demo video | Bence, Boldizsar |
| Team titles — `roleA`/`roleB`/`roleC` are placeholders | the three of you |
| Real photography: bench photo, power-profiler trace, The Keep in a distribution box | all |
| Hungarian copy — `/hu/` is configured but disabled | later |

## Deployment

Push to `main`. GitHub Actions builds, runs `check.sh`, and publishes to GitHub Pages.
`static/CNAME` carries the custom domain; DNS is on Cloudflare.
