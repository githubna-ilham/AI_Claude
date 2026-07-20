# Lab 02 — Zero-Shot, Few-Shot, Chain-of-Thought

**Modul**: Module 3 — Prompting Techniques
**Durasi**: 45 menit (3 task × ~15 menit)
**Mode**: Individual
**Tools**: **Anthropic Console — Workbench** (https://console.anthropic.com/workbench) + Google Spreadsheet
**Output**: Spreadsheet berisi output 3 teknik × 3 task + insight singkat per task

---

## Tujuan

Setelah lab ini Anda mampu:

1. Membandingkan akurasi 3 teknik prompting (zero-shot, few-shot, CoT) pada task yang identik.
2. Memilih teknik yang tepat untuk masing-masing task berdasarkan data, bukan opini.
3. Mengidentifikasi kapan CoT membantu dan kapan justru menjadi overhead yang tidak perlu.

---

## Prasyarat

- Telah menyelesaikan Module 3 (materi).
- Akun **Anthropic Console** pribadi aktif (https://console.anthropic.com).
- Anda telah menerima undangan untuk bergabung ke **Workspace pelatihan BPJS Ketenagakerjaan** yang disiapkan fasilitator. Seluruh usage Workbench selama lab ini akan otomatis ditagihkan ke billing pelatihan.
- Google Spreadsheet kosong untuk mencatat hasil.

> ℹ️ **Mengapa Workbench, bukan claude.ai?** Lab 02 memerlukan parameter **`temperature=0`** agar hasil eksperimen reproducible — output yang sama setiap kali prompt dijalankan ulang. claude.ai tidak mengekspos parameter `temperature`, sedangkan Workbench memberikan kontrol penuh. Hal ini krusial saat membandingkan kualitas zero-shot vs few-shot vs CoT secara objektif.

---

## Setup Workbench (3 menit)

1. Login ke https://console.anthropic.com.
2. Pada dropdown **workspace** (pojok kanan atas), pilih workspace pelatihan yang diinformasikan fasilitator.
3. Buka tab **Workbench** dari sidebar kiri.
4. Pada panel kanan, set:
   - **Model**: `claude-sonnet-4-5`
   - **Temperature**: `0`
   - **Max tokens**: `1024`
5. Kosongkan **System Prompt**. Seluruh prompt lab ini ditempel ke kolom **User**.
6. Setiap klik **Run** = 1 API call = memotong saldo workspace pelatihan. Susun draft prompt di editor teks dulu, baru tempel ke Workbench saat siap dieksekusi.

---

## Task 1 — Klasifikasi Sentimen Komentar Peserta BPJS

### 1.1 Dataset

Klasifikasikan ke `POSITIF`, `NEGATIF`, atau `NETRAL`.

```
S1: "Klaim JHT saya cair dalam 3 hari kerja setelah dokumen lengkap, pelayanannya cepat dan responsif!"
S2: "Sudah 2 minggu dokumen lengkap tapi klaim belum diproses, sudah hubungi 175 berkali-kali tidak ada solusi."
S3: "Proses pendaftaran peserta baru di SIPP sekarang sudah bisa online, tidak perlu datang ke kantor seperti dulu."
S4: "Awalnya semangat pakai JMO karena katanya mudah, tapi fitur verifikasi wajah selalu gagal di HP saya."
S5: "Wah mantap, appnya crash tiap hari tapi iuran tetap dipotong rutin, profesional sekali!"
```

**Ground truth** (untuk self-check):
S1 POSITIF | S2 NEGATIF | S3 NETRAL | S4 NEGATIF (mixed letdown) | S5 NEGATIF (sarkasme).

### 1.2 Prompt Templates

Jalankan ketiga template berikut untuk S1–S5. Ganti `{kalimat}` dengan tiap sampel.

<details>
<summary>👉 Zero-Shot Template</summary>

```text
Klasifikasikan sentimen kalimat berikut sebagai POSITIF, NEGATIF, atau NETRAL.

Kalimat: "{kalimat}"
Sentimen:
```

</details>

<details>
<summary>👉 Few-Shot Template</summary>

```text
Klasifikasikan sentimen kalimat sebagai POSITIF, NEGATIF, atau NETRAL.

<example>
Kalimat: "Klaim JKK saya diproses cepat, dokter yang ditunjuk juga profesional."
Sentimen: POSITIF
</example>
<example>
Kalimat: "Data saya salah di sistem BPJS, sudah lapor 3 kali tapi tidak diperbaiki juga."
Sentimen: NEGATIF
</example>
<example>
Kalimat: "Kantor cabang BPJS buka sesuai jam operasional yang tertera di website."
Sentimen: NETRAL
</example>
<example>
Kalimat: "Wah hebat ya, saldo JHT tidak bisa dilihat padahal iuran rajin dibayar /sarcasm"
Sentimen: NEGATIF
</example>

Kalimat: "{kalimat}"
Sentimen:
```

</details>

<details>
<summary>👉 Chain-of-Thought Template</summary>

```text
Klasifikasikan sentimen kalimat sebagai POSITIF, NEGATIF, atau NETRAL.

Langkah berpikir:
1. Identifikasi kata kunci sentimen.
2. Periksa indikator sarkasme (/sarc, kontras berlebihan, konteks yang tidak masuk akal).
3. Tentukan polaritas dominan.
4. Beri label.

<thinking>
{tulis langkah di sini}
</thinking>

<answer>
Sentimen: {LABEL}
</answer>

Kalimat: "{kalimat}"
```

</details>

### 1.3 Spreadsheet Task 1

| Sampel | Ground Truth | Output Zero-Shot | Z benar? | Output Few-Shot | F benar? | Output CoT | CoT benar? |
|--------|--------------|------------------|----------|-----------------|----------|------------|------------|
| S1     | POSITIF      |                  |          |                 |          |            |            |
| S2     | NEGATIF      |                  |          |                 |          |            |            |
| S3     | NETRAL       |                  |          |                 |          |            |            |
| S4     | NEGATIF      |                  |          |                 |          |            |            |
| S5     | NEGATIF      |                  |          |                 |          |            |            |
| **Akurasi (%)** | —    |                  |          |                 |          |            |            |

### 1.4 Insight Task 1

Tulis 1–2 kalimat: teknik mana yang paling akurat, dan mengapa?

---

## Task 2 — Perhitungan Iuran BPJS Ketenagakerjaan

### 2.1 Dataset

```
M1: Sebuah perusahaan memiliki karyawan dengan upah Rp 8.000.000/bulan
(gaji pokok + tunjangan tetap). Tingkat risiko pekerjaan: menengah (JKK 0,54%).
Hitung total iuran yang ditanggung pemberi kerja per bulan:
- JHT pemberi kerja: 3,7%
- JKK: 0,54%
- JKM: 0,3%
- JP pemberi kerja: 2% (upah aktual, karena di bawah batas maks Rp 9.559.600)

M2: Seorang peserta JHT berencana mencairkan sebagian saldo untuk keperluan
perumahan. Saldo JHT saat ini: Rp 45.000.000. Ketentuan: pencairan sebagian
maksimal 30% dari saldo. Dari nominal yang dicairkan, dikenakan pajak 5%
(masa kepesertaan ≥ 10 tahun). Berapa nominal bersih yang diterima peserta?

M3: Tim IT BPJS punya 5 task untuk migrasi sistem SIPP. Task A (persiapan data)
& B (konfigurasi server) masing-masing 3 hari, dapat dikerjakan paralel.
Task C (migrasi database) butuh A & B selesai dulu, durasi 2 hari.
Task D (testing UAT) & E (training operator) masing-masing 4 hari dan
dapat dikerjakan paralel setelah C selesai.
Berapa total waktu minimum proyek?
```

**Ground truth** (untuk self-check):
- **M1**: JHT = 3,7% × 8.000.000 = 296.000; JKK = 0,54% × 8.000.000 = 43.200; JKM = 0,3% × 8.000.000 = 24.000; JP = 2% × 8.000.000 = 160.000; Total = **Rp 523.200**.
- **M2**: Pencairan maks = 30% × 45.000.000 = 13.500.000; Pajak = 5% × 13.500.000 = 675.000; Diterima = **Rp 12.825.000**.
- **M3**: Total waktu minimum = **9 hari** (A & B paralel 3 hari → C 2 hari → D & E paralel 4 hari).

### 2.2 Prompt Templates

Ganti `{soal}` dengan teks M1, M2, atau M3.

<details>
<summary>👉 Zero-Shot Template</summary>

```text
Selesaikan soal berikut. Berikan jawaban akhirnya secara singkat.

Soal: "{soal}"
Jawaban:
```

</details>

<details>
<summary>👉 Few-Shot Template</summary>

```text
Selesaikan soal berikut. Berikan jawaban akhirnya secara singkat.

<example>
Soal: "Seorang karyawan dengan upah Rp 5.000.000/bulan. Hitung iuran JHT pekerja (2%) per bulan."
Jawaban: Iuran JHT pekerja = 2% × 5.000.000 = Rp 100.000 per bulan.
</example>
<example>
Soal: "Perusahaan A membayar iuran JP untuk karyawan dengan upah Rp 12.000.000/bulan. Tarif JP pemberi kerja 2%, batas upah JP Rp 9.559.600. Berapa iuran JP yang dibayar?"
Jawaban: Upah digunakan = min(12.000.000, 9.559.600) = 9.559.600. Iuran JP = 2% × 9.559.600 = Rp 191.192.
</example>

Soal: "{soal}"
Jawaban:
```

</details>

<details>
<summary>👉 Chain-of-Thought Template</summary>

```text
Selesaikan soal berikut. Pikirkan langkah demi langkah.

Langkah berpikir:
1. Identifikasi data yang diketahui dari soal.
2. Tentukan rumus atau metode yang relevan.
3. Lakukan perhitungan satu per satu, tulis hasil tiap langkah.
4. Simpulkan jawaban akhir dengan satuan yang sesuai.

<thinking>
{tulis langkah perhitungan di sini}
</thinking>

<answer>
Jawaban: {jawaban akhir}
</answer>

Soal: "{soal}"
```

</details>

### 2.3 Spreadsheet Task 2

| Sampel | Ground Truth | Output Zero-Shot | Z benar? | Output Few-Shot | F benar? | Output CoT | CoT benar? |
|--------|--------------|------------------|----------|-----------------|----------|------------|------------|
| M1     | Rp 523.200   |                  |          |                 |          |            |            |
| M2     | Rp 12.825.000 |                 |          |                 |          |            |            |
| M3     | 9 hari       |                  |          |                 |          |            |            |
| **Akurasi (%)** | —    |                  |          |                 |          |            |            |

### 2.4 Insight Task 2

Tulis 1–2 kalimat: pada soal mana CoT memberikan keunggulan paling nyata? Mengapa?

---

## Task 3 — Klasifikasi Tiket Layanan BPJS Ketenagakerjaan

### 3.1 Dataset

Klasifikasikan tiket ke salah satu kategori berikut:

| Kategori | Deskripsi |
|----------|-----------|
| `DATA_PESERTA_TIDAK_DITEMUKAN` | Nomor KPJ/NIK tidak terdaftar atau tidak ditemukan di sistem |
| `KLAIM_JHT_DOKUMEN_TIDAK_LENGKAP` | Pengajuan klaim ditolak karena dokumen tidak memenuhi persyaratan |
| `KEPESERTAAN_TIDAK_AKTIF` | Status kepesertaan non-aktif karena iuran tidak dibayar |
| `APLIKASI_JMO_ERROR` | Gangguan teknis pada aplikasi Jamsostek Mobile |
| `OTHER` | Tidak masuk kategori di atas |

```
T1: "Peserta mencoba login JMO tapi selalu muncul notifikasi 'NIK tidak terdaftar',
     padahal perusahaan sudah mendaftarkan 3 tahun lalu dan iuran rutin dibayar."

T2: "Pengajuan klaim JHT peserta ditolak sistem dengan keterangan dokumen tidak
     lengkap — peserta merasa sudah mengunggah semua persyaratan yang diminta."

T3: "Notifikasi dari sistem bahwa kepesertaan peserta berstatus non-aktif karena
     iuran bulan April–Juni belum dibayarkan oleh perusahaan pemberi kerja."

T4: "Aplikasi JMO peserta crash setiap kali membuka menu 'Lihat Saldo JHT'
     sejak pembaruan ke versi terbaru."

T5: "Peserta ingin mengganti nomor rekening bank tujuan pencairan JHT."
```

**Ground truth** (untuk self-check):
T1 `DATA_PESERTA_TIDAK_DITEMUKAN` | T2 `KLAIM_JHT_DOKUMEN_TIDAK_LENGKAP` | T3 `KEPESERTAAN_TIDAK_AKTIF` | T4 `APLIKASI_JMO_ERROR` | T5 `OTHER`.

### 3.2 Prompt Templates

Ganti `{tiket}` dengan T1–T5.

<details>
<summary>👉 Zero-Shot Template</summary>

```text
Klasifikasikan tiket berikut ke salah satu kategori:
DATA_PESERTA_TIDAK_DITEMUKAN, KLAIM_JHT_DOKUMEN_TIDAK_LENGKAP,
KEPESERTAAN_TIDAK_AKTIF, APLIKASI_JMO_ERROR, OTHER.

Tiket: "{tiket}"
Kategori:
```

</details>

<details>
<summary>👉 Few-Shot Template</summary>

```text
Klasifikasikan tiket berikut ke salah satu kategori:
DATA_PESERTA_TIDAK_DITEMUKAN, KLAIM_JHT_DOKUMEN_TIDAK_LENGKAP,
KEPESERTAAN_TIDAK_AKTIF, APLIKASI_JMO_ERROR, OTHER.

<example>
Tiket: "Peserta mendaftar JHT tahun lalu tapi namanya tidak muncul di portal SIPP."
Kategori: DATA_PESERTA_TIDAK_DITEMUKAN
</example>
<example>
Tiket: "Dana JHT peserta belum cair meski 10 hari sejak pengajuan, padahal dokumen sudah lengkap."
Kategori: KLAIM_JHT_DOKUMEN_TIDAK_LENGKAP
</example>
<example>
Tiket: "Iuran bulan Maret tidak terbayar oleh HRD, kepesertaan kini non-aktif."
Kategori: KEPESERTAAN_TIDAK_AKTIF
</example>

Tiket: "{tiket}"
Kategori:
```

</details>

<details>
<summary>👉 Chain-of-Thought Template</summary>

```text
Klasifikasikan tiket berikut ke salah satu kategori:
DATA_PESERTA_TIDAK_DITEMUKAN, KLAIM_JHT_DOKUMEN_TIDAK_LENGKAP,
KEPESERTAAN_TIDAK_AKTIF, APLIKASI_JMO_ERROR, OTHER.

Langkah berpikir:
1. Identifikasi gejala utama dari tiket (apa yang gagal? di mana?).
2. Cocokkan gejala dengan deskripsi tiap kategori.
3. Pilih kategori yang paling sesuai. Jika tidak ada yang cocok, pilih OTHER.

<thinking>
{tulis langkah di sini}
</thinking>

<answer>
Kategori: {LABEL}
</answer>

Tiket: "{tiket}"
```

</details>

### 3.3 Spreadsheet Task 3

| Sampel | Ground Truth | Output Zero-Shot | Z benar? | Output Few-Shot | F benar? | Output CoT | CoT benar? |
|--------|--------------|------------------|----------|-----------------|----------|------------|------------|
| T1     | DATA_PESERTA_TIDAK_DITEMUKAN |  |  |  |  |  |  |
| T2     | KLAIM_JHT_DOKUMEN_TIDAK_LENGKAP |  |  |  |  |  |  |
| T3     | KEPESERTAAN_TIDAK_AKTIF |  |  |  |  |  |  |
| T4     | APLIKASI_JMO_ERROR |  |  |  |  |  |  |
| T5     | OTHER |  |  |  |  |  |  |
| **Akurasi (%)** | — |  |  |  |  |  |  |

### 3.4 Insight Task 3

Tulis 1–2 kalimat: apakah few-shot sudah cukup untuk task taxonomy-driven seperti ini, atau CoT masih memberi nilai tambah?

---

## Insight Akhir (5 menit)

Setelah ketiga task selesai, tulis 3–5 bullet menjawab:

- Pada task mana zero-shot sudah memadai? Mengapa few-shot tidak memberi gain berarti?
- Pada task mana CoT memberikan keunggulan paling nyata?
- Adakah task di mana CoT justru memperburuk output (over-reasoning, langkah halusinasi)?
- Untuk masing-masing 3 task, teknik mana yang akan Anda pilih untuk produksi? Dengan alasan apa?

---

## Kriteria Selesai (Definition of Done)

- [ ] 3 task × 3 teknik = 9 kombinasi telah dijalankan di Workbench.
- [ ] Spreadsheet evaluasi terisi untuk seluruh sampel di setiap task (5 + 3 + 5 = 13 baris × 3 teknik).
- [ ] Akurasi per teknik per task dihitung (gunakan `=COUNTIF` di Google Sheets).
- [ ] Insight per task ditulis (1–2 kalimat tiap task).
- [ ] Insight akhir (3–5 bullet) ditulis.

---

## Tips

- Dengan `temperature=0`, output yang sama akan keluar setiap kali Anda klik Run — manfaatkan untuk eksperimen reproducible.
- Pada Task 1 S5 (sarkasme) dan Task 2 M3 (project scheduling dengan dependensi paralel), CoT sangat membantu apabila langkah berpikir dirumuskan secara eksplisit.
- Simpan prompt yang berhasil di Workbench (tombol **Save** di kanan atas) agar dapat dimuat ulang tanpa menulis ulang.
- Jika output inkonsisten meskipun `temperature=0`, biasanya **prompt-nya yang ambigu** — bukan modelnya. Perketat instruksi sebelum berpindah ke model yang lebih mahal.

---

## Deliverable

Satu Google Spreadsheet berisi 3 sheet (Task 1, Task 2, Task 3) sesuai template di atas + 1 sheet "Insight Akhir". Atur sharing ke **"Anyone with the link — Viewer"**, kirim tautannya ke channel pelatihan.
