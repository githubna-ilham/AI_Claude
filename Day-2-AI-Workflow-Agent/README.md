# Day 2 — AI Workflow + AI Agent Full

Pelatihan: **Prompt Engineering, AI Agent & AI App Development with Claude**
Penyelenggara: Multimatics
Durasi total program: 4 hari (40 jam)
Hari ini: **Day 2 (8 jam efektif, 480 menit + break)**

## Ringkasan Day 2

Day 2 menjembatani dari **prompt craft** (Day 1) menuju **sistem otomatis** dan **AI Agent berbasis Claude API**. Peserta belajar bagaimana prompt yang baik dirangkai menjadi *workflow*, lalu di-upgrade menjadi *agent* yang bisa mengambil keputusan dan memanggil tool. Diakhiri dengan implementasi end-to-end mini-agent helpdesk IT.

## Target Audiens

Software Developer, AI/ML Engineer, Data Analyst, Product Manager, Innovation Team, IT Architect. Materi disusun dengan dua jalur: konsep (untuk PM/IT Architect) dan implementasi (untuk Developer/ML Engineer).

## Learning Outcomes (Day 2)

Setelah menyelesaikan Day 2, peserta mampu:

1. Menerjemahkan kebutuhan bisnis (customer service, dokumen, laporan, analisis, internal KB) menjadi *prompt pack* siap pakai.
2. Merancang **multi-step AI workflow** dengan teknik *prompt chaining*, *task delegation*, dan *error handling* per step.
3. Membedakan **Chatbot vs Workflow vs Agent**, serta memahami arsitektur agent (planner, executor, memory, tools).
4. Mengimplementasikan **tool calling / function calling** pada Claude API untuk agent yang mampu mengambil aksi terhadap sistem eksternal.
5. Membangun **AI Agent end-to-end** dengan Claude API (autentikasi, conversation loop, tool execution, basic deployment posture).

## Alur Modul

| Module | Topik | Durasi | Lab |
|---|---|---|---|
| 5 | Prompt for Business Use Cases | 90 menit | Lab 04 — Use Case Prompt Pack |
| 6 | AI Workflow Automation | 90 menit | Lab 05 — Multi-Step Pipeline |
| 7 | Introduction to AI Agent | 90 menit | — (konseptual) |
| 8 | AI Agent Orchestration | 90 menit | Lab 06 — Tool Calling |
| 9 | Building AI Agent with Claude API | 120 menit | Lab 07 — Build Agent |

Total konten: **480 menit** (8 jam) + 60 menit break/QA fleksibel.

## Jadwal Sampel

| Waktu | Aktivitas |
|---|---|
| 08.30 – 09.00 | Recap Day 1 + warm-up |
| 09.00 – 10.30 | Module 5 + Lab 04 (paralel) |
| 10.30 – 10.45 | Coffee break |
| 10.45 – 12.15 | Module 6 + Lab 05 |
| 12.15 – 13.15 | Istirahat siang |
| 13.15 – 14.45 | Module 7 (banyak diskusi & whiteboard) |
| 14.45 – 15.00 | Coffee break |
| 15.00 – 16.30 | Module 8 + Lab 06 |
| 16.30 – 18.30 | Module 9 + Lab 07 (capstone) |
| 18.30 – 18.45 | Wrap-up Day 2 + preview Day 3 |

## Diagram Alur Day 2

```mermaid
flowchart LR
    A[Prompt Craft<br/>Day 1] --> B[M5: Prompt utk<br/>Business Use Case]
    B --> C[M6: Workflow<br/>Automation]
    C --> D[M7: Agent<br/>Fundamentals]
    D --> E[M8: Orchestration<br/>& Tool Calling]
    E --> F[M9: Build Agent<br/>w/ Claude API]
    F --> G[Capstone<br/>Day 3-4]
```

## Prasyarat Teknis

- Python 3.10+ terinstall, `pip install anthropic python-dotenv`.
- Anthropic API key (peserta atau shared trainer key). **Selalu** simpan di `.env`, jangan hardcode.
- Editor: VS Code / Cursor.
- Akses internet stabil.

## Catatan Fasilitator

- Mock data (FAQ helpdesk, sample tickets, mock weather/DB response) disiapkan trainer di folder `assets/` per lab.
- Default model: `claude-sonnet-4-5`. Gunakan `claude-haiku-4-5` untuk task ringan & demo cepat agar hemat token.
- Selalu mulai sesi lab dengan reminder: **API key disimpan di env var, tidak commit ke git.**

## Struktur Folder

```
Day-2-AI-Workflow-Agent/
├── README.md
├── Module-05-Prompt-for-Business-Use-Cases/
│   ├── materi.md
│   ├── speaker-notes.md
│   └── lab-04-use-case-prompt-pack/
├── Module-06-AI-Workflow-Automation/
│   ├── materi.md
│   ├── speaker-notes.md
│   └── lab-05-multi-step-pipeline/
├── Module-07-Introduction-AI-Agent/
│   ├── materi.md
│   └── speaker-notes.md
├── Module-08-AI-Agent-Orchestration/
│   ├── materi.md
│   ├── speaker-notes.md
│   └── lab-06-tool-calling/
└── Module-09-Building-AI-Agent-Claude-API/
    ├── materi.md
    ├── speaker-notes.md
    └── lab-07-build-agent/
```
