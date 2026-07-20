# Lab 01 — Anatomy of a Prompt (Konteks BPJS Ketenagakerjaan)

**Modul**: Module 2 — Prompt Engineering Basics
**Durasi**: 60 menit (4 use case × ~15 menit)
**Mode**: Individual atau berpasangan (maks 2 orang)
**Tools**: claude.ai (free tier sudah memadai) + Google Spreadsheet
**Output**: Google Spreadsheet berisi pasangan prompt & output (mandiri vs anatomi) untuk 4 use case

---

## Tujuan

Setelah lab ini, Anda mampu:

1. Merasakan langsung kesulitan mendapatkan output yang spesifik tanpa struktur prompt yang jelas.
2. Melihat bagaimana template anatomi (Role, Context, Task, Constraint, Output Format) mempersempit jarak antara output model dan output yang Anda harapkan.
3. Memverifikasi peningkatan kualitas secara empiris melalui perbandingan di claude.ai.

---

## Prasyarat

- Telah mengikuti Module 1 (Introduction to LLM & Claude) dan Module 2 (Prompt Engineering Basics).
- Akun **claude.ai** aktif (free tier memadai).
- Editor teks lokal atau Google Docs untuk menyimpan hasil.

> ℹ️ **Catatan tool**: Lab ini sepenuhnya dapat dijalankan menggunakan **claude.ai gratis**.

---

## Alur Lab

Untuk setiap use case Anda akan menjalankan 4 tahap berikut:

1. **Baca konteks** — situasi operasional di BPJS Ketenagakerjaan.
2. **Lihat output target** — contoh konkret jawaban "baik" yang harus didekati.
3. **Tahap A — Percobaan Mandiri**: Anda menulis prompt sendiri untuk mencoba menghasilkan output yang **mirip** dengan target. Jalankan di claude.ai, screenshot.
4. **Tahap B — Prompt Anatomi**: jalankan prompt referensi yang sudah disusun mengikuti template 5 komponen. Bandingkan hasilnya dengan Tahap A dan dengan output target.

---

## Use Case 1 — Balasan Keluhan Peserta (Klaim JHT Terlambat)

### 1.1 Konteks

Peserta **Ibu Sari** mengirim keluhan via kanal CS BPJS Ketenagakerjaan pada **10 Juli 2026**:

> "Saya mengajukan klaim JHT sejak 1 Juli 2026. Semua dokumen sudah diunggah di aplikasi JMO dan dinyatakan lengkap. Sudah lebih dari 2 minggu belum ada konfirmasi pencairan. Dana ini saya butuhkan untuk modal usaha setelah resign."

Asumsi SOP BPJS Ketenagakerjaan (untuk keperluan latihan):

- SLA pemrosesan klaim JHT online via JMO: maksimal **5 hari kerja** setelah dokumen dinyatakan lengkap.
- CS tidak diperbolehkan menjanjikan tanggal pencairan atau kompensasi bunga.
- Setiap balasan wajib menyertakan **nomor tiket** (gunakan placeholder `[NO_TIKET]`) dan saluran eskalasi (`care@bpjsketenagakerjaan.go.id` / `175`).

### 1.2 Output Target

Output "baik" untuk kasus ini memenuhi kriteria berikut:

- **Tone**: empatik namun profesional, panjang 100–150 kata.
- **Struktur**: pembuka (akui & minta maaf) → penjelasan SLA → langkah berikutnya → nomor tiket & kontak eskalasi → penutup.
- **Akurasi**: menyebut SLA 5 hari kerja, **tidak** menjanjikan kompensasi.
- **Format**: paragraf utuh siap-tempel (bukan bullet-point).

Contoh output target (referensi):

```
Yth. Ibu Sari,

Kami mohon maaf atas ketidaknyamanan yang Ibu alami terkait proses
klaim Jaminan Hari Tua (JHT) yang diajukan sejak 1 Juli 2026. Kami
memahami pentingnya dana tersebut untuk keperluan modal usaha Ibu.

Berdasarkan SOP layanan klaim JHT online melalui aplikasi JMO,
proses verifikasi dan pencairan membutuhkan waktu maksimal 5 hari
kerja terhitung sejak dokumen dinyatakan lengkap. Tim kami telah
mencatat keluhan Ibu dengan nomor tiket [NO_TIKET] dan sedang
melakukan penelusuran status pengajuan Ibu secara prioritas.

Untuk pembaruan status atau eskalasi lebih lanjut, Ibu dapat
menghubungi kami melalui email care@bpjsketenagakerjaan.go.id
atau hotline 175 dengan menyebutkan nomor tiket di atas.

Hormat kami,
Tim Customer Care BPJS Ketenagakerjaan
```

### 1.3 Tahap A — Percobaan Mandiri

Tulis prompt **versi Anda sendiri** untuk meminta Claude menghasilkan balasan yang **sedekat mungkin** dengan output target di atas. Anda boleh menyalin konteks keluhan dan SOP ke dalam prompt.

Setelah prompt siap:

1. Jalankan di **claude.ai** (percakapan baru).
2. Screenshot output dan simpan.
3. Tandai bagian output yang **belum sesuai** dengan target (misalnya: terlalu panjang, menjanjikan kompensasi, format bullet, dsb.).

### 1.4 Tahap B — Prompt Anatomi (Referensi)

> ⚠️ **Selesaikan Tahap A terlebih dahulu.** Buka prompt referensi di bawah hanya setelah Anda menjalankan percobaan mandiri.

<details>
<summary>👉 Klik untuk membuka Prompt Anatomi — Use Case 1</summary>

Salin prompt berikut **apa adanya** ke claude.ai (percakapan baru), kemudian jalankan:

```text
<role>
Anda adalah Customer Care Officer BPJS Ketenagakerjaan.
</role>

<context>
Keluhan dari Ibu Sari, 10 Juli 2026:
"Saya mengajukan klaim JHT sejak 1 Juli 2026. Semua dokumen sudah
diunggah di JMO dan dinyatakan lengkap. Sudah lebih dari 2 minggu
belum ada konfirmasi pencairan. Dana ini untuk modal usaha setelah resign."

SLA klaim JHT online via JMO: maksimal 5 hari kerja sejak dokumen lengkap.
CS tidak boleh menjanjikan kompensasi atau tanggal pasti pencairan.
</context>

<task>
Tulis balasan resmi untuk Ibu Sari.
</task>

<rules>
- Tone empatik & profesional, 100–150 kata, format paragraf.
- Sebut SLA 5 hari kerja.
- Sertakan nomor tiket [NO_TIKET] dan kontak care@bpjsketenagakerjaan.go.id / 175.
- Jangan menjanjikan kompensasi atau tanggal pasti.
</rules>

<output_format>
Balasan dibuka "Yth. Ibu Sari," dan ditutup
"Hormat kami, Tim Customer Care BPJS Ketenagakerjaan".
</output_format>
```

</details>

Screenshot output dan simpan berdampingan dengan output Tahap A.

### 1.5 Perbandingan

Isi tabel berikut:

| Aspek | Tahap A (Anda) | Tahap B (Anatomi) | Output Target |
|-------|----------------|-------------------|---------------|
| Tone empatik & profesional | | | ✅ |
| Panjang 100–150 kata | | | ✅ |
| Format paragraf (bukan bullet) | | | ✅ |
| Menyebut SLA 5 hari kerja | | | ✅ |
| Tidak menjanjikan kompensasi/tanggal pasti | | | ✅ |
| Menyertakan [NO_TIKET] + kontak | | | ✅ |

Tulis 2–3 kalimat refleksi: komponen mana di prompt Tahap A yang **hilang** sehingga outputnya menyimpang dari target?

---

## Use Case 2 — Klasifikasi Tiket Layanan Peserta

### 2.1 Konteks

Tiket masuk ke helpdesk BPJS Ketenagakerjaan:

> "Peserta melaporkan bahwa nomor KPJ (Kartu Peserta Jamsostek) mereka tidak ditemukan saat mencoba mengakses saldo JHT di aplikasi JMO. Perusahaan pemberi kerja sudah mendaftarkan peserta sejak 3 tahun lalu dan iuran rutin dibayar setiap bulan."

Asumsi taksonomi internal (untuk keperluan latihan):

| Kategori | Deskripsi |
|----------|-----------|
| `DATA_PESERTA_TIDAK_DITEMUKAN` | Nomor KPJ/NIK tidak terdaftar atau tidak ditemukan di sistem |
| `KLAIM_JHT_DOKUMEN_TIDAK_LENGKAP` | Pengajuan klaim ditolak karena dokumen tidak memenuhi persyaratan |
| `KEPESERTAAN_TIDAK_AKTIF` | Status kepesertaan non-aktif karena iuran tidak dibayar |
| `APLIKASI_JMO_ERROR` | Gangguan teknis pada aplikasi Jamsostek Mobile |
| `OTHER` | Tidak masuk kategori di atas |

Severity scale: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`.
Routing team: `CS_ONLINE`, `DATA_MASTER`, `KLAIM_OPS`, `IT_SUPPORT`.

### 2.2 Output Target

Output yang diharapkan adalah **JSON valid** dengan struktur:

```json
{
  "category": "DATA_PESERTA_TIDAK_DITEMUKAN",
  "severity": "HIGH",
  "route_to": "DATA_MASTER",
  "reasoning": "Nomor KPJ tidak ditemukan di sistem meskipun kepesertaan sudah 3 tahun dan iuran rutin dibayar, mengindikasikan potensi masalah migrasi atau input data di sisi pemberi kerja."
}
```

### 2.3 Tahap A — Percobaan Mandiri

Tulis prompt versi Anda sendiri untuk mengklasifikasikan tiket di atas. Targetkan output yang mirip dengan JSON di 2.2.

Jalankan di claude.ai (percakapan baru), screenshot output, dan catat:

- Apakah output JSON valid?
- Apakah `category` sesuai taksonomi yang Anda inginkan? (Apakah Anda bahkan menyebut taksonomi di prompt Anda?)
- Apakah `severity` & `route_to` muncul?

### 2.4 Tahap B — Prompt Anatomi (Referensi)

> ⚠️ **Selesaikan Tahap A terlebih dahulu.** Buka prompt referensi di bawah hanya setelah Anda menjalankan percobaan mandiri.

<details>
<summary>👉 Klik untuk membuka Prompt Anatomi — Use Case 2</summary>

Salin prompt berikut ke claude.ai (percakapan baru):

```text
<role>
Anda adalah Helpdesk Triage Analyst di BPJS Ketenagakerjaan.
</role>

<context>
Tiket:
"Peserta melaporkan bahwa nomor KPJ mereka tidak ditemukan saat
mengakses saldo JHT di JMO. Perusahaan sudah mendaftarkan sejak
3 tahun lalu dan iuran rutin dibayar setiap bulan."

Pilihan category: DATA_PESERTA_TIDAK_DITEMUKAN, KLAIM_JHT_DOKUMEN_TIDAK_LENGKAP,
KEPESERTAAN_TIDAK_AKTIF, APLIKASI_JMO_ERROR, OTHER.
Pilihan severity: LOW, MEDIUM, HIGH, CRITICAL.
Pilihan route_to: CS_ONLINE, DATA_MASTER, KLAIM_OPS, IT_SUPPORT.
</context>

<task>
Klasifikasikan tiket dan tentukan severity + team penanganan.
</task>

<rules>
- category, severity, dan route_to WAJIB dari pilihan di atas.
- reasoning maksimum 1 kalimat.
</rules>

<output_format>
Kembalikan HANYA JSON, tanpa teks tambahan:
{
  "category": "...",
  "severity": "...",
  "route_to": "...",
  "reasoning": "..."
}
</output_format>
```

</details>

Screenshot output dan simpan berdampingan dengan Tahap A.

### 2.5 Perbandingan

| Aspek | Tahap A (Anda) | Tahap B (Anatomi) | Output Target |
|-------|----------------|-------------------|---------------|
| Output adalah JSON valid | | | ✅ |
| `category` sesuai taksonomi (5 pilihan) | | | ✅ |
| `severity` muncul & valid | | | ✅ |
| `route_to` muncul & valid | | | ✅ |
| `reasoning` ada & relevan | | | ✅ |

Tulis 2–3 kalimat refleksi: komponen mana di prompt Tahap A yang membuat output sulit diproses sistem otomatis?

---

## Use Case 3 — Email Pemberitahuan Maintenance SIPP Online

### 3.1 Konteks

Tim IT BPJS Ketenagakerjaan akan melakukan maintenance pada **SIPP Online (Sistem Informasi Pelaporan Peserta)**:

- **Jadwal**: Sabtu, 12 Juli 2026, pukul **23.00 – 03.00 WIB** (4 jam).
- **Dampak**: Pelaporan iuran, pendaftaran peserta baru, dan perubahan data peserta via SIPP Online **tidak tersedia** selama jendela maintenance. Layanan klaim via JMO dan pelayanan di kantor cabang tidak terdampak.
- **PIC eskalasi**: Helpdesk BPJS Ketenagakerjaan, `care@bpjsketenagakerjaan.go.id`, hotline `175` (24 jam).
- **Audiens**: perusahaan pemberi kerja (pengguna aktif SIPP Online).

### 3.2 Output Target

Output "baik" adalah email berbahasa Indonesia formal yang memenuhi:

- **Struktur**: subjek email + salam + paragraf pembuka (tujuan) + tabel/blok detail (jadwal, dampak, layanan terdampak) + langkah antisipasi yang disarankan + kontak PIC + penutup.
- **Tone**: formal B2B, ringkas, tidak meminta maaf berlebihan.
- **Akurasi**: tanggal, jam, dan layanan terdampak sesuai konteks 3.1 — **tidak mengarang** layanan tambahan.
- **Format**: siap-tempel ke email client.

Contoh ringkas output target (referensi):

```
Subjek: [Pemberitahuan] Maintenance SIPP Online — Sabtu, 12 Juli 2026

Yth. Bapak/Ibu Pimpinan Perusahaan Peserta BPJS Ketenagakerjaan,

Bersama ini kami informasikan bahwa BPJS Ketenagakerjaan akan melakukan
pemeliharaan terjadwal pada sistem SIPP Online dengan rincian:

- Jadwal      : Sabtu, 12 Juli 2026, pukul 23.00 – 03.00 WIB
- Durasi      : 4 jam
- Dampak      : Pelaporan iuran, pendaftaran peserta baru, dan perubahan
                data peserta via SIPP Online tidak tersedia selama jendela tersebut.
- Tidak terdampak : Layanan klaim via JMO dan pelayanan di kantor cabang.

Kami menyarankan Bapak/Ibu untuk menyelesaikan kebutuhan pelaporan iuran
sebelum pukul 23.00 WIB atau setelah pukul 03.00 WIB pada tanggal tersebut.

Untuk eskalasi dan informasi lebih lanjut, silakan menghubungi Helpdesk
BPJS Ketenagakerjaan di care@bpjsketenagakerjaan.go.id atau hotline 175 (24 jam).

Hormat kami,
Tim IT BPJS Ketenagakerjaan
```

### 3.3 Tahap A — Percobaan Mandiri

Tulis prompt versi Anda sendiri agar Claude menghasilkan email yang sedekat mungkin dengan target di 3.2. Jalankan di claude.ai (percakapan baru), screenshot, dan catat aspek yang menyimpang dari target.

### 3.4 Tahap B — Prompt Anatomi (Referensi)

> ⚠️ **Selesaikan Tahap A terlebih dahulu.** Buka prompt referensi di bawah hanya setelah Anda menjalankan percobaan mandiri.

<details>
<summary>👉 Klik untuk membuka Prompt Anatomi — Use Case 3</summary>

```text
<role>
Anda adalah IT Communications Officer di BPJS Ketenagakerjaan.
</role>

<context>
Maintenance SIPP Online:
- Jadwal: Sabtu, 12 Juli 2026, 23.00 – 03.00 WIB (4 jam)
- Dampak: pelaporan iuran, pendaftaran peserta baru, perubahan data via SIPP Online tidak tersedia
- Tidak terdampak: layanan klaim via JMO dan kantor cabang
- PIC: Helpdesk BPJS Ketenagakerjaan — care@bpjsketenagakerjaan.go.id / 175

Audiens: perusahaan pemberi kerja (pengguna aktif SIPP Online).
</context>

<task>
Susun email pemberitahuan maintenance untuk perusahaan pemberi kerja.
</task>

<rules>
- Tone formal B2B, ringkas.
- Sebut jadwal, dampak, dan layanan TIDAK terdampak.
- Sertakan saran penyelesaian pelaporan sebelum/sesudah jendela maintenance.
- Sertakan kontak Helpdesk.
- Jangan tambahkan layanan yang tidak ada di context.
</rules>

<output_format>
Email lengkap dengan subjek, salam, isi, dan penutup
"Hormat kami, Tim IT BPJS Ketenagakerjaan".
</output_format>
```

</details>

### 3.5 Perbandingan

| Aspek | Tahap A (Anda) | Tahap B (Anatomi) | Output Target |
|-------|----------------|-------------------|---------------|
| Subjek email jelas & informatif | | | ✅ |
| Tone formal B2B | | | ✅ |
| Menyebut jadwal, durasi, dampak | | | ✅ |
| Menyebut layanan TIDAK terdampak (JMO/cabang) | | | ✅ |
| Tidak mengarang layanan tambahan | | | ✅ |
| Saran waktu pelaporan alternatif | | | ✅ |
| Menyertakan kontak Helpdesk | | | ✅ |

Tulis 2–3 kalimat refleksi.

---

## Use Case 4 — Ringkasan Notulen Rapat Evaluasi Klaim JHT

### 4.1 Konteks

Berikut transkrip rapat evaluasi **18 Juli 2026** (peserta: Andi — Kepala Divisi Klaim, Budi — IT Support, Cindy — Customer Care, Dewi — Kepatuhan):

```
Andi   : "Sejak kebijakan pencairan JHT sebagian berlaku per 1 Juli, volume klaim
          masuk melonjak 340%. Sistem antrian di portal JMO sempat overload selama
          3 jam pada tanggal 3 Juli."
Budi   : "Root cause sementara: kapasitas server antrian klaim tidak diperbesar
          sebelum kebijakan efektif. Tim infrastruktur sedang mengajukan proposal
          peningkatan kapasitas, dijadwalkan selesai 25 Juli."
Cindy  : "Dari sisi Customer Care, ada 2.847 tiket masuk dalam 2 minggu pertama
          Juli, mayoritas pertanyaan status klaim. Rata-rata waktu respons naik
          dari 2 jam ke 6 jam."
Dewi   : "Untuk sisi kepatuhan, SLA 5 hari kerja harus tetap terpenuhi. Dari
          sampling 100 klaim, ada 12 yang melewati SLA — perlu dilaporkan ke
          manajemen paling lambat minggu ini."
Andi   : "Action items: (1) Budi selesaikan proposal infrastruktur sebelum 22 Juli
          pukul 17.00, (2) Dewi siapkan laporan deviasi SLA ke manajemen sebelum
          23 Juli pukul 12.00, (3) Cindy tambah resource CS sementara hingga
          volume klaim stabil."
Budi   : "Risiko terbuka: jika peningkatan kapasitas terlambat dari jadwal 25 Juli,
          potensi overload kedua pada puncak klaim akhir bulan."
```

### 4.2 Output Target

Output "baik" adalah ringkasan terstruktur dengan **5 bagian wajib**:

- **Tanggal Rapat**
- **Peserta** (nama + peran)
- **Keputusan Utama** (poin bullet)
- **Action Items** (PIC + deadline per item)
- **Risiko Terbuka** (poin bullet)

Contoh output target (referensi):

```markdown
## Notulen Rapat Evaluasi Klaim JHT — 18 Juli 2026

**Peserta**: Andi (Kepala Divisi Klaim), Budi (IT Support),
Cindy (Customer Care), Dewi (Kepatuhan)

### Keputusan Utama
- Volume klaim JHT melonjak 340% sejak kebijakan pencairan sebagian berlaku 1 Juli.
- Root cause overload: kapasitas server antrian tidak ditingkatkan sebelum kebijakan efektif.
- Terdapat 12 dari 100 klaim sampel yang melewati SLA 5 hari kerja — wajib dilaporkan ke manajemen.

### Action Items
- [Budi] Selesaikan proposal peningkatan kapasitas infrastruktur — deadline 22 Juli 17.00.
- [Dewi] Siapkan laporan deviasi SLA ke manajemen — deadline 23 Juli 12.00.
- [Cindy] Tambah resource CS sementara hingga volume klaim stabil — tanpa deadline eksplisit.

### Risiko Terbuka
- Jika peningkatan kapasitas terlambat dari jadwal 25 Juli, potensi overload kedua saat puncak klaim akhir bulan.
```

### 4.3 Tahap A — Percobaan Mandiri

Tulis prompt versi Anda sendiri agar Claude menghasilkan ringkasan yang sedekat mungkin dengan target di 4.2 (gunakan transkrip di 4.1 sebagai data). Jalankan di claude.ai (percakapan baru), screenshot, dan catat aspek yang menyimpang.

### 4.4 Tahap B — Prompt Anatomi (Referensi)

> ⚠️ **Selesaikan Tahap A terlebih dahulu.** Buka prompt referensi di bawah hanya setelah Anda menjalankan percobaan mandiri.

<details>
<summary>👉 Klik untuk membuka Prompt Anatomi — Use Case 4</summary>

```text
<role>
Anda adalah Notulis di tim Operasional BPJS Ketenagakerjaan.
</role>

<context>
Transkrip rapat Evaluasi Klaim JHT, 18 Juli 2026:

"""
[tempel transkrip dari bagian 4.1 di sini]
"""
</context>

<task>
Susun notulen ringkas dengan bagian: Tanggal, Peserta, Keputusan Utama,
Action Items, Risiko Terbuka.
</task>

<rules>
- Action Items wajib menyebut PIC dan deadline jika ada.
- Jangan tambahkan informasi di luar transkrip.
</rules>

<output_format>
Markdown dengan heading "## Notulen Rapat Evaluasi Klaim JHT — {tanggal}"
dan sub-bagian: Peserta, Keputusan Utama, Action Items, Risiko Terbuka.
</output_format>
```

</details>

### 4.5 Perbandingan

| Aspek | Tahap A (Anda) | Tahap B (Anatomi) | Output Target |
|-------|----------------|-------------------|---------------|
| Tanggal rapat ditulis eksplisit | | | ✅ |
| Peserta + peran tercantum lengkap | | | ✅ |
| Keputusan Utama ada | | | ✅ |
| Action Items menyebut PIC + deadline | | | ✅ |
| Risiko Terbuka ada | | | ✅ |
| Tidak menambah informasi di luar transkrip | | | ✅ |
| Format markdown sesuai struktur output_format | | | ✅ |

Tulis 2–3 kalimat refleksi.

---

## Kriteria Selesai (Definition of Done)

- [ ] Keempat use case (1, 2, 3, 4) sudah dikerjakan dalam dua tahap (mandiri & anatomi).
- [ ] Screenshot atau output tersimpan untuk Tahap A dan Tahap B di setiap use case.
- [ ] Tabel perbandingan terisi untuk keempat use case.
- [ ] Refleksi singkat (2–3 kalimat) ditulis untuk setiap use case.

---

## Tips Penting

- **Jalankan setiap percobaan pada percakapan baru** di claude.ai agar perbandingan adil.
- **Gunakan XML tags** (`<context>`, `<task>`, `<rules>`, dsb.) untuk memisahkan instruksi dari data — Claude dilatih untuk memperhatikan struktur ini.
- **Tulis prompt dalam Bahasa Indonesia** jika audiens lokal. Claude memiliki kemampuan bilingual yang sangat baik.
- Jika output JSON pada Use Case 2 sesekali tidak konsisten, hal tersebut wajar — topik tersebut akan dibahas mendalam pada Module 4 (Structured Output).
- Tujuan lab adalah melatih **kerangka berpikir**, bukan mendapatkan output yang persis identik dengan target.

---

## Deliverable — Google Spreadsheet

Seluruh hasil lab disimpan dalam **satu Google Spreadsheet** per peserta. Setelah selesai, atur sharing menjadi **"Anyone with the link — Viewer"** lalu kirim tautannya ke channel pelatihan.

Template kolom (header pada baris 1, satu baris per use case):

| Use Case | Prompt Mandiri | Output Mandiri | Prompt Anatomi | Output Anatomi |
|----------|----------------|----------------|----------------|----------------|
| 1 — Balasan Keluhan Peserta (Klaim JHT) | | | | |
| 2 — Klasifikasi Tiket Layanan Peserta | | | | |
| 3 — Email Maintenance SIPP Online | | | | |
| 4 — Ringkasan Notulen Rapat Evaluasi Klaim JHT | | | | |

Konvensi pengisian:

- **Prompt Mandiri / Prompt Anatomi**: tempel teks prompt lengkap (gunakan `Alt+Enter` di Google Sheets untuk multi-baris).
- **Output Mandiri / Output Anatomi**: tempel teks output dari claude.ai, atau tempel link screenshot jika output panjang.

---

## Catatan Penutup

Lab ini merupakan **fondasi paling penting** sepanjang pelatihan. Anatomi prompt yang dikuasai di sini akan dipakai berulang pada:

- **Module 3 (Day 1)** — Anda akan menambahkan teknik lanjutan (few-shot, chain-of-thought) di atas anatomi yang sama.
- **Module 4 (Day 2 — pembuka)** — Anda akan memperketat **Output Format** menjadi JSON yang valid dan dapat dievaluasi secara otomatis.
- **Day 2 dan seterusnya** — Saat menulis prompt untuk fitur AI di `fin-app` (Next.js + Supabase), anatomi yang sama akan menjadi struktur dasar dari setiap prompt yang Anda definisikan dalam kode.

Use case BPJS Ketenagakerjaan yang dipakai di lab ini — balasan keluhan peserta, klasifikasi tiket, pemberitahuan maintenance, dan notulen rapat — mencerminkan skenario nyata yang dapat langsung diadaptasi untuk kebutuhan operasional sehari-hari.

Investasi waktu pada lab ini akan terasa manfaatnya selama 3 hari ke depan.
