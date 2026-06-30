# Lab 01 — Anatomy of a Prompt (Konteks Jalin)

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

1. **Baca konteks** — situasi operasional di Jalin.
2. **Lihat output target** — contoh konkret jawaban "baik" yang harus didekati.
3. **Tahap A — Percobaan Mandiri**: Anda menulis prompt sendiri untuk mencoba menghasilkan output yang **mirip** dengan target. Jalankan di claude.ai, screenshot.
4. **Tahap B — Prompt Anatomi**: jalankan prompt referensi yang sudah disusun mengikuti template 5 komponen. Bandingkan hasilnya dengan Tahap A dan dengan output target.

---

## Use Case 1 — Balasan Keluhan Nasabah (Transaksi Gagal)

### 1.1 Konteks

Nasabah Bank A bernama **Bapak Andi** mengirim keluhan ke kanal CS Jalin pada **27 Juni 2026**:

> "Saya transfer Rp 5.000.000 ke rekening anak saya di Bank B via BI-FAST tanggal 24 Juni. Transaksi gagal, tapi saldo saya sudah terdebit. Sudah 3 hari belum kembali. Mohon segera diproses, ini untuk biaya sekolah."

Asumsi SOP internal Jalin (untuk keperluan latihan):

- SLA reversal transaksi BI-FAST gagal: **1×24 jam hingga 7 hari kerja**, tergantung verifikasi bank tujuan.
- CS officer **tidak diperbolehkan** menjanjikan tanggal pasti pengembalian dana atau kompensasi finansial di luar reversal nominal.
- Setiap balasan wajib mencantumkan **nomor tiket** (gunakan placeholder `[NO_TIKET]`) dan saluran eskalasi (`cs@jalin.co.id` / `1500-XXX`).

### 1.2 Output Target

Output "baik" untuk kasus ini memenuhi kriteria berikut:

- **Tone**: empatik namun profesional, panjang 100–150 kata.
- **Struktur**: pembuka (akui & minta maaf) → penjelasan SLA → langkah berikutnya → nomor tiket & kontak eskalasi → penutup.
- **Akurasi**: menyebut SLA 1×24 jam – 7 hari kerja, **tidak** menjanjikan kompensasi.
- **Format**: paragraf utuh siap-tempel (bukan bullet-point).

Contoh output target (referensi):

```
Yth. Bapak Andi,

Kami memohon maaf atas ketidaknyamanan yang Bapak alami terkait transfer
sebesar Rp 5.000.000 pada tanggal 24 Juni 2026 yang belum berhasil
dikembalikan. Kami memahami urgensi dana tersebut untuk keperluan biaya
sekolah putra/putri Bapak.

Berdasarkan SOP penanganan reversal BI-FAST, proses pengembalian dana
membutuhkan waktu 1×24 jam hingga 7 hari kerja tergantung verifikasi
dari bank tujuan. Tim kami telah mencatat keluhan Bapak dengan nomor
tiket [NO_TIKET] dan saat ini sedang melakukan koordinasi dengan
Bank B untuk mempercepat proses.

Untuk pembaruan status atau eskalasi, Bapak dapat menghubungi kami
melalui email cs@jalin.co.id atau hotline 1500-XXX dengan menyebutkan
nomor tiket di atas.

Hormat kami,
Tim Customer Service Jalin
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
Anda adalah CS Officer Jalin Pembayaran Nusantara.
</role>

<context>
Keluhan dari Bapak Andi, 27 Juni 2026:
"Saya transfer Rp 5.000.000 ke rekening anak saya di Bank B via BI-FAST
tanggal 24 Juni. Transaksi gagal, tapi saldo saya sudah terdebit. Sudah
3 hari belum kembali."

SLA reversal BI-FAST gagal: 1×24 jam – 7 hari kerja.
CS tidak boleh menjanjikan kompensasi.
</context>

<task>
Tulis balasan resmi untuk Bapak Andi.
</task>

<rules>
- Tone empatik & profesional, 100–150 kata, format paragraf.
- Sebut SLA 1×24 jam – 7 hari kerja.
- Sertakan nomor tiket [NO_TIKET] dan kontak cs@jalin.co.id / 1500-XXX.
- Jangan menjanjikan kompensasi.
</rules>

<output_format>
Balasan email dibuka "Yth. Bapak Andi," dan ditutup
"Hormat kami, Tim Customer Service Jalin".
</output_format>
```

</details>

Screenshot output dan simpan berdampingan dengan output Tahap A.

### 1.5 Perbandingan

Isi tabel berikut:

| Aspek                                 | Tahap A (Anda) | Tahap B (Anatomi) | Output Target |
|---------------------------------------|----------------|-------------------|---------------|
| Tone empatik & profesional            |                |                   | ✅             |
| Panjang 100–150 kata                  |                |                   | ✅             |
| Format paragraf (bukan bullet)        |                |                   | ✅             |
| Menyebut SLA 1×24 jam – 7 hari kerja  |                |                   | ✅             |
| Tidak menjanjikan kompensasi          |                |                   | ✅             |
| Menyertakan [NO_TIKET] + kontak       |                |                   | ✅             |

Tulis 2–3 kalimat refleksi: komponen mana di prompt Tahap A yang **hilang** sehingga outputnya menyimpang dari target?

---

## Use Case 2 — Klasifikasi Tiket Incident Sistem Pembayaran

### 2.1 Konteks

Tiket masuk ke sistem ITSM Jalin:

> "Transaksi tarik tunai di ATM Link Bank C gagal sejak pukul 22.00 kemarin,
> namun mesin tetap mengeluarkan struk dengan status SUKSES. Saldo nasabah
> terdebit. Sudah ada 47 keluhan dari beberapa cabang."

Asumsi taksonomi internal (untuk keperluan latihan):

| Kategori                          | Deskripsi singkat                                              |
|-----------------------------------|----------------------------------------------------------------|
| `ATM_DISPENSE_ERROR_FALSE_SUCCESS`| Uang tidak keluar tetapi sistem mencatat sukses.               |
| `ATM_NETWORK_TIMEOUT`             | Koneksi ke switch terputus saat transaksi.                     |
| `ATM_RECEIPT_PRINTER_ISSUE`       | Mesin gagal mencetak struk.                                    |
| `BIFAST_REVERSAL_DELAY`           | Reversal BI-FAST melewati SLA.                                 |
| `OTHER`                           | Tidak masuk kategori di atas.                                  |

Severity scale: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`.
Routing team: `ATM_OPS`, `NETWORK`, `BIFAST_OPS`, `MERCHANT_QRIS`.

### 2.2 Output Target

Output yang diharapkan adalah **JSON valid** dengan struktur:

```json
{
  "category": "ATM_DISPENSE_ERROR_FALSE_SUCCESS",
  "severity": "HIGH",
  "route_to": "ATM_OPS",
  "reasoning": "Mesin mencetak struk SUKSES padahal dispensing gagal, saldo nasabah terdebit, dan terdapat 47 keluhan multi-cabang dalam waktu singkat."
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
Anda adalah Incident Triage Engineer di tim ITSM Jalin.
</role>

<context>
Tiket:
"Transaksi tarik tunai di ATM Link Bank C gagal sejak pukul 22.00 kemarin,
namun mesin tetap mengeluarkan struk SUKSES. Saldo nasabah terdebit.
Ada 47 keluhan dari beberapa cabang."

Pilihan category: ATM_DISPENSE_ERROR_FALSE_SUCCESS, ATM_NETWORK_TIMEOUT,
ATM_RECEIPT_PRINTER_ISSUE, BIFAST_REVERSAL_DELAY, OTHER.
Pilihan severity: LOW, MEDIUM, HIGH, CRITICAL.
Pilihan route_to: ATM_OPS, NETWORK, BIFAST_OPS, MERCHANT_QRIS.
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

| Aspek                                  | Tahap A (Anda) | Tahap B (Anatomi) | Output Target |
|----------------------------------------|----------------|-------------------|---------------|
| Output adalah JSON valid               |                |                   | ✅             |
| `category` sesuai taksonomi (5 pilihan) |                |                   | ✅             |
| `severity` muncul & valid              |                |                   | ✅             |
| `route_to` muncul & valid              |                |                   | ✅             |
| `reasoning` ada & relevan              |                |                   | ✅             |

Tulis 2–3 kalimat refleksi: komponen mana di prompt Tahap A yang membuat output sulit diproses sistem otomatis?

---

## Use Case 3 — Email Pemberitahuan Maintenance Window

### 3.1 Konteks

Tim Network Operations Jalin akan melakukan maintenance pada **switch ATM Link** dengan rincian:

- **Jadwal**: Minggu, 5 Juli 2026, pukul **00.30 – 04.30 WIB** (4 jam).
- **Dampak**: Transaksi tarik tunai, transfer, dan cek saldo lintas-bank via ATM Link **tidak tersedia** selama jendela maintenance. Transaksi via BI-FAST dan QRIS tidak terdampak.
- **PIC eskalasi**: NOC Jalin, `noc@jalin.co.id`, hotline `+62-21-XXXXXXX` (24 jam).
- **Audiens**: bank peserta jaringan ATM Link (BNI, BRI, Mandiri, BTN, dan bank lainnya).

### 3.2 Output Target

Output "baik" adalah email berbahasa Indonesia formal yang memenuhi:

- **Struktur**: subjek email + salam + paragraf pembuka (tujuan) + tabel/blok detail (jadwal, dampak, layanan terdampak) + langkah antisipasi yang disarankan + kontak PIC + penutup.
- **Tone**: formal B2B, ringkas, tidak meminta maaf berlebihan.
- **Akurasi**: tanggal, jam, dan layanan terdampak sesuai konteks 3.1 — **tidak mengarang** layanan tambahan.
- **Format**: siap-tempel ke email client.

Contoh ringkas output target (referensi):

```
Subjek: [Pemberitahuan] Maintenance Switch ATM Link — Minggu, 5 Juli 2026

Yth. Bapak/Ibu Mitra Bank Peserta Jaringan ATM Link,

Bersama ini kami informasikan bahwa PT Jalin Pembayaran Nusantara akan
melakukan pemeliharaan terjadwal pada switch ATM Link dengan rincian:

- Jadwal     : Minggu, 5 Juli 2026, pukul 00.30 – 04.30 WIB
- Durasi     : 4 jam
- Dampak     : Layanan tarik tunai, transfer, dan cek saldo lintas-bank
               via ATM Link tidak tersedia selama jendela tersebut.
- Tidak terdampak : Transaksi BI-FAST dan QRIS.

Kami menyarankan Bapak/Ibu untuk menginformasikan kepada nasabah dan
menyiapkan kanal alternatif (mobile banking / BI-FAST) selama jendela
maintenance.

Untuk eskalasi dan koordinasi teknis, silakan menghubungi NOC Jalin
di noc@jalin.co.id atau +62-21-XXXXXXX (24 jam).

Hormat kami,
Tim Network Operations
PT Jalin Pembayaran Nusantara
```

### 3.3 Tahap A — Percobaan Mandiri

Tulis prompt versi Anda sendiri agar Claude menghasilkan email yang sedekat mungkin dengan target di 3.2. Jalankan di claude.ai (percakapan baru), screenshot, dan catat aspek yang menyimpang dari target.

### 3.4 Tahap B — Prompt Anatomi (Referensi)

> ⚠️ **Selesaikan Tahap A terlebih dahulu.** Buka prompt referensi di bawah hanya setelah Anda menjalankan percobaan mandiri.

<details>
<summary>👉 Klik untuk membuka Prompt Anatomi — Use Case 3</summary>

```text
<role>
Anda adalah Network Operations Lead di Jalin Pembayaran Nusantara.
</role>

<context>
Maintenance switch ATM Link:
- Jadwal: Minggu, 5 Juli 2026, 00.30 – 04.30 WIB (4 jam)
- Dampak: tarik tunai, transfer, cek saldo via ATM Link tidak tersedia
- Tidak terdampak: BI-FAST dan QRIS
- PIC: NOC Jalin — noc@jalin.co.id / +62-21-XXXXXXX

Audiens: bank peserta jaringan ATM Link.
</context>

<task>
Susun email pemberitahuan maintenance untuk bank peserta.
</task>

<rules>
- Tone formal B2B, ringkas.
- Sebut jadwal, dampak, dan layanan TIDAK terdampak.
- Sertakan saran kanal alternatif dan PIC NOC.
- Jangan tambahkan layanan yang tidak ada di context.
</rules>

<output_format>
Email lengkap dengan subjek, salam, isi, dan penutup
"Hormat kami, Tim Network Operations PT Jalin Pembayaran Nusantara".
</output_format>
```

</details>

### 3.5 Perbandingan

| Aspek                                                  | Tahap A (Anda) | Tahap B (Anatomi) | Output Target |
|--------------------------------------------------------|----------------|-------------------|---------------|
| Subjek email jelas & informatif                        |                |                   | ✅             |
| Tone formal B2B (tidak meminta maaf berlebihan)        |                |                   | ✅             |
| Menyebut jadwal, durasi, dampak                        |                |                   | ✅             |
| Menyebut layanan TIDAK terdampak (BI-FAST/QRIS)        |                |                   | ✅             |
| Tidak mengarang layanan tambahan                       |                |                   | ✅             |
| Menyertakan saran kanal alternatif                     |                |                   | ✅             |
| Menyertakan PIC eskalasi NOC                           |                |                   | ✅             |

Tulis 2–3 kalimat refleksi.

---

## Use Case 4 — Ringkasan Notulen Rapat Operasional Switching

### 4.1 Konteks

Berikut transkrip ringkas rapat operasional Network Switching Jalin tanggal **26 Juni 2026** (peserta: Andi — NOC Lead, Budi — Switching Engineer, Cindy — Product Ops, Dewi — Compliance):

```
Andi   : "Insiden kemarin malam, switch ATM Link sempat down 12 menit dari
         22.07 – 22.19. Failover ke node sekunder berjalan tapi terlambat
         3 menit dari SLA internal."
Budi   : "Root cause sementara: memory leak di service routing v2.4.1.
         Vendor sudah dihubungi, patch v2.4.2 dijadwalkan diuji minggu depan
         di staging."
Cindy  : "Dampak ke bank peserta: 47 keluhan masuk via CS, mayoritas dari
         Bank C. Tidak ada kerugian finansial nasabah karena reversal
         otomatis berhasil semua."
Dewi   : "Dari sisi compliance, insiden ini perlu dilaporkan ke BI dalam
         3×24 jam karena durasi melebihi 10 menit. Saya akan siapkan draft
         laporan, butuh data teknis dari Budi paling lambat besok sore."
Andi   : "Action items: (1) Budi siapkan data teknis sebelum 27 Juni 17.00,
         (2) Dewi finalisasi laporan BI sebelum 28 Juni 12.00, (3) saya
         koordinasi dengan vendor untuk percepatan patch v2.4.2."
Budi   : "Risiko terbuka: jika patch v2.4.2 tidak lulus QA staging, kita
         harus pertimbangkan rollback ke v2.3.8 yang stabil tapi tidak
         mendukung BI-FAST routing terbaru."
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
## Notulen Rapat Operasional Switching — 26 Juni 2026

**Peserta**: Andi (NOC Lead), Budi (Switching Engineer),
Cindy (Product Ops), Dewi (Compliance)

### Keputusan Utama
- Root cause insiden 25 Juni: memory leak service routing v2.4.1.
- Patch v2.4.2 akan diuji di staging minggu depan.
- Insiden wajib dilaporkan ke BI dalam 3×24 jam.

### Action Items
- [Budi] Siapkan data teknis insiden — deadline 27 Juni 17.00.
- [Dewi] Finalisasi draft laporan ke BI — deadline 28 Juni 12.00.
- [Andi] Koordinasi dengan vendor untuk percepatan patch v2.4.2 — tanpa deadline eksplisit.

### Risiko Terbuka
- Jika patch v2.4.2 tidak lulus QA staging, opsi rollback ke v2.3.8 berisiko karena tidak mendukung BI-FAST routing terbaru.
```

### 4.3 Tahap A — Percobaan Mandiri

Tulis prompt versi Anda sendiri agar Claude menghasilkan ringkasan yang sedekat mungkin dengan target di 4.2 (gunakan transkrip di 4.1 sebagai data). Jalankan di claude.ai (percakapan baru), screenshot, dan catat aspek yang menyimpang.

### 4.4 Tahap B — Prompt Anatomi (Referensi)

> ⚠️ **Selesaikan Tahap A terlebih dahulu.** Buka prompt referensi di bawah hanya setelah Anda menjalankan percobaan mandiri.

<details>
<summary>👉 Klik untuk membuka Prompt Anatomi — Use Case 4</summary>

```text
<role>
Anda adalah Notulis di tim Operations Jalin.
</role>

<context>
Transkrip rapat Network Switching, 26 Juni 2026:

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
Markdown dengan heading "## Notulen Rapat Operasional Switching — {tanggal}"
dan sub-bagian: Peserta, Keputusan Utama, Action Items, Risiko Terbuka.
</output_format>
```

</details>

### 4.5 Perbandingan

| Aspek                                              | Tahap A (Anda) | Tahap B (Anatomi) | Output Target |
|----------------------------------------------------|----------------|-------------------|---------------|
| Tanggal rapat ditulis eksplisit                    |                |                   | ✅             |
| Peserta + peran tercantum lengkap                  |                |                   | ✅             |
| Keputusan Utama ada                                |                |                   | ✅             |
| Action Items menyebut PIC + deadline               |                |                   | ✅             |
| Risiko Terbuka ada                                 |                |                   | ✅             |
| Tidak menambah informasi di luar transkrip         |                |                   | ✅             |
| Format markdown sesuai struktur output_format      |                |                   | ✅             |

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

| Use Case                              | Prompt Mandiri | Output Mandiri | Prompt Anatomi | Output Anatomi |
|---------------------------------------|----------------|----------------|----------------|----------------|
| 1 — Balasan Keluhan Nasabah           |                |                |                |                |
| 2 — Klasifikasi Tiket Incident        |                |                |                |                |
| 3 — Email Maintenance Window          |                |                |                |                |
| 4 — Ringkasan Notulen Rapat Switching |                |                |                |                |

Konvensi pengisian:

- **Prompt Mandiri / Prompt Anatomi**: tempel teks prompt lengkap (gunakan `Alt+Enter` di Google Sheets untuk multi-baris).
- **Output Mandiri / Output Anatomi**: tempel teks output dari claude.ai, atau tempel link screenshot jika output panjang.

---

## Catatan Penutup

Lab ini merupakan **fondasi paling penting** sepanjang pelatihan. Anatomi prompt yang dikuasai di sini akan dipakai berulang pada:

- **Module 3 (Day 1)** — Anda akan menambahkan teknik lanjutan (few-shot, chain-of-thought) di atas anatomi yang sama.
- **Module 4 (Day 2 — pembuka)** — Anda akan memperketat **Output Format** menjadi JSON yang valid dan dapat dievaluasi secara otomatis.
- **Day 2 dan seterusnya** — Saat menulis prompt untuk fitur AI di `fin-app` (Next.js + Supabase), anatomi yang sama akan menjadi struktur dasar dari setiap prompt yang Anda definisikan dalam kode.

Investasi waktu pada lab ini akan terasa manfaatnya selama 3 hari ke depan.
