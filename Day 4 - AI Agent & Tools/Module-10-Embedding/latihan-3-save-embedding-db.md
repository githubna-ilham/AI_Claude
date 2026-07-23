# Section 3 — Save Embedding ke Tabel `transactions`

> Bagian dari **[Module 06 — Latihan](./latihan.md)**. Lanjutan dari **[Section 2 — Database Vector](./latihan-2-database-vector.md)**.

> Latihan untuk **menghubungkan `embed()`** dengan tabel `transactions` lewat 2 jalur: (1) modifikasi `quickAddTransaction` agar otomatis embed setiap insert baru, (2) pasang embedding di `createTransaction` & `updateTransaction` (`src/features/action.ts`) supaya form CRUD juga ikut menulis kolom `embedding`. Lalu verifikasi semantic search end-to-end. Tiga prompt siap copy-paste.
>
> **Estimasi**: 60–70 menit.

## Prasyarat Section 3

- [ ] Section 2 selesai. Tabel `transactions` punya kolom `embedding`, index HNSW, dan function `match_transactions` aktif.
- [ ] Section 1 selesai. Function `embed()` jalan dengan baik.
- [ ] Module 05 selesai. Server action `quickAddTransaction` ada di `src/features/quick-add.ts`.
- [ ] Anda sudah membaca bagian Section 3 di `materi.md`.

---

## 📚 Referensi Dokumentasi

Buka tab dokumentasi berikut sebagai referensi cepat selama Section 3:

- **[Supabase server actions (Next.js)](https://supabase.com/docs/guides/auth/server-side/nextjs)** — pattern `"use server"` + inisialisasi Supabase client.
- **[Supabase RPC reference](https://supabase.com/docs/reference/javascript/rpc)** — cara call function PostgreSQL dari JS/TS client.
- **[Supabase update reference](https://supabase.com/docs/reference/javascript/update)** — pattern UPDATE untuk backfill.
- **[Next.js Server Actions](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations)** — pattern call dari client + script.

---

## Prompt 1 — Modifikasi `quickAddTransaction` agar Embed `description` saat Insert

### Walkthrough Manual

Sebelum copy-paste prompt, pahami **perubahan minimal** di `src/features/quick-add.ts`. Tujuannya: setiap insert transaksi baru (via quick-add UI Module 05) **otomatis** menghasilkan `embedding` — tidak perlu backfill manual untuk data forward.

📂 **File yang dimodifikasi**: `src/features/quick-add.ts` (sudah ada dari Module 05 Section 5).

**1. Import `embed`**

📍 Lokasi: **bagian imports** di atas file, satu baris tambahan.

```ts
// src/features/quick-add.ts — imports
import { embed } from "@/lib/embeddings";   // ← tambahan
```

**2. Panggil `embed(transaction.note)` setelah parsing Claude**

📍 Lokasi: **di dalam `quickAddTransaction`**, setelah dapat `transaction` dari `toolUse.input` dan sebelum panggil `supabase.from("transactions").insert(...)`.

```ts
// src/features/quick-add.ts — di dalam quickAddTransaction
const transaction = toolUse.input as ParsedTransaction;

const embedding = await embed(transaction.note);    // ← tambahan
```

**3. Sertakan `embedding` di object insert**

📍 Lokasi: di `.insert({...})` yang sudah ada.

```ts
// src/features/quick-add.ts — modifikasi insert
const { error: insertError } = await supabase.from("transactions").insert({
  amount:      transaction.amount,
  type:        transaction.type,
  category:    transaction.category,
  date:        transaction.date,
  description: transaction.note,
  embedding,                                  // ← tambahan
});
```

**4. (Opsional) Handle error embedding tanpa blok insert**

📍 Lokasi: bungkus `embed()` di try/catch — kalau Voyage down, transaksi tetap tersimpan (embedding = NULL, bisa di-backfill nanti).

```ts
let embedding: number[] | null = null;
try {
  embedding = await embed(transaction.note);
} catch (err) {
  console.warn("[quickAddTransaction] embedding gagal, lanjut tanpa embedding:", err);
}
// ... insert dengan embedding (boleh null)
```

> 💡 **Trade-off**: pakai try/catch = transaksi user **tidak gagal** karena masalah eksternal (Voyage rate limit/down). Tapi ada **silent drift** — data tanpa embedding tidak ke-search. Untuk Fin-App, prioritas: jangan blokir user input. Backfill di Prompt 2 jadi safety net.

### Yang TIDAK perlu

- ❌ Tulis ulang seluruh `quickAddTransaction` — perubahan **maksimal 5 baris** (import + 1 call + 1 field di insert + optional try/catch).
- ❌ Modifikasi `prompts.ts`, tool schema, atau Claude API call — embedding **independen** dari parsing Claude.
- ❌ Tambah field embedding di `ParsedTransaction` type — embedding bukan output Claude, dihitung di server.
- ❌ Re-embed kalau user edit transaksi — di luar scope Section 3 (di-handle di Module 07 atau saat fitur edit dibuat).

### Verifikasi setelah file diubah

1. `npx tsc --noEmit` clean — tidak ada type error.
2. Reload Fin-App, buka halaman transaksi.
3. Quick-add: ketik "ngopi 5000" → Tambah → list refresh dengan transaksi baru.
4. Cek di Supabase SQL Editor:
   ```sql
   SELECT id, description, vector_dims(embedding) AS dims, created_at
   FROM transactions
   WHERE description = 'ngopi'
   ORDER BY created_at DESC LIMIT 1;
   ```
   → `dims = 1024`, transaksi paling baru sudah punya embedding non-null.
5. Coba quick-add 3–5 transaksi tambahan dengan variasi description ("bensin 50rb", "makan siang 35k", "beli buku 80000") untuk Section 3 lanjutan.

---

**Salin prompt berikut, paste ke Claude Code:**

```
Modifikasi server action quickAddTransaction (Module 05
Section 5) supaya setiap transaksi baru OTOMATIS punya
embedding di kolom transactions.embedding (yang ditambahkan
di Section 2 Module 06).

GOAL:
- Modifikasi file src/features/quick-add.ts.
- Perubahan minimal (≤5 baris):

  1. Import { embed } from "@/lib/embeddings".

  2. Di dalam quickAddTransaction, SETELAH dapat transaction
     dari toolUse.input dan SEBELUM panggil
     supabase.from("transactions").insert(...):

     const embedding = await embed(transaction.note);

  3. Tambahkan `embedding` di object .insert({...}).

  4. (OPSIONAL) Bungkus embed() dengan try/catch. Apabila
     gagal (Voyage down/rate limit), set embedding = null
     dan lanjut insert. Transaksi user TIDAK BOLEH gagal
     karena masalah Voyage — backfill jadi safety net.

CONTEXT:
- Tabel transactions sudah punya kolom embedding vector(1024)
  nullable (dari migration 0004 Section 2).
- Function embed() dari @/lib/embeddings sudah jalan (Section 1).
- Quick-add UI dari Module 05 Section 5 tetap berfungsi —
  perubahan ini transparan untuk user.

GUARDRAIL:
- JANGAN rewrite seluruh quickAddTransaction — hanya 3–5
  baris perubahan.
- JANGAN modifikasi prompts.ts, tool schema, atau Claude
  API call.
- JANGAN tambah field embedding di ParsedTransaction type
  — embedding dihitung di server, bukan output Claude.
- JANGAN re-embed kalau update transaksi — di luar scope.
```

**Verifikasi:**

1. `npx tsc --noEmit` clean.
2. Quick-add "ngopi 5000" via UI → tersimpan + list refresh.
3. SQL: `SELECT vector_dims(embedding) FROM transactions WHERE description = 'ngopi' ORDER BY created_at DESC LIMIT 1;` → `1024`.
4. Tidak ada error di terminal server.

---

## Prompt 2 — Embed di `createTransaction` & `updateTransaction` (`src/features/action.ts`)

### Walkthrough Manual

Selain quick-add (Prompt 1), Fin-App punya form CRUD manual untuk transaksi (dialog "Add transaction" + Edit). Server action-nya ada di `src/features/action.ts` — fungsi `createTransaction` dan `updateTransaction`. Supaya **setiap jalur insert/update** menghasilkan embedding (bukan cuma quick-add), kita pasang `embed()` di kedua function tersebut.

📂 **File yang dimodifikasi**: `src/features/action.ts` (sudah ada).

**1. Import `embed`**

📍 Lokasi: bagian imports.

```ts
// src/features/action.ts — imports
import { embed } from "@/lib/embeddings";   // ← tambahan
```

**2. Helper kecil untuk hitung embedding dari `description`**

📍 Lokasi: di atas function, atau inline. Dipakai di `createTransaction` dan `updateTransaction`. Bungkus try/catch supaya kegagalan Voyage tidak nge-block CRUD.

```ts
// src/features/action.ts — helper internal
async function safeEmbed(text: string | null): Promise<number[] | null> {
  if (!text) return null;
  try {
    return await embed(text);
  } catch (err) {
    console.warn("[action] embed gagal, lanjut tanpa vector:", err);
    return null;
  }
}
```

**3. Tambahkan `embedding` di `createTransaction` insert**

📍 Lokasi: `createTransaction`, sebelum `.insert(...)`. Pakai `parsed.data.description` sebagai sumber teks (sama dengan kolom yang disimpan).

```ts
// src/features/action.ts — createTransaction
const embedding = await safeEmbed(parsed.data.description || null);

const { error } = await supabase.from("transactions").insert({
  type:        parsed.data.type,
  category:    parsed.data.category,
  amount:      parsed.data.amount,
  description: parsed.data.description || null,
  date:        parsed.data.date,
  embedding,                                // ← tambahan
});
```

**4. Tambahkan `embedding` di `updateTransaction` update**

📍 Lokasi: `updateTransaction`, sebelum `.update(...)`. Karena user mungkin **mengubah** `description`, embedding lama jadi stale → re-embed wajib saat update.

```ts
// src/features/action.ts — updateTransaction
const embedding = await safeEmbed(parsed.data.description || null);

const { error } = await supabase
  .from("transactions")
  .update({
    type:        parsed.data.type,
    category:    parsed.data.category,
    amount:      parsed.data.amount,
    description: parsed.data.description || null,
    date:        parsed.data.date,
    embedding,                              // ← tambahan
  })
  .eq("id", id);
```

> 💡 **Kenapa di update juga?** Kalau user edit "ngopi" → "ngopi di Starbucks Plaza Senayan", makna semantik berubah cukup banyak. Kalau embedding tidak di-refresh, semantic search akan return hasil yang nyasar. Cost: 1 Voyage call per update — masih murah untuk CRUD manual yang frekuensinya rendah.

### Yang TIDAK perlu

- ❌ Modifikasi `getTransactions`, `deleteTransaction`, `getBalanceSummary` — tidak ada insert/update di sana.
- ❌ Cek "apakah description berubah?" sebelum re-embed — over-engineering, embed call sudah cepat. Optimasi diff nanti kalau pernah jadi bottleneck.
- ❌ Tulis ulang `TransactionInputSchema` — schema input tidak ditambah field embedding (sama seperti `ParsedTransaction` di Prompt 1).
- ❌ Buat helper terpisah di file lain — `safeEmbed` cukup di-define lokal di `action.ts`.

### Verifikasi setelah file diubah

1. `npx tsc --noEmit` clean.
2. Reload Fin-App, klik **"Add transaction"** → isi form → Simpan.
3. Cek di Supabase:
   ```sql
   SELECT id, description, vector_dims(embedding) AS dims, created_at
   FROM transactions
   ORDER BY created_at DESC LIMIT 3;
   ```
   → transaksi paling baru punya `dims = 1024`.
4. Edit salah satu transaksi (ubah `description`), klik Simpan. Ulangi query SQL → row tersebut `dims` tetap 1024, dan embedding-nya berubah (kalau mau dibandingkan secara eksplisit, simpan vektor lama sebelum edit).
5. Tidak ada error di terminal server.

---

**Salin prompt berikut, paste ke Claude Code:**

```
Tambahkan generate embedding di server actions
createTransaction dan updateTransaction di
src/features/action.ts. Setiap insert dan update wajib
menulis kolom transactions.embedding berdasarkan field
description.

GOAL:
- Modifikasi src/features/action.ts.
- Perubahan minimal:
  1. Import { embed } from "@/lib/embeddings".
  2. Tambahkan helper internal safeEmbed(text):
     - Return null kalau text falsy.
     - Bungkus embed() dengan try/catch; gagal → log warn,
       return null.
  3. Di createTransaction, SEBELUM .insert(...):
     - const embedding = await safeEmbed(parsed.data.description || null);
     - tambahkan field `embedding` di object insert.
  4. Di updateTransaction, SEBELUM .update(...):
     - const embedding = await safeEmbed(parsed.data.description || null);
     - tambahkan field `embedding` di object update.

CONTEXT:
- Tabel transactions punya kolom embedding vector(1024)
  nullable (migration Section 2).
- Function embed() dari @/lib/embeddings sudah jalan.
- TransactionInputSchema sudah ada — JANGAN diubah.
- Form CRUD (Add/Edit dialog) mengirim TransactionInput
  yang sudah include description.

GUARDRAIL:
- JANGAN modifikasi getTransactions, deleteTransaction,
  getBalanceSummary — di luar scope.
- JANGAN tambah field embedding di TransactionInputSchema.
- JANGAN throw kalau embed() gagal — safeEmbed return null
  agar CRUD tidak ke-block oleh Voyage rate limit / down.
- JANGAN cek diff description lama vs baru di update —
  selalu re-embed.
- JANGAN buat backfill script di prompt ini.
```

**Verifikasi:**

1. `npx tsc --noEmit` clean.
2. Add transaction via form → SQL `SELECT vector_dims(embedding) FROM transactions ORDER BY created_at DESC LIMIT 1;` → `1024`.
3. Edit transaction (ubah description) → row punya embedding non-null setelah save.
4. Tidak ada error di terminal saat insert/update.

---

## Prompt 3 — Verifikasi Semantic Search End-to-End

### Walkthrough Manual

Sekarang fondasi siap: ALTER + index + function (Section 2) + auto-embed di quick-add (Prompt 1) + auto-embed di CRUD (Prompt 2). Test akhir: bikin helper TypeScript `searchTransactions(query)` (dipakai dari Server Action / route handler nanti), lalu script test standalone yang memvalidasi RPC end-to-end di terminal.

📂 **File baru**: `src/features/search-transactions.ts` + script `scripts/test-search.ts`.

**1. Helper `searchTransactions` (untuk dipakai dari Server Action)**

📍 Lokasi: file baru `src/features/search-transactions.ts`. `'use server'` di baris pertama karena pakai `embed()` yang server-only.

```ts
// src/features/search-transactions.ts
"use server";

import { embed } from "@/lib/embeddings";
import { createClient } from "@/lib/supabase/server";

export type TransactionMatch = {
  id: string;
  type: "expense" | "income";
  category: string;
  amount: number;
  description: string;
  date: string;
  user_id: string | null;   // nullable — project belum punya login
  similarity: number;
};

export async function searchTransactions(
  query: string,
  opts: { threshold?: number; limit?: number } = {},
): Promise<TransactionMatch[]> {
  const { threshold = 0.5, limit = 5 } = opts;

  const queryEmbedding = await embed(query);
  const supabase = await createClient();

  const { data, error } = await supabase.rpc("match_transactions", {
    query_embedding: queryEmbedding,
    match_threshold: threshold,
    match_count: limit,
  });

  if (error) throw new Error(`searchTransactions failed: ${error.message}`);
  return (data ?? []) as TransactionMatch[];
}
```

**2. Script test standalone** — **JANGAN reuse helper di atas**

📍 Lokasi: file baru `scripts/test-search.ts`. Helper di langkah 1 pakai `createClient` dari `@/lib/supabase/server` yang panggil `cookies()` Next.js — ini **akan crash** di Node script standalone (`cookies was called outside a request scope`). Solusi: di script, buat supabase client langsung dari `@supabase/supabase-js` dan duplikasi logic `embed + rpc` di sini.

Tambahan kendala teknis di Node 20:
- `supabase-js` constructor inisialisasi `RealtimeClient` yang butuh global `WebSocket` (Node 20 belum punya native). Stub no-op cukup karena script ini hanya pakai RPC, bukan realtime.
- `embed()` import `server-only` → jalankan tsx dengan flag `--conditions=react-server`.
- Tanpa payment method di Voyage, rate limit = 3 RPM → throttle ~22 detik antar call.

```ts
// scripts/test-search.ts

// Node 20 belum punya `WebSocket` global; supabase-js init RealtimeClient
// di constructor. Script tidak pakai realtime → stub no-op cukup.
if (typeof (globalThis as { WebSocket?: unknown }).WebSocket === "undefined") {
  (globalThis as { WebSocket?: unknown }).WebSocket = class {
    constructor() {
      /* no-op */
    }
  };
}

import { createClient } from "@supabase/supabase-js";

import { embed } from "@/lib/embeddings";

type TransactionMatch = {
  id: string;
  type: "expense" | "income";
  category: string;
  amount: number;
  description: string;
  date: string;
  user_id: string | null;
  similarity: number;
};

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!,
);

const QUERIES = ["kopi", "makanan", "minuman hangat"];

function formatRp(n: number) {
  return `Rp ${n.toLocaleString("id-ID")}`;
}

async function searchTransactions(
  query: string,
  opts: { threshold?: number; limit?: number } = {},
): Promise<TransactionMatch[]> {
  const { threshold = 0.3, limit = 5 } = opts;

  const queryEmbedding = await embed(query);

  const { data, error } = await supabase.rpc("match_transactions", {
    query_embedding: queryEmbedding,
    match_threshold: threshold,
    match_count: limit,
  });

  if (error) throw new Error(`searchTransactions failed: ${error.message}`);
  return (data ?? []) as TransactionMatch[];
}

// Voyage tanpa payment method: 3 RPM. Throttle ~22 detik antar call.
const THROTTLE_MS = 22_000;
const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));

async function main() {
  for (let i = 0; i < QUERIES.length; i++) {
    const q = QUERIES[i];
    console.log(`\n=== Query: "${q}" ===`);

    const results = await searchTransactions(q, { threshold: 0.3, limit: 5 });

    if (results.length === 0) {
      console.log("(tidak ada hasil di atas threshold)");
    } else {
      console.table(
        results.map((r) => ({
          note: r.description,
          category: r.category,
          amount: formatRp(r.amount),
          similarity: r.similarity.toFixed(3),
        })),
      );
    }

    if (i < QUERIES.length - 1) {
      console.log(`(throttle ${THROTTLE_MS / 1000}s untuk hindari 429)`);
      await sleep(THROTTLE_MS);
    }
  }
}

main().catch(console.error);
```

**3. Run**

📍 Lokasi: terminal.

```bash
npx tsx --conditions=react-server --env-file=.env.local scripts/test-search.ts
```

> 💡 **Pilih query yang KONKRET dan SEMANTIK related dengan data Anda.** Description Fin-App pendek (≤30 char) seperti "Pizza", "Ngopi". Similarity terhadap query abstrak/kategorial seperti `"expense bulan ini"` atau `"pengeluaran besar"` cenderung sangat rendah (≤ 0.2) — itu bukan kasus semantic search, tapi **filter struktural** (date/type) yang akan dibahas di Module 07 (hybrid search). Untuk demo Section 3 ini, pakai query sinonim (`"kopi"` → "Ngopi"), kategori (`"makanan"` → "Pizza"), atau metafora (`"minuman hangat"` → "Ngopi").

### Catatan threshold yang realistis (Fin-App)

| Range threshold | Recall | Cocok untuk |
|---|---|---|
| **0.5 – 0.7** | rendah | Query sinonim langsung ("kopi" → "Ngopi") |
| **0.3 – 0.5** | sedang | Query kategori ("makanan" → "Pizza/Ngopi") |
| **< 0.3** | tinggi (noise) | Hanya untuk eksplorasi / threshold sangat longgar |

Default `searchTransactions` di-set ke **0.5**, tapi script test pakai **0.3** supaya query kategori tetap dapat hasil. Sesuaikan saat dipakai di fitur produk berdasarkan UX.

### Catatan otentikasi

Project Fin-App di kursus ini **belum punya login/autentikasi**, jadi kolom `user_id` di setiap transaksi bernilai `NULL`. Semua row "milik bersama" dan ikut muncul di hasil pencarian. Kalau di iterasi berikutnya menambahkan login + RLS, function `match_transactions` perlu di-update agar memfilter `user_id = auth.uid()`.

### Yang TIDAK perlu

- ❌ Bikin UI search bar lengkap — itu Module 07.
- ❌ Modifikasi `match_transactions` — function dari Section 2 sudah cukup.
- ❌ Tambah filter date / category di Prompt ini — hybrid filter di Module 07.
- ❌ Caching hasil search — out of scope.
- ❌ Pagination — `limit` 5 cukup untuk demonstrasi.
- ❌ Reuse helper Server Action di script — `cookies()` Next.js tidak available di Node standalone, **harus** duplikasi logic.

### Verifikasi setelah semua dijalankan

1. File `src/features/search-transactions.ts` ada dengan `"use server"`.
2. `npx tsc --noEmit` clean.
3. Script `scripts/test-search.ts` jalan tanpa error (5 queries × throttle = ~2 menit).
4. Query `"kopi"` → top-1 hasil punya `description` mengandung "kopi"/"ngopi" dengan similarity ≥ ~0.6.
5. Query `"makanan"` → muncul transaksi makanan ("Pizza", "Makan di warteg", dst) dengan similarity ≥ ~0.4.
6. Query `"minuman hangat"` (metafora) → tetap match "Ngopi" — bukti embedding menangkap makna semantik, bukan keyword.

---

**Salin prompt berikut, paste ke Claude Code:**

```
Bikin helper TypeScript searchTransactions yang panggil
function match_transactions via Supabase RPC, lalu script
test STANDALONE untuk verifikasi semantic search end-to-end.

GOAL:
- File 1: src/features/search-transactions.ts ("use server"):
  - Type TransactionMatch = { id, type, category, amount,
    description, date, user_id, similarity }.
    user_id WAJIB string | null (project belum punya auth).
  - Function searchTransactions(query: string, opts?: {
    threshold?: number; limit?: number }) returns
    Promise<TransactionMatch[]>.
  - Default opts: threshold = 0.5, limit = 5.
  - Internal: embed(query) → createClient() dari
    @/lib/supabase/server → supabase.rpc("match_transactions",
    { query_embedding, match_threshold, match_count }).
  - throw kalau error, return data.

- File 2: scripts/test-search.ts (STANDALONE, JANGAN reuse
  helper File 1):
  - DUPLIKASI logic embed + rpc di sini karena Next.js
    cookies() (yang dipakai @/lib/supabase/server) tidak
    available di Node script.
  - Pakai createClient dari "@supabase/supabase-js" (bukan
    yang dari @/lib/supabase/server).
  - Stub global WebSocket (Node 20 tidak punya native, dan
    supabase-js init RealtimeClient di constructor).
  - Throttle ~22 detik antar query (Voyage 3 RPM tanpa
    payment method).
  - 3 query konkret yang related dengan data demo:
    "kopi", "makanan", "minuman hangat".
  - Threshold 0.3, limit 5 (description Fin-App pendek,
    threshold tinggi terlalu strict).
  - console.table hasil: note (dari description), category,
    amount (formatted Rp id-ID), similarity (3 desimal).
  - Apabila kosong, log "(tidak ada hasil di atas threshold)".

- Jalankan:
  npx tsx --conditions=react-server --env-file=.env.local
  scripts/test-search.ts

  Flag --conditions=react-server diperlukan karena
  src/lib/embeddings.ts pakai directive `'use server'`.

CONTEXT:
- Function match_transactions sudah ada di Supabase (Section 2).
- Transaksi sudah punya embedding (Prompt 1 + 2).
- Node v20 (tidak punya WebSocket native).
- Voyage tanpa payment method: 3 RPM.

GUARDRAIL:
- JANGAN modifikasi match_transactions SQL function.
- JANGAN bikin UI search bar — itu Module 07.
- JANGAN tambah filter date / category di RPC call —
  hybrid filter di Module 07.
- JANGAN reuse @/lib/supabase/server di scripts/test-search.ts
  — cookies() tidak available di Node standalone.
- JANGAN asumsikan ada login/session — kolom user_id
  semuanya NULL.
- JANGAN pakai query abstrak/kategorial seperti "expense
  bulan ini" — similarity-nya rendah karena description
  Fin-App pendek dan konkret. Pakai query sinonim/kategori.
```

**Verifikasi:**

1. File `src/features/search-transactions.ts` ada dengan `"use server"`.
2. Script jalan tanpa error: `npx tsx --conditions=react-server --env-file=.env.local scripts/test-search.ts`.
3. Query "kopi" → top hit "Ngopi" / "Kopi ..." similarity ≥ ~0.6.
4. Query "makanan" → muncul transaksi makanan (similarity ≥ ~0.4).
5. Query "minuman hangat" (metafora) → tetap match "Ngopi" — bukti semantic vs keyword.

---

## Validasi Akhir Section 3

- [ ] `quickAddTransaction` di `src/features/quick-add.ts` punya tambahan `import embed` + `const embedding = await embed(...)` + field `embedding` di insert.
- [ ] Quick-add via UI menghasilkan transaksi baru dengan `embedding` non-null (verifikasi via SQL).
- [ ] `createTransaction` & `updateTransaction` di `src/features/action.ts` ikut menulis kolom `embedding` (via helper `safeEmbed`).
- [ ] Add transaction via form CRUD menghasilkan row dengan `embedding` non-null. Edit transaksi → embedding ter-refresh.
- [ ] `src/features/search-transactions.ts` ada dengan helper `searchTransactions`.
- [ ] `scripts/test-search.ts` jalan dengan flag `--conditions=react-server` dan menghasilkan top-K relevan untuk query konkret (mis. "kopi" → "Ngopi" dengan similarity ≥ 0.6).
- [ ] `npx tsc --noEmit` clean.

## Refleksi Section 3

1. `safeEmbed` di Prompt 2 selalu return null saat Voyage gagal. Apa konsekuensi: row akan punya `embedding IS NULL` dan tidak masuk hasil semantic search. Bagaimana cara mendeteksi & memperbaiki row-row ini di kemudian hari (mis. job berkala)?
2. Di Prompt 1 & 2, kami pakai try/catch di sekitar `embed()`. Apa konsekuensi UX kalau gagal — apakah user lihat error? Apakah ada cara komunikasikan ke user bahwa "transaksi tersimpan tapi belum bisa di-search"?
3. Untuk query "kopi", apakah Claude masih bisa membedakan antara "ngopi di kedai" vs "beli kopi bubuk untuk di rumah"? Apa yang menentukan?
4. Threshold default 0.5. Apa yang terjadi kalau Anda naikkan ke 0.8 atau turunkan ke 0.2? Test di script `test-search.ts`.
5. Kalau user nanti edit `description` transaksi (misal "ngopi" → "ngopi di starbucks"), embedding lama jadi stale. Bagaimana strategi handle update? (trigger DB? application-layer? batch re-embed periodik?)
6. Apa langkah pertama yang Anda bayangkan untuk Module 07 (RAG) — gabungkan hasil `searchTransactions` dengan AI Financial Advisor chatbot dari Module 05?

---

⬅️ Kembali: **[Section 2 — Database Vector](./latihan-2-database-vector.md)** · 🏠 Index: **[Module 06 — Latihan](./latihan.md)** · ➡️ Lanjut: **Module 07 — RAG** (akan datang)
