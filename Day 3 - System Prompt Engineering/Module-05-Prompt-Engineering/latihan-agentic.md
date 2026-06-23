# Section 4 — Agentic Workflow

> Bagian dari **[Module 05 — Latihan](./latihan.md)**. Lanjutan dari **[Section 3 — Role, Context, & Instruction](./latihan-rci.md)**.

> Latihan untuk memberi AI Advisor kemampuan **memanggil tool** — membaca data transaksi user dari Supabase saat dibutuhkan. Empat prompt siap copy-paste.
>
> **Estimasi**: 60–75 menit (paling teknis di Module 05).

## Prasyarat Section 4

- [ ] Section 1–3 selesai.
- [ ] Module 02 (Transactions CRUD) selesai — data transaksi ada di Supabase.

---

## Prompt 1 — Definisikan Tools untuk Claude

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

⬅️ Kembali: **[Section 3](./latihan-rci.md)** · 🏠 Index: **[Module 05 — Latihan](./latihan.md)**
