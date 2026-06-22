# Module 05 — Latihan

> Module ini terdiri dari **6 section** yang membangun teknik prompt engineering di atas AI Financial Advisor dari Module 04. **Kode dari section sebelumnya akan digunakan dan diperluas di section berikutnya** — bukan ditulis ulang.
>
> Total estimasi seluruh section: ±5–6 jam efektif.

## Prinsip Kontinuitas (Wajib Diperhatikan)

- ✅ **Lanjutkan kode yang sudah ada**. Setiap prompt secara eksplisit menyebut file mana yang akan diperluas.
- ❌ **Jangan hapus** komponen yang sudah jadi di section sebelumnya, kecuali Claude / latihan secara eksplisit memintanya.
- ✅ **Verifikasi setelah setiap prompt** — pastikan section sebelumnya tidak rusak sebelum lanjut.

---

# Section 1 — System Instruction

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

# Section 2 — Sample Parameter & Output Control

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

# Section 3 — Prompt Guides

> Latihan untuk merefactor system prompt AI Advisor sesuai best practice. Tiga prompt siap copy-paste.
>
> **Estimasi**: 30–40 menit.

## Prasyarat Section 3

- [ ] Section 1 + 2 selesai.

---

## Prompt 1 — Audit System Prompt yang Ada

**Salin prompt berikut:**

```
Saya ingin Anda mengaudit ADVISOR_SYSTEM di
src/features/prompts.ts.

GOAL:
- Baca isi ADVISOR_SYSTEM.
- Lakukan audit menggunakan 7 prinsip prompt yang baik:
  1. Spesifik vs abstrak
  2. Eksplisit vs implisit
  3. Ada contoh konkret?
  4. Larangan eksplisit
  5. Strukturkan dengan heading/list?
  6. Persona dipisah dari instruksi tugas?
  7. Apakah ada anti-pattern?

- Berikan output dalam bentuk:
  - Tabel: prinsip | nilai (✅/⚠️/❌) | catatan
  - Daftar perbaikan yang disarankan, prioritas tinggi ke
    rendah.

CONTEXT:
- File: src/features/prompts.ts.
- JANGAN modifikasi prompt-nya dulu — hanya audit di tahap
  ini.

GUARDRAIL:
- Audit harus jujur, jangan basa-basi.
- Berikan saran yang konkret (mis. "tambah contoh X di
  bagian Y"), bukan abstrak.
```

**Verifikasi:**

1. Claude menampilkan tabel audit dengan minimal 1 ⚠️ atau ❌.
2. Daftar perbaikan ada minimum 3 items.

---

## Prompt 2 — Iterasi Perbaikan Prompt

**Salin prompt berikut:**

```
Berdasarkan audit di Prompt 1, perbaiki ADVISOR_SYSTEM.

GOAL:
- Refactor src/features/prompts.ts.
- Terapkan 3-5 perbaikan prioritas tinggi dari audit
  sebelumnya.
- Pertahankan ekspor ADVISOR_SYSTEM (jangan rename).

CONTEXT:
- Hasil refactor harus mengikuti 7 prinsip:
  - Heading markdown jelas (## Persona, ## Lingkup, dst.)
  - Konkret, bukan abstrak
  - Larangan eksplisit dengan "JANGAN/HINDARI"
  - Format yang dapat dideteksi mata (Rupiah, %, dst dengan
    contoh)

GUARDRAIL:
- Setelah refactor, jalankan test cases manual berikut:
  1. "Halo, siapa kamu?" → respons identitas yang jelas.
  2. "Tips menabung untuk pemula?" → markdown rapi + list.
  3. "Berapa harga saham GOTO besok?" → menolak sopan +
     redirect.
  4. "Ringkasan pengeluaran saya bulan ini." → mengakui ia
     belum punya data (akan ditangani di Section 6).
  
- Apabila ada test gagal, iterasi lagi prompt-nya.
```

**Verifikasi:**

1. Run semua 4 test cases di chatbot.
2. Catat: berapa banyak yang langsung lolos, berapa yang butuh iterasi prompt tambahan.

---

## Prompt 3 — Versi Prompt dan A/B Test Manual

**Salin prompt berikut:**

```
Saya ingin mempertahankan versi lama untuk perbandingan
manual.

GOAL:
- Di src/features/prompts.ts, ekspor 2 versi:
  - ADVISOR_SYSTEM_V1 (versi dari Section 1)
  - ADVISOR_SYSTEM_V2 (versi yang baru di-refactor)
- ADVISOR_SYSTEM tetap diekspor sebagai alias ke V2 (yang
  aktif dipakai).
- Tambahkan komentar JSDoc di atas masing-masing yang
  menjelaskan kapan dipakai.

CONTEXT:
- File: prompts.ts.
- V1 berguna untuk perbandingan dan rollback cepat.

GUARDRAIL:
- JANGAN ubah route.ts atau parse-transaction.ts —
  ADVISOR_SYSTEM (alias V2) yang dipakai di sana.
- Versi V1 hanya untuk perbandingan, tidak dipakai
  production.
```

**Verifikasi:**

1. File prompts.ts memiliki V1, V2, dan alias.
2. Aplikasi tetap pakai V2 (yang refactor).
3. Anda dapat sewaktu-waktu switch ke V1 untuk perbandingan dengan ganti `ADVISOR_SYSTEM = ADVISOR_SYSTEM_V1`.

---

## Validasi Akhir Section 3

- [ ] System prompt sudah di-audit dan di-refactor.
- [ ] V1 dan V2 keduanya ada di file.
- [ ] Test cases lolos dengan V2.
- [ ] Tidak ada regresi.

## Refleksi Section 3

1. Anti-pattern mana yang ternyata ada di V1?
2. Apakah V2 menghasilkan respons yang **berbeda kualitas** dari V1?
3. Apakah V2 lebih ringkas atau lebih panjang dari V1?

---

# Section 4 — Zero-shot & Few-shot Prompting

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

# Section 5 — Role, Context, & Instruction

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

# Section 6 — Agentic Workflow

> Latihan untuk memberi AI Advisor kemampuan **memanggil tool** — membaca data transaksi user dari Supabase saat dibutuhkan. Empat prompt siap copy-paste.
>
> **Estimasi**: 60–75 menit (paling teknis di Module 05).

## Prasyarat Section 6

- [ ] Section 1–5 selesai.
- [ ] Module 02 (Transactions CRUD) selesai — data transaksi ada di Supabase.

---

## Prompt 1 — Definisikan Tools untuk Claude

**Salin prompt berikut:**

```
Saya ingin mendefinisikan tools yang dapat dipanggil Claude
untuk membaca data transaksi user.

GOAL:
- Buat file baru src/features/tools.ts.
- Ekspor konstanta TOOLS_DEFINITION: array berisi 2 tool:

  1. get_transactions
     - description: "Ambil daftar transaksi user dengan
       filter opsional. Gunakan saat user bertanya tentang
       transaksi spesifik atau analisis pola pengeluaran."
     - input_schema dengan properties:
       - category: string (optional, "Filter by category
         name, e.g. 'Food', 'Transport'")
       - start_date: string (optional, "YYYY-MM-DD")
       - end_date: string (optional, "YYYY-MM-DD")
       - type: enum["income", "expense"] (optional)
       - limit: number (optional, default 50)

  2. get_balance_summary
     - description: "Ambil ringkasan saldo, total income,
       dan total expense user (all-time). Gunakan saat
       user bertanya tentang kondisi keuangan secara umum."
     - input_schema: object kosong (tidak ada parameter).

- Ekspor TOOL_NAMES sebagai const enum/union untuk type
  safety: "get_transactions" | "get_balance_summary".

CONTEXT:
- Struktur tool definition mengikuti Anthropic SDK:
  { name, description, input_schema (JSON Schema) }.
- File: src/features/tools.ts.

GUARDRAIL:
- Description harus PRESCRIPTIVE — beri tahu Claude KAPAN
  pakai tool.
- Property descriptions juga harus jelas.
- JANGAN tambahkan tool yang bisa MENGUBAH data (create,
  update, delete) — Section 6 hanya read-only.
```

**Verifikasi:**

1. File `tools.ts` ada dengan ekspor `TOOLS_DEFINITION`.
2. TypeScript tidak error.

---

## Prompt 2 — Implementasi Eksekutor Tool

**Salin prompt berikut:**

```
Sekarang buat function yang mengeksekusi tool ketika Claude
memutuskan memanggilnya.

GOAL:
- Di src/features/tools.ts, tambah function:
  executeTool(name: string, input: any): Promise<string>

- Logic switch berdasarkan name:
  case "get_transactions":
    - Validasi input dengan Zod (category, start_date,
      end_date, type, limit semua optional).
    - Query Supabase: select * from transactions dengan
      filter yang sesuai.
    - Format hasil sebagai JSON string (Claude expects
      string, bukan object).
    - Return JSON string.
  
  case "get_balance_summary":
    - Reuse getBalanceSummary dari Module 02.
    - Format hasil sebagai JSON string.
    - Return JSON string.
  
  default:
    - Throw error "Unknown tool: ${name}"

CONTEXT:
- Import createClient dari "@/lib/supabase/server".
- Import getBalanceSummary dari "@/features/action".
- Pakai zod untuk validasi input.

GUARDRAIL:
- Apabila Supabase error, return JSON string dengan field
  error: { error: "Tidak dapat ambil data transaksi" }.
  JANGAN throw — biarkan Claude tahu tool gagal dan dia
  bisa merespons gracefully.
- Limit default 50, max 200 (cegah Claude minta semua data
  yang bisa boros token).
- File ini "use server".
```

**Verifikasi:**

1. Test cepat dari `experiments/test-tool.ts`:
   ```ts
   const r1 = await executeTool("get_transactions", { category: "Food", limit: 5 });
   console.log(r1);
   const r2 = await executeTool("get_balance_summary", {});
   console.log(r2);
   ```
2. Output adalah JSON string yang dapat di-parse.

---

## Prompt 3 — Integrasikan Tool Use ke Route Handler

**Salin prompt berikut:**

```
Sekarang sambungkan tool use ke route handler chatbot agar
Claude bisa memanggil tool saat dibutuhkan.

GOAL:
- Modifikasi src/app/api/advisor/route.ts.
- Tambahkan parameter tools: TOOLS_DEFINITION ke
  client.messages.stream() / create().
- Implementasi loop tool use:
  1. Panggil Claude.
  2. Iterasi response content blocks:
     - Apabila ada block type "tool_use", eksekusi tool
       via executeTool(name, input).
     - Push hasil ke array tool_results.
  3. Apabila ada tool_use, recurse: panggil ulang Claude
     dengan messages baru:
     ```
     messages = [
       ...originalMessages,
       { role: "assistant", content: response.content },
       { role: "user", content: tool_results }
     ]
     ```
  4. Loop maksimum 5 iterasi (safety).
  5. Apabila tidak ada tool_use, stream text content ke
     client seperti biasa.

- Pertahankan: streaming, thinking, system prompt RCI.

CONTEXT:
- Pakai client.messages.create() untuk loop tool use
  (lebih sederhana dari streaming saat tool calls).
- HANYA stream text content ke client di iterasi terakhir.

GUARDRAIL:
- Apabila iterasi mencapai 5, hentikan dan kirim pesan
  "Maaf, terlalu banyak step. Coba pertanyaan yang lebih
  spesifik."
- Apabila executeTool throw, lanjut dengan error message
  ke Claude — JANGAN crash.
- JANGAN ubah behaviour saat tidak ada tool_use (pertahankan
  streaming Module 04 Section 6).
```

**Verifikasi:**

1. Reload browser.
2. Kirim: "Berapa total expense food saya?"
3. Di console server (terminal `npm run dev`), seharusnya terlihat log Claude memanggil `get_transactions` dengan category="Food".
4. Respons di chatbot menampilkan **angka aktual** dari Supabase.

---

## Prompt 4 — Indikator UI Saat Tool Dipanggil

**Salin prompt berikut:**

```
Tambahkan UX feedback saat Claude memanggil tool, agar user
paham kenapa respons lebih lama.

GOAL:
- Modifikasi route.ts: kirim event khusus ke client saat
  tool_use terjadi. Pakai prefix marker:
  [[TOOL_CALL:get_transactions]]
  
  Setelah tool selesai, kirim:
  [[TOOL_DONE]]

- Modifikasi ai-chat-panel.tsx: parse marker dan tampilkan
  indikator di UI:
  - Saat tool_use detected, tampilkan bubble system kecil:
    "🔍 Membaca data transaksi Anda..."
  - Saat tool_done, ganti dengan ikon ✓ dan teks fade out.
- Bubble tool indicator: berbeda visual dari user/assistant
  (bg-muted, text-sm, italic).

CONTEXT:
- Pertahankan parsing thinking_delta dari Module 04 Section 6.

GUARDRAIL:
- Tool indicator hanya tampil saat ada tool call — tidak
  ganggu percakapan normal.
- Apabila ada multiple tool calls dalam satu turn, tampilkan
  semua indicator.
- JANGAN ubah message state untuk indicator — pakai state
  terpisah toolStatus: { name: string; status: "pending" |
  "done" } | null.
```

**Verifikasi:**

1. Kirim pertanyaan yang trigger tool: "Bagaimana keuangan saya?"
2. Indikator muncul: "🔍 Membaca data transaksi Anda...".
3. Setelah selesai, indikator hilang dan jawaban muncul.
4. Pertanyaan tanpa tool ("Halo, siapa kamu?") tidak menampilkan indikator.

---

## Validasi Akhir Section 6 (Akhir Module 05)

- [ ] File `tools.ts` dengan `TOOLS_DEFINITION` dan `executeTool`.
- [ ] Route handler memanggil tool dengan loop maks 5 iterasi.
- [ ] Indikator UI muncul saat tool dipanggil.
- [ ] Pertanyaan "Berapa total expense food saya?" dijawab dengan angka aktual.
- [ ] Pertanyaan tanpa tool tetap respons cepat tanpa indicator.
- [ ] Tidak ada regresi: thinking, streaming, multi-turn semua bekerja.

## Refleksi Section 6

1. Bagaimana akurasi Claude memilih tool yang tepat?
2. Pernah Claude memanggil tool yang tidak perlu? (Mis. pakai `get_transactions` untuk pertanyaan persona)
3. Apa pengalaman UX dari tool indicator?
4. Apabila menambah tool create/update/delete, apa safeguard yang Anda butuhkan?

---

## 🎉 Validasi Akhir Module 05

Setelah seluruh 6 section selesai, AI Financial Advisor Anda sudah:

- [ ] **System instruction** yang terstruktur dengan pola RCI.
- [ ] **Parameter generation** terkontrol (temperature, top_p, stop_sequences).
- [ ] **Few-shot examples** untuk konsistensi format.
- [ ] **Komposisi modular** prompt yang reusable.
- [ ] **Tool use** untuk akses data transaksi nyata.
- [ ] **Parser transaksi** dari teks natural di halaman Transactions.
- [ ] **Fitur Insight Mingguan** sebagai server action siap dipanggil.
- [ ] **Tidak ada regresi** pada Dashboard / Transactions / Chatbot dari Module 04.

Apabila seluruh checklist tercapai, AI Financial Advisor Anda sudah jauh dari sekadar chatbot — ia adalah **asisten cerdas** yang memahami data Anda, merespons dengan format konsisten, dan dapat di-extend untuk fitur baru dengan mudah.
