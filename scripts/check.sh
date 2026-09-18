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

echo "==> page weight"
if [ -f public/index.html ]; then
  bytes=$(wc -c < public/index.html)
  ok "index.html $((bytes / 1024)) kB ($bytes bytes)"
fi

echo
[ "$fail" -eq 0 ] && echo "PASS" || echo "FAILED"
exit $fail
