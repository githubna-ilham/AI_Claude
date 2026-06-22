# Section 5 — Role, Context, & Instruction

> Bagian dari **[Module 05 — Latihan](./latihan.md)**. Lanjutan dari **[Section 4 — Zero-shot & Few-shot Prompting](./latihan-few-shot.md)**.

> Latihan restrukturisasi system prompt dengan pola RCI dan demonstrasi reuse. Tiga prompt siap copy-paste.
>
> **Estimasi**: 35–45 menit.

## Prasyarat Section 5

- [ ] Section 1–4 selesai.

---

## Prompt 1 — Refactor `prompts.ts` ke Pola RCI

**Salin prompt berikut:**

```
Saya ingin merestrukturisasi system prompt dengan pola
Role-Context-Instruction yang modular.

GOAL:
- Refactor src/features/prompts.ts.
- Pecah ADVISOR_SYSTEM_V2 menjadi 4 konstanta terpisah:
  - ADVISOR_ROLE: persona Claude (1 paragraf).
  - ADVISOR_CONTEXT: konteks user dan domain (1-2 paragraf).
  - ADVISOR_FORMAT: aturan format output (list).
  - ADVISOR_INSTRUCTION: tugas dan batasan utama.

- Komposisi: ekspor ADVISOR_SYSTEM_V3 dengan template
  literal yang menggabungkan 4 konstanta + section
  "Contoh Interaksi" dari Section 4.

- Struktur final:
  # ROLE
  ${ADVISOR_ROLE}
  
  # CONTEXT
  ${ADVISOR_CONTEXT}
  
  # OUTPUT FORMAT
  ${ADVISOR_FORMAT}
  
  # INSTRUCTION
  ${ADVISOR_INSTRUCTION}
  
  # CONTOH INTERAKSI
  [examples dari Section 4]

- Update alias ADVISOR_SYSTEM = ADVISOR_SYSTEM_V3.

CONTEXT:
- Pertahankan ADVISOR_SYSTEM_V1 dan V2 untuk perbandingan.

GUARDRAIL:
- JANGAN ubah konten — hanya restrukturisasi.
- Test cases dari Section 3 harus tetap lolos.
- ADVISOR_ROLE jangan mengandung instruksi tugas (itu
  bagian INSTRUCTION).
- ADVISOR_CONTEXT jangan mengandung instruksi format
  (itu bagian FORMAT).
```

**Verifikasi:**

1. File prompts.ts memiliki konstanta terpisah: ADVISOR_ROLE, ADVISOR_CONTEXT, ADVISOR_FORMAT, ADVISOR_INSTRUCTION.
2. ADVISOR_SYSTEM_V3 menggabungkan keempatnya + examples.
3. Aplikasi pakai V3 (alias).
4. Run test cases dari Section 3 — semua lolos.

---

## Prompt 2 — Buat Varian Prompt: Insight Mingguan

**Salin prompt berikut:**

```
Demonstrasi keuntungan RCI: reuse role/context/format untuk
fitur lain.

GOAL:
- Di src/features/prompts.ts, tambahkan ekspor baru:
  INSIGHT_SYSTEM untuk fitur "Insight Mingguan".

- Struktur INSIGHT_SYSTEM:
  # ROLE
  ${ADVISOR_ROLE}                  ← reuse
  
  # CONTEXT
  ${ADVISOR_CONTEXT}               ← reuse
  
  # OUTPUT FORMAT
  ${ADVISOR_FORMAT}                ← reuse
  
  # INSTRUCTION
  ${INSIGHT_INSTRUCTION}           ← khusus

- INSIGHT_INSTRUCTION:
  "Berdasarkan data transaksi minggu ini yang akan diberikan
  user, berikan 3 insight penting tentang pola pengeluaran
  mereka. Format:
  
  ### Insight Minggu Ini
  
  1. **Insight 1**: [observasi konkret dengan angka]
  2. **Insight 2**: ...
  3. **Insight 3**: ...
  
  Akhiri dengan 1 saran actionable."

CONTEXT:
- File: prompts.ts.
- Ekspor: INSIGHT_SYSTEM, INSIGHT_INSTRUCTION.

GUARDRAIL:
- JANGAN duplikasi role/context/format — gunakan
  string interpolation untuk reuse.
- INSIGHT_INSTRUCTION harus standalone (tidak menyebut
  ADVISOR_INSTRUCTION).
```

**Verifikasi:**

1. File prompts.ts memiliki INSIGHT_SYSTEM yang reuse 3 konstanta dari ADVISOR.
2. File mengekspor: ADVISOR_SYSTEM, INSIGHT_SYSTEM, dan konstanta-konstanta penyusun.

---

## Prompt 3 — Server Action `getWeeklyInsight`

**Salin prompt berikut:**

```
Buat server action yang menggunakan INSIGHT_SYSTEM untuk
hasilkan insight dari data transaksi.

GOAL:
- Buat file baru src/features/insight.ts.
- Server action getWeeklyInsight(): Promise<string>.
- Logic:
  1. Query Supabase: ambil transaksi 7 hari terakhir.
     (Pakai pola createClient + select yang sudah ada di
     features/action.ts.)
  2. Format data ke string yang readable: misalnya
     daftar transaksi dengan tanggal, kategori, amount.
  3. Panggil Claude API:
     - system: INSIGHT_SYSTEM
     - messages: [{ role: "user", content: "Data transaksi
       saya minggu ini:\n\n" + formattedData }]
     - temperature: 0.5
     - max_tokens: 1024.
  4. Return text content.

CONTEXT:
- File "use server".
- Import INSIGHT_SYSTEM dari "@/features/prompts".
- Import createClient dari "@/lib/supabase/server".

GUARDRAIL:
- Apabila transaksi 7 hari terakhir kosong, return string
  "Belum ada transaksi minggu ini. Mulai catat untuk
  dapat insight." (TANPA panggil API — hemat).
- JANGAN ubah prompts.ts — sudah selesai di prompt 2.
- Apabila Claude response.content[0].type !== "text", throw
  error.
```

**Verifikasi:**

1. Test cepat dari `experiments/test-insight.ts`:
   ```ts
   const result = await getWeeklyInsight();
   console.log(result);
   ```
2. Output berupa string markdown dengan 3 insight + 1 saran.
3. (Opsional) Tambahkan tombol di dashboard untuk trigger insight ini — biarkan saya yang minta di section terpisah.

---

## Validasi Akhir Section 5

- [ ] Konstanta ROLE, CONTEXT, FORMAT, INSTRUCTION ada terpisah.
- [ ] ADVISOR_SYSTEM_V3 dan INSIGHT_SYSTEM komposisi modular.
- [ ] Server action `getWeeklyInsight` ada dan return insight string.
- [ ] Tidak ada regresi: chatbot tetap berfungsi dengan V3.

## Refleksi Section 5

1. Apakah refactor RCI lebih mudah di-iterasi vs prompt monolitik?
2. Apa keuntungan praktis dari komposisi modular yang Anda rasakan?
3. Apakah Anda akan menambah lapis lain selain RCI? (Mis. Examples, Guardrails)

---

⬅️ Kembali: **[Section 4](./latihan-few-shot.md)** · ➡️ Lanjut: **[Section 6 — Agentic Workflow](./latihan-agentic.md)**
