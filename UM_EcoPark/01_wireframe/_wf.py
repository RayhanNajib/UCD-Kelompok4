"""Wireframe helper - low fidelity SVG builder for UM EcoPark.

Deliberately grayscale-only: low fidelity must not carry colour decisions.
Palette and typography enter at the medium-fidelity stage via DESIGN.md tokens.
"""
import os

OUT = r"C:\AI AGENT\UM_EcoPark\01_wireframe"

G = {
    "bg": "#ffffff", "line": "#1a1a1a", "mid": "#8a8a8a", "light": "#d4d4d4",
    "fill": "#f4f4f4", "fill2": "#e6e6e6", "text": "#1a1a1a", "muted": "#6b6b6b",
}

W, H = 375, 812
PAD = 20
FONT = "Inter, 'Segoe UI', Arial, sans-serif"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def T(x, y, s, size=12, weight="400", anchor="start", fill=None):
    fill = fill or G["text"]
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{esc(s)}</text>')


def box(x, y, w, h, label="", sub="", fs=11, fill=None, rx=6):
    fill = fill or G["fill"]
    o = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
         f'fill="{fill}" stroke="{G["line"]}" stroke-width="1.5"/>']
    if label:
        cy = y + h / 2 + (-2 if sub else 4)
        o.append(T(x + w / 2, cy, label, fs, "600", "middle", G["line"]))
    if sub:
        o.append(T(x + w / 2, cy + 15, sub, 9, "400", "middle", G["muted"]))
    return "\n".join(o)


def bar(x, y, w, h=12, fill=None):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2:.1f}" '
            f'fill="{fill or G["light"]}"/>')


def rect(x, y, w, h, fill=None, stroke=None, sw=1.5, rx=6, dash=False):
    stroke = stroke if stroke is not None else G["line"]
    d = ' stroke-dasharray="5 4"' if dash else ''
    f = fill if fill is not None else "none"
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{f}" stroke="{stroke}" stroke-width="{sw}"{d}/>')


def hairline(x1, y1, x2, y2, dash=False, stroke=None):
    d = ' stroke-dasharray="4 3"' if dash else ''
    s = stroke or G["mid"]
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{s}" stroke-width="1"{d}/>'


def txt_block(x, y, w, lines, lh=15, size=11.5, fill=None):
    o = []
    for i, ln in enumerate(lines):
        o.append(T(x, y + i * lh, ln, size, "400", "start", fill or G["muted"]))
    return "\n".join(o)


def screen(title, no, body, footnote="", total=7):
    h = H + (46 if footnote else 0)
    o = [f'<rect x="0" y="0" width="{W}" height="{h}" fill="{G["bg"]}"/>',
         T(PAD, 26, "09:41", 11, "600"),
         T(W - PAD, 26, "LTE   100%", 10, "400", "end", G["muted"]),
         hairline(0, 38, W, 38),
         T(PAD, 66, title, 17, "700"),
         T(W - PAD, 66, f"{no}/{total}", 11, "400", "end", G["muted"]),
         hairline(0, 78, W, 78)]
    o.append(f'<g transform="translate(0,78)">{body}</g>')
    if footnote:
        fy = h - 30
        o.append(hairline(0, fy - 14, W, fy - 14, dash=True))
        o.append(T(PAD, fy, footnote, 9.5, "400", "start", G["muted"]))
    o.append(rect(0, 0, W, h, stroke=G["mid"], sw=1, rx=0))
    head = ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
            'viewBox="0 0 %d %d">' % (W, h, W, h))
    return head + "\n".join(o) + "\n</svg>\n"


def write(fn, svg):
    p = os.path.join(OUT, fn)
    with open(p, "w", encoding="utf-8") as f:
        f.write(svg)
    return p, os.path.getsize(p)


def write_all_boards(boards, wrap_w=None):
    """boards: list of (filename, svg). Also emits one contact sheet HTML."""
    made = []
    for fn, svg in boards:
        made.append(write(fn, svg))
    return made
