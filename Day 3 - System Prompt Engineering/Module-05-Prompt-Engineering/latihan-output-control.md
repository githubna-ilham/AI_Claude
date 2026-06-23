# Section 2 — Sample Parameter & Output Control

> Bagian dari **[Module 05 — Latihan](./latihan.md)**. Lanjutan dari **[Section 1 — System Instruction](./latihan-system-instruction.md)**.

> Latihan eksplorasi parameter sampling dan teknik structured output. Empat prompt siap copy-paste.
>
> **Estimasi**: 45–60 menit.

## Prasyarat Section 2

- [ ] Section 1 selesai. AI Advisor pakai parameter `system`.

---

## Prompt 1 — Eksperimen `top_p` vs `temperature`

**Salin prompt berikut:**

```
Bantu saya memahami beda top_p dan temperature.

GOAL:
- Buat file experiments/sampling-test.ts.
- Pertanyaan: "Berikan 3 ide nama unik untuk celengan
  digital saya."
- Jalankan 4 kombinasi:
  A: temperature=0.0, top_p tidak diset
  B: temperature=0.5, top_p tidak diset
  C: temperature tidak diset (default 1.0), top_p=0.5
  D: temperature tidak diset (default 1.0), top_p=0.9

- Untuk setiap kombinasi, jalankan 2 kali dan print hasil.
- Format output:
  --- A: temp=0, top_p=default ---
  Run 1: <hasil>
  Run 2: <hasil>
  ---

CONTEXT:
- Pakai Anthropic SDK langsung.
- Model: claude-haiku-4-5.
- max_tokens: 200.
- Boleh pakai system: ADVISOR_SYSTEM.

GUARDRAIL:
- JANGAN set temperature dan top_p bersamaan (anti-pattern
  per dokumentasi Anthropic).
- Catat observasi: pada setting mana hasilnya paling variatif?
  Paling konsisten?
```

**Verifikasi:**

1. Jalankan file.
2. Bandingkan output A vs D. A seharusnya konsisten antara Run 1 dan 2; D paling variatif.

---

## Prompt 2 — `stop_sequences` untuk Format Terkontrol

**Salin prompt berikut:**

```
Saya ingin Claude menghasilkan output yang berhenti di
penanda tertentu.

GOAL:
- Buat file experiments/stop-sequences-test.ts.
- Minta Claude menghasilkan ringkasan finansial dengan
  format:
  
  RINGKASAN:
  <ringkasan singkat>
  
  REKOMENDASI:
  <rekomendasi>
  
  ---END---

- Tambahkan stop_sequences: ["---END---"].
- Print hasil + stop_reason.
- Bandingkan: dengan dan tanpa stop_sequences.

CONTEXT:
- User message contoh: "Bulan ini income Rp 8.000.000,
  expense Rp 6.500.000. Berikan ringkasan keuangan saya."
- Pakai system ADVISOR_SYSTEM.

GUARDRAIL:
- Tanpa stop_sequences: Claude mungkin terus menulis setelah
  ---END---. Dengan stop_sequences, berhenti tepat di sana.
- Print stop_reason: dengan stop_sequences = "stop_sequence";
  tanpa = "end_turn".
```

**Verifikasi:**

1. Dengan stop_sequences: output berhenti di ---END---, stop_reason = "stop_sequence".
2. Tanpa: output mungkin lanjut bercerita, stop_reason = "end_turn".

---

## Prompt 3 — Structured Output: Parse Transaksi dari Teks Natural

**Salin prompt berikut:**

```
Saya ingin Claude mengekstrak data terstruktur dari pesan
casual user.

GOAL:
- Buat server action src/features/parse-transaction.ts.
- Function parseTransaction(userText: string): Promise<{
    type: "income" | "expense";
    amount: number;
    category: string;
    description: string;
  }>

- Gunakan Claude API dengan setting:
  - model: claude-haiku-4-5
  - temperature: 0.0 (deterministik)
  - system: instruksi singkat untuk parse ke JSON
  - User message: "Parse transaksi dari teks berikut: {text}"

- System instruction:
  "Anda parser. Ekstrak data transaksi dari teks user dan
  return JSON dengan struktur:
  { type: 'income' | 'expense', amount: number, category:
  string, description: string }
  Output WAJIB JSON valid, tidak ada teks lain."

- Validasi output dengan Zod schema.
- Return parsed object.

CONTEXT:
- Pakai Anthropic SDK dengan parameter system.
- Pakai zod yang sudah ter-install (kalau belum: npm install zod).
- Contoh input: "kemarin saya beli kopi 35rb di starbucks"
- Expected output: { type: "expense", amount: 35000, category:
  "Food & Drink", description: "Kopi di Starbucks" }.

GUARDRAIL:
- Apabila JSON tidak valid, throw error dengan pesan jelas.
- Apabila amount tidak ditemukan, throw error.
- File ini "use server".
```

**Verifikasi:**

1. Test cepat:
   ```ts
   // experiments/test-parser.ts
   const result = await parseTransaction("habis grab ke kantor 25 ribu");
   console.log(result);
   // Expected: { type: "expense", amount: 25000, category: "Transport"/"Transportation", description: "Grab ke kantor" }
   ```
2. Coba berbagai input casual: "gajian 5jt", "beli baju 200rb", "freelance 1.5jt".

---

## Prompt 4 — Integrasikan Parser ke UI

**Salin prompt berikut:**

```
Sekarang sambungkan parser ke UI Transactions agar user
bisa input dengan natural language.

GOAL:
- Di halaman /transactions, tambahkan tombol "✨ Quick Add
  (AI)" di samping tombol "+ Add transaction" yang sudah
  ada.
- Klik tombol → buka dialog kecil dengan:
  - Textarea: "Ketik transaksi natural language Anda..."
  - Tombol "Parse & Add"
- Saat di-klik:
  1. Tampilkan loading state.
  2. Panggil parseTransaction(text).
  3. Hasil parse di-preview di bawah textarea: type, amount,
     category, description.
  4. Tombol "Confirm Add" dan "Edit Manual".
  5. Klik Confirm → panggil createTransaction (yang sudah ada
     dari Module 02).

CONTEXT:
- Dialog dan komponen Shadcn sudah ter-install dari modul
  sebelumnya.
- Pakai useMutation untuk parseTransaction dan
  createTransaction.

GUARDRAIL:
- Apabila parsing gagal, tampilkan pesan error inline (bukan
  toast).
- Tombol "Edit Manual" → tutup dialog dan buka dialog Add
  Transaction biasa dengan field yang sudah pre-filled.
- JANGAN langsung create tanpa konfirmasi user — selalu
  preview dulu.
```

**Verifikasi:**

1. Klik "Quick Add (AI)" → dialog terbuka.
2. Ketik "beli sepatu lari 850 ribu" → klik Parse.
3. Preview menunjukkan: type=expense, amount=850000, category=Shopping/Sports, description="Sepatu lari".
4. Confirm → transaksi masuk ke tabel.

---

## Validasi Akhir Section 2

- [ ] File eksperimen sampling-test dan stop-sequences-test jalan.
- [ ] Server action `parseTransaction` ada di `src/features/parse-transaction.ts`.
- [ ] Validasi output JSON dengan Zod schema.
- [ ] Halaman Transactions punya tombol "Quick Add (AI)" yang berfungsi.
- [ ] Tidak ada regresi dari Section 1.

## Refleksi Section 2

1. Pada parameter mana Anda merasa **kontrol paling kuat**?
2. Apakah parser AI lebih cepat dari mengisi form manual?
3. Berapa kali parser memberikan hasil yang **salah**? Apa pattern kesalahannya?

---

⬅️ Kembali: **[Section 1](./latihan-system-instruction.md)** · ➡️ Lanjut: **[Section 3 — Role, Context, Instruction](./latihan-rci.md)**
