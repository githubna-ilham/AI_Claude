# Section 4 — Zero-shot & Few-shot Prompting

> Bagian dari **[Module 05 — Latihan](./latihan.md)**. Lanjutan dari **[Section 3 — Prompt Guides](./latihan-prompt-guides.md)**.

> Latihan menambahkan few-shot examples ke system prompt AI Advisor dan parser transaksi. Tiga prompt siap copy-paste.
>
> **Estimasi**: 40–50 menit.

## Prasyarat Section 4

- [ ] Section 1–3 selesai.

---

## Prompt 1 — Tambah Few-shot Examples ke Parser Transaksi

**Salin prompt berikut:**

```
Parser transaksi kadang salah label kategori. Tambahkan
few-shot examples untuk konsistensi.

GOAL:
- Modifikasi src/features/parse-transaction.ts.
- Sebelum panggil API, susun system instruction baru
  yang berisi:
  1. Instruksi singkat (sudah ada).
  2. Section "Contoh:" dengan 5-7 examples.

- Contoh-contoh yang harus disertakan:
  Input: "kemarin habis 35rb buat kopi"
  Output: { type: "expense", amount: 35000, category: "Food & Drink", description: "Kopi" }
  
  Input: "transfer 500rb ke ibu"
  Output: { type: "expense", amount: 500000, category: "Family", description: "Transfer ke ibu" }
  
  Input: "gajian 8 jt"
  Output: { type: "income", amount: 8000000, category: "Salary", description: "Gaji bulanan" }
  
  Input: "freelance dr klien dapet 1.5 jt"
  Output: { type: "income", amount: 1500000, category: "Freelance", description: "Freelance dari klien" }
  
  Input: "bayar internet indihome 350rb"
  Output: { type: "expense", amount: 350000, category: "Bills", description: "Internet Indihome" }

CONTEXT:
- File: parse-transaction.ts.
- Examples ditulis sebagai bagian dari system instruction
  (bukan messages array — itu untuk multi-turn).

GUARDRAIL:
- Pertahankan validasi Zod dan return type.
- Examples harus mewakili variasi: casual vs formal,
  income vs expense, kategori berbeda, format angka berbeda
  (rb, jt, ribu, juta).
- Setelah refactor, test dengan input baru yang TIDAK ada
  di examples — kategorisasi harus konsisten.
```

**Verifikasi:**

1. Coba parse input baru: "abis nongkrong di cafe 75rb".
2. Output: category seharusnya "Food & Drink" (konsisten dengan example).
3. Coba: "beli netflix langganan 60rb".
4. Output: category konsisten (mungkin "Entertainment" atau "Bills").

---

## Prompt 2 — Eksperimen Zero-shot vs Few-shot

**Salin prompt berikut:**

```
Saya ingin membandingkan akurasi zero-shot vs few-shot
secara terukur.

GOAL:
- Buat file experiments/shot-comparison.ts.
- Definisikan 10 test cases dengan input + expected
  category:
  - "habis grab 25rb" → Transport
  - "bayar listrik PLN 450rb" → Bills
  - "diskon shopee gajian 8jt" → Salary
  - "bonus tahunan 5 jt" → Income/Bonus
  - "ngopi di kanopi 50rb" → Food & Drink
  - "beli kucing scratching post 200rb" → Pet (atau Shopping)
  - "freelance video edit 800rb" → Freelance
  - "bayar BPJS 150rb" → Healthcare/Bills
  - "iuran RT 50rb" → Bills/Community
  - "investasi reksadana 1jt" → Investment

- Loop melalui test cases dengan 2 skenario:
  A: zero-shot (parser tanpa few-shot examples — versi lama)
  B: few-shot (parser dengan examples — versi baru)
- Hitung akurasi: berapa banyak yang category-nya match.

- Print perbandingan:
  Zero-shot: X/10 correct
  Few-shot:  Y/10 correct

CONTEXT:
- Untuk eksperimen ini, buat dua fungsi parse:
  parseZeroShot dan parseFewShot, masing-masing dengan
  system instruction yang berbeda.

GUARDRAIL:
- "Match" pakai matching fleksibel — case-insensitive, dan
  beberapa varian kategori dianggap correct (mis. "Food" /
  "Food & Drink" / "F&B").
- Print juga: pada test case mana kedua versi salah, dan
  pada mana hanya zero-shot yang salah.
```

**Verifikasi:**

1. Few-shot biasanya **lebih akurat** (mis. 8/10 vs 5/10).
2. Catat pola: kategori unik (Pet, Community) lebih sering benar di few-shot.

---

## Prompt 3 — Tambah Few-shot ke Advisor untuk Pertanyaan Ambigu

**Salin prompt berikut:**

```
ADVISOR_SYSTEM kadang bingung saat pertanyaan user singkat
atau ambigu. Tambahkan few-shot examples untuk pola respons
yang konsisten.

GOAL:
- Modifikasi ADVISOR_SYSTEM_V2 di prompts.ts.
- Tambahkan section "## Contoh Interaksi" di akhir prompt
  dengan 3 examples yang menggambarkan respons ideal:
  
  Example 1 — pertanyaan ambigu singkat:
    User: "tips dong"
    Assistant: "Apakah tips yang Anda maksud terkait
    menabung, mengelola anggaran, atau topik keuangan
    lain? Saya bantu sesuai kebutuhan."

  Example 2 — pertanyaan di luar topik:
    User: "Siapa presiden RI?"
    Assistant: "Saya AI Financial Advisor untuk Fin-App,
    jadi fokus saya keuangan personal Anda. Ada pertanyaan
    seputar pengelolaan keuangan yang bisa saya bantu?"

  Example 3 — pertanyaan teknis yang spesifik:
    User: "Strategi menabung untuk DP rumah 500 juta
    dalam 5 tahun."
    Assistant: "### Strategi Menabung Rp 500.000.000 dalam
    5 Tahun
    [3-4 poin konkret dengan angka]"

CONTEXT:
- Format contoh: "User: ... / Assistant: ...".
- Pertahankan section lainnya di ADVISOR_SYSTEM_V2.

GUARDRAIL:
- Examples harus pendek dan to-the-point — bukan template
  yang panjang.
- Setelah refactor, test:
  1. "tips" → should ask clarification (per Example 1).
  2. "Cuaca besok?" → should redirect (per Example 2).
  3. "Strategi pensiun 20 tahun lagi" → should give
     structured answer (per Example 3).
```

**Verifikasi:**

1. Test ketiga pola di chatbot.
2. Respons seharusnya mendekati gaya yang ada di contoh.

---

## Validasi Akhir Section 4

- [ ] Parser memiliki 5-7 few-shot examples.
- [ ] Eksperimen shot-comparison menunjukkan few-shot lebih akurat.
- [ ] Advisor system prompt memiliki section "Contoh Interaksi" dengan 3 examples.
- [ ] Test cases manual lolos.

## Refleksi Section 4

1. Untuk task apa Anda merasa few-shot **wajib**?
2. Untuk task apa zero-shot **sudah cukup**?
3. Berapa rata-rata peningkatan akurasi yang Anda observasi?

---

⬅️ Kembali: **[Section 3](./latihan-prompt-guides.md)** · ➡️ Lanjut: **[Section 5 — Role, Context, Instruction](./latihan-rci.md)**
