# Pelatihan Prompt Engineering, AI Agent & AI App Development with Claude

> Pelatihan 5 hari (50 jam) dari **Multimatics** untuk membangun solusi AI modern berbasis Claude — mulai dari **fondasi LLM & prompt engineering** (Day 1), **setup project Next.js + Supabase** (Day 2), **Claude API & system prompt engineering** (Day 3), **Embedding, RAG, & AI Agent** (Day 4), hingga **Multimodal & Generative Dashboard** (Day 5) di atas project `fin-app`.

---

## Learning Objectives

Setelah mengikuti pelatihan ini, peserta mampu:

1. Memahami konsep dan arsitektur Large Language Model (LLM).
2. Mendesain prompt profesional dan efektif.
3. Mengoptimalkan output AI menggunakan advanced prompting techniques.
4. Menggunakan Claude API untuk pengembangan aplikasi AI.
5. Membangun AI application berbasis Claude.
6. Mengembangkan AI Agent untuk automation workflow.
7. Mengimplementasikan RAG (Retrieval Augmented Generation).
8. Mengintegrasikan AI dengan tools, database, dan API eksternal.
9. Mendesain AI use case untuk kebutuhan bisnis.
10. Mengembangkan solusi AI end-to-end secara scalable & responsible.

## Target Peserta

- Software Developers (Backend / Frontend / Full-Stack)
- AI / ML Engineers (Beginner–Intermediate)
- Data Analysts / Data Engineers
- Product Managers / Product Owners
- IT Solution Architects / Tech Leads
- Digital Transformation & Innovation Team
- Business Technology / Startup / Internal Innovation Lab

## Prasyarat

- Pemahaman dasar AI / ChatGPT / Claude
- Basic programming JavaScript / TypeScript (familiar React/Next.js merupakan nilai tambah, tetapi tidak wajib — kode starter sudah disediakan)
- Pemahaman dasar API & aplikasi web
- Familiar dengan workflow digital bisnis
- Laptop minimal 8 GB RAM, koneksi internet stabil
- Anthropic API key (disediakan fasilitator atau peserta mendaftar di console.anthropic.com)
- Akun Supabase (free tier) untuk Day 2–5
- Akun Voyage AI (free tier) untuk Day 4 (Embedding & RAG)
- Sudah mengisi **[Pretest](pretest/PRETEST-AI-Claude.md)** sebelum hari pertama

---

## Struktur Pelatihan (5 Hari)

| Hari      | Fokus                                                                  | Module per Hari                                                                 |
| --------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| **Day 1 — Introduction LLM**         | Fondasi LLM, dasar prompt engineering, dan teknik prompting           | M01 Introduction LLM Claude · M02 Prompt Engineering Basics · M03 Prompting Techniques |
| **Day 2 — Road To AI Apps**          | Setup project Next.js + Supabase, AI-assisted coding | M04 Setup Project (Next.js + Supabase + pgvector) · M05 AI-Assisted Coding |
| **Day 3 — System Prompt Engineering**| Claude API, UI Chatbot, content generation & advanced prompt engineering pada aplikasi nyata | M06 Claude API · M07 UI Chatbot · M08 Content Generation · M09 Prompt Engineering |
| **Day 4 — AI Agent & Tools**         | Bangun pipeline data + retrieval dan AI Agent otonom di Fin-App | M10 Embedding · M11 RAG · M12 AI Agent |
| **Day 5 — Multimodal & Generative**  | Pemrosesan gambar/dokumen dan Generative Dashboard berbasis natural language | M13 Multimodal · M14 Generative Dashboard |

> Penomoran modul bersifat **sekuensial** dari M01 sampai M14 — berurutan lintas hari tanpa reset.

Metodologi: **30% concept — 60% hands-on — 5% case study — 5% discussion**.

### Jadwal Harian (Acuan)

| Waktu         | Aktivitas                                  |
| ------------- | ------------------------------------------ |
| 08:30 – 09:00 | Registrasi & recap hari sebelumnya         |
| 09:00 – 10:30 | Module pertama                             |
| 10:30 – 10:45 | Coffee break                               |
| 10:45 – 12:30 | Module kedua (+ lab)                       |
| 12:30 – 13:30 | ISHOMA                                     |
| 13:30 – 15:00 | Module ketiga                              |
| 15:00 – 15:15 | Coffee break                               |
| 15:15 – 16:45 | Module keempat / lab lanjutan              |
| 16:45 – 17:00 | Wrap-up & Q&A                              |

---

## Peta Direktori

```
AI_Claude/
├── README.md                                  # file ini
├── pretest/                                   # profiling peserta
├── posttest/                                  # evaluasi akhir
├── Day 1 - Introduction LLM/                  # M01 Intro LLM · M02 Prompt Eng Basics · M03 Prompting Techniques
├── Day 2 - Road To AI Apps/                   # M04 Setup Project · M05 AI-Assisted Coding
├── Day 3 - System Prompt Engineering/         # M06 Claude API · M07 UI Chatbot · M08 Content Generation · M09 Prompt Engineering
├── Day 4 - AI Agent & Tools/                  # M10 Embedding · M11 RAG · M12 AI Agent
├── Day 5 - Multimodal & Generative/           # M13 Multimodal · M14 Generative Dashboard
└── resources/                                 # templates, starter code, cheatsheet
    ├── claude-api-cheatsheet.md
    ├── prompt-templates/
    ├── agent-templates/
    └── starter-code/
```

---

## Tools & Technologies

1. **Claude** (claude.ai untuk eksplorasi, console.anthropic.com untuk API & Workbench)
2. **Claude API** — JavaScript/TypeScript SDK (`@anthropic-ai/sdk`) sebagai default tunggal
3. **Node.js 20 LTS+** (idealnya 22 LTS) — runtime utama untuk seluruh hands-on
4. **Next.js 16 (App Router) + TypeScript + Tailwind CSS + Shadcn UI** — stack project hands-on `fin-app`
5. **Supabase (Postgres)** — database utama + extension **`pgvector`** untuk Embedding & RAG di Day 4
6. **Voyage AI** — embedding provider default (`voyage-3`, 1024 dim — cloud, free tier cukup)
7. **REST API integration tools** — Postman / Insomnia (opsional)
8. **Vercel** (opsional) — untuk deploy hasil akhir Day 4

---

## Persiapan untuk Peserta (H-1)

- [ ] Install Node.js 20 LTS+ (idealnya 22 LTS)
- [ ] Install editor (Cursor / VS Code direkomendasikan) + extensions ESLint, Tailwind IntelliSense, Prettier
- [ ] Buat akun Anthropic Console: https://console.anthropic.com
- [ ] Dapatkan API key dari fasilitator (atau generate sendiri, top-up minimal $5)
- [ ] Buat akun Supabase: https://supabase.com (free tier; buat project baru region Singapore)
- [ ] Buat akun Voyage AI: https://www.voyageai.com (untuk embedding di Day 4)
- [ ] Clone repo materi: `git clone https://github.com/githubna-ilham/AI_Claude.git`
- [ ] Clone repo `fin-app` starter (link dari fasilitator) → `npm install`
- [ ] Jalankan smoke test JS untuk verifikasi API key (instruksi di `PENDAHULUAN.md`)
- [ ] Isi pretest (deadline H-3)

## Persiapan untuk Fasilitator

- [ ] Analisis hasil pretest → tentukan kedalaman teknis & use case dominan
- [ ] Siapkan akun Anthropic Console dengan budget cukup untuk demo & hands-on
- [ ] Siapkan repo `fin-app` starter (iterasi 1 CRUD selesai) untuk dibagikan H-3
- [ ] Siapkan dummy data: dokumen SOP, CSV transaksi, sample tiket, kontrak PDF
- [ ] Siapkan Supabase project demo dengan `pgvector` extension sudah aktif
- [ ] Cetak handout cheatsheet & checklist responsible AI
- [ ] Setup proyektor, internet ruang kelas, dan UPS minimal untuk demo

---

## Deliverables Peserta

1. Training materials (folder lengkap ini)
2. Prompt Engineering templates (di `resources/prompt-templates/`)
3. AI Agent templates (di `resources/agent-templates/`)
4. AI App starter code — `fin-app` (di `resources/starter-code/`)
5. Claude API Integration Guide (di `resources/claude-api-cheatsheet.md`)
6. Use case examples & business scenarios
7. Hands-on lab files (per module)
8. Working `fin-app` dengan fitur AI: chatbot, embedding, RAG, agent, multimodal
9. Certificate of Completion (dari Multimatics)

---

## Konvensi Materi

Setiap module mengikuti format seragam:

- `materi.md` — bahan utama (Learning Outcomes → Konsep Inti + diagram mermaid → Demo Live → Contoh Konkret → Hands-on Lab → Q&A → Bacaan Lanjutan)
- `latihan.md` (opsional) — latihan terstruktur untuk modul yang dominan konseptual
- `lab-*/README.md` — folder hands-on dengan brief, langkah, dan rubrik

## Kontak

- **Penyelenggara:** Multimatics — www.multimatics.co.id
- **Email fasilitator:** _(diisi tim Multimatics)_
