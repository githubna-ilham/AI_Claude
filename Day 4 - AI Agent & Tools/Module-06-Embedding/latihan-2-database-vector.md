# Section 2 — Database Vector

> Bagian dari **[Module 06 — Latihan](./latihan.md)**. Lanjutan dari **[Section 1 — Implementasi Embedding](./latihan-1-implementasi-embedding.md)**.

> Di section ini kita akan **memastikan pgvector aktif**, **menyiapkan kolom & index** di tabel `transactions` (plus function `match_transactions`), lalu **mengisi data dummy dan mencoba 3 distance operator** (`<=>`, `<->`, `<#>`) langsung di tabel sungguhan. Semua sudah siap dalam tiga prompt yang tinggal Anda salin.
>
> **Alur belajarnya**: verifikasi extension → ALTER tabel `transactions` + index + function → insert dummy + main-main dengan 3 operator. Pola yang kita ikuti benar-benar mencerminkan workflow asli: siapkan infrastruktur, isi data, baru query.
>
> **Estimasi waktu**: 40–50 menit.

## Prasyarat Section 2

- [ ] Section 1 sudah selesai dan function `embed()` berjalan lancar.
- [ ] Anda sudah meluangkan waktu membaca bagian Section 2 di `materi.md`.
- [ ] Anda punya akses ke Supabase project Fin-App (dari Module 01) beserta permission SQL Editor.

---

## 📚 Referensi Dokumentasi

Tab-tab dokumentasi berikut bagus untuk dibuka di samping sebagai teman selama Section 2 berjalan:

- **[pgvector GitHub](https://github.com/pgvector/pgvector)** — instalasi, syntax `vector(N)`, operator, dan contoh query.
- **[Supabase pgvector guide](https://supabase.com/docs/guides/database/extensions/pgvector)** — cara enable extension di Supabase plus contoh schema & best practice.
- **[HNSW index Supabase docs](https://supabase.com/docs/guides/ai/vector-indexes/hnsw-indexes)** — kapan memilih HNSW vs IVFFlat, plus parameter `m` dan `ef_construction`.
- **[Distance operators reference](https://github.com/pgvector/pgvector#distances)** — `<=>` cosine, `<->` L2, `<#>` negative inner product.

---

## Prompt 1 — Verifikasi Pgvector Aktif di Supabase

### Walkthrough Manual

Sebelum kita kirim prompt ke Claude, mari pahami dulu langkah verifikasinya. Tenang — di sesi ini tidak ada file lokal yang perlu diubah, semua dilakukan langsung di Supabase Dashboard.

📂 **Eksekusi SQL di Supabase Dashboard** (tidak ada file lokal yang berubah)

**1. Buka Supabase SQL Editor**

📍 Lokasi: [Supabase Dashboard](https://app.supabase.com/) → project Fin-App → sidebar kiri → **SQL Editor** → **New query**.

**2. Cek apakah extension `vector` sudah terpasang**

📍 Lokasi: SQL Editor → tempel query → Run.

```sql
-- Supabase SQL Editor — cek extension
SELECT * FROM pg_extension WHERE extname = 'vector';
```

Kalau hasilnya 1 row, berarti pgvector sudah aktif — silakan lompat ke step 4. Kalau kosong, mari lanjut ke step 3 untuk memasangnya.

**3. Pasang extension (kalau memang belum ada)**

📍 Lokasi: SQL Editor — window yang sama.

```sql
-- Supabase SQL Editor — install
CREATE EXTENSION IF NOT EXISTS vector;
```

**4. Konfirmasi versinya**

📍 Lokasi: SQL Editor.

```sql
-- Supabase SQL Editor — versi
SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';
```

Pastikan `extversion` minimal `0.5.0` — versi inilah yang sudah mendukung HNSW (yang akan kita pakai sebentar lagi).

### Yang sebaiknya tidak dilakukan

- ❌ Membuat file migration di prompt ini — itu jatahnya Prompt 2, jadi tunggu sebentar.
- ❌ Mengutak-atik kode TypeScript di project — fokus kita masih di sisi database.
- ❌ Restart Supabase project — tidak perlu, extension langsung aktif setelah `CREATE EXTENSION`.
- ❌ Mengedit `config.toml` Supabase lokal, kecuali Anda memang memakai `supabase start` (kebanyakan workflow di latihan ini langsung ke hosted).

### Verifikasi setelah eksekusi

1. Query `SELECT * FROM pg_extension WHERE extname = 'vector';` mengembalikan **satu row**.
2. Versi `extversion` minimal `0.5.0`.
3. Di Dashboard → Database → Extensions, `vector` sudah bertanda **Enabled** (hijau).
4. Tidak ada error yang muncul di SQL Editor.

---

**Silakan salin prompt berikut, lalu paste ke Claude Code:**

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

**Verifikasi singkat:**

1. Query `SELECT * FROM pg_extension WHERE extname = 'vector';` mengembalikan **satu row**.
2. `extversion` minimal `0.5.0` (semakin baru semakin baik — yang penting sudah mendukung HNSW).
3. Kalau row-nya masih kosong, jalankan dulu `CREATE EXTENSION`, lalu coba verifikasi ulang.

---

## Prompt 2 — Migration: Tambah Embedding ke Tabel `transactions` + Function `match_transactions`

### Walkthrough Manual

Sekarang giliran kita **memodifikasi tabel `transactions` yang sudah ada** (dari Module 05). Kita akan menambahkan kolom `embedding`, index HNSW, plus function SQL `match_transactions` untuk semantic search — semuanya dalam satu file migration. Perlu dicatat: kita **bukan membuat tabel baru** — Fin-App tetap memakai tabel `transactions` sebagai satu-satunya sumber data per-user.

📂 **File baru**: `supabase/migrations/0004_transactions_semantic_search.sql` (silakan sesuaikan nomornya dengan urutan migration di project Anda).

**1. Defensive `CREATE EXTENSION`**

📍 Lokasi: **baris awal** migration. Idempotent — aman walaupun dijalankan ulang di environment yang masih fresh.

```sql
-- supabase/migrations/0004_transactions_semantic_search.sql
create extension if not exists vector;
```

**2. ALTER TABLE — Tambahkan kolom `embedding`**

📍 Lokasi: setelah `CREATE EXTENSION`. Kita pakai **nullable** karena row lama (yang dibuat sebelum Module 06) memang belum punya embedding — nanti akan diisi via backfill di latihan-3.

```sql
alter table public.transactions
  add column if not exists embedding vector(1024);  -- voyage-3
```

**3. Index HNSW pada kolom `embedding`**

📍 Lokasi: setelah `ALTER TABLE`. Kita memilih `vector_cosine_ops` karena di Prompt 2 tadi kita sudah menetapkan `<=>` sebagai default operator untuk teks.

```sql
create index if not exists transactions_embedding_idx
  on public.transactions
  using hnsw (embedding vector_cosine_ops);
```

> ⚠️ **Catatan penting**: operator class di index (`vector_cosine_ops`) harus **selaras** dengan operator yang dipakai di query (`<=>` di function `match_transactions` di bawah). Kalau nanti Anda query memakai `<->`, index ini tidak akan ikut terpakai.

**4. Function `match_transactions`**

📍 Lokasi: setelah `CREATE INDEX`. Function ini akan dipanggil dari TypeScript via `supabase.rpc("match_transactions", {...})`.

```sql
create or replace function public.match_transactions (
  query_embedding vector(1024),
  match_threshold float,
  match_count int
)
returns table (
  id          uuid,
  type        text,
  category    text,
  amount      numeric,
  description text,
  date        date,
  user_id     uuid,
  similarity  float
)
language sql stable
as $$
  select
    transactions.id,
    transactions.type,
    transactions.category,
    transactions.amount,
    transactions.description,
    transactions.date,
    transactions.user_id,
    1 - (transactions.embedding <=> query_embedding) as similarity
  from public.transactions
  where transactions.embedding is not null
    and 1 - (transactions.embedding <=> query_embedding) > match_threshold
  order by transactions.embedding <=> query_embedding asc
  limit match_count;
$$;
```

**5. Apply migration**

📍 Lokasi: terminal — silakan pilih workflow yang paling nyaman.

```bash
# opsi A — CLI
supabase db push

# opsi B — paste manual ke SQL Editor di Dashboard
```

### Yang sebaiknya tidak dilakukan

- ❌ **Membuat tabel baru** — cukup ALTER tabel `transactions` yang sudah ada dari Module 05.
- ❌ **Menambahkan `NOT NULL`** di kolom `embedding` — row lama belum punya embedding, jadi backfill akan kita lakukan terpisah.
- ❌ **Membuat index untuk operator lain** (`<->`, `<#>`) — di Fin-App kita konsisten pakai cosine, jadi satu index sudah cukup.
- ❌ **Menambah RLS policy baru** — policy untuk `transactions` dari Module 05 sudah otomatis berlaku untuk semantic search.
- ❌ **Membiarkan Claude menjalankan `supabase db push`** secara otomatis — sebaiknya Anda sendiri yang mengeksekusi supaya lebih terkontrol.

### Verifikasi setelah file dibuat

1. File `supabase/migrations/0004_transactions_semantic_search.sql` sudah ada di folder migration.
2. Migration berhasil di-apply (via CLI maupun paste manual ke SQL Editor).
3. Cek kolom: `\d transactions` di psql (atau Dashboard → Database → Tables → transactions) — kolom `embedding` bertipe `vector` sudah muncul.
4. Cek index: `SELECT indexname FROM pg_indexes WHERE tablename = 'transactions';` — `transactions_embedding_idx` ada di daftarnya.
5. Cek function: `SELECT proname FROM pg_proc WHERE proname = 'match_transactions';` — mengembalikan 1 row.
6. Coba jalankan ulang migration — tidak ada error sama sekali (sifat idempotent terbukti berkat `IF NOT EXISTS` dan `OR REPLACE`).

---

**Silakan salin prompt berikut, lalu paste ke Claude Code:**

```
Sekarang modifikasi tabel transactions (dari Module 05)
untuk semantic search: tambah kolom embedding + index HNSW
+ function match_transactions. Saya sudah paham operator
distance dari prompt sebelumnya — index pakai
vector_cosine_ops karena teks pakai cosine.

GOAL:
- Buat file baru supabase/migrations/0004_transactions_semantic_search.sql.
- Isi dengan 4 statement berurutan:

  1. CREATE EXTENSION IF NOT EXISTS vector; (idempotent
     defensive — aman kalau extension sudah aktif).

  2. ALTER TABLE public.transactions
     ADD COLUMN IF NOT EXISTS embedding vector(1024);
     (NULLABLE — row lama belum punya embedding, backfill
     terpisah di latihan-3).

  3. CREATE INDEX IF NOT EXISTS transactions_embedding_idx
     ON public.transactions
     USING hnsw (embedding vector_cosine_ops);

  4. CREATE OR REPLACE FUNCTION public.match_transactions(
       query_embedding vector(1024),
       match_threshold float,
       match_count int
     )
     RETURNS TABLE (
       id uuid, type text, category text, amount numeric,
       description text, date date, user_id uuid, similarity float
     )
     LANGUAGE sql STABLE
     AS $$
       SELECT
         transactions.id, transactions.type, transactions.category,
         transactions.amount, transactions.description, transactions.date,
         transactions.user_id,
         1 - (transactions.embedding <=> query_embedding) AS similarity
       FROM public.transactions
       WHERE transactions.embedding IS NOT NULL
         AND 1 - (transactions.embedding <=> query_embedding) > match_threshold
       ORDER BY transactions.embedding <=> query_embedding ASC
       LIMIT match_count;
     $$;

- Setelah file dibuat, beri saya instruksi cara apply
  migration ini (CLI `supabase db push` ATAU paste manual ke
  SQL Editor — apapun yang sesuai workflow project saya).

CONTEXT:
- Tabel transactions sudah ada dari Module 05 (kolom: id,
  user_id, date, category, type, amount, description, created_at).
- Naming migration mengikuti file 0001/0002/0003 yang sudah
  ada di supabase/migrations/.
- Dimensi 1024 sesuai voyage-3.
- Pgvector extension sudah diverifikasi aktif di Prompt 1.

GUARDRAIL:
- JANGAN bikin tabel baru — pakai transactions yang sudah ada.
- JANGAN bikin embedding NOT NULL — backfill di latihan-3.
- JANGAN otomatis jalankan supabase db push.
- JANGAN bikin index tambahan untuk operator lain (<->, <#>).
- JANGAN bikin RLS policy baru — policy transactions dari
  Module 05 sudah cukup.
- Pakai IF NOT EXISTS / OR REPLACE supaya idempotent.
```

**Verifikasi singkat:**

1. File `supabase/migrations/0004_transactions_semantic_search.sql` sudah ada.
2. Migration berhasil di-apply (via CLI atau paste ke SQL Editor) — tanpa error.
3. Cek kolom: di Dashboard → Database → Tables → `transactions` → kolom `embedding` bertipe `vector` sudah muncul.
4. Cek index: `SELECT indexname FROM pg_indexes WHERE tablename = 'transactions';` — `transactions_embedding_idx` ada.
5. Cek function: `SELECT proname FROM pg_proc WHERE proname = 'match_transactions';` — mengembalikan 1 row.
6. (Bonus) Coba panggil function dengan vector dummy:
   ```sql
   SELECT * FROM match_transactions(
     (SELECT array_agg(random())::vector FROM generate_series(1, 1024)),
     0.0,
     5
   );
   ```
   Hasilnya: 0 row (karena semua `embedding` masih NULL). Itu sudah benar — kita akan mengisi data di Prompt 3 berikutnya.

---

## Prompt 3 — Insert Dummy + Coba 3 Distance Operator di Tabel `transactions`

### Walkthrough Manual

Tabel sudah siap, index sudah berdiri, function sudah ada — sekarang waktunya **mengisi data dummy** dan **bermain dengan 3 distance operator** (`<=>`, `<->`, `<#>`) langsung di tabel sungguhan. Pola yang kita pakai persis seperti workflow asli: **setup → fill → query**. Setelah selesai, kita bersihkan dummy supaya tabel kembali bersih untuk latihan-3.

### Memahami 3 Distance Operator

Sebelum masuk ke SQL, mari pakai analogi sederhana supaya nyaman dengan ketiga operator ini:

#### 🧭 `<=>` Cosine distance — "Kompas"

Bayangkan setiap embedding adalah **panah** yang menunjuk dari pusat ruangan. Cosine peduli pada **arah panah**, bukan seberapa panjang. Dua orang di pinggir kota dengan kompas yang menunjuk arah sama → cosine bilang "mirip", walau jarak mereka jauh.

- **Range**: `0` (identik) sampai `2` (berlawanan arah).
- **Kapan dipakai**: default untuk **teks** (embedding teks dari Voyage/OpenAI selalu dinormalisasi, jadi cosine bekerja optimal).
- **Kasus pakai Fin-App**: cari transaksi yang "mirip artinya" — "ngopi" mirip dengan "beli kopi" walau katanya berbeda.

#### 📏 `<->` L2 (Euclidean) distance — "Tali pengukur"

Bayangkan menarik tali lurus dari titik A ke titik B di ruangan — itulah L2. Sensitif pada **jarak fisik aktual** antar titik, termasuk panjang masing-masing panah.

- **Range**: `0` (titik sama) sampai tak hingga (`∞`).
- **Kapan dipakai**: embedding **gambar** atau **audio** (yang panjangnya berbeda-beda dan justru bermakna).
- **Kasus pakai Fin-App**: jarang. Untuk teks, sebagian besar pakai cosine.

#### ⚡ `<#>` Negative inner product — "Kompas + magnet"

Mirip kompas (arah), tapi juga peduli **kekuatan sinyal** (panjang panah). Karena pgvector pakai konvensi `ORDER BY ASC = paling mirip`, hasilnya **ditandai negatif** — semakin negatif justru semakin mirip.

- **Range**: angka negatif (untuk vektor mirip) sampai positif (untuk berlawanan).
- **Kapan dipakai**: kalau performa kritis dan Anda **yakin vektor sudah dinormalisasi** — paling cepat di antara ketiganya.
- **Kasus pakai Fin-App**: optimasi production. Hasilnya hampir identik dengan cosine (untuk teks), tapi sedikit lebih hemat CPU.

#### Ringkasan Praktis

| Operator | Analogi | Untuk teks | Default? |
|---|---|---|---|
| `<=>` Cosine | Kompas — arah saja | ✅ Sangat cocok | ✅ Ya |
| `<->` L2 | Tali pengukur — jarak fisik | ⚠️ Bisa, tapi kurang ideal | ❌ |
| `<#>` Negative inner product | Kompas + kekuatan | ✅ Cocok (kalau dinormalisasi) | ❌ (alternatif optimasi) |

**TL;DR**: untuk semantic search teks di Fin-App, **gunakan `<=>` (cosine)**. Dua operator lain kita coba supaya Anda merasakan bedanya — bukan karena Fin-App akan memakainya.

---

📂 **Eksekusi di Supabase SQL Editor** (tidak ada file lokal yang berubah)

**1. Blok A — Insert 10 dummy transaksi dengan random embedding**

📍 Lokasi: SQL Editor → New query → paste → Run. Kita pakai prefix `DUMMY-` di `description` agar mudah dibedakan dan dihapus di akhir. Variasi 10 transaksi: 4 kopi/minuman, 2 transport, 1 tagihan, 1 belanja, 1 hiburan, 1 income.

```sql
-- Supabase SQL Editor — Blok A: insert 10 dummy
INSERT INTO public.transactions (type, category, amount, description, embedding) VALUES
  ('expense', 'Makanan & Minuman', 25000, 'DUMMY-ngopi di starbucks',
   (SELECT array_agg(random())::vector FROM generate_series(1, 1024))),
  ('expense', 'Makanan & Minuman', 18000, 'DUMMY-beli kopi sachet di indomaret',
   (SELECT array_agg(random())::vector FROM generate_series(1, 1024))),
  ('expense', 'Makanan & Minuman', 35000, 'DUMMY-ngopi sore di kedai depan kantor',
   (SELECT array_agg(random())::vector FROM generate_series(1, 1024))),
  ('expense', 'Makanan & Minuman', 45000, 'DUMMY-makan siang nasi padang',
   (SELECT array_agg(random())::vector FROM generate_series(1, 1024))),
  ('expense', 'Makanan & Minuman', 22000, 'DUMMY-jajan martabak telor',
   (SELECT array_agg(random())::vector FROM generate_series(1, 1024))),
  ('expense', 'Transportasi', 50000, 'DUMMY-bensin motor seminggu',
   (SELECT array_agg(random())::vector FROM generate_series(1, 1024))),
  ('expense', 'Transportasi', 25000, 'DUMMY-ojek online ke kantor',
   (SELECT array_agg(random())::vector FROM generate_series(1, 1024))),
  ('expense', 'Tagihan', 350000, 'DUMMY-bayar listrik bulanan',
   (SELECT array_agg(random())::vector FROM generate_series(1, 1024))),
  ('expense', 'Belanja', 250000, 'DUMMY-beli sepatu baru',
   (SELECT array_agg(random())::vector FROM generate_series(1, 1024))),
  ('income', 'Gaji & Pemasukan', 5000000, 'DUMMY-gaji bulanan kantor',
   (SELECT array_agg(random())::vector FROM generate_series(1, 1024)));
```

> 💡 Kita sengaja **menghilangkan `user_id`** (biarkan NULL) supaya tidak terikat ke user tertentu. Karena Anda menjalankan ini lewat SQL Editor (admin role), RLS policy tidak ikut menghalangi insert.

**2. Blok B — Cek hasil insert**

📍 Lokasi: SQL Editor — query baru.

```sql
-- Supabase SQL Editor — Blok B: cek 10 dummy + dimensi embedding
SELECT id, category, amount, description, vector_dims(embedding) AS dims
FROM public.transactions
WHERE description LIKE 'DUMMY-%'
ORDER BY category, description;
```

Yang Anda harapkan lihat: **10 baris**, semua dengan `dims = 1024`, dikelompokkan per kategori.

**3. Blok C — Cosine distance `<=>` (default untuk teks)**

📍 Lokasi: SQL Editor — query baru. Kita generate satu query vector random, lalu cari top-5 transaksi terdekat (dengan vektor random).

```sql
-- Supabase SQL Editor — Blok C: cosine (<=>)
WITH q AS (
  SELECT (SELECT array_agg(random())::vector FROM generate_series(1, 1024)) AS qvec
)
SELECT description, category, embedding <=> (SELECT qvec FROM q) AS cosine_distance
FROM public.transactions
WHERE description LIKE 'DUMMY-%'
ORDER BY embedding <=> (SELECT qvec FROM q)
LIMIT 5;
```

> 💡 **Catatan penting**: karena embedding kita masih **random**, urutan hasilnya pun random. Anda **belum akan** melihat "kopi" berkumpul atau "transport" berkumpul — itu wajar. Demo "cari kopi → muncul kopi" yang sesungguhnya akan terasa di latihan-3, setelah `embed()` terintegrasi ke pipeline insert dan search.

**4. Blok D — L2 (Euclidean) distance `<->`**

📍 Lokasi: SQL Editor — query baru. Strukturnya sama persis dengan Blok C, kita hanya **mengganti `<=>` menjadi `<->`** di dua tempat (SELECT + ORDER BY).

```sql
-- Supabase SQL Editor — Blok D: L2 (<->)
WITH q AS (
  SELECT (SELECT array_agg(random())::vector FROM generate_series(1, 1024)) AS qvec
)
SELECT description, category, embedding <-> (SELECT qvec FROM q) AS l2_distance
FROM public.transactions
WHERE description LIKE 'DUMMY-%'
ORDER BY embedding <-> (SELECT qvec FROM q)
LIMIT 5;
```

**5. Blok E — Negative inner product `<#>`**

📍 Lokasi: SQL Editor — query baru. Ganti operator sekali lagi.

```sql
-- Supabase SQL Editor — Blok E: negative inner product (<#>)
WITH q AS (
  SELECT (SELECT array_agg(random())::vector FROM generate_series(1, 1024)) AS qvec
)
SELECT description, category, embedding <#> (SELECT qvec FROM q) AS neg_inner_product
FROM public.transactions
WHERE description LIKE 'DUMMY-%'
ORDER BY embedding <#> (SELECT qvec FROM q)
LIMIT 5;
```

> 💡 Karena tiap blok memakai vektor query baru (`random()`), urutan top-5 antar blok wajar saja berbeda. Yang ingin kita amati di sini bukan "operator mana paling akurat" — melainkan **syntax** dan kenyataan bahwa **semuanya memakai pola `ORDER BY ... ASC LIMIT N`** (pattern wajib supaya HNSW index ikut terpakai).

**6. Blok F — Coba function `match_transactions`**

📍 Lokasi: SQL Editor — query baru. Sekarang kita panggil function yang dibuat di Prompt 2 supaya terasa alur RPC-nya.

```sql
-- Supabase SQL Editor — Blok F: panggil function
SELECT description, category, similarity
FROM match_transactions(
  (SELECT array_agg(random())::vector FROM generate_series(1, 1024)),
  0.0,    -- threshold longgar (terima semua skor)
  5
);
```

Yang Anda harapkan lihat: 5 baris dengan kolom `similarity` di range `0..1`. Urutannya **belum semantik** karena embedding masih random — hasil semantic search yang sesungguhnya akan terasa di latihan-3, setelah `embed()` terintegrasi ke pipeline insert.

**7. Cleanup — Hapus dummy**

📍 Lokasi: SQL Editor — query baru. Bersihkan dummy supaya tabel kembali rapi untuk latihan-3.

```sql
-- Supabase SQL Editor — cleanup dummy
DELETE FROM public.transactions WHERE description LIKE 'DUMMY-%';
```

### Yang sebaiknya tidak dilakukan

- ❌ Memakai `TRUNCATE transactions` untuk cleanup — itu akan menghapus **semua** transaksi termasuk milik user. Cukup `DELETE WHERE description LIKE 'DUMMY-%'`.
- ❌ Mengisi `user_id` dengan UUID acak — itu akan melanggar foreign key constraint ke `auth.users`. Biarkan saja `NULL`.
- ❌ Mengharapkan urutan semantik di Blok C/D/E — itu baru terasa di latihan-3 setelah `embed()` sungguhan menggantikan embedding random. Di sini fokus kita hanya memahami syntax & range nilai output.

### Verifikasi setelah eksekusi

1. Blok B mengembalikan **10 row** dummy, semua dengan `dims = 1024`.
2. Blok C mengembalikan 5 row dengan kolom `cosine_distance` di range `0..1` (urutan acak — wajar).
3. Blok D mengembalikan 5 row dengan kolom `l2_distance` jauh lebih besar (~5–10) — wajar, range L2 memang berbeda dari cosine.
4. Blok E mengembalikan 5 row dengan kolom `neg_inner_product` bertanda **negatif** (kira-kira `-300` sampai `-500`).
5. Blok F mengembalikan 5 row dari function `match_transactions` dengan kolom `similarity`.
6. Setelah cleanup, query `SELECT count(*) FROM public.transactions WHERE description LIKE 'DUMMY-%';` mengembalikan `0`.

---

**Silakan salin prompt berikut, lalu paste ke Claude Code:**

```
Tabel transactions sudah punya kolom embedding + index HNSW
+ function match_transactions (dari Prompt 2). Sekarang saya
ingin insert 10 dummy lalu mencoba 3 distance operator
(<=>, <->, <#>) langsung di tabel real, plus memanggil
function match_transactions, lalu cleanup.

GOAL:
- Beri saya 7 blok SQL untuk dijalankan manual di Supabase
  SQL Editor.

  BLOK A — INSERT 10 dummy ke transactions (kolom: type,
  category, amount, description, embedding). user_id
  biarkan NULL. Description pakai prefix 'DUMMY-' supaya
  mudah dibersihkan. Variasi: 4 kopi/minuman, 2 transport,
  1 tagihan, 1 belanja, 1 hiburan, 1 income. Embedding
  pakai (SELECT array_agg(random())::vector
  FROM generate_series(1, 1024)).

  BLOK B — SELECT id, category, amount, description,
  vector_dims(embedding) AS dims FROM transactions
  WHERE description LIKE 'DUMMY-%' ORDER BY category,
  description.

  BLOK C — Cosine distance <=>: top-5 dummy terdekat ke
  random query vector. Kolom hasil: cosine_distance.

  BLOK D — L2 <->: sama dengan C, ganti operator. Kolom
  hasil: l2_distance.

  BLOK E — Negative inner product <#>: sama dengan C,
  ganti operator. Kolom hasil: neg_inner_product.

  BLOK F — Panggil function match_transactions dengan
  threshold 0.0, limit 5. Tampilkan description + category
  + similarity.

  BLOK G — DELETE FROM transactions WHERE
  description LIKE 'DUMMY-%'.

CONTEXT:
- Tabel transactions sudah punya kolom embedding vector(1024)
  + index HNSW + function match_transactions dari Prompt 2.
- Pgvector mendukung 3 operator distance: <=>, <->, <#>.
- Pola wajib: ORDER BY <operator> ASC LIMIT N (agar HNSW
  index kepakai).
- Tujuan: pahami syntax + range nilai output tiap operator.
  Hasil semantik TIDAK relevan karena vector random — itu
  akan terasa di latihan-3 setelah embed() terintegrasi.

GUARDRAIL:
- JANGAN pakai TRUNCATE — bisa kena semua transaksi user.
- JANGAN isi user_id dengan UUID acak — biarkan NULL agar
  tidak melanggar foreign key.
- Filter WHERE description LIKE 'DUMMY-%' di tiap query
  agar tidak mencampur dengan transaksi real (kalau ada).
- Pakai 1024 dim (voyage-3) konsisten dengan Section 1.
```

**Verifikasi singkat:**

1. Setelah Blok A: `SELECT count(*) FROM transactions WHERE description LIKE 'DUMMY-%';` → 10.
2. Blok B: 10 row dengan `dims = 1024`.
3. Blok C: 5 row, `cosine_distance` di range `0..1` (urutan acak — wajar).
4. Blok D: 5 row, `l2_distance` jauh lebih besar (~5–10).
5. Blok E: 5 row, `neg_inner_product` bertanda negatif (~`-300` sampai `-500`).
6. Blok F: 5 row dari `match_transactions` dengan kolom `similarity`.
7. Setelah Blok G: `SELECT count(*) FROM transactions WHERE description LIKE 'DUMMY-%';` → 0.

---

## Validasi Akhir Section 2

Sebelum kita melanjut ke Section 3, mari pastikan semua sudah berdiri kokoh:

- [ ] Pgvector extension aktif dan versinya sudah dikonfirmasi (≥ 0.5.0).
- [ ] Migration `0004_transactions_semantic_search.sql` sudah ada dan ter-apply.
- [ ] Tabel `transactions` sudah punya kolom baru `embedding vector(1024)` (nullable).
- [ ] Index HNSW `transactions_embedding_idx` ada.
- [ ] Function `match_transactions` ada (cek via `pg_proc`).
- [ ] Migration aman dijalankan ulang — tidak ada error berkat sifat idempotent-nya.
- [ ] Anda sudah mencoba 3 distance operator (`<=>`, `<->`, `<#>`) di tabel `transactions` dengan 10 dummy data dan mengamati perbedaan range nilai output-nya.
- [ ] Function `match_transactions` sudah dipanggil minimal sekali dan mengembalikan kolom `similarity`.
- [ ] Dummy `DUMMY-%` sudah dibersihkan — tabel kembali rapi untuk latihan-3.

## Refleksi Section 2

Refleksikan pertanyaan berikut secara mendalam sebelum melanjutkan ke section berikutnya:

1. Mengapa kita memilih index HNSW alih-alih IVFFlat di migration ini?
2. Apa beda hasil `<=>` (cosine distance) dengan `<->` (L2) saat vektor sudah ternormalisasi (seperti output Voyage)?
3. Kalau nanti Anda berpindah dari voyage-3 ke OpenAI `text-embedding-3-large` (3072 dim), apa saja yang harus disesuaikan di tabel `transactions`?
4. Mengapa kolom `embedding` kita biarkan `nullable` daripada `NOT NULL DEFAULT '[]'::vector`? Apa risikonya kalau kita memakai default array kosong?
5. Index `transactions_embedding_idx` memakai `vector_cosine_ops`. Apa yang terjadi kalau Anda query dengan `ORDER BY embedding <-> $1` (L2) — apakah index ini ikut terpakai?
6. Di Prompt 3 kita memakai filter `WHERE description LIKE 'DUMMY-%'`. Kira-kira pre-filter seperti itu memengaruhi performa HNSW tidak? Kenapa?
7. Function `match_transactions` tidak menyertakan filter `WHERE user_id = auth.uid()`. Kalau dipanggil dari server action dengan supabase client yang sudah authenticated, apakah RLS policy `transactions` tetap berlaku? Bagaimana cara Anda memastikannya?

---

⬅️ Kembali: **[Section 1 — Implementasi Embedding](./latihan-1-implementasi-embedding.md)** · 🏠 Index: **[Module 06 — Latihan](./latihan.md)** · ➡️ Lanjut: **[Section 3 — Save Embedding To DB Vector](./latihan-3-save-embedding-db.md)**
