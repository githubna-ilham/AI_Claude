# Section 4 — Reranking & Hybrid Search

> Bagian dari **[Module 07 — Latihan](./latihan.md)**. Lanjutan dari **[Section 3 — Chunking Strategy](./latihan-chunking.md)**.

> Latihan untuk **optimasi kualitas retrieval** lewat dua teknik production-grade: **Voyage `rerank-2.5`** (two-stage retrieval) dan **hybrid search** (vector + PostgreSQL full-text + RRF). Tiga prompt — prompt ketiga bersifat opsional dan paling kompleks.
>
> **Estimasi**: 60–70 menit.

## Prasyarat Section 4

- [ ] Section 3 selesai. `knowledge_chunks` berisi FAQ pendek + chunks dari ingest artikel.
- [ ] `searchKnowledge` jalan dengan baik.
- [ ] API key Voyage AI (sudah ada dari Module 06) — model `rerank-2.5` diakses dengan key yang sama.
- [ ] Anda sudah membaca bagian Section 4 di `materi.md`.

---

## Prompt 1 — Setup Voyage Rerank

**Salin prompt berikut, paste ke Claude Code:**

```
Sekarang siapkan helper rerank() berbasis Voyage rerank-2.5
untuk dipakai sebagai stage kedua retrieval.

GOAL:
- Edit src/lib/embeddings.ts (atau buat file baru
  src/lib/rerank.ts kalau lebih clean — sebut alasannya).
- Pakai VoyageAIClient yang sudah ada (atau init ulang
  dengan API key sama).
- Export:
  
  export type RerankResult = {
    index: number;   // index ke array candidates input
    score: number;   // relevance score 0-1
  };
  
  export async function rerank(
    query: string,
    candidates: string[],
    k: number = 5
  ): Promise<RerankResult[]>

- Implementasi:
  
  const res = await client.rerank({
    query,
    documents: candidates,
    model: "rerank-2.5",
    topK: k,
  });
  return res.data!.map(r => ({
    index: r.index!,
    score: r.relevanceScore!,
  }));

- Tambahkan handling: kalau candidates kosong, return []
  langsung (jangan call API).

CONTEXT:
- Voyage API: client.rerank({query, documents, model, topK}).
- topK adalah jumlah hasil yang dikembalikan, BUKAN jumlah
  yang dirank (rerank semua candidates, return top-K).

GUARDRAIL:
- JANGAN ubah embed() / embedBatch() yang sudah ada.
- JANGAN tambah dependency baru (voyageai SDK sudah
  terinstall sejak Module 06).
- Apabila Anda buat file baru src/lib/rerank.ts, pastikan
  pakai "server-only" agar API key tidak bocor.
```

**Verifikasi:**

1. Helper `rerank` ada dengan signature `(query, candidates, k)`.
2. `npx tsc --noEmit` clean.
3. Quick test di `experiments/test-rerank.ts` (opsional): rerank 3 string dummy dengan query, print hasil.

---

## Prompt 2 — Modify `searchKnowledge` Jadi Two-Stage

**Salin prompt berikut, paste ke Claude Code:**

```
Sekarang upgrade searchKnowledge untuk pakai two-stage
retrieval: vector search top-20, lalu rerank ke top-5.

GOAL:
- Edit src/features/knowledge.ts.
- Tambahkan flag opsional ke signature:
  
  export async function searchKnowledge(
    query: string,
    k: number = 5,
    threshold: number = 0.5,
    options: { rerank?: boolean } = {}
  ): Promise<KnowledgeChunk[]>

- Alur baru saat options.rerank === true:
  
  1. Vector search ambil top-20 (bukan k):
     supabase.rpc("match_knowledge_chunks",
       { query_embedding, match_count: 20 }).
  2. Filter dengan threshold (sama seperti sebelumnya).
  3. Apabila hasil >= 2, panggil rerank(query,
     filtered.map(c => c.content), k).
  4. Re-order filtered berdasarkan rerank result. Tambahkan
     field opsional `rerankScore: number` ke KnowledgeChunk.
  5. Return top-k.
  
  Apabila options.rerank === false (default), behavior tetap
  seperti sebelumnya (backward compat).

- Update KnowledgeChunk type:
  
  export type KnowledgeChunk = {
    id: string;
    content: string;
    metadata: Record<string, unknown>;
    distance: number;
    rerankScore?: number;
  };

- Tambah test di experiments/test-search.ts:
  Untuk 3 query dari Section 3 yang sebelumnya kurang
  relevan, jalankan dua kali:
  
  const noRerank = await searchKnowledge(q, 5, 0.6);
  const withRerank = await searchKnowledge(q, 5, 0.6,
    { rerank: true });
  
  Print perbandingan top-3 untuk masing-masing. Verifikasi:
  urutan berbeda, dan (subjektif) urutan dengan rerank
  terasa lebih relevan.

CONTEXT:
- Two-stage retrieval: cast wide (top-20) lalu narrow
  (rerank → top-5). Gain biasanya signifikan untuk query
  nuansa.
- Latensi tambahan ~200ms — masih dapat ditoleransi.

GUARDRAIL:
- JANGAN ubah signature behavior default (rerank=false
  artinya backward compat).
- Apabila rerank API throw, fall back ke hasil vector
  search asli (jangan crash request).
- JANGAN hard-code 20 sebagai top-N pre-rerank — keep
  sebagai konstanta di atas file (mis. RERANK_POOL_SIZE).
```

**Verifikasi:**

1. `searchKnowledge` punya parameter `options.rerank` opsional.
2. Test di `experiments/test-search.ts` menampilkan perbandingan no-rerank vs with-rerank untuk 3 query.
3. Top-3 dengan rerank punya minimal 1 chunk berbeda urutannya vs no-rerank (artinya rerank benar-benar bekerja).
4. Apabila Voyage rerank API gagal (simulasi: invalid model name temp), request tidak crash — fallback ke vector result.
5. `npx tsc --noEmit` clean.

---

## Prompt 3 — (Opsional) Hybrid Search dengan PostgreSQL Full-Text + RRF

**Salin prompt berikut, paste ke Claude Code:**

```
Sekarang tambahkan hybrid search: vector + keyword
(PostgreSQL full-text), digabung dengan RRF (Reciprocal
Rank Fusion).

CATATAN: Latihan ini OPSIONAL dan paling kompleks di Module
07. Selesaikan kalau Anda ingin pengalaman production-grade
RAG. Skip jika waktu Anda terbatas — Section 4 Prompt 1–2
sudah memberi gain kualitas terbesar.

GOAL:
- Buat migration baru:
  supabase/migrations/0005_knowledge_chunks_fts.sql
  Tambahkan generated tsvector column + index GIN:
  
  alter table knowledge_chunks
    add column if not exists content_tsv tsvector
    generated always as (
      to_tsvector('simple', coalesce(content, ''))
    ) stored;
  
  create index if not exists knowledge_chunks_content_tsv_idx
    on knowledge_chunks using gin (content_tsv);
  
  -- SQL function untuk keyword search:
  create or replace function keyword_search_knowledge_chunks(
    query_text text,
    match_count int
  )
  returns table (
    id uuid,
    content text,
    metadata jsonb,
    rank float
  )
  language sql stable as $$
    select id, content, metadata,
           ts_rank(content_tsv,
             plainto_tsquery('simple', query_text)) as rank
    from knowledge_chunks
    where content_tsv @@ plainto_tsquery('simple', query_text)
    order by rank desc
    limit match_count;
  $$;

- Edit src/features/knowledge.ts:
  
  Tambahkan helper:
  
  export async function hybridSearch(
    query: string,
    k: number = 5
  ): Promise<KnowledgeChunk[]>
  
  Alur:
  1. Paralel: vector search top-20 + keyword search top-20.
  2. Gabungkan via RRF (k_rrf = 60):
     score(doc_id) = sum over rankers of:
       1 / (60 + rank_in_ranker + 1)
  3. Sort by RRF score desc, return top-k.
  4. Distance field di KnowledgeChunk: pakai distance dari
     vector search (kalau ada), atau null kalau dokumen
     hanya match keyword.

- Tambahkan flag opsional di searchKnowledge:
  
  searchKnowledge(query, k, threshold, {
    rerank?: boolean;
    hybrid?: boolean;
  })
  
  Apabila hybrid=true, pakai hybridSearch sebagai pool
  awal (bukan vector search saja), lalu (opsional) rerank
  di atas hasilnya.

- Test di experiments/test-search.ts:
  Buat 2 query keyword-heavy:
  - "voyage-3" (atau nama brand/produk lain yang spesifik)
  - "50/30/20"
  
  Jalankan 3 mode untuk masing-masing:
  - vector only
  - hybrid (no rerank)
  - hybrid + rerank
  
  Print perbandingan top-3 untuk tiap mode. Observe:
  query keyword-heavy harusnya jauh lebih baik di hybrid.

CONTEXT:
- RRF formula: 1/(k+rank). k=60 standar Cormack 2009.
- ts_rank dari PostgreSQL TIDAK perlu dinormalisasi — RRF
  tidak peduli skala, hanya rank.
- Hybrid sangat membantu untuk: kode produk, nama brand,
  istilah teknis spesifik.

GUARDRAIL:
- JANGAN hapus searchKnowledge versi vector — tambah mode
  baru, jangan ganti.
- Migration HARUS idempotent (if not exists, create or
  replace).
- Apabila keyword search return 0 hasil (query tidak punya
  exact match), fall back ke vector saja.
- JANGAN paralelisasi rerank dengan retrieval — rerank
  butuh hasil retrieval dulu.
```

**Verifikasi:**

1. Migration `0005_knowledge_chunks_fts.sql` applied di Supabase.
2. SQL function `keyword_search_knowledge_chunks` ada dan return hasil untuk query mis. `"50/30/20"`.
3. `hybridSearch` di `src/features/knowledge.ts` jalan.
4. Test di `experiments/test-search.ts` membandingkan 3 mode untuk 2 query keyword-heavy.
5. Untuk query `"50/30/20"`, hybrid mode menemukan FAQ yang menyebut istilah persis lebih baik daripada vector saja.
6. `npx tsc --noEmit` clean.

---

## Validasi Akhir Section 4

- [ ] Helper `rerank()` ada dan jalan (Prompt 1).
- [ ] `searchKnowledge` punya opsi `rerank` (Prompt 2).
- [ ] Test perbandingan no-rerank vs with-rerank menampilkan perubahan urutan untuk query nuansa.
- [ ] (Opsional) Migration FTS + `hybridSearch` + RRF jalan (Prompt 3).
- [ ] Fallback handling jalan: error di rerank API tidak crash request.
- [ ] `npx tsc --noEmit` clean.

## Refleksi Section 4

1. Untuk query yang sebelumnya gagal di vector-only, mana yang lebih banyak menyelamatkan — rerank atau hybrid? Kenapa menurut Anda?
2. RRF pakai konstanta `k=60`. Apa yang terjadi kalau Anda set `k=5`? Posisi tinggi jadi lebih dominan atau kurang?
3. Latensi total RAG Anda sekarang (embed + retrieve + rerank + Claude): kira-kira berapa detik dari klik kirim sampai token pertama? Acceptable atau terlalu lambat?
4. Bagaimana cara Anda decide kapan harus turn off rerank/hybrid di production? (Hint: cost, latency budget, query patterns.)

---

⬅️ Kembali: **[Section 3 — Chunking Strategy](./latihan-chunking.md)** · 🏠 Index: **[Module 07 — Latihan](./latihan.md)** · ➡️ Lanjut: **Module 08** (akan datang — topik TBD)
