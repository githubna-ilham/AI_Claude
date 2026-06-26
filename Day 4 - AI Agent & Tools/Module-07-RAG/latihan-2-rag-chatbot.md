# Section 2 — Implementasi RAG di Chatbot AI Advisor

> Bagian dari **[Module 07 — Latihan](./latihan.md)**. Lanjutan dari **[Section 1 — Retrieval Helper](./latihan-1-retrieval.md)**.

> Di section ini kita memasang **pipeline RAG end-to-end** ke chatbot AI Advisor (`src/app/api/advisor/route.ts` dari Module 05). Dua perubahan utama: (1) menambahkan `ADVISOR_RAG_INSTRUCTION` + builder `buildAdvisorRAGSystem(context)` di `prompts.ts`, (2) memodifikasi route handler agar setiap pesan user memicu retrieval → build system prompt → stream Claude. Setelah selesai, chatbot di UI Fin-App menjawab pertanyaan user berdasarkan transaksi nyata mereka. Tiga prompt siap copy-paste.
>
> **Alur belajarnya**: siapkan prompt builder → wire ke route handler dengan logging → verifikasi end-to-end via 4 skenario percakapan di UI.
>
> **Estimasi waktu**: 70–90 menit.

## Prasyarat Section 2

- [ ] Section 1 selesai. `retrieveContextForChatbot` jalan dan output-nya seperti yang diharapkan.
- [ ] Module 05 Section 3 selesai. `ADVISOR_ROLE`, `ADVISOR_CONTEXT`, `ADVISOR_FORMAT`, `ADVISOR_INSTRUCTION` ada di `src/features/prompts.ts`. `ADVISOR_SYSTEM_V3` juga masih tersedia.
- [ ] Module 05 selesai. Route `/api/advisor` ada di `src/app/api/advisor/route.ts` dan chatbot UI sudah render daftar pesan + input.
- [ ] Tabel `transactions` punya minimal 5–10 transaksi nyata supaya retrieval terasa.
- [ ] Anda sudah membaca bagian Section 2 di `materi.md`.

---

## 📚 Referensi Dokumentasi

- **[Anthropic prompt engineering — RAG](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering)** — pola umum injection context dan anti-halusinasi guidance.
- **[Anthropic system prompts](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/system-prompts)** — pattern bagian-bagian system prompt.
- **[Anthropic streaming API](https://docs.claude.com/en/api/messages-streaming)** — pattern SSE yang sudah dipakai di Module 04/05.
- **[Next.js Route Handlers](https://nextjs.org/docs/app/building-your-application/routing/route-handlers)** — pattern POST handler di App Router.

---

## Prompt 1 — Tambah `ADVISOR_RAG_INSTRUCTION` + `buildAdvisorRAGSystem(context)` di `prompts.ts`

### Walkthrough Manual

Sebelum kita modifikasi route handler, sediakan dulu **system prompt yang RAG-aware** di `prompts.ts`. Karena konteks transaksi berbeda **setiap request** (query user berbeda), kita perlu **function builder** — bukan konstanta seperti `ADVISOR_SYSTEM_V3`.

📂 **File yang dimodifikasi**: `src/features/prompts.ts` (sudah ada dari Module 05).

**1. Tambah `ADVISOR_RAG_INSTRUCTION`**

📍 Lokasi: module-level, di bawah `ADVISOR_INSTRUCTION` yang sudah ada (Module 05 Section 3). Template dengan placeholder `{{CONTEXT}}` yang akan di-replace runtime.

```ts
// src/features/prompts.ts — tambahan
export const ADVISOR_RAG_INSTRUCTION = `
Anda menjawab pertanyaan user tentang keuangan personal mereka.

ATURAN PENGGUNAAN KONTEKS:
1. Bagian "KONTEKS TRANSAKSI" di bawah berisi transaksi user yang RELEVAN dengan pertanyaan.
2. JIKA konteks berisi data → jawab BERLANDASKAN data tersebut. Sebutkan angka, kategori,
   tanggal yang ada di konteks. JANGAN mengarang angka di luar yang tersedia.
3. JIKA konteks = "(tidak ada transaksi yang relevan ditemukan)" → katakan terus terang
   bahwa Anda tidak menemukan transaksi terkait di catatan user. Tawarkan saran umum
   tanpa mengarang angka spesifik.
4. JANGAN bertanya "berapa pengeluaran Anda?" — data sudah ada di konteks. Pakai itu.

KONTEKS TRANSAKSI:
{{CONTEXT}}
`.trim();
```

**2. Builder function `buildAdvisorRAGSystem(context)`**

📍 Lokasi: module-level, di bawah `ADVISOR_RAG_INSTRUCTION`. Reuse `ADVISOR_ROLE/CONTEXT/FORMAT` yang sudah ada — hanya `INSTRUCTION` yang berubah.

```ts
export function buildAdvisorRAGSystem(context: string): string {
  return `
# ROLE
${ADVISOR_ROLE}

# CONTEXT
${ADVISOR_CONTEXT}

# OUTPUT FORMAT
${ADVISOR_FORMAT}

# INSTRUCTION
${ADVISOR_RAG_INSTRUCTION.replace("{{CONTEXT}}", context)}
`.trim();
}
```

> 💡 **Kenapa `{{CONTEXT}}` pakai double-curly?** Konvensi template umum supaya jelas ini placeholder runtime, bukan template literal JavaScript. Anda boleh ganti dengan sintaks lain (mis. `<<CONTEXT>>`) selama konsisten.

### Yang sebaiknya tidak dilakukan

- ❌ Membuang `ADVISOR_SYSTEM_V3` lama — biarkan tetap ada. Section 3 (mode toggle) akan memakainya untuk mode General.
- ❌ Menulis ulang `ADVISOR_ROLE/CONTEXT/FORMAT` — reuse via interpolasi (pola RCI dari Module 05).
- ❌ Pakai template engine eksternal (mustache, handlebars) — `String.replace` sudah cukup untuk satu placeholder.
- ❌ Inject konteks di tengah-tengah `ROLE` atau `CONTEXT` — konteks selalu di blok `INSTRUCTION` supaya Claude tahu itu data, bukan identitas.

### Verifikasi setelah file diubah

1. `npx tsc --noEmit` clean — tidak ada type error.
2. Export `ADVISOR_RAG_INSTRUCTION`, `buildAdvisorRAGSystem` tersedia.
3. `ADVISOR_SYSTEM_V3` lama masih ada (tidak terhapus).

---

**Silakan salin prompt berikut, lalu paste ke Claude Code:**

```
Tambah ADVISOR_RAG_INSTRUCTION dan builder function
buildAdvisorRAGSystem(context) di src/features/prompts.ts.
Reuse ADVISOR_ROLE / ADVISOR_CONTEXT / ADVISOR_FORMAT yang
sudah ada dari Module 05 Section 3.

GOAL:
- Modifikasi src/features/prompts.ts (sudah ada).
- Tambahkan:

  1. export const ADVISOR_RAG_INSTRUCTION berisi:
     - Penjelasan singkat bahwa user nanya keuangan personal.
     - 4 aturan numbered:
       (a) Bagian KONTEKS TRANSAKSI berisi transaksi user
           relevan dengan pertanyaan.
       (b) Kalau konteks berisi data → jawab BERLANDASKAN
           data, sebutkan angka/kategori/tanggal, JANGAN
           mengarang angka di luar data.
       (c) Kalau konteks = "(tidak ada transaksi yang relevan
           ditemukan)" → katakan terus terang tidak ada
           transaksi terkait, tawarkan saran umum tanpa
           mengarang angka.
       (d) JANGAN bertanya "berapa pengeluaran Anda?" —
           data sudah ada di konteks.
     - Heading "KONTEKS TRANSAKSI:" diikuti placeholder
       {{CONTEXT}} di baris terakhir.

  2. export function buildAdvisorRAGSystem(context: string): string
     yang return template literal dengan:
     # ROLE
     ${ADVISOR_ROLE}

     # CONTEXT
     ${ADVISOR_CONTEXT}

     # OUTPUT FORMAT
     ${ADVISOR_FORMAT}

     # INSTRUCTION
     ${ADVISOR_RAG_INSTRUCTION.replace("{{CONTEXT}}", context)}

CONTEXT:
- ADVISOR_ROLE / ADVISOR_CONTEXT / ADVISOR_FORMAT /
  ADVISOR_INSTRUCTION sudah ada di file ini dari Module 05
  Section 3 (pola RCI).
- ADVISOR_SYSTEM_V3 lama TETAP DIPERTAHANKAN (jangan dihapus).

GUARDRAIL:
- JANGAN buang konstanta lama (ADVISOR_SYSTEM_V3, INSIGHT_SYSTEM
  dari Module 05/06, dst).
- JANGAN rewrite ADVISOR_ROLE/CONTEXT/FORMAT — reuse via
  interpolasi template literal.
- JANGAN pakai template engine eksternal — String.replace
  cukup untuk satu placeholder.
- Pakai trim() di akhir template supaya tidak ada newline
  ekstra di atas/bawah.
```

**Verifikasi singkat:**

1. `npx tsc --noEmit` clean.
2. Export baru: `ADVISOR_RAG_INSTRUCTION`, `buildAdvisorRAGSystem`.
3. `ADVISOR_SYSTEM_V3` masih ada.

---

## Prompt 2 — Wire RAG ke Route `/api/advisor` (Retrieval + Augmented Prompt + Logging)

### Walkthrough Manual

Sekarang inti integrasi: route handler `/api/advisor` (Module 05) di-modifikasi agar setiap pesan user memicu retrieval lalu memakai builder dari Prompt 1. Perubahan kerja inti ada **tiga langkah** sebelum `client.messages.stream(...)`:

1. Ambil pesan user terakhir dari `messages` array.
2. Panggil `retrieveContextForChatbot(lastUserMessage)`.
3. Build system prompt baru via `buildAdvisorRAGSystem(context)`.

Streaming SSE dan struktur response tetap sama dengan Module 04/05.

📂 **File yang dimodifikasi**: `src/app/api/advisor/route.ts` (sudah ada dari Module 05).

**1. Import helper baru**

📍 Lokasi: bagian imports atas.

```ts
// src/app/api/advisor/route.ts — imports
import { retrieveContextForChatbot } from "@/features/rag-context";
import { buildAdvisorRAGSystem } from "@/features/prompts";
```

**2. Ekstrak pesan user terakhir**

📍 Lokasi: setelah `const { messages } = await req.json();` di dalam handler.

```ts
const lastUserMessage = [...messages]
  .reverse()
  .find((m) => m.role === "user")?.content as string | undefined;
```

> 💡 **Mengapa pesan terakhir, bukan semua user message?** Konteks RAG fokus pada **pertanyaan saat ini**, bukan seluruh riwayat. Jika user bertanya "kopi minggu lalu", kemudian melanjutkan "kalau tagihan?", retrieval kedua harus berdasarkan "tagihan" saja — bukan kombinasi keduanya yang malah menambah noise.

**3. Retrieve konteks + bungkus dengan timing**

📍 Lokasi: setelah ekstrak pesan user. Tambahkan timing sederhana untuk observability.

```ts
const t0 = Date.now();
const context = lastUserMessage
  ? await retrieveContextForChatbot(lastUserMessage, { threshold: 0.05, limit: 5 })
  : "(belum ada pertanyaan)";
const tRetrieve = Date.now() - t0;
```

> ⚠️ **Threshold sangat rendah (0.05) — itu disengaja, bukan typo.**
>
> Empiris di Fin-App: description transaksi pendek ("Pizza", "Ngopi", "Makan di warteg"), sedangkan user mengirim **kalimat tanya natural language** seperti `"ada pengeluaran kopi kemarin?"` atau `"pengeluaran apa saja bulan ini?"`. Kalimat panjang dengan kata-kata filler ("ada", "pengeluaran", "kemarin", "?") menggeser embedding query menjauh dari embedding deskripsi pendek — similarity turun ke ~0.10–0.20 walaupun semantik nyambung.
>
> | Threshold | Hasil empiris |
> |---|---|
> | `0.5` | 0 hasil untuk hampir semua query natural language |
> | `0.3` | hanya match query 1-kata seperti "kopi" |
> | `0.15` | match sebagian (top-1 saja) |
> | `0.05` | semua transaksi relevan masuk konteks ✅ |
>
> **Trade-off:** dengan 0.05, query off-topic ("siapa presiden Indonesia?") juga akan menarik beberapa row sebagai noise. Mitigasi: aturan #3 di `ADVISOR_RAG_INSTRUCTION` (Prompt 1) menginstruksikan Claude untuk **menolak menggunakan konteks yang jelas tidak relevan** — Claude cukup pintar untuk ignore noise selama prompt-nya tegas. Solusi proper (parse intent → SQL filter untuk pertanyaan agregat) ada di Section 3 / Module 08.

**4. Build system prompt baru**

📍 Lokasi: tepat setelah retrieval.

```ts
const system = buildAdvisorRAGSystem(context);
```

**5. Logging ringan untuk debugging**

📍 Lokasi: sebelum stream call. Cukup `console.log` — bisa dipantau di terminal dev server atau Vercel logs.

```ts
console.log("[advisor/RAG]", {
  query: lastUserMessage?.slice(0, 80),
  retrieveMs: tRetrieve,
  contextChars: context.length,
  hasContext: !context.startsWith("(tidak ada"),
});
```

**6. Pakai system baru di stream call**

📍 Lokasi: parameter `system` di `client.messages.stream(...)`. Ganti dari konstanta lama (`ADVISOR_SYSTEM_V3` atau `ADVISOR_SYSTEM`) menjadi variable `system`.

```ts
const stream = client.messages.stream({
  model: "claude-haiku-4-5",
  max_tokens: 1024,
  system,                  // ← variable baru, bukan konstanta
  messages,
});
```

### Yang sebaiknya tidak dilakukan

- ❌ Menulis ulang seluruh route handler — perubahan **maksimal 12–15 baris** (import + ekstrak + retrieve + build + log + ganti parameter `system`).
- ❌ Memodifikasi SSE response handler — biarkan streaming pattern dari Module 04/05.
- ❌ Embedding semua pesan history — fokus retrieval hanya pada pesan user terakhir.
- ❌ Menambah caching di sini — `embed()` di Module 06 sudah punya strategi caching dasar. Retrieval cepat (~100ms), tidak butuh lapisan tambahan dulu.
- ❌ Membuat route `/api/advisor-rag` baru — modifikasi yang sudah ada agar chatbot existing langsung menjadi RAG-aware.
- ❌ Logging full system prompt — boros dan berisiko PII. Cukup metrics + 80 karakter pertama query.

### Verifikasi setelah file diubah

1. `npx tsc --noEmit` clean.
2. Jalankan dev server (`npm run dev`).
3. Buka chatbot di UI Fin-App.
4. Kirim pesan: `"ada pengeluaran kopi minggu lalu?"`.
5. Cek terminal dev server — pastikan tidak ada error dan log `[advisor/RAG]` muncul dengan field `query`, `retrieveMs`, `contextChars`, `hasContext: true`.
6. Streaming response muncul di UI seperti biasa.
7. (Pemeriksaan kualitas jawaban lanjut ke Prompt 3.)

---

**Silakan salin prompt berikut, lalu paste ke Claude Code:**

```
Modifikasi route handler chatbot AI Advisor
(src/app/api/advisor/route.ts dari Module 05) supaya setiap
user message memicu retrieval + augmentation sebelum stream
ke Claude. Sertakan logging ringan untuk debugging.

GOAL:
- Modifikasi src/app/api/advisor/route.ts (sudah ada).
- Perubahan minimal (~12–15 baris):

  1. Import:
     import { retrieveContextForChatbot } from "@/features/rag-context";
     import { buildAdvisorRAGSystem } from "@/features/prompts";

  2. SETELAH dapat messages dari req.json(), SEBELUM
     client.messages.stream(...):
     - Ekstrak pesan user terakhir:
       const lastUserMessage = [...messages].reverse()
         .find((m) => m.role === "user")?.content as string | undefined;
     - Retrieve dengan timing (threshold 0.05 — sangat
       longgar; lihat catatan walkthrough kenapa serendah ini
       untuk Fin-App):
       const t0 = Date.now();
       const context = lastUserMessage
         ? await retrieveContextForChatbot(lastUserMessage, { threshold: 0.05, limit: 5 })
         : "(belum ada pertanyaan)";
       const tRetrieve = Date.now() - t0;
     - Build system:
       const system = buildAdvisorRAGSystem(context);
     - Log:
       console.log("[advisor/RAG]", {
         query: lastUserMessage?.slice(0, 80),
         retrieveMs: tRetrieve,
         contextChars: context.length,
         hasContext: !context.startsWith("(tidak ada"),
       });

  3. Ganti parameter `system` di client.messages.stream(...) dari
     konstanta lama (ADVISOR_SYSTEM_V3 / ADVISOR_SYSTEM) menjadi
     variable `system` yang baru.

CONTEXT:
- retrieveContextForChatbot sudah ada di @/features/rag-context
  (Section 1) return Promise<string>.
- buildAdvisorRAGSystem sudah ada di @/features/prompts
  (Prompt 1 section ini) return string siap pakai sebagai
  parameter system Claude.
- Route handler existing pakai pola streaming SSE dari Module 04/05.
- Format pesan: { role: "user" | "assistant", content: string }.

GUARDRAIL:
- JANGAN rewrite seluruh route — perubahan minimal saja.
- JANGAN ubah pattern streaming SSE.
- JANGAN bikin route /api/advisor-rag baru — modifikasi yang
  sudah ada.
- JANGAN retrieve untuk semua pesan history — hanya pesan
  user terakhir.
- JANGAN tambah caching tambahan — embed() di Module 06 sudah
  cukup.
- JANGAN log full system prompt — boros + PII risk. Cukup
  metrics + 80 char pertama query.
- ADVISOR_SYSTEM_V3 lama tetap diekspor (di prompts.ts) —
  jangan dihapus, akan dipakai di Section 3 (mode toggle).
```

**Verifikasi singkat:**

1. `npx tsc --noEmit` clean.
2. Dev server jalan tanpa error.
3. Buka chatbot UI, kirim pesan apapun → streaming response muncul.
4. Terminal dev server menampilkan log `[advisor/RAG]` dengan 4 field per request.
5. `retrieveMs` di bawah 1000 untuk pertanyaan biasa.

---

## Prompt 3 — Verifikasi End-to-End via 4 Skenario Percakapan

### Walkthrough Manual

Fondasi sudah dipasang. Sekarang uji secara manual via UI Fin-App dengan 4 skenario yang merepresentasikan jenis pertanyaan berbeda — tujuannya memastikan RAG bekerja dengan benar dan Claude tidak berhalusinasi.

📂 **Tidak ada file yang dimodifikasi** — semua eksekusi manual di browser.

**1. Pastikan data sudah ada**

📍 Lokasi: Supabase SQL Editor.

```sql
SELECT count(*) AS total,
       count(*) FILTER (WHERE embedding IS NOT NULL) AS with_embedding
FROM transactions;
```

Yang diharapkan: `with_embedding >= 5` minimum supaya retrieval terasa.

**2. Empat skenario percakapan**

📍 Lokasi: chatbot UI Fin-App di browser.

| # | User input | Yang diharapkan dari Claude |
|---|---|---|
| 1 | `"ada pengeluaran kopi minggu lalu?"` | Menyebut transaksi kopi spesifik dari data Anda + angka & tanggal. |
| 2 | `"transport paling sering ke mana?"` | Menyebut bensin/ojek/grab dari transaksi Anda. |
| 3 | `"info pesawat ke Jepang"` | Akui tidak menemukan transaksi terkait, tawarkan saran umum tanpa angka spesifik. |
| 4 | `"apa itu inflasi?"` | Jawab dari training Claude (umum). Konteks akan kosong → Claude tetap bisa menjawab pertanyaan general. |

**3. Hal yang harus diperhatikan**

- ✅ **Angka di jawaban Claude muncul di konteks**. Buka network tab → lihat request body → cek log `[advisor/RAG]` di terminal → angka yang Claude sebut harus berasal dari konteks transaksi yang di-retrieve.
- ✅ **Untuk skenario 3, Claude tidak mengarang transaksi**. Marker `(tidak ada transaksi yang relevan ditemukan)` di konteks → Claude harus mengakui keterbatasan.
- ✅ **Streaming tetap mulus** — UX tidak terganggu oleh latency tambahan retrieval.
- ❌ **Red flag**: Claude menyebut angka yang tidak ada di konteks → ada halusinasi. Periksa apakah `ADVISOR_RAG_INSTRUCTION` aturan #2 cukup tegas.

**4. (Opsional) Periksa log per request di terminal**

📍 Lokasi: terminal dev server.

Untuk setiap pesan yang dikirim, Anda akan melihat log seperti:

```
[advisor/RAG] {
  query: 'ada pengeluaran kopi minggu lalu?',
  retrieveMs: 234,
  contextChars: 412,
  hasContext: true
}
```

`retrieveMs` biasanya 100–500ms (Voyage embed + Postgres HNSW). Jika lebih dari 2 detik → ada masalah di pipeline retrieval.

### Yang sebaiknya tidak dilakukan

- ❌ Membuat script test otomatis — verifikasi manual via UI sudah cukup untuk skala latihan ini.
- ❌ Mengasumsikan data Anda persis seperti contoh — sesuaikan skenario dengan data nyata Anda.
- ❌ Melewatkan skenario "off-topic" (skenario 3) — itu test paling penting untuk memastikan anti-halusinasi bekerja.

### Verifikasi setelah semua skenario diuji

1. Skenario 1 & 2 → Claude menyebut data nyata Anda dengan akurat.
2. Skenario 3 → Claude akui tidak ada data, tanpa mengarang angka.
3. Skenario 4 → Claude jawab pertanyaan general (dari training) tanpa terganggu konteks kosong.
4. Streaming UI tetap mulus di semua skenario.
5. Log `[advisor/RAG]` muncul per request dengan field lengkap.

---

**Silakan salin prompt berikut, lalu paste ke Claude Code:**

```
Bantu saya menjalankan smoke test end-to-end RAG di chatbot
AI Advisor. Saya akan menjalankan 4 skenario percakapan
manual di UI; bantu saya menafsirkan hasilnya dan diagnose
kalau ada yang tidak sesuai harapan.

GOAL:
- Beri saya checklist 4 skenario percakapan untuk dicoba
  di chatbot UI Fin-App:

  1. "ada pengeluaran kopi minggu lalu?" — harus sebut
     transaksi kopi spesifik dari data.
  2. "transport paling sering ke mana?" — harus sebut
     bensin/ojek/grab dari data.
  3. "info pesawat ke Jepang" — Claude harus akui tidak
     ada transaksi, JANGAN mengarang angka.
  4. "apa itu inflasi?" — Claude jawab umum dari training,
     konteks tetap dikirim tapi kosong/marker.

- Beri saya checklist apa saja yang harus diperhatikan
  per skenario:
  - Apakah angka di jawaban Claude muncul di konteks?
  - Apakah marker NO_CONTEXT_MARKER muncul di skenario 3?
  - Apakah streaming UI tetap mulus?

- Beri saya panduan diagnose kalau:
  (a) Claude tetap mengarang di skenario 3.
  (b) Skenario 1 & 2 hasilnya tidak ada di konteks (similarity
      semua di bawah threshold — biasanya bukan bug, melainkan
      perlu turunkan threshold lagi; lihat tabel empiris di
      walkthrough Prompt 2).
  (c) Error 500 di route handler.
  (d) retrieveMs di log melebihi 2000ms.

CONTEXT:
- Saya akan menjalankan manual di browser, bukan via Claude
  Code Bash tool.
- Tabel transactions sudah berisi data nyata (≥ 5 transaksi
  dengan embedding).
- Route /api/advisor sudah dimodifikasi di Prompt 2 dengan
  logging [advisor/RAG] di terminal.

GUARDRAIL:
- JANGAN bikin script automation — manual via UI cukup.
- JANGAN modifikasi prompts.ts / rag-context.ts / route
  handler — di prompt ini hanya verifikasi.
- Beri jawaban sebagai dokumen test plan markdown, bukan kode.
```

**Verifikasi singkat:**

1. Anda menerima dari Claude: checklist 4 skenario + diagnostic guide.
2. Anda menjalankan 4 skenario manual di UI.
3. Skenario 1 & 2: jawaban Claude sesuai data nyata.
4. Skenario 3: Claude akui tidak ada data tanpa mengarang.
5. Skenario 4: Claude jawab dari training (umum), tidak crash karena konteks kosong.

---

## Validasi Akhir Section 2

Sebelum Anda lanjut ke Section 3, mari pastikan pipeline RAG end-to-end bekerja kokoh:

- [ ] `src/features/prompts.ts` memiliki `ADVISOR_RAG_INSTRUCTION` (4 aturan + placeholder `{{CONTEXT}}`) dan `buildAdvisorRAGSystem(context: string): string`.
- [ ] `ADVISOR_SYSTEM_V3` lama (dan konstanta lain dari Module 05/06) tidak terhapus.
- [ ] Route `src/app/api/advisor/route.ts` memanggil `retrieveContextForChatbot` dan `buildAdvisorRAGSystem` per request.
- [ ] Parameter `system` di `client.messages.stream(...)` sekarang variable, bukan konstanta lama.
- [ ] Logging `[advisor/RAG]` muncul di terminal dev server per request dengan field `query`, `retrieveMs`, `contextChars`, `hasContext`.
- [ ] `npx tsc --noEmit` clean.
- [ ] Chatbot UI Fin-App tetap responsif — streaming jalan tanpa hambatan.
- [ ] Skenario 1 & 2 (kopi, transport): Claude menyebut transaksi nyata dengan angka & tanggal yang akurat.
- [ ] Skenario 3 (off-topic): Claude akui tidak ada data, tanpa mengarang angka.
- [ ] Skenario 4 (pertanyaan umum): Claude jawab dari training, tidak crash karena konteks kosong.

## Refleksi Section 2

Refleksikan pertanyaan berikut secara mendalam sebelum melanjutkan ke section berikutnya:

1. Sekarang Claude menjawab dengan data grounded. Tetapi pertanyaan agregat seperti _"berapa total belanja bulan ini?"_ kemungkinan kurang akurat — mengapa? Solusi yang lebih tepat untuk kasus tersebut?
2. Anda hanya retrieve pesan user **terakhir**. Apa konsekuensinya untuk percakapan multi-turn — misalnya user: "kopi minggu lalu?" → Claude jawab → user: "kalau yang Rp 25rb saja?" — apakah retrieval kedua dapat menemukan transaksi spesifik yang dimaksud?
3. Di Fin-App, kita pakai threshold sangat rendah (`0.05`) karena natural-language query Indonesia menggeser embedding terlalu jauh dari deskripsi pendek. Bagaimana cara menentukan threshold optimal secara empiris (mis. eval set 20 query × expected match)? Apakah threshold harus berbeda per skenario (kata-kunci pendek vs kalimat panjang)?
4. Aturan #2 di `ADVISOR_RAG_INSTRUCTION` melarang Claude "mengarang angka di luar konteks". Apa risikonya kalau aturan ini tidak ada? Coba bayangkan jawaban Claude untuk pertanyaan tentang transaksi yang tidak ada di konteks.
5. Bagaimana cara menangani **rate limit Voyage** kalau chatbot ramai dipakai? (mis. queue, in-memory cache untuk query yang sering, fallback ke non-RAG mode kalau gagal embed)
6. Logging saat ini hanya `console.log`. Untuk production-grade observability, pipeline seperti apa yang Anda bayangkan? (mis. log structured ke tabel → dashboard Metabase untuk latency, hit rate, marker rate)
7. Module 08 (function calling) akan mengatasi keterbatasan #1 (agregasi numerik). Bagaimana Anda akan menggabungkan RAG (untuk pertanyaan deskriptif tentang transaksi spesifik) + function calling (untuk pertanyaan agregat) di satu chatbot? Mana yang diputuskan duluan — Claude sendiri (agentic) atau router logic di app?

---

⬅️ Kembali: **[Section 1 — Retrieval Helper](./latihan-1-retrieval.md)** · 🏠 Index: **[Module 07 — Latihan](./latihan.md)** · ➡️ Lanjut: **[Section 3 — Mode Toggle: Personal vs General](./latihan-3-mode-toggle.md)**
