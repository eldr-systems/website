#!/usr/bin/env bash
# Build-output assertions for the Eldr Systems site.
set -uo pipefail
cd "$(dirname "$0")/.."

fail=0
ok()   { printf '  ok    %s\n' "$1"; }
bad()  { printf '  FAIL  %s\n' "$1"; fail=1; }
warn() { printf '  warn  %s\n' "$1"; }

echo "==> build"
# --cleanDestinationDir: without it, fingerprinted CSS from earlier builds
# piles up in public/ and every size measurement below is wrong.
if ! hugo --gc --minify --cleanDestinationDir --quiet; then
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

echo "==> static assets published"
# Declaring any module.mount targeting 'static' replaces Hugo's default
# static mount. When that happened, CNAME silently stopped shipping and
# the custom domain would have broken on deploy.
for f in CNAME robots.txt logo/favicon.svg graphics/og-image.png; do
  if [ -f "public/$f" ]; then ok "$f"; else bad "$f missing from public/"; fi
done
# Every <img src> on the homepage must resolve to a real file.
broken=""
for src in $(grep -rhoE 'src="/[^"]+"' public/index.html 2>/dev/null | sed 's/src="//;s/"//' | sort -u); do
  [ -f "public$src" ] || broken="$broken $src"
done
if [ -n "$broken" ]; then bad "img src with no file:$broken"; else ok "all homepage img src resolve"; fi

echo "==> brand typography"
if grep -rq 'font-stretch' public/css/ 2>/dev/null; then
  ok "Archivo width axis present in CSS"
else
  bad "font-stretch missing — the Archivo width axis was lost"
fi

echo "==> homepage nav anchors resolve"
# The kit shipped #work, #notes and #team pointing at the wrong elements.
# #audit replaced #how-we-work: the two-week spine IS the process section now.
missing=""
for id in audit offers layers keep team where; do
  grep -q "id=$id\|id=\"$id\"" public/index.html 2>/dev/null || missing="$missing #$id"
done
if [ -n "$missing" ]; then
  bad "nav anchors with no target:$missing"
else
  ok "all homepage section anchors resolve"
fi

echo "==> third-party requests"
# The footer claims "No cookies. No analytics. No third-party requests."
# BRAND.md: that line "only stays honest if the builder you pick doesn't
# quietly add its own." This is what keeps it honest.
# Destination links the visitor chooses to follow are not asset requests.
ext=$(grep -rhoE '(src|href)="https?://[^"]+"' public/ 2>/dev/null \
  | grep -vE 'eldrsystems\.com|github\.com|linkedin\.com|youtube\.com|schema\.org|w3\.org' \
  | sort -u)
if [ -n "$ext" ]; then
  echo "$ext" | sed 's/^/        /'
  bad "external asset requests found — the footer claim is no longer true"
else
  ok "no external asset requests"
fi

echo "==> unfilled placeholders"
# Warnings, not failures: the site must stay buildable and deployable while
# these are outstanding. The point is that they cannot be quietly forgotten.
# Note: --minify strips attribute quotes, so match aria-disabled bare.
n=0
flag() { warn "$1"; n=$((n + 1)); }
grep -rq 'roleA\|roleB\|roleC'  public/ && flag "team titles still roleA/roleB/roleC"
grep -rq '€\['                  public/ && flag "offer prices still bracketed"
grep -rq '\[X\] µA'             public/ && flag "The Keep current figure not measured"
grep -rq 'Demo video:'          public/ && flag "The Keep demo video not embedded"
n_out=$(grep -ro '\[[a-z ]*outstanding\]' public/ | wc -l)
[ "$n_out" -gt 0 ] && flag "$n_out Keep view artefact(s) outstanding"
grep -rq 'portrait-placeholder' public/ && flag "team photos still placeholders"
grep -rq 'Reg. no. —'           public/ && flag "Kft. registration details not filled"
d=$(grep -rho 'aria-disabled' public/index.html 2>/dev/null | wc -l)
[ "$d" -gt 0 ] && flag "$d disabled CTA(s) on the homepage — booking/social URLs unset"
if [ "$n" -eq 0 ]; then
  ok "no unfilled placeholders"
else
  echo "        $n outstanding — buildable, but not launch-ready"
fi

echo "==> page weight"
if [ -f public/index.html ]; then
  html=$(wc -c < public/index.html)
  css=$(cat public/css/*.css 2>/dev/null | wc -c)
  fonts=$(cat public/fonts/*.woff2 2>/dev/null | wc -c)
  # GitHub Pages serves gzip, so the compressed figure is what travels.
  gz=$(( $(gzip -9c public/index.html | wc -c) + $(cat public/css/*.css | gzip -9c | wc -c) ))
  ok "render-blocking, gzipped: $((gz / 1024)) kB (raw $(( (html + css) / 1024 )) kB)"
  # Fonts use font-display:swap, so they never block first paint.
  ok "fonts, streamed after paint then cached: $((fonts / 1024)) kB"
fi

echo
[ "$fail" -eq 0 ] && echo "PASS" || echo "FAILED"
exit $fail
