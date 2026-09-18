# Eldr Systems Website Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn `eldr-systems-kit/` into a Hugo site deployed to GitHub Pages at eldrsystems.com, with a complete homepage, offer detail pages and a notes collection.

**Architecture:** Hugo extended 0.166 renders static HTML. Tailwind v4 runs inside Hugo's asset pipeline via `css.TailwindCSS`, configured CSS-first with `@theme` so the brand tokens from `tokens/tokens.css` become Tailwind utilities. Everything the team might edit lives in `content/` or `data/`; templates hold structure only. No client-side JavaScript.

**Tech Stack:** Hugo extended 0.166 (via `~/.local/bin/hugo`, pinned in `mise.toml`), Tailwind CSS v4 + `@tailwindcss/cli` (build-time only, via npm), self-hosted Archivo + IBM Plex Mono woff2, GitHub Actions → GitHub Pages.

**Verification approach:** A static site has no unit tests in the usual sense. The equivalent is asserting on built output. `scripts/check.sh` is the test suite: it builds the site and greps `public/` for invariants — unresolved placeholders in `href`s, missing brand typography, broken internal links, page weight. Every task ends by running it.

---

## File Structure

| File | Responsibility |
|---|---|
| `hugo.toml` | Site config, menus, languages, all params and placeholders |
| `mise.toml` | Pins hugo-extended so all three founders build identically |
| `package.json` | `@tailwindcss/cli` only — build-time |
| `assets/css/main.css` | Tailwind import, `@theme` tokens, `@utility` brand rules |
| `assets/css/fonts.css` | `@font-face` for the self-hosted woff2 files |
| `assets/fonts/*.woff2` | Archivo variable + IBM Plex Mono, latin + latin-ext |
| `layouts/baseof.html` | HTML skeleton |
| `layouts/home.html` | Homepage — composes the eleven section partials |
| `layouts/page.html`, `layouts/list.html` | Generic single/list pages |
| `layouts/offers/`, `layouts/notes/` | Section-specific templates |
| `layouts/_partials/head.html` | Meta, OG tags, CSS pipeline, favicon |
| `layouts/_partials/header.html`, `footer.html` | Site chrome |
| `layouts/_partials/cta-link.html` | Renders a link *or* a disabled span if the URL param is empty |
| `layouts/_partials/icon.html` | `<use href="#eldr-name">` from the inlined sprite |
| `layouts/_partials/sections/*.html` | One file per homepage section |
| `data/*.yaml` | layers, audience, team, process |
| `content/` | Homepage copy, offers, notes, privacy, company |
| `static/` | logo, graphics, sprite, CNAME, robots.txt |
| `scripts/check.sh` | Build-output assertions — the test suite |
| `.github/workflows/deploy.yml` | Build and publish to Pages |

---

## Task 1: Scaffold the Hugo project and prove the toolchain works

**Files:**
- Create: `hugo.toml`, `mise.toml`, `package.json`, `.gitignore` (update)
- Create: `assets/css/main.css`
- Create: `layouts/baseof.html`, `layouts/home.html`
- Create: `scripts/check.sh`

- [ ] **Step 1: Pin Hugo and install Tailwind**

```bash
cd /home/koczka990/Projects/eldr-systems/website
printf '[tools]\nhugo-extended = "0.166.0"\n' > mise.toml
npm init -y
npm install --save-dev @tailwindcss/cli@^4
```

Expected: `node_modules/` appears, `package.json` lists `@tailwindcss/cli`.

- [ ] **Step 2: Write `hugo.toml`**

`buildStats` is what makes Tailwind work — it writes `hugo_stats.json` listing every
class, tag and id Hugo emitted, which Tailwind then scans instead of the source files.

```toml
baseURL = 'https://eldrsystems.com/'
languageCode = 'en-GB'
defaultContentLanguage = 'en'
title = 'Eldr Systems'
enableRobotsTXT = true

[build]
  [build.buildStats]
    enable = true
  [[build.cachebusters]]
    source = 'assets/notwatching/hugo_stats\.json'
    target = 'css'
  [[build.cachebusters]]
    source = '(postcss|tailwind)\.config\.js'
    target = 'css'

[module]
  [[module.mounts]]
    source = 'assets'
    target = 'assets'
  [[module.mounts]]
    source = 'hugo_stats.json'
    target = 'assets/notwatching/hugo_stats.json'
    disableWatch = true

[languages]
  [languages.en]
    languageName = 'English'
    weight = 1
  [languages.hu]
    languageName = 'Magyar'
    weight = 2
    disabled = true

[params]
  description = 'Eldr Systems builds low-power connected measurement devices end to end: electronics, firmware, NB-IoT/LTE-M connectivity, cloud and data analysis. Budapest.'
  ogDescription = 'Low-power cellular IoT and energy monitoring, engineered end to end by a small team in Budapest.'
  github = 'https://github.com/eldr-systems'

  # Unset on purpose. Anything empty renders as a disabled control,
  # never as a broken link. scripts/check.sh lists what is still empty.
  bookingUrl = ''
  email = ''
  linkedin = ''
  youtube = ''
  phone = '+36 30 123 1234'

  [params.company]
    legalName = 'Eldr Systems Kft.'
    seat = ''
    regNo = ''
    taxNo = ''
    vatNo = ''
```

- [ ] **Step 3: Write `assets/css/main.css`**

```css
/* Eldr Systems.
   Brand rule that CSS cannot enforce: ONE ember element per component, never two. */
@import "tailwindcss";
@source "hugo_stats.json";
```

- [ ] **Step 4: Write `layouts/baseof.html`**

```html
<!doctype html>
<html lang="{{ .Site.Language.LanguageCode | default "en" }}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ if .IsHome }}{{ .Site.Title }}{{ else }}{{ .Title }} — {{ .Site.Title }}{{ end }}</title>
  {{ with resources.Get "css/main.css" }}
    {{ $opts := dict "minify" hugo.IsProduction }}
    {{ with . | css.TailwindCSS $opts }}
      <link rel="stylesheet" href="{{ .RelPermalink }}">
    {{ end }}
  {{ end }}
</head>
<body class="bg-bone text-ink">
  {{ block "main" . }}{{ end }}
</body>
</html>
```

- [ ] **Step 5: Write `layouts/home.html`**

```html
{{ define "main" }}
<h1 class="text-4xl font-extrabold">Eldr Systems</h1>
{{ end }}
```

- [ ] **Step 6: Write `scripts/check.sh`**

This is the test suite. It grows in later tasks; start with the build gate.

```bash
#!/usr/bin/env bash
# Build-output assertions for the Eldr Systems site.
set -uo pipefail
cd "$(dirname "$0")/.."

fail=0
ok()   { printf '  ok    %s\n' "$1"; }
bad()  { printf '  FAIL  %s\n' "$1"; fail=1; }
warn() { printf '  warn  %s\n' "$1"; }

echo "==> build"
if ! hugo --gc --minify --quiet; then
  echo "  FAIL  hugo build failed"; exit 1
fi
ok "hugo build"

echo "==> unresolved placeholders in links"
if grep -rlE 'href="\[|src="\[' public/ >/dev/null 2>&1; then
  grep -rhoE '(href|src)="\[[^"]*\]"' public/ | sort -u | sed 's/^/        /'
  bad "bracketed placeholder used as a URL"
else
  ok "no bracketed placeholders in href/src"
fi

echo "==> page weight"
if [ -f public/index.html ]; then
  bytes=$(wc -c < public/index.html)
  ok "index.html $((bytes / 1024)) kB ($bytes bytes)"
fi

echo
[ "$fail" -eq 0 ] && echo "PASS" || echo "FAILED"
exit $fail
```

- [ ] **Step 7: Run the check — it must pass**

```bash
chmod +x scripts/check.sh && ./scripts/check.sh
```

Expected: `ok hugo build`, `ok no bracketed placeholders`, a kB figure, then `PASS`.
If Hugo errors on `css.TailwindCSS`, confirm `npx @tailwindcss/cli --help` runs.

- [ ] **Step 8: Update `.gitignore` and commit**

```bash
printf 'public/\nresources/_gen/\n.hugo_build.lock\nnode_modules/\nhugo_stats.json\n.DS_Store\n' > .gitignore
git add -A
git commit -m "Scaffold Hugo project with Tailwind v4 pipeline"
```

---

## Task 2: Self-host the fonts

Google serves Archivo as a genuine variable font (`font-weight: 400 900; font-stretch: 62% 125%`) — both axes the brand needs. `latin-ext` carries `ő` U+0151 and `ű` U+0171.

**Files:**
- Create: `assets/fonts/*.woff2`, `assets/css/fonts.css`
- Modify: `assets/css/main.css`

- [ ] **Step 1: Download the woff2 files**

```bash
mkdir -p assets/fonts && cd assets/fonts
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/131.0 Safari/537.36'
curl -s -A "$UA" "https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..900&family=IBM+Plex+Mono:wght@400;500&display=swap" -o /tmp/gf.css

# Keep only the latin and latin-ext blocks; drop cyrillic and vietnamese.
awk '/\/\* latin(-ext)? \*\//{keep=1} /\/\* (cyrillic|cyrillic-ext|vietnamese|greek|greek-ext) \*\//{keep=0} keep' /tmp/gf.css > /tmp/gf-latin.css
grep -oE 'https://fonts\.gstatic\.com[^)]+\.woff2' /tmp/gf-latin.css | sort -u | while read -r url; do
  curl -sSL "$url" -O
done
ls -la *.woff2
cd ../..
```

Expected: 4–6 `.woff2` files, roughly 15–60 kB each.

- [ ] **Step 2: Verify Hungarian glyphs survived the subset**

```bash
grep -A2 '/\* latin-ext \*/' /tmp/gf-latin.css | grep -o 'U+0100-024F' && echo "latin-ext covers U+0151 and U+0171"
```

Expected: the range prints. U+0151 (`ő`) and U+0171 (`ű`) both fall inside U+0100–024F.

- [ ] **Step 3: Write `assets/css/fonts.css`**

Generate it from the downloaded CSS so the `unicode-range` values stay exact:

```bash
sed -E 's#https://fonts\.gstatic\.com/[^)]*/([^/)]+\.woff2)#/fonts/\1#' /tmp/gf-latin.css > assets/css/fonts.css
head -20 assets/css/fonts.css
```

Expected: `@font-face` blocks with `src: url(/fonts/xxxx.woff2)`, `font-stretch: 62% 125%` preserved on Archivo.

- [ ] **Step 4: Mount fonts to a public path and import the CSS**

Add to `hugo.toml` under `[module]`:

```toml
  [[module.mounts]]
    source = 'assets/fonts'
    target = 'static/fonts'
```

Prepend to `assets/css/main.css`, above the Tailwind import:

```css
@import "./fonts.css";
@import "tailwindcss";
@source "hugo_stats.json";
```

- [ ] **Step 5: Verify the fonts are served and referenced**

```bash
hugo --gc --quiet && ls public/fonts/*.woff2 | head && grep -o 'font-stretch:62% 125%\|font-stretch: 62% 125%' public/css/*.css | head -1
```

Expected: woff2 files present under `public/fonts/`, and the variable width axis appears in the built CSS.

- [ ] **Step 6: Add a font assertion to `scripts/check.sh`**

Insert before the `page weight` block:

```bash
echo "==> self-hosted fonts"
if grep -rq 'fonts\.googleapis\.com\|fonts\.gstatic\.com' public/; then
  bad "still requesting fonts from Google"
else
  ok "no third-party font requests"
fi
if ls public/fonts/*.woff2 >/dev/null 2>&1; then
  ok "$(ls public/fonts/*.woff2 | wc -l) woff2 files served locally"
else
  bad "no local woff2 files"
fi
```

- [ ] **Step 7: Run the check and commit**

```bash
./scripts/check.sh && git add -A && git commit -m "Self-host Archivo and IBM Plex Mono"
```

Expected: `PASS`, including `no third-party font requests`.

---

## Task 3: Brand tokens as Tailwind theme

Everything in `eldr-systems-kit/tokens/tokens.css` becomes a Tailwind token so the design can be written in utilities without arbitrary values.

**Files:**
- Modify: `assets/css/main.css`

- [ ] **Step 1: Add the `@theme` block**

Append to `assets/css/main.css`:

```css
@theme {
  /* Colour — ration the ember. One per component. */
  --color-ink:       #14161A;
  --color-bone:      #F4F1EA;
  --color-ember:     #E2632B;
  --color-ember-dark:#C9551F;
  --color-slate:     #5B6B7A;
  --color-body:      #3A434C;
  --color-muted:     #4E5A66;
  --color-rule:      #C9C3B6;
  --color-rule-dark: #2B3036;
  --color-on-ink:    #C9CFD5;
  --color-muted-ink: #9AA5AF;

  --font-display: 'Archivo', 'Helvetica Neue', Helvetica, Arial, sans-serif;
  --font-mono:    'IBM Plex Mono', ui-monospace, Menlo, Consolas, monospace;

  /* Fluid scale: min at 390px viewport, max at 1440px. */
  --text-hero:  clamp(2.5rem, 1.30rem + 4.92vw, 4.625rem);
  --text-h2:    clamp(1.875rem, 1.28rem + 2.43vw, 2.75rem);
  --text-h3:    clamp(1.375rem, 1.10rem + 1.12vw, 1.75rem);
  --text-cta:   clamp(2.75rem, 1.16rem + 6.51vw, 5rem);
  --text-lead:  clamp(1.0625rem, 0.97rem + 0.38vw, 1.25rem);
  --text-label: 0.8125rem;

  --spacing-gutter:  clamp(1.25rem, 0.30rem + 3.90vw, 5rem);
  --spacing-section: clamp(3.5rem, 2.36rem + 4.68vw, 5.5rem);

  --radius-card: 26px;
  --container-page: 1440px;
}
```

- [ ] **Step 2: Add the brand utilities**

These carry the width axis and tracking. `BRAND.md`: "Losing the width axis is the
fastest way to make this look like a generic template." Defining them once means a
section cannot silently drop them.

```css
/* Display type is Archivo with WIDTH + tight tracking, not weight alone. */
@utility display-xl {
  font-family: var(--font-display);
  font-weight: 800;
  font-stretch: 112%;
  letter-spacing: -0.035em;
  line-height: 0.98;
}
@utility display-lg {
  font-family: var(--font-display);
  font-weight: 800;
  font-stretch: 112%;
  letter-spacing: -0.03em;
  line-height: 1.05;
}
@utility display-md {
  font-family: var(--font-display);
  font-weight: 800;
  font-stretch: 108%;
  letter-spacing: -0.02em;
  line-height: 1.05;
}
@utility display-cta {
  font-family: var(--font-display);
  font-weight: 850;
  font-stretch: 118%;
  letter-spacing: -0.04em;
  line-height: 0.96;
}
@utility label-mono {
  font-family: var(--font-mono);
  font-size: var(--text-label);
  color: var(--color-muted);
}

@layer base {
  html { -webkit-text-size-adjust: 100%; }
  body {
    background: var(--color-bone);
    color: var(--color-ink);
    font-family: var(--font-display);
    line-height: 1.5;
    -webkit-font-smoothing: antialiased;
  }
  a:hover { text-decoration: underline; text-underline-offset: 4px; }
  :focus-visible { outline: 3px solid var(--color-ember); outline-offset: 3px; }
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
      animation-duration: 0.01ms !important;
      transition-duration: 0.01ms !important;
    }
  }
}
```

- [ ] **Step 3: Exercise the tokens so Tailwind emits them**

Replace `layouts/home.html` body with:

```html
{{ define "main" }}
<h1 class="display-xl text-hero text-ink">We build connected measurement devices, from circuit board to dashboard.</h1>
<p class="label-mono">Low-power cellular IoT · Budapest</p>
{{ end }}
```

- [ ] **Step 4: Verify the width axis reaches the output**

```bash
hugo --gc --quiet && grep -o 'font-stretch: *112%' public/css/*.css | head -1 && grep -o 'clamp(2.5rem' public/css/*.css | head -1
```

Expected: both print. If `font-stretch` is missing, the `@utility` did not compile — check that `hugo_stats.json` exists and lists `display-xl`.

- [ ] **Step 5: Add a brand-invariant assertion to `scripts/check.sh`**

```bash
echo "==> brand typography"
if grep -rq 'font-stretch' public/css/ 2>/dev/null; then
  ok "width axis present in CSS"
else
  bad "font-stretch missing — the Archivo width axis was lost"
fi
```

- [ ] **Step 6: Run the check and commit**

```bash
./scripts/check.sh && git add -A && git commit -m "Map brand tokens into Tailwind theme"
```

---

## Task 4: Static assets and the icon sprite

**Files:**
- Create: `static/logo/`, `static/graphics/`, `static/robots.txt`
- Create: `layouts/_partials/sprite.html`, `layouts/_partials/icon.html`
- Create: `layouts/_partials/head.html`
- Modify: `layouts/baseof.html`

- [ ] **Step 1: Copy logos and graphics out of the kit**

```bash
mkdir -p static/logo static/graphics assets/svg
cp eldr-systems-kit/logo/*.svg static/logo/
cp eldr-systems-kit/graphics/*.svg static/graphics/
cp eldr-systems-kit/icons/_sprite.svg assets/svg/sprite.svg
ls static/logo | wc -l && ls static/graphics | wc -l
```

Expected: 9 logo files, 21 graphics.

- [ ] **Step 2: Write `layouts/_partials/sprite.html`**

Inlining the sprite (rather than linking it) is what lets its `var(--eldr-ink)` fills
follow the page tokens.

```html
{{ with resources.Get "svg/sprite.svg" }}{{ .Content | safeHTML }}{{ end }}
```

- [ ] **Step 3: Write `layouts/_partials/icon.html`**

Called as `{{ partial "icon.html" (dict "name" "solar" "class" "w-16 h-16") }}`.

```html
{{- $name := .name -}}
{{- $class := .class | default "w-16 h-16" -}}
<svg class="{{ $class }}" aria-hidden="true" focusable="false"><use href="#eldr-{{ $name }}"></use></svg>
```

- [ ] **Step 4: Write `layouts/_partials/head.html`**

```html
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{ if .IsHome }}{{ .Site.Title }} — connected measurement devices, circuit board to dashboard{{ else }}{{ .Title }} — {{ .Site.Title }}{{ end }}</title>
<meta name="description" content="{{ .Description | default .Site.Params.description }}">
<link rel="icon" href="/logo/favicon.svg" type="image/svg+xml">

<meta property="og:title" content="{{ if .IsHome }}{{ .Site.Title }}{{ else }}{{ .Title }}{{ end }}">
<meta property="og:description" content="{{ .Description | default .Site.Params.ogDescription }}">
<meta property="og:type" content="{{ if .IsPage }}article{{ else }}website{{ end }}">
<meta property="og:url" content="{{ .Permalink }}">
<meta property="og:image" content="{{ "graphics/og-image-1200x630.svg" | absURL }}">

{{ with resources.Get "css/main.css" }}
  {{ $opts := dict "minify" hugo.IsProduction }}
  {{ with . | css.TailwindCSS $opts }}
    {{ if hugo.IsProduction }}
      {{ with . | fingerprint }}
        <link rel="stylesheet" href="{{ .RelPermalink }}" integrity="{{ .Data.Integrity }}">
      {{ end }}
    {{ else }}
      <link rel="stylesheet" href="{{ .RelPermalink }}">
    {{ end }}
  {{ end }}
{{ end }}
```

- [ ] **Step 5: Rewrite `layouts/baseof.html` to use them**

```html
<!doctype html>
<html lang="{{ .Site.Language.LanguageCode | default "en" }}">
<head>{{ partial "head.html" . }}</head>
<body class="bg-bone text-ink font-display">
  {{ partial "sprite.html" . }}
  <div class="mx-auto max-w-page">
    {{ partial "header.html" . }}
    {{ block "main" . }}{{ end }}
    {{ partial "footer.html" . }}
  </div>
</body>
</html>
```

- [ ] **Step 6: Write `static/robots.txt`**

```
User-agent: *
Allow: /

Sitemap: https://eldrsystems.com/sitemap.xml
```

- [ ] **Step 7: Commit (build will fail until Task 5 adds header/footer)**

```bash
git add -A && git commit -m "Add logos, graphics and icon sprite"
```

---

## Task 5: Header, footer, and the disabled-link pattern

The kit's `href="[BOOKING LINK]"` would 404. `cta-link.html` makes an unset URL render as a non-clickable span instead.

**Files:**
- Create: `layouts/_partials/cta-link.html`, `header.html`, `footer.html`
- Modify: `scripts/check.sh`

- [ ] **Step 1: Write `layouts/_partials/cta-link.html`**

Called as `{{ partial "cta-link.html" (dict "url" .Site.Params.bookingUrl "text" "Book a 20-minute call" "class" "pill-ember") }}`.

```html
{{- $url := .url | default "" -}}
{{- $text := .text -}}
{{- $class := .class | default "" -}}
{{- if $url -}}
<a href="{{ $url }}" class="{{ $class }}">{{ $text }}</a>
{{- else -}}
<span class="{{ $class }} opacity-50 cursor-not-allowed" aria-disabled="true" title="Not yet available">{{ $text }}</span>
{{- end -}}
```

- [ ] **Step 2: Add pill utilities to `assets/css/main.css`**

```css
@utility pill-base {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 48px;
  padding: 0.9rem 1.6rem;
  border-radius: 999px;
  font-weight: 700;
  font-size: 1.0625rem;
  text-align: center;
}
@utility pill-ember {
  @apply pill-base;
  background: var(--color-ember);
  color: var(--color-ink);
}
@utility pill-ink {
  @apply pill-base;
  background: var(--color-ink);
  color: var(--color-bone);
}
@utility pill-outline {
  @apply pill-base;
  border: 2px solid var(--color-ink);
  padding: 0.8rem 1.5rem;
}
```

- [ ] **Step 3: Write `layouts/_partials/header.html`**

Nav IDs are corrected here: the kit pointed `#work`, `#notes` and `#team` at the wrong elements.

```html
<header class="flex flex-wrap items-center justify-between gap-4 px-gutter py-5">
  <a class="flex items-center gap-3.5 hover:no-underline" href="/">
    <svg viewBox="0 0 512 512" class="w-11 h-11 shrink-0" role="img" aria-label="Eldr Systems">
      <rect width="512" height="512" rx="74.7" fill="#F4F1EA"/>
      <path fill="#14161A" d="M412.52 279.08A158.22 158.22 0 1 0 366.48 369.25L334.24 336.21A112.05 112.05 0 0 1 146.35 279.08ZM146.35 232.92A112.05 112.05 0 0 1 365.65 232.92Z"/>
      <circle cx="375.12" cy="319.8" r="23.08" fill="#E2632B"/>
    </svg>
    <span class="flex items-baseline gap-[7px]">
      <span class="text-3xl font-[850] [font-stretch:120%] tracking-[-0.035em] leading-none">eldr</span>
      <span class="label-mono">systems</span>
    </span>
  </a>
  <nav class="flex flex-wrap items-center gap-[clamp(1rem,2vw,2rem)] text-[0.9375rem] font-medium" aria-label="Main">
    <a href="/#offers">Offers</a>
    <a href="/#layers">What we build</a>
    <a href="/notes/">Notes</a>
    <a href="/#keep">The Keep</a>
    <a href="/#team">Team</a>
    {{ partial "cta-link.html" (dict "url" .Site.Params.bookingUrl "text" "Book a call" "class" "pill-outline") }}
  </nav>
</header>
```

The `HU` link is intentionally absent — the Hungarian site is `disabled = true`, and a
link to a page that does not exist is worse than no link.

- [ ] **Step 4: Write `layouts/_partials/footer.html`**

```html
{{ $c := .Site.Params.company }}
<footer class="flex flex-wrap items-start justify-between gap-8 border-t-2 border-ink px-gutter pt-8 pb-12 font-mono text-label leading-[1.8] text-body">
  <div class="flex items-start gap-4">
    <svg viewBox="0 0 512 512" class="w-8 h-8 shrink-0" aria-hidden="true">
      <rect width="512" height="512" rx="74.7" fill="#14161A"/>
      <path fill="#F4F1EA" d="M412.52 279.08A158.22 158.22 0 1 0 366.48 369.25L334.24 336.21A112.05 112.05 0 0 1 146.35 279.08ZM146.35 232.92A112.05 112.05 0 0 1 365.65 232.92Z"/>
      <circle cx="375.12" cy="319.8" r="23.08" fill="#E2632B"/>
    </svg>
    <div class="flex flex-col">
      <span>{{ $c.legalName }}{{ with $c.seat }} · {{ . }}{{ end }}, Budapest</span>
      <span>Reg. no. {{ $c.regNo | default "—" }} · Tax no. {{ $c.taxNo | default "—" }} · EU VAT {{ $c.vatNo | default "—" }}</span>
    </div>
  </div>
  <div class="flex flex-col items-start sm:items-end sm:text-right">
    <span>
      <a href="/privacy/">Privacy</a> ·
      <a href="/company/">Company details</a> ·
      {{ partial "cta-link.html" (dict "url" .Site.Params.linkedin "text" "LinkedIn") }} ·
      <a href="{{ .Site.Params.github }}">GitHub</a> ·
      {{ partial "cta-link.html" (dict "url" .Site.Params.youtube "text" "YouTube") }}
    </span>
    <span>No cookies.</span>
  </div>
</footer>
```

- [ ] **Step 5: Verify header and footer render with no broken links**

```bash
./scripts/check.sh
grep -o 'aria-disabled="true"' public/index.html | wc -l
```

Expected: `PASS`, and 3 or more `aria-disabled` spans (booking in header, LinkedIn, YouTube) — proving unset params degrade safely.

- [ ] **Step 6: Commit**

```bash
git add -A && git commit -m "Add header and footer with safe placeholder links"
```

---

## Task 6: Data files

**Files:**
- Create: `data/layers.yaml`, `data/audience.yaml`, `data/process.yaml`, `data/team.yaml`

- [ ] **Step 1: Write `data/layers.yaml`**

```yaml
- name: Sensor + PCB
  line: Voltage, current and power, measured safely near mains.
  icon: pcb
- name: Firmware
  line: Sleep budgets, power-saving modes and OTA updates.
  icon: firmware
- name: NB-IoT / LTE-M
  line: PSM and eDRX tuned for the operator and the site.
  icon: nb-iot
- name: Cloud
  line: Ingest, storage, alerts and a simple dashboard.
  icon: cloud
- name: Analytics
  line: We find faults in your device data.
  icon: anomaly
```

- [ ] **Step 2: Write `data/audience.yaml`**

`ember: true` marks the one secondary line. Exactly one entry may set it.

```yaml
- text: Solar and battery installers
- text: EV-charger and heat-pump companies
- text: Energy management startups
- text: Building operators
- text: Cellular devices with battery or connection trouble
  ember: true
```

- [ ] **Step 3: Write `data/process.yaml`**

From `BRAND.md`'s "How we work": call → scoping document → build with weekly demos → handover.

```yaml
- step: "01"
  name: Call
  line: Twenty minutes. You describe what you need to measure and where.
  icon: book-a-call
- step: "02"
  name: Scoping document
  line: Fixed scope, fixed price, named deliverables. You own it whether or not we build.
  icon: fixed-scope
- step: "03"
  name: Build, with weekly demos
  line: Working hardware and data every week, not a status report.
  icon: interval
- step: "04"
  name: Handover
  line: Source code, schematics, build instructions and documentation. No lock-in.
  icon: handover
```

- [ ] **Step 4: Write `data/team.yaml`**

Names are unaccented deliberately. Titles are placeholders pending a team discussion.

```yaml
- name: Vencel Koczka
  role: Co-founder
  title: roleA
  email: vencel@eldrsystems.com
  photo: /graphics/portrait-placeholder.svg
- name: Bence Schoblocher
  role: Co-founder
  title: roleB
  email: bence@eldrsystems.com
  photo: /graphics/portrait-placeholder.svg
- name: Boldizsar Karancsi
  role: Co-founder
  title: roleC
  email: boldizsar@eldrsystems.com
  photo: /graphics/portrait-placeholder.svg
```

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "Add site data files"
```

---

## Task 7: Homepage sections ported from the kit

Port hero, layers, audience, offers, keep and CTA from `eldr-systems-kit/page/index.html`. Keep the bespoke arc-and-ember-dot SVGs — those are the design, not generic icons.

**Files:**
- Create: `layouts/_partials/sections/{hero,layers,audience,offers,keep,cta}.html`
- Create: `layouts/home.html`, `content/_index.md`

- [ ] **Step 1: Write `content/_index.md`**

```markdown
---
title: Eldr Systems
eyebrow: Low-power cellular IoT · Budapest
heading: We build connected measurement devices, from circuit board to dashboard.
lead: Low-power cellular IoT and energy monitoring, engineered end to end by a small team in Budapest.
keepStat: "[X] µA"
keepCaption: average current in PSM on The Keep, our own NB-IoT hub.
---
```

- [ ] **Step 2: Write `layouts/_partials/sections/hero.html`**

```html
<section class="grid grid-cols-12 items-center gap-x-6 gap-y-12 px-gutter pt-8 pb-section">
  <div class="col-span-12 flex flex-col gap-8 lg:col-span-6">
    <span class="label-mono">{{ .Params.eyebrow }}</span>
    <h1 class="display-xl text-hero">{{ .Params.heading }}</h1>
    <p class="max-w-[34ch] text-lead leading-normal text-body">{{ .Params.lead }}</p>
    <div class="flex flex-wrap gap-3 pt-2">
      {{ partial "cta-link.html" (dict "url" .Site.Params.bookingUrl "text" "Book a 20-minute call" "class" "pill-ember") }}
      <a href="#offers" class="pill-outline">See our offers</a>
    </div>
  </div>
  <div class="col-span-12 flex justify-center lg:col-start-7 lg:col-span-6 lg:justify-end">
    <svg viewBox="0 0 600 600" class="w-full max-w-[600px] h-auto" role="img" aria-label="The Eldr mark, opened out into a signal">
      <path d="M388.9,544.4 A260,260 0 1 0 544.4,388.9" fill="none" stroke="#14161A" stroke-width="1.5" opacity="0.35"/>
      <path d="M373.5,502.0 A215,215 0 1 0 502.0,373.5" fill="none" stroke="#14161A" stroke-width="2" opacity="0.6"/>
      <path d="M358.1,459.7 A170,170 0 1 0 459.7,358.1" fill="none" stroke="#14161A" stroke-width="11"/>
      <circle cx="420.2" cy="420.2" r="30" fill="#E2632B"/>
      <circle cx="300" cy="300" r="13" fill="#14161A"/>
    </svg>
  </div>
</section>
```

- [ ] **Step 3: Write `layouts/_partials/sections/layers.html`**

```html
<section class="border-t-2 border-ink px-gutter py-section" id="layers">
  <h2 class="display-lg text-h2">Five layers. One team.</h2>
  <div class="mt-14 grid gap-x-6 gap-y-8 [grid-template-columns:repeat(auto-fit,minmax(180px,1fr))]">
    {{ range .Site.Data.layers }}
    <div class="flex flex-col gap-4">
      {{ partial "icon.html" (dict "name" .icon "class" "w-18 h-18") }}
      <span class="text-xl font-bold">{{ .name }}</span>
      <p class="text-[0.9375rem] leading-normal text-body">{{ .line }}</p>
    </div>
    {{ end }}
  </div>
</section>
```

- [ ] **Step 4: Write `layouts/_partials/sections/audience.html`**

```html
<section class="border-t-2 border-ink px-gutter py-section">
  <div class="grid grid-cols-12 gap-x-6 gap-y-10">
    <div class="col-span-12 flex flex-col gap-6 lg:col-span-5">
      <h2 class="display-lg text-h2">For teams that measure things in the field</h2>
      <p class="text-lg leading-[1.55] text-body">You need remote monitoring and have no electronics or firmware team of your own.</p>
    </div>
    <div class="col-span-12 lg:col-start-7 lg:col-span-6">
      <ul class="list-none m-0 p-0">
        {{ range .Site.Data.audience }}
        <li class="flex items-center justify-between gap-4 border-t border-rule py-5 text-[clamp(1.0625rem,0.85rem+0.9vw,1.375rem)] font-semibold first:border-t-2 first:border-t-ink last:border-b-2 last:border-b-ink">
          <span>{{ .text }}</span>
          <span class="shrink-0 rounded-full {{ if .ember }}w-3.5 h-3.5 bg-ember{{ else }}w-2.5 h-2.5 bg-ink{{ end }}" aria-hidden="true"></span>
        </li>
        {{ end }}
      </ul>
    </div>
  </div>
</section>
```

- [ ] **Step 5: Write `layouts/_partials/sections/offers.html`**

Reads from `content/offers/` so adding an offer is one Markdown file (Task 8).

```html
<section class="border-t-2 border-ink px-gutter py-section" id="offers">
  <h2 class="display-lg text-h2">Fixed price. Scoped in one call.</h2>
  <div class="mt-14 grid gap-6 [grid-template-columns:repeat(auto-fit,minmax(280px,1fr))]">
    {{ range (where .Site.RegularPages "Section" "offers").ByWeight }}
    <article class="flex flex-col gap-5 rounded-card border-2 border-ink p-9 {{ if .Params.emphasised }}bg-ink text-bone{{ end }}">
      {{ partial "icon.html" (dict "name" .Params.icon "class" "w-26 h-26") }}
      <span class="label-mono {{ if .Params.emphasised }}!text-muted-ink{{ end }}">{{ .Params.duration }}</span>
      <h3 class="display-md text-h3">{{ .Title }}</h3>
      <p class="grow text-base leading-[1.55] {{ if .Params.emphasised }}text-on-ink{{ else }}text-body{{ end }}">{{ .Params.summary }}</p>
      <div class="flex items-center justify-between gap-4 border-t pt-4 {{ if .Params.emphasised }}border-rule-dark{{ else }}border-rule{{ end }}">
        <span class="font-mono text-base font-medium">{{ .Params.price }}</span>
        <a href="{{ .RelPermalink }}">Details →</a>
      </div>
    </article>
    {{ end }}
  </div>
</section>
```

- [ ] **Step 6: Write `layouts/_partials/sections/keep.html`**

```html
<section class="border-t-2 border-ink px-gutter py-section" id="keep">
  <div class="grid grid-cols-12 items-center gap-x-6 gap-y-10">
    <div class="col-span-12 flex aspect-video items-center justify-center rounded-card bg-ink p-4 text-center font-mono text-sm text-rule lg:col-span-7 lg:aspect-auto lg:h-[380px]">
      [Demo video: The Keep by Eldr Systems, 2 min]
    </div>
    <div class="col-span-12 flex flex-col items-start gap-5 lg:col-start-9 lg:col-span-4">
      <svg viewBox="0 0 360 80" class="w-full max-w-[360px] h-auto" role="img" aria-label="Current trace with three transmit bursts">
        <polyline points="0,70 60,70 62,14 70,26 78,70 180,70 182,40 190,52 198,70 300,70 302,14 310,26 318,70 360,70" fill="none" stroke="#14161A" stroke-width="2"/>
        <circle cx="62" cy="14" r="5.5" fill="#E2632B"/>
      </svg>
      <span class="font-mono text-[clamp(2.5rem,1.7rem+3.3vw,3.375rem)] font-medium tracking-[-0.03em] leading-none">{{ .Params.keepStat }}</span>
      <p class="max-w-[38ch] text-base leading-normal text-body">{{ .Params.keepCaption }}</p>
      <a href="/notes/" class="text-[1.0625rem] font-bold">Read the notes →</a>
    </div>
  </div>
</section>
```

- [ ] **Step 7: Write `layouts/_partials/sections/cta.html`**

The ember tile appears here and nowhere else — `BRAND.md`: "Ember tile is the loud version. Used exactly once, at the closing CTA."

```html
<section class="flex flex-wrap items-center justify-between gap-12 border-t-2 border-ink px-gutter py-section">
  <div class="flex flex-[1_1_20rem] flex-col gap-7">
    <h2 class="display-cta text-cta">Tell us what you need to measure.</h2>
    <div class="flex flex-wrap items-center gap-5">
      {{ partial "cta-link.html" (dict "url" .Site.Params.bookingUrl "text" "Book a 20-minute call" "class" "pill-ink") }}
      <span class="text-[1.0625rem] text-body">
        No pitch.{{ with .Site.Params.email }} Or email <a href="mailto:{{ . }}">{{ . }}</a>.{{ end }}
      </span>
    </div>
  </div>
  <svg class="w-[clamp(120px,20vw,240px)] h-auto shrink-0" viewBox="0 0 512 512" role="img" aria-label="Eldr Systems mark">
    <rect width="512" height="512" rx="74.7" fill="#E2632B"/>
    <path fill="#14161A" d="M412.52 279.08A158.22 158.22 0 1 0 366.48 369.25L334.24 336.21A112.05 112.05 0 0 1 146.35 279.08ZM146.35 232.92A112.05 112.05 0 0 1 365.65 232.92Z"/>
    <circle cx="375.12" cy="319.8" r="23.08" fill="#F4F1EA"/>
  </svg>
</section>
```

- [ ] **Step 8: Write `layouts/home.html`**

Sections 6, 8, 9 and 10 are added in Task 9; placeholders in the composition order now.

```html
{{ define "main" }}
{{ partial "sections/hero.html" . }}
{{ partial "sections/layers.html" . }}
{{ partial "sections/audience.html" . }}
{{ partial "sections/offers.html" . }}
{{ partial "sections/keep.html" . }}
{{ partial "sections/cta.html" . }}
{{ end }}
```

- [ ] **Step 9: Verify and commit**

```bash
./scripts/check.sh
grep -c '<section' public/index.html
```

Expected: `PASS`, and 6 sections. Offers will be empty until Task 8.

```bash
git add -A && git commit -m "Port homepage sections from the kit"
```

---

## Task 8: Offers content and detail pages

**Files:**
- Create: `content/offers/_index.md` + three offer pages
- Create: `layouts/offers/single.html`, `layouts/offers/list.html`

- [ ] **Step 1: Write `content/offers/_index.md`**

```markdown
---
title: Offers
description: Fixed-price engagements for low-power connected measurement devices.
---

Fixed price. Scoped in one call.
```

- [ ] **Step 2: Write `content/offers/poc-sprint.md`**

```markdown
---
title: Proof-of-concept sprint
weight: 1
duration: 4–8 weeks
price: from €[6,000]
icon: device
summary: A working connected measurement device, with source code, a dashboard and a measured battery-life estimate.
---

## What you get

- A working device measuring what you need, on your bench or on a real site
- Full source code and schematics, yours to keep
- A simple dashboard showing live and historical data
- A measured battery-life estimate from a real power-profiler trace, not a datasheet calculation

## How it runs

Four to eight weeks, depending on how many quantities you need to measure and whether
the site has mains power. Weekly demos with working hardware.

## What we need from you

One technical contact, a description of what is being measured and where, and access to
a representative site if the connectivity is uncertain.
```

- [ ] **Step 3: Write `content/offers/battery-connectivity.md`**

`emphasised: true` renders the ink card — the one visually weighted offer.

```markdown
---
title: Battery and connectivity fixes
weight: 2
emphasised: true
duration: 1–2 weeks
price: from €[3,000]
icon: battery-low
summary: Power traces, modem logs and a ranked fix plan for NB-IoT and LTE-M devices that drain or drop off.
---

## What you get

- Power-profiler traces of your device across a full duty cycle
- Modem logs read against the operator's actual PSM and eDRX timers
- A ranked list of fixes, each with the current it saves and the work it costs

## Who this is for

Devices already in the field that flatten their batteries early, or drop off the network
and come back hours later. Usually the cause is PSM negotiated differently than the
firmware assumes, or a wake-up path nobody measured.

## What we need from you

Two or three sample devices, the firmware source if you have it, and the SIM operator.
```

- [ ] **Step 4: Write `content/offers/device-analytics.md`**

```markdown
---
title: Device data analytics
weight: 3
duration: 3–6 weeks
price: from €[3,500]
icon: anomaly
summary: Fault and anomaly detection on the data your inverters, chargers or heat pumps already send.
---

## What you get

- Fault and anomaly detection on your existing telemetry
- A written account of which faults are detectable in the data you already have, and which need more sensing
- Detection running against your live data, with alerts

## Who this is for

Fleets already sending data that nobody has time to read. The faults are usually visible
months before the failure — nobody is looking.

## What we need from you

A data export covering at least one period containing a known fault, and a description
of what that fault was.
```

- [ ] **Step 5: Write `layouts/offers/single.html`**

```html
{{ define "main" }}
<article class="border-t-2 border-ink px-gutter py-section">
  <div class="max-w-[68ch] flex flex-col gap-6">
    <span class="label-mono">{{ .Params.duration }} · {{ .Params.price }}</span>
    <h1 class="display-xl text-hero">{{ .Title }}</h1>
    <p class="text-lead leading-normal text-body">{{ .Params.summary }}</p>
    <div class="prose-eldr">{{ .Content }}</div>
    <div class="flex flex-wrap items-center gap-5 border-t border-rule pt-8">
      {{ partial "cta-link.html" (dict "url" .Site.Params.bookingUrl "text" "Book a 20-minute call" "class" "pill-ember") }}
      <a href="/#offers">All offers →</a>
    </div>
  </div>
</article>
{{ end }}
```

- [ ] **Step 6: Add `prose-eldr` to `assets/css/main.css`**

Hugo emits plain `<h2>`, `<ul>`, `<p>` from Markdown; these give them brand styling without a Tailwind plugin.

```css
@utility prose-eldr {
  & h2 {
    font-family: var(--font-display);
    font-weight: 800;
    font-stretch: 108%;
    letter-spacing: -0.02em;
    font-size: var(--text-h3);
    margin-top: 2.5rem;
    margin-bottom: 1rem;
  }
  & p { color: var(--color-body); line-height: 1.6; margin-bottom: 1rem; }
  & ul { list-style: none; padding: 0; margin: 0 0 1.5rem; }
  & li {
    position: relative;
    padding-left: 1.5rem;
    color: var(--color-body);
    line-height: 1.6;
    margin-bottom: 0.5rem;
  }
  & li::before {
    content: "";
    position: absolute;
    left: 0; top: 0.6em;
    width: 8px; height: 8px;
    border-radius: 999px;
    background: var(--color-ink);
  }
  & a { text-decoration: underline; text-underline-offset: 4px; }
}
```

- [ ] **Step 7: Write `layouts/offers/list.html`**

```html
{{ define "main" }}
<section class="border-t-2 border-ink px-gutter py-section">
  <h1 class="display-xl text-hero">{{ .Title }}</h1>
  <div class="mt-14 grid gap-6 [grid-template-columns:repeat(auto-fit,minmax(280px,1fr))]">
    {{ range .Pages.ByWeight }}
    <article class="flex flex-col gap-5 rounded-card border-2 border-ink p-9">
      <span class="label-mono">{{ .Params.duration }}</span>
      <h2 class="display-md text-h3">{{ .Title }}</h2>
      <p class="grow text-base leading-[1.55] text-body">{{ .Params.summary }}</p>
      <div class="flex items-center justify-between gap-4 border-t border-rule pt-4">
        <span class="font-mono text-base font-medium">{{ .Params.price }}</span>
        <a href="{{ .RelPermalink }}">Details →</a>
      </div>
    </article>
    {{ end }}
  </div>
</section>
{{ end }}
```

- [ ] **Step 8: Verify the offer cards and detail pages exist**

```bash
./scripts/check.sh
ls public/offers/
grep -c 'Details →' public/index.html
```

Expected: `PASS`; three directories under `public/offers/`; 3 "Details →" links on the homepage.

- [ ] **Step 9: Commit**

```bash
git add -A && git commit -m "Add offers content and detail pages"
```

---

## Task 9: The four missing brand sections

`BRAND.md` lists eleven sections; the kit's direction covers seven. These are the four.

**Files:**
- Create: `layouts/_partials/sections/{process,proof,team,where}.html`
- Modify: `layouts/home.html`

- [ ] **Step 1: Write `layouts/_partials/sections/process.html`**

```html
<section class="border-t-2 border-ink px-gutter py-section" id="how-we-work">
  <h2 class="display-lg text-h2">How we work</h2>
  <div class="mt-14 grid gap-x-6 gap-y-10 [grid-template-columns:repeat(auto-fit,minmax(220px,1fr))]">
    {{ range .Site.Data.process }}
    <div class="flex flex-col gap-4 border-t-2 border-ink pt-6">
      <span class="font-mono text-label text-muted">{{ .step }}</span>
      {{ partial "icon.html" (dict "name" .icon "class" "w-16 h-16") }}
      <span class="text-xl font-bold">{{ .name }}</span>
      <p class="text-[0.9375rem] leading-normal text-body">{{ .line }}</p>
    </div>
    {{ end }}
  </div>
</section>
```

- [ ] **Step 2: Write `layouts/_partials/sections/proof.html`**

Pulls the three newest notes, so the section fills itself as write-ups are published. Renders nothing at all when there are no notes — an empty "Proof" heading is worse than no section.

```html
{{ $notes := first 3 (where .Site.RegularPages "Section" "notes").ByDate.Reverse }}
{{ with $notes }}
<section class="border-t-2 border-ink px-gutter py-section" id="proof">
  <div class="flex items-baseline justify-between gap-4">
    <h2 class="display-lg text-h2">Proof</h2>
    <a href="/notes/" class="label-mono">All notes →</a>
  </div>
  <div class="mt-14 grid gap-x-6 gap-y-10 [grid-template-columns:repeat(auto-fit,minmax(260px,1fr))]">
    {{ range . }}
    <article class="flex flex-col gap-3 border-t-2 border-ink pt-6">
      <span class="label-mono">{{ .Date.Format "2006-01-02" }}</span>
      <h3 class="display-md text-h3"><a href="{{ .RelPermalink }}">{{ .Title }}</a></h3>
      <p class="text-[0.9375rem] leading-normal text-body">{{ .Params.summary | default .Summary }}</p>
    </article>
    {{ end }}
  </div>
</section>
{{ end }}
```

- [ ] **Step 3: Write `layouts/_partials/sections/team.html`**

```html
<section class="border-t-2 border-ink px-gutter py-section" id="team">
  <div class="flex flex-col gap-6 max-w-[44ch]">
    <h2 class="display-lg text-h2">Three engineers in Budapest</h2>
    <p class="text-lg leading-[1.55] text-body">You talk to the people who build it. There is no account manager.</p>
  </div>
  <div class="mt-14 grid gap-x-6 gap-y-10 [grid-template-columns:repeat(auto-fit,minmax(240px,1fr))]">
    {{ range .Site.Data.team }}
    <div class="flex flex-col gap-4">
      <img src="{{ .photo }}" alt="" width="240" height="300" class="w-full rounded-card border-2 border-ink" loading="lazy">
      <div class="flex flex-col gap-1">
        <span class="text-xl font-bold">{{ .name }}</span>
        <span class="label-mono">{{ .role }} · {{ .title }}</span>
      </div>
    </div>
    {{ end }}
  </div>
</section>
```

The `title` values read `roleA` / `roleB` / `roleC` on purpose. They are visibly wrong so they cannot ship unnoticed; `scripts/check.sh` flags them in Task 11.

- [ ] **Step 4: Write `layouts/_partials/sections/where.html`**

```html
<section class="border-t-2 border-ink px-gutter py-section" id="where">
  <div class="grid grid-cols-12 gap-x-6 gap-y-8">
    <div class="col-span-12 lg:col-span-5">
      <h2 class="display-lg text-h2">Where and how</h2>
    </div>
    <dl class="col-span-12 grid gap-0 font-mono text-label lg:col-start-7 lg:col-span-6">
      <div class="flex justify-between gap-4 border-t-2 border-ink py-4">
        <dt class="text-muted">Based in</dt><dd>Budapest, Hungary</dd>
      </div>
      <div class="flex justify-between gap-4 border-t border-rule py-4">
        <dt class="text-muted">We work</dt><dd>EU-wide, remote and on site</dd>
      </div>
      <div class="flex justify-between gap-4 border-t border-rule py-4">
        <dt class="text-muted">Hours</dt><dd>CET / CEST</dd>
      </div>
      <div class="flex justify-between gap-4 border-t border-rule py-4">
        <dt class="text-muted">Languages</dt><dd>English, Hungarian</dd>
      </div>
      <div class="flex justify-between gap-4 border-t border-rule border-b-2 border-b-ink py-4">
        <dt class="text-muted">Contracts</dt><dd>English</dd>
      </div>
    </dl>
  </div>
</section>
```

- [ ] **Step 5: Compose the full eleven-section homepage**

Replace `layouts/home.html`:

```html
{{ define "main" }}
{{ partial "sections/hero.html" . }}
{{ partial "sections/layers.html" . }}
{{ partial "sections/audience.html" . }}
{{ partial "sections/offers.html" . }}
{{ partial "sections/process.html" . }}
{{ partial "sections/keep.html" . }}
{{ partial "sections/proof.html" . }}
{{ partial "sections/team.html" . }}
{{ partial "sections/where.html" . }}
{{ partial "sections/cta.html" . }}
{{ end }}
```

- [ ] **Step 6: Verify all sections render and nav anchors resolve**

```bash
./scripts/check.sh
for id in layers offers how-we-work keep team where; do
  grep -q "id=\"$id\"" public/index.html && echo "ok   #$id" || echo "FAIL #$id"
done
```

Expected: `PASS`, and every anchor found. `#proof` is absent until Task 10 adds a note — that is correct behaviour.

- [ ] **Step 7: Commit**

```bash
git add -A && git commit -m "Add how-we-work, proof, team and where sections"
```

---

## Task 10: Notes collection

**Files:**
- Create: `content/notes/_index.md`, `content/notes/psm-edrx-field-notes.md`
- Create: `layouts/notes/list.html`, `layouts/notes/single.html`

- [ ] **Step 1: Write `content/notes/_index.md`**

```markdown
---
title: Notes
description: Technical write-ups on low-power cellular IoT, from the bench and from the field.
---

Technical write-ups from the bench and from the field. No marketing.
```

- [ ] **Step 2: Write the first note**

Real, specific and defensible — the kit's voice rule is numbers over adjectives, and this must not read as filler.

```markdown
---
title: What PSM actually negotiates, and why your battery estimate is wrong
date: 2026-09-18
summary: The T3412 and T3324 timers your device asks for are a request, not a setting. The operator decides. Here is how to find out what you actually got.
---

## The request is not the answer

A device asking for a 24-hour TAU period and a 2-second active timer will often be
granted something else entirely. The attach request carries the requested values; the
accept carries what the network decided. Firmware that logs the request and not the
accept produces a battery estimate built on a number that was never true.

Read the granted values back after attach rather than trusting the request.

## Where the current actually goes

On a device transmitting a small payload hourly, the transmit burst is rarely the
problem. The recurring costs are the active timer window after each exchange, and any
wake-up path nobody measured — a sensor held in a higher power mode than intended, or a
regulator that never reaches its own low-power state.

A power profiler across one full duty cycle settles this in an afternoon. A datasheet
calculation does not.

## What to measure before quoting a battery life

- One complete duty cycle, from wake through transmit to the next wake
- Current during the active window after the exchange, not only during transmit
- Sleep current with every peripheral in its intended state
- The same measurement on a real network, not only against a base-station simulator

Numbers from a lab bench and numbers from a real operator's network differ, and the
difference is usually in the timers.
```

- [ ] **Step 3: Write `layouts/notes/list.html`**

```html
{{ define "main" }}
<section class="border-t-2 border-ink px-gutter py-section">
  <div class="max-w-[44ch] flex flex-col gap-6">
    <h1 class="display-xl text-hero">{{ .Title }}</h1>
    <div class="text-lead leading-normal text-body">{{ .Content }}</div>
  </div>
  <div class="mt-14 flex flex-col">
    {{ range .Pages.ByDate.Reverse }}
    <article class="flex flex-col gap-3 border-t-2 border-ink py-8">
      <span class="label-mono">{{ .Date.Format "2006-01-02" }}</span>
      <h2 class="display-md text-h3"><a href="{{ .RelPermalink }}">{{ .Title }}</a></h2>
      <p class="max-w-[68ch] text-base leading-[1.55] text-body">{{ .Params.summary | default .Summary }}</p>
    </article>
    {{ else }}
    <p class="label-mono">No notes published yet.</p>
    {{ end }}
  </div>
</section>
{{ end }}
```

- [ ] **Step 4: Write `layouts/notes/single.html`**

```html
{{ define "main" }}
<article class="border-t-2 border-ink px-gutter py-section">
  <div class="max-w-[68ch] flex flex-col gap-6">
    <span class="label-mono">{{ .Date.Format "2006-01-02" }} · {{ .ReadingTime }} min read</span>
    <h1 class="display-xl text-hero">{{ .Title }}</h1>
    {{ with .Params.summary }}<p class="text-lead leading-normal text-body">{{ . }}</p>{{ end }}
    <div class="prose-eldr">{{ .Content }}</div>
    <div class="flex flex-wrap items-center gap-5 border-t border-rule pt-8">
      {{ partial "cta-link.html" (dict "url" .Site.Params.bookingUrl "text" "Book a 20-minute call" "class" "pill-ember") }}
      <a href="/notes/">All notes →</a>
    </div>
  </div>
</article>
{{ end }}
```

- [ ] **Step 5: Verify notes render and Proof now appears**

```bash
./scripts/check.sh
ls public/notes/
grep -q 'id="proof"' public/index.html && echo "ok   proof section now renders"
```

Expected: `PASS`; `public/notes/` contains the index and the post; the Proof section now appears on the homepage.

- [ ] **Step 6: Commit**

```bash
git add -A && git commit -m "Add notes collection with first write-up"
```

---

## Task 11: Privacy, company details, 404, and the placeholder audit

**Files:**
- Create: `content/privacy.md`, `content/company.md`, `layouts/404.html`, `layouts/page.html`
- Modify: `scripts/check.sh`

- [ ] **Step 1: Write `layouts/page.html`**

```html
{{ define "main" }}
<article class="border-t-2 border-ink px-gutter py-section">
  <div class="max-w-[68ch] flex flex-col gap-6">
    <h1 class="display-xl text-hero">{{ .Title }}</h1>
    <div class="prose-eldr">{{ .Content }}</div>
  </div>
</article>
{{ end }}
```

- [ ] **Step 2: Write `content/privacy.md`**

Honest because the site genuinely has no analytics and no third-party requests — Tasks 2 and 12 enforce that.

```markdown
---
title: Privacy
---

## What we collect on this website

Nothing. This site sets no cookies, runs no analytics, embeds no third-party scripts and
loads its fonts from its own server. There is no tracking to opt out of.

Our host, GitHub Pages, records server logs including IP addresses for security and
abuse prevention. We do not have access to them.

## If you email us or book a call

We keep what you send us so we can reply and, if it goes further, so we can quote the
work. We do not sell it, and we do not add you to a mailing list.

## Your rights

Under the GDPR you may ask what we hold about you, ask for it to be corrected, or ask
for it to be deleted. Write to us and we will answer.

## Changes

If this page changes materially, the change will be visible in this site's public git
history at [github.com/eldr-systems](https://github.com/eldr-systems).
```

- [ ] **Step 3: Write `content/company.md`**

```markdown
---
title: Company details
---

Eldr Systems Kft. is a company registered in Hungary.

Registration details are published here once the company registration completes.

Contact and correspondence: Budapest, Hungary.
```

- [ ] **Step 4: Write `layouts/404.html`**

```html
{{ define "main" }}
<section class="border-t-2 border-ink px-gutter py-section flex flex-col items-start gap-8">
  <img src="/graphics/404.svg" alt="" width="360" height="240" class="max-w-[360px]">
  <h1 class="display-xl text-hero">That page is not here.</h1>
  <p class="max-w-[44ch] text-lead leading-normal text-body">The link may be old, or we may have moved something. The homepage is a good place to restart.</p>
  <a href="/" class="pill-ember">Back to the homepage</a>
</section>
{{ end }}
```

- [ ] **Step 5: Extend `scripts/check.sh` with the placeholder audit**

Insert before the `page weight` block:

```bash
echo "==> unfilled placeholders (warnings, not failures)"
placeholders=0
check_param() {
  if ! grep -q "$2" public/index.html 2>/dev/null; then
    warn "$1 is not set"; placeholders=$((placeholders + 1))
  fi
}
grep -rq 'roleA\|roleB\|roleC' public/ && { warn "team titles still roleA/roleB/roleC"; placeholders=$((placeholders+1)); }
grep -rq '€\[' public/ && { warn "prices still bracketed"; placeholders=$((placeholders+1)); }
grep -rq '\[X\] µA' public/ && { warn "The Keep current figure not measured"; placeholders=$((placeholders+1)); }
grep -rq 'Demo video:' public/ && { warn "demo video not embedded"; placeholders=$((placeholders+1)); }
grep -rq 'aria-disabled="true"' public/ && { warn "$(grep -roc 'aria-disabled="true"' public/index.html) disabled CTA(s) — booking/social URLs unset"; placeholders=$((placeholders+1)); }
grep -rq 'Reg. no. —' public/ && { warn "Kft. registration details not filled"; placeholders=$((placeholders+1)); }
grep -rq 'portrait-placeholder' public/ && { warn "team photos still placeholders"; placeholders=$((placeholders+1)); }
[ "$placeholders" -eq 0 ] && ok "no unfilled placeholders" || echo "        $placeholders placeholder group(s) outstanding — not blocking, but not launch-ready"
```

These are warnings, not failures: the site must be buildable and deployable while these
are outstanding. The point is that they cannot be forgotten.

- [ ] **Step 6: Verify**

```bash
./scripts/check.sh
```

Expected: `PASS`, with a list of outstanding placeholder warnings — including team titles, prices, the µA figure and the disabled booking CTA.

- [ ] **Step 7: Commit**

```bash
git add -A && git commit -m "Add privacy, company and 404 pages, plus placeholder audit"
```

---

## Task 12: Guarantee zero third-party requests and measure the page

The footer says "No cookies." `BRAND.md`: that line "only stays honest if the builder you pick doesn't quietly add its own."

**Files:**
- Modify: `scripts/check.sh`, `layouts/_partials/footer.html`

- [ ] **Step 1: Add the third-party request assertion**

```bash
echo "==> third-party requests"
ext=$(grep -rhoE '(src|href)="https?://[^"]+"' public/ \
  | grep -vE 'eldrsystems\.com|github\.com|linkedin\.com|youtube\.com|schema\.org|w3\.org' \
  | sort -u)
if [ -n "$ext" ]; then
  echo "$ext" | sed 's/^/        /'
  bad "external asset requests found — 'No cookies.' is no longer honest"
else
  ok "no external asset requests"
fi
```

`github.com`, `linkedin.com` and `youtube.com` are excluded because they are footer
destination links the visitor chooses to follow, not assets the browser fetches.

- [ ] **Step 2: Make the footer kB figure real**

The kit lists `[X] kB` as "measure the built page". Rather than hardcode a number that
goes stale, drop it — a wrong number is worse than none. Confirm the footer reads
`No cookies.` with no size claim (already the case from Task 5, Step 4).

- [ ] **Step 3: Verify and record the real page weight**

```bash
./scripts/check.sh
echo "total page weight including CSS and fonts:"
du -ch public/index.html public/css/*.css public/fonts/*.woff2 | tail -1
```

Expected: `PASS` with `no external asset requests`, and a total under roughly 150 kB.

- [ ] **Step 4: Commit**

```bash
git add -A && git commit -m "Assert zero third-party asset requests"
```

---

## Task 13: GitHub Actions deployment

**Files:**
- Create: `.github/workflows/deploy.yml`, `static/CNAME`

- [ ] **Step 1: Write `static/CNAME`**

```
eldrsystems.com
```

- [ ] **Step 2: Write `.github/workflows/deploy.yml`**

The Hugo version is pinned to match `mise.toml` so CI and local builds cannot diverge.

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

env:
  HUGO_VERSION: 0.166.0

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Install Hugo
        run: |
          curl -sSL -o hugo.deb \
            https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-amd64.deb
          sudo dpkg -i hugo.deb

      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: npm

      - run: npm ci

      - uses: actions/configure-pages@v5
        id: pages

      - name: Build
        env:
          HUGO_ENVIRONMENT: production
          TZ: Europe/Budapest
        run: hugo --gc --minify --baseURL "${{ steps.pages.outputs.base_url }}/"

      - name: Verify build output
        run: ./scripts/check.sh

      - uses: actions/upload-pages-artifact@v3
        with:
          path: ./public

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

- [ ] **Step 3: Verify the workflow parses**

```bash
python3 -c "import yaml,sys; yaml.safe_load(open('.github/workflows/deploy.yml')); print('workflow YAML valid')"
```

Expected: `workflow YAML valid`. If it errors, there is a stray character in the file — fix it before pushing.

- [ ] **Step 4: Commit**

```bash
git add -A && git commit -m "Add GitHub Pages deployment workflow"
```

- [ ] **Step 5: STOP — hand off to the user**

Do not push yet. Pushing triggers a deploy to a Pages site that is not configured, which
fails noisily. The user must first set **Settings → Pages → Source: GitHub Actions**.
Ask them to do it, then push.

---

## Task 14: README and final review

**Files:**
- Create: `README.md`

- [ ] **Step 1: Write `README.md`**

````markdown
# eldrsystems.com

The Eldr Systems website. Hugo + Tailwind v4, deployed to GitHub Pages.

## Running it locally

```bash
mise install       # installs the pinned Hugo
npm install        # installs Tailwind
hugo server        # http://localhost:1313
```

## Checking a change

```bash
./scripts/check.sh
```

Builds the site and asserts: no broken placeholder links, no third-party asset requests,
the Archivo width axis survives, fonts are served locally. It also lists which
placeholders are still unfilled. Run it before pushing.

## Editing content

| To change | Edit |
|---|---|
| Homepage headline, lead, The Keep figure | `content/_index.md` |
| An offer, or add a new one | `content/offers/*.md` |
| Publish a note | `content/notes/*.md` — new file, set `date` |
| The five layers, audience list, process steps, team | `data/*.yaml` |
| Booking link, email, social links, company details | `hugo.toml` under `[params]` |

Adding an offer file makes it appear on the homepage *and* generates its detail page.
Adding a note makes it appear in the Proof section on the homepage.

## Brand rules that the code cannot enforce

- **One ember element per component, never two.** Ember is rationed; that is why the
  design holds together.
- **The ember logo tile appears exactly once**, at the closing CTA.
- Display type needs its width axis (`font-stretch: 112%`), not just weight. Use the
  `display-*` utilities rather than writing type styles by hand.
- Numbers over adjectives. Banned: revolutionary, cutting-edge, next-generation,
  game-changing, seamless, world-class, leverage as a verb.

See `eldr-systems-kit/BRAND.md` for the full rules.

## Still to do before launch

Run `./scripts/check.sh` — the warnings are the list. Currently: booking link, prices,
The Keep's µA figure, the demo video, team titles and photos, Kft. registration details,
LinkedIn and YouTube, and real photography to replace the placeholder graphics.
````

- [ ] **Step 2: Commit the kit as the source of record**

```bash
git add -A eldr-systems-kit README.md
git commit -m "Add README and commit the design kit"
```

- [ ] **Step 3: Final full verification**

```bash
rm -rf public resources && ./scripts/check.sh && hugo --gc --minify --quiet && find public -name '*.html' | wc -l
```

Expected: `PASS` from a completely clean build; roughly 10–12 HTML files.

---

## Self-review notes

**Spec coverage:** Toolchain → Task 1. Fonts → Task 2. Brand invariants → Task 3. Repo
layout → Tasks 1, 4. Content model → Tasks 6, 8, 10. Routes → Tasks 7–11 (`/hu/` is
config-only in Task 1, correct per spec). Eleven homepage sections → Tasks 7, 9. Nav
fixes → Task 5. Known values → Task 6. Placeholder discipline → Tasks 5, 11. Deployment
→ Task 13. Non-goals respected: no JS, no CMS, no dark mode, no search.

**Known gaps deferred on purpose:** `/hu/` content, real photography, and the
`og-image` as PNG rather than SVG (some scrapers reject SVG OG images — worth revisiting
once a real photo exists to render it from).
