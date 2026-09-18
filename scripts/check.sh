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
