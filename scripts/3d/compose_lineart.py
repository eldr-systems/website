#!/usr/bin/env python3
# scripts/3d/compose_lineart.py LINEART_DIR OUT.svg
#
# Option A, the page half: stacks render_lineart.py's parts into one SVG. Each
# part is a <g> holding a bone fill (its silhouette, traced with potrace, so parts
# in front hide parts behind) and its ink linework, drawn in the exploded pose.
# --tx/--ty on each <g> is the way back to the closed pose; the CSS animates from
# there to 0, so with no animation the drawing rests exploded. A part with a
# waypoint (the sensor, which must clear the case wall) also carries --mx/--my,
# where it stops on the way, and data-legs="2" so the CSS gives it a two-leg path.
import json, os, re, subprocess, sys, tempfile

src, out = sys.argv[1], sys.argv[2]
meta = json.load(open(os.path.join(src, "parts.json")))
W, H = meta["width"], meta["height"]
PAD = 16

def silhouette(name):
    with tempfile.TemporaryDirectory() as tmp:
        pgm = os.path.join(tmp, "m.pgm")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i",
                        os.path.join(src, name + ".png"), "-pix_fmt", "gray", pgm], check=True)
        # -i: the part is white on black.
        svg = subprocess.run(["potrace", "-i", "-s", "--flat", "-t", "8", "-O", "1",
                              "-o", "-", pgm], check=True, capture_output=True, text=True).stdout
    transform = re.search(r'<g transform="([^"]+)"', svg).group(1)
    d = " ".join(" ".join(re.findall(r'<path d="([^"]+)"', svg)).split())
    # Colours as attributes, not only CSS: the clipped <use> copy of the base
    # doesn't reliably pick up page styles and would fall back to black fills.
    return f'<path class="fill" fill="#F4F1EA" transform="{transform}" d="{d}"/>'

parts, bounds = {}, []
for name, (tx, ty) in meta["travel"].items():
    data = json.load(open(os.path.join(src, name + ".json")))
    lines = [l for l in data["lines"] if len(l) > 1]
    d = "".join("M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in l) for l in lines)
    parts[name] = (tx, ty, silhouette(name),
                   f'<path class="lines" fill="none" stroke="#14161A" stroke-linecap="round" '
                   f'stroke-linejoin="round" stroke-width="{data["width"]}" d="{d}"/>')
    pts = [p for l in lines for p in l]
    for dx, dy in ((0, 0), (-tx, -ty)):  # exploded and closed poses
        bounds.append((min(x for x, _ in pts) + dx, min(y for _, y in pts) + dy,
                       max(x for x, _ in pts) + dx, max(y for _, y in pts) + dy))

x0 = min(b[0] for b in bounds) - PAD
y0 = min(b[1] for b in bounds) - PAD
vw = max(b[2] for b in bounds) + PAD - x0
vh = max(b[3] for b in bounds) + PAD - y0

def group(name, body):
    tx, ty = parts[name][:2]
    style, legs = f"--tx:{-tx}px;--ty:{-ty}px", ""
    for wx, wy in meta.get("waypoints", {}).get(name, [])[:1]:
        # Translations are relative to the exploded drawing.
        style += f";--mx:{round(wx - tx, 1)}px;--my:{round(wy - ty, 1)}px"
        legs = ' data-legs="2"'
    return f'<g class="part" data-part="{name}"{legs} style="{style}">{body}</g>'

# The base's walls without its open top: the whole frame, minus the opening.
opening = "M" + "L".join(f"{x} {y}" for x, y in meta["opening"]) + "Z"
front_clip = (f'<clipPath id="keep-base-front"><path clip-rule="evenodd" '
              f'd="M{x0} {y0}h{vw}v{vh}h{-vw}Z{opening}"/></clipPath>')

_, _, base_fill, base_lines = parts["case-base"]
body = "".join([
    # Back to front. The board and sensor sit inside the base: drawn over its
    # back, under its front walls, so they show through the opening and sink
    # behind the walls. The lid closes over everything.
    group("case-base", f'<g id="keep-base">{base_fill}{base_lines}</g>'),
    group("lilygo", "".join(parts["lilygo"][2:])),
    group("sensor", "".join(parts["sensor"][2:])),
    group("case-base", '<use href="#keep-base" clip-path="url(#keep-base-front)"/>'),
    group("case-top", "".join(parts["case-top"][2:])),
])

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.0f} {y0:.0f} {vw:.0f} {vh:.0f}" '
       f'class="keep-burst" role="img" aria-label="Exploded drawing of The Keep: the lid '
       f'lifted off the case, the LilyGO T-SIM7000G board raised out of the base, and the '
       f'AHT20 and BMP280 sensor board drawn out beside them.">'
       f'<defs>{front_clip}</defs>{body}</svg>\n')
open(out, "w").write(svg)
print(f"{out}: {len(svg) / 1024:.0f} kB, viewBox {vw:.0f} x {vh:.0f}")
