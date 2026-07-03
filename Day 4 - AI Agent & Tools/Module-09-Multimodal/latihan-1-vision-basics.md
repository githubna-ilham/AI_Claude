# Section 1 — Vision API Basics: Script PoC

> Bagian dari **[Module 09 — Latihan](./latihan.md)**.

> Di section ini kita membuat **script terminal** yang membaca file foto kwitansi lokal, mengubahnya ke base64, mengirim ke Claude vision, dan mencetak deskripsi tekstual yang dikembalikan. Tujuannya: **buktikan API + encoding bekerja** sebelum membangun UI di Section 2 dan pipeline lengkap di Section 3. Dua prompt siap copy-paste.
>
> **Alur belajarnya**: siapkan sample foto kwitansi → tulis script test → jalankan → observasi output Claude.
>
> **Estimasi waktu**: 30–40 menit.

## Prasyarat Section 1

- [ ] `@anthropic-ai/sdk` terinstal dan `ANTHROPIC_API_KEY` aktif di `.env.local`.
- [ ] Anda punya **minimal 1 foto kwitansi** (struk supermarket / kafe / parkir / dll.) untuk dipakai sebagai bahan test. Foto sebaiknya jelas, tidak blur, ukuran < 5 MB.
- [ ] Anda sudah membaca bagian "Konsep Multimodal" + Section 1 di `materi.md`.

---

## 📚 Referensi Dokumentasi

- **[Anthropic Vision API](https://docs.claude.com/en/docs/build-with-claude/vision)** — anatomi content block image, format yang didukung, batasan ukuran.
- **[Anthropic SDK Messages reference](https://docs.claude.com/en/api/messages)** — pattern `messages.create` dengan multi-content array.
- **[Node fs.readFileSync](https://nodejs.org/api/fs.html#fsreadfilesyncpath-options)** — baca file lokal ke Buffer.

---

## Prompt 1 — Script `scripts/test-vision.ts`

### Walkthrough Manual

Sebelum kita kirim prompt ke Claude, mari pahami **alur** script: baca file lokal → encode base64 → kirim ke Claude vision → cetak respons. Tidak ada UI, tidak ada DB.

📂 **File baru**: `scripts/test-vision.ts` + (opsional) sample image di `scripts/sample-kwitansi.jpg`.

**1. Imports + init client**

📍 Lokasi: baris awal file.

```ts
// scripts/test-vision.ts
import Anthropic from "@anthropic-ai/sdk";
import { readFileSync } from "fs";
import { resolve } from "path";

const client = new Anthropic();
```

**2. Baca file lokal + encode base64**

📍 Lokasi: di dalam `main()`. Path foto dari argumen CLI, default `./scripts/sample-kwitansi.jpg`.

```ts
async function main() {
  const imagePath = resolve(process.argv[2] ?? "./scripts/sample-kwitansi.jpg");
  const imageData = readFileSync(imagePath).toString("base64");
  const mediaType =
    imagePath.endsWith(".png") ? "image/png" :
    imagePath.endsWith(".webp") ? "image/webp" :
    "image/jpeg";

  console.log(`📷 Memproses: ${imagePath}`);
  console.log(`   media_type: ${mediaType}, size: ${Math.round((imageData.length * 0.75) / 1024)} KB\n`);
  // ... API call
}
```

> 💡 **Kenapa `imageData.length * 0.75`?** Base64 encoding membuat file ~33% lebih besar dari original. Untuk perkiraan ukuran asli, kalikan length string dengan 0.75.

**3. Call Claude vision**

📍 Lokasi: lanjutan `main()`.

```ts
  const response = await client.messages.create({
    model: "claude-haiku-4-5",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: [
          {
            type: "image",
            source: { type: "base64", media_type: mediaType, data: imageData },
          },
          {
            type: "text",
            text: "Ini foto struk/kwitansi. Sebutkan: (1) nama merchant, (2) tanggal kalau terlihat, (3) total amount, (4) item-item yang terbaca beserta harganya. Format singkat, plain text.",
          },
        ],
      },
    ],
  });

  const textBlock = response.content.find((c) => c.type === "text");
  console.log("=== Respons Claude ===\n");
  console.log(textBlock?.text ?? "(tidak ada respons text)");
}
```

**4. Bootstrap + error handling**

📍 Lokasi: paling bawah file.

```ts
main().catch((err) => {
  console.error("Vision test error:", err);
  process.exit(1);
});
```

**5. Jalankan**

```bash
# Pakai default path
npx tsx --env-file=.env.local scripts/test-vision.ts

# Atau spesifik file
npx tsx --env-file=.env.local scripts/test-vision.ts ./path/ke/struk.jpg
```

### Yang sebaiknya tidak dilakukan

- ❌ Mengirim image langsung sebagai string text — `content` harus array dengan block `type: "image"`, bukan inline di prompt.
- ❌ Memakai model lama yang tidak support vision — gunakan `claude-haiku-4-5` / `claude-sonnet-4-6` / `claude-opus-4-7`.
- ❌ Mengirim file > 5 MB — Anthropic akan reject. Kompresi/resize dulu kalau perlu.
- ❌ Hardcode API key di script — selalu via `.env.local` dan `--env-file` argument tsx.
- ❌ Logging full base64 string — boros terminal + potensial PII.

### Verifikasi setelah file dibuat

1. File `scripts/test-vision.ts` ada.
2. Anda punya foto kwitansi di path yang Anda specify.
3. Run script tanpa error — output muncul di terminal.
4. **Claude bisa membaca**: minimal **total amount** dan **1 item** dari struk teridentifikasi dengan benar.
5. Output `media_type` dan `size KB` sesuai file Anda.

---

**Silakan salin prompt berikut, lalu paste ke Claude Code:**

```
Buat script PoC vision: baca file foto kwitansi lokal, encode
base64, kirim ke Claude vision, cetak deskripsi tekstual.

GOAL:
- Buat file baru scripts/test-vision.ts.
- Logic:
  1. Import Anthropic SDK, fs (readFileSync), path (resolve).
  2. const client = new Anthropic();
  3. main():
     a. Path image dari process.argv[2], default
        "./scripts/sample-kwitansi.jpg". Resolve absolute.
     b. Read file → base64 string via
        readFileSync(path).toString("base64").
     c. Detect media_type dari ekstensi (.png → image/png,
        .webp → image/webp, default image/jpeg).
     d. console.log path + media_type + size KB
        (perkiraan: base64.length * 0.75 / 1024).
     e. client.messages.create:
        - model: "claude-haiku-4-5"
        - max_tokens: 1024
        - messages: [{ role: "user", content: [image_block,
          text_block] }]
        - text_block: "Ini foto struk/kwitansi. Sebutkan:
          (1) nama merchant, (2) tanggal kalau terlihat,
          (3) total amount, (4) item-item yang terbaca beserta
          harganya. Format singkat, plain text."
     f. Extract text block dari response.content,
        console.log hasilnya dengan header "=== Respons
        Claude ===".
  4. main().catch(err => { console.error; process.exit(1); }).

- Jalankan dengan:
  npx tsx --env-file=.env.local scripts/test-vision.ts
  npx tsx --env-file=.env.local scripts/test-vision.ts ./path/ke/struk.jpg

CONTEXT:
- ANTHROPIC_API_KEY sudah ada di .env.local.
- Claude Haiku 4.5 mendukung vision (image input via base64).
- Format content block image:
  { type: "image", source: { type: "base64", media_type, data } }.

GUARDRAIL:
- JANGAN hardcode API key — pakai env var.
- JANGAN log full base64 string — cuma path + media_type + size.
- JANGAN pakai model lama (claude-3-5-haiku dan sebelumnya) —
  vision butuh Claude 4.x.
- JANGAN inline image sebagai string di text prompt — harus
  content block terpisah.
- Tambahkan type guard untuk text block (response.content.find
  (c => c.type === "text")).
```

**Verifikasi singkat:**

1. File `scripts/test-vision.ts` ada.
2. Run dengan foto kwitansi: output cetak path + size + respons Claude.
3. Claude **berhasil membaca** minimum total amount + 1 item dari struk.
4. Tidak ada error TypeScript / runtime.

---

## Prompt 2 — Eksperimen dengan Beberapa Foto + Variasi Prompt

### Walkthrough Manual

Sekarang Anda punya script kerja. Mari uji **batas akurasi vision** Claude dengan beberapa variasi: struk yang mudah (printout jelas), struk yang sulit (foto miring/blur), variasi text prompt.

📂 **Tidak ada file yang dimodifikasi** — eksperimen manual via terminal.

**1. Siapkan 3 foto dengan tingkat kesulitan berbeda**

- **A. Mudah**: struk supermarket cetak rapi, lurus, terang.
- **B. Sedang**: struk kafe yang agak kusut atau ada cahaya samping.
- **C. Sulit**: foto miring, ada bayangan, atau resolusi rendah.

**2. Jalankan script untuk masing-masing foto**

```bash
npx tsx --env-file=.env.local scripts/test-vision.ts ./struk-A.jpg
npx tsx --env-file=.env.local scripts/test-vision.ts ./struk-B.jpg
npx tsx --env-file=.env.local scripts/test-vision.ts ./struk-C.jpg
```

Untuk masing-masing, catat:
- Apakah total amount benar?
- Apakah jumlah item yang ter-identifikasi sesuai struk asli?
- Apakah ada salah angka (mis. 25.000 jadi 250.000)?
- Berapa lama latency?

**3. Coba variasi prompt**

Edit `text_block` di script dengan variasi berikut, jalankan ulang dengan foto B:

| Variasi prompt | Yang ingin diuji |
|---|---|
| `"Apa yang tertulis di foto ini?"` (generik) | Apakah Claude proaktif menyebut detail penting tanpa diminta? |
| `"Sebutkan SETIAP item beserta harga dalam format JSON."` | Apakah hasil JSON-formatted? Berguna untuk pre-processing. |
| `"Hanya sebut TOTAL AMOUNT saja. Satu angka."` | Apakah Claude disiplin tidak ber-narrasi? |
| `"Apakah ini struk kafe atau supermarket? Jawab 'kafe' atau 'supermarket'."` | Vision sebagai classifier sederhana. |

**4. Coba model lain (opsional)**

Edit `model` ke `claude-sonnet-4-6` untuk foto C (yang sulit). Bandingkan akurasi & latency vs Haiku.

### Yang sebaiknya tidak dilakukan

- ❌ Membuat script automation untuk semua variasi — eksplorasi manual lebih informatif untuk fase belajar.
- ❌ Mengirim foto sensitif (mengandung nomor kartu, KTP) — pakai struk biasa saja.
- ❌ Test 50+ foto — 3 cukup untuk merasakan karakteristik vision.

### Verifikasi setelah eksperimen

1. Untuk foto A (mudah): total amount + jumlah item **benar 100%**.
2. Untuk foto B (sedang): total amount benar, mungkin 1–2 item salah harga atau spelling.
3. Untuk foto C (sulit): mungkin total benar tapi banyak item missing — Anda **mendapat intuisi** kapan vision bisa diandalkan dan kapan tidak.
4. Eksperimen variasi prompt menunjukkan **prompt yang sangat spesifik menghasilkan output yang lebih predictable**.

---

**Silakan salin prompt berikut, lalu paste ke Claude Code:**

```
Bantu saya eksplorasi karakteristik vision Claude Haiku 4.5
dengan beberapa variasi foto dan prompt. Saya akan jalankan
script test-vision.ts (dari Prompt 1) manual; bantu menyusun
checklist observasi + diagnose kalau ada hasil yang mencurigakan.

GOAL:
- Beri saya panduan eksperimen 3 foto tingkat kesulitan
  berbeda:
  - A. Mudah (struk cetak rapi, terang).
  - B. Sedang (kusut atau cahaya samping).
  - C. Sulit (miring, blur, atau resolusi rendah).

- Untuk tiap foto, beri checklist observasi:
  - Total amount benar / salah / partial.
  - Jumlah item yang ter-identifikasi vs asli.
  - Ada angka yang salah magnitude (25rb vs 250rb)?
  - Latency (perkiraan kasar dari output terminal).

- Beri 4 variasi text prompt untuk uji disiplin output Claude:
  1. Prompt generik "Apa yang tertulis?"
  2. Prompt JSON-formatted output.
  3. Prompt singkat "Hanya total amount".
  4. Prompt classifier "kafe atau supermarket".

- Diagnose:
  (a) Vision sering salah angka → cek apakah foto bisa
      di-rotasi/crop di client sebelum upload.
  (b) Latency > 5 detik → cek size base64 (kompresi dulu).
  (c) Output text terlalu narasi panjang → perketat prompt.

CONTEXT:
- Script test-vision.ts dari Prompt 1 sudah ada.
- Saya akan menjalankan manual di terminal, bukan via Claude
  Code Bash tool (kecuali Anda minta jalankan single test
  untuk demo).

GUARDRAIL:
- JANGAN bikin script automation — manual eksplorasi cukup.
- JANGAN sertakan foto sensitif sebagai contoh.
- Format jawaban sebagai checklist + diagnostic guide markdown.
```

**Verifikasi singkat:**

1. Anda menerima dari Claude: checklist 3 foto + 4 variasi prompt + diagnostic guide.
2. Anda jalankan minimal 3 eksperimen.
3. Foto A menghasilkan output akurat; foto B & C menunjukkan keterbatasan vision yang Anda catat.
4. Variasi prompt menunjukkan trade-off generic vs specific.

---

## Validasi Akhir Section 1

Sebelum Anda lanjut ke Section 2, mari pastikan vision API + pipeline base64 sudah dipahami:

- [ ] File `scripts/test-vision.ts` ada dan jalan tanpa error.
- [ ] Claude vision **berhasil membaca** total amount + minimal 1 item dari foto kwitansi nyata.
- [ ] Anda sudah test minimal 2–3 foto dengan tingkat kesulitan berbeda.
- [ ] Anda paham trade-off model (Haiku cepat & murah vs Sonnet/Opus akurat untuk struk sulit).
- [ ] Anda paham `content` block image vs text — keduanya array yang dikirim bareng.
- [ ] Anda paham pattern base64: `readFileSync(path).toString("base64")` di server, `FileReader.readAsDataURL` di client (kita pakai di Section 2).

## Refleksi Section 1

Refleksikan pertanyaan berikut secara mendalam sebelum melanjutkan ke section berikutnya:

1. Saat foto sulit (blur/miring), Claude kadang **mengarang** angka yang masuk akal tapi salah. Bagaimana cara mendeteksi ini di production — apakah ada self-confidence score dari model, atau perlu validasi via heuristik (mis. cek apakah total = sum items)?
2. Eksperimen variasi prompt menunjukkan prompt spesifik = output lebih predictable. Bagaimana strategi prompt untuk parsing struk yang **bervariasi format** (struk supermarket vs receipt parkir vs tagihan listrik)? Apakah 1 prompt cukup, atau perlu klasifikasi dulu lalu prompt khusus per jenis?
3. Haiku cukup untuk struk cetak biasa. Tapi untuk **handwriting** (kuitansi tulisan tangan), kemungkinan butuh Sonnet/Opus. Bagaimana strategi memilih model dinamis berdasarkan jenis input — apakah klasifikasi dulu (vision cheap) lalu re-process dengan model lebih kuat?
4. Biaya per image ~$0.0003 (Haiku). Kalau 1000 user upload 5 struk/bulan = 5000 image = ~$1.5/bulan. Pada skala apa biaya vision jadi concern, dan apa strategi caching (mis. hash file → skip re-process kalau duplikat)?

---

⬅️ Kembali: **[Module 09 — Latihan](./latihan.md)** · 🏠 Index: **[Day 4](../README.md)** · ➡️ Lanjut: **[Section 2 — Upload UI + Base64 Pipeline](./latihan-2-upload-ui.md)**
