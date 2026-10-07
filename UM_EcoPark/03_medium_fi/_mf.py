"""Medium-fidelity builder for UM EcoPark.

Reads DESIGN.md token values (exported to tokens.json by the design-md CLI) and
paints the same seven screens the low-fidelity pass defined. No layout decision
changes here: only colour, type, and component styling move.
"""
import json
import os

BRAND = r"C:\AI AGENT\UM_EcoPark\02_brand"
OUT = r"C:\AI AGENT\UM_EcoPark\03_medium_fi"

with open(os.path.join(BRAND, "tokens.json"), encoding="utf-8") as f:
    TOK = json.load(f)

C = {k: v["$value"]["hex"] for k, v in TOK["color"].items()
    if not k.startswith("$") and isinstance(v, dict) and "hex" in v["$value"]}
R = {k: int(v["$value"]["value"]) for k, v in TOK["rounded"].items() if not k.startswith("$")}
S = {k: int(v["$value"]["value"]) for k, v in TOK["spacing"].items() if not k.startswith("$")}

FONT = "Inter, 'Segoe UI', Roboto, Arial, sans-serif"
W, H = 375, 812
PAD = 16


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def T(x, y, s, size=14, weight="400", anchor="start", fill=None, ls=None, tabular=False):
    fill = fill or C["text-primary"]
    extra = f' letter-spacing="{ls}"' if ls else ""
    extra += ' style="font-variant-numeric:tabular-nums"' if tabular else ""
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{extra}>'
            f'{esc(s)}</text>')


def rect(x, y, w, h, fill="none", stroke=None, sw=1, rx=8, dash=False):
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    d = ' stroke-dasharray="5 4"' if dash else ""
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{fill}"{s}{d}/>')


def circle(x, y, r, fill, stroke=None):
    s = f' stroke="{stroke}" stroke-width="1.5"' if stroke else ""
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"{s}/>'


def shadow(x, y, w, h, rx, fill, lvl=0):
    s = ""
    if lvl == 1:
        s = ' filter="url(#l1)"'
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{s}/>'


def pill(x, y, w, h, text, bg, fg, size=11):
    return (rect(x, y, w, h, bg, None, 0, h / 2)
            + T(x + w / 2, y + h / 2 + size * 0.35, text, size, "600", "middle", fg))


def button(x, y, w, h, text, kind="primary"):
    md = R["md"]
    if kind == "primary":
        return (rect(x, y, w, h, C["primary"], None, 0, md)
                + T(x + w / 2, y + h / 2 + 5, text, 15, "600", "middle", "#ffffff"))
    if kind == "accent":
        return (rect(x, y, w, h, C["accent"], None, 0, 12)
                + T(x + w / 2, y + h / 2 + 5, text, 15, "700", "middle", C["text-primary"]))
    if kind == "secondary":
        return (rect(x, y, w, h, C["surface"], C["primary"], 1.5, 12)
                + T(x + w / 2, y + h / 2 + 5, text, 15, "600", "middle", C["text-primary"]))
    return ""


def card(x, y, w, h, rx=12):
    return rect(x, y, w, h, C["surface"], C["border"], 1, rx)


def status_chip(x, y, state):
    m = {"available": (C["status-available"], "Tersedia", "#ffffff", 76),
         "limited": (C["status-limited"], "Terbatas", C["text-primary"], 74),
         "full": (C["status-full"], "Penuh", "#ffffff", 62)}
    bg, label, fg, w = m[state]
    return pill(x, y, w, 24, label, bg, fg, 11)


def slot_tile(x, y, w, h, num, state):
    bg = {"available": C["status-available"], "limited": C["status-limited"],
          "full": C["status-full"]}[state]
    fg = C["text-primary"] if state == "limited" else "#ffffff"
    return (rect(x, y, w, h, bg, None, 0, 8)
            + T(x + w / 2, y + h / 2 + 4, num, 11, "700", "middle", fg, tabular=True))


def screen(title, no, body, footnote="", total=7):
    h = H + (44 if footnote else 0)
    o = [rect(0, 0, W, h, C["neutral"], None, 0, 0),
         T(PAD, 24, "09:41", 12, "600"),
         T(W - PAD, 24, "LTE  100%", 11, "600", "end", C["text-secondary"]),
         rect(PAD, 42, W - 2 * PAD, 44, C["surface"], None, 0, 12),
         T(PAD + 14, 69, title, 16, "700", "start", C["text-primary"]),
         T(W - PAD - 14, 69, f"{no}/{total}", 11, "500", "end", C["text-secondary"]),
         f'<g transform="translate(0,98)">{body}</g>']
    if footnote:
        fy = h - 26
        o.append(rect(0, fy - 20, W, 1, C["border"], None, 0, 0))
        o.append(T(PAD, fy, footnote, 10, "400", "start", C["text-secondary"]))
    defs = ('<defs><filter id="l1" x="-20%" y="-20%" width="140%" height="140%">'
            '<feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="#141a16" '
            'flood-opacity="0.12"/></filter></defs>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" '
            f'viewBox="0 0 {W} {h}">{defs}\n' + "\n".join(o) + "\n</svg>\n")


def write(fn, svg):
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, fn)
    with open(p, "w", encoding="utf-8") as f:
        f.write(svg)
    return p, os.path.getsize(p)
