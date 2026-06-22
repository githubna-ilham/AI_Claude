# Module 05 — Prompt Engineering

> **Tujuan modul**: Anda menguasai teknik **prompt engineering** untuk Claude API — dari mengatur persona AI lewat system instruction, mengontrol output, hingga merancang agentic workflow yang dapat memanggil tool.
>
> **Output akhir modul**: AI Financial Advisor yang Anda bangun di Module 04 menjadi **lebih cerdas, lebih konsisten, dan lebih kuat** — dapat memahami konteks, menjalankan task multi-langkah, dan menjawab dengan format yang dapat diandalkan.

---

## Outline Section

Module 05 terdiri dari **6 section** yang membangun di atas Module 04. Setiap section menambah satu kemampuan prompt engineering pada AI Financial Advisor:

| # | Section | Fokus | Status |
|---|---|---|---|
| **1** | **System Instruction** | Pakai parameter `system` untuk menetapkan persona, batasan, dan format output | ✅ Siap |
| **2** | **Sample Parameter & Output Control** | Praktik mendalam: `temperature`, `top_p`, `top_k`, `stop_sequences`, structured output + parser transaksi | ✅ Siap |
| **3** | **Prompt Guides** | Anatomi prompt yang baik: 7 prinsip, anti-pattern, iterative refinement | ✅ Siap |
| **4** | **Zero-shot & Few-shot Prompting** | Perbedaan & kapan pakai; tambah few-shot examples ke parser & advisor | ✅ Siap |
| **5** | **Role, Context, & Instruction** | Pattern RCI: komposisi modular, reuse untuk fitur Insight Mingguan | ✅ Siap |
| **6** | **Agentic Workflow** | Tool use — Claude memanggil `get_transactions` & `get_balance_summary` dari Supabase | ✅ Siap |

**Total estimasi durasi**: ±5–6 jam efektif (di luar break & diskusi).

> 💡 **Cara kerja modul ini**: sama dengan Module 04 — setiap section memberi prompt-prompt siap copy-paste untuk dieksekusi ke Claude Code, yang akan memodifikasi fitur AI Financial Advisor di Fin-App secara inkremental.

## Prinsip Kontinuitas Antar Section

Sama dengan Module 04, kode dari section sebelumnya **terus berlanjut**:

```
Module 04 (selesai) → AI Advisor pakai prompt prefixing
   │
Section 1 → Migrasi dari prompt prefixing ke parameter `system`
   │
Section 2 → Eksplorasi parameter control + structured output
   │
Section 3 → Refactor system prompt jadi terstruktur sesuai best practice
   │
Section 4 → Tambah few-shot examples di system prompt
   │
Section 5 → Restrukturisasi prompt dengan pola Role-Context-Instruction
   │
Section 6 → Aktifkan tool use (Claude dapat baca transaksi user dari Supabase)
```

Pada akhir Module 05, AI Financial Advisor Anda tidak hanya menjawab pertanyaan — ia **memahami konteks pengguna** (dengan akses ke data transaksi via tool) dan menjawab dengan **format yang konsisten** untuk integrasi UI yang lebih kaya.

---

# Section 1 — System Instruction

**Tujuan section**: bermigrasi dari **prompt prefixing** (Module 04 Section 3) ke **parameter `system`** yang lebih kuat dan efisien.

## Mengapa Migrasi?

Pada Module 04, Anda menempatkan instruksi format di **user message** lewat `INSTRUCTION_PREFIX`. Pola ini bekerja, tetapi punya keterbatasan:

| Aspek | Prompt Prefixing (Module 04) | System Instruction (Module 05) |
|---|---|---|
| **Lokasi** | Di dalam `messages[].content` | Parameter terpisah `system: "..."` |
| **Visibility ke user** | Bisa terlihat (kalau user inspect payload) | Tidak terlihat — terkesan native |
| **Token usage** | Dikirim **ulang** di setiap turn percakapan | Dikirim **sekali** sebagai konteks tetap |
| **Robustness** | Rentan terhadap "ignore previous instructions" | Lebih kuat — Claude dilatih untuk hormati system |
| **Format API** | Hack — tidak sesuai semantik API | Sesuai semantik resmi Anthropic |

Untuk percakapan multi-turn (yang sudah Anda bangun di Module 04 Section 7), system instruction **jauh lebih hemat** — bayangkan 20 turn × 50 token prefix = 1000 token boros di prompt prefixing yang seharusnya cukup satu kali.

## Anatomi System Instruction yang Baik

System instruction yang berkualitas memiliki struktur jelas. Ini contoh kerangka:

```ts
const ADVISOR_SYSTEM = `
Anda adalah AI Financial Advisor untuk aplikasi Fin-App.

## Persona
- Ramah, jelas, dan to-the-point.
- Profesional tetapi tidak kaku.

## Lingkup
- Topik keuangan personal: tabungan, pengeluaran, anggaran,
  investasi dasar, perencanaan finansial.
- Apabila pertanyaan di luar lingkup, sopan kembalikan ke
  topik.

## Format Output
- Bahasa: selalu Bahasa Indonesia.
- Markdown rapi: list bertanda untuk poin, bold untuk angka
  penting.
- Format Rupiah: "Rp 1.500.000" (titik pemisah ribuan).
- Persentase: "15%" (tanpa spasi sebelum %).

## Batasan
- Jangan memberi nasihat hukum atau perpajakan spesifik —
  sarankan konsultasi profesional.
- Jangan menjanjikan return investasi tertentu.
`;
```

Karakter penting:

1. **Identitas jelas** di awal — Claude tahu "siapa" dia.
2. **Sections terpisah** dengan heading — mudah di-iterate dan di-debug.
3. **Konkret, bukan abstrak** — "Format Rupiah: Rp 1.500.000" lebih baik dari "format Rupiah yang baik".
4. **Batasan ditulis sebagai DO NOT** — Claude lebih responsif terhadap larangan eksplisit.

## Cara Memanggil di SDK

```ts
client.messages.create({
  model: "claude-haiku-4-5",
  max_tokens: 1024,
  temperature: 0.5,
  system: ADVISOR_SYSTEM,                  // ← parameter system
  messages: [
    { role: "user", content: userMessage }  // ← bersih, tanpa prefix
  ],
});
```

Bandingkan dengan Module 04:

```ts
// Sebelum (Module 04):
messages: [{ role: "user", content: INSTRUCTION_PREFIX + userMessage }]

// Sekarang (Module 05):
system: ADVISOR_SYSTEM,
messages: [{ role: "user", content: userMessage }]
```

User message kembali "murni" sesuai input asli — lebih bersih untuk logging, debugging, dan analytics.

Lanjutkan ke `latihan.md` Section 1 untuk eksekusi.

---

# Section 2 — Sample Parameter & Output Control

**Tujuan section**: praktik mendalam **parameter sampling** Claude API (`temperature`, `top_p`, `top_k`, `stop_sequences`) dan teknik **structured output** untuk mendapatkan respons yang dapat diandalkan oleh kode.

## Parameter Sampling — Recap & Lanjutan

Pada Module 04 Anda sudah mengenal `temperature`. Anthropic API juga menyediakan dua parameter sampling lain:

### `top_p` (Nucleus Sampling)

`top_p` membatasi pilihan kata berikutnya ke **subset paling probable** yang **kumulatif** mencapai probabilitas `p`.

| Nilai | Karakter |
|---|---|
| `1.0` (default) | Pertimbangkan semua kata kandidat |
| `0.9` | Hanya pertimbangkan kata-kata paling probable yang kumulatifnya 90% |
| `0.5` | Pilihan jauh lebih terbatas — sangat fokus |

`top_p` sering dipakai **sebagai alternatif** `temperature`, bukan bersamaan. Anthropic menyarankan: pilih salah satu, jangan kedua-duanya.

### `top_k`

`top_k` membatasi pilihan kata berikutnya ke **K kata paling probable**.

| Nilai | Karakter |
|---|---|
| Tidak diset (default) | Tidak ada batas |
| `40` | Hanya pertimbangkan 40 kata teratas |
| `10` | Sangat fokus, kemungkinan repetitif |

Dipakai untuk **kontrol eksperimen** — jarang dibutuhkan di production.

### Kombinasi yang Praktis

| Skenario | Setting yang umum |
|---|---|
| Chatbot keuangan (faktual, sedikit kreatif) | `temperature: 0.5` |
| Ekstraksi data dari teks (deterministik) | `temperature: 0.0` |
| Brainstorm ide / nama kreatif | `temperature: 0.9` |
| Code generation | `temperature: 0.0` atau `0.2` |
| Output JSON terstruktur | `temperature: 0.0` |

## Structured Output — Mendapatkan JSON yang Konsisten

Untuk fitur Fin-App yang membutuhkan **output terstruktur** (mis. parse "Saya habis Rp 50.000 untuk makan siang" menjadi `{ amount: 50000, category: "Food", description: "makan siang" }`), Anda memerlukan teknik khusus.

### Teknik 1: Instruksi Eksplisit

```ts
system: `Ekstrak data transaksi dari pesan user.
Output WAJIB berupa JSON valid dengan format:
{
  "type": "income" | "expense",
  "amount": number,
  "category": string,
  "description": string
}
Tidak ada teks lain di luar JSON.`
```

Tambah `temperature: 0.0` untuk deterministik.

### Teknik 2: Stop Sequence

Tambahkan stop sequence yang mencegah Claude menulis penjelasan setelah JSON:

```ts
stop_sequences: ["```", "\n\nPenjelasan"]
```

### Teknik 3: Wrap dalam Markdown Code Block

Minta Claude memulai output dengan ` ```json ` — ini sering lebih reliable karena Claude terlatih mengenali pola tersebut. Lalu parse dengan regex sederhana.

## Validasi Output di Sisi Kode

Selalu **validasi** output JSON sebelum dipakai:

```ts
import { z } from "zod";

const TransactionSchema = z.object({
  type: z.enum(["income", "expense"]),
  amount: z.number().positive(),
  category: z.string(),
  description: z.string(),
});

const raw = JSON.parse(claudeResponse);
const parsed = TransactionSchema.safeParse(raw);
if (!parsed.success) {
  // Claude bisa "halusinasi" struktur — handle gracefully
  throw new Error("Output Claude tidak valid");
}
```

Lanjutkan ke `latihan.md` Section 2 untuk eksekusi.

---

# Section 3 — Prompt Guides

**Tujuan section**: memahami **anatomi prompt yang baik** dan **anti-pattern** yang merusak kualitas output — lalu refactor system prompt AI Advisor dari Section 1 sesuai best practice.

## Anatomi Prompt yang Baik

Prompt produktif memiliki **3 elemen** yang harus jelas:

```
┌─────────────────────────────────────────────────────┐
│ 1. KONTEKS  → "Siapa kamu, untuk apa, di mana"      │
│ 2. TUGAS    → "Apa yang harus dilakukan saat ini"   │
│ 3. FORMAT   → "Bagaimana output harus terlihat"     │
└─────────────────────────────────────────────────────┘
```

### Contoh: Buruk vs Baik

❌ **Prompt buruk** (semua tercampur, ambigu):

```
Bantu user dengan keuangan dan jawab dengan baik
```

✅ **Prompt baik** (3 elemen jelas terpisah):

```
KONTEKS:
Anda adalah AI Financial Advisor untuk aplikasi Fin-App,
sebuah personal finance tracker di Indonesia.

TUGAS:
Jawab pertanyaan user tentang keuangan personal —
pengeluaran, tabungan, perencanaan finansial dasar.

FORMAT:
- Bahasa Indonesia, ramah, to-the-point.
- Markdown rapi, format Rupiah "Rp 1.500.000".
- Apabila pertanyaan di luar topik keuangan, sopan
  kembalikan ke topik.
```

## 7 Prinsip Prompt yang Solid

1. **Spesifik, bukan abstrak**.
   - ❌ "tulis dengan baik"
   - ✅ "tulis dengan 2-3 paragraf, formal tetapi ramah, max 200 kata"

2. **Eksplisit, bukan implisit**.
   - ❌ Berharap Claude "tahu" konvensi project Anda.
   - ✅ Tulis konvensi tersebut langsung di prompt.

3. **Berikan contoh**.
   - Satu contoh konkret = ratusan kata penjelasan abstrak.

4. **Larangan eksplisit**.
   - "JANGAN sebut harga saham spesifik" lebih kuat dari "hindari hal sensitif".

5. **Strukturkan dengan heading / list**.
   - Markdown structure di prompt → Claude lebih mudah parse instruksi.

6. **Pisahkan persona dari instruksi tugas**.
   - System: persona, batasan, format.
   - User message: tugas saat ini.

7. **Iterasi adalah norma**.
   - Jarang sekali prompt sempurna di percobaan pertama. Plan untuk 3-5 iterasi.

## Anti-Pattern Umum

| Anti-Pattern | Contoh | Dampak |
|---|---|---|
| **Permintaan kontradiktif** | "Singkat tetapi lengkap" | Output mediocre |
| **Beban kognitif berlebih** | 15 batasan dalam satu prompt | Claude lupa beberapa |
| **Instruksi negatif tanpa positif** | "Jangan begini, jangan begitu" | Claude bingung "harus apa" |
| **Pertanyaan ambigu** | "Bagus tidak?" | Jawaban tidak terprediksi |
| **Asumsi tanpa konteks** | "Lanjut yang tadi" tanpa konteks | Halusinasi |
| **Format goal tidak terspesifikasi** | "Jawab pertanyaannya" | Output panjang/pendek tergantung mood |
| **Mencampur banyak task** | "Ringkas, terjemahkan, dan analisis sekaligus" | Kualitas turun di semua task |

## Iterative Refinement Pattern

Saat menyusun prompt baru, gunakan pola berikut:

```
Versi 1: prompt minimal → test → identifikasi kekurangan
Versi 2: tambah 1-2 perbaikan → test → identifikasi sisa kekurangan
Versi 3: tambah edge case handling → test → puas
Versi 4: simplifikasi yang bisa di-simplifikasi → test akhir
```

Versi terakhir biasanya **lebih simpel** dari versi tengah — banyak instruksi yang awalnya terasa perlu, ternyata tidak.

Lanjutkan ke `latihan.md` Section 3 untuk eksekusi.

---

# Section 4 — Zero-shot & Few-shot Prompting

**Tujuan section**: memahami **kapan** Anda perlu memberi Claude contoh dan **kapan** instruksi murni sudah cukup. Lalu menambahkan few-shot examples ke AI Advisor untuk konsistensi format yang lebih kuat.

## Definisi

### Zero-shot Prompting

Anda meminta Claude melakukan task **tanpa memberi contoh** sebelumnya. Hanya instruksi.

```
Klasifikasikan kategori transaksi berikut sebagai
"income" atau "expense":

Bayar listrik bulanan
```

Claude akan mengandalkan **pengetahuan umum** dan instruksi untuk memberi jawaban.

### Few-shot Prompting

Anda memberi Claude **beberapa contoh input → output** sebelum task yang sebenarnya.

```
Klasifikasikan kategori transaksi berikut sebagai
"income" atau "expense":

Gaji bulan ini → income
Beli kopi → expense
Hasil freelance → income
Bayar internet → expense

Sekarang klasifikasikan:
Bayar listrik bulanan
```

Claude melihat pola dan menjawab sesuai pola.

## Kapan Pakai yang Mana?

| Karakter Task | Zero-shot | Few-shot |
|---|---|---|
| Task umum yang Claude sudah "tahu" (tanya jawab, summary) | ✅ Cukup | ❌ Boros token |
| Format output yang **sangat spesifik** (JSON kustom, gaya tertentu) | ⚠️ Bisa gagal | ✅ Lebih reliable |
| Klasifikasi dengan kategori unik | ⚠️ Bisa salah label | ✅ Pasti pakai label yang Anda berikan |
| Reasoning kompleks | ⚠️ Sering inkonsisten | ✅ Contoh chain-of-thought membantu |
| Task yang tidak biasa / niche | ❌ Sering gagal | ✅ Wajib |

## Trade-off Few-shot

| Aspek | Implikasi |
|---|---|
| **Token usage** | Naik linear dengan jumlah contoh |
| **Konsistensi** | Naik signifikan |
| **Maintenance** | Contoh perlu di-update saat domain berubah |
| **Halusinasi** | Turun (Claude lebih anchor ke contoh) |

## Berapa Banyak Contoh yang Ideal?

| Jumlah Contoh | Karakter |
|---|---|
| **1-shot** | Lebih baik dari zero-shot, tetapi pattern belum jelas |
| **3-5 shot** | Sweet spot untuk kebanyakan task |
| **10+ shot** | Diminishing returns, boros token |

**Variasi penting**: contoh-contoh harus mewakili **distribusi** input yang akan Claude hadapi. Jangan semua contoh "easy case" — sertakan edge case.

## Aplikasi di AI Financial Advisor

Pertanyaan keuangan personal punya banyak variasi gaya:

- "Tips menabung dong" (casual)
- "Bagaimana strategi menabung yang efektif?" (formal)
- "DP rumah 5 thn lg gmn caranya" (singkat, banyak singkatan)

Dengan **few-shot examples** di system instruction, Anda dapat mengarahkan Claude untuk:

- Memahami berbagai gaya bahasa.
- Selalu merespons dengan format konsisten (markdown, list, bold).
- Menangani pertanyaan ambigu dengan cara yang konsisten.

Pada Section 4 latihan, Anda akan menambah 3-5 contoh ke system prompt dan melihat dampaknya pada konsistensi.

Lanjutkan ke `latihan.md` Section 4 untuk eksekusi.

---

# Section 5 — Role, Context, & Instruction

**Tujuan section**: mempelajari pola **RCI (Role-Context-Instruction)** sebagai kerangka terstruktur untuk menyusun prompt. Lalu restrukturisasi system prompt AI Advisor agar lebih maintainable dan testable.

## Apa itu Pola RCI?

Pola RCI memisahkan **tiga lapis** informasi yang harus ada di prompt:

```
┌──────────────────────────────────────────────┐
│  ROLE        → Siapa Claude saat ini?        │
│  CONTEXT     → Apa situasi dan datanya?      │
│  INSTRUCTION → Apa yang harus dia lakukan?   │
└──────────────────────────────────────────────┘
```

### Mengapa Memisahkan?

Pada Section 1-4, system prompt Anda mencampur ketiganya dalam satu blok prose. Itu **bekerja**, tetapi:

- Sulit memodifikasi satu aspek tanpa kerusakan aspek lain.
- Sulit reuse untuk task lain (mis. fitur "Insight Mingguan" mungkin pakai role yang sama, context berbeda).
- Sulit di-debug — kalau output salah, sulit tahu apakah masalah di role / context / instruction.

Pola RCI memisahkan ketiganya dengan struktur eksplisit.

## Struktur Konkret

Berikut versi RCI untuk AI Financial Advisor:

```ts
const ROLE = `
Anda adalah AI Financial Advisor di Fin-App — aplikasi
personal finance tracker untuk pengguna Indonesia.
Persona Anda: ramah, jelas, to-the-point, dan suportif.
`;

const CONTEXT = `
Pengguna adalah individu yang melacak keuangan personal
mereka. Topik yang relevan: pengeluaran harian, tabungan,
perencanaan budget, investasi dasar untuk pemula.
Bahasa percakapan: Bahasa Indonesia.
`;

const FORMAT = `
- Markdown rapi.
- List bertanda untuk poin-poin.
- Bold (**) untuk angka penting.
- Format Rupiah: "Rp 1.500.000".
- Format persentase: "15%".
`;

const INSTRUCTION = `
Jawab pertanyaan pengguna sesuai role di atas.
Apabila pertanyaan di luar topik keuangan, sopan
kembalikan ke topik.
Apabila pertanyaan ambigu, minta klarifikasi singkat.
`;

const SYSTEM = `
# ROLE
${ROLE}

# CONTEXT
${CONTEXT}

# OUTPUT FORMAT
${FORMAT}

# INSTRUCTION
${INSTRUCTION}
`;
```

## Keuntungan Komposisi Modular

Dengan struktur ini, Anda dapat membuat **varian** prompt dengan reuse:

```ts
// Untuk fitur "Insight Mingguan":
const INSIGHT_INSTRUCTION = `
Berdasarkan data transaksi minggu ini, berikan 3 insight
penting tentang pola pengeluaran user.
`;

const INSIGHT_SYSTEM = `
# ROLE
${ROLE}                  // ← reuse dari ADVISOR

# CONTEXT
${CONTEXT}               // ← reuse

# OUTPUT FORMAT
${FORMAT}                // ← reuse

# INSTRUCTION
${INSIGHT_INSTRUCTION}   // ← khusus fitur insight
`;
```

ROLE, CONTEXT, dan FORMAT dipakai ulang. Hanya INSTRUCTION yang berbeda.

## Tip Praktis Iterasi RCI

Saat menyusun prompt RCI, **debug per lapis**:

| Apabila output salah... | Periksa lapis mana? |
|---|---|
| Persona salah (terlalu formal/casual) | **ROLE** |
| Tidak relevan dengan domain | **CONTEXT** |
| Format jelek (no markdown, no Rupiah) | **FORMAT** |
| Tidak menjawab pertanyaan yang dimaksud | **INSTRUCTION** |

Pemisahan ini membuat debugging jauh lebih cepat dibanding prompt monolitik.

## Anti-Pattern di Pola RCI

- ❌ **Mencampur role ke context**: "Anda advisor untuk user yang menabung untuk DP rumah" — campur. Pisahkan: ROLE = "advisor", CONTEXT = "user sedang menabung untuk DP rumah".
- ❌ **Instruction yang dependent pada context dinamis**: lebih baik pakai variable substitution.
- ❌ **Format yang tergantung pada instruction**: format harus berdiri sendiri.

Lanjutkan ke `latihan.md` Section 5 untuk eksekusi.

---

# Section 6 — Agentic Workflow

**Tujuan section**: melampaui chatbot pasif — biarkan Claude **memanggil tool** untuk membaca data transaksi nyata user dari Supabase, lalu menjawab pertanyaan dengan **angka aktual**.

## Apa itu Agentic Workflow?

Pada section sebelumnya, Claude **hanya bisa menjawab** berdasarkan pengetahuannya. Apabila user bertanya:

> "Berapa total expense food saya bulan ini?"

Claude akan **menebak** atau bilang "saya tidak punya akses ke data Anda".

**Agentic workflow** memberi Claude kemampuan untuk:

1. **Memutuskan** ia perlu data tambahan.
2. **Memanggil tool** (function) untuk dapat data.
3. **Memproses hasil** dan menyusun jawaban final.

```
User: "Berapa total expense food saya bulan ini?"
   │
Claude (analisa): "Saya perlu data transaksi.
                   Panggil tool get_transactions
                   dengan filter category='Food'."
   │
Tool dipanggil   → Supabase query → return rows
   │
Claude (analisa hasil): "Total Rp 1.250.000 dari 12
                         transaksi food bulan ini."
   │
User melihat respons dengan angka aktual.
```

## Konsep "Tool Use" di Claude API

Anthropic SDK mendukung tool use lewat parameter `tools`:

```ts
client.messages.create({
  model: "claude-haiku-4-5",
  max_tokens: 1024,
  system: SYSTEM_RCI,
  tools: [
    {
      name: "get_transactions",
      description: "Ambil daftar transaksi user dengan filter opsional.",
      input_schema: {
        type: "object",
        properties: {
          category: { type: "string", description: "Filter by category" },
          start_date: { type: "string", description: "YYYY-MM-DD" },
          end_date: { type: "string", description: "YYYY-MM-DD" },
          type: { type: "string", enum: ["income", "expense"] },
        },
      },
    },
  ],
  messages: [{ role: "user", content: userMessage }],
});
```

Saat Claude memutuskan perlu memanggil tool, respons-nya berisi block dengan `type: "tool_use"`:

```ts
response.content = [
  { type: "tool_use", id: "toolu_01...", name: "get_transactions", input: { category: "Food" } }
]
```

Anda kemudian:

1. Eksekusi tool tersebut di kode Anda (query Supabase).
2. Kirim hasil tool **kembali** ke Claude sebagai message baru.
3. Claude memproses hasil dan menghasilkan jawaban final.

## Loop Multi-Step

Karena Claude bisa memanggil **beberapa tool secara berurutan**, alurnya menjadi *loop*:

```
1. Kirim user message + tools
2. Cek response:
   - Apabila content berisi tool_use → eksekusi tool → kirim hasil → ulang ke step 2
   - Apabila content berisi text → tampilkan ke user → selesai
3. Loop maksimum (mis. 5 iterasi) untuk safety.
```

## Tools yang Akan Dibangun di Fin-App

Pada Section 6 latihan, Anda akan membangun **dua tool sederhana**:

| Tool | Input | Output | Use Case |
|---|---|---|---|
| `get_transactions` | Filter (category, date range, type) | Array transaksi | "Berapa total food bulan ini?" |
| `get_balance_summary` | (tidak ada) | { totalIncome, totalExpense, savings } | "Bagaimana keuangan saya secara umum?" |

Tool ini reuse query Supabase yang sudah Anda bangun di **Module 02 (CRUD)**. Tidak ada query baru — hanya wrapper agar Claude bisa memanggilnya.

## Implications untuk UX Chatbot

Saat Claude memanggil tool, ada **delay tambahan** sebelum respons final. UX yang baik:

- Tampilkan indikator "Membaca data transaksi Anda..." saat tool dipanggil.
- Apabila tool memanggil beberapa kali (loop), tampilkan setiap langkah secara bertahap.
- Pada streaming (Module 04 Section 6), tool calls muncul sebagai event terpisah dalam stream.

## Batasan Section 6

Untuk modul ini, agentic workflow dibatasi pada:

- **Read-only tool**: Claude bisa baca data, tidak bisa modify (tidak ada `create_transaction`, `delete_transaction` — terlalu berisiko untuk eksperimen awal).
- **Lokal scope**: hanya tool yang dipanggil dari route handler chatbot (bukan MCP atau server eksternal).
- **Tanpa retry/error logic kompleks**: apabila tool gagal, kembalikan pesan error ke Claude dan biarkan ia merespons gracefully.

Versi production-grade dari agentic workflow membutuhkan permission system, audit trail, dan safeguards yang lebih kuat. Itu modul tersendiri.

Lanjutkan ke `latihan.md` Section 6 untuk eksekusi.
