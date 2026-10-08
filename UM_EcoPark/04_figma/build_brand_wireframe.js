const { Penpot } = require("./penpot_sse.js");

// Values read from 02_brand/tokens.json (DTCG). Source of truth, not guesses.
const TOK = {
  color: {
    primary: "#0f6e3d",
    secondary: "#1b3a5c",
    accent: "#f2a71b",
    neutral: "#f7f8f6",
    surface: "#ffffff",
    "text-primary": "#141a16",
    "text-secondary": "#5a6560",
    "status-available": "#15703c",
    "status-limited": "#e8a317",
    "status-full": "#c3352b",
    border: "#dce3dd",
  },
  rounded: { sm: 8, md: 12, lg: 16, pill: 999 },
  spacing: { xs: 4, sm: 8, md: 16, lg: 24, xl: 32, xxl: 48 },
  type: [
    ["display", 32, "700", "UM Copark"],
    ["h1", 24, "700", "Cari Slot Parkir"],
    ["h2", 18, "600", "Gedung B"],
    ["body-md", 16, "400", "312 slot tersedia hari ini"],
    ["body-sm", 14, "400", "Terakhir diperbarui 09:42"],
    ["caption", 12, "500", "Data sensor kampus"],
    ["metric-lg", 48, "700", "1.284"],
  ],
};

// Everything lands on the active page: Penpot refuses to mutate an inactive
// page, and openPage() does not move the sandbox viewport, so switching pages
// is not available here. Sections are separated by a board-name prefix instead.
const CODE = `
const TOK = ${JSON.stringify(TOK)};
const C = TOK.color;
const F = "Inter";
const solid = (hex) => [{ fillColor: hex, fillOpacity: 1 }];

const page = penpot.currentPage;

// wipe only the shapes we own, so a re-run never duplicates
for (const s of page.root.children.slice()) {
  if (/^(KIT|WF) /.test(String(s.name))) s.remove();
}

let made = 0;
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
const txt = (p, x, y, s, size, weight, fill) => {
  const t = penpot.createText(s);
  t.x = x;
  t.y = y;
  t.growType = "auto-width";
  t.fontFamily = F;
  t.fontSize = String(size);
  t.fontWeight = weight;
  t.letterSpacing = String(size * -0.01);
  t.fills = solid(fill);
  p.appendChild(t);
  made++;
  return t;
};

// ── Brand Kit, to the right of the existing 7 screens ─────────────────────
const X0 = 360 * 7 + 60 * 6 + 120;

const colors = penpot.createBoard();
colors.name = "KIT / Colors";
colors.resize(760, 430);
colors.x = X0;
colors.y = 0;
colors.fills = solid(C.surface);
page.root.appendChild(colors);
made++;
txt(colors, 32, 28, "UM Copark  -  Color", 24, "700", C["text-primary"]);
txt(colors, 32, 62, "Sumber: 02_brand/tokens.json (DTCG)", 12, "500", C["text-secondary"]);

Object.entries(C).forEach(([name, hex], i) => {
  const x = 32 + (i % 4) * 176;
  const y = 96 + Math.floor(i / 4) * 104;
  rect(colors, x, y, 160, 56, hex, 8, "KIT/" + name);
  txt(colors, x, y + 62, name, 12, "700", C["text-primary"]);
  txt(colors, x, y + 80, hex, 11, "400", C["text-secondary"]);
});

const type = penpot.createBoard();
type.name = "KIT / Type";
type.resize(760, 580);
type.x = X0;
type.y = 490;
type.fills = solid(C.surface);
page.root.appendChild(type);
made++;
txt(type, 32, 28, "UM Copark  -  Typography", 24, "700", C["text-primary"]);
txt(type, 32, 62, "Inter  -  7 role", 12, "500", C["text-secondary"]);
let ty = 100;
for (const [role, size, weight, sample] of TOK.type) {
  txt(type, 32, ty, sample, size, weight, C["text-primary"]);
  txt(type, 32, ty + Math.max(size, 16) + 8, role + "  /  " + size + "px  /  " + weight, 11, "400", C["text-secondary"]);
  ty += Math.max(size, 16) + 52;
}

const rs = penpot.createBoard();
rs.name = "KIT / Radius & Space";
rs.resize(760, 320);
rs.x = X0;
rs.y = 1130;
rs.fills = solid(C.surface);
page.root.appendChild(rs);
made++;
txt(rs, 32, 28, "Radius & Spacing", 24, "700", C["text-primary"]);
Object.entries(TOK.rounded).forEach(([k, v], i) => {
  const x = 32 + i * 176;
  const d = k === "pill" ? 48 : 56;
  rect(rs, x, 92, 120, d, C["status-available"], v, "KIT/r-" + k);
  txt(rs, x, 92 + d + 10, k + "  " + v + "px", 11, "700", C["text-primary"]);
});
txt(rs, 32, 216, "Spacing scale", 13, "700", C["text-primary"]);
Object.entries(TOK.spacing).forEach(([k, v], i) => {
  const x = 32 + i * 116;
  rect(rs, x, 244, v, 34, C.primary, 4, "KIT/s-" + k);
  txt(rs, x, 284, k + " " + v, 10, "500", C["text-secondary"]);
});

// ── Wireframe: low fidelity, 7 flows, one row below the brand boards ─────
const G = "#d9dedb";
const GD = "#b4bcb8";
const GT = "#8a938f";
const W = 360;
const H = 800;
const GAP = 60;
const Y0 = 1540;

const wboard = (name, x) => {
  const b = penpot.createBoard();
  b.name = "WF / " + name;
  b.resize(W, H);
  b.x = x;
  b.y = Y0;
  b.fills = solid("#ffffff");
  page.root.appendChild(b);
  made++;
  return b;
};
const wbox = (p, x, y, w, h, fill, r, label) => {
  rect(p, x, y, w, h, fill, r, label ? "WF/" + label : "");
  if (label) txt(p, x + 8, y + 8, label, 10, "500", "#6b7570");
};
const wtext = (p, x, y, s, size, weight, fill) => txt(p, x, y, s, size, weight, fill);

const bar = (p) => {
  wbox(p, 0, 0, W, 92, GD, 0, "");
  wtext(p, 24, 22, "Judul layar", 16, "700", "#6b7570");
  wtext(p, 24, 50, "Subjudul konteks", 11, "400", GT);
};
const nav = (p, active) => {
  const y = H - 64;
  wbox(p, 0, y, W, 64, "#eff1f0", 0, "");
  ["Beranda", "Slot", "Riwayat", "Profil"].forEach((n, i) => {
    wtext(p, 20 + i * 86, y + 24, n, 10, active === i ? "700" : "400", active === i ? "#6b7570" : GT);
    if (active === i) wbox(p, 20 + i * 86, y + 44, 50, 3, GD, 2, "");
  });
};

let b = wboard("S01 Beranda", 0);
bar(b);
wbox(b, 16, 108, W - 32, 112, G, 12, "Statistik total");
wbox(b, 16, 236, W - 32, 76, G, 12, "Card gedung");
wbox(b, 16, 324, W - 32, 76, G, 12, "Card gedung");
wbox(b, 16, 412, W - 32, 84, G, 12, "Info udara");
nav(b, 0);

b = wboard("S02 Detail Gedung", W + GAP);
bar(b);
wbox(b, 16, 108, W - 32, 128, G, 12, "Kapasitas");
wbox(b, 16, 248, W - 32, 132, G, 12, "Grid slot");
wbox(b, 16, 396, W - 32, 96, G, 12, "Fasilitas");
wbox(b, 16, 508, W - 32, 52, GD, 12, "CTA");
nav(b, 1);

b = wboard("S03 Slot Terpilih", W * 2 + GAP * 2);
bar(b);
wbox(b, 16, 108, W - 32, 168, G, 12, "Slot terpilih");
wbox(b, 16, 292, W - 32, 176, G, 12, "Rincian biaya");
wbox(b, 16, 484, W - 32, 52, GD, 12, "CTA bayar");
wbox(b, 16, 548, W - 32, 44, "#eff1f0", 12, "Batal");
nav(b, 1);

b = wboard("S04 Navigasi", W * 3 + GAP * 3);
bar(b);
wbox(b, 16, 108, W - 32, 96, G, 16, "Jarak");
for (let i = 0; i < 4; i++) wbox(b, 16, 220 + i * 68, W - 32, 56, G, 12, "Langkah " + (i + 1));
nav(b, 1);

b = wboard("S05 Status Kosong", W * 4 + GAP * 4);
bar(b);
wbox(b, 16, 108, W - 32, 148, "#eff1f0", 12, "Empty state");
wbox(b, 16, 272, W - 32, 120, G, 12, "Rekomendasi");
wbox(b, 16, 408, W - 32, 152, G, 12, "Tips");
nav(b, 2);

b = wboard("S06 Error Sensor", W * 5 + GAP * 5);
bar(b);
wbox(b, 16, 108, W - 32, 176, "#e3e6e5", 12, "Error state");
wbox(b, 16, 300, W - 32, 52, GD, 12, "Coba lagi");
wbox(b, 16, 364, W - 32, 52, G, 12, "Pilih slot lain");
wbox(b, 16, 432, W - 32, 128, G, 12, "Bantuan");
nav(b, 1);

b = wboard("S07 Kualitas Udara", W * 6 + GAP * 6);
bar(b);
wbox(b, 16, 108, W - 32, 140, G, 16, "Indeks AQI");
for (let i = 0; i < 4; i++) {
  wbox(b, 16, 264 + i * 62, W - 32, 50, G, 12, "Gedung " + "ABCD"[i]);
  wbox(b, 32, 294 + i * 62, 120, 6, GD, 3, "");
}
wbox(b, 16, 524, W - 32, 100, G, 12, "Catatan");
nav(b, 0);

return {
  made,
  pageShapes: page.root.children.length,
  boards: page.root.children.map((b) => b.name),
};
`;

(async () => {
  const p = new Penpot();
  const { session } = await p.connect();
  const { msg } = await p.call(session, "execute_code", { code: CODE });
  console.log(JSON.stringify(msg.result.content, null, 1).slice(0, 3000));
})();