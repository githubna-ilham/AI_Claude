# Section 3 — Chunking Strategy

> Bagian dari **[Module 07 — Latihan](./latihan.md)**. Lanjutan dari **[Section 2 — RAG End-to-End](./latihan-rag-end-to-end.md)**.

> Latihan untuk menambah kemampuan **ingest dokumen panjang** (artikel keuangan, ebook, panduan) ke `knowledge_chunks`. Tiga prompt siap copy-paste — bikin splitter, script ingest, dan verifikasi retrieval.
>
> **Estimasi**: 50–60 menit.

## Prasyarat Section 3

- [ ] Section 2 selesai. AI Advisor RAG-aware jalan end-to-end dengan FAQ pendek.
- [ ] Function `saveKnowledgeChunk` dari Module 06 jalan.
- [ ] `searchKnowledge` dari Section 1 jalan.
- [ ] Anda sudah membaca bagian Section 3 di `materi.md`.

---

## Prompt 1 — Buat Helper `chunkDocument` di `src/lib/chunking.ts`

**Salin prompt berikut, paste ke Claude Code:**

```
Sekarang bangun text splitter sederhana untuk dokumen
panjang sebelum embedding.

GOAL:
- Buat file baru src/lib/chunking.ts (tidak perlu
  "server-only" — pure function, bisa dipakai di mana
  saja).
- Export function:
  
  export type ChunkOptions = {
    size?: number;      // default 500 (character-based)
    overlap?: number;   // default 50
  };
  
  export function chunkDocument(
    text: string,
    opts: ChunkOptions = {}
  ): string[]

- Implementasi pendekatan SLIDING WINDOW character-based:
  
  1. Normalisasi whitespace berlebihan (multiple newline →
     2 newline max, trim).
  2. Loop: ambil substring [start, start + size], push ke
     chunks array.
  3. Geser start dengan (size - overlap) tiap iterasi.
  4. Hentikan saat start >= text.length.
  5. Untuk chunk terakhir, kalau panjang < 50 char,
     gabungkan dengan chunk sebelumnya (hindari chunk
     terlalu kecil).

- Pakai pendekatan character-based untuk kesederhanaan
  iterasi ini (bukan token). Beri comment di file:
  "// Note: character-based. Untuk token-based,
  pertimbangkan gpt-tokenizer di iterasi berikutnya."

- Apabila size <= overlap, throw Error informatif (mencegah
  infinite loop).

CONTEXT:
- Splitter ini akan dipakai di script ingest (Prompt 2).
- Pure function — gampang di-test, tidak ada I/O.

GUARDRAIL:
- JANGAN install package tambahan.
- JANGAN modifikasi src/features/knowledge.ts atau
  src/lib/embeddings.ts.
- Tambahkan minimal 3 unit test sederhana di file yang
  sama (atau file .test.ts terpisah) yang verifikasi:
  (a) text pendek (<size) → 1 chunk berisi seluruh teks.
  (b) text panjang → multiple chunk dengan overlap konsisten.
  (c) Throw saat size <= overlap.
  
  Pakai framework yang sudah ada di project (vitest/jest)
  atau tulis assertion inline yang bisa dijalankan dengan
  npx tsx.
```

**Verifikasi:**

1. File `src/lib/chunking.ts` ada dengan export `chunkDocument`.
2. Test 3 kasus pass (jalankan dengan command sesuai framework project).
3. `npx tsc --noEmit` clean.
4. Untuk teks 2000 karakter dengan `size=500, overlap=50`, hasil ~4–5 chunk dengan overlap karakter terlihat.

---

## Prompt 2 — Ingest Dokumen Panjang

**Salin prompt berikut, paste ke Claude Code:**

```
Sekarang bikin script ingest yang baca markdown file,
chunk, embed, dan simpan ke knowledge_chunks dengan
metadata lengkap.

GOAL:
- Buat file scripts/ingest-doc.ts.
- Argumen CLI: path ke markdown file (process.argv[2]).
- Alur:
  
  1. Baca file dari path (fs/promises readFile, utf-8).
  2. Ekstrak basename file sebagai source_doc.
  3. Panggil chunkDocument(text, {size: 500, overlap: 50}).
  4. Loop chunks:
     for (let i = 0; i < chunks.length; i++) {
       await saveKnowledgeChunk({
         content: chunks[i],
         metadata: {
           source: "ingest",
           source_doc: basename,
           chunk_idx: i,
           total_chunks: chunks.length,
           ingested_at: new Date().toISOString(),
         },
       });
       console.log(`[${i+1}/${chunks.length}] saved`);
     }
  5. Summary di akhir: total chunks, durasi, file source.

- Sequential (bukan Promise.all) supaya hormati rate limit
  Voyage.

- Buat file contoh: docs/sample-finance-article.md
  Isi: artikel keuangan personal Indonesia ~2000 kata
  (Anda generate sendiri). Topik bebas seputar finance —
  mis. "Panduan Lengkap Memulai Investasi Reksadana untuk
  Pemula" — minimum 4 heading section, paragraf-paragraf
  yang membahas: jenis reksadana, cara mulai, risiko,
  strategi diversifikasi, tips evaluasi.

CONTEXT:
- Script dijalankan: npx tsx --env-file=.env.local \
  scripts/ingest-doc.ts docs/sample-finance-article.md
- Idempotency: belum di-handle. Kalau di-run dua kali,
  akan ada duplikat. Catat di komentar awal file.

GUARDRAIL:
- JANGAN truncate knowledge_chunks di awal script.
- JANGAN paralelisasi penuh — sequential loop.
- Apabila satu chunk gagal save, log error tetapi LANJUT
  ke chunk berikutnya.
- Artikel sample HARUS dalam Bahasa Indonesia.
```

**Verifikasi:**

1. File `docs/sample-finance-article.md` ada dengan minimal 4 heading + ~2000 kata Bahasa Indonesia.
2. Jalankan: `npx tsx --env-file=.env.local scripts/ingest-doc.ts docs/sample-finance-article.md`.
3. Output progress per chunk + summary di akhir.
4. Cek di Supabase:
   ```sql
   SELECT count(*) FROM knowledge_chunks
   WHERE metadata->>'source' = 'ingest';
   ```
   Hasilnya = jumlah chunk yang dihasilkan splitter (mis. 5–10).

---

## Prompt 3 — Test Retrieval Setelah Chunking

**Salin prompt berikut, paste ke Claude Code:**

```
Sekarang verifikasi bahwa retrieval menemukan chunk di
TENGAH dokumen (bukan hanya chunk pertama) saat query-nya
match dengan section spesifik.

GOAL:
- Edit experiments/test-search.ts (dari Section 1).
- Tambahkan satu blok baru di akhir file: 3 query yang
  HARUSNYA match dengan section tengah/akhir
  sample-finance-article.md:
  
  Contoh query (sesuaikan dengan isi artikel Anda):
  - "perbedaan risiko reksadana saham dan obligasi"
  - "cara diversifikasi portofolio reksadana"
  - "tips evaluasi kinerja reksadana"

- Untuk tiap query, panggil
  searchKnowledge(query, 3, 0.6) lalu print:
  
  === QUERY: "..." ===
  [1] distance=0.234
      source_doc=sample-finance-article.md
      chunk_idx=3 / total=8
      content="..."

- Verifikasi manual: untuk minimal 2 dari 3 query, top
  hasil punya chunk_idx > 0 (artinya retrieval menemukan
  bagian tengah/akhir dokumen — bukan selalu chunk
  pertama).

- Print juga di akhir summary singkat:
  
  Total chunks dari ingest: ?
  Chunks yang muncul sebagai top-1 di test ini: ?

CONTEXT:
- Tujuan: validasi chunking + metadata berfungsi end-to-end
  untuk retrieval granular.
- Kalau semua query selalu return chunk_idx=0, kemungkinan
  embedding chunk awal terlalu dominan atau artikel tidak
  cukup beragam topiknya.

GUARDRAIL:
- JANGAN modifikasi src/.
- JANGAN truncate atau modifikasi data di knowledge_chunks.
- Apabila hasil tidak match ekspektasi, JANGAN langsung
  patch — diagnosa: query terlalu generik? overlap terlalu
  besar? artikel terlalu homogen?
```

**Verifikasi:**

1. Output `experiments/test-search.ts` mencakup blok 3 query baru dengan metadata.
2. Minimal 2 dari 3 query menemukan chunk dengan `chunk_idx > 0`.
3. Semua hasil punya `source_doc = sample-finance-article.md`.
4. Distance untuk top hasil < 0.5 (relevansi cukup baik).

---

## Validasi Akhir Section 3

- [ ] `src/lib/chunking.ts` punya `chunkDocument` + minimal 3 test pass.
- [ ] `scripts/ingest-doc.ts` jalan dan menambah chunks dari artikel sample.
- [ ] `docs/sample-finance-article.md` ada, Bahasa Indonesia, ~2000 kata, 4+ heading.
- [ ] `knowledge_chunks` punya rows dengan `metadata.source = "ingest"` dan `source_doc / chunk_idx / total_chunks` set.
- [ ] Retrieval di `experiments/test-search.ts` menemukan chunk tengah/akhir untuk minimal 2 dari 3 query baru.
- [ ] `npx tsc --noEmit` clean.

## Refleksi Section 3

1. Untuk artikel 2000 kata Anda, berapa chunk yang dihasilkan dengan `size=500, overlap=50` (karakter)? Apakah jumlahnya masuk akal?
2. Apabila Anda set `overlap=0`, apa risiko nyata di retrieval (selain ukuran storage)?
3. Mengapa kami simpan `chunk_idx` dan `total_chunks` di metadata? Apa kegunaannya untuk UI citation di Section 2?
4. Untuk dokumen yang punya struktur heading kuat (mis. dokumentasi teknis), apakah character-based splitter optimal? Apa alternatifnya?

---

⬅️ Kembali: **[Section 2 — RAG End-to-End](./latihan-rag-end-to-end.md)** · 🏠 Index: **[Module 07 — Latihan](./latihan.md)** · ➡️ Lanjut: **[Section 4 — Reranking & Hybrid Search](./latihan-reranking.md)**
