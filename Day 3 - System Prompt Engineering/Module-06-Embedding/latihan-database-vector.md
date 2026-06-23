# Section 3 — Database Vector

> Bagian dari **[Module 06 — Latihan](./latihan.md)**. Lanjutan dari **[Section 2 — Implementasi Embedding](./latihan-implementasi-embedding.md)**.

> Latihan untuk **verifikasi pgvector**, bikin migration `knowledge_chunks`, dan eksplorasi distance operator di SQL Editor Supabase. Tiga prompt siap copy-paste.
>
> **Estimasi**: 40–50 menit.

## Prasyarat Section 3

- [ ] Section 2 selesai. Function `embed()` jalan dengan baik.
- [ ] Anda sudah membaca bagian Section 3 di `materi.md`.
- [ ] Anda punya akses ke Supabase project Fin-App (dari Module 01) dengan permission SQL Editor.

---

## Prompt 1 — Verifikasi Pgvector Aktif di Supabase

**Salin prompt berikut, paste ke Claude Code:**

```
Saya perlu memastikan extension pgvector aktif di Supabase
project Fin-App sebelum bikin table vector.

GOAL:
- Beri saya SQL yang harus saya jalankan manual di Supabase
  SQL Editor untuk:
  
  1. Cek apakah extension `vector` sudah terinstall:
     SELECT * FROM pg_extension WHERE extname = 'vector';
  
  2. Apabila belum ada, install dengan:
     CREATE EXTENSION IF NOT EXISTS vector;
  
  3. Konfirmasi versi extension:
     SELECT extname, extversion FROM pg_extension
     WHERE extname = 'vector';

- Beri juga cara cek lewat Supabase Dashboard
  (Database → Extensions → cari "vector").

CONTEXT:
- Project Fin-App pakai Supabase (sesuai Module 01).
- Module 01 migration awal seharusnya sudah aktifkan
  pgvector — prompt ini sekadar verifikasi defensive.

GUARDRAIL:
- JANGAN buat file migration baru di prompt ini — itu
  Prompt 2.
- JANGAN modifikasi kode TypeScript apa pun.
- Apabila pgvector ternyata belum ada, beri tahu saya cara
  enable lewat Dashboard sebelum lanjut.
```

**Verifikasi:**

1. Query `SELECT * FROM pg_extension WHERE extname = 'vector';` mengembalikan **satu row**.
2. `extversion` minimal `0.5.0` (lebih baru = lebih baik, mendukung HNSW).
3. Apabila row kosong → jalankan `CREATE EXTENSION` dulu, lalu re-verifikasi.

---

## Prompt 2 — Buat Migration `knowledge_chunks` Table

**Salin prompt berikut, paste ke Claude Code:**

```
Sekarang bikin migration untuk table knowledge_chunks yang
akan menyimpan FAQ + knowledge base Fin-App.

GOAL:
- Buat file baru supabase/migrations/0003_knowledge_chunks.sql.
- Isi dengan:
  
  1. CREATE EXTENSION IF NOT EXISTS vector; (idempotent
     defensive)
  
  2. CREATE TABLE IF NOT EXISTS knowledge_chunks dengan
     kolom:
     - id UUID PRIMARY KEY DEFAULT gen_random_uuid()
     - content TEXT NOT NULL
     - embedding vector(1024) NOT NULL
     - metadata JSONB NOT NULL DEFAULT '{}'::jsonb
     - created_at TIMESTAMPTZ NOT NULL DEFAULT now()
  
  3. CREATE INDEX IF NOT EXISTS knowledge_chunks_embedding_idx
     ON knowledge_chunks USING hnsw (embedding
     vector_cosine_ops);
  
  4. COMMENT ON TABLE knowledge_chunks IS '...' dengan
     deskripsi singkat.

- Setelah file dibuat, beri saya instruksi cara apply
  migration ini ke Supabase (via CLI `supabase db push`
  ATAU paste manual ke SQL Editor — apapun yang sesuai
  workflow project saya).

CONTEXT:
- Naming convention migration mengikuti file 0001, 0002
  yang sudah ada di supabase/migrations/.
- Dimensi 1024 sesuai voyage-3.

GUARDRAIL:
- JANGAN drop / alter table yang sudah ada.
- JANGAN otomatis jalankan `supabase db push` — beri saya
  command-nya saja.
- Pakai IF NOT EXISTS di semua statement agar idempotent.
```

**Verifikasi:**

1. File `supabase/migrations/0003_knowledge_chunks.sql` ada.
2. Apply migration (via CLI atau paste ke SQL Editor).
3. Cek di Supabase: Database → Tables → ada table `knowledge_chunks` dengan kolom sesuai schema.
4. Cek index: `SELECT indexname FROM pg_indexes WHERE tablename = 'knowledge_chunks';` — ada `knowledge_chunks_embedding_idx`.

---

## Prompt 3 — Test Query Distance Operator

**Salin prompt berikut, paste ke Claude Code:**

```
Sebelum integrasi via TypeScript, saya ingin merasakan
distance operator pgvector langsung di SQL.

GOAL:
- Beri saya 3 blok SQL untuk dijalankan manual di Supabase
  SQL Editor:
  
  BLOK A — Insert 3 row dummy dengan random vector:
  INSERT INTO knowledge_chunks (content, embedding) VALUES
    ('Tips menabung dana darurat',
     (SELECT array_agg(random())::vector
      FROM generate_series(1, 1024))),
    ('Cara investasi reksadana pemula',
     (SELECT array_agg(random())::vector
      FROM generate_series(1, 1024))),
    ('Resep masakan rumahan murah',
     (SELECT array_agg(random())::vector
      FROM generate_series(1, 1024)));
  
  BLOK B — Buat query vector dummy, cari top-2 terdekat
  pakai operator <=> (cosine):
  WITH q AS (
    SELECT (SELECT array_agg(random())::vector
            FROM generate_series(1, 1024)) AS qvec
  )
  SELECT id, content, embedding <=> (SELECT qvec FROM q)
         AS cosine_distance
  FROM knowledge_chunks
  ORDER BY embedding <=> (SELECT qvec FROM q)
  LIMIT 2;
  
  BLOK C — Bandingkan dengan operator <-> (L2) dan <#>
  (negative inner product) untuk query yang sama. Beri saya
  query yang siap paste.

- Catatan: karena vektor random, hasilnya TIDAK akan
  bermakna semantik — tujuan latihan ini murni memahami
  syntax dan urutan ASC dari masing-masing operator.

CONTEXT:
- Pgvector mendukung 3 operator distance: <=>, <->, <#>.
- Vector cast: `'[0.1, 0.2, ...]'::vector` atau via
  array_agg seperti di atas.

GUARDRAIL:
- JANGAN modifikasi kode TypeScript.
- JANGAN drop / truncate row yang baru di-insert — itu
  dummy yang akan dibersihkan di Section 4 saat seed nyata
  masuk.
- Beri instruksi cleanup di akhir: DELETE FROM
  knowledge_chunks WHERE metadata = '{}'::jsonb AND
  content LIKE 'Tips%' OR content LIKE 'Cara%' OR content
  LIKE 'Resep%';
```

**Verifikasi:**

1. Blok A: 3 row ter-insert. Cek: `SELECT count(*) FROM knowledge_chunks;` → 3.
2. Blok B: query return 2 row dengan `cosine_distance` antara 0 dan ~1 (random vector → cosine biasanya sekitar 0.5).
3. Blok C: jalankan 3 variasi, perhatikan bahwa urutan top-2 **bisa berbeda** untuk operator yang berbeda meski query vector sama.
4. Jalankan DELETE cleanup. Cek: table balik ke kondisi kosong.

---

## Validasi Akhir Section 3

- [ ] Pgvector extension aktif, versi konfirmasi.
- [ ] Migration `0003_knowledge_chunks.sql` ada dan sudah ter-apply.
- [ ] Table `knowledge_chunks` punya kolom + index HNSW.
- [ ] Anda sudah menjalankan minimal sekali query dengan operator `<=>`.
- [ ] Cleanup dummy sudah dilakukan — table kosong, siap diisi data sungguhan.

## Refleksi Section 3

1. Mengapa kami pakai index HNSW alih-alih IVFFlat di migration ini?
2. Apa beda hasil `<=>` (cosine distance) dengan `<->` (L2) saat vektor sudah dinormalisasi (seperti output Voyage)?
3. Apabila Anda nanti pindah dari voyage-3 ke OpenAI `text-embedding-3-large` (3072 dim), apa yang harus berubah di schema?
4. Mengapa `metadata` bertipe `JSONB` alih-alih kolom-kolom terpisah?

---

⬅️ Kembali: **[Section 2 — Implementasi Embedding](./latihan-implementasi-embedding.md)** · 🏠 Index: **[Module 06 — Latihan](./latihan.md)** · ➡️ Lanjut: **[Section 4 — Save Embedding To DB Vector](./latihan-save-embedding-db.md)**
