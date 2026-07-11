"""
Build a dark-terminal achievements + work-experience card SVG (860px wide)
in a two-column layout:
  LEFT  (PAD … COL_MID-8):  🏆 Achievements + CP ratings
  RIGHT (COL_MID+8 … W-PAD): 💼 Work Experience timeline

Same chrome and stagger animation as the other cards.

    python scripts/make_achievements_card.py   →  achievements-card.svg
    STATIC=1 python ...                         →  frozen frame for preview
"""
import html
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(HERE, "..", "achievements-card.svg")
STATIC = bool(os.environ.get("STATIC"))

W  = 860
PAD = 24
TITLEBAR_H = 30
COL_MID = W // 2   # 430  — divider x position

BG    = "#0d1117"
BG2   = "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
INK   = "#c9d1d9"
ACCENT= "#58a6ff"
GREEN = "#3fb950"
GOLD  = "#f2cc60"
CYAN  = "#22d3ee"

ACH_H  = 34   # height per achievement (2-line: title + subtitle)
WORK_H = 46   # height per job (2-line: company+role + stack + divider space)
SEC_H  = 26   # section header height

# ===========================================================================
#  EDIT THIS
# ===========================================================================
ACHIEVEMENTS = [
    ("🥇", "1st — HACKaMINeD 2026, Tribastion",   "AI-powered PII platform · 400+ teams"),
    ("🥇", "1st — BREACH 2026 Fintech Hackathon",  "AI travel SaaS · 730+ registrations"),
    ("🚀", "Top 15 — NASA Space Apps 2024",         "Global 48-hour hackathon"),
    ("✅", "Cleared SIH Internal Round",             "Smart India Hackathon"),
    ("💡", "Codeforces Rating 905",                  "150+ problems solved"),
    ("💡", "LeetCode Rating 1470",                   "150+ problems solved"),
    ("🎓", "Scholarship Holder · CGPA 8.31",         "B.Tech CSE, Nirma University"),
]

WORK = [
    ("CheckMyWarranty",    "SWE Intern",               "May 2026 – Jun 2026",
     "React Native · TypeScript · Supabase · ML Kit · Groq LLaMA"),
    ("Inslyt",             "Software Engineer Intern",  "Jul 2025 – Sep 2025",
     "TypeScript · React · Docker · Jira · Bitbucket CI/CD"),
    ("Clezid",             "Front-End Developer Intern","Mar 2025 – May 2025",
     "React · JavaScript · Tailwind CSS · production real estate platform"),
]
# ===========================================================================

# Heights for each column
left_h  = SEC_H + len(ACHIEVEMENTS) * ACH_H
right_h = SEC_H + len(WORK) * WORK_H
content_h = max(left_h, right_h)
H = TITLEBAR_H + PAD + content_h + PAD


def esc(s):
    return html.escape(s)


def rise(inner, i, col="l"):
    """Fade + upward slide per-item; left col uses normal stagger, right col offset."""
    if STATIC:
        return f"<g>{inner}</g>"
    base = 0.10 if col == "l" else 0.14
    delay = base + i * 0.07
    return (
        f'<g opacity="0" transform="translate(0,5)">{inner}'
        f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.35s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" from="0 5" to="0 0" '
        f'begin="{delay:.2f}s" dur="0.35s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/></g>'
    )


parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'overflow="hidden" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<defs>'
    f'<linearGradient id="acbg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/>'
    '</linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#acbg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]
for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
parts.append(
    f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" text-anchor="middle">'
    f'vruxak@github: ~$ cat achievements.md</text>'
)

# Vertical divider
dv_y1 = TITLEBAR_H + PAD * 0.4
dv_y2 = H - PAD * 0.4
parts.append(
    f'<line x1="{COL_MID}" y1="{dv_y1:.1f}" x2="{COL_MID}" y2="{dv_y2:.1f}" '
    f'stroke="{FRAME}" stroke-opacity="0.55"/>'
)

# ── LEFT COLUMN: Achievements ──────────────────────────────────────────────
col_l = PAD
y_l = TITLEBAR_H + PAD

# section header
sec_l = (f'<text x="{col_l}" y="{y_l:.1f}" fill="{ACCENT}" font-size="12.5" font-weight="700">'
         f'&#8212; Achievements</text>')
parts.append(rise(sec_l, 0, "l"))
y_l += SEC_H

for ai, (emoji, title, sub) in enumerate(ACHIEVEMENTS):
    title_y = y_l + ACH_H * 0.42
    sub_y   = y_l + ACH_H * 0.82
    inner = (
        f'<text x="{col_l}" y="{title_y:.1f}" font-size="12.5">'
        f'<tspan>{esc(emoji)}</tspan>'
        f'  <tspan fill="{INK}" font-weight="600">{esc(title)}</tspan></text>'
        f'<text x="{col_l + 22}" y="{sub_y:.1f}" fill="{MUTED}" font-size="10.5">{esc(sub)}</text>'
    )
    parts.append(rise(inner, ai + 1, "l"))
    y_l += ACH_H

# ── RIGHT COLUMN: Work Experience ─────────────────────────────────────────
col_r = COL_MID + PAD
y_r = TITLEBAR_H + PAD

# section header
sec_r = (f'<text x="{col_r}" y="{y_r:.1f}" fill="{ACCENT}" font-size="12.5" font-weight="700">'
         f'&#8212; Work Experience</text>')
parts.append(rise(sec_r, 0, "r"))
y_r += SEC_H

for wi, (company, role, period, stack) in enumerate(WORK):
    row1_y = y_r + WORK_H * 0.30
    row2_y = y_r + WORK_H * 0.62

    inner = (
        # company + role (bold green) + period (muted, right-aligned)
        f'<text x="{col_r}" y="{row1_y:.1f}" font-size="12.5" font-weight="700">'
        f'<tspan fill="{GREEN}">{esc(company)}</tspan>'
        f'  <tspan fill="{MUTED}" font-size="11" font-weight="400">· {esc(role)}</tspan></text>'
        f'<text x="{W - PAD}" y="{row1_y:.1f}" fill="{MUTED}" font-size="10" text-anchor="end">'
        f'{esc(period)}</text>'
        # stack (cyan)
        f'<text x="{col_r}" y="{row2_y:.1f}" fill="{CYAN}" font-size="10.5">{esc(stack)}</text>'
    )
    parts.append(rise(inner, wi + 1, "r"))

    # separator between jobs
    if wi < len(WORK) - 1:
        sep_y = y_r + WORK_H - 4
        parts.append(
            f'<line x1="{col_r}" y1="{sep_y:.1f}" x2="{W - PAD}" y2="{sep_y:.1f}" '
            f'stroke="{FRAME}" stroke-opacity="0.35"/>'
        )
    y_r += WORK_H

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print(f"wrote {OUT} ({len(svg)} bytes); {W} x {H}")
