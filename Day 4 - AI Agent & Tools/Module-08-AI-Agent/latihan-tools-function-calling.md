# Section 2 — Tools & Function Calling

> Bagian dari **[Module 08 — Latihan](./latihan.md)**. Lanjutan dari **[Section 1 — Konsep AI Agent](./latihan-konsep-ai-agent.md)**.

> Latihan implementasi konkret: tambahkan tool `create_transaction` ke AI Advisor di Fin-App. Setelah selesai, user dapat mencatat pengeluaran lewat percakapan natural seperti _"Catat kopi 25rb tadi siang"_ — Claude memutuskan parameter, aplikasi mengeksekusi insert ke Supabase, lalu Claude konfirmasi ke user.
>
> **Estimasi Section 2**: 90–120 menit.

## Prasyarat Section 2

- [ ] Section 1 selesai. Anda paham pola ReAct dan flow 4-langkah function calling.
- [ ] Module 04–07 selesai. AI Advisor di Fin-App sudah berfungsi (streaming + RAG opsional).
- [ ] Module 05 Section 4 (Agentic Workflow) sudah pernah dieksekusi — minimal Anda paham tool use dasar di Claude API.
- [ ] Tabel `transactions` di Supabase sudah ada (dari Module 01).
- [ ] `@anthropic-ai/sdk` terinstal dan `ANTHROPIC_API_KEY` aktif.
- [ ] Dev server jalan (`npm run dev`), Claude Code aktif di terminal terpisah.

> ⚠️ **Penting**: Section ini menambahkan **action destruktif terbatas** (insert ke DB). Pastikan Anda pakai branch git baru sebelum mulai supaya mudah rollback.

---

## Prompt 1 — Deklarasi Tool `create_transaction`

**Salin prompt berikut, paste ke Claude Code:**

```
Saya ingin menambahkan tool definition untuk create_transaction
yang akan dipakai Claude API agar dapat mencatat pengeluaran
user lewat percakapan natural.

GOAL:
- Buat file baru src/lib/tools.ts.
- Ekspor konstanta TOOLS: Anthropic.Messages.Tool[] berisi satu
  tool definition: create_transaction.
- Tool definition harus mengikuti format Claude API:
  {
    name: "create_transaction",
    description: "...",
    input_schema: { type: "object", properties: {...}, required: [...] }
  }
- Field input_schema:
  - type: string enum ["income", "expense"]
  - amount: number positif (dalam Rupiah)
  - category: string (mis. "food", "transport", "salary", "shopping")
  - description: string singkat tentang transaksi
  - date: string format ISO 8601 (opsional — default ke hari ini
    apabila tidak diberikan)
- Required: ["type", "amount", "category", "description"]
- Description tool harus JELAS dan SPESIFIK — itu yang
  dibaca Claude untuk memutuskan kapan memanggilnya. Sertakan:
  - Kapan tool ini cocok dipakai (mis. "ketika user
    menyebutkan pengeluaran atau pendapatan baru")
  - Format yang diharapkan untuk setiap field (mis. amount
    dalam Rupiah penuh, BUKAN ribuan — "25rb" → 25000)
  - Contoh kalimat trigger ("Catat kopi 25rb", "Tadi makan
    siang habis 50ribu", "Gajian masuk 5 juta")

CONTEXT:
- File: src/lib/tools.ts. Hanya berisi konstanta TOOLS,
  TIDAK ada handler eksekusi (itu di Prompt 2).
- Import type dari "@anthropic-ai/sdk": Anthropic.Messages.Tool.
- Kategori transaksi (food, transport, dll.) sesuai dengan
  yang sudah ada di tabel transactions Fin-App.

GUARDRAIL:
- JANGAN buat handler eksekusi di file ini.
- JANGAN tambah tool lain selain create_transaction.
- input_schema HARUS valid JSON Schema (gunakan type, properties,
  required dengan benar).
- Format Rupiah: number dalam satuan penuh (1.500.000 jadi
  number 1500000, bukan "1.5jt").
- Tambahkan JSDoc singkat di atas konstanta TOOLS yang
  menjelaskan: tujuan file, cara import & pakai.

Setelah selesai, tampilkan struktur file dan jelaskan singkat
mengapa setiap field di input_schema penting.
```

**Verifikasi:**

1. File `src/lib/tools.ts` tercipta.
2. Buka file: konstanta `TOOLS` ekspor, type-nya `Anthropic.Messages.Tool[]`.
3. Description tool berisi minimal: kapan dipakai + format field + contoh trigger.
4. `input_schema` valid: ada `type: "object"`, `properties`, dan array `required`.
5. Tidak ada handler eksekusi di file ini.

---

## Prompt 2 — Handler Eksekusi `executeCreateTransaction`

**Salin prompt berikut:**

```
Sekarang implementasi handler yang mengeksekusi tool
create_transaction — insert ke Supabase.

GOAL:
- Buat file baru src/features/tool-handlers.ts.
- Ekspor async function executeCreateTransaction(input):
  Promise<{ success: boolean; data?: any; error?: string }>.
- Input type didefinisikan berdasarkan tool schema dari
  src/lib/tools.ts (re-define inline atau import dari shared
  types).
- Function:
  1. Validasi input (amount > 0, type adalah "income" atau
     "expense", category non-kosong).
  2. Apabila date tidak diberikan, default ke new Date()
     dalam format ISO.
  3. Panggil Supabase server client (pakai pola yang sama
     dengan getBalanceSummary di src/features/action.ts).
  4. Insert ke tabel transactions.
  5. Return success: true + data hasil insert, atau success: false
     + error message.

- Tambahkan dispatcher executeToolByName(name: string, input: unknown)
  yang switch berdasarkan name dan panggil handler yang sesuai.
  Untuk sekarang hanya support "create_transaction". Throw error
  apabila name tidak dikenal.

CONTEXT:
- File: src/features/tool-handlers.ts. Tambahkan "use server"
  di baris pertama.
- Pola Supabase: pakai pola yang ada di src/features/action.ts
  (server-only, env key tanpa NEXT_PUBLIC_).
- Tabel transactions di Supabase punya kolom: id, user_id, type,
  amount, category, description, date, created_at. Untuk
  single-user app di Fin-App, user_id boleh hardcoded ke nilai
  yang sudah ada di tabel (atau ambil dari helper getCurrentUserId
  apabila sudah dibuat di module sebelumnya).

GUARDRAIL:
- JANGAN expose detail internal Supabase ke caller — hanya
  return success/data/error structure.
- Apabila insert gagal (mis. constraint violation), return
  success: false + error message yang INFORMATIF (Claude akan
  baca ini untuk recover).
- JANGAN buat handler untuk tool lain — hanya create_transaction.
- Validasi input sebelum panggil DB (hemat round-trip).
- Tambahkan JSDoc di atas masing-masing function: tujuan,
  parameter, return value.

Setelah selesai, jelaskan singkat alur eksekusi dan format
return value yang dipilih.
```

**Verifikasi:**

1. File `src/features/tool-handlers.ts` ada dengan `"use server"` di baris pertama.
2. `executeCreateTransaction` validasi input, default date, dan panggil Supabase.
3. Return value bentuk `{ success, data?, error? }` — konsisten.
4. `executeToolByName` dispatcher ada dan handle hanya `create_transaction`.
5. (Opsional) Test cepat dari `experiments/`:
   ```ts
   import { executeCreateTransaction } from "../src/features/tool-handlers";
   const result = await executeCreateTransaction({
     type: "expense",
     amount: 25000,
     category: "food",
     description: "Kopi Starbucks",
   });
   console.log(result);
   ```
   Run: `npx tsx --env-file=.env.local experiments/test-tool-handler.ts`. Setelah itu, cek di Supabase Table Editor — row baru harus muncul.

---

## Prompt 3 — Integrasi Tools ke Route Handler `/api/advisor`

**Salin prompt berikut:**

```
Sekarang sambungkan tool definitions + handler ke route handler
/api/advisor. Setelah ini, Claude akan dapat memanggil
create_transaction lewat chatbot.

GOAL:
- Modifikasi src/app/api/advisor/route.ts.
- Tambahkan parameter tools ke client.messages.stream() (atau
  client.messages.create kalau tidak streaming):
  tools: TOOLS  // import dari src/lib/tools.ts
- Setelah respons Claude diterima, cek apakah ada content block
  bertipe "tool_use". Apabila ada:
  1. Panggil executeToolByName(toolUse.name, toolUse.input).
  2. Append assistant message (yang berisi tool_use) ke
     messages array.
  3. Append user message dengan content block bertipe
     "tool_result" + tool_use_id + content (JSON.stringify hasil).
  4. Panggil ulang client.messages.stream/create dengan messages
     yang sudah ter-update — Claude akan generate respons text
     final berdasarkan hasil tool.
- Pasang max iterations = 5 untuk safety (mencegah infinite loop
  apabila Claude terus-terusan panggil tool).

- Update system prompt (di src/lib/prompts.ts dari Module 05
  Section 1) untuk memberi tahu Claude tentang kemampuan baru:
  tambahkan kalimat di section "Lingkup" atau "Format" yang
  bilang: "Anda dapat mencatat transaksi user lewat tool
  create_transaction. Pakai tool ini ketika user menyebutkan
  pengeluaran/pendapatan baru, BUKAN ketika hanya bertanya
  tentang transaksi yang sudah ada."

CONTEXT:
- File yang dimodifikasi: src/app/api/advisor/route.ts dan
  src/lib/prompts.ts.
- Untuk streaming dengan tools: pakai approach NON-streaming
  dulu (client.messages.create) untuk simplicity. Streaming
  dengan tools lebih kompleks dan tidak wajib untuk latihan
  ini.
- Apabila response.stop_reason === "tool_use", artinya Claude
  ingin panggil tool. Apabila "end_turn", artinya selesai.

GUARDRAIL:
- JANGAN ubah behaviour multi-turn dari Module 04 Section 6
  (riwayat messages tetap dikirim).
- JANGAN ubah behaviour RAG dari Module 07 (kalau retrieval
  aktif, pertahankan).
- Loop tool_use harus PUNYA BATAS (max 5 iterations).
- JANGAN expose error mentah dari handler ke user — wrap
  dalam tool_result content yang informatif untuk Claude
  recover.
- Apabila handler return success: false, tetap append sebagai
  tool_result (Claude akan inform user error-nya secara natural).
- JANGAN UBAH user_id assumption — pakai pola yang sudah ada.

Setelah selesai, jelaskan singkat alur multi-turn dengan tool
use dan kapan loop berakhir.
```

**Verifikasi:**

1. Buka `src/app/api/advisor/route.ts` — `tools: TOOLS` ada di params API call.
2. Ada logic loop yang handle `stop_reason === "tool_use"`.
3. `executeToolByName` dipanggil dengan name + input dari `tool_use` block.
4. Loop max 5 iterations (mis. `for (let i = 0; i < 5 && response.stop_reason === "tool_use"; i++) { ... }`).
5. System prompt di `prompts.ts` di-update dengan keterangan tentang `create_transaction`.

---

## Prompt 4 — Test End-to-End di Chatbot

**Salin prompt berikut, paste ke Claude Code untuk verifikasi via logging + testing manual:**

```
Bantu saya test end-to-end fitur function calling yang baru
ditambahkan. Tambahkan logging dan jalankan beberapa skenario.

GOAL:
- Tambahkan console.log di src/app/api/advisor/route.ts pada
  3 titik kunci:
  1. Saat Claude memutuskan panggil tool: log nama + input
     ("[TOOL_USE] create_transaction", input)
  2. Saat handler selesai eksekusi: log success/error +
     ringkasan data ("[TOOL_RESULT] success: true, id: 42")
  3. Saat loop selesai (response final): log iteration count
     ("[DONE] iterations: 1")
- Skenario test (jalankan via chatbot di browser):

  SKENARIO 1: Pengeluaran sederhana
  Input: "Catat kopi 25rb tadi siang"
  Expected: tool dipanggil dengan
    type=expense, amount=25000, category≈"food",
    description≈"kopi". Respons konfirmasi natural.

  SKENARIO 2: Pendapatan
  Input: "Gajian masuk 5 juta tadi"
  Expected: tool dipanggil dengan
    type=income, amount=5000000, category≈"salary".

  SKENARIO 3: Pertanyaan TANPA action
  Input: "Berapa total expense food bulan ini?"
  Expected: tool TIDAK dipanggil (ini query, bukan create).
    Respons text biasa (atau via RAG kalau aktif).

  SKENARIO 4: Ambiguous
  Input: "Sepertinya aku mau beli kopi nanti"
  Expected: tool TIDAK dipanggil (future plan, bukan
    transaksi aktual). Respons text yang clarify atau
    konfirmasi sebelum action.

- Untuk setiap skenario, dokumentasikan di
  docs/MODULE-08-TEST-LOG.md:
  - Input user
  - Tool calls (kalau ada): nama + input + hasil
  - Respons final Claude
  - Pass/Fail + catatan kalau ada yang tidak sesuai expected

CONTEXT:
- File yang dimodifikasi: src/app/api/advisor/route.ts
  (logging) dan dokumentasi baru di docs/.
- Test dilakukan MANUAL di browser, bukan automated test —
  kita masih di fase eksplorasi.

GUARDRAIL:
- Logging hanya di server (route handler), JANGAN log
  data sensitif user di browser.
- Setelah test selesai, console.log debug boleh
  dipertahankan dengan flag DEBUG env, atau dihapus
  bersih.
- Apabila ada skenario yang FAIL, JANGAN langsung perbaiki
  — dokumentasikan dulu, lalu ke prompt berikutnya untuk
  iterasi.
```

**Verifikasi:**

1. Di terminal `npm run dev`, log `[TOOL_USE]`, `[TOOL_RESULT]`, `[DONE]` muncul saat skenario dijalankan.
2. Skenario 1 & 2: transaksi baru tercatat di Supabase Table Editor (cek `transactions` table).
3. Skenario 3: tidak ada `[TOOL_USE]` muncul — Claude jawab text biasa.
4. Skenario 4: Claude tidak langsung action — minta klarifikasi atau warning.
5. File `docs/MODULE-08-TEST-LOG.md` ada dengan 4 skenario terdokumentasi.

---

## Validasi Akhir Section 2

Pastikan checklist berikut tercapai sebelum lanjut ke section/module berikutnya:

- [ ] `src/lib/tools.ts` ekspor `TOOLS: Anthropic.Messages.Tool[]` dengan satu tool `create_transaction`.
- [ ] `src/features/tool-handlers.ts` ekspor `executeCreateTransaction` dan dispatcher `executeToolByName`.
- [ ] Route handler `/api/advisor` pakai `tools: TOOLS` + loop tool_use dengan max 5 iterations.
- [ ] System prompt di `prompts.ts` mention tool `create_transaction`.
- [ ] Test manual via chatbot: "Catat kopi 25rb tadi siang" → row baru muncul di Supabase + Claude konfirmasi.
- [ ] Pertanyaan non-action ("Berapa total expense?") TIDAK trigger tool.
- [ ] File `docs/MODULE-08-TEST-LOG.md` berisi minimal 4 skenario test.
- [ ] Tidak ada regresi di RAG (Module 07) atau multi-turn (Module 04 Section 6).
- [ ] Build production sukses (`npm run build`).

## Refleksi Section 2

Tuliskan pada catatan pribadi:

1. **Berapa kali iterasi prompt** Anda perlukan untuk membuat Claude konsisten **tidak** memanggil tool saat user hanya bertanya (skenario 3 & 4)? Apa yang membantu?
2. **Apakah description tool** Anda mengalami iterasi? Apa yang Anda ubah dan apa dampaknya pada keputusan Claude?
3. Adakah skenario di mana Claude **salah parse amount** (mis. "25rb" jadi 25 alih-alih 25000)? Bagaimana Anda fix di description / schema?
4. **Risiko keamanan apa** yang Anda lihat dari tool yang punya side effect ke DB? Bagaimana Anda akan tambah guardrail di production (mis. konfirmasi user sebelum action, soft-delete, rate limit)?
5. Apabila Anda harus tambah tool **kedua** (mis. `get_balance_summary`, `delete_transaction`), apa yang akan berubah di arsitektur Anda? Apakah dispatcher saat ini cukup, atau butuh refactor?

---

⬅️ Kembali: **[Section 1 — Konsep AI Agent](./latihan-konsep-ai-agent.md)** · 🏠 Index: **[Module 08 — Latihan](./latihan.md)** · ➡️ Lanjut: **Section 3** (akan datang — ReAct loop runtime, multi-tool, memory)
