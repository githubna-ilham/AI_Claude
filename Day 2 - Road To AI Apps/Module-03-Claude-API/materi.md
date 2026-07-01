# Module 03 — Claude API: Koneksi Pertama

> **Tujuan modul** (section pertama): Anda dapat memanggil **Claude API** dari sebuah file TypeScript sederhana, menerima respons-nya, dan menampilkan hasilnya di console terminal.
>
> **Output akhir section ini**: file `experiments/claude-test.ts` di project Fin-App yang ketika dijalankan, mengirimkan prompt ke Claude API, lalu mencetak balasan model di terminal.

---

## Apa yang Akan Anda Pelajari (Section Pertama)

1. Membedakan **Claude API** dari Claude Code dan Claude Desktop — tiga produk berbeda, satu underlying model.
2. Mendapatkan **API key** dari Anthropic Console dan menyimpannya dengan aman.
3. Memasang SDK resmi Anthropic untuk Node.js (`@anthropic-ai/sdk`).
4. Membuat file eksperimen `experiments/claude-test.ts` untuk uji koneksi.
5. Memahami **anatomi respons** Claude API: `content`, `usage`, `stop_reason`, dan lainnya.
6. Menjalankan file tersebut dan melihat hasilnya di console.

**Durasi belajar (section pertama)**: ±30 menit.

---

## 1. Apa itu Claude API?

**Claude API** adalah cara **programmatic** untuk menggunakan model Claude — bukan lewat aplikasi chat, tetapi lewat HTTP request langsung dari kode Anda. Inilah yang membuat Anda dapat **mengintegrasikan Claude ke aplikasi sendiri**: chatbot, agen otomatis, fitur summarization, dan seterusnya.

### Posisi Claude API di Ekosistem Anthropic

| Produk | Cara akses | Cocok untuk |
|---|---|---|
| **Claude Desktop / Claude.ai** | Chat UI grafis | Pengguna akhir, brainstorm, riset |
| **Claude Code** | Terminal CLI dengan tools | Developer yang sedang coding |
| **Claude API** | HTTP request dari kode | Developer yang **membangun aplikasi** yang menggunakan Claude |

Pada modul ini, fokus Anda adalah Claude API. API inilah yang nantinya akan menjadi otak fitur AI Fin-App: menjawab pertanyaan natural language tentang transaksi keuangan Anda.

### Konsep Utama Claude API

1. **Stateless** — setiap request berdiri sendiri. Apabila Anda ingin "percakapan", Anda yang menyimpan history dan mengirimnya kembali setiap request.
2. **Authentication via API Key** — header `x-api-key` di setiap request.
3. **Streaming opsional** — Claude dapat mengembalikan jawaban kata-demi-kata seperti ChatGPT, atau sekaligus utuh.
4. **Multimodal** — selain teks, dapat menerima gambar dan PDF sebagai input.
5. **Pricing per-token** — Anda dibayar berdasarkan jumlah token input + output. Free tier tersedia untuk eksperimen.

---

## 2. Mendapatkan API Key

### 2.1 Buat Akun di Anthropic Console

1. Buka **https://console.anthropic.com**.
2. Klik **Sign in** (gunakan akun Google, GitHub, atau email).
3. Apabila pertama kali, Anda akan diarahkan ke onboarding singkat.

### 2.2 Generate API Key

1. Di dashboard Console, klik menu sidebar **API Keys** (atau langsung ke `console.anthropic.com/settings/keys`).
2. Klik tombol **Create Key**.
3. Beri nama yang mudah diingat (contoh: `fina-app-development`).
4. **Salin nilai key-nya segera** — formatnya `sk-ant-api03-...`. Anthropic **tidak akan menampilkannya lagi** setelah Anda menutup modal.

> ⚠️ **Penting**: simpan API key di password manager Anda. Anggap key ini seperti password — orang lain yang memiliki key Anda dapat memanggil Claude **atas nama Anda** dan menagih biaya ke akun Anda.

### 2.3 Free Tier dan Pricing

Untuk eksperimen kecil seperti modul ini:

- Akun baru biasanya dapat **kredit gratis** (sekitar $5) untuk dipakai bereksperimen.
- Setelah habis, perlu menambah saldo dari **Billing** di Console.
- Biaya per-call untuk model Haiku sangat kecil (sekitar $0.001–0.003 untuk prompt sederhana).

> 💡 **Tip hemat**: untuk eksperimen dan latihan, gunakan model **Claude Haiku 4.5** (`claude-haiku-4-5`). Performanya sudah sangat baik untuk task umum, dengan biaya jauh lebih murah daripada Sonnet/Opus.

---

## 3. Simpan API Key di Project Fin-App

Buka file `.env.local` di folder `fina-app/` (yang sudah Anda buat di Module 01). Tambahkan baris baru:

```env
NEXT_PUBLIC_SUPABASE_URL=https://...supabase.co
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=sb_publishable_...

# Tambahkan baris ini:
ANTHROPIC_API_KEY=sk-ant-api03-...your-key...
```

⚠️ **Perhatikan penamaan**: kunci ini **tidak** menggunakan prefix `NEXT_PUBLIC_`. Mengapa?

- Prefix `NEXT_PUBLIC_` membuat variable **dapat dibaca oleh browser**.
- API key Anthropic adalah **rahasia** — apabila bocor ke browser, orang lain dapat memakai dan menagihkan biaya ke akun Anda.
- Tanpa prefix `NEXT_PUBLIC_`, variable hanya tersedia di sisi **server** (Node.js, server actions, route handlers, atau script standalone).

Tambahkan juga ke `.env.example` (yang di-commit ke git) sebagai dokumentasi — tetapi **hanya placeholder**, bukan nilai aslinya:

```env
# .env.example
ANTHROPIC_API_KEY=sk-ant-api03-...your-key-here...
```

---

## 4. Pasang SDK Anthropic

Di terminal, pada folder `fina-app/`, jalankan:

```bash
npm install @anthropic-ai/sdk
```

Verifikasi instalasi dengan melihat `package.json`:

```bash
grep anthropic package.json
```

Output yang diharapkan:

```
"@anthropic-ai/sdk": "^0.x.x",
```

SDK ini menyediakan client TypeScript dengan **type-safety** untuk request/response Claude API. Anda tidak perlu mengurus formatting HTTP request manual.

---

## 5. Buat File Eksperimen

Pada section ini, Anda akan membuat file standalone untuk uji koneksi. File ini **bukan bagian dari aplikasi Next.js** — hanya script TypeScript yang dijalankan dari terminal.

### 5.1 Lokasi File

Buat folder baru `experiments/` di root project (sejajar dengan `src/`, `supabase/`, dan lain-lain):

```bash
mkdir -p experiments
```

Lalu buat file `experiments/claude-test.ts`:

```ts
// experiments/claude-test.ts
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

async function main() {
  console.log("🚀 Mengirim request ke Claude API...");

  const response = await client.messages.create({
    model: "claude-haiku-4-5",
    max_tokens: 256,
    messages: [
      {
        role: "user",
        content: "Halo Claude! Sebutkan tiga hal yang menarik tentang Indonesia dalam satu paragraf.",
      },
    ],
  });

  console.log("\n✅ Respons diterima!\n");
  console.log("──────────────────────────────────────────");
  console.log(response.content[0].type === "text" ? response.content[0].text : "(non-text content)");
  console.log("──────────────────────────────────────────\n");

  console.log("📊 Statistik penggunaan token:");
  console.log(`   Input tokens : ${response.usage.input_tokens}`);
  console.log(`   Output tokens: ${response.usage.output_tokens}`);
  console.log(`   Stop reason  : ${response.stop_reason}`);
}

main().catch((err) => {
  console.error("❌ Error:", err);
  process.exit(1);
});
```

### 5.2 Penjelasan Singkat Setiap Bagian

**Import SDK:**
```ts
import Anthropic from "@anthropic-ai/sdk";
```

**Membuat client** — `apiKey` diambil otomatis dari `process.env.ANTHROPIC_API_KEY` apabila Anda meneruskannya:
```ts
const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
```

**Memanggil endpoint Messages** — endpoint utama Claude API:
- `model` — pilihan model Claude. Gunakan `claude-haiku-4-5` untuk eksperimen hemat.
- `max_tokens` — batas output. 256 cukup untuk balasan pendek; tambahkan jika butuh jawaban panjang.
- `messages` — array berisi giliran percakapan. Untuk request tunggal, cukup satu pesan `role: "user"`.

**Membaca response**:
- `response.content` adalah array — dapat berisi text block, tool_use block, dan sebagainya.
- Untuk text, periksa `content[0].type === "text"` sebelum mengakses `.text`.
- `response.usage` berisi jumlah token yang dipakai (untuk monitoring biaya).
- `response.stop_reason` memberi tahu mengapa Claude berhenti (`end_turn`, `max_tokens`, dan sebagainya).

---

## 6. Jalankan File Eksperimen

File `experiments/claude-test.ts` ditulis dalam TypeScript. Untuk menjalankannya langsung tanpa kompilasi manual, gunakan **tsx** (bagian dari ecosystem Next.js, biasanya sudah ter-install).

### 6.1 Jalankan dengan tsx

```bash
npx tsx --env-file=.env.local experiments/claude-test.ts
```

Catatan:
- `--env-file=.env.local` memberi tahu Node untuk memuat environment variable dari `.env.local`. Tanpa flag ini, `process.env.ANTHROPIC_API_KEY` akan `undefined`.
- `tsx` adalah runner yang dapat menjalankan TypeScript secara langsung.

### 6.2 Output yang Diharapkan

Apabila konfigurasi benar, terminal akan menampilkan:

```
🚀 Mengirim request ke Claude API...

✅ Respons diterima!

──────────────────────────────────────────
Indonesia memiliki banyak hal menarik. Pertama, negara ini
adalah negara kepulauan terbesar di dunia dengan lebih dari
17.000 pulau yang membentang dari Sabang hingga Merauke. Kedua,
Indonesia memiliki kekayaan budaya yang luar biasa dengan lebih
dari 300 kelompok etnis dan ratusan bahasa daerah. Ketiga,
keanekaragaman hayati Indonesia menempati posisi kedua tertinggi
di dunia, mencakup spesies endemik seperti orangutan, komodo,
dan rafflesia.
──────────────────────────────────────────

📊 Statistik penggunaan token:
   Input tokens : 28
   Output tokens: 142
   Stop reason  : end_turn
```

🎉 **Apabila Anda melihat output seperti di atas, koneksi pertama Anda ke Claude API berhasil.**

---

## 7. Anatomi Respons Claude API

Selain pesan utama, ada beberapa field penting di response yang perlu Anda pahami:

### 7.1 `content` — Array Block

Claude API mengembalikan respons sebagai **array block**, bukan string tunggal. Pada call sederhana, array hanya berisi satu block bertipe `text`. Tetapi pada call dengan **tool use** atau **extended thinking** (akan dibahas di modul berikutnya), array dapat berisi banyak block dengan tipe berbeda.

```ts
response.content = [
  { type: "text", text: "Indonesia memiliki..." }
]
```

#### Field per Tipe Block

Setiap block selalu memiliki field `type` (string) yang menjadi penanda tipe. Field selanjutnya tergantung nilai `type`:

| `type` | Field tambahan | Arti |
|---|---|---|
| `text` | `text: string` | Teks jawaban Claude. Ini tipe paling umum. |
| `text` | `citations?: Citation[]` | Opsional, muncul saat fitur **Citations** aktif — daftar sumber yang merujuk pada `documents` di request. |
| `thinking` | `thinking: string` | Isi reasoning saat **extended thinking** diaktifkan. |
| `thinking` | `signature: string` | Tanda tangan kriptografis untuk verifikasi block thinking saat dikirim ulang ke API. |
| `redacted_thinking` | `data: string` | Block thinking yang sebagian isinya disensor sistem keamanan; tetap perlu di-pass-through agar konteks utuh. |
| `tool_use` | `id: string` | ID unik panggilan tool — dipakai untuk mencocokkan `tool_result` pada turn berikutnya. |
| `tool_use` | `name: string` | Nama tool yang Claude ingin panggil. |
| `tool_use` | `input: object` | Argumen tool dalam bentuk JSON object sesuai `input_schema`. |
| `server_tool_use` | `id`, `name`, `input` | Sama seperti `tool_use`, tetapi dieksekusi di server Anthropic (misal `web_search`). |
| `web_search_tool_result` | `tool_use_id: string`, `content: Array \| Error` | Hasil pencarian web yang dikembalikan server Anthropic. |

> 💡 Pada **streaming**, Anda menerima event `content_block_start`, `content_block_delta`, lalu `content_block_stop` untuk setiap block — bentuk akhirnya tetap identik dengan tabel di atas.

#### Field Umum di Setiap Block

Selain field per tipe, semua block dapat membawa metadata berikut:

| Field | Tipe | Keterangan |
|---|---|---|
| `type` | `string` | Wajib. Penanda tipe block (`text`, `tool_use`, `thinking`, ...). |
| `cache_control` | `{ type: "ephemeral" } \| null` | Opsional. Muncul saat Anda mengaktifkan **prompt caching** pada block input — pada respons biasanya `null` atau tidak ada. |

#### Pola Pengaksesannya

```ts
for (const block of response.content) {
  if (block.type === "text") {
    console.log(block.text);
  } else if (block.type === "tool_use") {
    console.log(`Tool: ${block.name}`, block.input);
  } else if (block.type === "thinking") {
    console.log(`Reasoning: ${block.thinking}`);
  }
}
```

> ⚠️ **Selalu cek `block.type` sebelum mengakses field spesifik.** TypeScript SDK Anthropic menggunakan *discriminated union* — field seperti `.text` hanya ada setelah type-narrowing pada `type === "text"`.

### 7.2 `usage` — Akuntansi Token

```ts
response.usage = {
  input_tokens: 28,    // jumlah token yang Anda kirim
  output_tokens: 142,  // jumlah token yang Claude hasilkan
}
```

Token adalah unit penghitungan biaya. 1 token ≈ ¾ kata bahasa Inggris atau setengah kata bahasa Indonesia. Memantau angka ini membantu Anda mengoptimalkan penggunaan API.

### 7.3 `stop_reason` — Mengapa Claude Berhenti

| Nilai | Arti |
|---|---|
| `end_turn` | Claude selesai secara natural |
| `max_tokens` | Output mencapai batas `max_tokens` — kemungkinan terpotong |
| `stop_sequence` | Berhenti karena ketemu salah satu `stop_sequences` yang Anda tentukan |
| `tool_use` | Claude ingin memanggil tool (dibahas di modul lanjutan) |

> 💡 Apabila `stop_reason === "max_tokens"`, naikkan nilai `max_tokens` di request berikutnya.

### 7.4 `model` dan `id`

```ts
response.model = "claude-haiku-4-5"
response.id    = "msg_01ABC..."
```

- `model` memastikan model yang merespons sesuai permintaan Anda.
- `id` adalah ID unik response — berguna untuk logging dan debugging.

---

## 8. Troubleshooting

### Error: `ANTHROPIC_API_KEY is required`

Penyebab: env variable tidak ter-load. Pastikan:
- File `.env.local` ada dan berisi `ANTHROPIC_API_KEY=...`.
- Flag `--env-file=.env.local` di command `tsx`.

### Error: `401 authentication_error`

Penyebab: API key salah atau sudah dicabut. Periksa:
- Salin ulang dari Anthropic Console (mungkin ada karakter yang ter-trim).
- Cek apakah key masih aktif di Console → API Keys.

### Error: `429 rate_limit_error` atau `quota_exceeded`

Penyebab: melebihi limit gratis atau saldo habis. Periksa Billing di Anthropic Console.

### Error: `model not found`

Penyebab: nama model salah ketik atau model tidak tersedia di tier Anda. Coba `claude-haiku-4-5` yang umum tersedia.

---

## Recap Section Pertama

Anda telah:

1. Memahami posisi **Claude API** sebagai cara programmatic untuk memakai Claude.
2. **Membuat API key** di Anthropic Console dan menyimpannya di `.env.local`.
3. Memasang **SDK `@anthropic-ai/sdk`** di project Fin-App.
4. Membuat file eksperimen `experiments/claude-test.ts`.
5. Menjalankannya dengan `npx tsx --env-file=.env.local` dan **melihat respons Claude di terminal**.
6. Memahami **anatomi response**: content, usage, stop_reason.

**Section selanjutnya** akan mengeksplorasi:
- Menambahkan **system prompt** untuk mengontrol kepribadian Claude.
- Membangun **multi-turn conversation**.
- Streaming respons agar terasa lebih responsif.
- Tool use untuk membuat Claude dapat memanggil fungsi sendiri.
- Akhirnya: integrasi ke halaman Fin-App.

### Latihan Modul Ini (Kerjakan Berurutan)

1. **[Latihan 1 — Koneksi Pertama Claude API](./latihan.md)** *(±30 menit)*
   Eksperimen ringan untuk memperkuat pemahaman koneksi pertama: ganti prompt, atur `max_tokens`, bandingkan model, hitung estimasi biaya, dan tangani error. **Wajib selesai sebelum lanjut ke Latihan 2.**

2. **[Latihan 2 — Bangun Panel UI Chatbot AI Financial Advisor](./latihan-2-ui-chatbot.md)** *(±45–60 menit)*
   Latihan pure-UI tanpa logic API. Output: panel chatbot kosong di Fin-App yang siap dihubungkan ke Claude API di **Module 04**. Tidak memerlukan API key.

> 💡 Urutan ini disengaja: Latihan 1 memastikan koneksi & konsep API solid, baru Latihan 2 menyiapkan permukaan UI sebagai jembatan ke modul berikutnya.
