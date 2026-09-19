# Eldr Systems — brand rules for the build

Short version of the brand file, cut down to what someone building the website needs.

---

## Name

Written **Eldr Systems**. Capital E, rest lowercase. Never "ELDR", never "EldrSystems".
Wordmark is lowercase **eldr** with **systems** set smaller in mono.
Handles: `eldrsystems` everywhere. Domain: eldrsystems.com.

"The Keep by Eldr Systems" in public, always with the endorsement. On this site The Keep is our own product and test bed, not a separate business.

## Colour

| Token | Hex | Rule |
|---|---|---|
| Ink | `#14161A` | Text, dark surfaces, every icon stroke |
| Bone | `#F4F1EA` | Page background |
| Ember | `#E2632B` | Accent. **One ember element per icon or component, never two.** |
| Slate | `#5B6B7A` | Data and diagrams only |

Supporting greys are in `tokens/tokens.css`. Don't add colours: the whole design holds together because ember is rationed.

## Type

- **Archivo** (variable, width 62–125, weight 400–900) — headings and body
- **IBM Plex Mono** (400, 500) — labels, numbers, specs, footer

Display type uses width and tight tracking, not just weight: `font-stretch: 112%`, `letter-spacing: -0.03em`, weight 800. Losing the width axis is the fastest way to make this look like a generic template.

Both fonts must render Hungarian **ő** and **ű**. Archivo and IBM Plex Mono both do — check anyway if you swap either.

> Open decision: the brand file says IBM Plex Sans, this design uses Archivo. Pick one and update the other document.

## Logo

- **Primary use on the site: the inverse mark** — bone tile, ink glyph, ember dot. On a bone background the tile disappears and only the mark reads.
- Original (ink tile, bone glyph, ember dot) where it needs to sit against a light photo or a busy area, and in the footer.
- Ember tile (`logo/eldr-mark-ember.svg`) is the loud version. Not used on the site — the closing CTA carries the ember on its button instead.
- Tile corner radius is 74.7 on a 512 box — 14.6%. Keep it when resizing.
- Never a flame anywhere near The Keep. Never runes.

## Voice

1. Numbers over adjectives. "8 years on two AA cells", not "ultra-efficient".
2. Name the technology: NB-IoT, LTE-M, PSM, eDRX, OTA.
3. Plain English, short sentences — many readers are Swedish, Danish or German engineers reading in a second language.
4. Show experience through specifics, not years.
5. Be clear about scope, price and process.

**Banned:** revolutionary, cutting-edge, next-generation, game-changing, AI-powered solutions, synergy, seamless, world-class, leverage (as a verb).

## Imagery

Real photos only: our PCBs, power-profiler traces, a device in a real distribution box, the three of us at the bench. No stock smart-city glow, no AI brains or robots, no runes.

Until real photos exist, use the SVGs in `graphics/`. They are placeholders that look deliberate, which buys time — but they are still placeholders.

## Analytics and cookies

Cookieless (Plausible or similar), so no cookie banner. The footer line "No cookies." only stays honest if the builder you pick doesn't quietly add its own. Check this before launch — several page builders inject cookies by default.
