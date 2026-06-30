# Module 01 — Setup Project & Claude Code

> **Tujuan modul**: Anda siap melakukan coding di project Fina App dengan **Claude Code** sebagai *AI pair-programmer* di terminal.
>
> **Output akhir modul ini**: project Fina App ter-clone, dependencies terpasang, dev server berjalan, dan Claude Code aktif di working directory.

---

## Apa yang Akan Anda Pelajari

Setelah menyelesaikan modul ini, Anda akan mampu:

1. Menjelaskan **Claude Code** dan posisinya dibanding alat lain seperti ChatGPT atau GitHub Copilot.
2. Membedakan **Claude Code (CLI)**, **Claude Desktop**, dan **Claude.ai (web)**, serta memilih yang tepat untuk setiap kebutuhan.
3. Memasang dan memverifikasi Claude Code di terminal.
4. Meng-clone project starter Fina App dan menginstal dependencies-nya.
5. Menjalankan **smoke test** — dev server pertama kali dengan `.env.local` kosong, untuk memastikan tampilan dasar terbuka tanpa kesalahan pada stack development.
6. Memahami konsep **Supabase** (Backend-as-a-Service berbasis Postgres) sebagai fondasi data project.
7. Memahami konsep **pgvector** sebagai fondasi *semantic search* untuk fitur AI yang akan Anda bangun.
8. Membuat **project Supabase** pribadi dari nol.
9. Menjalankan **migration SQL** sehingga skema database siap pakai.
10. Memasukkan **contoh data transaksi** ke database.
11. Mengisi `.env.local` dengan credential Supabase Anda, lalu memverifikasi koneksi melalui dashboard.

**Durasi belajar**: ±90 menit (santai) atau 50 menit (untuk yang sudah familiar dengan stack development Node.js / Next.js).

---

## Prasyarat (Wajib Sudah Terpasang)

Sebelum memulai, pastikan tool berikut sudah tersedia di komputer Anda:

| Tool | Versi minimum | Cek dengan |
|---|---|---|
| **Node.js** | 20.x atau lebih baru | `node -v` |
| **npm** | 10.x atau lebih baru | `npm -v` |
| **Git** | 2.x | `git --version` |
| **VS Code** (atau editor lain) | terbaru | `code --version` |

Jika ada yang belum terpasang, silakan ikuti panduan instalasi resmi dari masing-masing tool.

> 💡 **Tip**: Pada macOS dan Linux, seluruh tool tersebut dapat dipasang lewat **Homebrew**:
> ```bash
> brew install node git
> brew install --cask visual-studio-code
> ```

---

## 1. Apa itu Claude Code?

**Claude Code** adalah CLI (Command Line Interface) dari Anthropic yang menjalankan Claude — model AI mereka — **langsung di terminal Anda**, lengkap dengan akses ke filesystem project.

Berbeda dengan ChatGPT atau Copilot, Claude Code dirancang untuk **bekerja bersama Anda di dalam project**, bukan sekadar menjawab pertanyaan dari luar.

| Aspek | Claude Code | ChatGPT (web/desktop) | GitHub Copilot |
|---|---|---|---|
| **Tempat berjalan** | Terminal di folder project | Browser/aplikasi terpisah | Inline di editor |
| **Akses file** | ✅ Membaca/mengedit file secara langsung | ❌ Perlu copy-paste manual | ✅ Tetapi konteksnya terbatas |
| **Eksekusi command** | ✅ `npm install`, `git`, dan lain-lain | ❌ | ❌ |
| **Tugas multi-langkah** | ✅ Dapat merencanakan dan menjalankan rangkaian aksi | ❌ Manual per langkah | ❌ Hanya auto-complete |
| **Cocok untuk** | Workflow coding penuh | Diskusi / tanya jawab | Auto-complete cepat |

Pada Day 2 ini, Claude Code akan berperan sebagai ***pair programmer***: Anda memberi instruksi dalam bahasa natural ("buatkan halaman transactions dengan tabel"), lalu Claude akan menulis kode, mengedit file, menjalankan perintah, dan menjelaskan apa yang sedang dikerjakannya.

---

## 2. Claude Code (CLI) vs Claude Desktop vs Claude.ai (web)

Anthropic menyediakan **tiga cara** untuk berinteraksi dengan Claude. Memahami perbedaannya akan membantu Anda memilih alat yang tepat untuk situasi yang tepat.

### Tabel Perbandingan

| Aspek | **Claude Code (CLI)** | **Claude Desktop** | **Claude.ai (web)** |
|---|---|---|---|
| **Bentuk** | Terminal / CLI | Aplikasi native (macOS, Windows) | Browser |
| **UI** | Text-only, REPL | GUI chat, nyaman | GUI chat |
| **Akses filesystem** | ✅ Langsung (read/edit file) | ⚠️ Melalui MCP server | ❌ Tidak |
| **Eksekusi command (bash, git, npm)** | ✅ Tersedia secara default | ⚠️ Melalui MCP | ❌ |
| **Edit kode multi-file** | ✅ Optimal | ⚠️ Mungkin, tetapi kurang nyaman | ❌ |
| **Diskusi / brainstorming** | ⚠️ Memadai, namun text-only | ✅ Nyaman | ✅ Nyaman |
| **Upload gambar / dokumen** | ✅ Lewat path file | ✅ Drag & drop | ✅ Drag & drop |
| **Projects (context library)** | ❌ (menggunakan folder) | ✅ | ✅ |
| **MCP servers** (integrasi tool eksternal) | ✅ Konfigurasi melalui settings | ✅ Setup GUI | ❌ |
| **Skill / agent custom** | ✅ | ⚠️ Terbatas | ❌ |
| **Mode suara (audio)** | ❌ | ✅ | ✅ |
| **Cocok untuk** | Coding, otomasi, tugas multi-langkah | Brainstorm + eksekusi sesekali | Tanya jawab cepat di mana saja |

### Kapan Memakai yang Mana?

**Gunakan Claude Code (CLI) ketika:**
- Anda sedang melakukan **coding pada project nyata**.
- Anda membutuhkan Claude untuk **mengeksekusi perintah** (instalasi package, menjalankan test, commit ke Git).
- Anda ingin Claude **mengedit banyak file** dalam satu instruksi.
- Anda mengerjakan **otomasi**: skill custom, hooks, atau scheduled run.
- Anda bekerja di **server remote** melalui SSH — CLI tetap dapat berjalan.

**Gunakan Claude Desktop ketika:**
- Anda ingin **berdiskusi panjang** sambil melihat preview/gambar.
- Anda melakukan **riset atau brainstorming** dengan banyak dokumen yang perlu di-upload.
- Anda ingin memanfaatkan fitur **Projects** untuk menyimpan konteks (misalnya dokumentasi internal).
- Anda membutuhkan **mode suara** untuk berinteraksi secara audio.
- Anda ingin menyiapkan **MCP server** dengan antarmuka grafis yang lebih ramah pengguna.

**Gunakan Claude.ai (web) ketika:**
- Anda bekerja di komputer publik atau orang lain, **tidak dapat memasang aplikasi**.
- Anda hanya membutuhkan **jawaban singkat** dari Claude.
- Anda mengakses dari **perangkat mobile atau tablet**.

### Gambaran Praktis pada Day 2

| Tahap pekerjaan | Tool yang ideal |
|---|---|
| Brainstorming "fitur AI apa yang cocok untuk tracker keuangan?" | Claude Desktop / Web |
| "Bacakan codebase ini, jelaskan alur datanya" | Claude Code |
| "Edit `page.tsx`, ubah judul menjadi X" | Claude Code |
| "Bantu saya menyusun prompt untuk Claude API" | Claude Desktop / Web |
| Setup environment, install dependency, jalankan migration | Claude Code |
| Mendiskusikan UX/copy dengan upload screenshot | Claude Desktop |

> 💡 **Dapat digunakan bersamaan**. Banyak developer terbiasa menggunakan Claude Desktop untuk brainstorming dan diskusi, lalu beralih ke Claude Code untuk eksekusi. Pola ini sangat produktif.

---

## 3. Install Claude Code

### macOS / Linux

Buka terminal, lalu jalankan perintah berikut:

```bash
npm install -g @anthropic-ai/claude-code
```

Atau menggunakan installer resmi:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

### Windows

Gunakan PowerShell (jalankan sebagai Administrator untuk instalasi pertama):

```powershell
npm install -g @anthropic-ai/claude-code
```

Atau melalui **WSL2** (sangat direkomendasikan): pasang Ubuntu di WSL2, buka terminal Ubuntu, lalu jalankan perintah macOS/Linux di atas.

### Verifikasi Instalasi

```bash
claude --version
```

Apabila berhasil, terminal akan menampilkan nomor versi (contoh: `claude-code 1.x.x`). Jika muncul pesan `command not found`, periksa apakah path global npm sudah terdaftar di `$PATH`:

```bash
npm config get prefix
# Contoh hasil: /Users/anda/.npm-global atau /usr/local
# Pastikan path tersebut ada di $PATH (di ~/.zshrc atau ~/.bashrc)
```

---

## 4. Login & Setup Pertama

Jalankan Claude Code untuk pertama kalinya:

```bash
claude
```

Anda akan diminta untuk:

1. **Login** — Claude Code akan menampilkan URL. Buka URL tersebut di browser, kemudian login menggunakan akun Claude Anda (atau buat akun baru di [claude.ai](https://claude.ai)).
2. **Permission mode** — pilih `Default` untuk sesi ini. Anda dapat menaikkan level kewenangan di kemudian hari ketika sudah lebih familiar.

Setelah login, Anda akan masuk ke **REPL interaktif**. Cobalah prompt sederhana berikut:

```
> halo, apa yang dapat kamu lakukan?
```

Claude akan merespons dengan ringkasan kemampuannya. Selamat — instalasi Anda berhasil.

Untuk keluar dari REPL: tekan `Ctrl+C` dua kali, atau ketik `/exit`.

---

## 5. Clone Project Starter Fina App

> 📦 **URL repository**: `https://github.com/githubna-ilham/fina-app-starter.git`

Buka terminal, lalu siapkan folder kerja untuk project (sebagai contoh `~/Projek/`):

```bash
mkdir -p ~/Projek && cd ~/Projek
git clone https://github.com/githubna-ilham/fina-app-starter.git fina-app
cd fina-app
```

Setelah proses clone selesai, struktur folder yang akan Anda temui kurang lebih seperti berikut:

```
fina-app/
├── public/
├── src/
│   ├── app/                 # Halaman Next.js (App Router)
│   ├── components/          # Komponen UI (Shadcn + custom)
│   ├── features/            # Server actions (lapisan data)
│   ├── lib/                 # Helper: format, supabase clients
│   ├── providers/           # React context providers
│   └── proxy.ts             # Next.js middleware (nama baru)
├── supabase/
│   └── migrations/          # SQL migrations untuk Supabase
│       ├── 0001_init.sql
│       └── 0002_match_transactions.sql
├── package.json
├── .env.example             # Template env vars
└── README.md
```

---

## 6. Install Dependencies

```bash
npm install
```

Tunggu sekitar 1–2 menit. Beberapa package utama yang akan terunduh antara lain:

- Next.js, React, TypeScript
- Dependencies Shadcn UI (Radix, Tailwind)
- Supabase SDK (`@supabase/supabase-js`, `@supabase/ssr`)
- TanStack Query
- Lucide icons, recharts, dan lain-lain

Jika muncul pesan warning seperti `npm warn deprecated …`, Anda dapat mengabaikannya — hal ini wajar pada proses instalasi.

Apabila yang muncul adalah **error** `npm ERR! …`, kemungkinan besar disebabkan versi Node.js yang belum sesuai. Pastikan Node.js yang terpasang adalah versi 20 atau lebih baru.

---

## 7. Smoke Test — Jalankan Dev Server Pertama Kali

Sebelum membahas konsep Supabase dan pgvector secara mendalam, pastikan terlebih dahulu bahwa project Anda sudah dapat berjalan. Smoke test ini hanya memerlukan beberapa menit, tetapi akan membantu mendeteksi masalah pada stack development (Node.js, npm, TypeScript, Next.js) sejak dini — sebelum Anda terbenam dalam topik berikutnya.

### 7.1 Siapkan File `.env.local` (Kosong Dulu)

Project starter membutuhkan keberadaan `.env.local` agar Next.js tidak mengeluarkan peringatan. Salin dari template yang tersedia:

```bash
cp .env.example .env.local
```

Untuk smoke test ini, **biarkan nilainya tetap berupa placeholder atau kosong**. Anda akan mengisinya dengan credential asli pada Step 13, setelah project Supabase Anda siap.

```env
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=
```

> 💡 **Mengapa setiap peserta perlu membuat project Supabase sendiri?** Agar database setiap peserta **terisolasi** (data tidak bercampur), dan Anda dapat mempelajari **alur setup dari nol** — bukan sekadar menyalin credential orang lain.

### 7.2 Jalankan Dev Server

Pada terminal di folder project, jalankan:

```bash
npm run dev
```

Output yang akan muncul kurang lebih seperti berikut:

```
▲ Next.js 16.2.6 (Turbopack)
- Local:        http://localhost:3000
- Network:      http://172.16.x.x:3000

✓ Ready in 381ms
```

Buka **http://localhost:3000** di browser Anda.

### 7.3 Apa yang Akan Anda Lihat?

- **Sidebar** di sisi kiri dengan brand "Fina App" beserta dua menu: Dashboard dan Transaction.
- **Dashboard header** ditambah 3 stat card (Savings / Incomes / Expenses).
- **Seluruh angka bernilai Rp 0** atau menampilkan tanda **—** — karena Supabase belum terhubung (environment variable masih kosong).
- Mungkin muncul beberapa **error pada console browser** (`Failed to fetch` atau sejenisnya) — hal ini wajar dan akan hilang setelah Supabase terhubung pada Step 13.

Apabila ketiga elemen di atas (sidebar, header, stat card) tampil dengan benar, **smoke test Anda berhasil**. Project siap untuk dikoneksikan ke Supabase.

### 7.4 Tes Claude Code di Project

Buka terminal **baru** pada folder project (atau gunakan split terminal). Jalankan:

```bash
claude
```

Coba berikan prompt berikut:

```
> jelaskan struktur folder src/ di project ini
```

Claude akan membaca filesystem dan memberikan penjelasan singkat mengenai peran setiap folder. **Inilah tool utama yang akan Anda andalkan sepanjang Day 2.**

> 💡 **Tip**: biarkan dev server tetap berjalan di terminal pertama. Selama Anda mengubah file, halaman akan otomatis *hot reload*. Apabila perlu menjalankan perintah lain (instalasi package, git, dll.), gunakan terminal kedua.

---

## 8. Apa itu Supabase?

**Supabase** adalah platform Backend-as-a-Service (BaaS) yang **open-source**. Ia sering disebut sebagai "alternatif Firebase yang berdiri di atas Postgres".

Secara ringkas, Supabase menyediakan **database, autentikasi, storage, realtime, dan edge functions** dalam satu dashboard — tanpa Anda perlu menyiapkan server sendiri.

### Komponen yang Disediakan Supabase

| Komponen | Fungsi | Digunakan di project? |
|---|---|---|
| **Postgres Database** | Database relasional production-grade | ✅ (tabel `transactions`) |
| **Auth** | Login email/password, OAuth (Google, GitHub), magic link | ⏳ Belum digunakan (kolom `user_id` sudah disiapkan) |
| **Storage** | Penyimpanan file (gambar, PDF) seperti S3 | ❌ Tidak diperlukan |
| **Realtime** | Subscribe perubahan data melalui WebSocket | ❌ Belum |
| **Edge Functions** | Serverless function berbasis Deno | ❌ Belum |
| **Extensions** | Plugin Postgres seperti pgvector, PostGIS | ✅ (`vector`, `pgcrypto`) |

### Mengapa Memilih Supabase?

| Pilihan | Kelebihan | Kekurangan |
|---|---|---|
| **Supabase** | Open-source, kekuatan penuh Postgres, free tier murah hati, SQL standar | Vendor-managed sehingga ada limit pada free tier |
| **Firebase** | Sudah matang, kuat untuk mobile, fitur realtime | NoSQL (Firestore) — query terbatas, *vendor lock-in* |
| **Raw Postgres + Node** | Kontrol penuh, gratis selamanya | Anda harus menyiapkan sendiri server, deployment, backup, dan scaling |
| **PlanetScale / Neon** | Serverless Postgres/MySQL, cepat | Hanya database, autentikasi dan storage perlu setup tambahan |

Untuk aplikasi **berbasis Postgres** yang nantinya membutuhkan **fitur AI** (pgvector) ditambah autentikasi dan storage di masa depan, Supabase merupakan **pilihan default yang masuk akal**.

### Konsep Penting di Supabase

1. **Project** — satu instance Postgres beserta dashboard-nya. Setiap peserta workshop ini akan memiliki project sendiri.
2. **API Keys** — terdiri dari dua jenis:
   - **Publishable key** (`sb_publishable_…`) — aman untuk digunakan di browser, RLS yang akan membatasi akses.
   - **Secret key** (`sb_secret_…`) — bypass RLS, **wajib disimpan di server**, dan **tidak boleh** dibocorkan ke client.
3. **Row Level Security (RLS)** — fitur Postgres yang membatasi akses per-baris berdasarkan policy. Wajib aktif di Supabase, karena inilah satu-satunya pembatas akses untuk publishable key.
4. **Auth schema** — Supabase secara otomatis membuat schema `auth` beserta tabel `users`. Apabila menggunakan autentikasi, foreign key dapat diarahkan ke `auth.users(id)`.

### Tier Pricing (per November 2026 — sewaktu-waktu dapat berubah)

| Plan | Database | Bandwidth | Auth users | Harga |
|---|---|---|---|---|
| **Free** | 500 MB | 5 GB | 50.000 MAU | $0 |
| **Pro** | 8 GB | 250 GB | 100.000 MAU | ±$25/bulan |
| **Team / Enterprise** | Custom | Custom | Custom | Sesuai kesepakatan |

Untuk keperluan workshop ini dan aplikasi personal seperti Fina App, **Free tier sudah lebih dari cukup**.

> 💡 **Free tier** Supabase akan **mem-pause** project apabila tidak aktif selama 7 hari. Anda dapat meng-unpause-nya secara manual dari dashboard tanpa kehilangan data.

---

## 9. Apa itu pgvector?

**pgvector** adalah **extension PostgreSQL** yang menambahkan tipe data `vector` beserta operator untuk **similarity search**. Extension ini merupakan **dasar teknologi** RAG (Retrieval-Augmented Generation) dan semantic search pada aplikasi AI modern.

### Mengapa Perlu Vector?

Sebuah **embedding model** (misalnya dari Claude, OpenAI, Voyage, atau Gemini) mengubah teks menjadi **array angka yang panjang** (vector). Angka-angka tersebut **merepresentasikan makna**, bukan sekadar urutan kata.

Berikut ilustrasi konseptual (di dunia nyata, embedding umumnya memiliki 768–3072 dimensi):

```
"makan kopi pagi"   → [0.12, -0.04, 0.88, 0.31, …, 0.07]  (1024 angka)
"ngopi sarapan"     → [0.10, -0.05, 0.86, 0.30, …, 0.08]  (sangat mirip)
"bayar cicilan KPR" → [-0.42, 0.91, 0.05, -0.66, …, 0.21] (jauh berbeda)
```

Dua teks dengan **makna yang serupa** akan menghasilkan vector yang **berdekatan** dalam ruang 1024 dimensi, meskipun kata-katanya berbeda.

### Apa yang Diberikan pgvector

1. **Tipe data baru**:
   ```sql
   create table transactions (
     ...
     embedding vector(1024)
   );
   ```

2. **Operator distance**:

   | Operator | Arti | Range hasil |
   |---|---|---|
   | `<->` | L2 (Euclidean) distance | 0..∞ |
   | `<#>` | Negative inner product | -∞..∞ |
   | `<=>` | **Cosine distance** | 0..2 |

   Untuk data teks, operator yang paling sering digunakan adalah **`<=>`** (cosine distance). Nilai `1 - (a <=> b)` setara dengan cosine similarity (range 0..1, semakin tinggi semakin mirip).

3. **Index ANN** (Approximate Nearest Neighbor):
   - **HNSW** — *Hierarchical Navigable Small World*. Cepat dan akurat. Inilah yang digunakan di project ini.
   - **IVFFlat** — proses build lebih cepat, namun memerlukan tuning parameter `lists`.

   Tanpa index, semantic search pada 1 juta baris berarti scan satu per satu (lambat). Dengan HNSW, kompleksitasnya menjadi O(log n) — hanya beberapa millisecond.

### Use Case di Fina App

Pada kolom `embedding vector(1024)`, aplikasi menyimpan **representasi makna** dari `description + category` setiap transaksi.

**Workflow yang akan dibangun** (di modul lanjutan):

```
Step 1: User memasukkan transaksi "Kopi pagi di kafe sebelah" dengan kategori Food
   → Aplikasi memanggil embedding model → menerima [0.12, -0.04, …] (1024 angka)
   → Simpan ke kolom embedding

Step 2: User bertanya di chat: "berapa total saya beli kopi minggu lalu?"
   → Aplikasi mengubah pertanyaan menjadi embedding query
   → Memanggil function match_transactions(query_embedding, 0.7, 10)
   → Postgres memanfaatkan HNSW index, mengembalikan 10 transaksi paling mirip
     (termasuk "Kopi pagi di kafe sebelah", meskipun pertanyaannya tidak
      menyebut frasa "kafe sebelah")
   → Aplikasi memformat jawaban menggunakan Claude API
```

### Function yang Sudah Disiapkan

Pada project starter sudah tersedia function **`match_transactions`** di `supabase/migrations/0002_match_transactions.sql`. Function ini memiliki karakteristik:

- **Input**: `query_embedding`, `match_threshold` (0..1), `match_count` (limit hasil).
- **Output**: kolom-kolom transaksi disertai skor `similarity`.
- **Optimasi**: memanfaatkan HNSW index sehingga query berjalan cepat.

> 📖 Penjelasan lengkap mengenai migration ini tersedia pada `docs/penjelasan-migrasi-database.md` di repository project.

### Mengapa Memilih Dimensi 1024?

Setiap embedding model memiliki dimensi output yang berbeda-beda:

| Model | Dimensi |
|---|---|
| Sentence-Transformers `all-MiniLM-L6-v2` | 384 |
| Voyage AI `voyage-3-lite` | 512 |
| Gemini `text-embedding-004` | 768 |
| **Voyage AI `voyage-3`** | **1024** |
| Cohere `embed-multilingual-v3` | 1024 |
| OpenAI `text-embedding-3-small` | 1536 (dapat di-shrink) |
| OpenAI `text-embedding-3-large` | 3072 |

Project starter ini menggunakan dimensi **1024** agar selaras dengan **Voyage AI `voyage-3`** — embedding model yang direkomendasikan resmi oleh Anthropic dan akan dipakai pada Module 06 (Embedding) untuk fitur AI Financial Advisor. **Dimensi vector pada tabel HARUS sama persis dengan output model embedding** yang digunakan. Apabila nantinya Anda mengganti model, dimensi kolom perlu disesuaikan dan seluruh data perlu di-embed ulang.

### Status di Project

Pada saat clone, file migration sudah tersedia namun **belum dijalankan** di database. Pada Step 11 berikutnya, Anda akan:

1. Membuat project Supabase pribadi.
2. Mengaktifkan extension `vector` (secara otomatis melalui migration).
3. Menjalankan kedua migration di SQL Editor.

Sebelum eksekusi tersebut, cukup pahami **konsep dasarnya** terlebih dahulu: pgvector merupakan jembatan antara **database** dan **kemampuan AI semantik**.

---

## 10. Membuat Project Supabase

Pada langkah ini, Anda akan membuat sebuah project Supabase yang akan menjadi backend dari Fina App Anda pribadi.

### 11.1 Sign Up / Login

1. Buka **https://supabase.com/dashboard** pada browser.
2. Klik **Sign in with GitHub** (cara tercepat) atau gunakan email.
3. Setelah login, Anda akan diarahkan ke halaman dashboard.

### 11.2 Buat Project Baru

1. Klik tombol **New project** di pojok kanan atas.
2. Isi formulir:
   - **Organization**: pilih organisasi default (atau buat baru apabila diminta).
   - **Project name**: `fina-app` (boleh nama lain).
   - **Database Password**: buat password yang kuat. **Simpan password ini di password manager** Anda. Supabase tidak akan menampilkannya kembali.
   - **Region**: pilih **Southeast Asia (Singapore)** — server terdekat dari Indonesia untuk latensi rendah.
   - **Plan**: **Free**.
3. Klik **Create new project**.
4. Tunggu sekitar 2 menit hingga proses provisioning selesai (akan ditampilkan progress bar).

> 💡 **Catatan tentang Database Password**: untuk Fina App, password ini sebenarnya jarang Anda gunakan — komunikasi dengan Supabase dilakukan melalui API key, bukan password DB. Walaupun demikian, password tetap perlu disimpan baik-baik untuk keperluan administrasi (misalnya koneksi `psql` langsung di kemudian hari).

### 11.3 Verifikasi Project Aktif

Setelah provisioning selesai, Anda akan masuk ke dashboard project. Pada sidebar kiri akan tampak menu seperti **Table Editor**, **SQL Editor**, **Authentication**, **Storage**, dan **Settings**. Apabila menu-menu tersebut sudah dapat diakses, berarti project Anda siap digunakan.

---

## 11. Menjalankan Migration di SQL Editor

Project Supabase Anda saat ini masih **kosong** — belum ada tabel apapun. Pada langkah ini, Anda akan menjalankan dua file migration yang sudah disediakan di project starter.

### 11.1 Migration Pertama — Skema Dasar

1. Pada dashboard Supabase, klik **SQL Editor** (ikon `</>`) di sidebar kiri.
2. Klik **New query** (di kanan atas).
3. Di editor lokal Anda (VS Code), buka file `fina-app/supabase/migrations/0001_init.sql`.
4. **Salin seluruh isinya**, lalu tempelkan ke SQL Editor Supabase.
5. Klik tombol **Run** (atau tekan `Cmd+Enter` / `Ctrl+Enter`).

✅ **Indikator sukses**: muncul pesan **"Success. No rows returned"** tanpa pesan error berwarna merah.

**Verifikasi cepat**:

- Buka **Table Editor** di sidebar. Tabel `transactions` seharusnya sudah ada dengan kolom: `id`, `type`, `category`, `amount`, `description`, `date`, `user_id`, `embedding`, `created_at`.
- Buka **Database → Extensions**. Carilah `vector` dan `pgcrypto` — status keduanya seharusnya **Enabled**.

### 11.2 Migration Kedua — Function Semantic Search

1. Pada SQL Editor, klik **New query** sekali lagi. (Jangan jalankan di tab yang sama dengan migration pertama agar mudah di-debug apabila ada error.)
2. Buka file `fina-app/supabase/migrations/0002_match_transactions.sql`.
3. Salin seluruh isinya, tempelkan ke SQL Editor, klik **Run**.

✅ **Indikator sukses**: pesan "Success. No rows returned".

**Verifikasi cepat**:

- Buka **Database → Functions**. Function `match_transactions` seharusnya sudah terdaftar.
- Buka **Database → Indexes**. Index `transactions_embedding_idx` seharusnya sudah tercipta.

> ⚠️ **Jangan menjalankan kedua migration dalam satu query yang sama**. Jika salah satu statement gagal, sisanya tidak akan ikut tereksekusi. Menjalankan terpisah memudahkan proses *debugging* apabila terjadi error.

---

## 12. Menambahkan Contoh Data Transaksi

Tabel `transactions` Anda sekarang sudah ada, namun masih **kosong**. Pada langkah ini, Anda akan menambahkan beberapa baris data dummy agar dashboard memiliki sesuatu untuk ditampilkan.

### 12.1 Insert Data Sample

Pada **SQL Editor**, buka query baru dan tempelkan SQL berikut:

```sql
insert into public.transactions (type, category, amount, description, date) values
  ('income',  'Salary',    5000000, 'Gaji bulanan',       '2026-06-01'),
  ('income',  'Freelance', 1500000, 'Project landing',    '2026-06-08'),
  ('expense', 'Food',       130000, 'Makan siang + kopi', '2026-06-11'),
  ('expense', 'Transport',   95000, 'Bensin',             '2026-06-10'),
  ('expense', 'Bills',      320000, 'Internet bulanan',   '2026-06-09'),
  ('expense', 'Shopping',   240000, 'Sepatu lari',        '2026-06-06');
```

Klik **Run**. Apabila berhasil, akan muncul pesan seperti **"Success. 6 rows inserted"**.

### 12.2 Penjelasan Singkat

- Kolom `id`, `created_at`, dan `embedding` sengaja **tidak diisi** — Postgres akan mengisinya secara otomatis (`id` = UUID acak, `created_at` = waktu saat ini, `embedding` = NULL).
- Kolom `user_id` juga dikosongkan; ini valid karena kolom tersebut nullable.
- Nilai `type` **wajib** salah satu dari `'income'` atau `'expense'` (ada *check constraint* di skema).
- Nilai `amount` ditulis dalam angka penuh **tanpa titik / koma** (`5000000`, bukan `5.000.000`).
- Nilai `date` mengikuti format `'YYYY-MM-DD'`.

### 12.3 Verifikasi di Table Editor

Buka **Table Editor → transactions**. Anda seharusnya melihat 6 baris yang baru saja dimasukkan.

> 💡 Anda dipersilakan menambah, mengubah, atau menghapus baris sesuai selera. Ini *database Anda sendiri* — silakan bereksperimen.

---

## 13. Mengisi `.env.local` dengan Credential Anda

Setelah project Supabase aktif dan migration berjalan, kini saatnya menyambungkan aplikasi Next.js Anda dengan Supabase melalui environment variables. File `.env.local` sudah Anda buat pada Step 7 (saat smoke test) — pada langkah ini Anda tinggal mengisinya dengan nilai yang sebenarnya.

### 13.1 Ambil URL dan Publishable Key

1. Di dashboard Supabase, klik ikon **Settings** (gerigi) di sidebar.
2. Pilih **API** pada submenu.
3. Anda akan menemui dua bagian:
   - **Project URL** — contoh `https://abcdefghijk.supabase.co`. Salin.
   - **Project API keys** atau **Publishable keys** — di sana ada key yang dimulai dengan `sb_publishable_...`. Salin.

> ⚠️ **Penting**: Anda akan melihat dua jenis key — **publishable** (`sb_publishable_...`) dan **secret** (`sb_secret_...`). Untuk Fina App, Anda **hanya memerlukan publishable key** karena seluruh akses dilakukan melalui RLS policy yang permissive. **Jangan menyalin secret key ke `.env.local`** — secret key bypass RLS dan tidak seharusnya tersedia di sisi client.

### 13.2 Tempelkan ke `.env.local`

Buka file `fina-app/.env.local` di VS Code. Ganti isinya menjadi seperti berikut, dengan nilai milik Anda:

```env
NEXT_PUBLIC_SUPABASE_URL=https://abcdefghijk.supabase.co
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=sb_publishable_xxxxxxxxxxxxxxxxxxxxxx
```

Simpan file.

### 13.3 Restart Dev Server

Next.js hanya membaca environment variables saat startup. Jadi setiap kali Anda mengubah `.env.local`, Anda perlu me-restart dev server:

```bash
# Pada terminal yang menjalankan `npm run dev`:
# Tekan Ctrl+C untuk menghentikan
# Lalu jalankan ulang:
npm run dev
```

---

## 14. Verifikasi Koneksi pada Dashboard

Buka kembali **http://localhost:3000** di browser, lalu reload halaman (Cmd+R / Ctrl+R).

Apabila semuanya berjalan benar, Anda akan melihat:

- **Card "Savings"** menampilkan saldo (income − expense). Dengan data sample di atas, nilainya adalah **Rp 5.715.000** (5.000.000 + 1.500.000 − 130.000 − 95.000 − 320.000 − 240.000).
- **Card "Incomes"** menampilkan total income: **Rp 6.500.000**.
- **Card "Expenses"** menampilkan total expense: **Rp 785.000**.

Apabila angka tampil dengan benar, **selamat** — aplikasi Anda telah terhubung dengan database Supabase yang Anda buat sendiri.

### Apabila Angka Masih Rp 0 atau Muncul Error

Silakan periksa hal-hal berikut secara berurutan:

1. **Apakah dev server sudah di-restart** setelah perubahan `.env.local`? (Ini penyebab paling umum.)
2. **Apakah URL dan key sudah benar?** Periksa tidak ada spasi di awal/akhir, tidak ada baris terbelah, dan tidak salah tertukar key publishable vs secret.
3. **Apakah migration sudah dijalankan?** Coba buka Table Editor di Supabase — tabel `transactions` harus ada dengan 6 baris data.
4. **Apakah RLS policy aktif?** Buka **Authentication → Policies** atau **Table Editor → transactions → Policies**. Policy "Permissive rules for all" seharusnya terdaftar. Tanpa policy ini, publishable key tidak dapat membaca data.

Apabila masih bermasalah, buka *console browser* (F12 → tab Console) dan baca pesan error-nya. Anda juga dapat **bertanya ke Claude Code**:

```
> halaman dashboard saya menampilkan Rp 0 semua padahal data sudah masuk
  di Supabase. tolong bantu saya cek apa penyebabnya.
```

Claude akan membaca `.env.local`, `src/lib/supabase/client.ts`, dan `src/features/action.ts` untuk membantu mendiagnosis masalah.

---

## 15. Validasi Akhir Modul

Sebelum melanjutkan ke Module 02, pastikan seluruh checklist berikut sudah tercapai:

**Toolchain & Project**
- [ ] `claude --version` mengeluarkan nomor versi (bukan `command not found`).
- [ ] `claude` REPL berhasil login dan merespons prompt sederhana.
- [ ] Folder `fina-app/` tersedia sebagai hasil clone.
- [ ] `npm install` selesai tanpa error fatal.
- [ ] `npm run dev` berjalan dan **http://localhost:3000** dapat diakses.

**Supabase**
- [ ] Project Supabase pribadi sudah dibuat dan aktif.
- [ ] Migration `0001_init.sql` berhasil dijalankan; tabel `transactions` terlihat di Table Editor.
- [ ] Migration `0002_match_transactions.sql` berhasil dijalankan; function `match_transactions` terdaftar di Database → Functions.
- [ ] Minimal 6 baris data contoh sudah dimasukkan ke tabel `transactions`.
- [ ] File `.env.local` sudah berisi `NEXT_PUBLIC_SUPABASE_URL` dan `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY` milik project Anda sendiri.

**Verifikasi Visual**
- [ ] Setelah dev server di-restart, dashboard pada browser menampilkan **angka aktual** (bukan Rp 0) pada ketiga stat card.

---

## Troubleshooting Cepat

### `claude: command not found` setelah `npm install -g`

Path global npm belum terdaftar di `$PATH`. Silakan periksa:

```bash
npm config get prefix
# Contoh hasil: /Users/anda/.npm-global
echo $PATH | grep ".npm-global"
```

Apabila hasil grep kosong, tambahkan baris berikut ke shell config (`~/.zshrc` untuk zsh, `~/.bashrc` untuk bash):

```bash
echo 'export PATH="$(npm config get prefix)/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Port 3000 Sudah Digunakan

Tutuplah process lain yang menggunakan port 3000, atau jalankan dev server pada port lain:

```bash
PORT=3001 npm run dev
```

### Error `cannot find module '@/...'`

Build cache mengalami kerusakan. Bersihkan, lalu lakukan rebuild:

```bash
rm -rf .next node_modules
npm install
npm run dev
```

### `EACCES` Saat `npm install -g`

Pada macOS atau Linux, npm prefix perlu dikonfigurasi agar tidak memerlukan sudo. **Hindari penggunaan `sudo npm install -g`** karena hal tersebut sering menimbulkan masalah permission di kemudian hari. Berikut solusi yang direkomendasikan:

```bash
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH="~/.npm-global/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
# Coba install ulang
npm install -g @anthropic-ai/claude-code
```

### Error pada SQL Editor — `permission denied for schema auth`

Apabila pesan ini muncul saat menjalankan migration `0001_init.sql`, kemungkinan project Supabase Anda belum sepenuhnya selesai melakukan provisioning. Tunggu 1–2 menit, lalu coba jalankan kembali.

### Migration `0001_init.sql` Sukses, Tetapi `0002` Gagal dengan `relation "transactions" does not exist`

Pesan ini muncul apabila SQL Editor menjalankan migration kedua sebelum yang pertama benar-benar selesai (misalnya karena di-paste di tab yang sama dan urutannya tertukar). Solusi: refresh halaman SQL Editor, lalu jalankan kembali migration kedua dalam **query baru** yang terpisah.

### Dashboard Menampilkan Rp 0 Padahal Data Sudah Masuk

Penyebab paling umum dan urutan pengecekan:

1. **Dev server belum di-restart** setelah `.env.local` diubah. Tekan `Ctrl+C` di terminal, lalu jalankan `npm run dev` kembali.
2. **URL atau key salah ketik**. Periksa tidak ada spasi tersembunyi atau baris yang terpotong.
3. **Tertukar publishable dengan secret key**. Publishable diawali `sb_publishable_...` dan inilah yang digunakan.
4. **RLS policy belum aktif**. Buka **Table Editor → transactions → Policies**. Policy "Permissive rules for all" harus tercantum.

### Error `Failed to fetch` di Console Browser

Biasanya disebabkan oleh URL Supabase yang tidak valid (typo) atau project Supabase sedang di-pause (free tier pause setelah 7 hari idle). Buka dashboard Supabase Anda; apabila project dalam status paused, klik **Restore project**.

---

## Recap & Langkah Selanjutnya

Pada modul ini Anda telah:

1. Memasang Claude Code di terminal dan memverifikasi bahwa ia berjalan dengan baik.
2. Memahami perbedaan Claude Code (CLI), Claude Desktop, dan Claude.ai (web).
3. Meng-clone project starter Fina App dan menginstal seluruh dependencies.
4. Mempelajari konsep Supabase dan pgvector sebagai fondasi project.
5. Menjalankan dev server pertama kali dengan `.env.local` kosong untuk memastikan tampilan dasar terbuka.
6. **Membuat project Supabase pribadi** dari nol.
7. **Menjalankan kedua migration** (`0001_init.sql` dan `0002_match_transactions.sql`) di SQL Editor.
8. **Memasukkan contoh data** transaksi ke tabel `transactions`.
9. **Mengisi `.env.local`** dengan URL dan publishable key milik Anda sendiri.
10. **Memverifikasi koneksi** melalui dashboard — angka pada stat card sudah menampilkan total dari data Anda.

**Module 02** akan membahas **AI-Assisted Coding dengan Claude Code**: anatomi Claude Code (tools, konteks, permission modes), pola prompt yang efektif untuk coding, serta empat workflow umum (eksplorasi, fitur, refactoring, debugging). Anda juga akan berlatih langsung dengan **generate dokumentasi project** dan **membangun fitur CRUD** untuk halaman Transactions di atas Fina App yang sudah disiapkan di modul ini.

📂 Lihat: `Module-02-AI-Assisted-Coding/materi.md`
