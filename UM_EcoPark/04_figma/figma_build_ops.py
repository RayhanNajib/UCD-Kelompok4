"""Build the UM EcoPark Figma ops list from DESIGN.md tokens.

Kept as a module so the ops JSON is regenerated from the token file rather than
hand-copied. Run figma_build_ops.py to refresh 04_figma/ops.json.
"""

import json
import os

BRAND = r"C:\AI AGENT\UM_EcoPark\02_brand"
OUT = r"C:\AI AGENT\UM_EcoPark\04_figma"

TOK = json.load(open(os.path.join(BRAND, "tokens.json"), encoding="utf-8"))
C = {k: v["$value"]["hex"] for k, v in TOK["color"].items()
     if not k.startswith("$") and isinstance(v, dict) and "hex" in v["$value"]}
R = {k: int(v["$value"]["value"]) for k, v in TOK["rounded"].items() if not k.startswith("$")}
S = {k: int(v["$value"]["value"]) for k, v in TOK["spacing"].items() if not k.startswith("$")}

GREY = {"bg": "#ffffff", "line": "#1a1a1a", "mid": "#9a9a9a", "soft": "#d4d4d4", "fill": "#f0f0f0"}
W, H = 375, 812
PAD = S["md"]          # 16
ops = []

# ── Page 1: Brand Kit ────────────────────────────────────────────────────────
ops.append({"op": "page", "name": "Brand Kit"})

ops.append({"op": "frame", "name": "Colors", "parent": "Brand Kit",
            "x": 0, "y": 0, "w": 1240, "h": 420, "fill": C["neutral"]})
ops.append({"op": "text", "parent": "Colors", "text": "Color tokens", "x": 40, "y": 56,
            "size": 28, "weight": 700, "fill": C["text-primary"], "name": "h_colors"})
ops.append({"op": "text", "parent": "Colors",
            "text": "Status trio is the only way availability is shown. "
                    "Amber takes dark text: white on #e8a317 is 2.1:1.",
            "x": 40, "y": 84, "size": 14, "fill": C["text-secondary"]})

sw = [(k, v) for k, v in C.items()]
for i, (name, hexv) in enumerate(sw):
    col, row = i % 6, i // 6
    x, y = 40 + col * 195, 130 + row * 128
    ops.append({"op": "rect", "parent": "Colors", "name": f"sw_{name}",
                "x": x, "y": y, "w": 175, "h": 76, "fill": hexv, "radius": R["sm"]})
    ops.append({"op": "text", "parent": "Colors", "text": name,
                "x": x, "y": y + 96, "size": 13, "weight": 600, "fill": C["text-primary"]})
    ops.append({"op": "text", "parent": "Colors", "text": hexv.upper(),
                "x": x, "y": y + 114, "size": 12, "fill": C["text-secondary"]})

ops.append({"op": "frame", "name": "Type", "parent": "Brand Kit",
            "x": 0, "y": 440, "w": 1240, "h": 560, "fill": C["neutral"]})
ops.append({"op": "text", "parent": "Type", "text": "Typography", "x": 40, "y": 496,
            "size": 28, "weight": 700, "fill": C["text-primary"]})
ops.append({"op": "text", "parent": "Type",
            "text": "Inter throughout. Display and metrics run tight so large numbers "
                    "do not stack vertically. Tabular figures on every count so the "
                    "board does not jump as the sensor sends a new value.",
            "x": 40, "y": 524, "size": 14, "fill": C["text-secondary"], "w": 700})

type_rows = [
    ("display", "Slot tersedia", 32, 700, C["text-primary"]),
    ("h1", "Rektorat", 24, 700, C["text-primary"]),
    ("h2", "Lantai 2", 18, 600, C["text-primary"]),
    ("body-md", "Zona Hijau - dekat pintu masuk", 16, 400, C["text-primary"]),
    ("body-sm", "Gedung parkir", 14, 400, C["text-secondary"]),
    ("caption", "Slot update tiap 30 detik", 12, 400, C["text-secondary"]),
    ("metric-lg", "142", 48, 700, C["status-limited"]),
]
y = 570
for token, sample, size, weight, fill in type_rows:
    ops.append({"op": "text", "parent": "Type", "text": sample,
                "x": 40, "y": y + size, "size": size, "weight": weight, "fill": fill})
    ops.append({"op": "text", "parent": "Type",
                "text": f"{token} / {size}px / w{weight}",
                "x": 640, "y": y + size, "size": 13, "fill": C["text-secondary"]})
    y += size + 34

ops.append({"op": "rect", "parent": "Type", "x": 40, "y": 880, "w": 1160, "h": 1, "fill": C["border"]})
ops.append({"op": "text", "parent": "Type", "text": "Rounded corners", "x": 40, "y": 916,
            "size": 15, "weight": 600, "fill": C["text-primary"]})
for i, (k, v) in enumerate(R.items()):
    ops.append({"op": "rect", "parent": "Type", "name": f"r_{k}",
                "x": 40 + i * 300, "y": 934, "w": 260, "h": 40, "fill": C["surface"],
                "stroke": C["border"], "radius": min(v, 20)})
    ops.append({"op": "text", "parent": "Type", "text": f"{k} - {v}px",
                "x": 56 + i * 300, "y": 960, "size": 13, "fill": C["text-secondary"]})

# ── Page 2: Wireframe (low fidelity, grayscale) ─────────────────────────────
ops.append({"op": "page", "name": "Wireframe"})


def wtext(parent, y, s, size=13, bold=False, x=PAD, fill=None, w=None):
    o = {"op": "text", "parent": parent, "text": s, "x": x, "y": y,
         "size": size, "weight": 600 if bold else 400,
         "fill": fill or GREY["line"]}
    if w:
        o["w"] = w
    ops.append(o)


def wbox(parent, y, h, label, x=PAD, w=None, strong=False):
    w = w if w is not None else W - 2 * PAD
    ops.append({"op": "rect", "parent": parent, "x": x, "y": y, "w": w, "h": h,
                "fill": GREY["fill"], "stroke": GREY["mid"] if not strong else GREY["line"],
                "strokeWeight": 1.5 if strong else 1, "radius": 8})
    if label:
        wtext(parent, y + h / 2 + 5, label, 12, False, x + 12, GREY["mid"])


def b_beranda(parent, y):
    wtext(parent, y + 18, "Selamat pagi, Rina", 18, True)
    wtext(parent, y + 40, "Kampus Rektorat, 06.45", 12, False, fill=GREY["mid"])
    y += 62
    wtext(parent, y + 10, "Status Parkir Sekarang", 14, True)
    y += 24
    for nm in ["Rektorat", "FMIPA", "FEB"]:
        wbox(parent, y, 56, nm + " - status chip")
        y += 64
    y += 8
    wbox(parent, y, 48, "Cek Slot per Lantai", strong=True)
    y += 56
    wbox(parent, y, 44, "Atur Pengingat")


def b_detail(parent, y):
    wtext(parent, y + 18, "Rektorat", 18, True)
    wtext(parent, y + 40, "Gedung parkir 3 lantai", 12, False, fill=GREY["mid"])
    y += 62
    for fl in ["Lantai 1", "Lantai 2", "Lantai 3"]:
        wtext(parent, y + 12, fl, 13, True)
        y += 22
        for r in range(2):
            for c in range(6):
                ops.append({"op": "rect", "parent": parent, "x": PAD + c * 55, "y": y,
                            "w": 46, "h": 32, "fill": GREY["fill"],
                            "stroke": GREY["mid"], "radius": 6})
            y += 38
        y += 10
    wbox(parent, y, 48, "Pilih Lantai dan Slot", strong=True)


def b_slot(parent, y):
    ops.append({"op": "rect", "parent": parent, "x": PAD, "y": y, "w": W - 2 * PAD, "h": 120,
                "fill": GREY["fill"], "stroke": GREY["mid"], "radius": R["lg"]})
    wtext(parent, y + 62, "Slot B-214", 28, True, x=W / 2 - 60)
    wtext(parent, y + 92, "Zona Hijau - dekat pintu", 12, False, x=W / 2 - 78, fill=GREY["mid"])
    y += 140
    for lb in ["Jarak ke gedung FE", "Estimasi waktu hemat", "Jarak tempuh"]:
        wtext(parent, y + 14, lb, 12, False, fill=GREY["mid"])
        ops.append({"op": "rect", "parent": parent, "x": PAD, "y": y + 24,
                    "w": W - 2 * PAD, "h": 1, "fill": GREY["soft"]})
        y += 34
    y += 10
    wbox(parent, y, 50, "Navigasi ke Slot", strong=True)


def b_navigasi(parent, y):
    wtext(parent, y + 12, "Menuju ke Slot B-214", 14, True)
    y += 28
    ops.append({"op": "rect", "parent": parent, "x": PAD, "y": y, "w": W - 2 * PAD, "h": 300,
                "fill": GREY["bg"], "stroke": GREY["mid"], "radius": R["md"]})
    for r in range(5):
        for c in range(6):
            ops.append({"op": "rect", "parent": parent, "x": PAD + 20 + c * 48, "y": y + 24 + r * 42,
                        "w": 40, "h": 32, "fill": GREY["fill"], "stroke": GREY["mid"], "radius": 4})
    ops.append({"op": "ellipse", "parent": parent, "x": PAD + 30, "y": y + 268,
                "w": 14, "h": 14, "fill": GREY["line"]})
    y += 320
    wbox(parent, y, 50, "Mulai Navigasi", strong=True)


def b_error(parent, y):
    ops.append({"op": "rect", "parent": parent, "x": PAD, "y": y, "w": W - 2 * PAD, "h": 44,
                "fill": GREY["fill"], "stroke": GREY["line"], "strokeWeight": 1.5, "radius": R["md"]})
    wtext(parent, y + 27, "Data parkir tidak tersedia", 13, True, x=PAD + 14)
    y += 54
    wtext(parent, y + 10, "Sensor terakhir merespons 12 menit lalu", 11, False, fill=GREY["mid"])
    y += 30
    wbox(parent, y, 46, "Coba Lagi", strong=True)
    y += 54
    wbox(parent, y, 44, "Lapor ke Satpam")
    y += 64
    wtext(parent, y + 10, "Tips", 12, True)
    y += 22
    for t in ["Parkir di area terbuka jika sensor mati",
              "Pusat informasi di pos satpam utama",
              "Lapor bila slot sudah terisi ulang"]:
        wtext(parent, y + 10, "- " + t, 11, False, fill=GREY["mid"])
        y += 20


def b_pengaturan(parent, y):
    wtext(parent, y + 18, "Pengaturan", 18, True)
    y += 40
    for lb in ["Nama", "Fakultas", "Gedung favorit"]:
        wtext(parent, y + 14, lb, 12, False, fill=GREY["mid"])
        ops.append({"op": "rect", "parent": parent, "x": PAD, "y": y + 24,
                    "w": W - 2 * PAD, "h": 1, "fill": GREY["soft"]})
        y += 34
    y += 14
    wtext(parent, y + 10, "Pengingat", 13, True)
    y += 24
    for t in ["06.00", "07.30", "12.00"]:
        wbox(parent, y, 44, t)
        ops.append({"op": "rect", "parent": parent, "x": W - PAD - 52, "y": y + 10,
                    "w": 40, "h": 24, "fill": GREY["soft"], "radius": 12})
        y += 52


def b_laporan(parent, y):
    wtext(parent, y + 18, "Kualitas Udara", 18, True)
    y += 40
    ops.append({"op": "rect", "parent": parent, "x": PAD, "y": y, "w": W - 2 * PAD, "h": 110,
                "fill": GREY["fill"], "stroke": GREY["mid"], "radius": R["lg"]})
    wtext(parent, y + 60, "142", 44, True, x=W / 2 - 40)
    wtext(parent, y + 82, "Index udara UM", 12, False, x=W / 2 - 52, fill=GREY["mid"])
    y += 130
    wtext(parent, y + 10, "Perbandingan sebelum dan sesudah", 12, True)
    y += 24
    for t in ["- 8% emisi dari parkir liar", "- 11 menit waktu terbuang", "+ 3 slot hijau baru"]:
        wtext(parent, y + 10, t, 12, False)
        y += 22
    y += 12
    wtext(parent, y + 10, "Estimasi mengikuti pendekatan Carbon Footprint UB 2024", 10, False, fill=GREY["mid"])
    wtext(parent, y + 26, "Sumber: UI GreenMetric 2024", 10, False, fill=GREY["mid"])


SCREENS = [
    ("WF 01 Beranda", "01 Beranda", "1/7", b_beranda),
    ("WF 02 Detail Gedung", "02 Detail Gedung", "2/7", b_detail),
    ("WF 03 Slot Terpilih", "03 Slot Terpilih", "3/7", b_slot),
    ("WF 04 Navigasi", "04 Navigasi", "4/7", b_navigasi),
    ("WF 05 Status Kosong", "05 Status Kosong", "5/7", b_error),
    ("WF 06 Pengaturan", "06 Pengaturan", "6/7", b_pengaturan),
    ("WF 07 Laporan", "07 Laporan", "7/7", b_laporan),
]

for idx, (frame_name, title, step, builder) in enumerate(SCREENS):
    # lay frames out in a row so the page reads as a flow
    ops.append({"op": "frame", "name": frame_name, "parent": "Wireframe",
                "x": idx * (W + 40), "y": 0, "w": W, "h": H, "fill": GREY["bg"]})
    ops.append({"op": "rect", "parent": frame_name, "x": PAD, "y": 20, "w": W - 2 * PAD, "h": 22,
                "fill": GREY["fill"], "stroke": GREY["mid"], "radius": 4})
    ops.append({"op": "text", "parent": frame_name, "text": title, "x": PAD + 8, "y": 36,
                "size": 13, "weight": 600, "fill": GREY["line"]})
    ops.append({"op": "text", "parent": frame_name, "text": step, "x": W - PAD - 8, "y": 36,
                "size": 11, "fill": GREY["mid"], "align": "right"})
    builder(frame_name, 64)


# ── Page 3: Screens (medium fidelity, tokens applied) ────────────────────────
ops.append({"op": "page", "name": "Screens"})


def chrome(name, idx, title, step):
    """App bar + status strip shared by every medium-fi frame."""
    ops.append({"op": "text", "parent": name, "text": "09:41", "x": PAD, "y": 24,
                "size": 12, "weight": 600, "fill": C["text-primary"]})
    ops.append({"op": "text", "parent": name, "text": f"{idx}/7", "x": W - PAD, "y": 24,
                "size": 11, "weight": 600, "fill": C["text-secondary"], "align": "right"})
    ops.append({"op": "rect", "parent": name, "x": PAD, "y": 36, "w": W - 2 * PAD, "h": 44,
                "fill": C["surface"], "radius": R["md"]})
    ops.append({"op": "text", "parent": name, "text": title, "x": PAD + 14, "y": 63,
                "size": 16, "weight": 700, "fill": C["text-primary"]})


def mtext(parent, y, s, size=13, bold=False, x=PAD, fill=None, align="left", w=None):
    o = {"op": "text", "parent": parent, "text": s, "x": x, "y": y,
         "size": size, "weight": 600 if bold else 400,
         "fill": fill or C["text-primary"], "align": align}
    if w:
        o["w"] = w
    ops.append(o)


def chip(parent, x, y, state, label=None):
    m = {"available": (C["status-available"], "Tersedia", "#ffffff", 76),
         "limited": (C["status-limited"], "Terbatas", C["text-primary"], 74),
         "full": (C["status-full"], "Penuh", "#ffffff", 62)}
    bg, lab, fg, w = m[state]
    lab = label or lab
    ops.append({"op": "rect", "parent": parent, "x": x, "y": y, "w": w, "h": 24,
                "fill": bg, "radius": R["pill"]})
    ops.append({"op": "text", "parent": parent, "text": lab, "x": x + w / 2, "y": y + 16,
                "size": 11, "weight": 600, "fill": fg, "align": "center"})


def button(parent, y, label, kind="primary", h=52):
    if kind == "primary":
        bg, fg, stroke = C["primary"], "#ffffff", None
    elif kind == "accent":
        bg, fg, stroke = C["accent"], C["text-primary"], None
    else:
        bg, fg, stroke = C["surface"], C["text-primary"], C["primary"]
    o = {"op": "rect", "parent": parent, "x": PAD, "y": y, "w": W - 2 * PAD, "h": h,
         "fill": bg, "radius": R["md"]}
    if stroke:
        o["stroke"] = stroke
        o["strokeWeight"] = 1.5
    ops.append(o)
    ops.append({"op": "text", "parent": parent, "text": label, "x": W / 2, "y": y + h / 2 + 5,
                "size": 15, "weight": 700 if kind == "accent" else 600,
                "fill": fg, "align": "center"})


def tile(parent, x, y, num, state, w=46, h=32):
    bg = {"available": C["status-available"], "limited": C["status-limited"],
          "full": C["status-full"]}[state]
    fg = C["text-primary"] if state == "limited" else "#ffffff"
    ops.append({"op": "rect", "parent": parent, "x": x, "y": y, "w": w, "h": h,
                "fill": bg, "radius": R["sm"]})
    ops.append({"op": "text", "parent": parent, "text": num, "x": x + w / 2, "y": y + h / 2 + 4,
                "size": 11, "weight": 700, "fill": fg, "align": "center"})


def m_beranda(parent, y):
    mtext(parent, y + 18, "Selamat pagi, Rina", 19, True)
    mtext(parent, y + 40, "Kampus Rektorat, 06.45", 12, fill=C["text-secondary"])
    y += 62
    mtext(parent, y + 12, "Status Parkir Sekarang", 14, True)
    y += 26
    for nm, st in [("Rektorat", "available"), ("FMIPA", "limited"), ("FEB", "available")]:
        ops.append({"op": "rect", "parent": parent, "x": PAD, "y": y, "w": W - 2 * PAD, "h": 60,
                    "fill": C["surface"], "stroke": C["border"], "radius": R["md"]})
        mtext(parent, y + 26, nm, 15, True, x=PAD + 14)
        mtext(parent, y + 44, "Gedung parkir", 11, x=PAD + 14, fill=C["text-secondary"])
        chip(parent, W - PAD - 90, y + 18, st)
        y += 68
    y += 4
    button(parent, y, "Cek Slot per Lantai")
    y += 62
    button(parent, y, "Atur Pengingat 06.00", "secondary", 48)


def m_detail(parent, y):
    mtext(parent, y + 18, "Rektorat", 19, True)
    mtext(parent, y + 40, "Gedung parkir 3 lantai", 12, fill=C["text-secondary"])
    y += 62
    for fl, st in [("Lantai 1", "available"), ("Lantai 2", "limited"), ("Lantai 3", "available")]:
        mtext(parent, y + 16, fl, 14, True)
        chip(parent, W - PAD - 90, y, st)
        y += 24
        for r in range(2):
            for c in range(6):
                tile(parent, PAD + c * 55, y, f"B{211 + r * 6 + c}", st)
            y += 38
        y += 8
    button(parent, y + 6, "Pilih Lantai dan Slot Kosong")


def m_slot(parent, y):
    ops.append({"op": "rect", "parent": parent, "x": PAD, "y": y, "w": W - 2 * PAD, "h": 132,
                "fill": C["surface"], "stroke": C["border"], "radius": R["lg"]})
    mtext(parent, y + 54, "Slot B-214", 30, True, x=W / 2, align="center")
    ops.append({"op": "rect", "parent": parent, "x": W / 2 - 58, "y": y + 70, "w": 116, "h": 26,
                "fill": C["primary"], "radius": R["pill"]})
    mtext(parent, y + 88, "Lantai 2", 12, True, x=W / 2, fill="#ffffff", align="center")
    mtext(parent, y + 116, "Zona Hijau - dekat pintu masuk", 11, x=W / 2,
          fill=C["text-secondary"], align="center")
    y += 148
    for lb, val in [("Jarak ke gedung FE", "45 meter"), ("Estimasi waktu hemat", "11 menit"),
                    ("Jarak tempuh", "3 menit jalan kaki")]:
        mtext(parent, y + 12, lb, 12, fill=C["text-secondary"])
        mtext(parent, y + 12, val, 13, True, x=W - PAD, align="right")
        ops.append({"op": "rect", "parent": parent, "x": PAD, "y": y + 24,
                    "w": W - 2 * PAD, "h": 1, "fill": C["border"]})
        y += 32
    y += 14
    button(parent, y, "Navigasi ke Slot", "accent", 54)


def m_navigasi(parent, y):
    mtext(parent, y + 12, "Menuju ke Slot B-214", 14, True)
    y += 28
    ops.append({"op": "rect", "parent": parent, "x": PAD, "y": y, "w": W - 2 * PAD, "h": 320,
                "fill": C["surface"], "stroke": C["border"], "radius": R["md"]})
    mtext(parent, y + 26, "Denah Lantai 2", 13, True, x=PAD + 16)
    for r in range(4):
        for c in range(6):
            st = "full" if (r == 1 and c == 5) else ("limited" if (r == 0 and c == 4) else "available")
            tile(parent, PAD + 20 + c * 48, y + 48 + r * 40, "", st, 40, 30)
    ops.append({"op": "rect", "parent": parent, "x": PAD + 20 + 1 * 48, "y": y + 88,
                "w": 40, "h": 30, "stroke": C["accent"], "strokeWeight": 3, "radius": R["sm"]})
    ops.append({"op": "text", "parent": parent, "text": "B214", "x": PAD + 20 + 1 * 48 + 20,
                "y": y + 108, "size": 8, "weight": 700, "fill": C["text-primary"], "align": "center"})
    ops.append({"op": "ellipse", "parent": parent, "x": PAD + 32, "y": y + 272,
                "w": 14, "h": 14, "fill": C["secondary"]})
    mtext(parent, y + 16, "Tujuan: B214", 10, True, x=PAD + 200, fill=C["primary"])
    y += 336
    button(parent, y, "Mulai Navigasi", "accent", 54)


def m_error(parent, y):
    ops.append({"op": "rect", "parent": parent, "x": PAD, "y": y, "w": W - 2 * PAD, "h": 44,
                "fill": C["status-full"], "radius": R["md"]})
    mtext(parent, y + 28, "Data parkir tidak tersedia", 13, True, x=PAD + 14, fill="#ffffff")
    mtext(parent, y + 64, "Sensor terakhir merespons 12 menit lalu", 11, fill=C["text-secondary"])
    y += 82
    button(parent, y, "Coba Lagi", "primary", 50)
    y += 62
    button(parent, y, "Lapor ke Satpam", "secondary", 48)
    y += 64
    ops.append({"op": "rect", "parent": parent, "x": PAD, "y": y, "w": W - 2 * PAD, "h": 1,
                "fill": C["border"]})
    y += 18
    mtext(parent, y + 6, "Tips", 12, True)
    y += 20
    for t in ["Parkir di area terbuka jika sensor mati",
              "Pusat informasi di pos satpam utama",
              "Lapor bila slot sudah terisi ulang"]:
        mtext(parent, y + 8, "- " + t, 11, fill=C["text-secondary"])
        y += 20


def m_pengaturan(parent, y):
    mtext(parent, y + 18, "Pengaturan", 19, True)
    y += 42
    for lb, val in [("Nama", "Rina"), ("Fakultas", "Teknik"), ("Gedung favorit", "Rektorat")]:
        mtext(parent, y + 12, lb, 12, fill=C["text-secondary"])
        mtext(parent, y + 12, val, 13, True, x=W - PAD, align="right")
        ops.append({"op": "rect", "parent": parent, "x": PAD, "y": y + 22,
                    "w": W - 2 * PAD, "h": 1, "fill": C["border"]})
        y += 32
    y += 20
    mtext(parent, y + 6, "Pengingat", 13, True)
    y += 20
    for jam, on in [("06.00", True), ("07.30", False), ("12.00", True)]:
        ops.append({"op": "rect", "parent": parent, "x": PAD, "y": y, "w": W - 2 * PAD, "h": 52,
                    "fill": C["surface"], "stroke": C["border"], "radius": R["md"]})
        mtext(parent, y + 32, jam, 14, True, x=PAD + 14)
        ops.append({"op": "rect", "parent": parent, "x": W - PAD - 52, "y": y + 14,
                    "w": 40, "h": 24, "fill": C["primary"] if on else C["border"],
                    "radius": R["pill"]})
        ops.append({"op": "ellipse", "parent": parent,
                    "x": W - PAD - 52 + (30 if on else 10), "y": y + 17,
                    "w": 18, "h": 18, "fill": "#ffffff"})
        y += 60


def m_laporan(parent, y):
    mtext(parent, y + 18, "Kualitas Udara", 19, True)
    y += 42
    ops.append({"op": "rect", "parent": parent, "x": PAD, "y": y, "w": W - 2 * PAD, "h": 120,
                "fill": C["surface"], "stroke": C["border"], "radius": R["lg"]})
    mtext(parent, y + 64, "142", 48, True, x=W / 2, align="center", fill=C["status-limited"])
    mtext(parent, y + 86, "Indeks udara UM", 12, x=W / 2, fill=C["text-secondary"], align="center")
    chip(parent, W / 2 - 48, y + 94, "limited", "Tidak Sehat")
    y += 136
    mtext(parent, y + 10, "Perbandingan sebelum dan sesudah", 12, True)
    y += 24
    for t, col in [("- 8% emisi dari parkir liar", C["status-available"]),
                   ("- 11 menit waktu terbuang", C["status-available"]),
                   ("+ 3 slot hijau baru", C["primary"])]:
        mtext(parent, y + 10, t, 12, fill=col)
        y += 22
    y += 10
    mtext(parent, y + 10, "Estimasi mengikuti pendekatan Carbon Footprint UB 2024", 10,
          fill=C["text-secondary"])
    mtext(parent, y + 26, "Sumber: UI GreenMetric 2024", 10, fill=C["text-secondary"])


MF = [
    ("MF 01 Beranda", "Beranda", 1, m_beranda),
    ("MF 02 Detail Gedung", "Detail Gedung", 2, m_detail),
    ("MF 03 Slot Terpilih", "Slot Terpilih", 3, m_slot),
    ("MF 04 Navigasi", "Navigasi", 4, m_navigasi),
    ("MF 05 Status Kosong", "Status Kosong", 5, m_error),
    ("MF 06 Pengaturan", "Pengaturan", 6, m_pengaturan),
    ("MF 07 Laporan", "Laporan", 7, m_laporan),
]

for idx, (frame_name, title, num, builder) in enumerate(MF):
    ops.append({"op": "frame", "name": frame_name, "parent": "Screens",
                "x": idx * (W + 40), "y": 0, "w": W, "h": H, "fill": C["neutral"]})
    chrome(frame_name, num, title, f"{num}/7")
    builder(frame_name, 96)


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, "ops.json")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(ops, f, ensure_ascii=False, indent=1)
    by_op = {}
    for o in ops:
        by_op[o["op"]] = by_op.get(o["op"], 0) + 1
    print(f"{len(ops)} ops -> {p}")
    print(by_op)


if __name__ == "__main__":
    main()