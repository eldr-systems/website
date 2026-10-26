#!/usr/bin/env python3
# scripts/3d/compose_flipbook.py STROKES.json OUT.svg [REST_FRAME]
#
# Option A, scroll-driven: render_assembly.py's "strokes" frames as one SVG
# flipbook. Each frame is a <g class="f"> holding one path; the CSS (see
# FLIPBOOK_CSS below, which the page includes) shows exactly one of them for each
# slice of a scroll timeline, so scrolling down assembles The Keep and scrolling
# up takes it apart. REST_FRAME (the Blender frame nearest it, default 122) is
# the one shown without the animation: reduced motion, or no scroll timelines.
import json, sys

src, out = sys.argv[1], sys.argv[2]
rest_at = int(sys.argv[3]) if len(sys.argv) > 3 else 122
data = json.load(open(src))
W, H, frames = data["width"], data["height"], data["frames"]

TOLERANCE = 0.7  # px at 1440 wide: points closer than this to the line are dropped

def simplify(pts):
    """Ramer–Douglas–Peucker, iterative."""
    if len(pts) < 3:
        return pts
    keep = [False] * len(pts)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        a, b = stack.pop()
        (ax, ay), (bx, by) = pts[a], pts[b]
        dx, dy = bx - ax, by - ay
        norm = (dx * dx + dy * dy) ** 0.5
        far, idx = 0, None
        for i in range(a + 1, b):
            px, py = pts[i]
            # A closed stroke ends where it starts: measure from that point
            # instead of a zero-length line, or the whole loop collapses.
            d = (abs(dy * (px - ax) - dx * (py - ay)) / norm if norm
                 else ((px - ax) ** 2 + (py - ay) ** 2) ** 0.5)
            if d > far:
                far, idx = d, i
        if idx is not None and far > TOLERANCE:
            keep[idx] = True
            stack += [(a, idx), (idx, b)]
    return [p for p, k in zip(pts, keep) if k]

def path(strokes):
    """Relative coordinates: shorter numbers, and gzip loves the repetition."""
    d, cx, cy = [], 0, 0
    for stroke in strokes:
        pts = simplify(stroke)
        x, y = pts[0]
        d.append(f"m{x - cx} {y - cy}")
        for nx, ny in pts[1:]:
            d.append(f"{nx - x} {ny - y}")
            x, y = nx, ny
        cx, cy = x, y
    # "m" then bare pairs: SVG reads the pairs after an m as relative line-tos.
    return " ".join(d).replace(" -", "-")

rest = min(range(len(frames)), key=lambda i: abs(frames[i]["frame"] - rest_at))
n = len(frames)
groups = []
for i, fr in enumerate(frames):
    # Each frame owns an equal slice of the scroll range, as percentages the CSS
    # maps onto it.
    cls = "f rest" if i == rest else "f"
    groups.append(f'<g class="{cls}" style="--from:{100 * i / n:.2f}%;--to:{100 * (i + 1) / n:.2f}%">'
                  f'<path d="M0 0{path(fr["strokes"])}"/></g>')

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" class="keep-flipbook" '
       f'role="img" aria-label="Line drawing of The Keep assembling: the LilyGO T-SIM7000G board '
       f'flips over and drops into the case, the AHT20 and BMP280 sensor stands up into its '
       f'chamber, and the lid closes." fill="none" stroke="#14161A" stroke-width="1.3" '
       f'stroke-linecap="round" stroke-linejoin="round">'
       + "".join(groups) + "</svg>\n")
open(out, "w").write(svg)
print(f"{out}: {n} frames, {len(svg) / 1024:.0f} kB")
