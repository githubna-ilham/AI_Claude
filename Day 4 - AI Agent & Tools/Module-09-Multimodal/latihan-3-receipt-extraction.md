# Section 3 — Receipt Extraction + Auto-Insert ke `transactions`

> Bagian dari **[Module 09 — Latihan](./latihan.md)**. Lanjutan dari **[Section 2 — Upload UI + Base64 Pipeline](./latihan-2-upload-ui.md)**.

> Di section ini kita **lengkapi `parseReceipt`** — bukan lagi placeholder. Pipeline: foto base64 → Claude vision + tool use `save_receipt_transactions` (force tool choice) → array items → insert paralel ke `transactions`. Setelah selesai, user upload foto struk → 2–3 detik kemudian semua transaksi tercatat. Tiga prompt siap copy-paste.
>
> **Alur belajarnya**: deklarasi tool `save_receipt_transactions` (untuk array items) → upgrade `parseReceipt` ke vision + tool call + insert paralel → test 3 skenario foto dengan kompleksitas berbeda.
>
> **Estimasi waktu**: 70–90 menit.

## Prasyarat Section 3

- [ ] Section 1 & 2 selesai. Script vision PoC jalan + UI upload pipeline kirim base64 ke server.
- [ ] Module 05 Section 5 selesai. Pattern tool use (`SAVE_TRANSACTION_TOOL` + `quickAddTransaction`) sudah familiar.
- [ ] Module 08 Section 2 selesai. Anda paham `tool_choice: { type: "tool", name: "..." }` untuk force panggil tool.
- [ ] Tabel `transactions` siap menerima insert (kolom: id, type, category, amount, description, date, user_id nullable, embedding nullable, created_at).
- [ ] Anda punya 2–3 foto kwitansi nyata dengan kompleksitas berbeda (struk biasa, struk multi-item, struk dengan PPN) untuk test di Prompt 3.

> ⚠️ **Penting**: Section ini melakukan **insert ke DB tanpa konfirmasi user**. Untuk production wajib tambah review step. Di latihan ini kita prioritaskan demo flow end-to-end. Buat branch git baru sebelum mulai.

---

## 📚 Referensi Dokumentasi

- **[Anthropic tool use — forcing](https://docs.claude.com/en/docs/agents-and-tools/tool-use/implement-tool-use#forcing-tool-use)** — pattern `tool_choice: { type: "tool", name }` agar Claude wajib memanggil tool.
- **[Anthropic vision + tools](https://docs.claude.com/en/docs/build-with-claude/vision)** — image content block bisa digabung dengan tools dalam satu request.
- **[Supabase insert reference](https://supabase.com/docs/reference/javascript/insert)** — pattern insert single + batch.

---

## Prompt 1 — Deklarasi Tool `save_receipt_transactions` di `src/lib/tools.ts`

### Walkthrough Manual

Tool ini berbeda dengan `save_transaction` (Module 05 Section 5) yang menerima **single item**: struk biasanya berisi **banyak item**, jadi kita pakai schema dengan **array `items`**. Plus optional `merchant` untuk konteks tambahan.

📂 **File yang dimodifikasi/dibuat**: `src/lib/tools.ts` (extend dari Module 08, atau buat `src/lib/receipt-tools.ts` terpisah supaya lebih modular).

**1. Tool definition dengan array items**

📍 Lokasi: ekspor baru `RECEIPT_TOOLS` (atau tambah ke `TOOLS` yang sudah ada — pilih sesuai preferensi arsitektur Anda). Saran: file terpisah supaya tool chatbot vs tool receipt-parser jelas pemisahannya.

```ts
// src/lib/tools.ts — atau src/lib/receipt-tools.ts
import type Anthropic from "@anthropic-ai/sdk";

export const RECEIPT_TOOLS: Anthropic.Messages.Tool[] = [
  {
    name: "save_receipt_transactions",
    description: `Ekstrak dan simpan SEMUA transaksi yang terlihat di struk/kwitansi.

KAPAN DIPAKAI:
- Setiap kali user mengirim foto struk/kwitansi.
- Panggil SEKALI dengan array items berisi SEMUA line item yang terbaca.

FIELD per item:
- amount: angka penuh Rupiah (integer positif).
- category: salah satu dari "food", "transport", "shopping", "bills",
  "entertainment", "health", "education", "other".
- description: nama item dari struk (≤40 char).
- date: tanggal struk ISO 8601 (YYYY-MM-DD). Default hari ini kalau tidak terbaca.

ATURAN PARSING:
- type per item SELALU "expense" (struk = pengeluaran user).
- Kalau struk berisi 1 total saja tanpa breakdown, return 1 item dengan
  description = nama merchant / jenis pembayaran.
- Skip baris non-transaksi (header struk, footer, "Subtotal", "Kembalian",
  "Tunai", "Diterima").
- Untuk PPN/pajak: ada 2 opsi:
  (a) Distribusikan proporsional ke amount item terkait (lebih akurat),
      atau
  (b) Buat 1 item terpisah dengan description "PPN" category "other".
  Pilih (a) kalau jumlah item ≤ 5 (mudah dibagi), (b) kalau banyak.
- merchant: opsional, nama toko/kafe untuk konteks user di respons.`,
    input_schema: {
      type: "object" as const,
      properties: {
        items: {
          type: "array",
          description: "Array semua line item yang terbaca dari struk",
          items: {
            type: "object",
            properties: {
              amount: { type: "number", description: "Nominal Rupiah (integer positif)" },
              category: { type: "string", description: "Kategori (food/transport/shopping/bills/entertainment/health/education/other)" },
              description: { type: "string", description: "Nama item dari struk (≤40 char)" },
              date: { type: "string", description: "ISO 8601 YYYY-MM-DD" },
            },
            required: ["amount", "category", "description", "date"],
          },
        },
        merchant: { type: "string", description: "Nama merchant/toko dari struk (opsional)" },
      },
      required: ["items"],
    },
  },
];
```

> 💡 **Mengapa tool terpisah dari `save_transaction` (Module 05)?** Schema-nya beda: receipt punya `items[]` (array), `save_transaction` single object. Pisah agar prompt + handler tetap clean. Plus kita tidak ingin Claude bingung memilih tool mana untuk receipt vs quick-add text.

### Yang sebaiknya tidak dilakukan

- ❌ Memakai `save_transaction` (Module 05) untuk receipt — schema-nya single item, tidak cocok untuk struk multi-item.
- ❌ Menerima `type` per item di schema — receipt selalu expense, hindari ambiguitas.
- ❌ Mengizinkan `category` sebagai string bebas (tanpa enum guidance di description) — Claude bisa keluar dari kategori yang Fin-App pakai.
- ❌ Memakai `tool_choice: "auto"` di Section 3 — receipt parser harus **force** call tool, jangan biarkan Claude jawab dengan text panjang.

### Verifikasi setelah file dibuat/diubah

1. File yang berisi `RECEIPT_TOOLS` ada (di `tools.ts` atau `receipt-tools.ts` terpisah).
2. Ekspor `RECEIPT_TOOLS: Anthropic.Messages.Tool[]` dengan 1 tool `save_receipt_transactions`.
3. Schema punya `items: array` dengan field per-item required: `amount`, `category`, `description`, `date`.
4. `npx tsc --noEmit` clean.
5. Description tool punya section KAPAN DIPAKAI + FIELD + ATURAN PARSING (handling PPN dll.).

---

**Silakan salin prompt berikut, lalu paste ke Claude Code:**

```
Tambah tool definition save_receipt_transactions untuk
ekstraksi multi-item dari foto kwitansi. Tool ini terpisah
dari save_transaction (Module 05 Section 5) karena schema-nya
berbeda (array items vs single object).

GOAL:
- Buat file baru src/lib/receipt-tools.ts (atau extend
  src/lib/tools.ts — pilih sesuai preferensi arsitektur).
- Ekspor RECEIPT_TOOLS: Anthropic.Messages.Tool[] berisi 1 tool:
  save_receipt_transactions.

- Schema input_schema:
  - items: array of object, required:
    - amount: number (Rupiah integer)
    - category: string (enum food/transport/shopping/bills/
      entertainment/health/education/other)
    - description: string ≤40 char
    - date: string ISO 8601 (YYYY-MM-DD)
  - merchant: string opsional
  - required: ["items"]

- Description tool WAJIB punya section:
  KAPAN DIPAKAI:
  - Setiap kali user kirim foto struk/kwitansi.
  - Panggil SEKALI dengan array items berisi semua line item.

  FIELD per item:
  - (jelaskan amount, category enum, description ≤40 char,
    date ISO default hari ini).

  ATURAN PARSING:
  - type per item SELALU "expense" (struk = pengeluaran).
  - Struk 1 total saja → 1 item description = merchant name.
  - Skip baris non-transaksi (Subtotal, Kembalian, Tunai, dll.).
  - PPN handling: distribusi proporsional kalau item ≤5,
    item terpisah "PPN" category "other" kalau banyak.
  - merchant opsional untuk konteks respons.

CONTEXT:
- Tool ini dipanggil dengan tool_choice forced di Prompt 2
  (parseReceipt).
- Kategori sesuai dengan yang dipakai di transactions (food,
  transport, shopping, bills, entertainment, health, education,
  other).
- Pattern Anthropic.Messages.Tool[] sama dengan TOOLS di Module
  08 Section 2.

GUARDRAIL:
- JANGAN duplikat / extend save_transaction Module 05 —
  schema berbeda (array vs single).
- JANGAN expose type di schema item — receipt selalu expense.
- JANGAN bikin category sebagai string bebas tanpa enum
  guidance — kategori harus match yang dipakai di Fin-App.
- WAJIB `type: "object" as const` untuk TypeScript happy.
- WAJIB items.items.required lengkap (amount, category,
  description, date).
```

**Verifikasi singkat:**

1. File yang berisi `RECEIPT_TOOLS` ada.
2. Schema valid dengan `items: array` + required field per item.
3. Description punya section KAPAN/FIELD/ATURAN PARSING.
4. `npx tsc --noEmit` clean.

---

## Prompt 2 — Upgrade `parseReceipt` ke Vision + Tool Call + Insert Paralel

### Walkthrough Manual

Sekarang inti integrasi: ganti placeholder `parseReceipt` (Section 2 Prompt 1) dengan implementasi penuh. Alur internal:

```mermaid
sequenceDiagram
    autonumber
    participant App as parseReceipt (server)
    participant Claude as Claude API
    participant DB as Supabase

    App->>Claude: messages: [image + text]<br/>tools: RECEIPT_TOOLS<br/>tool_choice: forced save_receipt_transactions
    Note over Claude: Vision baca struk<br/>+ panggil tool dengan array items
    Claude-->>App: tool_use: { items: [...], merchant: "..." }
    Note over App: Extract items array
    par Insert paralel
        App->>DB: insert item 1
        App->>DB: insert item 2
        App->>DB: insert item 3
    end
    DB-->>App: results array
    App-->>App: hitung sukses vs gagal
    App-->>Caller: { message, items }
```

📂 **File yang dimodifikasi**: `src/features/receipt-parser.ts` (skeleton dari Section 2).

**1. Imports**

📍 Lokasi: baris atas.

```ts
// src/features/receipt-parser.ts
"use server";

import Anthropic from "@anthropic-ai/sdk";
import { createClient } from "@/lib/supabase/server";
import { RECEIPT_TOOLS } from "@/lib/receipt-tools";  // atau "@/lib/tools" kalau Anda inline

const client = new Anthropic();

type ReceiptItem = {
  amount: number;
  category: string;
  description: string;
  date: string;
};
```

**2. Function `parseReceipt` (overwrite skeleton)**

📍 Lokasi: replace function yang ada dari Section 2.

```ts
export async function parseReceipt(input: { base64: string; mediaType: string }) {
  const t0 = Date.now();

  const response = await client.messages.create({
    model: "claude-haiku-4-5",
    max_tokens: 2048,
    tools: RECEIPT_TOOLS,
    tool_choice: { type: "tool", name: "save_receipt_transactions" },
    messages: [
      {
        role: "user",
        content: [
          {
            type: "image",
            source: {
              type: "base64",
              media_type: input.mediaType as "image/jpeg" | "image/png" | "image/webp",
              data: input.base64,
            },
          },
          {
            type: "text",
            text: "Ini foto struk/kwitansi. Ekstrak SEMUA transaksi yang terlihat dan panggil tool save_receipt_transactions dengan array items lengkap.",
          },
        ],
      },
    ],
  });

  const visionMs = Date.now() - t0;
  console.log("[parseReceipt] vision:", { ms: visionMs, stop_reason: response.stop_reason });

  const toolUse = response.content.find((c) => c.type === "tool_use");
  if (!toolUse || toolUse.type !== "tool_use") {
    return { message: "Claude tidak memanggil tool. Coba foto yang lebih jelas.", items: [] as ReceiptItem[] };
  }

  const { items, merchant } = toolUse.input as { items: ReceiptItem[]; merchant?: string };
  if (!items || items.length === 0) {
    return { message: "Tidak ada transaksi ter-ekstrak dari foto.", items: [] };
  }

  console.log("[parseReceipt] extracted:", { merchant, count: items.length });

  // Insert paralel via Promise.all
  const supabase = await createClient();
  const inserts = await Promise.all(
    items.map((item) =>
      supabase.from("transactions").insert({
        type: "expense",
        amount: item.amount,
        category: item.category,
        description: item.description.slice(0, 40),
        date: item.date,
      })
    )
  );

  const fails = inserts.filter((r) => r.error).length;
  const oks = inserts.length - fails;

  console.log("[parseReceipt] inserts:", { oks, fails, totalMs: Date.now() - t0 });

  return {
    message: `${oks} transaksi tercatat${merchant ? ` dari ${merchant}` : ""}${fails > 0 ? ` (${fails} gagal)` : ""}.`,
    items,
  };
}
```

> 💡 **Mengapa `tool_choice` force?** Tanpa force, Claude bisa jawab dengan text "saya tidak yakin struk ini bisa dibaca dengan baik" — yang tidak bisa kita parse. Force memastikan output selalu structured. Kalau benar-benar tidak bisa baca, items akan kosong dan kita handle terpisah.

### Yang sebaiknya tidak dilakukan

- ❌ Looping tool_use (multi-iteration) — receipt parser **single-shot**, tidak butuh ReAct loop. Force tool choice + extract sekali sudah cukup.
- ❌ Mengisi `user_id` dengan UUID acak — biarkan NULL (project belum punya auth, sama seperti `quickAddTransaction` Module 05).
- ❌ Embed `description` di sini — biarkan NULL. Kalau perlu di-embed nanti, jalankan backfill terpisah seperti Module 06 Section 3.
- ❌ Mengembalikan error mentah ke client — wrap di `message` string yang user-friendly.
- ❌ Skip logging — `[parseReceipt] vision` + `inserts` log penting untuk debugging "kenapa hasil parse aneh".
- ❌ Memakai `model: "claude-opus-4-7"` untuk struk biasa — Haiku cukup & lebih hemat. Upgrade hanya kalau Section 3 verifikasi nunjukin akurasi rendah.

### Verifikasi setelah file diubah

1. File `src/features/receipt-parser.ts` ter-upgrade (bukan lagi placeholder).
2. Imports lengkap: Anthropic, createClient, RECEIPT_TOOLS.
3. `tool_choice` di-force ke `save_receipt_transactions`.
4. Insert pakai `Promise.all`.
5. Return value: `{ message, items }`.
6. `npx tsc --noEmit` clean.
7. Belum di-test dari UI — itu di Prompt 3.

---

**Silakan salin prompt berikut, lalu paste ke Claude Code:**

```
Upgrade parseReceipt (skeleton dari Section 2 Prompt 1)
menjadi implementasi penuh: Claude vision + tool use forced +
insert paralel ke transactions.

GOAL:
- Modifikasi src/features/receipt-parser.ts.
- Tambah imports: Anthropic, createClient dari
  "@/lib/supabase/server", RECEIPT_TOOLS dari
  "@/lib/receipt-tools" (atau "@/lib/tools" kalau Anda inline).
- Type ReceiptItem inline (amount, category, description, date).
- const client = new Anthropic().

- Replace function parseReceipt(input):
  1. Catat timing t0 = Date.now().
  2. await client.messages.create:
     - model: "claude-haiku-4-5"
     - max_tokens: 2048
     - tools: RECEIPT_TOOLS
     - tool_choice: { type: "tool", name: "save_receipt_transactions" }
     - messages: [{ role: "user", content: [image_block, text_block] }]
     - text_block: "Ini foto struk/kwitansi. Ekstrak SEMUA transaksi
       yang terlihat dan panggil tool save_receipt_transactions dengan
       array items lengkap."
  3. Log [parseReceipt] vision: { ms, stop_reason }.
  4. Cari tool_use block di response.content. Kalau tidak ada,
     return { message: "Claude tidak memanggil tool. Coba foto
     yang lebih jelas.", items: [] }.
  5. Extract { items, merchant } dari toolUse.input.
     Kalau items kosong/undefined, return message + items: [].
  6. Log [parseReceipt] extracted: { merchant, count }.
  7. Init supabase, insert paralel via Promise.all:
     items.map(item => supabase.from("transactions").insert({
       type: "expense",
       amount: item.amount,
       category: item.category,
       description: item.description.slice(0, 40),
       date: item.date,
     }))
  8. Hitung oks vs fails.
  9. Log [parseReceipt] inserts: { oks, fails, totalMs }.
  10. Return { message: "${oks} transaksi tercatat${merchant ?
      ` dari ${merchant}` : ''}${fails > 0 ? ` (${fails} gagal)`
      : ''}.", items }.

CONTEXT:
- Skeleton parseReceipt sudah ada dari Section 2 Prompt 1.
- RECEIPT_TOOLS sudah dibuat di Prompt 1 Section ini.
- Pattern createClient supabase sama dengan
  quickAddTransaction Module 05.
- Tabel transactions kolom: id, type, category, amount,
  description, date, user_id nullable, embedding nullable.

GUARDRAIL:
- JANGAN loop tool_use (multi-iteration) — receipt parser
  single-shot.
- JANGAN isi user_id (biarkan NULL, sama dengan quick-add).
- JANGAN embed description di sini — backfill terpisah kalau
  perlu.
- JANGAN expose error mentah Supabase ke client — wrap di
  message user-friendly.
- WAJIB tool_choice forced supaya output selalu structured.
- WAJIB log vision timing + extracted count + insert results
  untuk debugging.
- Truncate description.slice(0, 40) untuk jaga DB column
  length (defensive).
- Pakai Haiku — Opus overkill untuk struk biasa.
```

**Verifikasi singkat:**

1. File `src/features/receipt-parser.ts` ter-upgrade.
2. `npx tsc --noEmit` clean.
3. Dev server jalan tanpa error.
4. Skeleton sudah diganti dengan implementasi penuh (sudah ada vision call + tool extract + DB insert).

---

## Prompt 3 — Test End-to-End dengan 3 Skenario Foto

### Walkthrough Manual

Pipeline lengkap sudah ter-pasang. Sekarang uji manual via UI Fin-App dengan **3 foto** yang merepresentasikan kompleksitas berbeda.

📂 **Tidak ada file yang dimodifikasi** — semua eksekusi manual di browser.

**1. Siapkan 3 foto kwitansi**

- **A. Sederhana**: struk dengan 1–2 item (mis. struk parkir, kuitansi tunggal).
- **B. Multi-item**: struk supermarket / kafe dengan 5–10 item.
- **C. Dengan PPN/pajak**: struk yang punya breakdown "Subtotal + PPN 11% = Total" (mis. restoran besar, hotel, retail formal).

**2. Tiga skenario test**

📍 Lokasi: chatbot UI Fin-App di browser → halaman transaksi → tombol Upload Kwitansi.

| # | Foto | Yang diharapkan | Cek di Supabase |
|---|---|---|---|
| 1 | A — Sederhana | `"1–2 transaksi tercatat dari [merchant]"` | 1–2 row baru muncul, amount + description sesuai |
| 2 | B — Multi-item | `"5–10 transaksi tercatat dari [merchant]"` | Semua item ter-insert paralel dengan kategori yang sesuai |
| 3 | C — Dengan PPN | `"N transaksi tercatat dari [merchant]"` (N bisa = jumlah item + 1 item PPN, atau N = jumlah item dengan amount sudah ter-distribusi PPN) | Cek apakah total sum amount items ≈ total tertulis di struk |

**3. Hal yang harus diperhatikan**

- ✅ Latency total ~2–4 detik (vision Haiku ~1.5–2.5s + insert paralel ~200–500ms).
- ✅ Log terminal dev server menampilkan `[parseReceipt] vision: { ms, stop_reason }` + `extracted: { count }` + `inserts: { oks, fails }`.
- ✅ Pesan UI sesuai jumlah transaksi tercatat.
- ✅ Cek Supabase Table Editor → row baru dengan `type=expense`, kategori sesuai, amount benar.
- ⚠️ **Red flag**: Claude mengarang angka (mis. total 100rb tapi sum items jadi 250rb). Tindak lanjut: tampilkan **preview & konfirmasi** di iterasi UI berikutnya.

**4. (Opsional) Bandingkan dengan model Sonnet untuk foto sulit**

Kalau foto C menghasilkan parse yang kurang akurat (mis. PPN salah dihitung), ubah `model` di `parseReceipt` ke `claude-sonnet-4-6` dan jalankan ulang. Bandingkan akurasi vs biaya.

### Yang sebaiknya tidak dilakukan

- ❌ Membuat script automation — verifikasi manual via UI cukup untuk fase eksplorasi.
- ❌ Skip skenario C — itu test paling penting untuk membuktikan tool description "handling PPN" bekerja.
- ❌ Auto-revert insert kalau salah — di latihan ini biarkan jadi bahan refleksi (konfirmasi UX adalah follow-up).
- ❌ Tambah review step di section ini — fokus dulu pada flow ekstraksi. UX preview/confirm di iterasi berikutnya.

### Verifikasi setelah eksperimen

1. Skenario 1 (sederhana): 1–2 row baru di Supabase, message UI sesuai.
2. Skenario 2 (multi-item): 5–10 row baru, semua kategori valid (food/transport/dll.), insert paralel (timing terlihat dari log).
3. Skenario 3 (PPN): jumlah row + sum amount approximate total struk. Strategi PPN (item terpisah atau distribusi) terlihat dari `description` items.
4. Tidak ada error 500 di route.
5. Log terminal lengkap dengan timing per stage (vision ms, total ms).

---

**Silakan salin prompt berikut, lalu paste ke Claude Code:**

```
Bantu saya test end-to-end pipeline upload kwitansi di Fin-App.
Saya akan jalankan 3 skenario manual via UI; bantu menyusun
checklist observasi + diagnose kalau ada yang tidak sesuai.

GOAL:
- Beri saya panduan eksperimen 3 foto kwitansi:
  A. Sederhana (1-2 item, mis. struk parkir).
  B. Multi-item (5-10 item, mis. struk supermarket).
  C. Dengan PPN (breakdown Subtotal + PPN 11% = Total).

- Untuk tiap skenario, checklist observasi:
  - Pesan UI sesuai jumlah transaksi tercatat?
  - Cek Supabase Table Editor: row baru muncul dengan
    type=expense, kategori valid, amount benar?
  - Latency total ~2-4 detik?
  - Log terminal: [parseReceipt] vision: { ms, stop_reason }
    + extracted: { count } + inserts: { oks, fails }?
  - Sum amount items ≈ total tertulis di struk?
  - Untuk PPN: strategi handling (item terpisah "PPN" atau
    distribusi proporsional)?

- Diagnose:
  (a) Pesan UI bilang "Claude tidak memanggil tool" → cek
      apakah foto jelas, atau coba model Sonnet.
  (b) Jumlah items kurang dari yang terlihat di struk →
      perketat description tool ATURAN PARSING (skip
      Subtotal/Kembalian, dst).
  (c) Amount salah magnitude (25rb jadi 250rb) → cek apakah
      vision Haiku punya issue dengan font tertentu, coba
      Sonnet.
  (d) PPN handling tidak konsisten → eksplisitkan strategi
      di description tool.
  (e) Error 500 di route → cek tool_choice format & response
      shape.

CONTEXT:
- Saya akan menjalankan manual di browser, bukan via Claude
  Code Bash tool.
- Pipeline parseReceipt sudah ter-upgrade di Prompt 2.
- Tabel transactions siap menerima insert (user_id NULL OK).
- Saya punya 2-3 foto kwitansi nyata untuk test.

GUARDRAIL:
- JANGAN bikin script automation — manual cukup.
- JANGAN modifikasi kode di prompt ini — fokus verifikasi.
- Format jawaban sebagai test plan markdown + diagnostic guide.
- WAJIB highlight skenario C sebagai test paling penting
  (PPN handling = bukti tool description ATURAN PARSING bekerja).
```

**Verifikasi singkat:**

1. Anda menerima dari Claude: checklist 3 skenario + diagnostic guide.
2. Skenario A: 1–2 row baru di Supabase, message UI sesuai.
3. Skenario B: 5–10 row baru, semua kategori valid.
4. Skenario C: row + sum amount approximate total struk.
5. Log terminal lengkap dengan timing per stage.

---

## Validasi Akhir Section 3

Sebelum Anda menyelesaikan Module 09, mari pastikan pipeline upload kwitansi bekerja end-to-end:

- [ ] File `src/lib/receipt-tools.ts` (atau extend `tools.ts`) ekspor `RECEIPT_TOOLS` dengan tool `save_receipt_transactions`.
- [ ] Schema tool punya `items: array` dengan field required per item + optional `merchant`.
- [ ] `src/features/receipt-parser.ts` ter-upgrade: vision call + `tool_choice` forced + extract items + insert paralel.
- [ ] Logging `[parseReceipt]` muncul dengan stage `vision`, `extracted`, `inserts` + timing.
- [ ] Test skenario A (struk sederhana): row baru muncul di Supabase, pesan UI sesuai.
- [ ] Test skenario B (multi-item): semua items ter-insert paralel.
- [ ] Test skenario C (dengan PPN): strategi handling PPN konsisten (item terpisah atau distribusi).
- [ ] Tidak ada regresi: quick-add (Module 05) + RAG chatbot (Module 07) + tool use chatbot (Module 08) tetap jalan.
- [ ] `npx tsc --noEmit` clean.
- [ ] Build production sukses (`npm run build`).

## Refleksi Section 3

Refleksikan pertanyaan berikut secara mendalam:

1. Pipeline saat ini **auto-insert tanpa konfirmasi user**. Apa risiko UX-nya — apakah ada skenario di mana user marah karena transaksi salah ter-insert? Bagaimana cara design preview UI yang minimal friction tapi tetap memberi user kontrol (mis. tampil 3 detik countdown sebelum confirm, atau modal review)?
2. Strategi PPN dipilih oleh Claude (terdistribusi proporsional vs item terpisah). Apa konsekuensi untuk **analytics** di Fin-App? (mis. kategori "other" untuk PPN bisa membengkak; sum per kategori jadi over/under count). Bagaimana cara desain skema yang lebih bersih?
3. Saat ini tool description tidak menyebut handling **mata uang non-IDR** (mis. struk hotel luar negeri dalam USD/SGD). Bagaimana Anda extend tool agar handle currency? Apakah cukup tambah field `currency` di item, atau perlu konversi runtime?
4. Vision Haiku biaya ~$0.0003 per image. Kalau Fin-App punya 10K user yang upload 5 struk/bulan = 50K image = ~$15/bulan. Pada skala apa biaya jadi concern, dan apa strategi caching (mis. hash file → skip duplikat)?
5. Sekarang user upload **satu foto** per request. Bagaimana cara handle **multi-foto sekaligus** (mis. user foto 5 struk dalam satu sesi)? Apakah pattern paralel sama atau perlu queue/batch?
6. Pipeline ini terpisah dari chatbot AI Advisor. Bagaimana cara **integrasikan ke chatbot** supaya user bisa attach foto langsung di percakapan ("nih catat kopi ini" + attachment)? Apa file/route mana yang perlu diubah?
7. Anda men-design tool dengan field `category` enum-like di description. Bagaimana cara membuat enum **dynamic** (mis. user bisa custom kategori di settings)? Apakah perlu fetch list dari DB → inject ke description runtime?

---

⬅️ Kembali: **[Section 2 — Upload UI](./latihan-2-upload-ui.md)** · 🏠 Index: **[Module 09 — Latihan](./latihan.md)** · ➡️ Lanjut: **Module 10+** (akan datang)
