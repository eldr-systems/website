import os, sys
d = sys.argv[1]
kb = lambda f: round(os.path.getsize(os.path.join(d, f)) / 1024) if os.path.exists(os.path.join(d, f)) else "?"
html = open(os.path.join(d, "template.html")).read()
for k, v in {"%%SVG%%": open(os.path.join(d, "keep-burst.svg")).read(), "%%SVG_KB%%": kb("keep-burst.svg"),
             "%%WEBM_KB%%": kb("keep-burst.webm"), "%%MP4_KB%%": kb("keep-burst.mp4")}.items():
    html = html.replace(k, str(v))
open(os.path.join(d, "index.html"), "w").write(html)
