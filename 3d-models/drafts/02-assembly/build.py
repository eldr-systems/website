#!/usr/bin/env python3
# Builds index.html from template.html, inlining keep-flipbook.svg: the scroll
# timeline only reaches an SVG that is part of the page.
import gzip, os, re
d = os.path.dirname(os.path.abspath(__file__))
svg = open(os.path.join(d, "keep-flipbook.svg")).read()
html = open(os.path.join(d, "template.html")).read()
for k, v in {"%%FLIPBOOK%%": svg, "%%FRAMES%%": len(re.findall(r'<g class="f', svg)),
             "%%KB%%": round(len(svg) / 1024), "%%GZ%%": round(len(gzip.compress(svg.encode(), 9)) / 1024)}.items():
    html = html.replace(k, str(v))
open(os.path.join(d, "index.html"), "w").write(html)
