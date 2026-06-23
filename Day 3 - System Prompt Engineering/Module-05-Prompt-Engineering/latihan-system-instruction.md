# Section 1 — System Instruction

> Bagian dari **[Module 05 — Latihan](./latihan.md)**. Lanjutan dari **[Module 04 — Section 6: Multi-Turn](../Module-04-Content-Generation/latihan-6-multi-turn.md)**.

> Latihan untuk bermigrasi dari **prompt prefixing** (Module 04) ke **parameter `system`**. Tiga prompt siap copy-paste.
>
> **Estimasi**: 30–40 menit.

## Prasyarat Section 1

- [ ] Module 04 selesai. AI Advisor pakai prompt prefixing dan dapat multi-turn.
- [ ] Anda sudah membaca bagian Section 1 di `materi.md`.

---

## Prompt 1 — Buat File `prompts.ts` dengan System Instruction

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

## Prompt 3 — Bandingkan Token Usage Sebelum vs Sesudah

**Salin prompt berikut:**

```
Saya ingin tahu seberapa hemat token dengan migrasi ini.

GOAL:
- Buat file baru experiments/token-comparison.ts.
- Jalankan 2 skenario dengan pertanyaan yang sama (mis.
  "Tips menabung untuk DP rumah dalam 5 tahun"):
  
  Skenario A (gaya Module 04 - prefixing):
  - Tidak pakai parameter system.
  - Messages berisi INSTRUCTION_PREFIX + question.
  
  Skenario B (gaya Module 05 - system):
  - Pakai parameter system: ADVISOR_SYSTEM.
  - Messages berisi question saja.

- Print untuk masing-masing:
  - input_tokens
  - output_tokens
  - Total biaya estimasi.

- Simulasikan percakapan 5 turn (kirim 5 kali) untuk Skenario
  A dan B — hitung total tokens di seluruh percakapan.

CONTEXT:
- Pakai Anthropic SDK langsung di file ini.
- Model: claude-haiku-4-5.
- Pertanyaan bisa hardcode atau loop melalui array.

GUARDRAIL:
- JANGAN modifikasi route.ts atau prompts.ts.
- Print perbandingan dengan format tabel ASCII yang clear.
```

**Verifikasi:**

1. Jalankan: `npx tsx --env-file=.env.local experiments/token-comparison.ts`.
2. Output menunjukkan: Skenario B (system) menggunakan **lebih sedikit token total** di percakapan 5-turn.
3. Catat persentase penghematan — biasanya 15-30%.

---

## Validasi Akhir Section 1

- [ ] File `prompts.ts` dengan `ADVISOR_SYSTEM` ada.
- [ ] Route handler pakai parameter `system`, tidak lagi prefix.
- [ ] `INSTRUCTION_PREFIX` dari Module 04 sudah dihapus (atau dipindah).
- [ ] Test cases manual: respons konsisten dengan Module 04.
- [ ] Token usage perbandingan menunjukkan penghematan signifikan.

## Refleksi Section 1

1. Berapa persen penghematan token yang Anda dapat?
2. Apakah ada perbedaan kualitas jawaban antara pre dan post migrasi?
3. Adakah edge case di mana prompt prefixing terasa lebih baik dari system?

---

⬅️ Kembali: **[Module 04 — Multi-Turn](../Module-04-Content-Generation/latihan-6-multi-turn.md)** · ➡️ Lanjut: **[Section 2 — Sample Parameter & Output Control](./latihan-output-control.md)**
