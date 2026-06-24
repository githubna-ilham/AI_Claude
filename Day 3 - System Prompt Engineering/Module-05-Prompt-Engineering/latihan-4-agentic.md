# Section 4 — Agentic Workflow

> Bagian dari **[Module 05 — Latihan](./latihan.md)**. Lanjutan dari **[Section 3 — Role, Context, & Instruction](./latihan-3-rci.md)**.

> Latihan untuk memberi AI Advisor kemampuan **memanggil tool** — membaca data transaksi user dari Supabase saat dibutuhkan. Empat prompt siap copy-paste.
>
> **Estimasi**: 60–75 menit (paling teknis di Module 05).

## Prasyarat Section 4

- [ ] Section 1–3 selesai.
- [ ] Module 02 (Transactions CRUD) selesai — data transaksi ada di Supabase.

---

## 📚 Referensi Dokumentasi

Sebelum mulai, akan sangat membantu kalau Anda buka tab dokumentasi resmi untuk referensi cepat saat ada kebingungan:

- **[Tool use overview](https://docs.claude.com/en/docs/build-with-claude/tool-use)** — konsep tool use, kapan pakai, dan flow request/response.
- **[Tool use parameter format](https://docs.claude.com/en/api/messages)** — struktur `tools` array, `input_schema` (JSON Schema), `tool_use` & `tool_result` blocks.
- **[Tool use examples](https://docs.claude.com/en/docs/build-with-claude/tool-use/overview)** — pola request/response lengkap dengan multi-iteration.
- **[Agentic patterns](https://docs.claude.com/en/docs/build-with-claude/tool-use)** — multi-step reasoning dengan loop tool call.

---

## Prompt 1 — Definisikan Tools untuk Claude

### Walkthrough Manual (sebelum pakai prompt)

Sebelum copy-paste prompt, pahami **anatomi tool definition** di Anthropic SDK. Setiap tool punya 3 bagian wajib: `name`, `description`, `input_schema` (JSON Schema).

📂 **File baru**: `src/features/tools.ts` (definisi + akan diisi eksekutor di Prompt 2)

**1. Import type dari SDK**

📍 Lokasi: **paling atas file**.

```ts
// src/features/tools.ts — bagian import
import type Anthropic from "@anthropic-ai/sdk";
```

**2. Konstanta `TOOLS_DEFINITION`**

📍 Lokasi: **module level**, exported. Type: `Anthropic.Messages.Tool[]`.

```ts
// src/features/tools.ts — module level
export const TOOLS_DEFINITION: Anthropic.Messages.Tool[] = [
  {
    name: "get_transactions",
    description:
      "Ambil daftar transaksi user dengan filter opsional. " +
      "Gunakan saat user bertanya tentang transaksi spesifik atau analisis pola pengeluaran.",
    input_schema: {
      type: "object",
      properties: {
        category: { type: "string", description: "Filter by category name, e.g. 'Food', 'Transport'" },
        start_date: { type: "string", description: "YYYY-MM-DD" },
        end_date: { type: "string", description: "YYYY-MM-DD" },
        type: { type: "string", enum: ["income", "expense"] },
        limit: { type: "number", description: "Default 50, max 200" },
      },
    },
  },
  {
    name: "get_balance_summary",
    description:
      "Ambil ringkasan saldo, total income, dan total expense user (all-time). " +
      "Gunakan saat user bertanya tentang kondisi keuangan secara umum.",
    input_schema: { type: "object", properties: {} },
  },
];
```

**3. Type union untuk type safety**

📍 Lokasi: **module level**, di bawah `TOOLS_DEFINITION`.

```ts
// src/features/tools.ts — module level
export type ToolName = "get_transactions" | "get_balance_summary";
```

> 💡 **Description = signal terkuat untuk Claude**. Description yang prescriptive ("Gunakan saat user bertanya tentang...") jauh lebih efektif daripada description deskriptif ("Function untuk ambil data").

### Yang TIDAK perlu

- ❌ Tool yang **mengubah data** (create/update/delete) — Section 4 hanya read-only. Tool write butuh confirmation layer yang lebih kompleks.
- ❌ Description deskriptif tanpa cue kapan pakai — Claude bingung memilih.
- ❌ `input_schema` longgar tanpa `properties` jelas — Claude akan tebak format dan sering salah.
- ❌ Implementasi eksekutor di file yang sama dulu — Prompt 2 menambah eksekutor.

### Verifikasi setelah file dibuat

1. File `src/features/tools.ts` ada dengan ekspor `TOOLS_DEFINITION`.
2. `npx tsc --noEmit` — tidak ada error type.
3. Inspect: `TOOLS_DEFINITION.length === 2`, nama persis `get_transactions` dan `get_balance_summary`.
4. Tiap tool punya `description` yang mengandung kata "Gunakan saat..." (prescriptive cue).

---

**Salin prompt berikut:**

```
Saya ingin mendefinisikan tools yang dapat dipanggil Claude
untuk membaca data transaksi user.

GOAL:
- Buat file baru src/features/tools.ts.
- Ekspor konstanta TOOLS_DEFINITION: array berisi 2 tool:

  1. get_transactions
     - description: "Ambil daftar transaksi user dengan
       filter opsional. Gunakan saat user bertanya tentang
       transaksi spesifik atau analisis pola pengeluaran."
     - input_schema dengan properties:
       - category: string (optional, "Filter by category
         name, e.g. 'Food', 'Transport'")
       - start_date: string (optional, "YYYY-MM-DD")
       - end_date: string (optional, "YYYY-MM-DD")
       - type: enum["income", "expense"] (optional)
       - limit: number (optional, default 50)

  2. get_balance_summary
     - description: "Ambil ringkasan saldo, total income,
       dan total expense user (all-time). Gunakan saat
       user bertanya tentang kondisi keuangan secara umum."
     - input_schema: object kosong (tidak ada parameter).

- Ekspor TOOL_NAMES sebagai const enum/union untuk type
  safety: "get_transactions" | "get_balance_summary".

CONTEXT:
- Struktur tool definition mengikuti Anthropic SDK:
  { name, description, input_schema (JSON Schema) }.
- File: src/features/tools.ts.

GUARDRAIL:
- Description harus PRESCRIPTIVE — beri tahu Claude KAPAN
  pakai tool.
- Property descriptions juga harus jelas.
- JANGAN tambahkan tool yang bisa MENGUBAH data (create,
  update, delete) — Section 4 hanya read-only.
```

**Verifikasi:**

1. File `tools.ts` ada dengan ekspor `TOOLS_DEFINITION`.
2. TypeScript tidak error.

---

## Prompt 2 — Implementasi Eksekutor Tool

### Walkthrough Manual (sebelum pakai prompt)

Sebelum copy-paste prompt, pahami pola eksekutor: **switch by name → validate input → query Supabase → return JSON string**. Claude expect string output, bukan object.

📂 **File yang diubah**: `src/features/tools.ts` (tambah function di file yang sama dari Prompt 1)

**1. Tambah directive `"use server"` di baris pertama**

📍 Lokasi: **baris 1**. Karena sekarang file ini punya function yang query Supabase.

```ts
// src/features/tools.ts — baris pertama (TAMBAH/PASTIKAN ADA)
"use server";
```

> ⚠️ `"use server"` di file yang juga mengekspor konstanta + type **boleh**. Type ter-erase saat build, konstanta diserialisasi.

**2. Import Zod, Supabase client, dan helper Module 02**

📍 Lokasi: **bagian import**.

```ts
// src/features/tools.ts — bagian import (tambahan)
import { z } from "zod";
import { createClient } from "@/lib/supabase/server";
import { getBalanceSummary } from "@/features/action";
```

**3. Zod schema untuk validasi input tiap tool**

📍 Lokasi: **module level**, sebelum function `executeTool`.

```ts
// src/features/tools.ts — module level
const GetTransactionsInput = z.object({
  category: z.string().optional(),
  start_date: z.string().optional(),
  end_date: z.string().optional(),
  type: z.enum(["income", "expense"]).optional(),
  limit: z.number().min(1).max(200).default(50),
});
```

**4. Function `executeTool(name, input)`**

📍 Lokasi: **module level**, exported async function. Switch berdasarkan `name`. **JANGAN throw** saat Supabase error — return JSON dengan field `error` supaya Claude bisa respons gracefully.

```ts
// src/features/tools.ts — module level
export async function executeTool(name: string, input: any): Promise<string> {
  switch (name) {
    case "get_transactions": {
      const args = GetTransactionsInput.parse(input);
      const supabase = await createClient();
      let q = supabase.from("transactions").select("*").limit(args.limit);
      if (args.category) q = q.eq("category", args.category);
      if (args.type) q = q.eq("type", args.type);
      if (args.start_date) q = q.gte("date", args.start_date);
      if (args.end_date) q = q.lte("date", args.end_date);
      const { data, error } = await q;
      if (error) return JSON.stringify({ error: "Tidak dapat ambil data transaksi" });
      return JSON.stringify(data);
    }
    case "get_balance_summary": {
      try {
        const summary = await getBalanceSummary();
        return JSON.stringify(summary);
      } catch {
        return JSON.stringify({ error: "Tidak dapat ambil ringkasan saldo" });
      }
    }
    default:
      throw new Error(`Unknown tool: ${name}`);
  }
}
```

### Yang TIDAK perlu

- ❌ **Throw saat Supabase error** — Claude butuh string response untuk reasoning. Throw akan crash route handler.
- ❌ **Limit > 200** — cegah Claude minta ribuan baris yang boros token.
- ❌ **Return object** dari `executeTool` — Anthropic SDK expect string di `tool_result.content`. `JSON.stringify` selalu.
- ❌ **Logger** — biarkan output stdout cukup untuk debugging.

### Verifikasi setelah file diubah

1. Cek `"use server"` di baris 1.
2. Buat `experiments/test-tool.ts`:
   ```ts
   import { executeTool } from "../src/features/tools";
   async function main() {
     console.log(await executeTool("get_transactions", { category: "Food", limit: 5 }));
     console.log(await executeTool("get_balance_summary", {}));
   }
   main().catch(console.error);
   ```
3. Jalankan: `npx tsx --env-file=.env.local experiments/test-tool.ts`.
4. Output keduanya adalah **JSON string** yang dapat di-`JSON.parse(...)`.
5. Test error case: `executeTool("unknown_tool", {})` → throw error "Unknown tool".

---

**Salin prompt berikut:**

```
Sekarang buat function yang mengeksekusi tool ketika Claude
memutuskan memanggilnya.

GOAL:
- Di src/features/tools.ts, tambah function:
  executeTool(name: string, input: any): Promise<string>

- Logic switch berdasarkan name:
  case "get_transactions":
    - Validasi input dengan Zod (category, start_date,
      end_date, type, limit semua optional).
    - Query Supabase: select * from transactions dengan
      filter yang sesuai.
    - Format hasil sebagai JSON string (Claude expects
      string, bukan object).
    - Return JSON string.
  
  case "get_balance_summary":
    - Reuse getBalanceSummary dari Module 02.
    - Format hasil sebagai JSON string.
    - Return JSON string.
  
  default:
    - Throw error "Unknown tool: ${name}"

CONTEXT:
- Import createClient dari "@/lib/supabase/server".
- Import getBalanceSummary dari "@/features/action".
- Pakai zod untuk validasi input.

GUARDRAIL:
- Apabila Supabase error, return JSON string dengan field
  error: { error: "Tidak dapat ambil data transaksi" }.
  JANGAN throw — biarkan Claude tahu tool gagal dan dia
  bisa merespons gracefully.
- Limit default 50, max 200 (cegah Claude minta semua data
  yang bisa boros token).
- File ini "use server".
```

**Verifikasi:**

1. Test cepat dari `experiments/test-tool.ts`:
   ```ts
   const r1 = await executeTool("get_transactions", { category: "Food", limit: 5 });
   console.log(r1);
   const r2 = await executeTool("get_balance_summary", {});
   console.log(r2);
   ```
2. Output adalah JSON string yang dapat di-parse.

---

## Prompt 3 — Integrasikan Tool Use ke Route Handler

### Walkthrough Manual (sebelum pakai prompt)

Sebelum copy-paste prompt, pahami **flow tool use loop** di Anthropic SDK: call Claude → cek `stop_reason === "tool_use"` → eksekusi tool → append `tool_result` → call Claude ulang → ulang sampai `stop_reason === "end_turn"` atau max iterasi.

📂 **File yang diubah**: `src/app/api/advisor/route.ts` (modifikasi handler `POST`)

**1. Import `TOOLS_DEFINITION` + `executeTool`**

📍 Lokasi: **paling atas file**, bagian import.

```ts
// src/app/api/advisor/route.ts — bagian import
import { TOOLS_DEFINITION, executeTool } from "@/features/tools";
```

**2. Pakai `client.messages.create()` untuk fase tool loop (bukan streaming)**

📍 Lokasi: **di dalam POST handler**. Streaming **tidak cocok** untuk fase tool calling karena perlu inspect content blocks lengkap. Streaming hanya dipakai di iterasi **terakhir** (saat Claude menjawab user).

```ts
// src/app/api/advisor/route.ts — di dalam POST handler
let workingMessages = [...history, { role: "user", content: lastMessage }];
let finalResponse: Anthropic.Messages.Message | null = null;

for (let iter = 0; iter < 5; iter++) {
  const resp = await client.messages.create({
    model: selectedModel,
    max_tokens: 1024,
    system: ADVISOR_SYSTEM,
    tools: TOOLS_DEFINITION,           /* ← BARU */
    messages: workingMessages,
  });

  if (resp.stop_reason !== "tool_use") {
    finalResponse = resp;
    break;
  }

  // Eksekusi semua tool_use blocks di iterasi ini
  const toolResults = [];
  for (const block of resp.content) {
    if (block.type === "tool_use") {
      const result = await executeTool(block.name, block.input);
      toolResults.push({
        type: "tool_result" as const,
        tool_use_id: block.id,
        content: result,
      });
    }
  }

  // Append assistant response + user tool_results
  workingMessages.push({ role: "assistant", content: resp.content });
  workingMessages.push({ role: "user", content: toolResults });
}

if (!finalResponse) {
  return new Response("Maaf, terlalu banyak step. Coba pertanyaan yang lebih spesifik.");
}
```

**3. Stream text content dari `finalResponse` ke client**

📍 Lokasi: **setelah loop**. Ambil text block dari `finalResponse.content` dan kirim sebagai stream response (atau plain text — sesuaikan dengan implementasi Module 04).

**4. Pertahankan thinking + RCI**

📍 Lokasi: **dalam parameter `client.messages.create`**. Parameter `thinking: { type: "adaptive" }` (Opus 4.7) atau `output_config: { effort: "..." }` boleh ditambah seperti Module 04 Section 5.

### Yang TIDAK perlu

- ❌ **Streaming saat fase tool loop** — perlu content blocks lengkap untuk parse `tool_use`. Stream hanya di iterasi final.
- ❌ **Crash route** saat `executeTool` throw — `executeTool` sudah return JSON `{error}` untuk Supabase error. Kalau throw lain, wrap try/catch dan inject error message ke `tool_result`.
- ❌ **Iterasi unlimited** — wajib hard cap 5 untuk safety (Claude bisa loop forever kalau tool description ambigu).
- ❌ **Modifikasi behavior tanpa tool_use** — pertahankan streaming Module 04 Section 6 saat `stop_reason !== "tool_use"` di iterasi pertama.

### Verifikasi setelah file diubah

1. Reload browser.
2. Kirim: "Berapa total expense food saya?".
3. Di terminal `npm run dev`, log menunjukkan Claude memanggil `get_transactions` dengan `{ category: "Food" }`.
4. Respons di chatbot menampilkan **angka aktual** dari Supabase (bukan placeholder).
5. Kirim pertanyaan **tanpa tool**: "Halo, siapa kamu?" → respons cepat, tidak ada log tool call.
6. Stress test: kirim "analisis lengkap keuangan saya semua waktu" — kalau loop > 5 iterasi, muncul pesan "Maaf, terlalu banyak step...".

---

**Salin prompt berikut:**

```
Sekarang sambungkan tool use ke route handler chatbot agar
Claude bisa memanggil tool saat dibutuhkan.

GOAL:
- Modifikasi src/app/api/advisor/route.ts.
- Tambahkan parameter tools: TOOLS_DEFINITION ke
  client.messages.stream() / create().
- Implementasi loop tool use:
  1. Panggil Claude.
  2. Iterasi response content blocks:
     - Apabila ada block type "tool_use", eksekusi tool
       via executeTool(name, input).
     - Push hasil ke array tool_results.
  3. Apabila ada tool_use, recurse: panggil ulang Claude
     dengan messages baru:
     ```
     messages = [
       ...originalMessages,
       { role: "assistant", content: response.content },
       { role: "user", content: tool_results }
     ]
     ```
  4. Loop maksimum 5 iterasi (safety).
  5. Apabila tidak ada tool_use, stream text content ke
     client seperti biasa.

- Pertahankan: streaming, thinking, system prompt RCI.

CONTEXT:
- Pakai client.messages.create() untuk loop tool use
  (lebih sederhana dari streaming saat tool calls).
- HANYA stream text content ke client di iterasi terakhir.

GUARDRAIL:
- Apabila iterasi mencapai 5, hentikan dan kirim pesan
  "Maaf, terlalu banyak step. Coba pertanyaan yang lebih
  spesifik."
- Apabila executeTool throw, lanjut dengan error message
  ke Claude — JANGAN crash.
- JANGAN ubah behaviour saat tidak ada tool_use (pertahankan
  streaming Module 04 Section 6).
```

**Verifikasi:**

1. Reload browser.
2. Kirim: "Berapa total expense food saya?"
3. Di console server (terminal `npm run dev`), seharusnya terlihat log Claude memanggil `get_transactions` dengan category="Food".
4. Respons di chatbot menampilkan **angka aktual** dari Supabase.

---

## Prompt 4 — Indikator UI Saat Tool Dipanggil

### Walkthrough Manual (sebelum pakai prompt)

Sebelum copy-paste prompt, pahami pola: route handler kirim **marker khusus** di stream (mis. `[[TOOL_CALL:get_transactions]]`), UI parse marker dan tampilkan indikator visual.

📂 **File yang diubah**:
- `src/app/api/advisor/route.ts` — tambah emit marker saat `tool_use`.
- `src/components/chat/ai-chat-panel.tsx` — parse marker, render indikator.

**1. Di route.ts: emit marker sebelum eksekusi tool**

📍 Lokasi: **di dalam POST handler**, **di dalam loop tool use** (Prompt 3), **sebelum dan sesudah `executeTool(...)`**. Marker dikirim via stream channel yang sama.

```ts
// src/app/api/advisor/route.ts — dalam loop tool use
for (const block of resp.content) {
  if (block.type === "tool_use") {
    controller.enqueue(encoder.encode(`[[TOOL_CALL:${block.name}]]`));
    const result = await executeTool(block.name, block.input);
    controller.enqueue(encoder.encode(`[[TOOL_DONE]]`));
    toolResults.push({ /* ... */ });
  }
}
```

> 💡 Marker `[[TOOL_CALL:name]]` dan `[[TOOL_DONE]]` adalah **convention internal** kita, BUKAN format SDK Anthropic. Bisa string apapun asal konsisten di kedua sisi.

**2. Di `ai-chat-panel.tsx`: state `toolStatus`**

📍 Lokasi: **di dalam function component**, bersama state lain (`isWaiting`, `messages`, dst.).

```tsx
// src/components/chat/ai-chat-panel.tsx — di dalam function AIChatPanel()
const [toolStatus, setToolStatus] = useState<{
  name: string;
  status: "pending" | "done";
} | null>(null);
```

**3. Parse marker saat streaming chunk diterima**

📍 Lokasi: **di handler stream reader** (sudah ada sejak Module 04 Section 6 untuk thinking_delta). Tambah cek marker.

```tsx
// src/components/chat/ai-chat-panel.tsx — di stream reader loop
const TOOL_CALL_RE = /\[\[TOOL_CALL:(\w+)\]\]/;
const TOOL_DONE = "[[TOOL_DONE]]";

if (chunk.includes(TOOL_DONE)) {
  setToolStatus(null);                 // fade out
} else {
  const m = chunk.match(TOOL_CALL_RE);
  if (m) {
    setToolStatus({ name: m[1], status: "pending" });
  } else {
    // chunk biasa — append ke message buffer seperti Module 04
  }
}
```

**4. Render indikator di JSX body**

📍 Lokasi: **di JSX return**, **body messages area**, **setelah `messages.map(...)`** dan **setelah indikator `isWaiting`**. Hanya tampil saat `toolStatus !== null`.

```tsx
// src/components/chat/ai-chat-panel.tsx — JSX body
{toolStatus && (
  <div className="flex items-center gap-2 rounded bg-muted px-3 py-2 text-sm italic text-muted-foreground">
    <Loader2 className="h-3 w-3 animate-spin" />
    {toolStatus.name === "get_transactions" && "🔍 Membaca data transaksi Anda..."}
    {toolStatus.name === "get_balance_summary" && "💰 Menghitung ringkasan saldo..."}
  </div>
)}
```

### Yang TIDAK perlu

- ❌ **Push tool indicator ke `messages` state** — pakai state terpisah supaya tidak polute riwayat chat.
- ❌ **Marker yang mungkin nabrak konten asli** (mis. pakai single bracket `[name]`) — pilih marker yang **tidak mungkin** muncul di teks chat (double bracket `[[...]]`).
- ❌ **Bubble user/assistant biasa untuk indicator** — visual harus berbeda (italic, bg-muted, text-sm).
- ❌ **Animasi/transisi rumit** — fade-out sederhana sudah cukup; fokus pada clarity, bukan polish.

### Verifikasi setelah file diubah

1. Reload browser.
2. Kirim: "Bagaimana keuangan saya?" → indikator "💰 Menghitung ringkasan saldo..." muncul, hilang setelah tool selesai.
3. Kirim: "Berapa expense food bulan ini?" → indikator "🔍 Membaca data transaksi Anda..." muncul.
4. Kirim: "Halo, siapa kamu?" → **tidak ada** indikator (tidak ada tool call).
5. `isWaiting` (loading utama) tetap aktif sepanjang flow — indikator tool adalah **tambahan**, bukan pengganti.

---

**Salin prompt berikut:**

```
Tambahkan UX feedback saat Claude memanggil tool, agar user
paham kenapa respons lebih lama.

GOAL:
- Modifikasi route.ts: kirim event khusus ke client saat
  tool_use terjadi. Pakai prefix marker:
  [[TOOL_CALL:get_transactions]]
  
  Setelah tool selesai, kirim:
  [[TOOL_DONE]]

- Modifikasi ai-chat-panel.tsx: parse marker dan tampilkan
  indikator di UI:
  - Saat tool_use detected, tampilkan bubble system kecil:
    "🔍 Membaca data transaksi Anda..."
  - Saat tool_done, ganti dengan ikon ✓ dan teks fade out.
- Bubble tool indicator: berbeda visual dari user/assistant
  (bg-muted, text-sm, italic).

CONTEXT:
- Pertahankan parsing thinking_delta dari Module 04 Section 6.

GUARDRAIL:
- Tool indicator hanya tampil saat ada tool call — tidak
  ganggu percakapan normal.
- Apabila ada multiple tool calls dalam satu turn, tampilkan
  semua indicator.
- JANGAN ubah message state untuk indicator — pakai state
  terpisah toolStatus: { name: string; status: "pending" |
  "done" } | null.
```

**Verifikasi:**

1. Kirim pertanyaan yang trigger tool: "Bagaimana keuangan saya?"
2. Indikator muncul: "🔍 Membaca data transaksi Anda...".
3. Setelah selesai, indikator hilang dan jawaban muncul.
4. Pertanyaan tanpa tool ("Halo, siapa kamu?") tidak menampilkan indikator.

---

## Validasi Akhir Section 4 (Akhir Module 05)

- [ ] File `tools.ts` dengan `TOOLS_DEFINITION` dan `executeTool`.
- [ ] Route handler memanggil tool dengan loop maks 5 iterasi.
- [ ] Indikator UI muncul saat tool dipanggil.
- [ ] Pertanyaan "Berapa total expense food saya?" dijawab dengan angka aktual.
- [ ] Pertanyaan tanpa tool tetap respons cepat tanpa indicator.
- [ ] Tidak ada regresi: thinking, streaming, multi-turn semua bekerja.

## Refleksi Section 4

1. Bagaimana akurasi Claude memilih tool yang tepat?
2. Pernah Claude memanggil tool yang tidak perlu? (Mis. pakai `get_transactions` untuk pertanyaan persona)
3. Apa pengalaman UX dari tool indicator?
4. Apabila menambah tool create/update/delete, apa safeguard yang Anda butuhkan?

---

## 🎉 Validasi Akhir Module 05

Setelah seluruh 4 section selesai, AI Financial Advisor Anda sudah:

- [ ] **System instruction** yang terstruktur dengan pola RCI.
- [ ] **Parameter generation** terkontrol (temperature, top_p, stop_sequences).
- [ ] **Komposisi modular** prompt yang reusable.
- [ ] **Tool use** untuk akses data transaksi nyata.
- [ ] **Parser transaksi** dari teks natural di halaman Transactions.
- [ ] **Fitur Insight Mingguan** sebagai server action siap dipanggil.
- [ ] **Tidak ada regresi** pada Dashboard / Transactions / Chatbot dari Module 04.

Apabila seluruh checklist tercapai, AI Financial Advisor Anda sudah jauh dari sekadar chatbot — ia adalah **asisten cerdas** yang memahami data Anda, merespons dengan format konsisten, dan dapat di-extend untuk fitur baru dengan mudah.

---

⬅️ Kembali: **[Section 3](./latihan-3-rci.md)** · 🏠 Index: **[Module 05 — Latihan](./latihan.md)**
