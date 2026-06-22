# Section 1 — Integrasi Claude API ke Chatbot

> Bagian dari **[Module 04 — Latihan](./latihan.md)**. Lanjutan dari **[Latihan UI Chatbot di Module 03](../Module-03-Claude-API/latihan-ui-chatbot.md)**.

> Latihan untuk **menghidupkan** chatbot dari Latihan UI Module 03: mengganti mock messages dengan respons asli dari Claude API. Empat prompt siap copy-paste.
>
> **Estimasi Section 1**: 40–50 menit.

## Prasyarat Section 1

- [ ] Latihan UI chatbot di Module 03 selesai. Panel chatbot tampil dengan UI lengkap (mock messages, input, toggle).
- [ ] Module 03 selesai. SDK `@anthropic-ai/sdk` ter-install dan `ANTHROPIC_API_KEY` sudah ada di `.env.local`.
- [ ] Dev server berjalan: `npm run dev`.
- [ ] Claude Code aktif di terminal terpisah.

> ⚠️ **Penting**: Section 1 **memperluas** kode dari Latihan UI Module 03. Jangan menulis ulang `ai-chat-panel.tsx` dari nol — minta Claude untuk **memodifikasi** file yang sudah ada.

---

## Prompt 1 — Buat Server Action `askAdvisor`

### Walkthrough Manual (sebelum pakai prompt)

Sebelum copy-paste prompt ke Claude, pahami dulu apa saja yang harus ada di file `src/features/advisor.ts`. Ini akan membantu Anda **mereview** output Claude dan menangkap kesalahan kalau ada.

**File baru: `src/features/advisor.ts`** (satu file, tidak modifikasi yang lain)

**1. Directive `"use server"` di baris pertama**

Wajib agar Next.js menganggap file ini server action. Tanpa ini, fungsi tidak akan jalan saat dipanggil dari client.

```ts
"use server";
```

**2. Import SDK Anthropic**

SDK sudah ter-install di Module 03 (`@anthropic-ai/sdk` ada di `package.json`).

```ts
import Anthropic from "@anthropic-ai/sdk";
```

**3. Inisialisasi client (di module level, bukan di dalam function)**

Instantiate sekali saja, di-reuse setiap pemanggilan — lebih efisien daripada bikin baru tiap call. API key TANPA prefix `NEXT_PUBLIC_` karena ini server-only.

```ts
const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});
```

**4. Function `askAdvisor(message: string): Promise<string>`**

Alur internal:

- **Validasi input dulu** — kalau `message.trim()` kosong, langsung `throw new Error("Pesan tidak boleh kosong")`. Ini SEBELUM API call agar hemat biaya.
- **Panggil `client.messages.create(...)`** dengan param:
  - `model: "claude-haiku-4-5"` (murah untuk eksperimen)
  - `max_tokens: 1024`
  - `messages: [{ role: "user", content: message }]`
- **Cek tipe response block** — `response.content[0]` bisa berbentuk `"text"`, `"tool_use"`, `"thinking"`, dll. Kalau bukan `"text"`, throw error.
- **Return `block.text`** (string saja), JANGAN return raw response object.

**5. JSDoc singkat di atas function** — tujuan, parameter, return value.

### Yang TIDAK perlu

- ❌ Schema Zod (input cuma `string`)
- ❌ Koneksi Supabase (server action ini tidak sentuh DB)
- ❌ Try/catch besar (biarkan error throw, caller yang handle)
- ❌ Logger / observability (cukup throw error message yang jelas)

### Verifikasi setelah file dibuat

1. Cek baris 1 ada `"use server";`
2. API key TANPA `NEXT_PUBLIC_`
3. Test cepat:
   ```ts
   // experiments/test-advisor.ts
   import { askAdvisor } from "../src/features/advisor";
   console.log(await askAdvisor("Halo, apa kabar?"));
   ```
   ```bash
   npx tsx --env-file=.env.local experiments/test-advisor.ts
   ```

---

**Salin prompt berikut, paste ke Claude Code:**

```
Saya ingin membuat server action untuk memanggil Claude API
dari chatbot.

GOAL:
- Buat file baru src/features/advisor.ts.
- Ekspor server action async askAdvisor(message: string):
  Promise<string>.
- Function memanggil Claude API menggunakan SDK
  @anthropic-ai/sdk yang sudah ter-install.
- Return berupa string respons dari Claude (text content
  block pertama).

CONTEXT:
- Pola server action sama dengan src/features/action.ts
  (getBalanceSummary, dst). File dimulai dengan "use server".
- API key diambil dari process.env.ANTHROPIC_API_KEY (TANPA
  prefix NEXT_PUBLIC_).
- Pakai model "claude-haiku-4-5" untuk eksperimen hemat biaya.
- max_tokens: 1024.
- Pesan dikirim sebagai single user message:
  messages: [{ role: "user", content: message }]

GUARDRAIL:
- Apabila response.content[0] bukan tipe "text", throw error
  dengan pesan jelas.
- Apabila message kosong / whitespace-only, throw error
  "Pesan tidak boleh kosong" tanpa memanggil API (hemat biaya).
- JANGAN expose detail internal API ke caller (mis. raw
  response object) — hanya return string.
- Tambahkan komentar JSDoc singkat di atas function: tujuan,
  parameter, return value.

Setelah selesai, jelaskan singkat strukturnya.
```

**Verifikasi:**

1. File `src/features/advisor.ts` tercipta dengan struktur yang diminta.
2. Buka file & pastikan ada `"use server"` di baris pertama.
3. Verifikasi API key dipanggil tanpa prefix `NEXT_PUBLIC_`.
4. (Opsional) test cepat dari `experiments/`:
   ```ts
   // experiments/test-advisor.ts
   import { askAdvisor } from "../src/features/advisor";
   console.log(await askAdvisor("Halo, apa kabar?"));
   ```
   Jalankan: `npx tsx --env-file=.env.local experiments/test-advisor.ts`

---

## Prompt 2 — Integrasi ke AIChatPanel (Ganti Mock dengan API Call)

**Salin prompt berikut:**

```
Hubungkan tombol kirim di AIChatPanel ke server action
askAdvisor.

GOAL:
- Di src/components/chat/ai-chat-panel.tsx, modifikasi
  handler "kirim pesan" yang saat ini push mock message.
- Alur baru saat user klik kirim (atau tekan Enter):
  1. Push user message ke state messages (sudah dilakukan
     sekarang — pertahankan).
  2. Kosongkan input (sudah ada — pertahankan).
  3. Set state isThinking = true.
  4. Panggil askAdvisor dengan isi user message.
  5. Push assistant message ke state messages dengan content
     dari hasil askAdvisor.
  6. Set isThinking = false.

- Tambahkan state baru: useState<boolean>(false) untuk
  isThinking.
- Disable input dan tombol kirim selama isThinking === true.
- Saat isThinking, di bawah pesan terakhir, tampilkan
  indikator "AI sedang mengetik..." dengan ikon Loader2 dari
  lucide-react (animate-spin).

CONTEXT:
- Import askAdvisor dari "@/features/advisor".
- Mock messages awal dari Latihan UI Module 03 dipertahankan sebagai
  initial state (jangan hapus dulu — Section selanjutnya
  akan mengurus welcome message).
- Komponen Loader2 dipakai dengan animate-spin dari Tailwind.

GUARDRAIL:
- JANGAN ubah struktur header / footer panel — hanya
  modifikasi handler dan body messages area.
- ID pesan unik: gunakan crypto.randomUUID() atau Date.now()
  untuk id setiap message baru.
- Indikator "sedang mengetik" muncul di posisi yang sama
  dengan bubble assistant biasa (kiri, tanpa background
  bubble).
```

**Verifikasi:**

1. Reload browser. Mock messages masih tampil (initial state).
2. Ketik pertanyaan "Berikan tip menghemat pengeluaran" → klik kirim.
3. Pesan user muncul, lalu indikator "AI sedang mengetik..." tampil.
4. Beberapa detik kemudian, respons asli dari Claude muncul sebagai bubble assistant dengan markdown ter-render.
5. Input kembali aktif, dapat ketik pertanyaan baru.

---

## Prompt 3 — Error Handling + Tombol Retry

**Salin prompt berikut:**

```
Tambahkan penanganan error di alur pemanggilan askAdvisor.

GOAL:
- Bungkus pemanggilan askAdvisor di Prompt 2 dengan
  try/catch.
- Tambahkan state baru:
  - lastError: { message: string; userQuestion: string } | null
- Saat catch:
  1. Set isThinking = false.
  2. Set lastError dengan pesan error dan pertanyaan yang
     gagal.
- Saat lastError != null, tampilkan di bawah daftar pesan
  sebuah bubble error berstyle khusus:
  - Background bg-rose-50 dark:bg-rose-950/40.
  - Border border-rose-200.
  - Ikon AlertCircle (lucide-react) warna rose.
  - Pesan: "Terjadi kesalahan saat menghubungi AI: {error
    message}".
  - Tombol "Coba lagi" — saat di-klik:
    a. Set lastError = null.
    b. Panggil ulang alur kirim dengan userQuestion dari
       lastError.
- Saat user mengetik pesan baru manual (mengganti input),
  TIDAK perlu menghapus error — biarkan tetap tampil sampai
  retry sukses atau pesan baru terkirim.
- Saat pesan baru terkirim sukses, set lastError = null.

CONTEXT:
- File yang dimodifikasi: src/components/chat/ai-chat-panel.tsx.
- Pakai komponen Button variant="outline" untuk tombol Coba
  lagi.
- Pesan error biasanya datang dari error.message — apabila
  error bukan instance Error, gunakan "Unknown error".

GUARDRAIL:
- JANGAN menggunakan toast — error harus tampil INLINE di
  chat area, agar user tetap punya konteks pertanyaan apa
  yang gagal.
- Tombol retry tidak boleh push pesan user duplikat ke
  state messages — gunakan userQuestion langsung sebagai
  argumen ke askAdvisor.
- Indikator error tidak muncul jika lastError = null.
```

**Verifikasi:**

1. Sengaja salahkan API key di `.env.local` (tambah karakter di akhir). Restart dev server.
2. Kirim pertanyaan → indikator typing → kemudian muncul **bubble error merah** dengan tombol "Coba lagi".
3. Perbaiki API key, restart dev server.
4. Klik "Coba lagi" → error hilang, indikator typing muncul, respons asli akhirnya tampil.
5. (Edge case) Ketik pertanyaan baru saat error tampil → error tetap tampil sampai pertanyaan baru sukses.

---

## Prompt 4 — Bersihkan Mock Messages, Tambah Welcome

**Salin prompt berikut:**

```
Bersihkan mock messages dari Latihan UI Module 03 dan ganti dengan satu
welcome message dari assistant.

GOAL:
- Ubah initial state messages di AIChatPanel dari array
  berisi 3-4 mock menjadi array dengan SATU pesan welcome
  dari assistant.
- Pesan welcome:
  - role: "assistant"
  - content (markdown):
    "Halo! Saya **AI Financial Advisor** Anda. Saya dapat
    membantu Anda dengan:

    - Analisis pola pengeluaran
    - Tips menghemat dan menabung
    - Pertanyaan umum tentang keuangan personal

    Apa yang ingin Anda tanyakan?"

CONTEXT:
- File: src/components/chat/ai-chat-panel.tsx.
- Pesan welcome ditulis langsung di state initialization,
  bukan dari API.
- Format markdown dengan list dan bold dipertahankan saat
  render.

GUARDRAIL:
- HANYA satu welcome message di initial state — bukan
  banyak.
- Welcome message TIDAK boleh berasal dari panggilan API
  (hemat biaya, instant tampil).
- JANGAN ubah behavior lain (handler kirim, error, dll.).
```

**Verifikasi:**

1. Reload browser.
2. Panel chatbot menampilkan satu pesan welcome yang ramah dari assistant.
3. Pesan welcome ter-format dengan baik (bold + list).
4. Kirim pertanyaan baru → respons asli dari Claude muncul setelah welcome.

---

## Validasi Akhir Section 1

Pastikan checklist berikut tercapai sebelum lanjut ke Section 2:

- [ ] Server action `askAdvisor` ada di `src/features/advisor.ts`.
- [ ] API key diambil dari env (TANPA prefix `NEXT_PUBLIC_`).
- [ ] Pertanyaan user mendapat respons asli dari Claude (bukan mock).
- [ ] Indikator "AI sedang mengetik..." muncul saat menunggu respons.
- [ ] Input & tombol kirim disabled selama menunggu.
- [ ] Pesan error tampil inline (bukan toast) saat API call gagal.
- [ ] Tombol "Coba lagi" berfungsi tanpa duplikasi pesan user.
- [ ] Welcome message tampil saat panel pertama kali dibuka.
- [ ] Tidak ada warning di console browser tentang process.env client-side.

## Refleksi Section 1

Tuliskan pada catatan pribadi:

1. **Berapa detik** rata-rata waktu respons Claude untuk pertanyaan sederhana?
2. Adakah perbedaan kualitas jawaban ketika Anda mengubah pertanyaan dari **vague** ke **spesifik**? (Coba: "Beri tips" vs "Beri tiga tips konkret untuk mengurangi biaya makan di luar")
3. Apakah ada **format yang tidak ter-render** dengan baik di chatbot? (Misalnya tabel, code block)
4. Apa **error pertama** yang Anda temui saat membangun Section 1? Bagaimana Anda mendiagnosisnya?
5. Apakah Anda berpikir untuk menambahkan **rate limit di sisi UI** (mencegah spam)? Mengapa atau mengapa tidak?

---

⬅️ Kembali: **[Latihan UI Module 03](../Module-03-Claude-API/latihan-ui-chatbot.md)** · ➡️ Lanjut: **[Section 2 — Text Generation](./latihan-section-2.md)**
