"""
Build a dark-terminal header card SVG (860px wide)
Contains the Name and Tagline.

    python scripts/make_header_card.py   →  header-card.svg
    STATIC=1 python ...                  →  frozen frame for preview
"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "..", "header-card.svg")
STATIC = bool(os.environ.get("STATIC"))

W  = 860
H  = 120
PAD = 24
TITLEBAR_H = 30

BG    = "#0d1117"
BG2   = "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
INK   = "#c9d1d9"
ACCENT= "#58a6ff"
GREEN = "#3fb950"

def esc(s):
    return html.escape(s)

def rise(inner, i):
    if STATIC:
        return f"<g>{inner}</g>"
    delay = 0.10 + i * 0.08
    return (
        f'<g opacity="0" transform="translate(0,6)">{inner}'
        f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.35s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" from="0 6" to="0 0" '
        f'begin="{delay:.2f}s" dur="0.35s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/></g>'
    )

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'overflow="hidden" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<defs>'
    f'<linearGradient id="hbg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
    '</linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#hbg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]

for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')

parts.append(
    f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" text-anchor="middle">'
    f'vruxak@github: ~$ whoami &amp;&amp; cat tagline.txt</text>'
)

y = TITLEBAR_H + PAD

# Name
name_line = (f'<text x="{PAD}" y="{y + 16}" font-size="22" font-weight="700" fill="{ACCENT}">'
             f'Vruxak Patel</text>')
parts.append(rise(name_line, 0))

# Tagline
tagline_line = (f'<text x="{PAD}" y="{y + 44}" font-size="13" fill="{INK}">'
                f'GDG Organizer · AI/ML &amp; Full Stack Developer · Scholarship Holder</text>')
parts.append(rise(tagline_line, 1))

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print(f"wrote {OUT} ({len(svg)} bytes); {W} x {H}")
