"""Generate the UM Copark low-fidelity wireframes as SVG + a single HTML sheet.

One layout table drives both outputs, so the HTML and the Figma-importable SVG
can never drift apart. Wireframes stay grayscale on purpose: no colour until the
information architecture is agreed.

Run:  python build_wireframe_assets.py
Out:  04_figma/wireframes.html   - view / print / share
      04_figma/wireframes.svg    - drag straight into Figma
      04_figma/wf_<screen>.svg   - one file per screen
"""

from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(r"C:\AI AGENT\UM_EcoPark\04_figma")

W, H = 360, 800          # Android standard, dp
GAP = 60
G = "#d9dedb"            # placeholder block
GD = "#b4bcb8"           # strong placeholder
GT = "#8a938f"           # annotation text
GDARK = "#6b7570"        # annotation text, high contrast on G
EDGE = "#eef1f0"

BAR_H, NAV_H = 92, 64

SCREENS = [
    ("S01 Beranda", "Beranda", [
        ("box", 16, 108, W - 32, 112, G, 12, "Statistik total slot"),
        ("box", 16, 236, W - 32, 76, G, 12, "Card gedung - B"),
        ("box", 16, 324, W - 32, 76, G, 12, "Card gedung - A"),
        ("box", 16, 412, W - 32, 84, G, 12, "Kualitas udara"),
    ], 0),
    ("S02 Detail Gedung", "Slot", [
        ("box", 16, 108, W - 32, 128, G, 12, "Kapasitas per lantai"),
        ("box", 16, 248, W - 32, 132, G, 12, "Grid slot tersedia"),
        ("box", 16, 396, W - 32, 96, G, 12, "Fasilitas"),
        ("box", 16, 508, W - 32, 52, GD, 12, "CTA Pilih Slot"),
    ], 1),
    ("S03 Slot Terpilih", "Slot", [
        ("box", 16, 108, W - 32, 168, G, 12, "Slot dipilih"),
        ("box", 16, 292, W - 32, 176, G, 12, "Rincian biaya"),
        ("box", 16, 484, W - 32, 52, GD, 12, "CTA Bayar"),
        ("box", 16, 548, W - 32, 44, EDGE, 12, "Batal"),
    ], 1),
    ("S04 Navigasi", "Slot", [
        ("box", 16, 108, W - 32, 96, G, 16, "Jarak tersisa"),
        ("step", 16, 220, W - 32, 56, "Langkah 1"),
        ("step", 16, 288, W - 32, 56, "Langkah 2"),
        ("step", 16, 356, W - 32, 56, "Langkah 3"),
        ("step", 16, 424, W - 32, 56, "Langkah 4"),
    ], 1),
    ("S05 Status Kosong", "Riwayat", [
        ("box", 16, 108, W - 32, 148, EDGE, 12, "Empty state"),
        ("box", 16, 272, W - 32, 120, G, 12, "Rekomendasi gedung"),
        ("box", 16, 408, W - 32, 152, G, 12, "Tips parking"),
    ], 2),
    ("S06 Error Sensor", "Slot", [
        ("box", 16, 108, W - 32, 176, "#e3e6e5", 12, "Error state"),
        ("box", 16, 300, W - 32, 52, GD, 12, "CTA Coba lagi"),
        ("box", 16, 364, W - 32, 52, G, 12, "Pilih slot lain"),
        ("box", 16, 432, W - 32, 128, G, 12, "Bantuan"),
    ], 1),
    ("S07 Kualitas Udara", "Beranda", [
        ("box", 16, 108, W - 32, 140, G, 16, "Indeks AQI"),
        ("bar", 16, 264, W - 32, 50, "Gedung A"),
        ("bar", 16, 326, W - 32, 50, "Gedung B"),
        ("bar", 16, 388, W - 32, 50, "Gedung C"),
        ("bar", 16, 450, W - 32, 50, "Gedung D"),
        ("box", 16, 524, W - 32, 100, G, 12, "Catatan sumber"),
    ], 0),
]

NAV_ITEMS = ["Beranda", "Slot", "Riwayat", "Profil"]


def chrome(title: str, active: int) -> str:
    """App bar + bottom nav, identical across every screen."""
    out = [
        f'<rect x="0" y="0" width="{W}" height="{BAR_H}" fill="{GD}"/>',
        f'<text x="24" y="38" font-size="16" font-weight="700" fill="{GDARK}">Judul layar</text>',
        f'<text x="24" y="62" font-size="11" fill="{GT}">Subjudul konteks</text>',
    ]
    y = H - NAV_H
    out.append(f'<rect x="0" y="{y}" width="{W}" height="{NAV_H}" fill="{EDGE}"/>')
    out.append(f'<rect x="0" y="{y}" width="{W}" height="1" fill="{G}"/>')
    for i, item in enumerate(NAV_ITEMS):
        x = 20 + i * 86
        fill = GDARK if i == active else GT
        weight = "700" if i == active else "400"
        out.append(
            f'<text x="{x}" y="{y + 34}" font-size="10" font-weight="{weight}" fill="{fill}">{item}</text>'
        )
        if i == active:
            out.append(
                f'<rect x="{x}" y="{y + 44}" width="50" height="3" rx="1.5" fill="{GD}"/>'
            )
    return "".join(out)


def block(kind, x, y, w, h, *rest) -> str:
    """One wireframe element: a placeholder box with its role written inside.

    "step" and "bar" rows carry only (kind, x, y, w, h, label); "box" rows add
    fill, radius before the label.
    """
    label = rest[-1]
    fill = rest[-3] if len(rest) >= 3 else G
    radius = rest[-2] if len(rest) >= 3 else 0
    if kind == "bar":
        body = [
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}"/>',
            f'<text x="{x + 12}" y="{y + 26}" font-size="12" font-weight="700" fill="{GDARK}">{escape(label)}</text>',
            f'<rect x="{x + 16}" y="{y + 30}" width="120" height="6" rx="3" fill="{GD}"/>',
        ]
        return "".join(body)

    if kind == "step":
        body = [
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}"/>',
            f'<circle cx="{x + 26}" cy="{y + 28}" r="12" fill="none" stroke="{GD}" stroke-width="2"/>',
            f'<text x="{x + 46}" y="{y + 32}" font-size="11" font-weight="700" fill="{GDARK}">{escape(label)}</text>',
        ]
        return "".join(body)

    rx = f' rx="{radius}"' if radius else ""
    body = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}"{rx} fill="{fill}"/>',
        f'<text x="{x + 10}" y="{y + 24}" font-size="11" font-weight="500" fill="{GDARK}">{escape(label)}</text>',
    ]
    return "".join(body)


def screen_body(title: str, rows, active: int) -> str:
    parts = [chrome(title, active)]
    for i, row in enumerate(rows):
        parts.append(block(*row))
        # connector between consecutive steps on the navigation screen
        if row[0] == "step" and i < len(rows) - 1:
            nxt = rows[i + 1]
            parts.append(
                f'<rect x="{row[1] + 26}" y="{row[2] + row[3]}" width="2" '
                f'height="{nxt[2] - (row[2] + row[3])}" fill="{G}"/>'
            )
    return "".join(parts)


def screen_svg(title: str, rows, active: int) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}">'
        f'<rect width="{W}" height="{H}" fill="#ffffff"/>'
        f"{screen_body(title, rows, active)}</svg>"
    )


def combined_svg() -> str:
    total_w = W * len(SCREENS) + GAP * (len(SCREENS) - 1)
    parts = []
    for i, (title, _a, rows, active) in enumerate(SCREENS):
        x = i * (W + GAP)
        parts.append(
            f'<g transform="translate({x},0)">{screen_body(title, rows, active)}</g>'
        )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="{H}" '
        f'viewBox="0 0 {total_w} {H}">'
        f'<rect width="{total_w}" height="{H}" fill="#f7f8f6"/>' + "".join(parts) + "</svg>"
    )


HTML = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>UM Copark - Wireframe</title>
<style>
  :root {{ --ink:#141a16; --muted:#5a6560; --line:#dce3dd; --bg:#f7f8f6; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; padding:32px 24px 64px; background:var(--bg); color:var(--ink);
         font:15px/1.5 Inter,"Segoe UI",system-ui,sans-serif; }}
  header {{ max-width:1360px; margin:0 auto 28px; }}
  h1 {{ margin:0 0 6px; font-size:24px; letter-spacing:-.01em; }}
  p {{ margin:0; color:var(--muted); max-width:70ch; }}
  .sheet {{ display:flex; gap:{gap}px; overflow-x:auto; padding:24px;
            background:#fff; border:1px solid var(--line); border-radius:16px;
            max-width:1360px; margin:0 auto; }}
  figure {{ margin:0; flex:0 0 auto; }}
  figcaption {{ margin-top:12px; font-size:13px; font-weight:700; }}
  figcaption span {{ display:block; font-weight:400; color:var(--muted); font-size:12px; }}
  svg {{ display:block; width:360px; height:800px; border:1px solid var(--line); border-radius:8px; }}
  footer {{ max-width:1360px; margin:24px auto 0; font-size:13px; color:var(--muted); }}
</style>
</head>
<body>
<header>
  <h1>UM Copark - Wireframe</h1>
  <p>Tujuh alur low-fidelity, Android {w}dp.Abu-abu sepenuhnya: belum ada keputusan warna,
     supaya arsitektur informasi dulu disepakati sebelum masuk tahap visual.
     Seret file wireframes.svg ke Figma untuk layer vektor asli.</p>
</header>
<div class="sheet">
{cards}
</div>
<footer>Sumber token: 02_brand/tokens.json &middot; semua ukuran dalam dp, rasio 1:1</footer>
</body>
</html>
"""


def main() -> None:
    cards = []
    for title, _nav, rows, active in SCREENS:
        slug = title.split()[0].lower()
        path = OUT / f"wf_{slug}.svg"
        path.write_text(screen_svg(title, rows, active), encoding="utf-8")
        cards.append(
            f"<figure>{screen_svg(title, rows, active)}"
            f"<figcaption>{escape(title)}<span>{len(rows)} elemen &middot; "
            f"tab {escape(_nav)}</span></figcaption></figure>"
        )

    (OUT / "wireframes.svg").write_text(combined_svg(), encoding="utf-8")
    html = HTML.format(gap=GAP, w=W, cards="".join(cards))
    (OUT / "wireframes.html").write_text(html, encoding="utf-8")

    print(f"wireframes.svg   {len(combined_svg())} bytes")
    print(f"wireframes.html  {len(html)} bytes")
    print(f"per-screen svg   {len(SCREENS)} files")


if __name__ == "__main__":
    main()