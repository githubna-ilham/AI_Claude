# Section 2 — Implementasi Embedding

> Bagian dari **[Module 06 — Latihan](./latihan.md)**. Lanjutan dari **[Section 1 — Konsep Embedding](./latihan-konsep-embedding.md)**.

> Latihan untuk **setup Voyage AI** + bangun function `embed()` reusable + verifikasi semantic similarity. Tiga prompt siap copy-paste.
>
> **Estimasi**: 50–60 menit.

## Prasyarat Section 2

- [ ] Section 1 selesai. Anda paham cosine similarity secara konseptual.
- [ ] Anda sudah membaca bagian Section 2 di `materi.md`.
- [ ] Akun Voyage AI sudah dibuat, API key sudah didapat ([voyageai.com](https://www.voyageai.com/)).

---

## Prompt 1 — Install Voyage AI SDK + Setup API Key

**Salin prompt berikut, paste ke Claude Code:**

```
Saya ingin setup Voyage AI sebagai provider embedding untuk
Fin-App.

GOAL:
- Install package `voyageai` sebagai dependency project
  (bukan devDependency).
- Tambah variable VOYAGE_API_KEY ke .env.local (placeholder
  saja — saya akan isi manual setelahnya).
- Tambah baris VOYAGE_API_KEY="" ke .env.example agar
  developer lain tahu env var ini dibutuhkan.
- Buat file experiments/voyage-ping.ts: panggil
  client.embed() sekali dengan input ["hello world"], print
  panjang vektor + 3 angka pertama. Tujuan: konfirmasi koneksi
  dan API key valid.

CONTEXT:
- Model yang dipakai: voyage-3 (1024 dim, rekomendasi
  Anthropic).
- Project pakai TypeScript + Next.js (sesuai Module 01).

GUARDRAIL:
- JANGAN buat file di src/ — itu untuk Prompt 2.
- JANGAN hard-code API key di file ts mana pun — selalu
  via process.env.
- Apabila .env.local belum ada, beri tahu saya untuk buat
  manual (jangan auto-generate dengan dummy value).
```

**Verifikasi:**

1. `package.json` punya `"voyageai"` di `dependencies`.
2. `.env.example` punya baris `VOYAGE_API_KEY=""`.
3. Isi `.env.local` dengan API key Anda, lalu jalankan:
   `npx tsx --env-file=.env.local experiments/voyage-ping.ts`.
4. Output: `dim: 1024` dan 3 angka float (mis. `[0.012, -0.034, 0.058]`).

---

## Prompt 2 — Buat `src/lib/embeddings.ts`

**Salin prompt berikut, paste ke Claude Code:**

```
Sekarang bangun function embed() reusable yang dipakai di
seluruh aplikasi.

GOAL:
- Buat file baru src/lib/embeddings.ts.
- Mulai dengan import "server-only" di baris pertama untuk
  cegah bundle ke client.
- Ekspor dua function:
  
  1. embed(text: string): Promise<number[]>
     → embed satu teks, return vector 1024-dim.
  
  2. embedBatch(texts: string[]): Promise<number[][]>
     → embed banyak teks dalam satu request (batching).
  
- Inisialisasi VoyageAIClient SEKALI di module scope, baca
  API key dari process.env.VOYAGE_API_KEY.
- Throw error yang jelas apabila VOYAGE_API_KEY tidak ada di
  env.
- Tambah JSDoc singkat untuk masing-masing function.

CONTEXT:
- Model: voyage-3, dimensi 1024.
- File ini akan dipanggil dari Server Actions / route
  handler di section selanjutnya.

GUARDRAIL:
- JANGAN tambah caching dulu — itu akan dibahas terpisah.
- JANGAN modifikasi file lain selain src/lib/embeddings.ts.
- JANGAN ubah experiments/voyage-ping.ts dari prompt 1.
```

**Verifikasi:**

1. File `src/lib/embeddings.ts` ada dengan dua export: `embed` dan `embedBatch`.
2. Baris pertama: `import "server-only";`.
3. Tidak ada error TypeScript saat `npx tsc --noEmit`.
4. Tidak ada hard-coded API key di file.

---

## Prompt 3 — Test Semantic Similarity

**Salin prompt berikut, paste ke Claude Code:**

```
Sekarang verifikasi function embed() benar-benar menangkap
makna semantik, bukan hanya keyword.

GOAL:
- Buat file experiments/test-embeddings.ts.
- Import embedBatch dari "@/lib/embeddings".
- Definisikan 5 kalimat:
  
  s1 = "Beli kopi di Starbucks tadi pagi"
  s2 = "Makan siang nasi padang di warung"
  s3 = "Investasi reksadana saham untuk jangka panjang"
  s4 = "Beli ayam goreng untuk makan malam"
  s5 = "Pertimbangkan portfolio diversifikasi obligasi"
  
- Embed semua sekaligus via embedBatch.
- Implementasi cosine similarity (reuse dari Section 1 OK,
  copy ke file ini).
- Print similarity matrix 5x5 dalam format tabel rapi
  (gunakan padStart untuk alignment).
- Print juga 3 pasangan paling mirip dan 3 paling tidak
  mirip.

CONTEXT:
- Asumsi semantik:
  - s1 (kopi), s2 (nasi padang), s4 (ayam goreng) =
    kategori makanan/F&B → harus saling dekat.
  - s3 (reksadana), s5 (obligasi) = kategori
    investasi → harus dekat satu sama lain.
  - Lintas kategori (mis. s1 vs s3) → harus jauh.

GUARDRAIL:
- JANGAN modifikasi src/lib/embeddings.ts.
- File ini di experiments/, BUKAN di src/.
- Jalankan dengan `npx tsx --env-file=.env.local
  experiments/test-embeddings.ts`.
```

**Verifikasi:**

1. Output matriks 5×5 dengan diagonal = 1.0000.
2. Pasangan `(s1, s2)`, `(s2, s4)`, `(s1, s4)` muncul di top similarity (skor > 0.6).
3. Pasangan `(s3, s5)` punya skor tinggi (> 0.6).
4. Pasangan lintas kategori (mis. `s1` vs `s3`) punya skor lebih rendah daripada pasangan dalam kategori.
5. Apabila hasil tidak sesuai ekspektasi, debug: cek apakah teks benar-benar terkirim ke API, cek dimensi vector.

---

## Validasi Akhir Section 2

- [ ] Package `voyageai` terinstall.
- [ ] `.env.local` punya `VOYAGE_API_KEY` valid, `.env.example` punya placeholder.
- [ ] `src/lib/embeddings.ts` punya `embed()` + `embedBatch()` + import `"server-only"`.
- [ ] Test similarity matrix menunjukkan kategori makanan mengelompok terpisah dari kategori investasi.
- [ ] `npx tsc --noEmit` clean.

## Refleksi Section 2

1. Berapa skor cosine similarity tertinggi yang Anda dapat antara dua kalimat lintas kategori? Apakah itu mengejutkan?
2. Apabila Anda mengubah satu kata di kalimat (mis. "kopi" → "teh"), seberapa besar perubahan skor similarity?
3. Mengapa import `"server-only"` penting di `src/lib/embeddings.ts`? Apa risiko kalau di-skip?
4. Berapa estimasi biaya kalau Anda embed 10.000 deskripsi transaksi (asumsi ~20 token per deskripsi)?

---

⬅️ Kembali: **[Section 1 — Konsep Embedding](./latihan-konsep-embedding.md)** · 🏠 Index: **[Module 06 — Latihan](./latihan.md)** · ➡️ Lanjut: **[Section 3 — Database Vector](./latihan-database-vector.md)**
