# Section 1 — Retrieval Helper untuk Chatbot

> Bagian dari **[Module 07 — Latihan](./latihan.md)**. Asumsi **[Module 06](../Module-06-Embedding/latihan.md)** sudah selesai.

> Di section ini kita membangun **retrieval helper** `retrieveContextForChatbot(query)` yang membungkus `searchTransactions` (dari Module 06) lalu memformat hasilnya menjadi string konteks yang siap disisipkan ke system prompt Claude. Dua prompt siap copy-paste.
>
> **Alur belajarnya**: bikin helper format → coba lewat script test. Hasil akhirnya: satu function yang panggil-saja dari mana pun di app.
>
> **Estimasi waktu**: 30–40 menit.

## Prasyarat Section 1

- [ ] Module 06 selesai. Function `searchTransactions` ada di `src/features/search-transactions.ts` dan jalan dengan baik.
- [ ] Tabel `transactions` punya data nyata (dari quick-add atau backfill). Minimal 5–10 transaksi supaya retrieval terasa.
- [ ] Anda sudah membaca bagian "Konsep RAG" + Section 1 di `materi.md`.

---

## 📚 Referensi Dokumentasi

Tab-tab dokumentasi berikut bagus untuk dibuka di samping sebagai teman selama Section 1:

- **[Anthropic RAG cookbook](https://github.com/anthropics/anthropic-cookbook/tree/main/skills/retrieval_augmented_generation)** — contoh format konteks yang efektif untuk Claude.
- **[Voyage AI docs](https://docs.voyageai.com/)** — referensi cepat embed() yang sudah kita pakai di Module 06.
- **[Supabase RPC reference](https://supabase.com/docs/reference/javascript/rpc)** — pattern call function `match_transactions`.

---

## Prompt 1 — Bikin `retrieveContextForChatbot` di `src/features/rag-context.ts`

### Walkthrough Manual

Sebelum kita kirim prompt ke Claude, mari pahami **bentuk akhir helper**: satu function async yang menerima query user, mengembalikan **string** siap inject ke system prompt. Tidak lebih, tidak kurang.

📂 **File baru**: `src/features/rag-context.ts`.

**1. Directive + imports**

📍 Lokasi: baris awal file. `"use server"` karena memanggil `embed()` (server-only).

```ts
// src/features/rag-context.ts — baris awal
"use server";

import {
  searchTransactions,
  type TransactionMatch,
} from "@/features/search-transactions";
```

**2. Marker untuk kasus tanpa hasil**

📍 Lokasi: module-level constant. String penanda ini akan diakui oleh `ADVISOR_RAG_INSTRUCTION` di Section 2 supaya Claude tidak mengarang ketika konteks kosong.

```ts
export const NO_CONTEXT_MARKER = "(tidak ada transaksi yang relevan ditemukan)";
```

**3. Function `retrieveContextForChatbot`**

📍 Lokasi: export top-level. Default threshold `0.5`, limit `5` — angka ini sweet spot untuk dataset puluhan/ratusan transaksi.

```ts
export async function retrieveContextForChatbot(
  userQuery: string,
  opts: { threshold?: number; limit?: number } = {}
): Promise<string> {
  const matches = await searchTransactions(userQuery, {
    threshold: opts.threshold ?? 0.5,
    limit: opts.limit ?? 5,
  });

  if (matches.length === 0) return NO_CONTEXT_MARKER;

  return matches.map(formatTransactionForContext).join("\n");
}
```

**4. Helper format per row**

📍 Lokasi: module-level helper. Format: satu baris per transaksi, semua field penting + similarity score (opsional, membantu debugging awal).

```ts
function formatTransactionForContext(m: TransactionMatch): string {
  const amount = `Rp ${m.amount.toLocaleString("id-ID")}`;
  return `- ${m.date} | ${m.category} | ${m.type} | ${amount} | "${m.description}" (similarity: ${m.similarity.toFixed(2)})`;
}
```

> 💡 **Kenapa format multiline plain text?** Claude membaca teks paling baik. Kalau dipaksa JSON, ia akan parse mental dulu — boros token. Format `- field | field | ...` cukup natural dan kompak.

### Yang sebaiknya tidak dilakukan

- ❌ Memodifikasi `searchTransactions` — biarkan apa adanya. `rag-context.ts` adalah pembungkus, bukan refactor.
- ❌ Return array atau object — return string. Konsumen helper ini (Section 3) butuh string, bukan object.
- ❌ Menyertakan kolom `id` / `user_id` di output — Claude tidak butuh, hanya menambah noise.
- ❌ Caching di sini — `embed()` di Module 06 sudah punya strategi caching. Tidak perlu lapis tambahan.

### Verifikasi setelah file dibuat

1. File `src/features/rag-context.ts` ada dengan `"use server"` di baris pertama.
2. Export `retrieveContextForChatbot`, `NO_CONTEXT_MARKER`.
3. `npx tsc --noEmit` clean.
4. Tidak ada hardcoded threshold/limit — semua via parameter dengan default.

---

**Silakan salin prompt berikut, lalu paste ke Claude Code:**

```
Bikin retrieval helper untuk chatbot RAG: function yang
panggil searchTransactions (Module 06) dan format hasilnya
jadi string konteks siap inject ke system prompt.

GOAL:
- Buat file baru src/features/rag-context.ts.
- Baris pertama: "use server";
- Export const NO_CONTEXT_MARKER =
  "(tidak ada transaksi yang relevan ditemukan)".
- Export async function retrieveContextForChatbot(
    userQuery: string,
    opts: { threshold?: number; limit?: number } = {}
  ): Promise<string>
  Alur:
  1. Panggil searchTransactions(userQuery, {
       threshold: opts.threshold ?? 0.5,
       limit: opts.limit ?? 5,
     }).
  2. Apabila matches.length === 0, return NO_CONTEXT_MARKER.
  3. Map setiap match jadi format:
     "- {date} | {category} | {type} | Rp {amount.toLocaleString('id-ID')} | \"{description}\" (similarity: {similarity.toFixed(2)})"
  4. Join dengan "\n", return string.

CONTEXT:
- searchTransactions sudah ada di @/features/search-transactions
  (Module 06 Section 3), return TransactionMatch[].
- TransactionMatch fields: id, type, category, amount, description,
  date, user_id, similarity.
- Format konteks pakai Indonesian Rupiah (toLocaleString id-ID).
- File ini hanya wrapper format — JANGAN modifikasi
  searchTransactions.

GUARDRAIL:
- JANGAN return array atau object — return string siap pakai.
- JANGAN sertakan kolom id/user_id di output — Claude tidak butuh,
  hanya menambah noise & token cost.
- JANGAN tambah caching di sini — embed() di Module 06 sudah
  punya strategi caching.
- JANGAN modifikasi searchTransactions atau match_transactions.
```

**Verifikasi singkat:**

1. File `src/features/rag-context.ts` ada dengan `"use server"`.
2. Export `retrieveContextForChatbot`, `NO_CONTEXT_MARKER`.
3. `npx tsc --noEmit` clean.

---

## Prompt 2 — Script Test `scripts/test-rag-context.ts`

### Walkthrough Manual

Sebelum dipakai di route chatbot, mari pastikan helper-nya menghasilkan format yang masuk akal dengan beberapa query realistis.

📂 **File baru**: `scripts/test-rag-context.ts`.

**1. Imports + array query**

📍 Lokasi: top-level file. Variasi query: ada yang harus ketemu (kalau data Anda berisi kopi/transport), ada yang sengaja "off-topic" supaya marker muncul.

```ts
// scripts/test-rag-context.ts
import { retrieveContextForChatbot } from "@/features/rag-context";

const QUERIES = [
  "kopi minggu lalu",
  "pengeluaran transportasi",
  "bayar tagihan listrik",
  "pesawat ke jepang",  // sengaja off-topic untuk uji NO_CONTEXT_MARKER
];

async function main() {
  for (const q of QUERIES) {
    console.log(`\n=== Query: "${q}" ===`);
    const context = await retrieveContextForChatbot(q, {
      threshold: 0.4,
      limit: 5,
    });
    console.log(context);
  }
}

main().catch(console.error);
```

**2. Run**

📍 Lokasi: terminal di root project.

```bash
npx tsx --env-file=.env.local scripts/test-rag-context.ts
```

**3. Output yang diharapkan**

Untuk query yang ada data-nya, output sekitar:

```
=== Query: "kopi minggu lalu" ===
- 2026-06-23 | Makanan & Minuman | expense | Rp 25.000 | "ngopi di starbucks" (similarity: 0.85)
- 2026-06-22 | Makanan & Minuman | expense | Rp 18.000 | "beli kopi sachet di indomaret" (similarity: 0.81)
- 2026-06-20 | Makanan & Minuman | expense | Rp 35.000 | "ngopi sore di kedai depan kantor" (similarity: 0.78)
```

Untuk query off-topic:

```
=== Query: "pesawat ke jepang" ===
(tidak ada transaksi yang relevan ditemukan)
```

### Yang sebaiknya tidak dilakukan

- ❌ Bikin UI test — script CLI cukup untuk verifikasi format. UI test ada di Section 3.
- ❌ Asumsi data Anda persis sama dengan contoh — silakan ganti `QUERIES` sesuai data nyata Anda.
- ❌ Commit script ini ke production — ini hanya untuk verifikasi Section 1, boleh dihapus setelah selesai.

### Verifikasi setelah script dijalankan

1. Untuk minimal 2 dari 4 query, muncul daftar transaksi yang masuk akal secara semantik.
2. Untuk query off-topic, muncul `(tidak ada transaksi yang relevan ditemukan)`.
3. Format setiap baris konsisten: `- date | category | type | Rp amount | "description" (similarity: X.XX)`.
4. Tidak ada error TypeScript atau runtime.

---

**Silakan salin prompt berikut, lalu paste ke Claude Code:**

```
Bikin script test untuk verifikasi retrieveContextForChatbot
dengan 4 query (3 yang harus ada data, 1 sengaja off-topic).

GOAL:
- Buat file scripts/test-rag-context.ts.
- Import retrieveContextForChatbot dari @/features/rag-context.
- Array QUERIES = [
    "kopi minggu lalu",
    "pengeluaran transportasi",
    "bayar tagihan listrik",
    "pesawat ke jepang"  // off-topic
  ].
- async function main(): loop tiap query, log
  '=== Query: "..." ===', call retrieveContextForChatbot
  dengan { threshold: 0.4, limit: 5 }, log hasil.
- main().catch(console.error).
- Jalankan dengan:
  npx tsx --env-file=.env.local scripts/test-rag-context.ts

CONTEXT:
- retrieveContextForChatbot return string (multiline atau
  NO_CONTEXT_MARKER).
- Tabel transactions sudah berisi data nyata dari Module 06.

GUARDRAIL:
- JANGAN modifikasi retrieveContextForChatbot.
- JANGAN bikin UI test — CLI cukup.
- Threshold 0.4 (sedikit longgar) supaya bisa lihat hasil
  edge case juga.
```

**Verifikasi singkat:**

1. Script jalan tanpa error.
2. 3 query pertama memunculkan transaksi yang masuk akal.
3. Query off-topic memunculkan `(tidak ada transaksi yang relevan ditemukan)`.
4. Format output konsisten satu baris per transaksi.

---

## Validasi Akhir Section 1

Sebelum kita melanjut ke Section 2, mari pastikan helper retrieval sudah berdiri kokoh:

- [ ] File `src/features/rag-context.ts` ada dengan `"use server"`, export `retrieveContextForChatbot` + `NO_CONTEXT_MARKER`.
- [ ] `npx tsc --noEmit` clean.
- [ ] Script test berjalan dan memunculkan output yang masuk akal untuk minimal 3 dari 4 query.
- [ ] Marker `NO_CONTEXT_MARKER` muncul untuk query off-topic.
- [ ] Tidak ada perubahan di `searchTransactions` atau `match_transactions` (Section 1 ini murni pembungkus baru).

## Refleksi Section 1

Refleksikan pertanyaan berikut secara mendalam sebelum melanjutkan ke section berikutnya:

1. Default `threshold = 0.5` dan `limit = 5`. Apa konsekuensi kalau Anda turunkan threshold ke `0.3` (lebih longgar) atau naikkan ke `0.7` (lebih ketat)? Bagaimana ini mempengaruhi kualitas jawaban Claude nanti?
2. Format konteks kita pakai pipe-separated multiline. Kalau diganti markdown table atau JSON, apa trade-off-nya (token cost, parsing oleh Claude, readability log)?
3. Kita menyertakan `similarity` di output. Apakah Claude pakai angka itu untuk apa-apa, atau itu hanya untuk Anda saat debugging?
4. `NO_CONTEXT_MARKER` ditulis sebagai string Bahasa Indonesia. Apa risikonya kalau marker-nya berbahasa Inggris (mis. "no relevant transactions found")? Apa konsekuensinya untuk Claude yang menjawab dalam Bahasa Indonesia?

---

⬅️ Kembali: **[Module 07 — Latihan](./latihan.md)** · 🏠 Index: **[Day 4](../README.md)** · ➡️ Lanjut: **[Section 2 — Implementasi RAG di Chatbot](./latihan-2-rag-chatbot.md)**
