# Section 2 — Text Generation

> Bagian dari **[Module 04 — Latihan](./latihan.md)**. Lanjutan dari **[Section 1](./latihan-1-integrasi-api.md)**.

> Latihan untuk mengeksplorasi parameter generation Claude API: `max_tokens`, `temperature`, `stop_sequences` — serta pola **prompt prefixing** untuk mengarahkan format output tanpa system instruction. Empat prompt siap copy-paste.
>
> **Estimasi Section 2**: 35–45 menit.

> 📌 **Catatan**: Module 04 sengaja **belum menggunakan parameter `system`**. Format dan persona dikontrol murni lewat user message + parameter generation. System instruction adalah topik tersendiri.

## Prasyarat Section 2

- [ ] Section 1 selesai (+ Latihan UI Module 03). Chatbot dapat menerima pertanyaan dan menampilkan respons asli dari Claude.
- [ ] Anda sudah membaca bagian Section 2 di `materi.md`.

---

## 📚 Referensi Dokumentasi

Section ini banyak bermain dengan **parameter generation**. Bookmark halaman ini untuk referensi cepat:

- **[Messages API parameters](https://docs.claude.com/en/api/messages)** — daftar lengkap: `temperature`, `top_p`, `top_k`, `max_tokens`, `stop_sequences`, `stop_reason`.
- **[Tuning sampling parameters](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/temperature)** — kapan pakai temperature rendah vs tinggi, kombinasi dengan `top_p`.
- **[Models overview](https://docs.claude.com/en/docs/about-claude/models/overview)** — harga per 1M token tiap model (relevan saat lihat biaya eksperimen).
- **[Stop reasons](https://docs.claude.com/en/api/messages#response-stop-reason)** — `"end_turn"`, `"max_tokens"`, `"stop_sequence"`, `"tool_use"`, dll.

---

## Prompt 1 — Tambah Parameter `temperature` ke `askAdvisor`

### Walkthrough Manual (sebelum pakai prompt)

Perubahan kecil tetapi penting: satu parameter baru di API call. Memahami secara manual membuat Anda paham efek `temperature` terhadap kualitas respons.

📂 **File yang diubah**: `src/features/advisor.ts` (modifikasi)

**1. Tambah `temperature` ke `client.messages.create(...)`**

📍 Lokasi: **di dalam function `askAdvisor`**, di object argumen `client.messages.create({...})` yang sudah ada sejak Section 1.

```ts
// src/features/advisor.ts — di dalam function askAdvisor
const response = await client.messages.create({
  model: "claude-haiku-4-5",
  max_tokens: 1024,
  temperature: 0.5,                              // ← BARU
  messages: [{ role: "user", content: message }],
});
```

**2. Update JSDoc di atas function**

📍 Lokasi: **tepat di atas `export async function askAdvisor`**.

```ts
// src/features/advisor.ts — di atas function
/**
 * Server action untuk meminta jawaban dari AI Financial Advisor.
 * Menggunakan temperature 0.5 (seimbang antara faktual dan natural)
 * untuk konteks chatbot keuangan.
 */
```

### Yang TIDAK perlu

- ❌ Mengubah `model` atau `max_tokens` (cukup tambah satu parameter saja).
- ❌ Menambahkan parameter `system` (Module 04 belum pakai system instruction).
- ❌ Mengekspor konstanta `TEMPERATURE` — hardcode dulu di call site.
- ❌ Membuat wrapper / opsional parameter — cukup nilai literal `0.5`.

### Verifikasi setelah file diubah

1. Pastikan tidak ada error TypeScript di file.
2. Reload chatbot, kirim "Berikan 3 ide nama tabungan untuk DP rumah." sebanyak 3x.
3. Jawaban biasanya **mirip tetapi tidak identik** — variasi sedang.
4. (Opsional) Ubah sementara ke `temperature: 0.0`, restart, jawaban harusnya hampir identik.

---

**Salin prompt berikut, paste ke Claude Code:**

```
Saya ingin mengontrol tingkat kreativitas respons Claude.
Tambahkan parameter temperature ke server action.

GOAL:
- Modifikasi src/features/advisor.ts.
- Tambahkan parameter `temperature: 0.5` ke
  client.messages.create() (saat ini hanya ada model,
  max_tokens, messages).
- Tambahkan JSDoc di atas function yang menjelaskan
  alasan pemilihan 0.5 (seimbang antara faktual dan
  natural).

CONTEXT:
- Range temperature 0.0 - 1.0.
- Untuk chatbot keuangan: 0.5 seimbang (faktual tetapi tidak
  kaku).
- JANGAN tambahkan parameter system — Module 04 belum pakai
  system instruction.

GUARDRAIL:
- Pertahankan validasi kosong dan return type dari Section 1.
- JANGAN ubah model atau max_tokens.
```

**Verifikasi:**

1. Kirim pertanyaan yang sama 3 kali di chatbot: "Berikan 3 ide nama tabungan untuk DP rumah."
2. Bandingkan respons. Dengan temperature 0.5, jawaban biasanya **mirip tetapi tidak identik**.
3. (Opsional) Untuk eksperimen lebih, ubah temperature jadi `0.0`, restart server, kirim pertanyaan sama 3 kali — jawaban harusnya sangat mirip atau identik.

---

## Prompt 2 — Eksplorasi `temperature` di File Eksperimen

### Walkthrough Manual (sebelum pakai prompt)

File eksperimen standalone — terpisah dari aplikasi utama. Tujuannya melatih intuisi: berapa besar variasi output di tiap level `temperature`.

📂 **File yang diubah**: `experiments/temperature-test.ts` (file baru)

**1. Import SDK + inisialisasi client**

📍 Lokasi: **paling atas file**.

```ts
// experiments/temperature-test.ts — bagian atas
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});
```

**2. Function `main` dengan double-loop**

📍 Lokasi: **di bawah inisialisasi**. Loop outer: temperature values. Loop inner: 2 attempts.

```ts
// experiments/temperature-test.ts — function main
async function main() {
  const temperatures = [0.0, 0.5, 1.0];
  const question = "Berikan satu nama unik untuk celengan digital.";

  for (const temp of temperatures) {
    console.log(`\n--- temperature: ${temp} ---`);
    for (let attempt = 1; attempt <= 2; attempt++) {
      const response = await client.messages.create({
        model: "claude-haiku-4-5",
        max_tokens: 100,
        temperature: temp,
        messages: [{ role: "user", content: question }],
      });
      const block = response.content[0];
      const text = block.type === "text" ? block.text : "(non-text)";
      console.log(`Attempt ${attempt}: ${text}`);
    }
  }
}

main().catch((err) => { console.error(err); process.exit(1); });
```

### Yang TIDAK perlu

- ❌ Memodifikasi `askAdvisor` — eksperimen ini berdiri sendiri.
- ❌ Output JSON / file — cukup `console.log` ke stdout.
- ❌ Retry logic kalau error — fail-fast supaya cepat ketahuan.
- ❌ Validasi input atau prompt prefixing — bukan tujuan eksperimen ini.

### Verifikasi setelah file diubah

1. Jalankan: `npx tsx --env-file=.env.local experiments/temperature-test.ts`.
2. Temperature 0.0 → 2 attempt biasanya identik / hampir identik.
3. Temperature 0.5 → variasi sedang.
4. Temperature 1.0 → variasi tinggi, sering sangat berbeda.

---

**Salin prompt berikut:**

```
Bantu saya membuat eksperimen membandingkan temperature.

GOAL:
- Buat file baru experiments/temperature-test.ts.
- Loop melalui 3 nilai temperature: 0.0, 0.5, 1.0.
- Untuk setiap nilai, kirim pertanyaan yang sama 2 kali:
  "Berikan satu nama unik untuk celengan digital."
- Print hasil dengan format:
  --- temperature: 0.0 ---
  Attempt 1: <jawaban>
  Attempt 2: <jawaban>
  --- temperature: 0.5 ---
  ...

- Pakai Anthropic SDK langsung (bukan via askAdvisor).
- Model: "claude-haiku-4-5".
- max_tokens: 100 (jawabannya singkat).

CONTEXT:
- File standalone seperti experiments/claude-test.ts dari
  Module 03.
- Jalankan dengan: npx tsx --env-file=.env.local
  experiments/temperature-test.ts

GUARDRAIL:
- JANGAN modifikasi askAdvisor — eksperimen ini terpisah.
- Print clear separator antar temperature setting.
```

**Verifikasi:**

1. Jalankan file. Hasilnya:
   - Temperature 0.0 → dua attempt biasanya identik atau hampir identik.
   - Temperature 0.5 → variasi sedang.
   - Temperature 1.0 → variasi tinggi, kadang sangat berbeda.
2. Eksperimen ini melatih intuisi Anda tentang parameter temperature.

---

## Prompt 3 — Eksplorasi `max_tokens` dan `stop_reason`

### Walkthrough Manual (sebelum pakai prompt)

Eksperimen kedua: lihat efek `max_tokens` ke output dan field `stop_reason`. Pemahaman ini krusial untuk men-tuning aplikasi production.

📂 **File yang diubah**: `experiments/max-tokens-test.ts` (file baru)

**1. Setup client (sama seperti Prompt 2)**

📍 Lokasi: **paling atas file**.

```ts
// experiments/max-tokens-test.ts — bagian atas
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});
```

**2. Loop nilai `max_tokens` + log `stop_reason`**

📍 Lokasi: **function `main` di bawah inisialisasi**. Yang paling penting di-log: `stop_reason` dan `usage.output_tokens`.

```ts
// experiments/max-tokens-test.ts — function main
async function main() {
  const question = "Jelaskan secara detail strategi menghemat pengeluaran bulanan.";
  const limits = [50, 200, 1024];

  for (const limit of limits) {
    const response = await client.messages.create({
      model: "claude-haiku-4-5",
      max_tokens: limit,
      temperature: 0.5,
      messages: [{ role: "user", content: question }],
    });
    const block = response.content[0];
    const text = block.type === "text" ? block.text : "(non-text)";
    console.log(`\n--- max_tokens: ${limit} ---`);
    console.log(`stop_reason: ${response.stop_reason}`);
    console.log(`output_tokens: ${response.usage.output_tokens}`);
    console.log(`Hasil: ${text.slice(0, 300)}${text.length > 300 ? "..." : ""}`);
  }
}

main().catch((err) => { console.error(err); process.exit(1); });
```

### Yang TIDAK perlu

- ❌ Menambah parameter `system` — bukan tujuan.
- ❌ Streaming — eksperimen ini sinkron saja.
- ❌ Save ke file — cukup print.
- ❌ Menghitung biaya / token usd-equivalent — fokus pada `stop_reason`.

### Verifikasi setelah file diubah

1. Jalankan: `npx tsx --env-file=.env.local experiments/max-tokens-test.ts`.
2. `max_tokens: 50` → `stop_reason: "max_tokens"`, output terpotong.
3. `max_tokens: 200` → mungkin masih terpotong atau pas.
4. `max_tokens: 1024` → `stop_reason: "end_turn"`, output natural.

---

**Salin prompt berikut:**

```
Bantu saya membuat eksperimen tentang max_tokens dan
stop_reason.

GOAL:
- Buat file baru experiments/max-tokens-test.ts.
- Pakai pertanyaan: "Jelaskan secara detail strategi
  menghemat pengeluaran bulanan."
- Loop melalui 3 nilai max_tokens: 50, 200, 1024.
- Untuk setiap nilai, print:
  --- max_tokens: 50 ---
  stop_reason: <reason>
  output_tokens: <jumlah>
  Hasil: <teks>
  (panjang teks dapat di-truncate jika sangat panjang)
  ---

CONTEXT:
- File standalone.
- Model: claude-haiku-4-5.
- temperature: 0.5.

GUARDRAIL:
- Print stop_reason dengan jelas — ini intinya.
- JANGAN tambah system parameter.
```

**Verifikasi:**

1. Jalankan file. Amati:
   - max_tokens 50 → output terpotong, `stop_reason: "max_tokens"`.
   - max_tokens 200 → mungkin masih terpotong, atau pas.
   - max_tokens 1024 → biasanya selesai natural, `stop_reason: "end_turn"`.
2. Anda sekarang punya intuisi: max_tokens harus **cukup** untuk pertanyaan terpanjang yang ekspektasi.

---

## Prompt 4 — Prompt Prefixing untuk Mengarahkan Format

### Walkthrough Manual (sebelum pakai prompt)

Tanpa parameter `system`, format output diarahkan lewat **prefix** yang digabung ke user message. Pola ini mudah dipakai dan sering jadi langkah pertama sebelum migrate ke system instruction.

📂 **File yang diubah**: `src/features/advisor.ts` (modifikasi)

**1. Definisikan konstanta `INSTRUCTION_PREFIX`**

📍 Lokasi: **di module level** (di bawah inisialisasi `client`, di atas function `askAdvisor`).

```ts
// src/features/advisor.ts — di bawah const client
const INSTRUCTION_PREFIX = `Anda menjawab dalam Bahasa Indonesia, ramah dan to-the-point. Pakai markdown: list bertanda untuk poin, bold untuk angka penting. Format Rupiah: "Rp 1.500.000". Persentase: "15%".

Pertanyaan: `;
```

**2. Gabungkan prefix ke user message**

📍 Lokasi: **di dalam function `askAdvisor`**, modifikasi argumen `content` di array `messages`.

```ts
// src/features/advisor.ts — di dalam function askAdvisor
const response = await client.messages.create({
  model: "claude-haiku-4-5",
  max_tokens: 1024,
  temperature: 0.5,
  messages: [{ role: "user", content: INSTRUCTION_PREFIX + message }],  // ← UBAH
});
```

### Yang TIDAK perlu

- ❌ Menambah parameter `system` — Module 04 belum pakai.
- ❌ Memindah `INSTRUCTION_PREFIX` ke file lain — cukup di `advisor.ts`.
- ❌ Trim atau modifikasi `message` user (selain concat prefix).
- ❌ Menambahkan branching bahasa / locale — fix Indonesia saja dulu.

### Verifikasi setelah file diubah

1. Reload chatbot. Kirim "Tips menghemat pengeluaran bulanan."
2. Respons dalam Bahasa Indonesia, pakai list bertanda, ada bold di angka.
3. Format Rupiah sesuai instruksi ("Rp 1.500.000").
4. (Opsional) Kirim pertanyaan dalam English — Claude tetap balas Bahasa Indonesia.

---

**Salin prompt berikut:**

```
Saya ingin mengarahkan format output (markdown, bahasa,
gaya) lewat user message, bukan system parameter.

GOAL:
- Modifikasi src/features/advisor.ts.
- Sebelum mengirim ke API, "prefix" user message dengan
  instruksi format. Buat konstanta INSTRUCTION_PREFIX di
  file yang sama:

  const INSTRUCTION_PREFIX = `Anda menjawab dalam Bahasa
  Indonesia, ramah dan to-the-point. Pakai markdown:
  list bertanda untuk poin, bold untuk angka penting.
  Format Rupiah: "Rp 1.500.000". Persentase: "15%".

  Pertanyaan: `;

- Saat memanggil API, gabungkan:
  content: INSTRUCTION_PREFIX + message

- Pertahankan parameter temperature dari Prompt 1.

CONTEXT:
- Inilah pola "prompt prefixing" — instruksi tetap di user
  message, tidak di system parameter.

GUARDRAIL:
- JANGAN tambahkan parameter system: ke API call.
- Pertahankan return type dan validasi kosong.
- JANGAN pindahkan INSTRUCTION_PREFIX ke file lain dulu —
  cukup di advisor.ts.
```

**Verifikasi:**

1. Reload browser. Kirim: "Tips menghemat pengeluaran bulanan."
2. Respons seharusnya:
   - Dalam Bahasa Indonesia.
   - Pakai list bertanda.
   - Format Rupiah dan persen sesuai instruksi.
3. (Opsional) Sengaja kirim pertanyaan dengan English: "How to save money?" — Claude masih akan menjawab dalam Bahasa Indonesia karena instruksi prefix.

---

## Validasi Akhir Section 2

- [ ] Parameter `temperature: 0.5` aktif di `askAdvisor`.
- [ ] File eksperimen `temperature-test.ts` jalan tanpa error.
- [ ] File eksperimen `max-tokens-test.ts` jalan tanpa error.
- [ ] Prompt prefixing aktif — respons konsisten Bahasa Indonesia + markdown.
- [ ] **TIDAK ADA** parameter `system` di mana pun di Module 04.
- [ ] Tidak ada regresi dari Section 1 (+ Latihan UI Module 03).

## Refleksi Section 2

1. Pada temperature berapa Anda merasa respons paling **alami** untuk konteks keuangan?
2. Apa kerugian prompt prefixing dibanding system instruction? (Hint: token usage.)
3. Apakah Anda menemui pertanyaan yang Claude **abaikan** instruction prefix-nya? (Mis. tetap jawab dalam English.)
4. Untuk task ekstraksi data terstruktur (mis. parse "Rp 50.000 makan siang"), apakah temperature 0.0 atau 0.5 lebih cocok? Mengapa?

---

⬅️ Kembali: **[Section 1](./latihan-1-integrasi-api.md)** · ➡️ Lanjut: **[Section 3 — Thinking / Thought](./latihan-3-thinking.md)**
