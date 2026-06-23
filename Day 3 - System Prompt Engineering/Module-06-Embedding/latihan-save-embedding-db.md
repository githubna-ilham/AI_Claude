# Section 4 — Save Embedding To DB Vector

> Bagian dari **[Module 06 — Latihan](./latihan.md)**. Lanjutan dari **[Section 3 — Database Vector](./latihan-database-vector.md)**.

> Latihan untuk **menghubungkan `embed()` + table `knowledge_chunks`** lewat helper Server Action, lalu seed FAQ keuangan personal. Tiga prompt siap copy-paste.
>
> **Estimasi**: 60–70 menit.

## Prasyarat Section 4

- [ ] Section 3 selesai. Table `knowledge_chunks` ada, kosong, index HNSW aktif.
- [ ] Section 2 selesai. Function `embed()` jalan dengan baik.
- [ ] Anda sudah membaca bagian Section 4 di `materi.md`.
- [ ] Supabase client helper sudah tersedia (dari Module 01, biasanya `src/lib/supabase/server.ts`).

---

## Prompt 1 — Helper Function `saveKnowledgeChunk` di Server Action

**Salin prompt berikut, paste ke Claude Code:**

```
Sekarang hubungkan embed() (Section 2) dengan
knowledge_chunks (Section 3) lewat satu helper.

GOAL:
- Buat file baru src/features/knowledge.ts.
- Baris pertama: "use server";
- Ekspor function async saveKnowledgeChunk yang menerima
  parameter:
  
  {
    content: string;
    metadata?: Record<string, unknown>;
  }
  
  dan mengembalikan { id: string }.

- Alur internal:
  1. Panggil embed(content) dari "@/lib/embeddings" untuk
     dapat vector.
  2. Inisialisasi Supabase server client (sesuaikan dengan
     helper yang sudah ada di project, mis. dari
     "@/lib/supabase/server").
  3. INSERT ke knowledge_chunks dengan content, embedding,
     metadata; .select("id").single().
  4. Throw Error yang informatif apabila gagal.
  5. Return { id }.

CONTEXT:
- Helper ini dipanggil dari script seed (Prompt 2) dan
  nanti dari fitur admin / lokal lainnya.
- Embedding berdimensi 1024 sesuai voyage-3 — sudah match
  dengan schema vector(1024).

GUARDRAIL:
- JANGAN ubah src/lib/embeddings.ts atau migration SQL.
- JANGAN tambah fitur lain (delete, update, query) di file
  ini — itu di section RAG lanjutan.
- Apabila import path Supabase client di project saya
  berbeda, beri tahu saya path yang benar berdasarkan file
  yang sudah ada di src/lib/supabase/.
```

**Verifikasi:**

1. File `src/features/knowledge.ts` ada dengan `"use server";` di baris pertama.
2. Export `saveKnowledgeChunk` ada dan signature sesuai.
3. `npx tsc --noEmit` clean.
4. Tidak ada hard-code data — semua via parameter.

---

## Prompt 2 — Seed FAQ Data

**Salin prompt berikut, paste ke Claude Code:**

```
Sekarang seed FAQ keuangan personal sebagai knowledge base
awal untuk AI Advisor.

GOAL:
- Buat file scripts/seed-knowledge.ts.
- Hardcode array 10 FAQ keuangan personal (gunakan daftar
  di materi.md Section 4, atau parafrase serupa).
- Loop, panggil saveKnowledgeChunk untuk setiap entry
  dengan:
  
  metadata: {
    source: "seed",
    category: "personal-finance-faq",
    seeded_at: new Date().toISOString()
  }

- Print progress per chunk:
  "[k/10] saved id=... content='...'"
- Print summary di akhir: jumlah sukses + jumlah gagal +
  total durasi.
- Apabila ada chunk yang gagal, log error tetapi LANJUT ke
  chunk berikutnya (jangan crash seluruh script).

CONTEXT:
- Script dijalankan manual dari local dev:
  `npx tsx --env-file=.env.local scripts/seed-knowledge.ts`
- Idempotency belum dibutuhkan untuk seed pertama — kalau
  dijalankan dua kali, akan ada duplikat. Itu OK untuk
  sekarang.

GUARDRAIL:
- JANGAN ubah saveKnowledgeChunk — pakai apa adanya.
- JANGAN truncate table dulu di awal script — biarkan user
  cleanup manual kalau perlu.
- JANGAN paralelisasi dengan Promise.all penuh — pakai
  sequential loop (atau Promise.all dengan batch kecil ≤ 5)
  untuk hormat rate limit Voyage.
```

**Verifikasi:**

1. Jalankan: `npx tsx --env-file=.env.local scripts/seed-knowledge.ts`.
2. Output progress 10 baris `[k/10] saved id=...`.
3. Summary: `10 sukses, 0 gagal`.
4. Total durasi (perkiraan 5–15 detik tergantung latency Voyage).

---

## Prompt 3 — Verifikasi Roundtrip

**Salin prompt berikut, paste ke Claude Code:**

```
Saya ingin verifikasi data tersimpan dengan benar — content,
embedding, dan metadata semua valid.

GOAL:
- Beri saya 4 query SQL untuk dijalankan manual di Supabase
  SQL Editor:
  
  QUERY 1 — Hitung total + cek dims:
  SELECT
    count(*) AS total,
    min(vector_dims(embedding)) AS min_dim,
    max(vector_dims(embedding)) AS max_dim
  FROM knowledge_chunks;
  
  QUERY 2 — Sampling content + preview embedding:
  SELECT
    id,
    content,
    vector_dims(embedding) AS dims,
    substring(embedding::text, 1, 60) AS preview,
    metadata
  FROM knowledge_chunks
  ORDER BY created_at
  LIMIT 5;
  
  QUERY 3 — Validasi metadata:
  SELECT
    metadata->>'source' AS source,
    metadata->>'category' AS category,
    count(*) AS jumlah
  FROM knowledge_chunks
  GROUP BY 1, 2;
  
  QUERY 4 — Cek tidak ada NULL embedding:
  SELECT count(*) FROM knowledge_chunks
  WHERE embedding IS NULL;
  
- Untuk setiap query, beri SATU baris ekspektasi hasil
  ringkas.

CONTEXT:
- Tujuan: verifikasi roundtrip seed → DB selesai dengan
  integritas penuh sebelum lanjut ke iterasi RAG.

GUARDRAIL:
- JANGAN modifikasi data — query SELECT only.
- JANGAN buat file baru.
- Beri instruksi cleanup OPSIONAL di akhir (DELETE FROM
  knowledge_chunks WHERE metadata->>'source' = 'seed')
  hanya apabila saya minta reset.
```

**Verifikasi:**

1. Query 1: `total = 10` (atau jumlah seed Anda), `min_dim = max_dim = 1024`.
2. Query 2: 5 baris dengan content sesuai seed, `preview` berupa string mulai dengan `[` dan angka float.
3. Query 3: satu baris `source=seed, category=personal-finance-faq, jumlah=10`.
4. Query 4: `count = 0`.
5. Apabila salah satu verifikasi gagal, debug sebelum lanjut — fondasi yang rusak akan menyulitkan iterasi RAG berikutnya.

---

## Validasi Akhir Section 4

- [ ] File `src/features/knowledge.ts` ada dengan `saveKnowledgeChunk`.
- [ ] File `scripts/seed-knowledge.ts` ada dan sudah dijalankan sukses.
- [ ] Table `knowledge_chunks` berisi 10 row (atau jumlah seed Anda).
- [ ] Semua row punya `dims = 1024`, `embedding` non-null.
- [ ] Metadata `source=seed, category=personal-finance-faq` terverifikasi.
- [ ] `npx tsc --noEmit` clean.

## Refleksi Section 4

1. Berapa lama total durasi seed 10 chunk? Kalau diskalakan ke 10.000 chunk, berapa estimasi durasinya?
2. Mengapa kami simpan `metadata.source = "seed"`? Apa nilainya saat data mulai bertambah dari sumber lain (user input, scrape, dll)?
3. Apabila Anda ingin update salah satu FAQ (mis. mengubah teks "50/30/20"), apakah perlu re-embed? Mengapa?
4. Apa langkah pertama yang Anda bayangkan untuk iterasi RAG berikutnya — query natural language dari user → hasil chunk relevan?

---

⬅️ Kembali: **[Section 3 — Database Vector](./latihan-database-vector.md)** · 🏠 Index: **[Module 06 — Latihan](./latihan.md)** · ➡️ Lanjut: **Module 07 — RAG** (akan datang)
