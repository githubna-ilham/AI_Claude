# Lab 02 — Zero-Shot, Few-Shot, Chain-of-Thought

**Modul**: Module 3 — Prompting Techniques
**Durasi**: 45 menit
**Mode**: Individual; peer comparison di 5 menit terakhir.
**Tools**: claude.ai (Sonnet 4.x) atau Anthropic Console — Workbench (set `temperature=0` untuk konsistensi).
**Output**: tabel evaluasi 3 teknik × 3 task + insight 3-5 bullet.

---

## Tujuan

Peserta mampu:
1. Membandingkan akurasi, latency persepsi, dan token usage dari 3 teknik prompting pada task identik.
2. Memilih teknik yang tepat untuk masing-masing task berdasarkan data, bukan opini.
3. Mengidentifikasi kapan CoT membantu, dan kapan menjadi overhead yang tidak perlu.

---

## Prasyarat

- Telah menyelesaikan Module 3 (materi & demo).
- Akun claude.ai aktif. Dianjurkan Console Workbench karena dapat set `temperature=0`.
- Spreadsheet atau tabel kosong untuk mencatat hasil.

---

## Dataset Lab

### Task 1 — Klasifikasi Sentimen (5 sampel)

Klasifikasikan ke `POSITIF`, `NEGATIF`, `NETRAL`.

```
S1: "Aplikasi makin enak dipakai setelah update."
S2: "Customer service-nya jutek banget, males balik."
S3: "Pengiriman tepat waktu, sesuai jadwal."
S4: "Awalnya excited tapi ternyata fiturnya minim banget."
S5: "Mantap jiwa nih layanannya /sarcasm"
```

**Ground truth** (untuk evaluasi sendiri di akhir):
S1: POSITIF, S2: NEGATIF, S3: NETRAL, S4: NEGATIF, S5: NEGATIF (sarkasme).

### Task 2 — Ekstraksi Entitas (3 sampel)

Ekstrak `person`, `organization`, `location`, `date` dari kalimat berita.

```
E1: "Pada 12 Maret 2024, Direktur Utama PT Bank Mandiri Darmawan Junaidi mengumumkan dividen di Jakarta."
E2: "Yusuf Hadi, peneliti BRIN, mempresentasikan riset di Bandung pada Kamis lalu."
E3: "Kementerian Komunikasi merilis peraturan baru bulan depan di Jakarta — diumumkan Menteri Budi Arie."
```

### Task 3 — Reasoning Matematika (3 sampel)

```
M1: Sebuah toko menjual 4 jenis produk:
- Kaos: 120 unit @ Rp 75.000
- Celana: 80 unit @ Rp 150.000
- Topi: 200 unit @ Rp 35.000
- Sepatu: 50 unit @ Rp 250.000
Berapa total revenue, dan produk apa yang revenue-nya paling besar?

M2: Andi pinjam 5 juta dengan bunga sederhana 12% per tahun, jangka 6 bulan.
Berapa total yang harus dibayar di akhir periode?

M3: Sebuah tim project punya 5 task. Task A & B masing-masing 3 hari, dapat
dikerjakan paralel. Task C butuh A & B selesai, durasi 2 hari. Task D & E
masing-masing 4 hari dan dapat dikerjakan paralel setelah C selesai.
Berapa total waktu minimum project?
```

---

## Langkah

### Langkah 1 — Setup (5 menit)

1. Buka Console Workbench atau claude.ai.
2. Set `temperature=0` (Workbench) untuk konsistensi.
3. Siapkan dokumen / spreadsheet dengan tabel evaluasi (template di bawah).

### Langkah 2 — Run 3 Teknik untuk Task 1 (10 menit)

#### Zero-Shot Template
```text
Klasifikasikan sentimen kalimat berikut sebagai POSITIF, NEGATIF, atau NETRAL.

Kalimat: "{kalimat}"
Sentimen:
```

#### Few-Shot Template
```text
Klasifikasikan sentimen kalimat sebagai POSITIF, NEGATIF, atau NETRAL.

<example>
Kalimat: "Produknya membantu banget."
Sentimen: POSITIF
</example>
<example>
Kalimat: "Kecewa, fiturnya tidak sesuai janji."
Sentimen: NEGATIF
</example>
<example>
Kalimat: "Aplikasi berfungsi sebagaimana mestinya."
Sentimen: NETRAL
</example>
<example>
Kalimat: "Bagus sih, tapi mahal."
Sentimen: NETRAL
</example>
<example>
Kalimat: "Wah keren bisa ngabisin kuota saya, makasih ya /sarcasm"
Sentimen: NEGATIF
</example>

Kalimat: "{kalimat}"
Sentimen:
```

#### Chain-of-Thought Template
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

Jalankan ketiga template untuk S1–S5. Catat output di tabel.

### Langkah 3 — Run 3 Teknik untuk Task 2 (10 menit)

Adaptasi template di atas untuk ekstraksi entitas. Untuk output, paksa format JSON sederhana:

```json
{"person": [...], "organization": [...], "location": [...], "date": [...]}
```

### Langkah 4 — Run 3 Teknik untuk Task 3 (10 menit)

Untuk reasoning matematika, ekspektasi:
- Zero-shot: jawaban langsung, risiko error tinggi.
- Few-shot: beri 1-2 contoh soal+solusi.
- CoT: paksa langkah 1-2-3-... sebelum jawaban.

### Langkah 5 — Tabulasi & Peer Compare (10 menit)

Isi tabel evaluasi (template di bawah), kemudian bandingkan dengan 1 rekan.

---

## Template Tabel Evaluasi

| Task   | Sampel | Ground truth | Zero-shot output | Z benar? | Few-shot output | F benar? | CoT output | CoT benar? | Catatan       |
|--------|--------|--------------|------------------|----------|-----------------|----------|------------|------------|---------------|
| Task 1 | S1     |              |                  |          |                 |          |            |            |               |
| Task 1 | S2     |              |                  |          |                 |          |            |            |               |
| Task 1 | S3     |              |                  |          |                 |          |            |            |               |
| Task 1 | S4     |              |                  |          |                 |          |            |            |               |
| Task 1 | S5     |              |                  |          |                 |          |            |            |               |
| Task 2 | E1     |              |                  |          |                 |          |            |            |               |
| ...    |        |              |                  |          |                 |          |            |            |               |
| Task 3 | M1     |              |                  |          |                 |          |            |            |               |
| ...    |        |              |                  |          |                 |          |            |            |               |

Hitung **akurasi per teknik per task** (%):

| Task   | Zero-shot acc | Few-shot acc | CoT acc | Winner |
|--------|---------------|--------------|---------|--------|
| Task 1 |               |              |         |        |
| Task 2 |               |              |         |        |
| Task 3 |               |              |         |        |

---

## Insight Writing (5 menit)

Tulis 3–5 bullet menjawab:

- Teknik mana yang menang di setiap task? Mengapa?
- Apakah ada task di mana zero-shot sudah cukup? Mengapa few-shot tidak memberi gain?
- Apakah ada task di mana CoT **memperburuk** output? (over-reasoning, hallucinated step)
- Estimasi token cost: kira-kira berapa kali lipat few-shot vs zero-shot?
- Rekomendasi praktis: untuk masing-masing dari 3 task, teknik mana yang Anda pilih ke produksi?

---

## Kriteria Selesai

- [ ] 3 teknik × 3 task = 9 kombinasi telah dijalankan.
- [ ] Tabel evaluasi terisi penuh untuk minimal 2 task (idealnya 3).
- [ ] Akurasi per teknik per task dihitung.
- [ ] Insight 3-5 bullet ditulis.
- [ ] Peer review dilakukan (minimal 1 rekan).

---

## Rubrik

| Kriteria                                    | 0      | 2                 | 4                                  |
|---------------------------------------------|--------|-------------------|------------------------------------|
| Kelengkapan eksperimen                      | < 3 kombinasi | 4–6 kombinasi | 7–9 kombinasi penuh                |
| Konsistensi setup (temperature, format)     | Tidak konsisten | Sebagian konsisten | Sepenuhnya konsisten              |
| Kualitas tabulasi & perhitungan akurasi     | Tidak ada | Ada tapi salah hitung | Lengkap & benar                |
| Insight (bukti-based, bukan opini)          | Tidak ada | Generik           | Spesifik, kuantitatif, actionable  |

**Total maks**: 16. Target: 10+.

---

## Tips

- **Jalankan 2x** untuk memverifikasi konsistensi, bahkan dengan `temperature=0` masih ada variansi minimal.
- Untuk sarkasme (S5), CoT sangat membantu jika Anda menyebut "periksa sarkasme" eksplisit.
- Pada Task 3 M3 (project scheduling), CoT hampir wajib. Zero-shot sering salah.
- Jika Anda pakai claude.ai (tidak ada `temperature=0`), jalankan **2-3 kali per teknik** dan ambil mayoritas.

---

## Deliverable

Simpan dalam dokumen (Google Sheet / Excel / Markdown) dengan tabel evaluasi lengkap + insight section. Kirim ke fasilitator via channel pelatihan.
