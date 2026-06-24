# Day 3 — System Prompt Engineering

> **Catatan**: Lanjutan dari **[Day 2 — Road To AI Apps](../Day%202%20-%20Road%20To%20AI%20Apps/)**. Pada Day 3 Anda **membangun fitur AI** di atas Fin-App yang sudah disiapkan di Day 2 — mulai dari integrasi Claude API, sampai prompt engineering tingkat lanjut dengan tool use (agentic workflow).

## Tujuan

Setelah menyelesaikan materi ini, peserta diharapkan mampu:

1. **Integrasi Claude API** ke aplikasi Next.js modern: server action, route handler streaming, error handling.
2. Mengontrol **parameter generation** (`temperature`, `max_tokens`, `stop_sequences`) untuk hasil sesuai kebutuhan.
3. Memanfaatkan **Extended Thinking** model Opus dan menampilkannya di UI sebagai *collapsible reasoning*.
4. Membangun pengalaman **streaming** kata-demi-kata untuk chat AI yang responsif.
5. Mengelola **multi-turn conversation** dengan riwayat percakapan + windowing.
6. Menerapkan **prompt engineering best practices**: system instruction, role-context-instruction pattern, output control.
7. Merancang **agentic workflow**: Claude memanggil tool (mis. `get_transactions`) untuk mengambil data dari Supabase secara mandiri.

## Outline Modul

| Modul | Judul | Estimasi |
|---|---|---|
| **04** | Content Generation — 6 section: Integrasi API → Text Generation → Thinking → Switching Mode → Streaming → Multi-Turn | 4–5 jam |
| **05** | Prompt Engineering — 4 section: System Instruction → Parameter & Output Control → Role-Context-Instruction → Agentic Workflow | 3–4 jam |
| **06** | Embedding — 4 section: Konsep → Implementasi Voyage AI → Database Vector (pgvector) → Save Embedding To DB | 4–5 jam |
| **07** | RAG (konseptual) — 1 section: halusinasi → closed/open book → alur kerja RAG → kapan dipakai | 30–45 menit (baca) |

Total estimasi: **±12–15 jam efektif** untuk Module 04–07 (di luar break & diskusi).

## Prasyarat

- **Module 01–03 dari [Day 2](../Day%202%20-%20Road%20To%20AI%20Apps/)** sudah selesai.
- **Latihan UI Chatbot** di [Module 03 Day 2](../Day%202%20-%20Road%20To%20AI%20Apps/Module-03-Claude-API/latihan-ui-chatbot.md) sudah dieksekusi — panel chatbot statis sudah tampil di Fin-App.
- `@anthropic-ai/sdk` terinstal dan `ANTHROPIC_API_KEY` ada di `.env.local`.
- Claude Code aktif di terminal kedua.

## Struktur Folder

```
Day 3 - System Prompt Engineering/
├── README.md                                       (file ini)
├── Module-04-Content-Generation/         ✅ siap (6 section)
│   ├── materi.md                         (overview + Section 1–6 detail + diagram Mermaid)
│   ├── latihan.md                        (index 6 section)
│   ├── latihan-1-integrasi-api.md          (Section 1 — Integrasi Claude API ke Chatbot)
│   ├── latihan-2-text-generation.md        (Section 2 — Text Generation)
│   ├── latihan-3-thinking.md               (Section 3 — Thinking / Thought)
│   ├── latihan-4-switching-thinking.md     (Section 4 — Switching Thinking Mode)
│   ├── latihan-5-streaming.md              (Section 5 — Streaming Process)
│   └── latihan-6-multi-turn.md             (Section 6 — Multi-Turn Conversation)
├── Module-05-Prompt-Engineering/         ✅ siap (4 section)
│   ├── materi.md                         (outline + Section 1–4 detail + diagram Mermaid)
│   ├── latihan.md                        (index 4 section)
│   ├── latihan-1-system-instruction.md     (Section 1 — System Instruction)
│   ├── latihan-2-output-control.md         (Section 2 — Output Control)
│   ├── latihan-3-rci.md                    (Section 3 — Role, Context, Instruction)
│   └── latihan-4-agentic.md                (Section 4 — Agentic Workflow)
├── Module-06-Embedding/                  ✅ siap (4 section)
│   ├── materi.md                         (konsep + implementasi + DB vector + save embedding)
│   ├── latihan.md                        (index 4 section)
│   ├── latihan-konsep-embedding.md       (Section 1 — Konsep Embedding)
│   ├── latihan-implementasi-embedding.md (Section 2 — Implementasi Voyage AI)
│   ├── latihan-database-vector.md        (Section 3 — Database Vector pgvector)
│   └── latihan-save-embedding-db.md      (Section 4 — Save Embedding To DB Vector)
└── Module-07-RAG/                        ✅ siap (konseptual saja)
    ├── materi.md                         (Konsep RAG: halusinasi, open/closed book, alur kerja, variasi)
    └── latihan.md                        (refleksi konseptual, tidak ada coding)
```

## Alur Belajar

```
Day 2 Module 03 (latihan UI Chatbot)
        ↓  panel chatbot statis siap
Day 3 Module 04 Section 1 — Integrasi Claude API
        ↓  +server action askAdvisor
Day 3 Module 04 Section 2 — Text Generation
        ↓  +temperature, prompt prefixing
Day 3 Module 04 Section 3 — Thinking
        ↓  +extended thinking + collapsible UI
Day 3 Module 04 Section 4 — Switching Thinking
        ↓  +toggle + budget Haiku/Opus
Day 3 Module 04 Section 5 — Streaming
        ↓  +route handler /api/advisor
Day 3 Module 04 Section 6 — Multi-Turn
        ↓  +messages[] + windowing
Day 3 Module 05 — Prompt Engineering
        → system instruction, RCI, tool use (agentic)
```

🚀 **Mulai**: [Module 04 — Content Generation](./Module-04-Content-Generation/materi.md)
