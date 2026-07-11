"""
Build two separate dark-terminal SVG cards (each 428px wide):
  achievements-card.svg  →  🏆 Achievements
  work-exp-card.svg      →  💼 Work Experience

Display them side-by-side in the README (same row as portrait + neofetch).

    python scripts/make_achievements_card.py
    STATIC=1 python scripts/make_achievements_card.py   # frozen preview
"""
import html
import os

HERE   = os.path.dirname(os.path.abspath(__file__))
OUT_A  = os.path.join(HERE, "..", "achievements-card.svg")
OUT_W  = os.path.join(HERE, "..", "work-exp-card.svg")
STATIC = bool(os.environ.get("STATIC"))

W      = 428
PAD    = 20
TITLEBAR_H = 30

BG    = "#0d1117"
BG2   = "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
INK   = "#c9d1d9"
ACCENT= "#58a6ff"
GREEN = "#3fb950"
GOLD  = "#f2cc60"
CYAN  = "#22d3ee"

ACH_H  = 34   # height per achievement (title + subtitle)
WORK_H = 50   # height per job (company/role + stack + breathing room)
SEC_H  = 26   # section header

# ===========================================================================
#  EDIT THIS
# ===========================================================================
ACHIEVEMENTS = [
    ("🥇", "1st — HACKaMINeD 2026, Tribastion",  "AI-powered PII platform · 400+ teams"),
    ("🥇", "1st — BREACH 2026 Fintech Hackathon", "AI travel SaaS · 730+ registrations"),
    ("🚀", "Top 15 — NASA Space Apps 2024",        "Global 48-hour hackathon"),
    ("✅", "Cleared SIH Internal Round",            "Smart India Hackathon"),
    ("💡", "Codeforces Rating 905",                 "150+ problems solved"),
    ("💡", "LeetCode Rating 1470",                  "150+ problems solved"),
    ("🎓", "Scholarship Holder · CGPA 8.31",        "B.Tech CSE, Nirma University"),
]

WORK = [
    ("CheckMyWarranty", "SWE Intern",               "May 2026 – Jun 2026",
     "React Native · TypeScript · Supabase · ML Kit · Groq LLaMA"),
    ("Inslyt",          "Software Engineer Intern",  "Jul 2025 – Sep 2025",
     "TypeScript · React · Docker · Jira · Bitbucket CI/CD"),
    ("Clezid",          "Front-End Developer Intern","Mar 2025 – May 2025",
     "React · JavaScript · Tailwind CSS · production real estate platform"),
]
# ===========================================================================


def esc(s):
    return html.escape(s)


def rise(inner, i):
    if STATIC:
        return f"<g>{inner}</g>"
    delay = 0.10 + i * 0.07
    return (
        f'<g opacity="0" transform="translate(0,5)">{inner}'
        f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.35s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" '
        f'begin="{delay:.2f}s" dur="0.35s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/></g>'
    )


def card_shell(H, grad_id, title_text):
    """Return the opening SVG + chrome elements as a list of strings."""
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" overflow="hidden" '
        f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
        f'<defs><linearGradient id="{grad_id}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
        f'</linearGradient></defs>',
        f'<rect width="{W}" height="{H}" rx="12" fill="url(#{grad_id})"/>',
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
        f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
    ]
    for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
    parts.append(
        f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="11" '
        f'text-anchor="middle">{esc(title_text)}</text>'
    )
    return parts


# ── Card 1: Achievements ────────────────────────────────────────────────────
ach_content_h = SEC_H + len(ACHIEVEMENTS) * ACH_H
ach_H = TITLEBAR_H + PAD + ach_content_h + PAD

parts_a = card_shell(ach_H, "abg", "vruxak@github: ~$ cat achievements.md")

y = TITLEBAR_H + PAD
parts_a.append(rise(
    f'<text x="{PAD}" y="{y:.1f}" fill="{ACCENT}" font-size="12.5" font-weight="700">&#8212; Achievements</text>',
    0
))
y += SEC_H

for ai, (emoji, title, sub) in enumerate(ACHIEVEMENTS):
    title_y = y + ACH_H * 0.42
    sub_y   = y + ACH_H * 0.82
    inner = (
        f'<text x="{PAD}" y="{title_y:.1f}" font-size="12.5">'
        f'<tspan>{esc(emoji)}</tspan>'
        f'  <tspan fill="{INK}" font-weight="600">{esc(title)}</tspan></text>'
        f'<text x="{PAD + 22}" y="{sub_y:.1f}" fill="{MUTED}" font-size="10.5">{esc(sub)}</text>'
    )
    parts_a.append(rise(inner, ai + 1))
    y += ACH_H

parts_a.append("</svg>")
svg_a = "".join(parts_a)
with open(OUT_A, "w") as f:
    f.write(svg_a)
print(f"wrote {OUT_A} ({len(svg_a)} bytes); {W} x {ach_H}")


# ── Card 2: Work Experience ─────────────────────────────────────────────────
work_content_h = SEC_H + len(WORK) * WORK_H
work_H = ach_H  # force same height as achievements card for visual symmetry

parts_w = card_shell(work_H, "wbg", "vruxak@github: ~$ cat work-exp.md")

y = TITLEBAR_H + PAD
parts_w.append(rise(
    f'<text x="{PAD}" y="{y:.1f}" fill="{ACCENT}" font-size="12.5" font-weight="700">&#8212; Work Experience</text>',
    0
))
y += SEC_H

for wi, (company, role, period, stack) in enumerate(WORK):
    row1_y = y + WORK_H * 0.28
    row2_y = y + WORK_H * 0.56
    per_y  = row1_y

    inner = (
        f'<text x="{PAD}" y="{row1_y:.1f}" font-size="12.5" font-weight="700">'
        f'<tspan fill="{GREEN}">{esc(company)}</tspan>'
        f'  <tspan fill="{MUTED}" font-size="11" font-weight="400">· {esc(role)}</tspan></text>'
        f'<text x="{W - PAD}" y="{per_y:.1f}" fill="{MUTED}" font-size="10" text-anchor="end">{esc(period)}</text>'
        f'<text x="{PAD}" y="{row2_y:.1f}" fill="{CYAN}" font-size="10" '
        f'textLength="{W - PAD*2}" lengthAdjust="spacing">{esc(stack)}</text>'
    )
    parts_w.append(rise(inner, wi + 1))

    if wi < len(WORK) - 1:
        sep_y = y + WORK_H - 6
        parts_w.append(
            f'<line x1="{PAD}" y1="{sep_y:.1f}" x2="{W - PAD}" y2="{sep_y:.1f}" '
            f'stroke="{FRAME}" stroke-opacity="0.4"/>'
        )
    y += WORK_H

parts_w.append("</svg>")
svg_w = "".join(parts_w)
with open(OUT_W, "w") as f:
    f.write(svg_w)
print(f"wrote {OUT_W} ({len(svg_w)} bytes); {W} x {work_H}")
