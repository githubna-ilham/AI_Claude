# Day 3 — System Prompt Engineering

> **Catatan**: Lanjutan dari **[Day 2 — Road To AI Apps](../Day%202%20-%20Road%20To%20AI%20Apps/)**. Day 3 dimulai dengan koneksi Claude API dan membangun UI Chatbot, lalu dilanjutkan dengan content generation dan prompt engineering tingkat lanjut di atas Fin-App.

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
| **06** | Claude API — Koneksi Pertama (SDK + file eksperimen + console output) | 30–90 menit |
| **07** | UI Chatbot — Latihan membangun panel chatbot statis di Fin-App (prasyarat Module 08) | 30–60 menit |
| **08** | Content Generation — 6 section: Integrasi API → Text Generation → Thinking → Switching Mode → Streaming → Multi-Turn | 4–5 jam |
| **09** | Prompt Engineering — 4 section: System Instruction → Parameter & Output Control → Role-Context-Instruction → Agentic Workflow | 3–4 jam |

Total estimasi: **±8–11 jam efektif** untuk Module 06–09 (di luar break & diskusi).

## Prasyarat

- **Module 04–05 dari [Day 2](../Day%202%20-%20Road%20To%20AI%20Apps/)** sudah selesai.
- `@anthropic-ai/sdk` terinstal dan `ANTHROPIC_API_KEY` ada di `.env.local`.
- Claude Code aktif di terminal kedua.

## Struktur Folder

```
Day 3 - System Prompt Engineering/
├── README.md                                       (file ini)
├── Module-06-Claude-API/                 ✅ siap
│   ├── materi.md                         (koneksi pertama via SDK + console output)
│   └── latihan.md                        (Latihan 1 — 6 eksperimen: prompt, max_tokens, model, biaya, error)
├── Module-07-UI-Chatbot/                 ✅ siap
│   ├── materi.md                         (membangun panel chatbot statis di Fin-App)
│   └── latihan.md                        (latihan UI chatbot — prasyarat Module 08)
├── Module-08-Content-Generation/         ✅ siap (6 section)
│   ├── materi.md                         (overview + Section 1–6 detail + diagram Mermaid)
│   ├── latihan.md                        (index 6 section)
│   ├── latihan-1-integrasi-api.md          (Section 1 — Integrasi Claude API ke Chatbot)
│   ├── latihan-2-text-generation.md        (Section 2 — Text Generation)
│   ├── latihan-3-thinking.md               (Section 3 — Thinking / Thought)
│   ├── latihan-4-switching-thinking.md     (Section 4 — Switching Thinking Mode)
│   ├── latihan-5-streaming.md              (Section 5 — Streaming Process)
│   └── latihan-6-multi-turn.md             (Section 6 — Multi-Turn Conversation)
└── Module-09-Prompt-Engineering/         ✅ siap (4 section + 1 bonus)
    ├── materi.md                         (outline + Section 1–4 detail + diagram Mermaid)
    ├── latihan.md                        (index 5 section)
    ├── latihan-1-system-instruction.md     (Section 1 — System Instruction)
    ├── latihan-2-output-control.md         (Section 2 — Output Control)
    ├── latihan-3-rci.md                    (Section 3 — Role, Context, Instruction)
    ├── latihan-4-agentic.md                (Section 4 — Agentic Workflow)
    └── latihan-5-structured-output.md      (Section 5 — Structured Output via Tool Use)
```

## Alur Belajar

```
Day 2 Module 05 (AI-Assisted Coding selesai)
        ↓
Day 3 Module 06 — Claude API (koneksi pertama via SDK)
        ↓  API key terkonfigurasi + eksperimen dasar
Day 3 Module 07 — UI Chatbot
        ↓  panel chatbot statis siap di Fin-App
Day 3 Module 08 Section 1 — Integrasi Claude API
        ↓  +server action askAdvisor
Day 3 Module 08 Section 2 — Text Generation
        ↓  +temperature, prompt prefixing
Day 3 Module 08 Section 3 — Thinking
        ↓  +extended thinking + collapsible UI
Day 3 Module 08 Section 4 — Switching Thinking
        ↓  +toggle + budget Haiku/Opus
Day 3 Module 08 Section 5 — Streaming
        ↓  +route handler /api/advisor
Day 3 Module 08 Section 6 — Multi-Turn
        ↓  +messages[] + windowing
Day 3 Module 09 — Prompt Engineering
        → system instruction, RCI, tool use (agentic) + structured output
        ↓
Day 4 (Embedding → RAG → AI Agent)
```

🚀 **Mulai**: [Module 06 — Claude API](./Module-06-Claude-API/materi.md) · **Lanjut ke Day 4**: [Day 4 — AI Agent & Tools](../Day%204%20-%20AI%20Agent%20%26%20Tools/)
