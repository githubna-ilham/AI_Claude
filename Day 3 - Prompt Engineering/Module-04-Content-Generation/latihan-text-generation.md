# Section 2 — Text Generation

> Bagian dari **[Module 04 — Latihan](./latihan.md)**. Lanjutan dari **[Section 1](./latihan-integrasi-api.md)**.

> Latihan untuk mengeksplorasi parameter generation Claude API: `max_tokens`, `temperature`, `stop_sequences` — serta pola **prompt prefixing** untuk mengarahkan format output tanpa system instruction. Empat prompt siap copy-paste.
>
> **Estimasi Section 2**: 35–45 menit.

> 📌 **Catatan**: Module 04 sengaja **belum menggunakan parameter `system`**. Format dan persona dikontrol murni lewat user message + parameter generation. System instruction adalah topik tersendiri.

## Prasyarat Section 2

- [ ] Section 1 selesai (+ Latihan UI Module 03). Chatbot dapat menerima pertanyaan dan menampilkan respons asli dari Claude.
- [ ] Anda sudah membaca bagian Section 2 di `materi.md`.

---

## Prompt 1 — Tambah Parameter `temperature` ke `askAdvisor`

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

⬅️ Kembali: **[Section 1](./latihan-integrasi-api.md)** · ➡️ Lanjut: **[Section 3 — Thinking / Thought](./latihan-thinking.md)**
