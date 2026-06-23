# Lab 02 — Zero-Shot, Few-Shot, Chain-of-Thought

**Modul**: Module 3 — Prompting Techniques
**Durasi**: 45 menit
**Mode**: Individual; peer comparison di 5 menit terakhir.
**Tools**: **Anthropic Console — Workbench** (https://console.anthropic.com/workbench). Lab ini memerlukan kontrol parameter `temperature=0` agar A/B test antar teknik fair. Anda akan login menggunakan **akun Anthropic Console pribadi** Anda yang sudah diundang ke **Workspace pelatihan** oleh fasilitator (lihat Prasyarat di bawah).
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
- Akun **Anthropic Console** pribadi aktif (https://console.anthropic.com).
- Anda sudah menerima dan menerima **undangan email** untuk bergabung ke **Workspace pelatihan Jalin** yang dibuat fasilitator. Setelah accept undangan, Anda dapat memilih workspace tersebut dari dropdown kanan atas Console.
- Semua usage di Workbench selama lab ini akan **otomatis ditagih ke billing fasilitator** — Anda tidak perlu top-up pribadi.
- Spreadsheet atau tabel kosong untuk mencatat hasil.

> ℹ️ **Belum menerima undangan?** Hubungi fasilitator. Pastikan email yang Anda berikan saat registrasi pelatihan sama dengan email yang Anda gunakan di Anthropic Console.

> ℹ️ **Mengapa Workbench, bukan claude.ai?** Untuk Lab 02 ini Anda perlu menetapkan **`temperature=0`** agar hasil eksperimen reproducible — yaitu output yang sama setiap kali prompt dijalankan ulang. claude.ai tidak mengekspos parameter `temperature`, sedangkan Workbench memberikan kontrol penuh. Ini krusial saat Anda ingin membandingkan kualitas zero-shot vs few-shot vs CoT secara objektif.

---

## Mengenal Workbench (Tur Singkat 3 Menit)

Sebelum mulai eksperimen, kenali dulu UI Workbench. Buka https://console.anthropic.com/workbench (pastikan dropdown workspace kanan atas menunjuk ke **"Pelatihan Jalin 2026-06"**).

### Layout UI

Workbench dibagi menjadi 3 area utama:

```
┌─────────────────────────────────────┬──────────────────────────┐
│  AREA KIRI — Prompt Editor          │  PANEL KANAN — Parameter │
│                                     │                          │
│  [ System Prompt    (opsional)  ]   │  Model    [Sonnet 4.x ▼] │
│                                     │                          │
│  [ User message (instruksi Anda) ]  │  Temperature   [ 0.0  ]  │
│                                     │  Max tokens    [ 1024 ]  │
│  [ Assistant (prefill, opsional) ]  │  Top P         [ 1.0  ]  │
│                                     │                          │
│                                     │  ▶ Run                   │
└─────────────────────────────────────┴──────────────────────────┘
                  │
                  ▼
       AREA BAWAH — Output Response + token usage
```

### Elemen yang Akan Anda Pakai di Lab Ini

| Elemen | Fungsi | Yang Anda lakukan |
|--------|--------|-------------------|
| **System Prompt** (atas) | Instruksi tetap untuk role/context — opsional | Kosongkan dulu untuk lab ini |
| **User message** (tengah) | Tempat menulis prompt Anda | Tempel prompt zero-shot / few-shot / CoT di sini |
| **Assistant prefill** (opsional) | Awalan jawaban yang dipaksakan ke model | Tidak dipakai di lab ini (dibahas di Module 4) |
| **Model dropdown** (kanan) | Pilih `claude-sonnet-4-5`, `haiku`, atau `opus` | Set ke `claude-sonnet-4-5` |
| **Temperature** | 0 = deterministik (paling konsisten), 1 = paling kreatif | Set ke **`0`** |
| **Max tokens** | Batas panjang output | `1024` sudah cukup |
| **Run button** (▶) | Eksekusi prompt → panggil API | Klik untuk dapat output |
| **Output area** (bawah) | Tampilkan response + jumlah token input/output | Salin output ke spreadsheet evaluasi Anda |

### 6 Langkah Menjalankan Prompt Pertama

1. **Klik area "User"** di tengah → kursor masuk ke text box besar.
2. **Tempel atau ketik prompt** Anda. Contoh test cepat:

   ```
   Klasifikasikan sentimen kalimat berikut sebagai POSITIF, NEGATIF, atau NETRAL.

   Kalimat: "Aplikasi makin enak dipakai setelah update."
   Sentimen:
   ```

3. **Cek panel kanan**: pastikan Model = `claude-sonnet-4-5`, Temperature = `0`, Max tokens = `1024`.
4. **Klik tombol "Run"** (▶) di panel kanan.
5. **Tunggu 2–5 detik**. Output muncul di bawah area prompt. Akan terlihat:
   - **Response text** (jawaban model).
   - **Usage** (di footer area output): jumlah token input + output → berguna untuk estimasi biaya nanti.
   - **Latency** (durasi eksekusi).
6. **Catat hasil** ke spreadsheet evaluasi Anda.

### Trick yang Berguna

- **Edit ulang prompt**: cukup ubah teks di area User, klik Run lagi → output baru muncul (tidak menimpa, ada history).
- **Reset percakapan**: tombol **"Clear"** atau ikon trash di area prompt.
- **Save prompt**: tombol **"Save"** di kanan atas → beri nama (mis. `M3-Lab02-ZeroShot-Sentimen`) → Anda dapat memuatnya kembali nanti tanpa menulis ulang.
- **Bandingkan side-by-side**: gunakan tombol **"+"** atau **"Compare"** (kalau tersedia di UI Anda) untuk membuka 2 panel prompt sekaligus → eksperimen A/B menjadi lebih cepat.
- **Cek API code**: tombol **"Get code"** atau **"View code"** menampilkan snippet TypeScript/Python yang setara dengan prompt Anda di Workbench — berguna untuk Day 2 saat Anda mulai integrasi via SDK.

### Yang Harus Diingat

- Setiap klik **"Run"** = 1 API call = **memotong saldo Workspace pelatihan**. Hemat run dengan: (1) draft prompt dulu di editor teks, (2) baru tempel ke Workbench saat siap dieksekusi.
- Jika output salah/tidak sesuai → **fix prompt-nya** dulu sebelum naik ke model yang lebih mahal. Jangan langsung loncat dari Sonnet ke Opus hanya karena Sonnet sekali "salah".
- Jika UI Anda berbeda dengan deskripsi di atas (Anthropic memperbarui UI secara berkala) → konsep utama (System / User / Run / parameter di kanan) tetap sama. Tanyakan fasilitator jika menemukan elemen yang berbeda.

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

### Task 2 — Reasoning Matematika (3 sampel)

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

**Ground truth** (untuk evaluasi sendiri di akhir):
- **M1**: Total revenue = **Rp 40.500.000** (Kaos 9 juta + Celana 12 juta + Topi 7 juta + Sepatu 12,5 juta). Revenue tertinggi = **Sepatu (Rp 12.500.000)**.
- **M2**: Total yang harus dibayar = **Rp 5.300.000** (pokok 5 juta + bunga sederhana 5 juta × 12% × 6/12 = 300 ribu).
- **M3**: Total waktu minimum project = **9 hari** (A&B paralel 3 hari → C 2 hari → D&E paralel 4 hari).

### Task 3 — Klasifikasi Sentimen Konteks Jalin (5 sampel)

Sama dengan Task 1 (label: `POSITIF`, `NEGATIF`, `NETRAL`), tapi domain berbeda — kalimat berikut adalah komentar nasabah tentang layanan pembayaran. Tujuannya: melihat apakah teknik yang menang di Task 1 (komentar aplikasi umum) tetap menang di domain finansial dengan istilah teknis (BI-FAST, ATM Link, dispute, dll).

```
J1: "Transfer via BI-FAST cepat banget, sampai dalam 2 detik, mantap!"
J2: "Sudah seminggu komplain dispute saldo terdebit tapi belum diproses, kecewa."
J3: "Aplikasinya update lagi, layoutnya berubah, tapi fungsi utamanya masih sama."
J4: "Awalnya senang karena ATM Link gratis tarik tunai, tapi ternyata limitnya kecil banget."
J5: "Wah keren ya tiap mau transfer harus loading 30 detik, hemat waktu sekali /sarcasm"
```

**Ground truth** (untuk evaluasi sendiri di akhir):
J1: POSITIF, J2: NEGATIF, J3: NETRAL, J4: NEGATIF (mixed sentiment dengan letdown), J5: NEGATIF (sarkasme).

---

## Langkah

### Langkah 1 — Setup (5 menit)

1. Login ke **Anthropic Console** di https://console.anthropic.com menggunakan akun pribadi Anda.
2. Di dropdown **workspace** (pojok kanan atas), pilih **"Pelatihan Jalin"** (atau nama workspace yang diberitahukan fasilitator). Pastikan Anda **berpindah ke workspace pelatihan** — bukan workspace pribadi default.
3. Buka tab **Workbench** dari sidebar kiri.
4. Pilih model **`claude-sonnet-4-5`** di panel kanan.
5. Set parameter di panel kanan:
   - **`temperature`** = `0` (paling penting — agar output deterministik).
   - **`max_tokens`** = `1024` (cukup untuk semua task lab ini).
6. Siapkan dokumen / spreadsheet dengan tabel evaluasi (template di bawah).

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

### Langkah 3 — Run 3 Teknik untuk Task 2 — Reasoning Matematika (10 menit)

Gunakan 3 template di bawah. Ganti placeholder `{soal}` dengan teks M1, M2, atau M3 dari Dataset Lab.

#### Zero-Shot Template
```text
Selesaikan soal matematika berikut. Berikan jawaban akhirnya secara singkat.

Soal: "{soal}"
Jawaban:
```

#### Few-Shot Template
```text
Selesaikan soal matematika berikut. Berikan jawaban akhirnya secara singkat.

<example>
Soal: "Bu Sari membeli 3 kg apel @ Rp 25.000/kg dan 2 kg jeruk @ Rp 30.000/kg. Berapa total yang harus dibayar?"
Jawaban: Apel 3 × 25.000 = 75.000; Jeruk 2 × 30.000 = 60.000; Total = 135.000.
</example>
<example>
Soal: "Pak Budi menabung Rp 50 juta di deposito dengan bunga sederhana 5% per tahun selama 2 tahun. Berapa saldo akhir?"
Jawaban: Bunga = 50 juta × 5% × 2 = 5 juta. Saldo akhir = 50 juta + 5 juta = 55 juta.
</example>

Soal: "{soal}"
Jawaban:
```

#### Chain-of-Thought Template
```text
Selesaikan soal matematika berikut. Pikirkan langkah demi langkah.

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

**Ekspektasi tiap teknik**:
- **Zero-shot**: jawaban langsung tanpa eksplisit menyebut langkah → risiko error tinggi pada soal multi-step.
- **Few-shot**: contoh soal + solusi memandu pola pikir model.
- **CoT**: model menulis langkah 1 → 2 → 3 → … sebelum jawaban akhir. Untuk M3 (project scheduling dengan dependensi paralel), ini hampir wajib.

Jalankan ketiga template untuk M1, M2, M3. Catat output di tabel.

### Langkah 4 — Run 3 Teknik untuk Task 3 — Sentimen Konteks Jalin (5 menit)

**Gunakan kembali 3 template Task 1** tanpa modifikasi — peserta hanya mengganti `{kalimat}` dengan J1–J5. Tujuannya: lihat apakah pemenang teknik di Task 1 (domain umum) **tetap konsisten** ketika domain berubah ke konteks finansial (BI-FAST, ATM Link, dispute).

Jalankan ketiga template untuk J1–J5. Catat output di tabel.

> 💡 **Observasi yang diharapkan**: Sarkasme di J5 (mirip pola S5 di Task 1) seharusnya tetap sulit untuk zero-shot. Mixed sentiment J4 (mirip S4) akan menguji apakah CoT konsisten lintas domain.

### Langkah 5 — Tabulasi & Peer Compare (5 menit)

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
| Task 2 | M1     |              |                  |          |                 |          |            |            |               |
| Task 2 | M2     |              |                  |          |                 |          |            |            |               |
| Task 2 | M3     |              |                  |          |                 |          |            |            |               |
| Task 3 | J1     |              |                  |          |                 |          |            |            |               |
| Task 3 | J2     |              |                  |          |                 |          |            |            |               |
| Task 3 | J3     |              |                  |          |                 |          |            |            |               |
| Task 3 | J4     |              |                  |          |                 |          |            |            |               |
| Task 3 | J5     |              |                  |          |                 |          |            |            |               |

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
- **Konsistensi domain**: apakah teknik pemenang di Task 1 (sentimen umum) sama dengan pemenang di Task 3 (sentimen Jalin)? Jika berbeda, kenapa?

---

## Kriteria Selesai

- [ ] 3 teknik × 3 task = 9 kombinasi telah dijalankan (Task 1: 5 sampel, Task 2: 3 sampel, Task 3: 5 sampel — total ~39 run).
- [ ] Tabel evaluasi terisi penuh untuk minimal 2 task (idealnya 3).
- [ ] Akurasi per teknik per task dihitung.
- [ ] Insight 3-5 bullet ditulis.
- [ ] Peer review dilakukan (minimal 1 rekan).

---

## Rubrik

| Kriteria                                    | 0      | 2                 | 4                                  |
|---------------------------------------------|--------|-------------------|------------------------------------|
| Kelengkapan eksperimen                      | < 3 kombinasi | 4–6 kombinasi | 7–9 kombinasi penuh                |
| Konsistensi setup (format prompt, jumlah run per teknik) | Tidak konsisten | Sebagian konsisten | Sepenuhnya konsisten   |
| Kualitas tabulasi & perhitungan akurasi     | Tidak ada | Ada tapi salah hitung | Lengkap & benar                |
| Insight (bukti-based, bukan opini)          | Tidak ada | Generik           | Spesifik, kuantitatif, actionable  |

**Total maks**: 16. Target: 10+.

---

## Tips

- Dengan `temperature=0`, output yang sama akan keluar setiap Anda klik "Run" — manfaatkan ini untuk eksperimen yang reproducible.
- Untuk sarkasme (S5), CoT sangat membantu jika Anda menyebut "periksa sarkasme" eksplisit.
- Pada Task 2 M3 (project scheduling), CoT hampir wajib. Zero-shot sering salah.
- Jangan lupa **save prompt** Anda di Workbench (tombol "Save" di kanan atas) — Anda dapat membandingkan versi-versi prompt nanti tanpa harus menulis ulang.
- Jika prompt menghasilkan output yang inkonsisten meski `temperature=0`, kemungkinan besar **prompt-nya yang ambigu** — bukan modelnya. Itu sinyal untuk memperketat instruksi.

---

## Deliverable

Simpan dalam dokumen (Google Sheet / Excel / Markdown) dengan tabel evaluasi lengkap + insight section. Kirim ke fasilitator via channel pelatihan.
