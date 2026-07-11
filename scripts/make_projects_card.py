"""
Build a dark-terminal projects card SVG (860px wide) to sit below the
portrait/info-card row.  Each project renders as two lines:
  Line 1: project name (accent blue) + tag (gold) + stack (cyan-ish muted)
  Line 2: one-sentence description (light gray)

Same chrome and stagger animation as the other cards.

    python scripts/make_projects_card.py   →  projects-card.svg
    STATIC=1 python ...                    →  frozen frame for preview
"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "..", "projects-card.svg")
STATIC = bool(os.environ.get("STATIC"))

W  = 860
PAD = 24
TITLEBAR_H = 30

BG    = "#0d1117"
BG2   = "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
INK   = "#c9d1d9"
ACCENT= "#58a6ff"
CYAN  = "#79c0ff"
GREEN = "#3fb950"
GOLD  = "#f2cc60"

LINE1_H = 21   # name + stack
LINE2_H = 18   # description
ROW_H   = LINE1_H + LINE2_H   # 39 per project
GAP_H   = 10   # gap between projects

# ===========================================================================
#  EDIT THIS — your featured projects
#  (name, tag, stack, one-line-description)
# ===========================================================================
PROJECTS = [
    ("PII Shield",
     "🏆 Winner",
     "Next.js · FastAPI · PostgreSQL · BERT · spaCy",
     "3-layer AI detection · 16 Indian PII categories · AES-256-GCM · DPDPA 2023 compliant"),

    ("Auto-Complete Search Tool",
     "",
     "React · Node.js · Express · MongoDB · D3.js",
     "Trie + Max Heap · sub-100ms over 10K+ entries · Levenshtein typo correction"),

    ("TradeFlow",
     "AI / ML",
     "Flutter · Python · TensorFlow · Firebase",
     "LSTM stock prediction 85%+ directional accuracy · Alpha Vantage & GNews pipeline"),

    ("CareVox",
     "",
     "Next.js · TypeScript · OpenRouter",
     "Real-time AI voice agent · symptom triage · specialist recommendation · clinical reports"),

    ("CodeZap",
     "",
     "React · Node.js",
     "AI-powered full-stack app generator from natural language prompts"),

    ("Frame2Flow",
     "",
     "Next.js · TypeScript",
     "Wireframe-to-code converter powered by vision language models"),
]
# ===========================================================================

n = len(PROJECTS)
content_h = n * ROW_H + (n - 1) * GAP_H
H = TITLEBAR_H + PAD + content_h + PAD


def esc(s):
    return html.escape(s)


def rise(inner, i):
    """Fade + slight upward slide, staggered; freezes visible."""
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
    f'<linearGradient id="pbg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
    '</linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#pbg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]
for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
parts.append(
    f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" text-anchor="middle">'
    f'vruxak@github: ~/projects $ ls -la</text>'
)

y = TITLEBAR_H + PAD
for pi, (name, tag, stack, desc) in enumerate(PROJECTS):
    # thin separator between projects (skip before first)
    if pi > 0:
        sep_y = y - GAP_H / 2
        parts.append(
            f'<line x1="{PAD}" y1="{sep_y:.1f}" x2="{W - PAD}" y2="{sep_y:.1f}" '
            f'stroke="{FRAME}" stroke-opacity="0.45"/>'
        )

    # Line 1: ▸ name [tag] · stack
    line1_y = y + LINE1_H * 0.80
    line1  = (f'<text x="{PAD}" y="{line1_y:.1f}" font-size="13">'
              f'<tspan fill="{MUTED}">▸ </tspan>'
              f'<tspan fill="{ACCENT}" font-weight="700">{esc(name)}</tspan>')
    if tag:
        line1 += f'<tspan fill="{GOLD}" font-size="10.5" font-weight="400">  [{esc(tag)}]</tspan>'
    line1 += f'<tspan fill="{MUTED}" font-size="11" font-weight="400">  ·  {esc(stack)}</tspan></text>'

    # Line 2: description (slightly indented)
    line2_y = y + LINE1_H + LINE2_H * 0.82
    line2 = (f'<text x="{PAD + 16}" y="{line2_y:.1f}" fill="{INK}" font-size="11.5">'
             f'{esc(desc)}</text>')

    parts.append(rise(line1 + line2, pi))

    y += ROW_H
    if pi < n - 1:
        y += GAP_H

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print(f"wrote {OUT} ({len(svg)} bytes); {W} x {H}")
