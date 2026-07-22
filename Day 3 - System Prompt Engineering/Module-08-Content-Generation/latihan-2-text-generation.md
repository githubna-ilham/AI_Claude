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

<details>
<summary><strong>Salin prompt berikut, paste ke Claude Code</strong></summary>

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

</details>

**Verifikasi:**

1. Kirim pertanyaan yang sama 3 kali di chatbot: "Berikan 3 ide nama tabungan untuk DP rumah."
2. Bandingkan respons. Dengan temperature 0.5, jawaban biasanya **mirip tetapi tidak identik**.
3. (Opsional) Untuk eksperimen lebih, ubah temperature jadi `0.0`, restart server, kirim pertanyaan sama 3 kali — jawaban harusnya sangat mirip atau identik.

---

## Prompt 2 — Naikkan `max_tokens` di `askAdvisor`

### Walkthrough Manual (sebelum pakai prompt)

`max_tokens: 1024` dari Section 1 cukup untuk pertanyaan singkat, tapi rawan terpotong untuk pertanyaan detail (mis. "Jelaskan strategi investasi jangka panjang"). Naikkan ke `2048` agar respons tidak berhenti di tengah kalimat.

📂 **File yang diubah**: `src/features/advisor.ts` (modifikasi)

**1. Ubah nilai `max_tokens`**

📍 Lokasi: **di dalam function `askAdvisor`**, di object argumen `client.messages.create({...})`.

```ts
// src/features/advisor.ts — di dalam function askAdvisor
const response = await client.messages.create({
  model: "claude-haiku-4-5",
  max_tokens: 2048,   // ← naik dari 1024
  temperature: 0.5,
  messages: [{ role: "user", content: message }],
});
```

**Mengapa 2048?** Jawaban keuangan yang detail (analisis portofolio, perbandingan produk) bisa mencapai 800–1200 token. `1024` terlalu mepet; `2048` memberi ruang cukup tanpa boros biaya seperti `4096`.

### Yang TIDAK perlu

- ❌ Membuat file eksperimen — perubahan langsung di `advisor.ts`.
- ❌ Mengubah parameter lain (`temperature`, `model`).
- ❌ Menambah parameter `system`.

### Verifikasi setelah file diubah

1. Reload chatbot. Kirim pertanyaan panjang: "Jelaskan perbedaan reksa dana pasar uang, pendapatan tetap, dan saham — mana yang cocok untuk dana darurat, mana untuk investasi 10 tahun?"
2. Respons seharusnya **tidak terpotong** di tengah kalimat.
3. (Opsional) Bandingkan dengan sementara set ke `max_tokens: 100` — respons akan terpotong tiba-tiba.

**Hasil yang Diharapkan** — bagian yang diubah:

```ts
// src/features/advisor.ts — di dalam function askAdvisor
const response = await client.messages.create({
  model: "claude-haiku-4-5",
  max_tokens: 2048,   // naik dari 1024
  temperature: 0.5,
  messages: [{ role: "user", content: message }],
});
```

<details>
<summary><strong>Salin prompt berikut, paste ke Claude Code</strong></summary>

```
Naikkan max_tokens di server action askAdvisor.

GOAL:
- Modifikasi src/features/advisor.ts.
- Ubah max_tokens dari 1024 menjadi 2048 di dalam
  client.messages.create().

CONTEXT:
- Jawaban keuangan yang detail bisa mencapai 800–1200 token.
- 1024 terlalu mepet; 2048 memberi ruang cukup.
- Pertahankan temperature: 0.5 dari Prompt 1.

GUARDRAIL:
- JANGAN ubah parameter lain.
- JANGAN tambah parameter system.
```

</details>

**Verifikasi:**

1. Reload chatbot. Kirim: "Jelaskan perbedaan reksa dana pasar uang, pendapatan tetap, dan saham — mana yang cocok untuk dana darurat, mana untuk investasi 10 tahun?"
2. Respons muncul lengkap, tidak terpotong di tengah kalimat.

---

---

## Prompt 3 — Prompt Prefixing untuk Mengarahkan Format

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

<details>
<summary><strong>Salin prompt berikut, paste ke Claude Code</strong></summary>

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

</details>

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
- [ ] `max_tokens` sudah dinaikkan ke `2048` di `askAdvisor`.
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
