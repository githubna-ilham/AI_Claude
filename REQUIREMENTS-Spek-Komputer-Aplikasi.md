# Requirements — Spesifikasi Komputer & Aplikasi

> Persyaratan teknis untuk **peserta** dan **fasilitator** pelatihan AI Claude (4 hari).
> Verifikasi semua item ini selesai **H-1** sebelum pelatihan dimulai.
>
> **Catatan stack**: Mulai cohort ini, seluruh hands-on menggunakan **JavaScript/TypeScript (Next.js)**. Tidak lagi menggunakan Python. Alasan: alignment dengan project demo `fin-app` (Next.js + Supabase + Shadcn UI) yang dipakai sebagai backbone hands-on Day 2 hingga Capstone.

---

## A. Spesifikasi Hardware (Laptop Peserta)

### A.1 Minimum (Mampu mengikuti, tapi terbatas)

| Komponen      | Spesifikasi                                  |
| ------------- | -------------------------------------------- |
| **CPU**       | Intel Core i5 gen 8 / AMD Ryzen 5 / Apple M1 |
| **RAM**       | 8 GB                                         |
| **Storage**   | 20 GB free space                             |
| **OS**        | Windows 10/11, macOS 12+, Ubuntu 22.04+      |
| **Display**   | 13" 1080p                                    |
| **Network**   | WiFi 802.11n + ethernet backup               |
| **Battery**   | Min 4 jam (atau colokan tersedia di kursi)   |

### A.2 Direkomendasikan (Lancar untuk semua lab)

| Komponen      | Spesifikasi                                          |
| ------------- | ---------------------------------------------------- |
| **CPU**       | Intel Core i7 gen 11+ / AMD Ryzen 7 / Apple M2/M3/M4 |
| **RAM**       | **16 GB** (paling impactful)                         |
| **Storage**   | 50 GB free SSD                                       |
| **OS**        | Windows 11, macOS 14+, Ubuntu 24.04                  |
| **Display**   | 14"+ 1440p / Retina                                  |
| **Network**   | WiFi 6 + ethernet backup                             |

### A.3 Catatan Penting

- **RAM 8 GB sudah cukup** untuk stack JS (Next.js dev server + browser + editor). RAM 16 GB membuat workflow Day 3-4 (multi-tab + dev server + Supabase Studio) jauh lebih nyaman.
- **GPU tidak wajib.** Inference LLM lewat Claude API (cloud). Embedding lewat Voyage AI (cloud) atau model di Supabase Edge (cloud) — tidak ada beban lokal.
- **Tablet / Chromebook TIDAK direkomendasikan** — banyak lab perlu install Node.js, jalankan dev server lokal, dan operasi terminal.
- **Mouse eksternal** opsional tapi membantu untuk Day 3-4 (banyak coding).

---

## B. Software Wajib (Pre-Install H-3 sampai H-1)

### B.1 Runtime & Bahasa

| Software       | Versi minimum | Wajib?                         | Link install                                  |
| -------------- | ------------- | ------------------------------ | --------------------------------------------- |
| **Node.js**    | **20 LTS+** (idealnya 22 LTS) | **Wajib (default semua lab)** | https://nodejs.org/                           |
| **npm**        | bundled (≥10) | Wajib                          | (ikut Node.js)                                |
| **Git**        | latest        | Wajib                          | https://git-scm.com/downloads                 |

> 💡 **Tips Node.js**: Gunakan **nvm** (macOS/Linux: https://github.com/nvm-sh/nvm, Windows: https://github.com/coreybutler/nvm-windows) untuk manage multiple versi Node.js. Berguna jika peserta sudah memiliki project lain dengan versi Node.js berbeda.

### B.2 Editor / IDE (pilih salah satu)

| Editor                 | Rekomendasi untuk                                    | Link download                                  |
| ---------------------- | ---------------------------------------------------- | ---------------------------------------------- |
| **VS Code**            | Default — paling universal                           | https://code.visualstudio.com/download         |
| **Cursor**             | Rekomendasi #1 (sinergi dengan workflow AI-assisted) | https://cursor.com/download                    |
| **WebStorm**           | Bila peserta sudah biasa JetBrains                   | https://www.jetbrains.com/webstorm/download/   |

**Extension VS Code yang direkomendasikan** (install dari Marketplace tab di dalam VS Code, atau klik link di bawah):

| Extension                              | Fungsi                              | Link Marketplace                                                                                       |
| -------------------------------------- | ----------------------------------- | ------------------------------------------------------------------------------------------------------ |
| **ESLint** (dbaeumer)                  | Linting otomatis                    | https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint                             |
| **Tailwind CSS IntelliSense** (bradlc) | Autocomplete class Tailwind         | https://marketplace.visualstudio.com/items?itemName=bradlc.vscode-tailwindcss                          |
| **Prettier** (esbenp)                  | Format kode otomatis                | https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode                             |
| **GitLens** (eamodio)                  | History git lebih detail di editor  | https://marketplace.visualstudio.com/items?itemName=eamodio.gitlens                                    |

### B.3 Browser

Pilih salah satu (versi terbaru). Disarankan membuat **profile khusus pelatihan** agar terisolasi dari akun pribadi.

| Browser     | Link download                                  |
| ----------- | ---------------------------------------------- |
| **Chrome**  | https://www.google.com/chrome/                 |
| **Edge**    | https://www.microsoft.com/edge/download        |
| **Firefox** | https://www.mozilla.org/firefox/new/           |
| **Brave** (opsional) | https://brave.com/download/           |

### B.4 Tools Tambahan

| Tool                  | Fungsi di pelatihan                          | Wajib? | Link download                                                  |
| --------------------- | -------------------------------------------- | ------ | -------------------------------------------------------------- |
| **Postman**           | Test Claude API request manual               | Opsional | https://www.postman.com/downloads/                           |
| **Insomnia**          | Alternatif Postman (lebih ringan)            | Opsional | https://insomnia.rest/download                                |
| **Supabase CLI**      | Manage migration & local dev Supabase        | Opsional (semua bisa via Supabase Studio web) | https://supabase.com/docs/guides/local-development/cli/getting-started |
| **DBeaver**           | Inspect database Postgres (cross-platform, gratis) | Opsional | https://dbeaver.io/download/                            |
| **TablePlus**         | Alternatif DBeaver (UI lebih modern, free tier) | Opsional | https://tableplus.com/download                             |
| **Slack**             | Channel pelatihan untuk Q&A                  | Wajib (1 dari ini) | https://slack.com/downloads                          |
| **Telegram Desktop**  | Channel pelatihan untuk Q&A                  | Wajib (1 dari ini) | https://desktop.telegram.org/                        |

---

## C. Inisialisasi Project & Package (Install H-1)

Pelatihan ini menggunakan **template project `fin-app`** (Next.js 16 + TypeScript + Tailwind + Shadcn UI) yang akan dikembangkan bertahap dari Day 2 sampai Capstone.

### C.1 Clone Repo Pelatihan

```bash
git clone https://github.com/githubna-ilham/AI_Claude.git
cd AI_Claude
```

### C.2 Clone Template Hands-on (`fin-app`)

Project starter berada di repo terpisah (dishare fasilitator H-3). Setelah di-clone:

```bash
cd fin-app
npm install
```

Perintah `npm install` akan menarik semua dependensi dari `package.json`. Dependensi inti yang digunakan sepanjang pelatihan:

```json
{
  "dependencies": {
    "next": "^16.2.6",
    "react": "^19.2.4",
    "react-dom": "^19.2.4",
    "@anthropic-ai/sdk": "^0.30.0",
    "@supabase/supabase-js": "^2.45.0",
    "zod": "^3.23.0",
    "date-fns": "^4.0.0",
    "voyageai": "^0.0.4"
  },
  "devDependencies": {
    "typescript": "^5",
    "@types/node": "^20",
    "@types/react": "^19",
    "tailwindcss": "^4",
    "@tailwindcss/postcss": "^4",
    "eslint": "^9",
    "eslint-config-next": "^16.2.6"
  }
}
```

> 💡 Daftar di atas adalah **target final** setelah seluruh hari selesai. Beberapa paket (Anthropic SDK, Voyage AI) baru di-install saat hari relevan (Day 2 dan Day 3) — instruksi `npm install` per hari akan ada di materi tiap modul.

### C.3 Verifikasi Instalasi Node.js & npm

```bash
node --version    # harus ≥ v20.x
npm --version     # harus ≥ 10.x
git --version
```

### C.4 Verifikasi Dev Server

```bash
cd fin-app
npm run dev
```

Buka http://localhost:3000 — halaman Next.js default harus muncul. Hentikan dev server dengan `Ctrl+C`.

---

## D. Akun & Layanan Cloud (Setup H-3)

| Layanan                       | Wajib?  | Cara setup                                                    | Catatan biaya                              |
| ----------------------------- | ------- | ------------------------------------------------------------- | ------------------------------------------ |
| **Anthropic Console**         | **WAJIB** | https://console.anthropic.com → sign up → generate API key  | Top-up min $5; pelatihan habiskan ~$2-5/peserta |
| **Supabase**                  | **WAJIB** | https://supabase.com → sign up → buat project baru           | Free tier cukup (500 MB DB, 2 GB bandwidth) |
| **Voyage AI**                 | **WAJIB (Day 3)** | https://www.voyageai.com → sign up → API key            | Free tier cukup untuk pelatihan            |
| **GitHub**                    | Wajib   | Akun GitHub aktif                                             | Free                                       |
| **Google Account**            | Wajib   | Untuk akses Google Form pretest/posttest                      | Free                                       |
| **Vercel**                    | Opsional | https://vercel.com (login dengan GitHub) untuk deploy capstone | Free hobby tier cukup                    |

### D.1 Setup Anthropic API Key

Tiap peserta WAJIB:

1. Generate Anthropic API key dari https://console.anthropic.com/settings/keys
2. Top-up minimum $5 (atau gunakan key yang disediakan fasilitator)
3. Simpan key di file `.env.local` project (bukan environment variable global, supaya tidak bocor ke project lain):

   ```env
   ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxx
   ```

4. Verifikasi (jalankan dari folder `fin-app/` setelah `npm install @anthropic-ai/sdk dotenv`):

   ```bash
   node -e "import('dotenv').then(d=>d.config({path:'.env.local'})).then(()=>import('@anthropic-ai/sdk')).then(({default:Anthropic})=>new Anthropic().messages.create({model:'claude-haiku-4-5',max_tokens:20,messages:[{role:'user',content:'ping'}]})).then(r=>console.log(r.content[0].text))"
   ```

   Hasil yang diharapkan: muncul respons singkat dari Claude di terminal.

### D.2 Setup Supabase Project

1. Buat project baru di https://supabase.com/dashboard → **New project**
2. Pilih region terdekat (Singapore untuk Indonesia)
3. Tunggu provisioning ~2 menit, lalu masuk ke **Project Settings → API**
4. Catat 2 nilai ini ke `.env.local`:

   ```env
   NEXT_PUBLIC_SUPABASE_URL=https://xxxxxxxx.supabase.co
   SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJI...
   ```

5. (Day 3 only) Aktifkan extension **`vector`** untuk RAG:
   - Buka **Database → Extensions** → search `vector` → enable. Detail penggunaan dibahas di materi Day 3.

### D.3 Setup Voyage AI (Day 3)

1. Sign up di https://www.voyageai.com
2. Generate API key, tambahkan ke `.env.local`:

   ```env
   VOYAGE_API_KEY=pa-xxxxxxxxxxxx
   ```

### D.4 `.env.local` Template Lengkap

Setiap project pakai `.env.local` (Next.js convention) — jangan commit ke git:

```env
# Anthropic (Day 2+)
ANTHROPIC_API_KEY=sk-ant-api03-...

# Supabase (Day 2+)
NEXT_PUBLIC_SUPABASE_URL=https://xxxxxxxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJI...

# Voyage AI (Day 3)
VOYAGE_API_KEY=pa-...
```

Pastikan `.gitignore` berisi (Next.js default sudah cover, tapi worth checking):

```
.env*.local
node_modules/
.next/
```

---

## E. Per-Hari Yang Perlu Disiapkan

### Day 1 — Prompt Engineering Fundamentals

**Peserta cukup browser + akun Anthropic Console. Belum perlu coding.**

- [ ] Akses https://claude.ai (free tier OK, Pro lebih nyaman)
- [ ] Akses https://console.anthropic.com/workbench (untuk demo parameter + prefill)
- [ ] Pretest sudah diisi

### Day 2 — AI Workflow & Agent (dengan `fin-app`)

**Mulai coding dengan stack JavaScript:**

- [ ] Node.js 20+ ter-install (`node --version`)
- [ ] Repo `fin-app` sudah di-clone, `npm install` jalan tanpa error
- [ ] `npm run dev` berhasil menampilkan halaman di http://localhost:3000
- [ ] Anthropic API key sudah di `.env.local` + verifikasi smoke test JS jalan
- [ ] Supabase project sudah dibuat, URL + service-role key di `.env.local`
- [ ] Editor (VS Code / Cursor) + ESLint + Tailwind IntelliSense terinstal

### Day 3 — AI App + RAG (dengan Supabase pgvector)

**Paling intensive setup:**

- [ ] Extension `vector` (pgvector) di Supabase project sudah enabled
- [ ] Voyage AI key sudah di `.env.local`
- [ ] Sample dokumen sudah ada di folder lab (disediakan fasilitator)
- [ ] Disk space cek: minimum 5 GB free (untuk dependencies + sample data)
- [ ] Browser bisa akses Supabase Studio (kadang diblokir corporate proxy)

### Day 4 — Product, Governance, Capstone

- [ ] Slide deck tool: Google Slides / Keynote / PowerPoint
- [ ] Optional: Figma / Excalidraw / Miro untuk diagram arsitektur
- [ ] Optional: akun Vercel (login dgn GitHub) untuk deploy capstone
- [ ] Form rubrik (Google Form) sudah dibuat oleh fasilitator
- [ ] Backup API key budget untuk capstone (tiap tim bisa pakai 50-100 calls demo)

---

## F. Setup untuk Fasilitator (Tambahan)

### F.1 Hardware Fasilitator

| Komponen       | Spesifikasi                              |
| -------------- | ---------------------------------------- |
| Laptop         | Spek **direkomendasikan** (A.2), 16 GB RAM |
| Layar tambahan | Untuk presentasi + notes                 |
| HDMI/USB-C adapter | Untuk proyektor ruang kelas          |

### F.2 Software Fasilitator

- Semua yang ada di B + C + D
- **Anthropic Console** dengan **budget cukup** ($50-100 untuk demo intensif 4 hari)
- **Supabase Pro** (opsional, hanya jika peserta ramai dan free tier tidak cukup untuk demo session)
- **OBS / Loom** untuk rekaman sesi (jika perlu)
- **Screen annotation tool** (Annotate, Presentify) untuk highlight saat demo
- **Timer / stopwatch** (banyak lab time-boxed)

### F.3 Konten yang Harus Siap

- [ ] Slide presentasi per Module (slide deck di-export dari `materi.md`)
- [ ] Repo `fin-app` versi starter (iterasi 1 selesai) sudah di-share H-3
- [ ] Sample dokumen HR (PDF kebijakan cuti, SOP DOCX, FAQ CSV) di `lab-day-3/sample_docs/`
- [ ] 5 contoh deskripsi transaksi bahasa Indonesia untuk Lab Day 2 (auto-categorize)
- [ ] Golden Q&A set 10-20 pasang untuk eval RAG Day 3
- [ ] Mock data transaksi (CSV / SQL seed) untuk Capstone
- [ ] PDF dummy berisi indirect prompt injection untuk demo Module 14
- [ ] Cetak: Use Case Canvas A3 (1/peserta), checklist Responsible AI, OWASP LLM Top 10

### F.4 Backup Plan

- **API key cadangan** bila key utama kena rate limit
- **Hotspot 4G/5G** bila WiFi ruang kelas drop
- **Snapshot Supabase project** (export SQL) siap untuk peserta yang ketinggalan migration
- **Pre-recorded demo video** untuk segmen kritis bila live demo gagal
- **Pre-seeded Supabase project** sebagai fallback bila peserta gagal setup Supabase sendiri

---

## G. Setup untuk Ruang Pelatihan

| Item                          | Spesifikasi                                     |
| ----------------------------- | ----------------------------------------------- |
| **Proyektor / TV**            | Min 4K untuk teks code yang jelas              |
| **Audio**                     | Wireless mic + speaker                          |
| **Internet**                  | Min 50 Mbps untuk 15-20 peserta, redundant      |
| **Power outlet**              | 1 colokan per peserta minimum                   |
| **Whiteboard / flipchart**    | Untuk Module 7-8 (diagram agent), Module 13 (canvas) |
| **AC / sirkulasi**            | Banyak laptop = panas                           |
| **Snack & kopi**              | Sesi intensif 8 jam butuh asupan                |

---

## H. Checklist Final (H-1)

**Untuk Peserta:**

- [ ] Hardware memenuhi minimum (idealnya direkomendasikan)
- [ ] Node.js 20+ & Git terinstal
- [ ] Editor (VS Code / Cursor) + extensions terinstal
- [ ] Repo `fin-app` sudah di-clone, `npm install` & `npm run dev` jalan
- [ ] Anthropic API key didapat & ada di `.env.local`
- [ ] Supabase project dibuat, URL + service-role key di `.env.local`
- [ ] Voyage AI key (untuk Day 3) ada di `.env.local`
- [ ] Akun GitHub aktif
- [ ] Pretest sudah diisi
- [ ] Test ping API berhasil (smoke test JS)
- [ ] Browser dengan profile pelatihan

**Untuk Fasilitator:**

- [ ] Semua di atas (sebagai backup demo)
- [ ] Slide deck final per Module
- [ ] Repo `fin-app` starter sudah di-share ke peserta
- [ ] Sample data & golden set sudah disiapkan
- [ ] API key budget cukup ($50-100)
- [ ] Aset cetak (Canvas A3, checklist)
- [ ] Ruang kelas tervalidasi (proyektor, internet, listrik)
- [ ] Backup plan teruji (hotspot, pre-seeded Supabase, video)

---

## I. FAQ Singkat

**Q: Kenapa pakai JavaScript / TypeScript, bukan Python?**
A: Stack hands-on pelatihan ini terpusat pada project `fin-app` (Next.js + Supabase + Shadcn UI). Dengan JS/TS sebagai bahasa tunggal, peserta tidak perlu konteks switching antara backend Python + frontend JS — semua dalam satu codebase yang sama. Konsep prompting, workflow, dan agent **fully transferable** ke Python jika peserta perlu di project lain.

**Q: Apakah harus pakai Mac?**
A: Tidak. Windows / Linux / Mac semuanya kompatibel. Mac M-series + Windows + Linux semua menjalankan Node.js dengan lancar.

**Q: Berapa biaya total Anthropic API untuk 1 peserta 4 hari?**
A: Estimasi $2-5 untuk semua hands-on bila peserta tertib (pakai Haiku untuk task ringan, Sonnet untuk yang perlu kualitas). Top-up $10 sudah aman.

**Q: Apakah bisa offline?**
A: TIDAK. Claude API, Supabase, dan Voyage AI semuanya cloud-based. Internet stabil mutlak diperlukan.

**Q: Apakah bisa pakai LLM open-source (Llama, Mistral)?**
A: Konsep prompting & agent transferable, tapi materi pelatihan ini spesifik Claude API (tool use format, prompt caching, dll.). Untuk Capstone bila ingin demo dengan LLM lokal, perlu adaptasi pribadi.

**Q: Boleh pakai akun Anthropic team / organization?**
A: Boleh, dan justru lebih praktis untuk fasilitator (1 API key, multiple users via metadata).

**Q: Bagaimana kalau peserta belum punya kartu kredit untuk Anthropic?**
A: Fasilitator sediakan API key bersama dengan budget tracking per user via `metadata.user_id`.

**Q: Saya sudah punya Node.js versi lain (mis. 18). Harus uninstall?**
A: Tidak. Pakai **nvm** untuk switch versi: `nvm install 20 && nvm use 20`. Project-local `.nvmrc` di repo `fin-app` akan otomatis pakai versi yang sesuai.

**Q: Supabase free tier cukup tidak untuk pelatihan?**
A: Cukup. 500 MB database + 2 GB bandwidth jauh di atas kebutuhan pelatihan. Project bisa di-pause setelah pelatihan untuk hemat kuota.

**Q: Saya tidak familiar dengan React / Next.js. Apakah masih bisa ikut?**
A: Bisa. Day 1 sama sekali tidak menyentuh kode. Day 2-4 fokus integrasi Claude — kode React/Next.js sudah disediakan via `fin-app` starter, peserta hanya perlu **modify dan tambahkan logic AI** di file yang sudah ditunjuk. Tidak ada lab yang minta peserta menulis komponen React dari nol.
