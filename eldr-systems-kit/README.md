# Eldr Systems — website kit

Everything from the design work, in formats a website builder can actually take.
Built from the approved direction **G · Graphic, built on the mark**, with the **inverse** logo as the primary lockup.

---

## What's in here

```
README.md                      this file
BRAND.md                       brand rules, cut down to what a builder needs

page/index.html                the whole homepage, responsive, one file, no build step
copy/homepage-copy.md          every string on the page + the placeholder checklist

tokens/tokens.css              CSS custom properties — paste into global CSS
tokens/tokens.json             for Figma Tokens Studio or a theme config
tokens/tailwind.tokens.js      for theme.extend

logo/eldr-mark-inverse.svg     ← primary
logo/eldr-mark-primary.svg     the original
logo/eldr-mark-ember.svg       loud version, closing CTA only
logo/eldr-mark-mono-*.svg      one-colour, for stamps and single-colour print
logo/eldr-mark-transparent.svg no tile, for placing on photos
logo/eldr-lockup-*.svg         mark + wordmark
logo/favicon.svg

icons/                         32 icons, 64 px, 2 px stroke
icons/_sprite.svg              all 32 as <symbol>s — one request, then <use href="#eldr-solar">
icons/contact-sheet.html       open in a browser to see them all
icons/_index.json              names and labels

graphics/                      9 section graphics + 12 patterns and placeholders,
                               including og-image-1200x630 and linkedin-banner-1128x282
```

Icons use `var(--eldr-ink)` and `var(--eldr-ember)`, so they follow `tokens.css` when inlined. Loaded as `<img src>` they fall back to the correct hex values.

---

## How to get this into a builder

**The short answer: don't, yet.** `page/index.html` is a finished, responsive, dependency-free page. Dragging that folder onto Cloudflare Pages or Netlify puts eldrsystems.com live this afternoon, free, at about 30 kB, with no cookie banner. Rebuilding it inside a builder is a week of work to arrive at the same page, slower and with a monthly bill.

The three of you can edit HTML. The website is not the bottleneck — the first three client conversations are.

**When a builder does earn its place:** when Sobi or Boldi need to add a case study without touching a repo, or when you're running 15+ pages in two languages. That's the 12–18 month version of this site, not the 30-day one. At that point the honest options are:

- **Webflow** — the only mainstream builder that won't fight this design. Custom CSS, HTML embeds, real CMS for case studies and notes. Check its cookie behaviour against your "No cookies." footer line.
- **Framer** — faster to learn, less exact. The variable-width Archivo headings are the thing most likely to drift.
- **Astro + Cloudflare Pages** — if it's going to be code anyway, this is the one that grows into a case-study site cleanly. Markdown in, static HTML out.

Avoid Squarespace, Wix and WordPress here. All three will quietly re-style the type and add cookies.

**If you do go into a builder,** the order that wastes the least time:

1. Paste `tokens/tokens.css` into the global custom CSS. Everything downstream depends on it.
2. Load the two fonts. In Webflow that's a custom code embed with the Google Fonts link from the top of `index.html`.
3. Upload `logo/` and `icons/` to the asset library. Use `eldr-mark-inverse.svg` as the header logo and `favicon.svg` as the favicon.
4. Build sections as HTML embeds, copying each `<section>` from `index.html` one at a time. Don't rebuild them from native blocks — the grid behaviour and the type settings are the design.
5. Fill in the placeholders from `copy/homepage-copy.md`.

---

## Things to know before you hand this to anyone

- **The lockup SVGs use live text**, so they need Archivo installed to render correctly. Fine on the web where the font loads; wrong in a PDF or on someone else's machine. Before the capability sheet and the business cards, have the designer convert the wordmark to outlines. The mark files have no text and are safe everywhere.
- **Prices are bracketed placeholders.** Whether to show "from €" at all is still open in the brand file. Showing them filters out tyre-kickers and costs you the occasional larger job.
- **Four sections from the brand file aren't in this direction:** How we work, Team, Proof, Where and how. Graphics exist for the first two. The Team section matters — for a three-person firm the team is the product.
- **Every graphic is a placeholder standing in for a photo you haven't taken.** They look intentional, which is a trap: it's easy to ship the site and never replace them. The bench photo and one real power-profiler trace are worth an afternoon.
- **Archivo vs IBM Plex Sans** is an open contradiction between this design and the brand file. Resolve it before the capability sheet, or the PDF and the website won't match.
