# Section 1 — System Instruction

> Bagian dari **[Module 05 — Latihan](./latihan.md)**. Lanjutan dari **[Module 04 — Section 6: Multi-Turn](../Module-04-Content-Generation/latihan-6-multi-turn.md)**.

> Latihan untuk bermigrasi dari **prompt prefixing** (Module 04) ke **parameter `system`**. Tiga prompt siap copy-paste.
>
> **Estimasi**: 30–40 menit.

## Prasyarat Section 1

- [ ] Module 04 selesai. AI Advisor pakai prompt prefixing dan dapat multi-turn.
- [ ] Anda sudah membaca bagian Section 1 di `materi.md`.

---

## 📚 Referensi Dokumentasi

Sebelum mulai, akan sangat membantu kalau Anda buka tab dokumentasi resmi Claude untuk referensi cepat saat ada kebingungan:

- **[System prompts](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/system-prompts)** — overview, kapan pakai parameter `system`, batasan, dan best practice migrasi dari pola prefixing.
- **[Messages API — parameter `system`](https://docs.claude.com/en/api/messages)** — format string vs content blocks, posisinya di payload `messages.create(...)`.
- **[Prompt caching (opsional)](https://docs.claude.com/en/docs/build-with-claude/prompt-caching)** — cara cache system prompt yang panjang agar hemat biaya saat percakapan multi-turn.
- **[Migration patterns](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/system-prompts)** — alasan teknis kenapa system parameter lebih hemat dibanding prefixing user message tiap turn.

---

## Prompt 1 — Buat File `prompts.ts` dengan System Instruction

### Walkthrough Manual (sebelum pakai prompt)

Sebelum copy-paste prompt ke Claude, pahami dulu apa saja yang harus ada di file baru `src/features/prompts.ts`. Ini akan membantu Anda **mereview** output Claude.

📂 **File baru**: `src/features/prompts.ts` (satu file konstanta, tidak modifikasi yang lain)

**1. File ini TIDAK pakai `"use server"`**

📍 Lokasi: **baris pertama file**. Karena ini hanya berisi konstanta string (bukan function async), tidak perlu directive `"use server"`. Bisa di-import dari client maupun server.

```ts
// src/features/prompts.ts — baris pertama
// (TIDAK ada "use server" — ini file konstanta murni)
```

**2. Konstanta `ADVISOR_SYSTEM` (string multi-line)**

📍 Lokasi: **di module level**, ekspor langsung. Pakai template literal (backtick) supaya struktur markdown tetap terbaca di IDE.

```ts
// src/features/prompts.ts — module level
export const ADVISOR_SYSTEM = `
## Persona
Anda adalah **AI Financial Advisor** untuk Fin-App...

## Lingkup
- Pengeluaran, tabungan, budget, investasi pemula
- ...

## Format Output
- Markdown rapi (list bertanda, bold untuk angka)
- Format mata uang: Rp 1.500.000
- ...

## Batasan
- JANGAN beri nasihat hukum/pajak spesifik
- JANGAN janjikan return investasi
`.trim();
```

**3. Empat section wajib (mirror struktur di materi.md "Anatomi System Instruction yang Baik")**

- **Persona** — siapa Claude, gaya bicara, bahasa.
- **Lingkup** — topik yang boleh dijawab.
- **Format Output** — markdown, list, format angka.
- **Batasan** — yang TIDAK boleh dilakukan.

### Yang TIDAK perlu

- ❌ Directive `"use server"` (file ini hanya konstanta — di-import oleh route handler nanti).
- ❌ Function atau builder — cukup konstanta string statis.
- ❌ Modifikasi `route.ts` atau `advisor.ts` di prompt ini — itu akan dilakukan di Prompt 2.
- ❌ Komentar JSDoc panjang — heading markdown di dalam string sudah cukup self-documenting.

### Verifikasi setelah file dibuat

1. File `src/features/prompts.ts` ada dengan ekspor `ADVISOR_SYSTEM`.
2. Struktur prompt terbagi dalam sections jelas dengan heading markdown (`## Persona`, `## Lingkup`, dst.).
3. Tidak ada error TypeScript saat `npx tsc --noEmit`.
4. File TIDAK punya `"use server"` di baris pertama.

---

**Salin prompt berikut:**

```
Saya ingin memindahkan instruksi format dari user message
prefix ke parameter system.

GOAL:
- Buat file baru src/features/prompts.ts.
- Ekspor konstanta ADVISOR_SYSTEM dengan struktur jelas
  (sections terpisah: Persona, Lingkup, Format Output,
  Batasan).

CONTEXT:
- Persona: AI Financial Advisor untuk Fin-App, ramah,
  to-the-point, profesional, Bahasa Indonesia.
- Lingkup: keuangan personal (pengeluaran, tabungan,
  budget, investasi pemula).
- Format output: markdown, list bertanda, bold untuk angka,
  Rp 1.500.000, 15%.
- Batasan: jangan beri nasihat hukum/pajak spesifik; jangan
  janjikan return investasi.

GUARDRAIL:
- File ini hanya berisi konstanta — JANGAN tambah "use server".
- Gunakan template literal multi-line untuk readability.
- JANGAN ubah file advisor.ts atau route.ts di prompt ini —
  itu akan dilakukan di prompt 2.
```

**Verifikasi:**

1. File `src/features/prompts.ts` ada dengan ekspor `ADVISOR_SYSTEM`.
2. Struktur prompt terbagi dalam sections jelas dengan heading markdown (## Persona, ## Lingkup, dst.).
3. Tidak ada error TypeScript.

---

## Prompt 2 — Migrasi `route.ts` dari Prefixing ke System

### Walkthrough Manual (sebelum pakai prompt)

Sebelum copy-paste prompt ke Claude, pahami perubahan kecil tapi penting di `src/app/api/advisor/route.ts`. Ini bukan rewrite — hanya **swap** dari pola prefixing ke parameter `system`.

📂 **File yang diubah**: `src/app/api/advisor/route.ts` (modifikasi, BUKAN file baru)

**1. Tambah import `ADVISOR_SYSTEM`**

📍 Lokasi: **paling atas file**, di bagian import (bersama import `Anthropic`, dll. dari Module 04).

```ts
// src/app/api/advisor/route.ts — bagian import
import { ADVISOR_SYSTEM } from "@/features/prompts";
```

**2. Hapus `INSTRUCTION_PREFIX` lama**

📍 Lokasi: **di module level**, declaration `const INSTRUCTION_PREFIX = "..."` yang dibuat di Module 04. Hapus seluruhnya — sudah tidak dipakai.

```ts
// src/app/api/advisor/route.ts — HAPUS BARIS INI (dari Module 04)
// const INSTRUCTION_PREFIX = `Anda adalah AI Financial Advisor...`;
```

**3. Bersihkan penggabungan prefix + user message di array `messages`**

📍 Lokasi: **di dalam handler `POST`**, area saat membangun `messages` payload sebelum `client.messages.stream(...)`. Sebelum migrasi, ada penggabungan `INSTRUCTION_PREFIX + " " + lastUserMessage`. Sekarang user message dikirim **murni**.

```ts
// src/app/api/advisor/route.ts — di dalam POST handler, SEBELUM (Module 04)
const messages = [
  ...history,
  { role: "user", content: INSTRUCTION_PREFIX + " " + lastMessage }, // ← prefix di-prepend
];

// SESUDAH (Module 05) — user message murni
const messages = [
  ...history,
  { role: "user", content: lastMessage },
];
```

**4. Tambah parameter `system` di `client.messages.stream(...)`**

📍 Lokasi: **di dalam handler `POST`**, di pemanggilan `client.messages.stream({ ... })` (atau `.create()` untuk branching Opus). Tambahkan `system: ADVISOR_SYSTEM` sebagai parameter API.

```ts
// src/app/api/advisor/route.ts — di dalam POST handler
const stream = client.messages.stream({
  model: selectedModel,
  max_tokens: 1024,
  system: ADVISOR_SYSTEM,                  /* ← BARU */
  messages,                                 /* ← user message murni */
  // ...thinking, temperature, dst. dari Module 04 — pertahankan
});
```

> 💡 `system` adalah **parameter top-level**, bukan masuk ke array `messages`. Salah satu kesalahan umum: meletakkan system sebagai message dengan `role: "system"` (itu OpenAI pattern, BUKAN Anthropic).

### Yang TIDAK perlu

- ❌ Mengubah struktur **streaming** atau handler thinking — pertahankan persis dari Module 04 Section 6.
- ❌ Modifikasi branching Haiku/Opus — `selectedModel` tetap ditentukan oleh logic Module 04.
- ❌ Membersihkan file eksperimen di `experiments/` yang masih pakai `INSTRUCTION_PREFIX` — itu untuk Prompt 3 perbandingan.
- ❌ Refactor temperature/max_tokens — biarkan persis.

### Verifikasi setelah file diubah

1. Reload browser. Kirim pertanyaan "Halo, siapa kamu?".
2. Respons dalam Bahasa Indonesia, format markdown rapi (sama seperti Module 04).
3. Buka DevTools → Network → cek request body ke `/api/advisor`: array `messages` **tidak** lagi mengandung prefix instruksi.
4. Multi-turn tetap bekerja: kirim pertanyaan lanjutan, konteks percakapan terjaga.
5. Jalankan `npx tsc --noEmit` — tidak ada error tentang `INSTRUCTION_PREFIX` undefined.

---

**Salin prompt berikut:**

```
Sekarang ganti pola prompt prefixing dengan parameter
system di route handler chatbot.

GOAL:
- Modifikasi src/app/api/advisor/route.ts.
- Hapus INSTRUCTION_PREFIX dari pemanggilan API.
- Tambahkan parameter system: ADVISOR_SYSTEM (import dari
  "@/features/prompts").
- Messages array sekarang langsung berisi user message
  tanpa prefix.

CONTEXT:
- Pertahankan: temperature, max_tokens, branching Haiku/Opus,
  thinking support, streaming.
- INSTRUCTION_PREFIX bisa dihapus dari file (sudah tidak
  dipakai).

GUARDRAIL:
- JANGAN ubah struktur streaming atau penanganan thinking.
- Apabila ada test cases di experiments/ yang masih pakai
  INSTRUCTION_PREFIX, JANGAN sentuh dulu — minta saya
  bersihkan manual.
```

**Verifikasi:**

1. Reload browser. Kirim pertanyaan "Halo, siapa kamu?"
2. Respons dalam Bahasa Indonesia, format rapi (sama seperti Module 04).
3. Buka DevTools → Network → cek body request: messages user **murni** (tanpa prefix).
4. Multi-turn masih bekerja.

---

## Validasi Akhir Section 1

- [ ] File `prompts.ts` dengan `ADVISOR_SYSTEM` ada.
- [ ] Route handler pakai parameter `system`, tidak lagi prefix.
- [ ] `INSTRUCTION_PREFIX` dari Module 04 sudah dihapus (atau dipindah).
- [ ] Test cases manual: respons konsisten dengan Module 04.

## Refleksi Section 1

1. Apakah ada perbedaan kualitas jawaban antara pre dan post migrasi?
2. Adakah edge case di mana prompt prefixing terasa lebih baik dari system?
3. Bagaimana Anda akan menjelaskan bedanya `system` vs prompt prefixing ke developer lain?

---

⬅️ Kembali: **[Module 04 — Multi-Turn](../Module-04-Content-Generation/latihan-6-multi-turn.md)** · ➡️ Lanjut: **[Section 2 — Sample Parameter & Output Control](./latihan-2-output-control.md)**
