# UM EcoPark — Design Deliverable Pipeline

Smart Campus Parking UM (Transportasi utama) x Green Campus (Sub-tema).
Kelompok 4 UCD 2026 — Universitas Negeri Malang.

## Struktur

```
UM_EcoPark/
├── 00_flow/          Tahap 0 — Flow design (screen map, 3 jalur, state)
├── 01_wireframe/     Tahap 1 — Low fidelity wireframe (grayscale, tanpa warna)
├── 02_brand/         Tahap 2 — Brand guideline (DESIGN.md + exports)
├── 03_medium_fi/     Tahap 3 — Medium fidelity design (token diterapkan)
└── docs/             Catatan keputusan desain
```

## Urutan Kerja (dan kenapa)

| Tahap | Isi | Skill | Kenapa di posisi ini |
|---|---|---|---|
| 0 | Flow design | `archify` | Mustahil bikin layar tanpa tahu alurnya |
| 1 | Wireframe low-fi | manual HTML/SVG | Sengaja tanpa warna - user menilai warna, bukan alur |
| 2 | Brand guideline | `design-md` | Warna & font masuk HANYA setelah alur locked |
| 3 | Medium fidelity | token + wireframe | Warna/font nyata, komponen nyata |

## Platform

Web responsif, mobile-first (375px baseline).
Mahasiswa = Majority user = HP. Gate Digital UM sudah QRIS cashless.

## Ground Rules (dari `ucd-excalidraw-canvas`)

- Nol emoji, nol ikon dekoratif dalam teks formal.
- Semua angka harus berasal dari sumber nyata atau diberi label estimasi.
- Tidak ada placeholder image, tidak ada Unsplash.
- Penomoran_acak tidak dipakai; semua label deskriptif.

## Sumber Data (sudah diverifikasi sebelumnya)

- Skripsi UM 2023 (repository.um.ac.id/355402) — 1.731 motor + 241 mobil puncak, indeks 74%
- Sudutkota.id 24 Juli 2025 — Gate Digital Rp 1,5 M, WR II Prof. Puji Handayani
- Mojok.co Des 2024 — esai Ahmad Fahrizal Ilham + kutipan P1-P8
- UI GreenMetric 2024 — UM skor 8025, TR 1575 (terlemah ke-2)
- Benchmark karbon: IPB, UB, Unand, ITB, Unimal

## Status Verifikasi (2026-10-06)

| Pemeriksaan | Hasil |
|---|---|
| archify visual-check flow | pass di 375x667, 768x1024, 1440x900, 2048x1320 |
| SVG low-fi (7 layar) | XML valid semua, ASCII bersih |
| design-md lint DESIGN.md | 0 error, 0 warning |
| Export token | tokens.json (DTCG), tailwind.theme.json, theme.css |
| SVG medium-fi (7 layar) | XML valid semua, warna dari tokens.json |

Catatan: pemeriksaan visual piksel (apakah tampilannya benar) belum dilakukan —
perlu review manusia atau model dengan kemampuan vision. Geometri dicek
otomatis lewat visual-check arsitektur, bukan lewat pemahaman visual.
