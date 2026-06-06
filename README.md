# Pelatihan Prompt Engineering, AI Agent & AI App Development with Claude

> Pelatihan 4 hari (40 jam) dari **Multimatics** untuk membangun solusi AI modern berbasis Claude — mulai dari desain prompt, AI automation, AI Agent, hingga AI App + RAG untuk kebutuhan enterprise.

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
- Basic programming (Python atau JavaScript)
- Pemahaman dasar API & aplikasi web
- Familiar dengan workflow digital bisnis
- Laptop minimal 8 GB RAM, koneksi internet stabil
- Anthropic API key (disediakan fasilitator atau peserta mendaftar di console.anthropic.com)
- Sudah mengisi **[Pretest](pretest/PRETEST-AI-Claude.md)** sebelum hari pertama

---

## Struktur Pelatihan (4 Hari)

| Hari      | Fokus                                                                       | Module       |
| --------- | --------------------------------------------------------------------------- | ------------ |
| **Day 1** | Prompt Engineering Fundamentals + Advanced                                  | 1–4          |
| **Day 2** | AI Workflow + AI Agent (Concept → Orchestration → Claude API)               | 5–9          |
| **Day 3** | AI App Development + RAG (Retrieval Augmented Generation)                   | 10–12        |
| **Day 4** | AI Product Design + Governance + **Capstone Project**                       | 13–14 + Capstone |

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
├── Day-1-Prompt-Engineering/                  # Module 1–4
├── Day-2-AI-Workflow-Agent/                   # Module 5–9
├── Day-3-AI-App-RAG/                          # Module 10–12
├── Day-4-Product-Governance-Capstone/         # Module 13–14 + Capstone
└── resources/                                 # templates, starter code, cheatsheet
    ├── claude-api-cheatsheet.md
    ├── prompt-templates/
    ├── agent-templates/
    └── starter-code/
```

---

## Tools & Technologies

1. **Claude** (claude.ai untuk eksplorasi, console.anthropic.com untuk API)
2. **Claude API** — Python SDK (`anthropic`) sebagai default, JS SDK (`@anthropic-ai/sdk`) sebagai alternatif
3. **Python 3.11+** / **Node.js 20+**
4. **Vector Database** — Chroma (lokal) atau pgvector; opsi cloud Pinecone/Weaviate
5. **LangChain / Agent Framework** (opsional — fokus utama vanilla Claude API agar peserta paham fundamental)
6. **REST API integration tools** — Postman / Insomnia
7. **AI Workflow tools** — overview konseptual (n8n, Make, Zapier untuk konteks low-code)

---

## Persiapan untuk Peserta (H-1)

- [ ] Install Python 3.11+ dan/atau Node.js 20+
- [ ] Install editor (Cursor / VS Code direkomendasikan)
- [ ] Buat akun Anthropic Console: https://console.anthropic.com
- [ ] Dapatkan API key dari fasilitator (atau generate sendiri, top-up minimal $5)
- [ ] Clone repo materi: `git clone https://github.com/githubna-ilham/AI_Claude.git`
- [ ] `pip install anthropic chromadb` (atau ekuivalen Node.js)
- [ ] Isi pretest (deadline H-3)

## Persiapan untuk Fasilitator

- [ ] Analisis hasil pretest → tentukan kedalaman teknis & use case dominan
- [ ] Siapkan akun Anthropic Console dengan budget cukup untuk demo & hands-on
- [ ] Siapkan dummy data: dokumen SOP, CSV transaksi, sample tiket, kontrak PDF
- [ ] Siapkan vector DB lokal (Chroma docker / pgvector) yang terverifikasi jalan
- [ ] Cetak handout cheatsheet & checklist responsible AI
- [ ] Setup proyektor, internet ruang kelas, dan UPS minimal untuk demo

---

## Deliverables Peserta

1. Training materials (folder lengkap ini)
2. Prompt Engineering templates (di `resources/prompt-templates/`)
3. AI Agent templates (di `resources/agent-templates/`)
4. AI App starter code (di `resources/starter-code/`)
5. Claude API Integration Guide (di `resources/claude-api-cheatsheet.md`)
6. Use case examples & business scenarios
7. Hands-on lab files (per module)
8. Capstone project files (working prototype + slide)
9. Certificate of Completion (dari Multimatics)

---

## Konvensi Materi

Setiap module mengikuti format seragam:

- `materi.md` — bahan utama (Learning Outcomes → Konsep Inti + diagram mermaid → Demo Live → Contoh Konkret → Hands-on Lab → Q&A → Bacaan Lanjutan)
- `speaker-notes.md` — cue fasilitator, alokasi waktu, jawaban kunci, common pitfall
- `lab-*/README.md` — folder hands-on dengan brief, langkah, dan rubrik

## Kontak

- **Penyelenggara:** Multimatics — www.multimatics.co.id
- **Email fasilitator:** _(diisi tim Multimatics)_
