const { Penpot } = require("./penpot_sse.js");

// Tokens: C:\AI AGENT\UM_EcoPark\02_brand\tokens.json -> DESIGN.md authoritative values
const C = {
  primary: "#0f6e3d",
    primaryDark: "#1b3a5c",
    primaryLight: "#e8f2ea",
    secondary: "#f2a71b",
    accent: "#c3352b",
    bg: "#f7f8f6",
    surface: "#ffffff",
    ink: "#141a16",
    inkMuted: "#5a6560",
    line: "#dce3dd",
    success: "#15703c",
    danger: "#c3352b",
    warning: "#e8a317",
};
const F = "Inter";
const W = 360;
const H = 800;

const CODE = `
const C = ${JSON.stringify(C)};
const F = ${JSON.stringify(F)};
const W = ${W};
const H = ${H};
const solid = (hex) => [{ fillColor: hex, fillOpacity: 1 }];

// ── helpers: idempotent so re-runs update instead of duplicating ──────────
// Penpot normalises "/" to " / " in shape names, so match on "COPARK" alone.
const old = penpot.currentPage.root.children.filter((s) => String(s.name).startsWith("COPARK"));
for (const s of old) s.remove();

let made = 0;
const board = (name, x) => {
  const b = penpot.createBoard();
  b.name = name;
  b.resize(W, H);
  b.x = x;
  b.y = 0;
  b.fills = solid(C.bg);
  made++;
  return b;
};
const rect = (p, x, y, w, h, fill, r = 0, name = "") => {
  const s = penpot.createRectangle();
  s.resize(w, h);
  s.x = x;
  s.y = y;
  s.fills = solid(fill);
  s.borderRadius = r;
  if (name) s.name = name;
  p.appendChild(s);
  made++;
  return s;
};
const txt = (p, x, y, s, size = 13, weight = "400", fill = C.ink, w = "auto-width") => {
  const t = penpot.createText(s);
  t.x = x;
  t.y = y;
  t.growType = w;
  t.fontFamily = F;
  t.fontSize = String(size);
  t.fontWeight = weight;
  t.letterSpacing = String(size * 0.01);
  t.fills = solid(fill);
  p.appendChild(t);
  made++;
  return t;
};
const appbar = (p, title, sub) => {
  rect(p, 0, 0, W, 92, C.primary, 0);
  txt(p, 24, 22, title, 20, "700", "#FFFFFF");
  if (sub) txt(p, 24, 52, sub, 12, "400", "#a9d4bd");
};
const navbar = (p, items, active) => {
  const y = H - 64;
  rect(p, 0, y, W, 64, C.surface, 0);
  rect(p, 0, y, W, 1, C.line, 0);
  const step = W / items.length;
  items.forEach((it, i) => {
    const cx = step * i + step / 2;
    if (i === active) rect(p, cx - 22, y + 8, 44, 3, C.primary, 2);
    txt(p, cx - 26, y + 20, it, 10, i === active ? "700" : "400", i === active ? C.primary : C.inkMuted);
  });
};
const card = (p, x, y, w, h, title, lines) => {
  rect(p, x, y, w, h, C.surface, 12);
  rect(p, x, y, 4, h, C.primary, 2);
  txt(p, x + 16, y + 14, title, 14, "700");
  lines.forEach((l, i) => txt(p, x + 16, y + 38 + i * 18, l, 11, "400", C.inkMuted));
};

// ── Page 2: Screens, medium fidelity, mobile 360x800 ──────────────────────
const GAP = 60;
const screens = [];

const b1 = board("COPARK/S01 Beranda", 0);
appbar(b1, "UM Copark", "Universitas Negeri Malang");
rect(b1, 16, 108, W - 32, 112, C.primaryDark, 16);
txt(b1, 32, 124, "Total Slot Tersedia", 12, "400", "#a9d4bd");
txt(b1, 32, 146, "1.284", 40, "700", "#FFFFFF");
txt(b1, 32, 192, "dari 1.560 slot", 11, "400", "#7fc39a");
rect(b1, 16, 236, W - 32, 76, C.surface, 12);
txt(b1, 32, 252, "Gedung B", 13, "700");
txt(b1, 32, 274, "B214, B215, B216", 11, "400", C.inkMuted);
rect(b1, W - 116, 252, 92, 44, C.primaryLight, 10);
txt(b1, W - 104, 268, "Lihat", 11, "700", C.primaryDark);
rect(b1, 16, 324, W - 32, 76, C.surface, 12);
txt(b1, 32, 340, "Gedung A", 13, "700");
txt(b1, 32, 362, "A101, A102, A103", 11, "400", C.inkMuted);
rect(b1, W - 116, 340, 92, 44, C.primaryLight, 10);
txt(b1, W - 104, 356, "Lihat", 11, "700", C.primaryDark);
rect(b1, 16, 412, W - 32, 84, C.surface, 12);
txt(b1, 32, 428, "Kualitas Udara chargers", 13, "700");
txt(b1, 32, 450, "Baik  -  Indeks 42", 11, "400", C.success);
navbar(b1, ["Beranda", "Slot", "Riwayat", "Profil"], 0);
screens.push(b1);

const b2 = board("COPARK/S02 Detail Gedung", W + GAP);
appbar(b2, "Detail Gedung", "Gedung B  -  Universitas Negeri Malang");
card(b2, 16, 108, W - 32, 128, "Kapasitas", [
  "Tersedia   312 dari 480 slot",
  "Lantai 1   24 kosong",
  "Lantai 2   186 kosong",
  "Lantai 3   102 kosong",
]);
rect(b2, 16, 248, W - 32, 132, C.surface, 12);
txt(b2, 32, 264, "Slot Tersedia", 14, "700");
["B214", "B215", "B216", "B301"].forEach((s, i) => {
  const x = 32 + (i % 2) * 148;
  const y = 292 + Math.floor(i / 2) * 40;
  rect(b2, x, y, 132, 32, C.primaryLight, 8);
  txt(b2, x + 52, y + 9, s, 12, "700", C.primaryDark);
});
rect(b2, 16, 396, W - 32, 96, C.surface, 12);
txt(b2, 32, 412, "Fasilitas", 14, "700");
txt(b2, 32, 436, "Ramp akses kursi roda", 11, "400", C.inkMuted);
txt(b2, 32, 456, "Jalur evakuasi ditandai", 11, "400", C.inkMuted);
rect(b2, 16, 508, W - 32, 52, C.primary, 12);
txt(b2, W / 2 - 40, 524, "Pilih Slot", 14, "700", "#FFFFFF");
navbar(b2, ["Beranda", "Slot", "Riwayat", "Profil"], 1);
screens.push(b2);

const b3 = board("COPARK/S03 Slot Terpilih", W * 2 + GAP * 2);
appbar(b3, "Konfirmasi Slot", "Gedung B  -  Lantai 2");
rect(b3, 16, 108, W - 32, 168, C.surface, 12);
txt(b3, 32, 124, "Slot B214", 24, "700", C.primaryDark);
rect(b3, 32, 164, 92, 28, C.primaryLight, 8);
txt(b3, 44, 171, "Tersedia", 11, "700", C.success);
txt(b3, 32, 206, "Gedung B  -  Lantai 2  -  Zona Timur", 11, "400", C.inkMuted);
txt(b3, 32, 232, "Estimasi durasi   4 jam", 12, "700");
rect(b3, 16, 292, W - 32, 176, C.surface, 12);
txt(b3, 32, 308, "Ringkasan Biaya", 14, "700");
const fees = [
  ["Tarif dasar", "Rp 2.000"],
  ["Durasi 4 jam", "Rp 4.000"],
  ["Diskon mahasiswa", "- Rp 1.000"],
  ["Total", "Rp 5.000"],
];
fees.forEach((f, i) => {
  const y = 336 + i * 26;
  txt(b3, 32, y, f[0], 11, i === 3 ? "700" : "400", i === 3 ? C.ink : C.inkMuted);
  txt(b3, W - 100, y, f[1], 11, i === 3 ? "700" : "400", i === 3 ? C.primaryDark : C.inkMuted);
});
rect(b3, 16, 484, W - 32, 52, C.primary, 12);
txt(b3, W / 2 - 48, 500, "Bayar Sekarang", 14, "700", "#FFFFFF");
rect(b3, 16, 548, W - 32, 44, C.surface, 12);
txt(b3, W / 2 - 56, 560, "Batal", 13, "700", C.inkMuted);
navbar(b3, ["Beranda", "Slot", "Riwayat", "Profil"], 1);
screens.push(b3);

const b4 = board("COPARK/S04 Navigasi", W * 3 + GAP * 3);
appbar(b4, "Navigasi ke Slot", "Petunjuk langkah ke B214");
rect(b4, 16, 108, W - 32, 96, C.primaryDark, 16);
txt(b4, 32, 124, "Jarak tersisa", 12, "400", "#a9d4bd");
txt(b4, 32, 144, "120 meter", 32, "700", "#FFFFFF");
txt(b4, 32, 182, "Estimasi 2 menit", 11, "400", "#7fc39a");
const steps = [
  ["Keluar dari lift lantai 1", "Sudah"],
  ["Belok kiri di koridor utama", "60 m"],
  ["Naik tangga menuju lantai 2", "40 m"],
  ["Slot B214 di sisi kanan", "Tujuan"],
];
steps.forEach((s, i) => {
  const y = 220 + i * 68;
  rect(b4, 16, y, W - 32, 56, C.surface, 12);
  rect(b4, 32, y + 16, 24, 24, i === 3 ? C.primary : C.primaryLight, 12);
  txt(b4, 38, y + 22, String(i + 1), 11, "700", i === 3 ? "#FFFFFF" : C.primaryDark);
  txt(b4, 68, y + 12, s[0], 12, "700");
  txt(b4, 68, y + 32, s[1], 10, "400", C.inkMuted);
  if (i < 3) rect(b4, 43, y + 40, 2, 28, C.line, 0);
});
navbar(b4, ["Beranda", "Slot", "Riwayat", "Profil"], 1);
screens.push(b4);

const b5 = board("COPARK/S05 Status Kosong", W * 4 + GAP * 4);
appbar(b5, "Riwayat Parkir", "Aktivitas terakhir");
rect(b5, 16, 108, W - 32, 92, C.surface, 12);
txt(b5, 32, 124, "Belum ada riwayat", 14, "700");
txt(b5, 32, 150, "Sesi parkirmu akan muncul di sini", 11, "400", C.inkMuted);
rect(b5, W / 2 - 90, 176, 180, 40, C.primaryLight, 20);
txt(b5, W / 2 - 52, 187, "Mulai parkir", 12, "700", C.primaryDark);
rect(b5, 16, 220, W - 32, 152, C.surface, 12);
txt(b5, 32, 236, "Rekomendasi", 13, "700");
txt(b5, 32, 262, "Gedung C paling kosong saat ini", 11, "400", C.inkMuted);
txt(b5, 32, 284, "94% tersedia  -  12 menit berjalan", 10, "400", C.success);
rect(b5, 16, 388, W - 32, 120, C.surface, 12);
txt(b5, 32, 404, "Tips Parking", 13, "700");
txt(b5, 32, 430, "Gunakan jalur kanan saat ramai", 11, "400", C.inkMuted);
txt(b5, 32, 452, "Parkir di zona Student Area", 11, "400", C.inkMuted);
txt(b5, 32, 474, "K Rodeomotor tersedia dekat", 11, "400", C.inkMuted);
navbar(b5, ["Beranda", "Slot", "Riwayat", "Profil"], 2);
screens.push(b5);

const b6 = board("COPARK/S06 Error Sensor", W * 5 + GAP * 5);
appbar(b6, "Sensor Tidak Terbaca", "Gedung B  -  Lantai 2");
rect(b6, 16, 108, W - 32, 176, "#fdf1f0", 12);
rect(b6, 16, 108, 4, 176, C.danger, 2);
txt(b6, 32, 128, "Sensor B214 tidak merespons", 15, "700", C.danger);
txt(b6, 32, 158, "Status slot belum dapat dipastikan.", 11, "400", C.inkMuted);
txt(b6, 32, 180, "Coba lagi atau pilih slot lain.", 11, "400", C.inkMuted);
txt(b6, 32, 214, "Terakhir diperbarui  09:42", 10, "400", C.inkMuted);
rect(b6, 16, 300, W - 32, 52, C.primary, 12);
txt(b6, W / 2 - 44, 316, "Coba Lagi", 14, "700", "#FFFFFF");
rect(b6, 16, 364, W - 32, 52, C.surface, 12);
txt(b6, W / 2 - 56, 380, "Pilih Slot Lain", 13, "700", C.primaryDark);
rect(b6, 16, 432, W - 32, 128, C.surface, 12);
txt(b6, 32, 448, "Sebelum resorted", 13, "700");
txt(b6, 32, 474, "Cek area informasi gedung", 11, "400", C.inkMuted);
txt(b6, 32, 496, "Hubungi petugas bila tetap gagal", 11, "400", C.inkMuted);
txt(b6, 32, 518, "Lapor lewat menu Profil", 11, "400", C.inkMuted);
navbar(b6, ["Beranda", "Slot", "Riwayat", "Profil"], 1);
screens.push(b6);

const b7 = board("COPARK/S07 Kualitas Udara", W * 6 + GAP * 6);
appbar(b7, "Kualitas Udara", "Pemantauan live kampus");
rect(b7, 16, 108, W - 32, 140, C.primaryDark, 16);
txt(b7, 32, 124, "Indeks Kualitas Udara", 12, "400", "#a9d4bd");
txt(b7, 32, 146, "42", 44, "700", "#FFFFFF");
txt(b7, 76, 172, "BAIK", 14, "700", "#7fc39a");
txt(b7, 32, 200, "PM2.5  12 ug/m3   -   CO  0.4 ppm", 10, "400", "#7fc39a");
const aq = [
  ["Gedung A", 38, C.success],
  ["Gedung B", 44, C.success],
  ["Gedung C", 51, C.warning],
  ["Gedung D", 67, C.secondary],
];
aq.forEach((a, i) => {
  const y = 264 + i * 62;
  rect(b7, 16, y, W - 32, 50, C.surface, 12);
  txt(b7, 32, y + 10, a[0], 12, "700");
  rect(b7, 32, y + 30, W - 220, 6, C.line, 3);
  rect(b7, 32, y + 30, (W - 220) * (a[1] / 100), 6, a[2], 3);
  txt(b7, W - 56, y + 18, String(a[1]), 12, "700", a[2]);
});
rect(b7, 16, 524, W - 32, 100, C.surface, 12);
txt(b7, 32, 540, "CatatanGamet", 12, "700");
txt(b7, 32, 564, "Sensor diperbarui tiap 5 menit", 11, "400", C.inkMuted);
txt(b7, 32, 586, "Data dariium Green Campus", 11, "400", C.inkMuted);
navbar(b7, ["Beranda", "Slot", "Riwayat", "Profil"], 0);
screens.push(b7);

return {
  made,
  boards: screens.map((s) => s.name),
  pageShapes: penpot.currentPage.root.children.length,
};
`;

(async () => {
  const p = new Penpot();
  const { session } = await p.connect();
  const { msg } = await p.call(session, "execute_code", { code: CODE });
  console.log(JSON.stringify(msg.result.content, null, 1).slice(0, 2500));
})();