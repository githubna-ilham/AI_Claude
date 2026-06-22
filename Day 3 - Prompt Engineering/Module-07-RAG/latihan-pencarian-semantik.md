# Section 1 — Pencarian Semantik (Vector Query)

> Bagian dari **[Module 07 — Latihan](./latihan.md)**. Lanjutan dari **[Module 06 — Section 4: Save Embedding To DB Vector](../Module-06-Embedding/latihan-save-embedding-db.md)**.

> Latihan untuk membangun **primitif retrieval** — helper `searchKnowledge()` yang menerima natural language query dan mengembalikan top-K chunk dari `knowledge_chunks`. Tiga prompt siap copy-paste.
>
> **Estimasi**: 50–60 menit.

## Prasyarat Section 1

- [ ] Module 06 selesai. Table `knowledge_chunks` berisi minimal 10 FAQ ter-embed (`source = "seed"`).
- [ ] Function `embed()` di `src/lib/embeddings.ts` jalan.
- [ ] Helper Supabase server di `src/lib/supabase/` tersedia (dari Module 01).
- [ ] Anda sudah membaca bagian Section 1 di `materi.md`.

---

## Prompt 1 — Buat Helper `searchKnowledge` di `src/features/knowledge.ts`

**Salin prompt berikut, paste ke Claude Code:**

```
Sekarang bangun primitif retrieval untuk RAG — function
yang menerima natural language query dan mengembalikan
top-K chunk paling mirip dari knowledge_chunks.

GOAL:
- Buka src/features/knowledge.ts (sudah ada dari Module 06,
  berisi saveKnowledgeChunk).
- Tambahkan export type KnowledgeChunk:
  
  export type KnowledgeChunk = {
    id: string;
    content: string;
    metadata: Record<string, unknown>;
    distance: number;
  };

- Tambahkan export async function searchKnowledge(
    query: string,
    k: number = 5,
    threshold: number = 0.5
  ): Promise<KnowledgeChunk[]>

- Alur internal:
  1. Panggil embed(query) untuk dapat query vector.
  2. Jalankan SQL: SELECT id, content, metadata,
     (embedding <=> $1) AS distance
     FROM knowledge_chunks
     ORDER BY embedding <=> $1
     LIMIT $2.
  3. Karena Supabase JS client tidak support operator <=>
     langsung dari builder, BUAT migration baru di
     supabase/migrations/0004_match_knowledge_chunks.sql
     yang mendefinisikan SQL function:
     
     create or replace function match_knowledge_chunks(
       query_embedding vector(1024),
       match_count int
     )
     returns table (
       id uuid,
       content text,
       metadata jsonb,
       distance float
     )
     language sql stable as $$
       select id, content, metadata,
              (embedding <=> query_embedding) as distance
       from knowledge_chunks
       order by embedding <=> query_embedding
       limit match_count;
     $$;
     
  4. Di searchKnowledge, panggil
     supabase.rpc("match_knowledge_chunks",
       { query_embedding: queryVector, match_count: k }).
  5. Filter hasil dengan distance > threshold dibuang.
  6. Return array KnowledgeChunk.

CONTEXT:
- Threshold 0.5 = cosine distance, anything more than that
  considered "tidak relevan" (lihat materi Section 1).
- Helper ini akan dipakai di Section 2 untuk integrasi
  ke /api/advisor.

GUARDRAIL:
- JANGAN ubah saveKnowledgeChunk yang sudah ada.
- JANGAN ubah migration 0003 (knowledge_chunks).
- Pastikan migration baru idempotent (create or replace).
- Jangan hard-code k atau threshold di SQL — keep semua
  parameter dari TypeScript.
```

**Verifikasi:**

1. File `src/features/knowledge.ts` punya export `KnowledgeChunk` type dan `searchKnowledge` function.
2. Migration `supabase/migrations/0004_match_knowledge_chunks.sql` ada dan idempotent.
3. Jalankan migration via Supabase CLI atau SQL Editor — function `match_knowledge_chunks` terdaftar.
4. `npx tsc --noEmit` clean.

---

## Prompt 2 — Test `searchKnowledge` dari File Eksperimen

**Salin prompt berikut, paste ke Claude Code:**

```
Sekarang verifikasi searchKnowledge bekerja dengan query
natural language.

GOAL:
- Buat file experiments/test-search.ts.
- Hardcode array 5 query natural language Indonesia:
  
  const queries = [
    "cara nabung",
    "investasi untuk pemula",
    "dana darurat keuangan",
    "rasio utang yang aman",
    "tips beli rumah"
  ];

- Loop tiap query, panggil searchKnowledge(query, 3, 1.0)
  (threshold 1.0 = ambil semua top-3 tanpa filter, supaya
  saya bisa lihat distance asli semua hasil).
- Print untuk tiap query:
  
  === QUERY: "..." ===
  [1] distance=0.234 | content="..."
  [2] distance=0.312 | content="..."
  [3] distance=0.456 | content="..."

- Truncate content ke 80 karakter pertama agar output rapi.

CONTEXT:
- Tujuan: verifikasi semantic search jalan — FAQ yang
  related muncul lebih dekat dibanding yang tidak related.
- Karena threshold tinggi (1.0), saya bisa observe nilai
  distance asli untuk tuning di Prompt 3.

GUARDRAIL:
- JANGAN modifikasi src/features/knowledge.ts.
- Jalankan via: npx tsx --env-file=.env.local experiments/test-search.ts
- Pastikan import path relatif sesuai (mis. dari experiments/
  ke src/features/knowledge perlu path alias atau relative).
```

**Verifikasi:**

1. Output 5 blok query, masing-masing dengan 3 hasil + distance.
2. Untuk query `"cara nabung"`, top hasil yang muncul adalah FAQ tentang menabung / tabungan.
3. Untuk query `"dana darurat keuangan"`, top hasil adalah FAQ tentang `emergency fund`.
4. Distance untuk hasil pertama umumnya `< 0.4` untuk query yang ada di FAQ.

---

## Prompt 3 — Tuning Threshold

**Salin prompt berikut, paste ke Claude Code:**

```
Sekarang eksperimen dengan threshold untuk pahami trade-off
filtering hasil.

GOAL:
- Modifikasi experiments/test-search.ts.
- Tambahkan satu loop tambahan di bagian akhir file: untuk
  threshold values [0.3, 0.5, 0.7], jalankan ulang 5 query
  yang sama dengan searchKnowledge(query, 5, threshold).
- Print:
  
  === THRESHOLD = 0.3 ===
  Query "cara nabung" → 2 hasil
  Query "investasi untuk pemula" → 3 hasil
  ...
  
  === THRESHOLD = 0.5 ===
  Query "cara nabung" → 4 hasil
  ...

- Tambahkan satu query "kontrol" yang sengaja TIDAK related:
  "resep masakan rendang" → harapan: 0 hasil di threshold
  ketat, 0–1 di threshold longgar.

- Di akhir file, tulis comment block dengan insight Anda:
  
  /*
   * Insight tuning threshold:
   * - Threshold 0.3 → ... (catat observasi)
   * - Threshold 0.5 → ...
   * - Threshold 0.7 → ...
   * - Query kontrol "rendang" → ...
   *
   * Rekomendasi default Fin-App: threshold = ?
   */

CONTEXT:
- Tujuan: bangun intuisi kapan hasil dianggap relevan vs
  tidak. Threshold yang terlalu ketat → kehilangan match
  yang sebenarnya valid. Terlalu longgar → noise.

GUARDRAIL:
- JANGAN ubah searchKnowledge.
- JANGAN modifikasi src/.
- Insight di comment harus berdasarkan output ASLI yang
  Anda observe — bukan asumsi generik.
```

**Verifikasi:**

1. Jalankan ulang `experiments/test-search.ts` — output mencakup tabel jumlah hasil per threshold.
2. Tren yang wajar: threshold naik → jumlah hasil bertambah.
3. Query kontrol `"rendang"` umumnya kosong di threshold ≤ 0.5.
4. Comment block insight terisi dengan observasi nyata, bukan template kosong.

---

## Validasi Akhir Section 1

- [ ] `src/features/knowledge.ts` punya `searchKnowledge` dengan signature `(query, k, threshold)`.
- [ ] Migration `0004_match_knowledge_chunks.sql` ada dan applied di Supabase.
- [ ] `experiments/test-search.ts` jalan tanpa error.
- [ ] Anda dapat menjelaskan trade-off threshold 0.3 vs 0.5 vs 0.7 dengan kata-kata sendiri.
- [ ] `npx tsc --noEmit` clean.

## Refleksi Section 1

1. Mengapa kami pakai SQL function `match_knowledge_chunks` di Postgres alih-alih raw SQL di TypeScript?
2. Apa yang terjadi kalau threshold di-set 0.0? Apa yang terjadi kalau di-set 2.0?
3. Untuk query kontrol "rendang", kalau ternyata ada hasil dengan distance 0.7 — apa kemungkinan penyebabnya?
4. Bagaimana cara Anda mengukur "kualitas retrieval" secara objektif? (Hint: precision@k, recall, MRR — tidak perlu implementasi, cukup pahami konsep.)

---

⬅️ Kembali: **[Module 06 — Save Embedding To DB](../Module-06-Embedding/latihan-save-embedding-db.md)** · 🏠 Index: **[Module 07 — Latihan](./latihan.md)** · ➡️ Lanjut: **[Section 2 — RAG End-to-End](./latihan-rag-end-to-end.md)**
