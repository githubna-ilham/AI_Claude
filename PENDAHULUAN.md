# Pendahuluan, Prerequisite & Persiapan — AI Claude Training

> Dokumen pembuka pelatihan **"Prompt Engineering, AI Agent & AI App Development with Claude"** (4 hari / 40 jam) — Multimatics.
> Wajib Anda baca **sebelum Day-1** dimulai.

---

## 1. Pendahuluan

### 1.1 Latar Belakang

Adopsi Large Language Model (LLM) telah bergeser dari sekadar *chatbot* menjadi fondasi otomasi, *knowledge worker augmentation*, dan produk digital generasi baru. **Claude** dari Anthropic merupakan salah satu LLM paling matang untuk konteks enterprise — unggul dalam *reasoning*, *long-context* (200K+ token), *tool use*, dan *responsible AI*.

Namun demikian, sebagian besar organisasi masih berhenti pada tahap **"prompt biasa"**. Untuk benar-benar memperoleh nilai bisnis, tim teknis perlu menguasai spektrum yang lebih luas:

```
Prompt Engineering  →  AI Workflow  →  AI Agent  →  AI Application + RAG  →  Governance
```

Pelatihan ini dirancang untuk menutup gap tersebut secara end-to-end dalam **4 hari intensif**, dengan komposisi **30% konsep — 60% hands-on — 5% case study — 5% diskusi**.

### 1.2 Tujuan Pembelajaran

Setelah menyelesaikan pelatihan ini, Anda akan mampu:

1. Memahami konsep dan arsitektur LLM (Claude family, context window, sampling, tokenization).
2. Mendesain prompt yang profesional, terukur, dan *reproducible*.
3. Mengoptimalkan output AI menggunakan *advanced prompting* (CoT, few-shot, structured output, evals).
4. Menggunakan **Claude API** (JavaScript/TypeScript) untuk pengembangan aplikasi AI.
5. Membangun AI Application end-to-end berbasis Claude.
6. Mengembangkan **AI Agent** untuk otomasi workflow dengan *tool use*.
7. Mengimplementasikan **RAG** (Retrieval Augmented Generation) menggunakan vector database.
8. Mengintegrasikan AI dengan tools, database, dan API eksternal secara aman.
9. Mendesain AI use case yang sesuai kebutuhan bisnis dengan ROI yang jelas.
10. Mengembangkan solusi AI yang *scalable* dan *responsible* (governance, risk, security).

### 1.3 Peta Pelatihan

| Hari      | Fokus                                                            | Module       |
| --------- | ---------------------------------------------------------------- | ------------ |
| **Day 1** | Prompt Engineering Fundamentals + Advanced                       | 1–3          |
| **Day 2** | Structured Output + AI Workflow + AI Agent                       | 4–9          |
| **Day 3** | AI App Development + RAG                                         | 10–12        |
| **Day 4** | AI Product Design + Governance + **Capstone Project**            | 13–14 + Cap. |

### 1.4 Untuk Siapa Pelatihan Ini

Pelatihan ini dirancang untuk Anda yang berperan sebagai:

- Software Developer (Backend / Frontend / Full-Stack)
- AI / ML Engineer (Beginner – Intermediate)
- Data Analyst / Data Engineer
- Product Manager / Product Owner
- IT Solution Architect / Tech Lead
- Anggota tim Digital Transformation atau Innovation Lab

---

## 2. Prerequisite

Bagian ini berisi **syarat minimum** yang sebaiknya Anda penuhi sebelum hari pertama. Jika Anda belum memenuhi seluruhnya, Anda tetap dapat mengikuti pelatihan — namun perlu usaha mandiri lebih untuk mengejar materi.

### 2.1 Pengetahuan yang Diperlukan

| Area                   | Tingkat        | Indikator "siap"                                                   |
| ---------------------- | -------------- | ------------------------------------------------------------------ |
| Konsep AI / LLM        | Awareness      | Pernah menggunakan ChatGPT/Claude, memahami istilah *prompt* dan *token* |
| Pemrograman            | Basic          | Mampu membaca dan menulis fungsi sederhana di **JavaScript / TypeScript** (familiar dengan React/Next.js merupakan nilai tambah, tetapi tidak wajib) |
| API & HTTP             | Basic          | Memahami `GET`/`POST`, JSON, header, status code                   |
| Command line / Terminal | Basic         | Mampu menjalankan `cd`, `ls`, eksekusi script, dan setting environment variable |
| Git                    | Basic (opsional)| Mampu menjalankan `clone`, `pull` — cukup untuk mengambil materi |
| Workflow bisnis        | Awareness      | Memahami proses digital di domain pekerjaan Anda                    |

> **Anda tidak perlu**: latar belakang ML, statistik lanjut, atau pengalaman *training* model. Pelatihan ini berfokus pada *application*, bukan *research*.

### 2.2 Hardware Minimum

Detail lengkap tersedia di [`REQUIREMENTS-Spek-Komputer-Aplikasi.md`](REQUIREMENTS-Spek-Komputer-Aplikasi.md). Ringkasan:

| Komponen   | Minimum                                            | Direkomendasikan                            |
| ---------- | -------------------------------------------------- | ------------------------------------------- |
| CPU        | Intel i5 gen 8 / Ryzen 5 / Apple M1                | Intel i7 gen 11+ / Ryzen 7 / Apple M2+      |
| RAM        | **8 GB**                                           | **16 GB** (penting untuk Day-3 RAG lab)     |
| Storage    | 20 GB free                                         | 50 GB free SSD                              |
| OS         | Windows 10/11, macOS 12+, Ubuntu 22.04+            | Windows 11, macOS 14+, Ubuntu 24.04         |
| Internet   | WiFi stabil minimal 10 Mbps                        | WiFi 6 + ethernet backup                    |
| Battery    | Minimal 4 jam (atau pastikan colokan tersedia)     | —                                           |

> ❌ **Tidak didukung**: Tablet, Chromebook, atau perangkat yang tidak mampu menginstal Node.js dan menjalankan dev server lokal.

### 2.3 Akun & Akses

- ✅ Akun **Anthropic Console** — daftar di https://console.anthropic.com
- ✅ **Anthropic API key** — disediakan oleh fasilitator, atau generate sendiri (top-up minimal **$5** untuk seluruh lab)
- ✅ Akun **Supabase** — daftar di https://supabase.com (free tier cukup; digunakan untuk Day 2–4 sebagai database `fin-app` + pgvector untuk RAG)
- ✅ Akun **Voyage AI** — daftar di https://www.voyageai.com (free tier cukup; digunakan untuk embedding di Day 3)
- ✅ Akun **GitHub** (untuk meng-clone materi)
- ✅ Email aktif untuk korespondensi dan sertifikat

---

## 3. Persiapan yang Perlu Anda Lakukan

Checklist berikut diurutkan berdasarkan *deadline*. Centang setiap item ketika sudah Anda selesaikan.

### 3.1 H-7 sampai H-3 — Administratif

- [ ] Konfirmasi kehadiran Anda kepada penyelenggara
- [ ] Isi **[Pretest](pretest/PRETEST-AI-Claude.md)** dengan *deadline* **H-3**. Jawaban Anda akan digunakan untuk menyesuaikan kedalaman materi dan pilihan use case selama pelatihan.
- [ ] Tentukan **satu use case nyata** dari pekerjaan Anda yang ingin dibawa ke Capstone Day-4 (misalnya: otomasi tiket support, RAG dokumen SOP internal, dan sebagainya)
- [ ] Baca cepat `README.md` repo ini untuk memahami peta materi keseluruhan

### 3.2 H-3 sampai H-1 — Setup Teknis

#### Step 1 — Install Runtime

```bash
node --version            # harus >= 20 (idealnya 22 LTS)
npm --version             # bundled dengan Node.js, harus >= 10
```

Link install:
- Node.js 20 LTS+: https://nodejs.org/ (download installer sesuai OS)
- Tips: pasang **nvm** (https://github.com/nvm-sh/nvm untuk macOS/Linux, https://github.com/coreybutler/nvm-windows untuk Windows) jika Anda sudah memiliki project lain dengan versi Node.js berbeda.

#### Step 2 — Install Editor

Anda direkomendasikan menggunakan salah satu dari:
- **Cursor** — https://cursor.com (AI-native, paling nyaman untuk pelatihan ini)
- **VS Code** — https://code.visualstudio.com beserta ekstensi: *ESLint*, *Tailwind CSS IntelliSense*, *Prettier*, *GitLens*

#### Step 3 — Clone Repository Materi

```bash
git clone https://github.com/githubna-ilham/AI_Claude.git
cd AI_Claude
```

Selain repo materi, fasilitator juga akan membagikan link repo **`fin-app`** (Next.js starter) yang akan digunakan sebagai backbone hands-on Day 2 hingga Capstone. Clone repo tersebut di lokasi yang Anda inginkan.

#### Step 4 — Install Dependencies (di folder `fin-app`)

```bash
cd fin-app
npm install
```

Perintah ini akan menarik seluruh dependensi (Next.js, React, Tailwind, Shadcn UI, Anthropic SDK, Supabase client, dll.). Detail daftar paket ada di `package.json` dan dijabarkan di [`REQUIREMENTS-Spek-Komputer-Aplikasi.md`](REQUIREMENTS-Spek-Komputer-Aplikasi.md).

#### Step 5 — Konfigurasi API Key & Environment Variables

Buat file **`.env.local`** di folder `fin-app/` (Next.js convention):

```env
# Anthropic (Day 2+)
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Supabase (Day 2+)
NEXT_PUBLIC_SUPABASE_URL=https://xxxxxxxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJI...

# Voyage AI (Day 3)
VOYAGE_API_KEY=pa-xxxxxxxxxxxx
```

> ⚠️ **Jangan commit file `.env.local` ke git.** Next.js sudah menyertakan pola ini di `.gitignore` default, tetapi pastikan kembali sebelum push.

#### Step 6 — Smoke Test (verifikasi seluruh setup berjalan)

Buat file `smoke-test.mjs` di folder `fin-app/`:

```javascript
import 'dotenv/config';
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

const resp = await client.messages.create({
  model: 'claude-sonnet-4-6',
  max_tokens: 128,
  messages: [
    { role: 'user', content: 'Sebut 1 keuntungan utama Claude untuk enterprise dalam 1 kalimat.' },
  ],
});

console.log(resp.content[0].text);
```

Jalankan:

```bash
node --env-file=.env.local smoke-test.mjs
```

✅ Jika sebaris jawaban berhasil muncul → setup Anda sudah berhasil.
❌ Jika muncul error → simpan screenshot dan hubungi penyelenggara **sebelum** Day-1 dimulai.

#### Step 7 — Verifikasi Dev Server Next.js

```bash
npm run dev
```

Buka http://localhost:3000 — halaman default `fin-app` harus muncul. Hentikan dengan `Ctrl+C`.

### 3.3 H-1 — Pengecekan Akhir

- [ ] Laptop terisi penuh, jangan lupa membawa charger
- [ ] Mouse eksternal (opsional, namun membantu kenyamanan)
- [ ] Headset (jika Anda mengikuti sesi hybrid atau online)
- [ ] Kuota internet cadangan (tethering dari ponsel) untuk berjaga-jaga jika WiFi bermasalah
- [ ] Buku catatan dan pulpen untuk mencatat konsep
- [ ] Tutup aplikasi berat yang tidak diperlukan (Slack, Spotify masih boleh; namun proyek IDE yang berat sebaiknya ditutup)

### 3.4 Day-1 Pagi — Sebelum Sesi Dimulai

- [ ] Datang 30 menit lebih awal untuk registrasi
- [ ] Sambungkan laptop ke WiFi ruang kelas
- [ ] Verifikasi API key masih aktif (jalankan ulang `node --env-file=.env.local smoke-test.mjs`)
- [ ] Tarik versi terbaru repo: `git pull origin main`

---

## 4. Bantuan & Eskalasi

Jika Anda mengalami kendala, gunakan tabel berikut untuk menentukan saluran yang tepat:

| Masalah                         | Hubungi                                |
| ------------------------------- | -------------------------------------- |
| Pendaftaran & administrasi      | Multimatics — www.multimatics.co.id    |
| Setup teknis (Node.js / Supabase / API / dll.) | Penyelenggara via channel komunikasi resmi pelatihan |
| API key tidak berfungsi         | Penyelenggara (untuk pengecekan kuota dan billing) |
| Pertanyaan materi & repo        | Buka issue di GitHub repo ini          |

---

## 5. Referensi Lanjutan

- [`README.md`](README.md) — overview pelatihan
- [`REQUIREMENTS-Spek-Komputer-Aplikasi.md`](REQUIREMENTS-Spek-Komputer-Aplikasi.md) — detail spesifikasi hardware dan software
- [`pretest/PRETEST-AI-Claude.md`](pretest/PRETEST-AI-Claude.md) — pretest peserta
- [`resources/claude-api-cheatsheet.md`](resources/claude-api-cheatsheet.md) — cheatsheet Claude API
- [`resources/references.md`](resources/references.md) — bacaan lanjutan
- Dokumentasi resmi Anthropic: https://docs.anthropic.com

---

*Sudah siap belajar? Silakan lanjut ke [Day-1 — Prompt Engineering](Day-1-Prompt-Engineering/README.md).*
