# Section 2 — Sample Parameter & Output Control

> Bagian dari **[Module 05 — Latihan](./latihan.md)**. Lanjutan dari **[Section 1 — System Instruction](./latihan-1-system-instruction.md)**.

> Latihan ini membangun fitur **Parse Transaksi via AI** secara bertahap — dari parser stand-alone, ke server action dengan DB integration, sampai UI yang user-facing. Setiap prompt menambah satu lapis ke fitur yang sama, tanpa file eksperimen terpisah. Teori `top_p`, `top_k`, `stop_sequences` sudah dibahas di `materi.md`; di sini kita fokus implementasi.
>
> **Estimasi**: 60–75 menit.

## Prasyarat Section 2

- [ ] Section 1 selesai. AI Advisor pakai parameter `system`.
- [ ] Tabel `transactions` di Supabase sudah ada (dari Module 01).
- [ ] Server action `createTransaction` (atau equivalent) dari Module 02 berfungsi.
- [ ] Anda sudah membaca bagian Section 2 di `materi.md` (`temperature`, `top_p`, `top_k`, `stop_sequences`).

---

## 📚 Referensi Dokumentasi

Sebelum mulai, akan sangat membantu kalau Anda buka tab dokumentasi resmi untuk referensi cepat:

- **[Messages API parameters](https://docs.claude.com/en/api/messages)** — `temperature`, `top_p`, `top_k`, `stop_sequences`, dan kapan satu lebih cocok dari yang lain.
- **[Structured outputs](https://docs.claude.com/en/docs/build-with-claude/structured-outputs)** — JSON mode, schema enforcement, pola prompting agar Claude return JSON murni.
- **[Stop sequences guide](https://docs.claude.com/en/api/messages)** — cara pakai `stop_sequences` untuk batasi output di marker tertentu.
- **[Zod docs](https://zod.dev/)** — schema validation TypeScript yang akan dipakai untuk verifikasi output Claude.
- **[Server Actions Next.js](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations)** — pola `"use server"`, memanggil server action dari client component.

---

## Prompt 1 — Buat Parser Transaksi (`src/lib/parsers/transaction-parser.ts`)

### Walkthrough Manual (sebelum pakai prompt)

Sebelum copy-paste prompt ke Claude, pahami dulu struktur parser stand-alone yang akan dibuat. Tujuan: function `parseTransactionFromText(text)` yang minta Claude convert natural language ke struktur transaksi, lalu validate dengan Zod.

📂 **File baru**: `src/lib/parsers/transaction-parser.ts` (parser utility, dipanggil dari server action di Prompt 3)

**1. Directive `"use server"` di baris pertama**

📍 Lokasi: **baris 1 file**. Wajib karena parser ini panggil Anthropic SDK yang butuh `ANTHROPIC_API_KEY` (server-only).

```ts
// src/lib/parsers/transaction-parser.ts — baris pertama
"use server";
```

**2. Import Anthropic SDK + Zod + setup client**

📍 Lokasi: **bagian import** setelah directive.

```ts
// src/lib/parsers/transaction-parser.ts — bagian import
import Anthropic from "@anthropic-ai/sdk";
import { z } from "zod";

const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
```

**3. Zod schema sebagai kontrak antara Claude dan app**

📍 Lokasi: **module level**, sebelum function. Schema ini = source of truth untuk struktur transaksi.

```ts
// src/lib/parsers/transaction-parser.ts — module level
export const TransactionSchema = z.object({
  type: z.enum(["income", "expense"]),
  amount: z.number().positive(),
  category: z.string().min(1),
  description: z.string().min(1),
});

export type ParsedTransaction = z.infer<typeof TransactionSchema>;
```

**4. System prompt yang menekankan "JSON murni, tidak ada teks lain"**

📍 Lokasi: **module level**, const string.

```ts
// src/lib/parsers/transaction-parser.ts — module level
const PARSER_SYSTEM = `Anda parser transaksi keuangan. Ekstrak data dari teks user dan return JSON dengan struktur EKSPLISIT:
{ "type": "income" | "expense", "amount": number, "category": string, "description": string }

Aturan:
- Output WAJIB JSON valid murni — TANPA markdown fence, TANPA penjelasan, TANPA prose extra.
- amount selalu dalam Rupiah penuh (mis. "35rb" → 35000, "1.5jt" → 1500000).
- type = "expense" untuk pengeluaran, "income" untuk pemasukan.
- category: tebak kategori singkat (Food, Transport, Shopping, Salary, dll.).
- description: ringkas, 3-8 kata.`;
```

**5. Function `parseTransactionFromText(text)`**

📍 Lokasi: **module level**, exported async function. Alur:

- Call `client.messages.create()` dengan `model: "claude-haiku-4-5"`, `temperature: 0`, `system: PARSER_SYSTEM`.
- Parse `response.content[0].text` → `JSON.parse` → `TransactionSchema.safeParse`.
- Kalau gagal Zod, throw error dengan pesan jelas.

```ts
// src/lib/parsers/transaction-parser.ts — module level
export async function parseTransactionFromText(text: string): Promise<ParsedTransaction> {
  const response = await client.messages.create({
    model: "claude-haiku-4-5",
    max_tokens: 300,
    temperature: 0,
    system: PARSER_SYSTEM,
    messages: [{ role: "user", content: text }],
  });

  const block = response.content[0];
  if (block.type !== "text") throw new Error("Response bukan text block");

  let raw: unknown;
  try {
    raw = JSON.parse(block.text);
  } catch {
    throw new Error(`Output Claude bukan JSON valid: ${block.text.slice(0, 120)}`);
  }

  const parsed = TransactionSchema.safeParse(raw);
  if (!parsed.success) {
    throw new Error(`Validasi Zod gagal: ${parsed.error.message}`);
  }
  return parsed.data;
}
```

### Yang TIDAK perlu

- ❌ File `experiments/` sebagai output utama — semua kode produksi di `src/`.
- ❌ UI rendering — itu di Prompt 4.
- ❌ Tools / function calling — kita pakai instruksi eksplisit + parse JSON sederhana (tool use dibahas di Section 4).
- ❌ Streaming — parser ini blocking; response pendek, lebih cepat tanpa stream.
- ❌ Retry otomatis — biarkan caller (server action) yang putuskan retry/fallback.

### Verifikasi setelah file dibuat

1. File `src/lib/parsers/transaction-parser.ts` ada dengan `"use server"` di baris 1.
2. Export `parseTransactionFromText` dan `TransactionSchema` tersedia.
3. `npx tsc --noEmit` tidak ada error.
4. (Opsional) test cepat via `experiments/test-parser.ts`:
   ```ts
   import { parseTransactionFromText } from "../src/lib/parsers/transaction-parser";
   async function main() {
     console.log(await parseTransactionFromText("Tadi siang ngopi 35rb di Starbucks"));
   }
   main().catch(console.error);
   ```
   Jalankan: `npx tsx --env-file=.env.local experiments/test-parser.ts`. Expected: `{ type: 'expense', amount: 35000, category: 'Food', description: '...' }`.

---

**Salin prompt berikut:**

```
Saya ingin parser stand-alone yang convert natural language
ke struktur transaksi via Claude.

GOAL:
- Buat file src/lib/parsers/transaction-parser.ts.
- Baris 1: "use server".
- Ekspor TransactionSchema (Zod):
    type: enum("income", "expense"),
    amount: number positif,
    category: string non-empty,
    description: string non-empty.
- Ekspor type ParsedTransaction = z.infer<typeof TransactionSchema>.
- Ekspor async function parseTransactionFromText(text: string):
  Promise<ParsedTransaction>.
- Definisikan const PARSER_SYSTEM yang menekankan:
  - Output WAJIB JSON murni (tanpa markdown, tanpa prose).
  - amount selalu dalam Rupiah penuh (35rb -> 35000).
  - Tebak category singkat (Food, Transport, dll.).

CONTEXT:
- Model: claude-haiku-4-5.
- temperature: 0 (deterministik).
- max_tokens: 300.
- Pakai Anthropic SDK langsung, NOT tool use.

GUARDRAIL:
- Apabila JSON.parse gagal, throw error dengan potongan
  output Claude untuk debugging.
- Apabila Zod safeParse gagal, throw error berisi pesan Zod.
- File ini "use server" — JANGAN di-import dari client tanpa
  perantara server action.
- JANGAN tambah retry atau caching — biarkan caller yang
  putuskan.
```

**Verifikasi:**

1. File terbentuk dengan struktur sesuai walkthrough.
2. Test dengan "Tadi siang ngopi 35rb di Starbucks" → return `{ type: 'expense', amount: 35000, category: 'Food', description: ... }`.

---

## Prompt 2 — Tambah `stop_sequences` sebagai Guardrail

### Walkthrough Manual (sebelum pakai prompt)

Sebelum copy-paste prompt, pahami kenapa `stop_sequences` membantu di sini. Kadang Claude (walau sudah di-instruksi "JSON murni") masih nambah prose seperti `"Penjelasan: ..."` setelah closing brace. `stop_sequences` adalah safety net — Claude **berhenti generate** segera setelah marker tertentu muncul.

📂 **File yang diubah**: `src/lib/parsers/transaction-parser.ts` (modifikasi, BUKAN file baru)

**1. Tambah `stop_sequences` ke `client.messages.create()`**

📍 Lokasi: **di dalam `parseTransactionFromText`**, di parameter pemanggilan API — tepat setelah `messages`.

```ts
// src/lib/parsers/transaction-parser.ts — di dalam parseTransactionFromText
const response = await client.messages.create({
  model: "claude-haiku-4-5",
  max_tokens: 300,
  temperature: 0,
  system: PARSER_SYSTEM,
  messages: [{ role: "user", content: text }],
  stop_sequences: ["\n\n", "\nPenjelasan", "\nNote:", "\nCatatan"],   /* ← BARU */
});
```

> 💡 Marker `\n\n` ampuh karena JSON satu-baris Claude akan diikuti dua newline kalau ia mau mulai prose. Sebelum prose mulai, Claude sudah berhenti.

**2. (Opsional) Logging `stop_reason` untuk debugging awal**

📍 Lokasi: **tepat setelah API call**, sebelum parse JSON. Boleh dihapus di production.

```ts
// src/lib/parsers/transaction-parser.ts — di dalam parseTransactionFromText
if (process.env.NODE_ENV !== "production") {
  console.log("[parser] stop_reason:", response.stop_reason);
}
```

> ⚠️ `stop_reason === "stop_sequence"` di sini **bukan masalah** — JSON-nya sudah lengkap sebelum stop. Yang harus diwaspadai justru kalau JSON belum tertutup saat stop terjadi.

### Yang TIDAK perlu

- ❌ Mengubah `PARSER_SYSTEM` — sudah eksplisit di Prompt 1.
- ❌ Validasi tambahan — Zod sudah cukup tangkap output rusak.
- ❌ Logging detail `stop_reason` di production — cukup untuk debugging awal.
- ❌ Menambah retry loop kalau stop terlalu cepat — kalau itu sering kejadian, justru tanda kita perlu pindah ke tool use (Section 4).

### Verifikasi setelah file diubah

1. `npx tsc --noEmit` tidak ada error.
2. Paste teks yang biasanya bikin Claude nambah penjelasan (mis. "Bayar listrik 250rb, kemungkinan ini PLN ya?") via test script:
   ```bash
   npx tsx --env-file=.env.local experiments/test-parser.ts
   ```
3. Output sekarang **hanya JSON** — Zod `safeParse` lolos, tidak ada error parse karena prose ikutan.
4. Cek log development: `stop_reason` biasanya `"end_turn"` (Claude selesai sendiri) atau `"stop_sequence"` (stop ketrigger). Keduanya OK selama JSON valid.

---

**Salin prompt berikut:**

```
Tambahkan stop_sequences sebagai guardrail kedua di
parseTransactionFromText supaya Claude tidak nambah prose
setelah JSON.

GOAL:
- Modifikasi src/lib/parsers/transaction-parser.ts.
- Tambah parameter stop_sequences di client.messages.create():
    ["\n\n", "\nPenjelasan", "\nNote:", "\nCatatan"]
- (Opsional, dev only) console.log response.stop_reason
  untuk debugging.

CONTEXT:
- Walau system prompt sudah tegas "JSON murni", Claude
  occasionally masih nambah prose. stop_sequences = safety
  net.
- JSON Claude biasanya satu baris; \n\n hampir pasti
  menandai mulai prose ekstra.

GUARDRAIL:
- JANGAN ubah PARSER_SYSTEM — sudah cukup di Prompt 1.
- JANGAN tambah retry — kalau stop terlalu cepat berulang,
  catat sebagai bahan diskusi untuk migrasi ke tool use.
- Logging stop_reason HANYA di development (cek NODE_ENV).
```

**Verifikasi:**

1. Test dengan teks yang biasanya trigger prose, output sekarang murni JSON.
2. Zod safeParse lolos, tidak ada error "bukan JSON valid".

---

## Prompt 3 — Server Action `parseAndCreateTransaction`

### Walkthrough Manual (sebelum pakai prompt)

Sebelum copy-paste prompt, pahami pembagian tanggung jawab. `parseTransactionFromText` (Prompt 1+2) **hanya** parse teks → struktur. Sekarang kita bikin entry point user-facing yang gabungkan parse + insert ke Supabase.

📂 **File baru**: `src/features/transaction-from-text.ts` (server action, dipanggil langsung dari client component di Prompt 4)

**1. Directive `"use server"` di baris pertama**

📍 Lokasi: **baris 1 file**.

```ts
// src/features/transaction-from-text.ts — baris pertama
"use server";
```

**2. Import parser + Supabase server client**

📍 Lokasi: **bagian import**. Pola Supabase client sesuaikan dengan yang sudah ada di project (mis. `src/features/action.ts` dari Module 02).

```ts
// src/features/transaction-from-text.ts — bagian import
import { parseTransactionFromText, type ParsedTransaction } from "@/lib/parsers/transaction-parser";
import { createClient } from "@/lib/supabase/server"; // sesuaikan dengan helper project
```

**3. Tipe return discriminated union**

📍 Lokasi: **module level**, sebelum function. Pattern `{ ok: true, ... } | { ok: false, error }` memudahkan UI handle hasil.

```ts
// src/features/transaction-from-text.ts — module level
type Result =
  | { ok: true; transaction: ParsedTransaction & { id: string } }
  | { ok: false; error: string };
```

**4. Function `parseAndCreateTransaction(text)`**

📍 Lokasi: **module level**, exported async function. Alur:

- Validasi `text.trim()` non-empty → return `{ ok: false, error }` kalau kosong.
- Try-catch `parseTransactionFromText(text)` → kalau throw, tangkap dan return `{ ok: false, error: err.message }`.
- Ambil user_id via Supabase auth helper (pola yang sama dengan Module 02).
- Insert ke tabel `transactions` dengan `parsed` + `user_id`.
- Return `{ ok: true, transaction: insertedRow }`.

```ts
// src/features/transaction-from-text.ts — module level
export async function parseAndCreateTransaction(text: string): Promise<Result> {
  if (!text.trim()) {
    return { ok: false, error: "Teks transaksi tidak boleh kosong" };
  }

  let parsed: ParsedTransaction;
  try {
    parsed = await parseTransactionFromText(text);
  } catch (err) {
    return { ok: false, error: err instanceof Error ? err.message : "Parse gagal" };
  }

  const supabase = await createClient();
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) return { ok: false, error: "User tidak terautentikasi" };

  const { data, error } = await supabase
    .from("transactions")
    .insert({ ...parsed, user_id: user.id })
    .select()
    .single();

  if (error) return { ok: false, error: error.message };
  return { ok: true, transaction: data };
}
```

### Yang TIDAK perlu

- ❌ Optimistic update — itu tanggung jawab UI (Prompt 4) kalau diperlukan.
- ❌ Rate limiting — di Module 09+ saat kita bahas production hardening.
- ❌ Membuat tabel baru — pakai `transactions` yang sudah ada dari Module 01.
- ❌ Branching ke advisor — fitur ini berdiri sendiri, terpisah dari chatbot.
- ❌ Re-export `parseTransactionFromText` — UI tidak boleh panggil parser langsung; selalu lewat server action ini.

### Verifikasi setelah file dibuat

1. File `src/features/transaction-from-text.ts` ada dengan `"use server"` di baris 1.
2. `npx tsc --noEmit` tidak ada error.
3. (Opsional) test via `experiments/test-create-from-text.ts`:
   ```ts
   import { parseAndCreateTransaction } from "../src/features/transaction-from-text";
   async function main() {
     console.log(await parseAndCreateTransaction("Tadi pagi sarapan nasi uduk 15rb"));
   }
   main().catch(console.error);
   ```
4. Cek Supabase Table Editor → tabel `transactions` punya row baru: `type: expense, amount: 15000, category: Food, description: "sarapan nasi uduk"`.
5. Test error path: kirim string kosong → return `{ ok: false, error: "Teks transaksi tidak boleh kosong" }`.

---

**Salin prompt berikut:**

```
Bungkus parser ke server action yang juga insert ke
Supabase. Ini entry point user-facing.

GOAL:
- Buat file src/features/transaction-from-text.ts.
- Baris 1: "use server".
- Ekspor async function parseAndCreateTransaction(text: string):
    Promise<{ ok: true, transaction: T } | { ok: false, error: string }>
- Alur:
    1. Validasi text.trim() non-empty.
    2. Call parseTransactionFromText (try/catch).
    3. Ambil user_id via Supabase auth (pola sama dgn
       src/features/action.ts dari Module 02).
    4. Insert ke tabel transactions dengan parsed + user_id.
    5. Return discriminated union.

CONTEXT:
- parseTransactionFromText ada di
  src/lib/parsers/transaction-parser.ts.
- Supabase server client helper sudah ada di
  src/lib/supabase/server (sesuaikan kalau path beda).
- Tabel transactions sudah ada dari Module 01 dengan kolom
  type, amount, category, description, user_id.

GUARDRAIL:
- JANGAN throw — selalu return discriminated union supaya
  UI mudah handle.
- JANGAN buat tabel baru.
- JANGAN re-export parseTransactionFromText — UI harus
  selalu lewat server action ini.
- Apabila tidak ada user (unauth), return ok: false.
```

**Verifikasi:**

1. Call dari test script: `parseAndCreateTransaction("Tadi pagi sarapan nasi uduk 15rb")` → return `{ ok: true, transaction: {...} }`.
2. Cek Supabase Table Editor → row baru muncul dengan field sesuai.
3. Test string kosong → return `{ ok: false, error: "..." }`.

---

## Prompt 4 — Integrasi ke UI (Halaman Transactions)

### Walkthrough Manual (sebelum pakai prompt)

Sebelum copy-paste prompt, pahami pola **preview before commit**. UI baru: tombol "Quick Add via AI" → textarea + button "Parse via AI" → preview struktur → Confirm/Cancel. User tetap punya kendali terakhir sebelum data masuk.

📂 **File baru**: `src/components/transactions/quick-add-ai.tsx` (client component).
📂 **File yang diubah**: `src/app/transactions/page.tsx` (atau path halaman Transactions sesuai struktur project).

**1. Buat client component `QuickAddAi`**

📍 Lokasi: **file baru** `src/components/transactions/quick-add-ai.tsx`. Wajib `"use client"` di baris 1 karena pakai `useState` + handler interaktif.

```tsx
// src/components/transactions/quick-add-ai.tsx — baris pertama
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Loader2 } from "lucide-react";
import { parseAndCreateTransaction } from "@/features/transaction-from-text";
```

**2. State component**

📍 Lokasi: **di dalam fungsi `QuickAddAi`**.

```tsx
// src/components/transactions/quick-add-ai.tsx — dalam komponen
const router = useRouter();
const [text, setText] = useState("");
const [isProcessing, setIsProcessing] = useState(false);
const [result, setResult] = useState<
  | { ok: true; transaction: { type: string; amount: number; category: string; description: string } }
  | { ok: false; error: string }
  | null
>(null);
```

**3. Handler `handleSubmit`**

📍 Lokasi: **function di dalam komponen**. Panggil server action langsung — Next.js handle networking.

```tsx
// src/components/transactions/quick-add-ai.tsx — dalam komponen
async function handleSubmit() {
  setIsProcessing(true);
  setResult(null);
  const res = await parseAndCreateTransaction(text);
  setResult(res);
  setIsProcessing(false);
  if (res.ok) {
    setText("");
    router.refresh(); // refetch list transaksi
  }
}
```

**4. JSX dengan textarea + tombol + preview/error**

📍 Lokasi: **return** komponen.

```tsx
// src/components/transactions/quick-add-ai.tsx — return
return (
  <div className="space-y-3 rounded-lg border p-4">
    <h3 className="font-semibold">Quick Add via AI</h3>
    <textarea
      className="w-full rounded border p-2 text-sm"
      rows={3}
      value={text}
      onChange={(e) => setText(e.target.value)}
      placeholder="Contoh: Tadi siang ngopi 35rb di Starbucks"
      disabled={isProcessing}
    />
    <button
      onClick={handleSubmit}
      disabled={isProcessing || !text.trim()}
      className="inline-flex items-center gap-2 rounded bg-blue-600 px-3 py-2 text-sm text-white disabled:opacity-50"
    >
      {isProcessing && <Loader2 className="h-4 w-4 animate-spin" />}
      Parse via AI
    </button>

    {result?.ok === true && (
      <div className="rounded border border-green-200 bg-green-50 p-3 text-sm">
        <p className="font-medium text-green-800">Berhasil ditambahkan</p>
        <p>Type: {result.transaction.type}</p>
        <p>Amount: Rp {result.transaction.amount.toLocaleString("id-ID")}</p>
        <p>Category: {result.transaction.category}</p>
        <p>Description: {result.transaction.description}</p>
      </div>
    )}

    {result?.ok === false && (
      <p className="rounded border border-rose-200 bg-rose-50 p-3 text-sm text-rose-700">
        {result.error}
      </p>
    )}
  </div>
);
```

**5. Pasang ke halaman Transactions**

📍 Lokasi: **`src/app/transactions/page.tsx`** (atau path yang sesuai). Mount `<QuickAddAi />` di atas tabel transaksi.

```tsx
// src/app/transactions/page.tsx — di dalam JSX
import { QuickAddAi } from "@/components/transactions/quick-add-ai";

// ... di dalam return:
<QuickAddAi />
{/* lalu list transaksi yang sudah ada */}
```

### Yang TIDAK perlu

- ❌ Voice input / OCR — di luar scope module.
- ❌ Multi-language detection — Claude handle Indonesian + English secara natural via prompt.
- ❌ Edit hasil parse sebelum confirm — iterasi berikutnya; untuk sekarang server action langsung insert (user lihat hasil setelah berhasil).
- ❌ Animasi loading fancy — `Loader2` spinner sederhana cukup.
- ❌ Optimistic update — `router.refresh()` cukup responsif untuk fitur ini.

### Verifikasi setelah file diubah

1. Reload halaman `/transactions`. Komponen "Quick Add via AI" muncul di atas list.
2. Ketik "Beli kopi 25rb" → klik **Parse via AI** → spinner muncul.
3. ~2 detik kemudian, kartu hijau muncul: type=expense, amount=25000, category=Food, description=...
4. List transaksi di bawah otomatis ter-refresh, row baru terlihat.
5. Test error: ketik teks aneh "asdf asdf 123" → kartu merah muncul dengan pesan error Zod/parse.
6. Build production: `npm run build` sukses tanpa error TypeScript.

---

**Salin prompt berikut:**

```
Buat UI untuk fitur Quick Add via AI di halaman
Transactions. Pakai server action yang sudah ada.

GOAL:
- Buat client component
  src/components/transactions/quick-add-ai.tsx ("use client").
  State:
    text: string
    isProcessing: boolean
    result: { ok: true, transaction } | { ok: false, error } | null
- Textarea + button "Parse via AI" + Loader2 saat processing.
- Saat sukses (ok=true): tampilkan preview hijau berisi
  type/amount/category/description, reset textarea, call
  router.refresh().
- Saat error (ok=false): tampilkan box merah inline (BUKAN
  toast).
- Pasang <QuickAddAi /> di src/app/transactions/page.tsx
  (atau file halaman Transactions yang sesuai) di atas list.

CONTEXT:
- Server action: parseAndCreateTransaction dari
  @/features/transaction-from-text.
- Pakai useRouter dari next/navigation untuk refetch.
- Lucide-react sudah ter-install (Loader2).
- Tailwind sudah ter-setup.

GUARDRAIL:
- JANGAN panggil parseTransactionFromText langsung dari
  client — selalu lewat parseAndCreateTransaction.
- JANGAN tambah voice input / OCR / multi-language switch.
- JANGAN auto-submit — user harus klik tombol.
- Error harus inline, BUKAN toast.
- Disable button saat isProcessing atau text.trim() kosong.
```

**Verifikasi:**

1. Halaman Transactions tampil komponen Quick Add via AI.
2. "Beli kopi 25rb" → preview hijau + row baru di list.
3. Teks aneh → box merah inline dengan pesan error.
4. `npm run build` sukses.

---

## Validasi Akhir Section 2

- [ ] `src/lib/parsers/transaction-parser.ts` ada dengan `parseTransactionFromText` dan `TransactionSchema`.
- [ ] `stop_sequences` aktif di API call parser.
- [ ] Zod validation tangkap halusinasi (test dengan teks aneh).
- [ ] Server action `parseAndCreateTransaction` di `src/features/transaction-from-text.ts` berhasil insert ke Supabase.
- [ ] UI "Quick Add via AI" di halaman Transactions berfungsi end-to-end (parse → insert → list ter-refresh).
- [ ] Build production sukses (`npm run build`).
- [ ] Tidak ada regresi dari Section 1 (AI Advisor tetap jalan).

## Refleksi Section 2

1. Apa risiko terbesar dari fitur "parse via AI" ini di production? (mis. user input typo, halusinasi kategori, amount salah konversi, dll.)
2. Bagaimana Anda akan handle case Claude return `category` yang tidak ada di enum Supabase Anda? (saat ini Zod tidak constrain category ke enum spesifik — sengaja, supaya fleksibel.)
3. `stop_sequences` bekerja baik tapi cukup brittle (bergantung pada Claude mengeluarkan marker tertentu). Kapan Anda akan migrasi ke **tool use** untuk task ini (Section 4)? Sinyal apa yang akan trigger keputusan itu?
4. Bagaimana cara Anda monitor akurasi parser di production? (logging input/output sample, eval set bulanan, user feedback button, dll.)
5. `temperature: 0` di parser vs `temperature` default di Advisor — kenapa beda? Kalau Advisor diset `temperature: 0`, apa yang akan berubah?

---

⬅️ Kembali: **[Section 1](./latihan-1-system-instruction.md)** · ➡️ Lanjut: **[Section 3 — Role, Context, Instruction](./latihan-3-rci.md)**
