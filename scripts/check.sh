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

echo "==> brand typography"
if grep -rq 'font-stretch' public/css/ 2>/dev/null; then
  ok "Archivo width axis present in CSS"
else
  bad "font-stretch missing — the Archivo width axis was lost"
fi

echo "==> homepage nav anchors resolve"
# The kit shipped #work, #notes and #team pointing at the wrong elements.
missing=""
for id in layers offers how-we-work keep team where; do
  grep -q "id=$id\|id=\"$id\"" public/index.html 2>/dev/null || missing="$missing #$id"
done
if [ -n "$missing" ]; then
  bad "nav anchors with no target:$missing"
else
  ok "all homepage section anchors resolve"
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
  bytes=$(wc -c < public/index.html)
  ok "index.html $((bytes / 1024)) kB ($bytes bytes)"
fi

echo
[ "$fail" -eq 0 ] && echo "PASS" || echo "FAILED"
exit $fail
