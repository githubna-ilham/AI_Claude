# Section 1 — Konsep Embedding

> Bagian dari **[Module 06 — Latihan](./latihan.md)**. Lanjutan dari **[Module 05 — Section 4: Agentic Workflow](../Module-05-Prompt-Engineering/latihan-4-agentic.md)**.

> Latihan untuk membangun **intuisi embedding** sebelum integrasi SDK. Dua prompt: satu eksplorasi visual tanpa coding, satu menghitung cosine similarity manual.
>
> **Estimasi**: 30–40 menit.

## Prasyarat Section 1

- [ ] Module 05 selesai. AI Advisor sudah pakai system instruction + tool use.
- [ ] Anda sudah membaca bagian Section 1 di `materi.md`.
- [ ] Akses internet (untuk eksplorasi tool online di Prompt 1).

---

## Prompt 1 — Eksplorasi Embedding Online (Tanpa Coding)

**Salin prompt berikut, paste ke Claude Code:**

```
Saya ingin merasakan apa itu embedding space sebelum menulis
kode apa pun.

GOAL:
- Bantu saya mengeksplorasi visualisasi embedding secara
  interaktif lewat tool online.
- Beri instruksi langkah-demi-langkah untuk membuka
  TensorFlow Projector (https://projector.tensorflow.org/)
  dan menggunakan dataset bawaan Word2Vec 10K.
- Beri 5 kata Indonesia/Inggris untuk saya cari di projector
  (mis. "money", "savings", "coffee", "investment", "food")
  — saya akan amati kata mana yang muncul sebagai nearest
  neighbors-nya.

CONTEXT:
- Ini latihan konseptual untuk Module 06 Section 1 — TIDAK
  ada kode yang dibuat di prompt ini.
- Tujuan: bangun intuisi bahwa kata dengan makna mirip akan
  berdekatan di ruang vektor.

GUARDRAIL:
- JANGAN buat file apa pun di project.
- JANGAN install package atau modifikasi konfigurasi.
- Cukup beri instruksi naratif + 5 kata eksplorasi + 3
  pertanyaan reflektif untuk saya jawab sendiri setelah
  eksplorasi.
```

**Verifikasi:**

1. Anda berhasil membuka TensorFlow Projector di browser.
2. Anda mencoba minimal 3 dari 5 kata dan mengamati 5–10 nearest neighbors masing-masing.
3. Anda menemukan setidaknya satu kasus "tetangga yang tidak intuitif" (mis. embedding training mencerminkan korelasi yang tidak Anda duga).

---

## Prompt 2 — Hitung Cosine Similarity Manual di File Eksperimen

**Salin prompt berikut, paste ke Claude Code:**

```
Saya ingin bangun intuisi cosine similarity dengan menulis
kode dari nol (tanpa SDK embedding apa pun dulu).

GOAL:
- Buat file baru experiments/embedding-intuition.ts.
- Hardcode 5 "vektor mainan" berdimensi 3 yang
  merepresentasikan kalimat berikut secara MANUAL (Anda
  pilih angka yang masuk akal):
  
  v1 = "Beli kopi di Starbucks"        → [?, ?, ?]
  v2 = "Bayar minuman di kafe"          → [?, ?, ?]
  v3 = "Makan siang di restoran"        → [?, ?, ?]
  v4 = "Setor tabungan ke bank"         → [?, ?, ?]
  v5 = "Investasi reksadana"            → [?, ?, ?]
  
  (Pilih angka sedemikian rupa sehingga v1 & v2 dekat,
  v4 & v5 dekat, dan kedua kelompok itu berjauhan.)

- Implementasi function `cosineSimilarity(a, b)` dari nol
  (dot product / (norm a * norm b)).
- Loop semua pasangan, print matriks similarity.
- Print juga ranking pasangan dari paling mirip ke paling
  tidak mirip.

CONTEXT:
- Tujuan: pahami matematika di balik similarity SEBELUM
  pakai embedding API.
- Dimensi 3 dipilih agar manusia bisa memvisualisasi & cek
  manual.

GUARDRAIL:
- JANGAN install package apa pun (`voyageai`, `openai`, dll
  itu untuk Section 2).
- JANGAN modifikasi file di src/ — ini hanya eksperimen.
- Pakai TypeScript murni, jalankan dengan `npx tsx`.
```

**Verifikasi:**

1. Jalankan: `npx tsx experiments/embedding-intuition.ts`.
2. Output menunjukkan matriks 5×5 similarity, dengan diagonal = 1.0.
3. Pasangan `(v1, v2)` dan `(v4, v5)` muncul di urutan teratas ranking.
4. Pasangan lintas kelompok (mis. `(v1, v4)`) muncul di urutan bawah.

---

## Validasi Akhir Section 1

- [ ] Eksplorasi TensorFlow Projector selesai, intuisi "kata mirip → dekat" terkonfirmasi.
- [ ] File `experiments/embedding-intuition.ts` ada dan jalan.
- [ ] Anda dapat menjelaskan cosine similarity dengan kata-kata sendiri.
- [ ] Anda paham bahwa dimensi 3 hanya mainan — model nyata pakai 1024+ dimensi.

## Refleksi Section 1

1. Mengapa cosine similarity (bukan L2 / Euclidean) menjadi default untuk embedding teks?
2. Apa yang terjadi kalau dua vektor identik kecuali magnitude-nya beda (mis. `[1,2,3]` vs `[10,20,30]`)? Cosine atau L2 yang berubah?
3. Apabila Anda tambah dimensi keempat ke vektor mainan, apakah ranking similarity akan berubah drastis? Mengapa / mengapa tidak?

---

⬅️ Kembali: **[Module 05 — Agentic Workflow](../Module-05-Prompt-Engineering/latihan-4-agentic.md)** · 🏠 Index: **[Module 06 — Latihan](./latihan.md)** · ➡️ Lanjut: **[Section 2 — Implementasi Embedding](./latihan-implementasi-embedding.md)**
