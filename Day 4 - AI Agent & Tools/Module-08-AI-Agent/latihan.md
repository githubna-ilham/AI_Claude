# Module 08 — Latihan: Multi-Tool di Quick-Add (Bertahap menuju Parallel)

> Module 08 mengembangkan kemampuan **AI Agent** di Fin-App lewat satu pipeline konkret: **extend `quickAddTransaction`** (Module 05 Section 5) agar punya 3 tools (save + delete + update), dipasang **bertahap** — dari single tool per request, lalu di-upgrade ke **parallel** execution. Tiga prompt siap copy-paste.
>
> Total estimasi: ±2–2,5 jam efektif.
>
> ⚠️ Module ini akan diperluas dengan section lanjutan (ReAct loop runtime, memory, error recovery, multi-agent) di iterasi berikutnya.

## Alur Progresif (Penting Dipahami)

Kita sengaja mendesain 3 prompt **bertingkat** supaya peserta merasakan dampak tiap perubahan:

| Prompt | Yang dibangun | Status `quickAddTransaction` |
|---|---|---|
| 1 | Definisi 2 tools baru (`delete_transactions` + `update_transaction`) + handler-nya | Belum tersentuh — tools standalone |
| 2 | Wire tools ke `quickAddTransaction` + dispatcher | Bisa save/delete/update — **single tool per request** |
| 3 | Upgrade ke parallel execution | Bisa multi-save + mixed save/delete/update **dalam 1 kalimat** |

Tiap prompt punya verifikasi sendiri sebelum lanjut — jangan lompat.

## Prinsip Kontinuitas (Wajib Diperhatikan)

- ✅ **Lanjutkan kode yang sudah ada** dari Module 05 Section 5 (`quickAddTransaction` + `SAVE_TRANSACTION_TOOL`).
- ❌ **Jangan hapus** komponen yang sudah jadi di module sebelumnya, kecuali Claude / latihan secara eksplisit memintanya.
- ✅ **Verifikasi setelah setiap prompt** — pastikan prompt sebelumnya tidak rusak sebelum lanjut.
- 📖 **Baca dulu** bagian "Konsep AI Agent" dan "Tools & Function Calling" di `materi.md` sebelum mulai Prompt 1 — intuisi pola ReAct + flow 4-langkah function calling + parallel function calling penting supaya implementasi tidak hanya "ikut resep".

## Prasyarat

- [ ] Module 05 Section 5 selesai. `quickAddTransaction` + `SAVE_TRANSACTION_TOOL` ada di `src/features/quick-add.ts` dan jalan untuk single-transaksi.
- [ ] Anda sudah membaca `materi.md` — paham definisi AI Agent + pola ReAct + flow 4-langkah function calling + parallel function calling.
- [ ] Halaman transaksi Fin-App siap. Quick-add field render dan submit OK.
- [ ] Tabel `transactions` siap menerima insert/update/delete (kolom: id, type, category, amount, description, date, user_id nullable).
- [ ] `@anthropic-ai/sdk` terinstal dan `ANTHROPIC_API_KEY` aktif.
- [ ] Claude Code aktif di terminal terpisah.

> ⚠️ **Penting**: Latihan ini memodifikasi `quickAddTransaction` yang sudah berfungsi. Buat branch git baru sebelum mulai Prompt 1 supaya mudah rollback.

---

## 📚 Referensi Dokumentasi

- **[Anthropic tool use](https://docs.claude.com/en/docs/agents-and-tools/tool-use/overview)** — anatomi tool definition + flow 4-langkah.
- **[Anthropic parallel tool use](https://docs.claude.com/en/docs/agents-and-tools/tool-use/implement-tool-use#parallel-tool-use)** — pola memanggil tool yang sama / beda beberapa kali dalam satu response (dipakai di Prompt 3).
- **[Anthropic tool_choice](https://docs.claude.com/en/docs/agents-and-tools/tool-use/implement-tool-use#controlling-claudes-output)** — beda `auto` / `any` / `tool`.
- **[Supabase update reference](https://supabase.com/docs/reference/javascript/update)** — pattern UPDATE per row.
- **[Supabase delete reference](https://supabase.com/docs/reference/javascript/delete)** — pattern DELETE WHERE id IN.
- **[Promise.all (MDN)](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/all)** — eksekusi paralel di TypeScript.

---

## Prompt 1 — Definisi 2 Tools Baru (`delete_transactions` + `update_transaction`) + Handlers

### Walkthrough Manual

Di prompt ini kita **belum** menyentuh function `quickAddTransaction`. Fokus: deklarasi dua tool baru + handler eksekusinya, sehingga di Prompt 2 tinggal di-wire. Pemisahan ini membuat tiap perubahan kecil dan mudah di-verifikasi.

📂 **File yang dimodifikasi**: `src/features/quick-add.ts` (tambah definisi + handler di samping yang sudah ada dari Module 05 Section 5).

**1. Tool definition `DELETE_TRANSACTION_TOOL`**

📍 Lokasi: di samping `SAVE_TRANSACTION_TOOL` yang sudah ada.

```ts
// src/features/quick-add.ts — tambahan
const DELETE_TRANSACTION_TOOL: Anthropic.Messages.Tool = {
  name: "delete_transactions",
  description: `Hapus transaksi dari database berdasarkan keyword di description.

KAPAN DIPAKAI:
- User minta hapus/batalkan/buang transaksi: "hapus transaksi kopi terakhir",
  "batalkan parkir kemarin", "buang transaksi yang salah".

CARA KERJA:
- Cari transaksi yang description mengandung keyword (case-insensitive),
  diurutkan dari yang TERBARU, lalu hapus sebanyak max_delete row.

FIELD:
- description_keyword: kata benda saja (JANGAN sertakan kata kerja "hapus").
- max_delete: default 1, MAKSIMAL 5 (safety cap di server).`,
  input_schema: {
    type: "object" as const,
    properties: {
      description_keyword: { type: "string", description: "Kata kunci match (case-insensitive)" },
      max_delete: { type: "number", description: "Jumlah max yang dihapus (default 1, max 5)" },
    },
    required: ["description_keyword"],
  },
};
```

**2. Tool definition `UPDATE_TRANSACTION_TOOL`**

📍 Lokasi: di bawah `DELETE_TRANSACTION_TOOL`.

```ts
const UPDATE_TRANSACTION_TOOL: Anthropic.Messages.Tool = {
  name: "update_transaction",
  description: `Ubah field transaksi paling baru yang match keyword di description.

KAPAN DIPAKAI:
- User minta UBAH / GANTI / PERBAIKI / KOREKSI nilai transaksi:
  "ubah amount kopi terakhir jadi 30rb",
  "ganti kategori parkir ke transport",
  "koreksi deskripsi makan jadi makan padang".

CARA KERJA:
- Cari SATU transaksi terbaru yang description mengandung keyword,
  lalu UPDATE field yang disebutkan user (amount / category / description).

FIELD:
- description_keyword: kata benda untuk match transaksi yang mau diubah.
- new_amount: nilai amount baru (opsional).
- new_category: kategori baru (opsional, salah satu dari food/transport/
  shopping/bills/entertainment/health/education/salary/other).
- new_description: description baru (opsional, ≤40 char).
- MINIMAL SATU dari new_* field WAJIB di-set, jika tidak tool tidak
  bisa mengubah apa pun.`,
  input_schema: {
    type: "object" as const,
    properties: {
      description_keyword: { type: "string", description: "Kata kunci match transaksi yang mau diubah" },
      new_amount: { type: "number", description: "Amount baru (Rupiah integer)" },
      new_category: { type: "string", description: "Kategori baru" },
      new_description: { type: "string", description: "Description baru (≤40 char)" },
    },
    required: ["description_keyword"],
  },
};
```

**3. Type result + helper handler**

📍 Lokasi: **module-level** di `src/features/quick-add.ts`, tepatnya **setelah kedua tool definitions** baru (`DELETE_TRANSACTION_TOOL` + `UPDATE_TRANSACTION_TOOL` dari step 1 & 2) tapi **sebelum function `quickAddTransaction`** yang sudah ada dari Module 05 Section 5.

Struktur file akhir (urutan module-level) jadi seperti ini:

```ts
// src/features/quick-add.ts
"use server";

import Anthropic from "@anthropic-ai/sdk";
import { createClient } from "@/lib/supabase/server";
import { revalidatePath } from "next/cache";
import { QUICK_ADD_SYSTEM } from "@/features/prompts";

const client = new Anthropic();

// === TOOL DEFINITIONS ===
const SAVE_TRANSACTION_TOOL: Anthropic.Messages.Tool = { /* dari Module 05 */ };
const DELETE_TRANSACTION_TOOL: Anthropic.Messages.Tool = { /* step 1 di atas */ };
const UPDATE_TRANSACTION_TOOL: Anthropic.Messages.Tool = { /* step 2 di atas */ };

// === TYPES ===
type ParsedTransaction = { /* dari Module 05 */ };

type ExecResult =                       // ← tambahan
  | { ok: true; kind: "save"; id?: string }
  | { ok: true; kind: "delete"; count: number }
  | { ok: true; kind: "update"; field_changed: string[] }
  | { ok: false; kind: "save" | "delete" | "update" | "unknown"; error: string };

// === HANDLERS (helper, dipakai oleh dispatcher di Prompt 2) ===
async function executeDelete(supabase, input) { /* ... */ }   // ← tambahan
async function executeUpdate(supabase, input) { /* ... */ }   // ← tambahan

// === MAIN FUNCTION ===
export async function quickAddTransaction(formData: FormData) {
  // body fungsi yang ada dari Module 05 — BELUM diubah di Prompt 1
}
```

```ts
type ExecResult =
  | { ok: true; kind: "save"; id?: string }
  | { ok: true; kind: "delete"; count: number }
  | { ok: true; kind: "update"; field_changed: string[] }
  | { ok: false; kind: "save" | "delete" | "update" | "unknown"; error: string };

async function executeDelete(
  supabase: Awaited<ReturnType<typeof createClient>>,
  input: { description_keyword: string; max_delete?: number }
): Promise<ExecResult> {
  const limit = Math.min(Math.max(input.max_delete ?? 1, 1), 5); // hard cap 5

  const { data: matches, error: findErr } = await supabase
    .from("transactions")
    .select("id")
    .ilike("description", `%${input.description_keyword}%`)
    .order("date", { ascending: false })
    .limit(limit);

  if (findErr) return { ok: false, kind: "delete", error: findErr.message };
  if (!matches || matches.length === 0) {
    return { ok: false, kind: "delete", error: `Tidak ada transaksi dengan keyword "${input.description_keyword}".` };
  }

  const ids = matches.map((m) => m.id);
  const { error: delErr } = await supabase.from("transactions").delete().in("id", ids);
  if (delErr) return { ok: false, kind: "delete", error: delErr.message };

  return { ok: true, kind: "delete", count: matches.length };
}

async function executeUpdate(
  supabase: Awaited<ReturnType<typeof createClient>>,
  input: { description_keyword: string; new_amount?: number; new_category?: string; new_description?: string }
): Promise<ExecResult> {
  // Bangun update payload dari field yang non-undefined
  const updatePayload: Record<string, unknown> = {};
  const fieldChanged: string[] = [];
  if (input.new_amount !== undefined) { updatePayload.amount = input.new_amount; fieldChanged.push("amount"); }
  if (input.new_category !== undefined) { updatePayload.category = input.new_category; fieldChanged.push("category"); }
  if (input.new_description !== undefined) { updatePayload.description = input.new_description.slice(0, 40); fieldChanged.push("description"); }

  if (fieldChanged.length === 0) {
    return { ok: false, kind: "update", error: "Tidak ada field baru yang disebutkan untuk diubah." };
  }

  // Cari SATU transaksi terbaru match
  const { data: match, error: findErr } = await supabase
    .from("transactions")
    .select("id")
    .ilike("description", `%${input.description_keyword}%`)
    .order("date", { ascending: false })
    .limit(1)
    .maybeSingle();

  if (findErr) return { ok: false, kind: "update", error: findErr.message };
  if (!match) {
    return { ok: false, kind: "update", error: `Tidak ada transaksi dengan keyword "${input.description_keyword}".` };
  }

  const { error: updErr } = await supabase.from("transactions").update(updatePayload).eq("id", match.id);
  if (updErr) return { ok: false, kind: "update", error: updErr.message };

  return { ok: true, kind: "update", field_changed: fieldChanged };
}
```

> 💡 **Mengapa update hanya 1 transaksi?** Update bulk berisiko user salah ganti banyak row. Single update + matching paling baru = perilaku yang predictable dan aman.

### Yang sebaiknya tidak dilakukan

- ❌ Menyentuh function `quickAddTransaction` di Prompt 1 — kita pisah agar perubahan kecil dan mudah dibatalkan.
- ❌ Mengizinkan `max_delete` tanpa hard cap server-side — Claude bisa salah parse "semua" jadi angka besar.
- ❌ Update by raw id — Claude tidak punya akses id. Pakai keyword + paling baru.
- ❌ Update multiple row sekaligus — terlalu berisiko untuk single command. Single match cukup.
- ❌ Memberikan akses update ke field `type`, `date`, atau `user_id` — itu di luar scope tool ini.

### Verifikasi setelah file diubah

1. `npx tsc --noEmit` clean.
2. Export `DELETE_TRANSACTION_TOOL`, `UPDATE_TRANSACTION_TOOL`, `executeDelete`, `executeUpdate` tersedia (lihat di IDE auto-import).
3. (Opsional) Smoke test dari script:
   ```ts
   // experiments/test-handlers.ts
   import { createClient } from "@/lib/supabase/server";
   import { executeDelete, executeUpdate } from "@/features/quick-add";

   const supabase = await createClient();
   console.log(await executeDelete(supabase, { description_keyword: "test-xyz" }));
   console.log(await executeUpdate(supabase, { description_keyword: "test-xyz", new_amount: 99000 }));
   ```
   Run: `npx tsx --env-file=.env.local experiments/test-handlers.ts`. Output: error informatif kalau keyword tidak match, atau success kalau ada data nyata yang cocok.

---

**Silakan salin prompt berikut, lalu paste ke Claude Code:**

```
Tambahkan 2 tool definitions baru (delete_transactions +
update_transaction) + 2 handler-nya di src/features/quick-add.ts.
JANGAN sentuh function quickAddTransaction yet — itu di Prompt 2.

GOAL:
- Modifikasi src/features/quick-add.ts (sudah ada dari Module 05 Section 5).

  1. Tambah DELETE_TRANSACTION_TOOL (Anthropic.Messages.Tool):
     - name: "delete_transactions"
     - description: KAPAN DIPAKAI (hapus/batalkan/buang), CARA KERJA
       (ILIKE %keyword% + ORDER BY date DESC LIMIT max_delete), FIELD
       (description_keyword tanpa kata kerja, max_delete default 1 max 5).
     - input_schema: properties description_keyword (string), max_delete
       (number), required ["description_keyword"].

  2. Tambah UPDATE_TRANSACTION_TOOL (Anthropic.Messages.Tool):
     - name: "update_transaction"
     - description: KAPAN DIPAKAI (ubah/ganti/koreksi nilai), CARA KERJA
       (cari SATU transaksi terbaru, update field yang disebut), FIELD
       (description_keyword + new_amount? + new_category? + new_description?),
       aturan MINIMAL SATU new_* field wajib.
     - input_schema: properties description_keyword (string), new_amount
       (number), new_category (string), new_description (string),
       required ["description_keyword"].

  3. Tambah type ExecResult discriminated union:
     - { ok: true, kind: "save", id?: string }
     - { ok: true, kind: "delete", count: number }
     - { ok: true, kind: "update", field_changed: string[] }
     - { ok: false, kind: "save"|"delete"|"update"|"unknown", error: string }

  4. Ekspor async function executeDelete(supabase, input):
     a. Clamp max_delete ke [1, 5] hard cap.
     b. SELECT id WHERE description ILIKE '%keyword%' ORDER BY date DESC
        LIMIT N.
     c. Kosong → error informatif.
     d. DELETE WHERE id IN (...). Return count.

  5. Ekspor async function executeUpdate(supabase, input):
     a. Bangun updatePayload dari new_* field yang non-undefined,
        track fieldChanged: string[].
     b. Kalau fieldChanged kosong, return error "Tidak ada field baru
        yang disebutkan untuk diubah."
     c. SELECT id WHERE description ILIKE '%keyword%' ORDER BY date DESC
        LIMIT 1 .maybeSingle(). Slice description ≤40 char defensive.
     d. UPDATE WHERE id = match.id. Return success + fieldChanged.

CONTEXT:
- SAVE_TRANSACTION_TOOL & quickAddTransaction sudah ada dari Module
  05 Section 5 — JANGAN ubah.
- Supabase ILIKE = case-insensitive pattern match.
- user_id NULL OK (project belum punya auth).

GUARDRAIL:
- JANGAN sentuh function quickAddTransaction di Prompt 1.
- WAJIB hard cap max_delete ke 5 di server.
- JANGAN izinkan update tanpa minimal 1 new_* field.
- JANGAN update by raw id dari Claude.
- JANGAN update multiple row sekaligus.
- WAJIB type discriminated union untuk ExecResult.
- Ekspor handler functions supaya bisa di-test independent.
```

**Verifikasi singkat:**

1. `npx tsc --noEmit` clean.
2. Ekspor baru tersedia: `DELETE_TRANSACTION_TOOL`, `UPDATE_TRANSACTION_TOOL`, `executeDelete`, `executeUpdate`.
3. Type `ExecResult` ada dengan 4 variant.
4. (Opsional) Smoke test dari script: panggil `executeDelete({ description_keyword: "test-xyz" })` → return error informatif kalau tidak match.

---

## Prompt 2 — Wire 3 Tools ke `quickAddTransaction` (Single Tool per Request)

### Walkthrough Manual

Sekarang **wire** ketiga tools ke `quickAddTransaction`. Tahap ini sengaja membatasi **satu tool per request** — extract menggunakan `.find` (first match). Tujuannya: peserta bisa **rasakan dispatcher bekerja** sebelum upgrade ke parallel di Prompt 3.

📂 **File yang dimodifikasi**:
- `src/features/quick-add.ts` — wire dispatcher
- `src/features/prompts.ts` — extend `QUICK_ADD_INSTRUCTION` dengan section delete + update

**1. Update `tools` di `client.messages.create`**

📍 Lokasi: di dalam `quickAddTransaction`.

```ts
// src/features/quick-add.ts — di dalam quickAddTransaction
const resp = await client.messages.create({
  model: "claude-haiku-4-5",
  max_tokens: 1024,
  system: QUICK_ADD_SYSTEM,
  tools: [SAVE_TRANSACTION_TOOL, DELETE_TRANSACTION_TOOL, UPDATE_TRANSACTION_TOOL], // ← 3 tools
  tool_choice: { type: "any" }, // wajib panggil tool
  messages: [{ role: "user", content: `Hari ini: ${today}\n\nInstruksi: ${text}` }],
});
```

> 💡 **Mengapa `any` bukan `auto`?** `any` memastikan Claude **wajib** memanggil tool (tidak boleh jawab tekstual). Untuk quick-add, kita selalu mau ada action.

**2. Extract first tool_use + dispatch by name (single only)**

📍 Lokasi: ganti pattern lama (yang asumsi `save_transaction` tunggal) dengan dispatcher generik berdasarkan `tb.name`. **Pakai `.find` (single only)** — parallel di Prompt 3.

```ts
// src/features/quick-add.ts — dispatcher single-tool
const toolBlock = resp.content.find(
  (b): b is Anthropic.Messages.ToolUseBlock => b.type === "tool_use"
);

if (!toolBlock) {
  return { ok: false, message: "Claude tidak memanggil tool. Coba teks lebih spesifik." };
}

console.log(`[quickAdd] tool call: ${toolBlock.name}`);

const supabase = await createClient();

let result: ExecResult;
if (toolBlock.name === "save_transaction") {
  // Logika save yang sudah ada (extract parsed, insert)
  const parsed = toolBlock.input as ParsedTransaction;
  const { error } = await supabase.from("transactions").insert({
    amount: parsed.amount,
    type: parsed.type,
    category: parsed.category,
    date: parsed.date,
    description: parsed.description,
  });
  result = error
    ? { ok: false, kind: "save", error: error.message }
    : { ok: true, kind: "save" };
} else if (toolBlock.name === "delete_transactions") {
  result = await executeDelete(supabase, toolBlock.input as { description_keyword: string; max_delete?: number });
} else if (toolBlock.name === "update_transaction") {
  result = await executeUpdate(supabase, toolBlock.input as { description_keyword: string; new_amount?: number; new_category?: string; new_description?: string });
} else {
  result = { ok: false, kind: "unknown", error: `Unknown tool: ${toolBlock.name}` };
}

revalidatePath("/transactions");

// Compose message berdasarkan jenis action
let message: string;
if (!result.ok) {
  message = `Gagal: ${result.error}`;
} else if (result.kind === "save") {
  message = "1 transaksi tercatat.";
} else if (result.kind === "delete") {
  message = `${result.count} transaksi dihapus.`;
} else {
  message = `Transaksi diperbarui (field: ${result.field_changed.join(", ")}).`;
}

return { ok: result.ok, message };
```

> 💡 **Pakai `.find` di tahap ini sengaja**. Walau Claude bisa kembalikan multiple `tool_use` blocks, kita ambil yang pertama saja untuk fokus mendemonstrasikan dispatcher dulu. Multi/mixed di Prompt 3.

**3. Update `QUICK_ADD_INSTRUCTION` di `prompts.ts`**

📍 Lokasi: tambahkan section DELETE + UPDATE + aturan "satu tool per request".

```ts
// src/features/prompts.ts — tambahan di QUICK_ADD_INSTRUCTION
DELETE TRANSAKSI:
Kalau user minta HAPUS / BATALKAN / BUANG / DELETE, panggil tool
delete_transactions dengan description_keyword (kata benda saja).
Contoh:
- "hapus transaksi kopi terakhir" → delete_transactions({ description_keyword: "kopi", max_delete: 1 })
- "batalkan 2 transaksi parkir" → max_delete: 2

UPDATE TRANSAKSI:
Kalau user minta UBAH / GANTI / KOREKSI / PERBAIKI nilai transaksi,
panggil tool update_transaction dengan description_keyword (untuk
mencari) + new_amount / new_category / new_description (field yang
diubah).
Contoh:
- "ubah amount kopi terakhir jadi 30rb" → { description_keyword: "kopi", new_amount: 30000 }
- "ganti kategori parkir ke transport" → { description_keyword: "parkir", new_category: "transport" }
- "koreksi deskripsi makan jadi makan padang" → { description_keyword: "makan", new_description: "makan padang" }

SATU TOOL PER REQUEST:
Untuk sekarang, panggil HANYA SATU tool per request. Kalau input
mengandung multiple actions (mis. "ngopi 25rb dan hapus parkir"),
pilih SATU yang paling jelas; biarkan yang lain di-handle di
request berikutnya.
```

> 💡 **Aturan "satu tool per request"** sengaja membatasi Claude di tahap ini. Di Prompt 3 kita longgarkan + tambah `Promise.all` di app side.

### Yang sebaiknya tidak dilakukan

- ❌ Pakai `.filter` + `Promise.all` di Prompt 2 — itu spoiler untuk Prompt 3. Pakai `.find` dulu supaya peserta merasakan progression.
- ❌ Membuang `SAVE_TRANSACTION_TOOL` schema atau alur insert dari Module 05.
- ❌ Tambah tool destruktif lain (mass delete, drop table) — fokus 3 tool dulu.
- ❌ Mengembalikan error mentah Supabase ke user — wrap di `message` user-friendly.
- ❌ Lupa update `QUICK_ADD_INSTRUCTION` — tanpa instruksi delete/update, Claude tidak tahu kapan memanggil tool baru.

### Verifikasi setelah file diubah

1. `npx tsc --noEmit` clean.
2. Reload halaman transaksi.
3. Pastikan ada beberapa transaksi nyata di DB sebagai bahan test delete/update.
4. Test SAVE (regresi): `"ngopi 5000"` → 1 row baru, message `"1 transaksi tercatat."`. Log: `[quickAdd] tool call: save_transaction`.
5. Test DELETE: `"hapus transaksi kopi terakhir"` → 1 row "kopi" hilang, message `"1 transaksi dihapus."`. Log: `[quickAdd] tool call: delete_transactions`.
6. Test UPDATE: `"ubah amount kopi terakhir jadi 30000"` → 1 row dengan "kopi" punya amount baru 30000, message `"Transaksi diperbarui (field: amount)."`. Log: `[quickAdd] tool call: update_transaction`.
7. Test input multi (mis. `"ngopi 25rb dan hapus parkir"`) → hanya **satu** action yang ter-eksekusi (yang Claude pilih). Itu yang akan kita upgrade di Prompt 3.

---

**Silakan salin prompt berikut, lalu paste ke Claude Code:**

```
Wire 3 tools (save + delete + update dari Prompt 1) ke
quickAddTransaction. Untuk sekarang single tool per request saja
(pakai .find, bukan .filter). Parallel di Prompt 3.

GOAL:
- Modifikasi src/features/quick-add.ts:
  1. Update tools di client.messages.create:
     tools: [SAVE_TRANSACTION_TOOL, DELETE_TRANSACTION_TOOL,
             UPDATE_TRANSACTION_TOOL]
     tool_choice: { type: "any" }

  2. Ganti pattern extract dari old single-save logic ke dispatcher:
     - const toolBlock = resp.content.find(b => b.type === "tool_use")
       dengan type guard Anthropic.Messages.ToolUseBlock.
     - Kalau tidak ada, return { ok: false, message: "Claude tidak
       memanggil tool. Coba teks lebih spesifik." }.
     - console.log(`[quickAdd] tool call: ${toolBlock.name}`).
     - if/else if dispatch by toolBlock.name:
       * save_transaction → extract ParsedTransaction, insert ke
         transactions (logika save yang sudah ada).
       * delete_transactions → await executeDelete(supabase, input).
       * update_transaction → await executeUpdate(supabase, input).
       * default → result = { ok: false, kind: "unknown", error: ... }.

  3. revalidatePath("/transactions").

  4. Compose message berdasarkan result.kind:
     - !result.ok → "Gagal: ${error}"
     - kind === "save" → "1 transaksi tercatat."
     - kind === "delete" → "${count} transaksi dihapus."
     - kind === "update" → "Transaksi diperbarui (field: ${fieldChanged.join(', ')})."

  5. Return { ok, message }.

- Modifikasi src/features/prompts.ts (QUICK_ADD_INSTRUCTION):
  - Tambah section DELETE TRANSAKSI (3 contoh) +
    UPDATE TRANSAKSI (3 contoh) +
    SATU TOOL PER REQUEST (aturan + alasan).

CONTEXT:
- DELETE_TRANSACTION_TOOL, UPDATE_TRANSACTION_TOOL, executeDelete,
  executeUpdate sudah ada dari Prompt 1.
- SAVE_TRANSACTION_TOOL dan ParsedTransaction type sudah ada dari
  Module 05 Section 5.

GUARDRAIL:
- JANGAN pakai .filter atau Promise.all di prompt ini — itu Prompt 3.
- JANGAN buang logika save existing — tetap pakai pattern yang sama.
- JANGAN pakai tool_choice "auto" — pakai "any" supaya Claude wajib
  panggil tool.
- JANGAN expose error mentah Supabase ke user.
- WAJIB section "SATU TOOL PER REQUEST" di QUICK_ADD_INSTRUCTION
  supaya Claude tidak coba multi-call.
```

**Verifikasi singkat:**

1. `npx tsc --noEmit` clean.
2. SAVE (regresi): `"ngopi 5000"` → 1 row, `"1 transaksi tercatat."`, log `tool call: save_transaction`.
3. DELETE: `"hapus transaksi kopi terakhir"` → row hilang, `"1 transaksi dihapus."`, log `tool call: delete_transactions`.
4. UPDATE: `"ubah amount kopi terakhir jadi 30000"` → amount berubah, `"Transaksi diperbarui (field: amount)."`, log `tool call: update_transaction`.
5. Input multi (`"ngopi 25rb dan hapus parkir"`) → cuma 1 action ter-eksekusi (limitation yang akan di-fix di Prompt 3).

---

## Prompt 3 — Upgrade ke Parallel: Multi-Save + Mixed dalam Satu Kalimat

### Walkthrough Manual

Sekarang upgrade ke **parallel function calling**. Tiga perubahan:

1. **System prompt**: longgarkan "satu tool per request" → izinkan multi-call.
2. **Extract**: ganti `.find` (single) → `.filter` (semua tool_use blocks).
3. **Execute**: ganti single dispatch → `Promise.all` + composed message yang menyebut detail per jenis.

📂 **File yang dimodifikasi**:
- `src/features/quick-add.ts`
- `src/features/prompts.ts`

**1. Ganti `.find` jadi `.filter` + `Promise.all` dispatcher**

📍 Lokasi: di dalam `quickAddTransaction`, ganti blok dispatcher dari Prompt 2.

```ts
// src/features/quick-add.ts — pengganti dispatcher Prompt 2
const toolBlocks = resp.content.filter(
  (b): b is Anthropic.Messages.ToolUseBlock => b.type === "tool_use"
);

if (toolBlocks.length === 0) {
  return { ok: false, message: "Claude tidak memanggil tool. Coba teks lebih spesifik." };
}

console.log(
  `[quickAdd] ${toolBlocks.length} tool call(s) terdeteksi:`,
  toolBlocks.map((tb) => tb.name).join(", ")
);

const supabase = await createClient();

const results: ExecResult[] = await Promise.all(
  toolBlocks.map(async (tb) => {
    if (tb.name === "save_transaction") {
      const parsed = tb.input as ParsedTransaction;
      const { error } = await supabase.from("transactions").insert({
        amount: parsed.amount,
        type: parsed.type,
        category: parsed.category,
        date: parsed.date,
        description: parsed.description,
      });
      return error
        ? { ok: false, kind: "save" as const, error: error.message }
        : { ok: true, kind: "save" as const };
    } else if (tb.name === "delete_transactions") {
      return executeDelete(supabase, tb.input as { description_keyword: string; max_delete?: number });
    } else if (tb.name === "update_transaction") {
      return executeUpdate(supabase, tb.input as { description_keyword: string; new_amount?: number; new_category?: string; new_description?: string });
    } else {
      return { ok: false, kind: "unknown", error: `Unknown tool: ${tb.name}` };
    }
  })
);
```

**2. Compose message gabungan**

📍 Lokasi: setelah `Promise.all`. Hitung per jenis.

```ts
const saved = results.filter((r) => r.ok && r.kind === "save").length;
const deleted = results.filter((r) => r.ok && r.kind === "delete")
  .reduce((sum, r) => sum + ((r as Extract<ExecResult, { kind: "delete" }>).count ?? 0), 0);
const updated = results.filter((r) => r.ok && r.kind === "update").length;
const fails = results.filter((r) => !r.ok).length;

revalidatePath("/transactions");

const parts: string[] = [];
if (saved > 0) parts.push(`${saved} transaksi tercatat`);
if (deleted > 0) parts.push(`${deleted} transaksi dihapus`);
if (updated > 0) parts.push(`${updated} transaksi diperbarui`);
if (fails > 0) parts.push(`${fails} gagal`);

return {
  ok: fails === 0,
  message: parts.length > 0 ? parts.join(", ") + "." : "Tidak ada perubahan.",
};
```

**3. Update `QUICK_ADD_INSTRUCTION` — longgarkan "satu tool per request"**

📍 Lokasi: ganti section `SATU TOOL PER REQUEST` (dari Prompt 2) dengan `MULTI-ACTION & MIXED`.

```ts
// src/features/prompts.ts — replace section di QUICK_ADD_INSTRUCTION
MULTI-ACTION & MIXED:
User BOLEH menggabungkan beberapa actions dalam satu kalimat
(dipisahkan koma, "dan", "lalu", "+", dst.). Panggil tool yang
sesuai BEBERAPA KALI dalam satu response.

Contoh:
- "ngopi 25rb dan beli buku 80rb" → save_transaction × 2 paralel.
- "makan siang 35rb, bensin 50rb, parkir 5rb" → save_transaction × 3.
- "ngopi 25rb dan hapus parkir kemarin" →
  save_transaction({ ngopi 25k... }) + delete_transactions({ keyword: "parkir" }).
- "hapus kopi terakhir dan ubah amount makan jadi 50rb" →
  delete_transactions({ keyword: "kopi" }) + update_transaction({ keyword: "makan", new_amount: 50000 }).

JANGAN gabungkan multiple item jadi 1 amount summed. Setiap action
punya tool_use sendiri.
```

> 💡 **Parallel function calling aktif by default di Claude 4.x**. Anda tidak perlu setting khusus — Claude akan memutuskan sendiri kapan paralel masuk akal selama system prompt mengizinkan.

### Yang sebaiknya tidak dilakukan

- ❌ Loop sequential (`for...of await`) untuk eksekusi — kehilangan benefit paralel. Pakai `Promise.all`.
- ❌ Split `tool_result` ke multiple user messages — semua dari satu response Claude harus di SATU user message (kalau Anda nanti pakai pola loop tool_use).
- ❌ Membuang aturan keyword/hard-cap dari Prompt 1 — tool definitions tetap sama, hanya orchestration yang berubah.
- ❌ Lupa update message composition — kalau hanya copy logic Prompt 2, multi-action akan kelihatan seperti single action.

### Verifikasi setelah file diubah

1. `npx tsc --noEmit` clean.
2. Test 5 skenario:
   - **Single save** (regresi): `"ngopi 5000"` → 1 row, `"1 transaksi tercatat."`.
   - **Multi save**: `"ngopi 25rb dan beli buku 80rb"` → 2 row, `"2 transaksi tercatat."`. Log: `2 tool call(s) terdeteksi: save_transaction, save_transaction`.
   - **Single delete**: `"hapus transaksi kopi terakhir"` → row hilang, `"1 transaksi dihapus."`.
   - **Mixed save + delete**: `"ngopi 25rb dan hapus parkir kemarin"` → 1 row baru + 1 row parkir hilang, `"1 transaksi tercatat, 1 transaksi dihapus."`. Log: `2 tool call(s) terdeteksi: save_transaction, delete_transactions`.
   - **Mixed delete + update**: `"hapus kopi terakhir dan ubah amount makan jadi 50000"` → 1 hilang + 1 di-update, `"1 transaksi dihapus, 1 transaksi diperbarui."`.
3. Cek Supabase Table Editor untuk konfirmasi state akhir.

---

**Silakan salin prompt berikut, lalu paste ke Claude Code:**

```
Upgrade quickAddTransaction (dari Prompt 2) ke parallel function
calling: extract semua tool_use blocks via .filter, eksekusi
Promise.all, compose message yang sebut detail per jenis.

GOAL:
- Modifikasi src/features/quick-add.ts:
  1. Ganti const toolBlock = resp.content.find(...) ke
     const toolBlocks = resp.content.filter(
       (b): b is Anthropic.Messages.ToolUseBlock => b.type === "tool_use"
     ).

  2. Kalau toolBlocks.length === 0, return error. Selain itu:
     console.log(`[quickAdd] N tool call(s) terdeteksi: <names>`).

  3. Ganti if/else dispatcher single jadi Promise.all over toolBlocks.map.
     Inside map: dispatch by tb.name (save/delete/update/unknown),
     return ExecResult. Save handler tetap inline (insert), delete
     dan update pakai executeDelete/executeUpdate.

  4. Setelah Promise.all, hitung:
     - saved = results.filter(r => r.ok && r.kind === "save").length
     - deleted = sum of count dari results yang ok+delete
     - updated = results.filter(r => r.ok && r.kind === "update").length
     - fails = results.filter(r => !r.ok).length

  5. Compose message dengan parts: string[] — push "${saved} transaksi
     tercatat" / "${deleted} transaksi dihapus" / "${updated} transaksi
     diperbarui" / "${fails} gagal" hanya kalau > 0. Join dengan ", "
     + suffix ".".

  6. Return { ok: fails === 0, message }.

- Modifikasi src/features/prompts.ts (QUICK_ADD_INSTRUCTION):
  - Replace section "SATU TOOL PER REQUEST" (dari Prompt 2) dengan
    section "MULTI-ACTION & MIXED" yang menjelaskan user boleh gabung
    multiple actions. Sertakan 4 contoh:
    * multi save: "ngopi 25rb dan beli buku 80rb"
    * multi save besar: "makan 35rb, bensin 50rb, parkir 5rb"
    * mixed save+delete: "ngopi 25rb dan hapus parkir kemarin"
    * mixed delete+update: "hapus kopi terakhir dan ubah amount makan
      jadi 50rb"
  - Tegaskan JANGAN gabungkan multiple item jadi 1 amount summed.

CONTEXT:
- Backend dari Prompt 1 (handlers) + Prompt 2 (dispatcher single)
  sudah berjalan.
- ExecResult discriminated union sudah ada dari Prompt 1.

GUARDRAIL:
- JANGAN loop sequential (for...of await) — pakai Promise.all.
- JANGAN ubah tool definitions atau handlers dari Prompt 1.
- JANGAN biarkan aturan "satu tool per request" dari Prompt 2 — harus
  diganti dengan MULTI-ACTION & MIXED.
- JAGA backward compat: single action tetap jalan (toolBlocks.length === 1
  = special case dari N).
- Pesan harus informatif per jenis (tercatat / dihapus / diperbarui).
```

**Verifikasi singkat:**

1. `npx tsc --noEmit` clean.
2. Single save (regresi): `"ngopi 5000"` → 1 row, `"1 transaksi tercatat."`.
3. Multi save: `"ngopi 25rb dan beli buku 80rb"` → 2 row, `"2 transaksi tercatat."`.
4. Mixed save+delete: `"ngopi 25rb dan hapus parkir kemarin"` → 1 row baru + 1 hilang, `"1 transaksi tercatat, 1 transaksi dihapus."`.
5. Mixed delete+update: `"hapus kopi terakhir dan ubah amount makan jadi 50000"` → 1 hilang + 1 update, `"1 transaksi dihapus, 1 transaksi diperbarui."`.
6. Log: `[quickAdd] N tool call(s) terdeteksi: ...` muncul untuk multi-action.

---

## Validasi Akhir Module 08

Sebelum Anda menutup Module 08, mari pastikan progression 3-tahap bekerja end-to-end:

**Setelah Prompt 1 (definisi tools + handlers):**

- [ ] `DELETE_TRANSACTION_TOOL` dan `UPDATE_TRANSACTION_TOOL` tertdeklarasi di `src/features/quick-add.ts`.
- [ ] `executeDelete` punya hard cap server-side `Math.min(max_delete ?? 1, 5)`.
- [ ] `executeUpdate` build payload dari `new_*` field non-undefined + tolak kalau semua undefined.
- [ ] Keduanya pakai `ILIKE %keyword%` + `ORDER BY date DESC` untuk match.
- [ ] Type `ExecResult` discriminated union dengan 4 variant.
- [ ] Function `quickAddTransaction` BELUM tersentuh di Prompt 1.

**Setelah Prompt 2 (wire single tool per request):**

- [ ] `tools` di `messages.create` berisi 3 tool: save + delete + update.
- [ ] Pattern extract pakai `.find` (single tool) dengan type guard.
- [ ] Dispatcher if/else by `tb.name`.
- [ ] `QUICK_ADD_INSTRUCTION` punya section DELETE + UPDATE + SATU TOOL PER REQUEST.
- [ ] Test single save / delete / update masing-masing jalan dengan message UI yang sesuai.
- [ ] Log terminal `[quickAdd] tool call: <name>` muncul per request.

**Setelah Prompt 3 (upgrade ke parallel):**

- [ ] Pattern extract sudah `.filter` (semua tool_use blocks), bukan `.find`.
- [ ] Eksekusi pakai `Promise.all` untuk paralel.
- [ ] `QUICK_ADD_INSTRUCTION` section `SATU TOOL PER REQUEST` sudah diganti `MULTI-ACTION & MIXED` dengan 4 contoh.
- [ ] Message UI compose detail per jenis: tercatat + dihapus + diperbarui + gagal (hanya yang > 0).
- [ ] Test 5 skenario di Prompt 3 jalan (single save regresi + multi save + single delete + mixed save+delete + mixed delete+update).
- [ ] Log terminal `[quickAdd] N tool call(s) terdeteksi: <names>` muncul untuk multi-action.

**Umum:**

- [ ] `npx tsc --noEmit` clean di setiap prompt.
- [ ] Build production sukses (`npm run build`).
- [ ] Tidak ada regresi di chatbot RAG (Module 07) atau fitur lain.

## Refleksi Module 08

Refleksikan pertanyaan berikut secara mendalam sebelum melanjutkan ke module berikutnya:

1. Mengapa progression Prompt 1 → 2 → 3 dibuat bertahap (bukan langsung parallel)? Apa yang Anda dapat dari memisahkan "definisi tools" vs "wire single" vs "upgrade parallel"?
2. `tool_choice: "any"` memaksa Claude wajib panggil tool minimal 1×. Apa konsekuensi kalau user input nonsense (mis. _"halo apa kabar?"_) — apakah Claude tetap memaksa panggil tool dengan data ngawur? Bagaimana cara handle ini di production?
3. Insert + delete + update paralel via `Promise.all` mengasumsikan tiap action **independen**. Skenario apa di mana action saling tergantung (mis. "ubah kopi terakhir lalu hapus kopi tertua") — apakah pattern ini cocok, atau perlu sequential dengan kontrol urutan?
4. Delete by `ILIKE %keyword%` + Update by `ILIKE %keyword%` rentan **false positive** — user maksud "kopi pagi" tapi yang ter-modifikasi "ngopi sore". Bagaimana cara design UI konfirmasi yang minimal friction (mis. show preview match + tombol "Konfirmasi" / "Batal") sebelum execute?
5. Hard cap `max_delete = 5` adalah safety net. Apa skenario di mana user **benar-benar** butuh hapus > 5 sekaligus? Bagaimana cara desain "batch delete dengan konfirmasi eksplisit" tanpa kompromi pada safety default?
6. Tool `update_transaction` hanya update 1 row terbaru. Kalau user maksud "ubah semua kopi minggu ini jadi expense kategori food", desain tool yang berbeda diperlukan. Apa schema + safety guard yang Anda usulkan untuk bulk update?
7. Kalau Module 06 (embedding) aktif, save baru harus juga di-embed, delete harus hapus embedding row, update harus re-embed kalau description berubah. Bagaimana memastikan konsistensi pipeline embedding di tiga jenis action?
8. Sekarang quick-add **bisa save + delete + update**, sementara chatbot AI Advisor (Module 07) **bisa query data** (RAG) tapi tidak ada action. Bagaimana cara menggabungkan: chatbot bisa juga create/delete/update via natural language? Apa risiko **destructive action di conversation** dan cara mitigasinya?

---

🏠 Kembali: **[Day 4 — AI Agent & Tools](../README.md)** · ⬅️ Sebelumnya: **[Module 07 — RAG](../Module-07-RAG/latihan.md)** · ➡️ Lanjut: **[Module 09 — Multimodal](../Module-09-Multimodal/latihan.md)** (upload kwitansi → auto-extract → insert)
