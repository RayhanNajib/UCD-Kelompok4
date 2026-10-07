---
version: alpha
name: UM EcoPark
description: Sistem informasi parkir kampus yang menjawab satu pertanyaan dalam tiga puluh detik.
colors:
  primary: "#0F6E3D"
  secondary: "#1B3A5C"
  accent: "#F2A71B"
  neutral: "#F7F8F6"
  surface: "#FFFFFF"
  text-primary: "#141A16"
  text-secondary: "#5A6560"
  status-available: "#15703C"
  status-limited: "#E8A317"
  status-full: "#C3352B"
  border: "#DCE3DD"
typography:
  display:
    fontFamily: Inter
    fontSize: 2rem
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "-0.02em"
  h1:
    fontFamily: Inter
    fontSize: 1.5rem
    fontWeight: 700
    lineHeight: 1.25
    letterSpacing: "-0.015em"
  h2:
    fontFamily: Inter
    fontSize: 1.125rem
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: "-0.01em"
  body-md:
    fontFamily: Inter
    fontSize: 1rem
    fontWeight: 400
    lineHeight: 1.5
  body-sm:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: 400
    lineHeight: 1.45
  caption:
    fontFamily: Inter
    fontSize: 0.75rem
    fontWeight: 500
    lineHeight: 1.4
  metric-lg:
    fontFamily: Inter
    fontSize: 3rem
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "-0.03em"
rounded:
  sm: 8px
  md: 12px
  lg: 16px
  pill: 999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  xxl: 48px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "#FFFFFF"
    typography: "{typography.h1}"
    rounded: "{rounded.md}"
    padding: 16px
  button-primary-hover:
    backgroundColor: "#0B552F"
    textColor: "#FFFFFF"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text-primary}"
    rounded: "{rounded.md}"
    padding: 16px
  slot-available:
    backgroundColor: "{colors.status-available}"
    textColor: "#FFFFFF"
    rounded: "{rounded.sm}"
  slot-limited:
    backgroundColor: "{colors.status-limited}"
    textColor: "#141A16"
    rounded: "{rounded.sm}"
  slot-full:
    backgroundColor: "{colors.status-full}"
    textColor: "#FFFFFF"
    rounded: "{rounded.sm}"
  card-building:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text-primary}"
    rounded: "{rounded.md}"
    padding: 16px
  card-building-border:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text-secondary}"
  chip-reminder:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.text-primary}"
    rounded: "{rounded.pill}"
    padding: 8px
  page-canvas:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.text-primary}"
  divider-line:
    backgroundColor: "{colors.border}"
    textColor: "{colors.text-secondary}"
  banner-error:
    backgroundColor: "#FDF2F1"
    textColor: "{colors.status-full}"
    rounded: "{rounded.md}"
    padding: 16px
---

## Overview

UM EcoPark adalah sistem informasi parkir untuk Universitas Negeri Malang. Satu
layar harus menjawab satu pertanyaan mendasar dalam waktu paling lama tiga
puluh detik: **di lantai berapa ada slot kosong, dan berapa lama saya perlu
menuju ke sana.**

Identitas visualnya bukankan "-" parser. Brand ini lahir dari dua hal yang
terbukti di lapangan: kampus yang menuntut ketepatan waktu, dan janji bahwa
mobilitas yang lebih baik menghasilkan udara yang lebih bersih. Karena itu
paletnya hijau untuk aksi dan keadaan, dan hanya satu aksen hangat untuk
menyorot hal yang harus dipakai sekarang, bukan nanti.

Arah baca yang diuji di lapangan adalah durasi, bukanportionalitas visual:
penggunaUM glanced sambil berjalan, bukan membaca./fonts kecil, kontras
tinggi, dan setiap statusbroadcast dapat dibaca dalam sekali lihat.

---

## Colors

**Primary - Deep Campus Green (#0F6E3D).** Warna aksi utama. Hijau dipilih karena
merujuk pada akuntabilitas dan campus hijau UM, bukan karena dekorasi. Dipakai
pada tombol, tautan, dan state aktif. Lahir dari UI GreenMetric 2024: UM berada
di peringkat 196 dunia dengan skor 8025, dan komponen Transportation (TR)
justru yang terlemah di 1575. Warna ini adalah pengingat bahwa Proposal ini
untuk menutup celah itu.

**Secondary - Slate Blue (#1B3A5C).** Struktur dan navigasi. Dipakai pada app
bar, header gedung, dan teks pembanding. Netral dan dingin supaya tidak
bersaing dengan hijau aksi.

**Accent - Amber (#F2A71B).** Satu warna hangat, disimpan khusus untuk
menyorot tindakan yang bersifat waktu-sensitif: tombol "Navigasi ke Slot" dan
pengingat pagi. Tidak boleh dipakai lebih dari satu kali per layar; kalau dua
tombol warna sama muncul bersamaan, salah satu keliru.

**Status trio - Hijau / Kuning / Merah.** Fondasi cara pengguna membaca
ketersediaan. Ini adalah bahasa visual paling penting di aplikasi:

| Token | Hex | Artinya | Contoh |
|---|---|---|---|
| `status-available` | #15703C | Lebih dari 10 slot kosong | Lantai 1 Rektorat |
| `status-limited` | #E8A317 | Terbatas, 1 sampai 10 slot | Lantai 2 Rektorat |
| `status-full` | #C3352B | Penuh, pindah gedung | FMIPA saat jam 08.00 |

Kuning memakai teks gelap (#141A16), bukan putih, karena kontras putih di atas
#E8A317 hanya 2,1:1 dan gagal WCAG AA. Merah dan hijau memakai teks putih.

---

## Typography

Inter untuk semua tingkat, karena bentuk hurufnya netral di ukuran kecil dan
memiliki tinggi-x yang konsisten sehingga baris status tidak terlihat bergoyang
saat angka berubah dari "3" menjadi "12".

**Skala thick-and-tight.** Display dan metrik memakai line-height rapat
(1,0 sampai 1,2) dan letter-spacing negatif karena angka besar menumpuk vertikal
dan ruang vertikal yang terbuang. Body copy memakai 1,5 karena itu ukuran baca
nyata di layar HP.

**Angka tabular untuk metrik.** Angka pada slot count, waktu, dan emisi memakai
fitur tabular sehingga nilainya tidak melompat saat berubah. Tanpa ini, papan
status berkedip setiap kali sensor mengirim angka baru.

**Caption untuk sumber data.** Setiap angka yang berasal dari sumber eksternal
menggunakan `caption` 12px dan warna `text-secondary`, karena angka riset
bukan angka yang dibuat aplikasi.

---

## Layout

Mobile-first dengan baseline 375px. Semua jarak mengikuti kelipatan 8; proyek ini
tidak punya layout desktop terpisah, melainkan tata letak yang sama dengan
kontainer yang melebar.

- **Konten** berhenti pada 480px pada layar lebar, dibaca sebagai kolom yang
  terpusat, bukan tabel yang melar.
- **Grid slot** memakai grid dengan `gap: 8px`, minimal lebar kolom 44px agar
  target sentuh mencapai standar 44px.
- **App bar** tinggi 56px, menempel di atas, tidak ikut menggulir.
- **Tombol utama** setinggi minimal 52px, penuh lebar pada layar HP.

---

## Elevation & Depth

Elevation dipakai untuk hal yang bisa ditekan, bukan untuk dekorasi. Hanya dua
ditekan, bukan untuk dekorasi. Hanya dua tingkat yang dipakai.

- **Level 0 - permukaan.** Kartu gedung dan baris slot. Tidak ada bayangan.
- **Level 1 - lapisan.** Sheet navigasi dan banner error, dengan
  `box-shadow: 0 8px 24px rgba(20, 26, 22, 0.12)`.

Tombol ditekan menggunakan perubahan warna latar, bukan bayangan, karena
bayangan di layar kecil berubah menjadi kabut visual.

---

## Shapes

Semua sudut 8px ke atas. Slot parkir memakai 8px, kartu 12px, sheet 16px.
Lingkaran penuh hanya untuk badge status berbentuk pill dan tombolstea.

Radius besar-besar pada elemen kecil membuat tampilan terasa moonya, dan
grid slot justru yang harus terbaca sebagai utilitas, bukan produk konsumen.

---

## Components

**Slot tile.** Unit atom dari sistem. Berisi nomor slot dan zona. Tiga varian
warna sesuai status trio. Semua slot satu ukuran, satu baseline-aligned, supaya
pengguna membandingkannya satu sama lain tanpa perlu membaca label.

**Building card.** Menampilkan nama gedung, status, dan jumlah slot tersisa.
Digunakan di beranda.-hover memberi outline primary 1px, bukan bayangan.

**Primary button - Navigasi ke Slot.** Tombol amber dengan teks gelap. Hanya
muncul setelah slot dipilih. TTY: Menempel di bawah layar, penuh lebar,
karena ini aksi yang dilakukan sambil berjalan.

**Status banner - Error.** Warna merah soft dengan ikon dan teks. Menyertakan
cap waktu data terakhir, karena-presentasi data basi lebih jujur daripada
menyembunyikannya. Dua jalan keluar selalu tersedia: Coba Lagi dan Lapor.

**Eco-metric card.** Angka besar, label kecil, dan satu baris metodologi. Tidak
boleh menampilkan emisi sebagai angka tanpa sumber rumus - estimate memakai
pendekatan Carbon Footprint UB 2024 dan harus disebut sebagai estimasi.

---

## Do's and Don'ts

**Do**
- Gunakan status trio sebagai satu-satunya cara menampilkan ketersediaan.
- Tampilkan cap waktu setiap kali data dianggap basi.
- Sebutkan sumber rumus di setiap angka emisi.
- Targetkan 44px untuk setiap target sentuh di grid slot.

**Don't**
- Jangan memakai warna lain untuk status; merahReserved untuk error juga, bukan
  untuk "penuh dengan prioritas", yang tetap Merah status penuh.
- Jangan menampilkan slot kosong tanpa menjelaskan berarti.Diagnostics.
- Jangan menambahkan tab "Lingkungan" terpisah; lingkungan adalah dimensi dari
  layar yang sama, bukan tujuan yang terpisah.
- Jangan menebak ketersediaan saat sensor tidak merespons.
