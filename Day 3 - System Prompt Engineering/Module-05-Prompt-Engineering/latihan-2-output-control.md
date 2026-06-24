# Section 2 — Output Control

> Bagian dari **[Module 05 — Latihan](./latihan.md)**. Lanjutan dari **[Section 1 — System Instruction](./latihan-1-system-instruction.md)**.

> Latihan ini membangun fitur **Catat Transaksi via Chatbot** — user mengetik di chatbot AI Financial Advisor _"ngopi 25rb tadi siang"_, parser AI ekstrak struktur transaksinya, lalu otomatis tersimpan di Supabase + chatbot konfirmasi di bubble. Tidak ada halaman/UI baru — semua terintegrasi ke `AIChatPanel` yang sudah Anda bangun. Teori `structured output`, `stop_sequences`, dan validasi Zod sudah dibahas di `materi.md`; di sini fokus implementasi.
>
> **Estimasi**: 60–75 menit.

## Prasyarat Section 2

- [ ] Section 1 selesai. AI Advisor pakai parameter `system`.
- [ ] Tabel `transactions` di Supabase sudah ada (dari Module 01).
- [ ] Server action `createTransaction` (atau equivalent) dari Module 02 berfungsi.
- [ ] Anda sudah membaca bagian Section 2 di `materi.md` (structured output, `stop_sequences`, validasi Zod).

---

## 📚 Referensi Dokumentasi

Sebelum mulai, akan sangat membantu kalau Anda buka tab dokumentasi resmi untuk referensi cepat:

- **[Messages API parameters](https://docs.claude.com/en/api/messages)** — `temperature`, `stop_sequences`, dan parameter terkait output control.
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

## Prompt 4 — Integrasi ke Chatbot AI Financial Advisor

### Walkthrough Manual (sebelum pakai prompt)

Fitur ini **tidak butuh halaman baru** — kita pasang langsung di `AIChatPanel` yang sudah Anda bangun. Idenya: di samping tombol **Send** (untuk ngobrol ke advisor), tambah tombol **📝 Catat Transaksi**. Saat user klik tombol Catat, input teks-nya **bukan dikirim ke advisor**, tapi ke server action `parseAndCreateTransaction`. Hasil berhasil/gagal ditampilkan sebagai bubble chat baru — UX-nya seamless seperti ngobrol normal.

📂 **File yang diubah**: `src/components/chat/ai-chat-panel.tsx` (modifikasi)

**1. Import server action + ikon tambahan**

📍 Lokasi: **bagian import** di atas.

```tsx
// src/components/chat/ai-chat-panel.tsx — bagian import
import { Receipt } from "lucide-react"; // ikon untuk tombol Catat
import { parseAndCreateTransaction } from "@/features/transaction-from-text";
```

**2. Handler baru `handleCatatTransaksi`**

📍 Lokasi: **di dalam function `AIChatPanel`**, sejajar dengan `handleSend` yang sudah ada.

```tsx
// src/components/chat/ai-chat-panel.tsx — di dalam function AIChatPanel()
async function handleCatatTransaksi() {
  const text = input.trim();
  if (!text || isWaiting) return;

  // 1. Push user message ke chat (biar user lihat apa yang dia kirim)
  setMessages((prev) => [
    ...prev,
    { id: crypto.randomUUID(), role: "user", content: text },
  ]);
  setInput("");
  setIsWaiting(true);

  try {
    // 2. Call server action — BUKAN advisor
    const res = await parseAndCreateTransaction(text);

    // 3. Tampilkan hasil sebagai bubble assistant
    const reply = res.ok
      ? `✅ **Transaksi tercatat:**\n\n- Tipe: ${res.transaction.type}\n- Nominal: Rp ${res.transaction.amount.toLocaleString("id-ID")}\n- Kategori: ${res.transaction.category}\n- Deskripsi: ${res.transaction.description}`
      : `❌ Gagal mencatat: ${res.error}\n\nCoba ketik ulang dengan format yang lebih jelas, contoh: _"Kopi Starbucks 25rb tadi siang"_.`;

    setMessages((prev) => [
      ...prev,
      { id: crypto.randomUUID(), role: "assistant", content: reply },
    ]);
    setLastError(null);
  } catch (err) {
    const message = err instanceof Error ? err.message : "Unknown error";
    setLastError({ message, userQuestion: text });
  } finally {
    setIsWaiting(false);
  }
}
```

**3. Tombol baru di footer panel — sebelah tombol Send**

📍 Lokasi: **di JSX return**, **footer area**, di sebelah `<Button>` Send yang sudah ada.

```tsx
// src/components/chat/ai-chat-panel.tsx — di JSX return, area footer
<div className="flex items-end gap-2">
  <Textarea
    value={input}
    onChange={(e) => setInput(e.target.value)}
    onKeyDown={handleKeyDown}
    disabled={isWaiting}
    placeholder="Ask AI Advisor here"
    /* ...props lain... */
  />

  <Button
    type="button"
    size="icon"
    variant="outline"
    onClick={handleCatatTransaksi}
    disabled={isWaiting || !input.trim()}
    aria-label="Catat sebagai transaksi"
    title="Catat sebagai transaksi (bukan tanya advisor)"
  >
    <Receipt className="size-4" />
  </Button>

  <Button
    type="button"
    size="icon"
    onClick={handleSend}
    disabled={!canSend}
    aria-label="Send message"
    /* ...class emerald yang sudah ada... */
  >
    <Send className="size-4" />
  </Button>
</div>
```

**4. (Opsional) Update welcome message agar mention fitur baru**

📍 Lokasi: **`INITIAL_MESSAGES`** di atas component. Tambah satu bullet point.

```tsx
// src/components/chat/ai-chat-panel.tsx — INITIAL_MESSAGES
content: `Halo! Saya **AI Financial Advisor** Anda. Saya dapat membantu Anda dengan:

- Analisis pola pengeluaran
- Tips menghemat dan menabung
- Pertanyaan umum tentang keuangan personal
- **Mencatat transaksi otomatis** — ketik "kopi 25rb tadi siang" lalu tekan tombol 🧾 di sebelah Send.

Apa yang ingin Anda tanyakan?`,
```

### Yang TIDAK perlu

- ❌ **Halaman/route baru** — semua di `AIChatPanel`. Tidak modifikasi `src/app/transactions/page.tsx`.
- ❌ **Auto-detect intent** ("ini transaksi apa pertanyaan?") — terlalu rumit untuk Section 2; user memilih eksplisit via tombol. Auto-detect bisa di Section 4 dengan **tool use**.
- ❌ **Streaming respons konfirmasi** — hasil parse sangat singkat (~50 token), streaming malah overkill. Push sekaligus.
- ❌ **Optimistic UI** (langsung tampil sebelum DB confirm) — buat bingung kalau parse gagal di tengah jalan.
- ❌ **Preview-sebelum-confirm** — bisa di iterasi berikutnya. Untuk sekarang flow: kirim → langsung insert → konfirmasi bubble.

### Verifikasi setelah file diubah

1. Reload browser. Chatbot panel muncul dengan **2 tombol** di footer: ikon 🧾 (Catat) + ✈️ (Send) di sebelah Textarea.
2. Ketik `"Beli kopi 25rb tadi siang di Starbucks"` → klik tombol 🧾 (BUKAN Send).
3. ~2 detik kemudian, bubble assistant muncul: ✅ Transaksi tercatat dengan detail type/nominal/kategori/deskripsi.
4. Buka tab Transactions → row baru muncul di list (kalau halaman pakai server component, perlu reload manual atau Anda tambahkan `router.refresh()` di handler).
5. Test error: ketik `"asdf asdf 123"` → klik 🧾 → bubble assistant muncul dengan ❌ pesan gagal yang ramah.
6. Test alur normal: ketik pertanyaan `"Tips hemat bulanan?"` → klik **Send** (✈️) → masuk ke advisor flow biasa (tidak diparse sebagai transaksi).
7. Build production sukses: `npm run build`.

> 💡 **Catatan UX**: tombol 🧾 sengaja **outline variant** (tidak emerald-filled seperti Send) supaya secara visual user tahu ini "action sekunder" — alurnya jelas: default = ngobrol, opsi = catat.

---

**Salin prompt berikut:**

```
Tambahkan fitur "Catat Transaksi" ke chatbot AI Financial
Advisor. Pasang langsung di AIChatPanel, BUKAN buat
halaman/komponen terpisah.

GOAL:
- Modifikasi src/components/chat/ai-chat-panel.tsx.
- Tambah handler baru handleCatatTransaksi():
  1. Ambil input.trim(), validasi non-empty + tidak isWaiting.
  2. Push user message ke state messages.
  3. setIsWaiting(true).
  4. Call parseAndCreateTransaction(text) dari
     @/features/transaction-from-text.
  5. Push bubble assistant berisi:
     - Saat ok=true: "✅ Transaksi tercatat" + detail
       type/amount/category/description (markdown list).
     - Saat ok=false: "❌ Gagal mencatat: <error>"
       + saran format yang lebih jelas.
  6. setIsWaiting(false).
- Tambah satu tombol icon baru di footer (sebelah Send):
  ikon Receipt dari lucide-react, variant="outline",
  size="icon".
  - Click → panggil handleCatatTransaksi.
  - disabled saat isWaiting || !input.trim().
  - aria-label + title yang menjelaskan ("Catat sebagai
    transaksi").
- Update INITIAL_MESSAGES welcome (assistant) untuk menambah
  satu bullet point yang menjelaskan cara catat transaksi
  via tombol 🧾.

CONTEXT:
- parseAndCreateTransaction sudah ada di
  src/features/transaction-from-text.ts (Prompt 3).
- Tombol Send (Send icon, emerald) sudah ada — JANGAN diganti
  fungsi-nya. Tombol Catat adalah TAMBAHAN, bukan
  pengganti.
- isWaiting + lastError + state messages sudah ada di
  component.

GUARDRAIL:
- JANGAN buat halaman/route baru.
- JANGAN auto-detect intent (user memilih lewat tombol —
  Send vs Receipt).
- JANGAN streaming bubble konfirmasi — push sekaligus.
- JANGAN ubah handler handleSend yang sudah ada.
- Tombol Receipt HARUS variant="outline" supaya secara visual
  beda dari Send (action sekunder).
- Push user message sebelum call server action (UX: user
  lihat apa yang dia kirim).
```

**Verifikasi:**

1. Chatbot panel sekarang punya 2 tombol di footer: 🧾 Catat (outline) + ✈️ Send (emerald).
2. Ketik transaksi → 🧾 → bubble assistant konfirmasi.
3. Ketik pertanyaan → ✈️ → masuk advisor flow normal.
4. Test gagal: teks aneh → bubble error ramah.
5. Welcome message di awal chat sudah mention fitur catat transaksi.
6. `npm run build` sukses.

---

## Validasi Akhir Section 2

- [ ] `src/lib/parsers/transaction-parser.ts` ada dengan `parseTransactionFromText` dan `TransactionSchema`.
- [ ] `stop_sequences` aktif di API call parser.
- [ ] Zod validation tangkap halusinasi (test dengan teks aneh).
- [ ] Server action `parseAndCreateTransaction` di `src/features/transaction-from-text.ts` berhasil insert ke Supabase.
- [ ] Tombol 🧾 Catat Transaksi muncul di footer `AIChatPanel` (sebelah Send).
- [ ] Ketik transaksi + klik 🧾 → bubble konfirmasi ✅ muncul + row baru di Supabase.
- [ ] Ketik pertanyaan + klik Send → masih masuk advisor flow (tidak diparse sebagai transaksi).
- [ ] Test gagal: teks aneh → bubble error ramah dengan saran format.
- [ ] Welcome message awal sudah mention fitur catat transaksi via tombol.
- [ ] Build production sukses (`npm run build`).
- [ ] Tidak ada regresi dari Section 1 (AI Advisor tetap jalan normal lewat Send).

## Refleksi Section 2

1. Apa risiko terbesar dari fitur "parse via AI" ini di production? (mis. user input typo, halusinasi kategori, amount salah konversi, dll.)
2. **Dua tombol di chatbot footer** (Send + Catat) — apakah UX-nya intuitif buat user awam? Bagaimana Anda akan menjelaskan bedanya tanpa user manual? (mis. tooltip, onboarding, atau langsung **auto-detect intent**?)
3. Auto-detect intent ("ini transaksi atau pertanyaan?") sengaja tidak diimplementasi di section ini — kenapa menurut Anda itu **pilihan yang masuk akal**? Kapan Anda akan beralih ke auto-detect (Section 4 dengan tool use)?
4. Bagaimana Anda akan handle case Claude return `category` yang tidak ada di enum Supabase Anda? (saat ini Zod tidak constrain category ke enum spesifik — sengaja, supaya fleksibel.)
5. `stop_sequences` bekerja baik tapi cukup brittle (bergantung pada Claude mengeluarkan marker tertentu). Kapan Anda akan migrasi ke **tool use** untuk task ini (Section 4)? Sinyal apa yang akan trigger keputusan itu?
6. `temperature: 0` di parser vs `temperature` default di Advisor — kenapa beda? Kalau Advisor diset `temperature: 0`, apa yang akan berubah?

---

⬅️ Kembali: **[Section 1](./latihan-1-system-instruction.md)** · ➡️ Lanjut: **[Section 3 — Role, Context, Instruction](./latihan-3-rci.md)**
