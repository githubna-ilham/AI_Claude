# Section 1 — Implementasi Embedding

> Bagian dari **[Module 06 — Latihan](./latihan.md)**. Lanjutan dari **[Konsep Embedding (Pendahuluan)](./materi.md#konsep-embedding-pendahuluan)**.

> Latihan untuk **setup Voyage AI** + bangun function `embed()` reusable + verifikasi semantic similarity. Tiga prompt siap copy-paste.
>
> **Estimasi**: 50–60 menit.

## Prasyarat Section 1

- [ ] Bagian "Konsep Embedding (Pendahuluan)" di `materi.md` sudah dibaca dan dipahami.
- [ ] Anda sudah membaca bagian Section 1 di `materi.md`.
- [ ] Akun Voyage AI sudah dibuat, API key sudah didapat ([voyageai.com](https://www.voyageai.com/)).

---

## 📚 Referensi Dokumentasi

Buka tab dokumentasi berikut sebagai referensi cepat selama Section 1:

- **[Voyage AI SDK reference](https://docs.voyageai.com/docs/api-reference)** — fungsi `client.embed()`, parameter `model`, `input_type`, struktur response.
- **[voyage-3 model spec](https://docs.voyageai.com/docs/embeddings)** — 1024-dim, max input length, harga per token.
- **[Voyage AI TypeScript SDK install](https://docs.voyageai.com/docs/install)** — npm package `voyageai`.
- **[Caching strategies for embeddings](https://docs.voyageai.com/docs/embeddings)** — hash content untuk hindari re-embed (akan dipakai di module RAG lanjutan).

---

## Prompt 1 — Install Voyage AI SDK + Setup API Key

### Walkthrough Manual

Sebelum copy-paste prompt ke Claude, pahami perubahan kecil yang akan terjadi di `package.json`, `.env.local`, dan `.env.example`, plus satu file ping untuk konfirmasi koneksi.

📂 **File yang diubah**: `package.json` + `.env.local` + `.env.example`
📂 **File baru**: `experiments/voyage-ping.ts`

**1. Install package `voyageai`**

📍 Lokasi: terminal di root project.

```bash
npm install voyageai
```

Verifikasi `package.json` punya `"voyageai"` di **`dependencies`** (bukan `devDependencies`).

**2. Tambah API key ke `.env.local`**

📍 Lokasi: `.env.local` di root project. Tambah baris baru di akhir file.

```bash
# .env.local — server-only, JANGAN commit
VOYAGE_API_KEY="pa-..." # isi dari https://dash.voyageai.com/
```

**3. Tambah placeholder ke `.env.example`**

📍 Lokasi: `.env.example` di root project. Tambah placeholder kosong agar developer lain tahu env var ini dibutuhkan.

```bash
# .env.example — committed
VOYAGE_API_KEY=""
```

**4. Buat `experiments/voyage-ping.ts`**

📍 Lokasi: folder `experiments/` (sandbox). Tujuan: konfirmasi koneksi + dimensi vektor.

```ts
// experiments/voyage-ping.ts
import { VoyageAIClient } from "voyageai";

async function main() {
  const client = new VoyageAIClient({ apiKey: process.env.VOYAGE_API_KEY });
  const result = await client.embed({ input: ["hello world"], model: "voyage-3" });
  const vec = result.data[0].embedding;
  console.log("dim:", vec.length);
  console.log("preview:", vec.slice(0, 3));
}

main().catch((err) => { console.error(err); process.exit(1); });
```

### Yang TIDAK perlu

- ❌ Buat file di `src/` — itu untuk Prompt 2.
- ❌ Hard-code API key di file `.ts` — selalu via `process.env`.
- ❌ Install `@anthropic-ai/sdk` lagi (sudah ada dari Module 03).
- ❌ Wrap `experiments/voyage-ping.ts` dengan try/catch besar — biarkan error throw natural.

### Verifikasi setelah file dibuat

1. `package.json` punya `"voyageai"` di `dependencies`.
2. `.env.example` punya baris `VOYAGE_API_KEY=""`.
3. `.env.local` punya `VOYAGE_API_KEY` dengan value asli (TIDAK di-commit).
4. Jalankan: `npx tsx --env-file=.env.local experiments/voyage-ping.ts`.
5. Output: `dim: 1024` dan 3 angka float (mis. `[0.012, -0.034, 0.058]`).

---

**Salin prompt berikut, paste ke Claude Code:**

```
Saya ingin setup Voyage AI sebagai provider embedding untuk
Fin-App.

GOAL:
- Install package `voyageai` sebagai dependency project
  (bukan devDependency).
- Tambah variable VOYAGE_API_KEY ke .env.local (placeholder
  saja — saya akan isi manual setelahnya).
- Tambah baris VOYAGE_API_KEY="" ke .env.example agar
  developer lain tahu env var ini dibutuhkan.
- Buat file experiments/voyage-ping.ts: panggil
  client.embed() sekali dengan input ["hello world"], print
  panjang vektor + 3 angka pertama. Tujuan: konfirmasi koneksi
  dan API key valid.

CONTEXT:
- Model yang dipakai: voyage-3 (1024 dim, rekomendasi
  Anthropic).
- Project pakai TypeScript + Next.js (sesuai Module 01).

GUARDRAIL:
- JANGAN buat file di src/ — itu untuk Prompt 2.
- JANGAN hard-code API key di file ts mana pun — selalu
  via process.env.
- Apabila .env.local belum ada, beri tahu saya untuk buat
  manual (jangan auto-generate dengan dummy value).
```

**Verifikasi:**

1. `package.json` punya `"voyageai"` di `dependencies`.
2. `.env.example` punya baris `VOYAGE_API_KEY=""`.
3. Isi `.env.local` dengan API key Anda, lalu jalankan:
   `npx tsx --env-file=.env.local experiments/voyage-ping.ts`.
4. Output: `dim: 1024` dan 3 angka float (mis. `[0.012, -0.034, 0.058]`).

---

## Prompt 2 — Buat `src/lib/embeddings.ts`

### Walkthrough Manual

Sebelum copy-paste prompt ke Claude, pahami dulu struktur file `src/lib/embeddings.ts` yang akan dibuat. File ini akan jadi **satu-satunya** entry point ke Voyage API di seluruh aplikasi.

📂 **File baru**: `src/lib/embeddings.ts`

**1. Directive `"server-only"` di baris pertama**

📍 Lokasi: **baris 1** file. Memaksa bundler Next.js melempar error kalau file ini terimport dari client component.

```ts
// src/lib/embeddings.ts — baris 1
import "server-only";
```

**2. Import + singleton client**

📍 Lokasi: **module scope** (di luar function). Instantiate sekali, reuse seluruh request — hemat memori.

```ts
// src/lib/embeddings.ts — module scope
import { VoyageAIClient } from "voyageai";

if (!process.env.VOYAGE_API_KEY) {
  throw new Error("VOYAGE_API_KEY belum di-set di environment.");
}

const client = new VoyageAIClient({ apiKey: process.env.VOYAGE_API_KEY });
const MODEL = "voyage-3";
```

**3. Function `embed(text)`**

📍 Lokasi: **export top-level** di file. Tujuan: embed satu teks → return `number[]` (1024-dim).

```ts
// src/lib/embeddings.ts — export
/** Embed satu teks → vector 1024-dim (voyage-3). */
export async function embed(text: string): Promise<number[]> {
  const result = await client.embed({ input: [text], model: MODEL });
  return result.data[0].embedding;
}
```

**4. Function `embedBatch(texts)`**

📍 Lokasi: **export top-level** di file. Tujuan: hemat round-trip — embed banyak teks sekaligus.

```ts
// src/lib/embeddings.ts — export
/** Embed banyak teks dalam satu request → array of 1024-dim vectors. */
export async function embedBatch(texts: string[]): Promise<number[][]> {
  const result = await client.embed({ input: texts, model: MODEL });
  return result.data.map((d) => d.embedding);
}
```

### Yang TIDAK perlu

- ❌ Caching layer (LRU, Redis, dll.) — di-skip sekarang, dibahas di module RAG lanjutan.
- ❌ Retry/backoff manual — SDK Voyage sudah handle dasar; lebih advanced di production.
- ❌ Validasi panjang input — Voyage akan throw error sendiri kalau terlalu panjang.
- ❌ Modifikasi `experiments/voyage-ping.ts` — itu sandbox dari Prompt 1.

### Verifikasi setelah file dibuat

1. File `src/lib/embeddings.ts` ada dengan dua export: `embed` dan `embedBatch`.
2. Baris pertama: `import "server-only";`.
3. `npx tsc --noEmit` clean (tanpa error TypeScript).
4. Tidak ada hard-coded API key di file — semua via `process.env.VOYAGE_API_KEY`.
5. Coba import dari client component → harusnya gagal build (itu yang kita mau).

---

**Salin prompt berikut, paste ke Claude Code:**

```
Sekarang bangun function embed() reusable yang dipakai di
seluruh aplikasi.

GOAL:
- Buat file baru src/lib/embeddings.ts.
- Mulai dengan import "server-only" di baris pertama untuk
  cegah bundle ke client.
- Ekspor dua function:
  
  1. embed(text: string): Promise<number[]>
     → embed satu teks, return vector 1024-dim.
  
  2. embedBatch(texts: string[]): Promise<number[][]>
     → embed banyak teks dalam satu request (batching).
  
- Inisialisasi VoyageAIClient SEKALI di module scope, baca
  API key dari process.env.VOYAGE_API_KEY.
- Throw error yang jelas apabila VOYAGE_API_KEY tidak ada di
  env.
- Tambah JSDoc singkat untuk masing-masing function.

CONTEXT:
- Model: voyage-3, dimensi 1024.
- File ini akan dipanggil dari Server Actions / route
  handler di section selanjutnya.

GUARDRAIL:
- JANGAN tambah caching dulu — itu akan dibahas terpisah.
- JANGAN modifikasi file lain selain src/lib/embeddings.ts.
- JANGAN ubah experiments/voyage-ping.ts dari prompt 1.
```

**Verifikasi:**

1. File `src/lib/embeddings.ts` ada dengan dua export: `embed` dan `embedBatch`.
2. Baris pertama: `import "server-only";`.
3. Tidak ada error TypeScript saat `npx tsc --noEmit`.
4. Tidak ada hard-coded API key di file.

---

## Prompt 3 — Test Semantic Similarity

### Walkthrough Manual

Sebelum copy-paste prompt ke Claude, pahami flow file eksperimen ini. Tujuannya: konfirmasi bahwa `embed()` benar-benar menangkap **makna semantik**, bukan kata kunci.

📂 **File baru**: `experiments/test-embeddings.ts`

**1. Import + 5 kalimat uji**

📍 Lokasi: **top-level** di file. Pilih kalimat yang sengaja mengelompok ke 2 kategori semantik.

```ts
// experiments/test-embeddings.ts — top-level
import { embedBatch } from "@/lib/embeddings";

const sentences = [
  "Beli kopi di Starbucks tadi pagi",                  // s1 — food
  "Makan siang nasi padang di warung",                 // s2 — food
  "Investasi reksadana saham untuk jangka panjang",    // s3 — finance
  "Beli ayam goreng untuk makan malam",                // s4 — food
  "Pertimbangkan portfolio diversifikasi obligasi",    // s5 — finance
];
```

**2. Cosine similarity (reuse dari pendahuluan konsep)**

📍 Lokasi: **top-level**. Copy implementasi dari `experiments/embedding-intuition.ts` — tidak perlu library.

```ts
// experiments/test-embeddings.ts — top-level
function cosine(a: number[], b: number[]): number {
  const dot = a.reduce((s, ai, i) => s + ai * b[i], 0);
  const nA = Math.sqrt(a.reduce((s, x) => s + x * x, 0));
  const nB = Math.sqrt(b.reduce((s, x) => s + x * x, 0));
  return dot / (nA * nB);
}
```

**3. Embed + matriks + ranking**

📍 Lokasi: **di dalam `async function main()`**. Wajib async karena `embedBatch` adalah Promise.

```ts
// experiments/test-embeddings.ts — di dalam main()
const vecs = await embedBatch(sentences);
// build & print 5x5 matrix dengan padStart untuk alignment
// build pairs.sort(desc), print top-3 + bottom-3
```

**4. Run**

📍 Lokasi: terminal.

```bash
npx tsx --env-file=.env.local experiments/test-embeddings.ts
```

### Yang TIDAK perlu

- ❌ Modifikasi `src/lib/embeddings.ts` — file ini hanya consumer.
- ❌ Pindahkan file ke `src/` — eksperimen tetap di `experiments/`.
- ❌ Library tabel (cli-table3, dll.) — `padStart` cukup.
- ❌ Loop manual ke API per kalimat — pakai `embedBatch` (1 round-trip).

### Verifikasi setelah file dibuat

1. Output matriks 5×5 dengan diagonal = 1.0000.
2. Pasangan `(s1, s2)`, `(s2, s4)`, `(s1, s4)` muncul di top similarity (skor > 0.6).
3. Pasangan `(s3, s5)` punya skor tinggi (> 0.6).
4. Pasangan lintas kategori (mis. `s1` vs `s3`) punya skor lebih rendah daripada pasangan dalam kategori.
5. Apabila ekspektasi tidak tercapai — cek apakah path alias `@/lib/embeddings` resolve dengan benar via tsx.

---

**Salin prompt berikut, paste ke Claude Code:**

```
Sekarang verifikasi function embed() benar-benar menangkap
makna semantik, bukan hanya keyword.

GOAL:
- Buat file experiments/test-embeddings.ts.
- Import embedBatch dari "@/lib/embeddings".
- Definisikan 5 kalimat:
  
  s1 = "Beli kopi di Starbucks tadi pagi"
  s2 = "Makan siang nasi padang di warung"
  s3 = "Investasi reksadana saham untuk jangka panjang"
  s4 = "Beli ayam goreng untuk makan malam"
  s5 = "Pertimbangkan portfolio diversifikasi obligasi"
  
- Embed semua sekaligus via embedBatch.
- Implementasi cosine similarity (reuse dari pendahuluan konsep OK,
  copy ke file ini).
- Print similarity matrix 5x5 dalam format tabel rapi
  (gunakan padStart untuk alignment).
- Print juga 3 pasangan paling mirip dan 3 paling tidak
  mirip.

CONTEXT:
- Asumsi semantik:
  - s1 (kopi), s2 (nasi padang), s4 (ayam goreng) =
    kategori makanan/F&B → harus saling dekat.
  - s3 (reksadana), s5 (obligasi) = kategori
    investasi → harus dekat satu sama lain.
  - Lintas kategori (mis. s1 vs s3) → harus jauh.

GUARDRAIL:
- JANGAN modifikasi src/lib/embeddings.ts.
- File ini di experiments/, BUKAN di src/.
- Jalankan dengan `npx tsx --env-file=.env.local
  experiments/test-embeddings.ts`.
```

**Verifikasi:**

1. Output matriks 5×5 dengan diagonal = 1.0000.
2. Pasangan `(s1, s2)`, `(s2, s4)`, `(s1, s4)` muncul di top similarity (skor > 0.6).
3. Pasangan `(s3, s5)` punya skor tinggi (> 0.6).
4. Pasangan lintas kategori (mis. `s1` vs `s3`) punya skor lebih rendah daripada pasangan dalam kategori.
5. Apabila hasil tidak sesuai ekspektasi, debug: cek apakah teks benar-benar terkirim ke API, cek dimensi vector.

---

## Validasi Akhir Section 1

- [ ] Package `voyageai` terinstall.
- [ ] `.env.local` punya `VOYAGE_API_KEY` valid, `.env.example` punya placeholder.
- [ ] `src/lib/embeddings.ts` punya `embed()` + `embedBatch()` + import `"server-only"`.
- [ ] Test similarity matrix menunjukkan kategori makanan mengelompok terpisah dari kategori investasi.
- [ ] `npx tsc --noEmit` clean.

## Refleksi Section 1

1. Berapa skor cosine similarity tertinggi yang Anda dapat antara dua kalimat lintas kategori? Apakah itu mengejutkan?
2. Apabila Anda mengubah satu kata di kalimat (mis. "kopi" → "teh"), seberapa besar perubahan skor similarity?
3. Mengapa import `"server-only"` penting di `src/lib/embeddings.ts`? Apa risiko kalau di-skip?
4. Berapa estimasi biaya kalau Anda embed 10.000 deskripsi transaksi (asumsi ~20 token per deskripsi)?

---

⬅️ Kembali: **[Konsep Embedding (Pendahuluan)](./materi.md#konsep-embedding-pendahuluan)** · 🏠 Index: **[Module 06 — Latihan](./latihan.md)** · ➡️ Lanjut: **[Section 2 — Database Vector](./latihan-2-database-vector.md)**
