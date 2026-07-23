# Day 4 — AI Agent & Tools

> **Catatan**: Lanjutan dari **[Day 3 — System Prompt Engineering](../Day%203%20-%20System%20Prompt%20Engineering/)**. Day 4 membangun **pipeline data + retrieval** (Embedding → RAG), lalu menggabungkan semuanya menjadi **AI Agent otonom** dengan tool use.
>
> Setelah Day 3 menyiapkan fondasi (Claude API, prompt engineering, structured output), Day 4 melengkapi stack: data ter-embed di pgvector → RAG di chatbot → agent yang otonom. Multimodal & Generative Dashboard dilanjutkan di **[Day 5](../Day%205%20-%20Multimodal%20%26%20Generative/)**.

## Tujuan

Setelah menyelesaikan materi ini, peserta diharapkan mampu:

1. Memahami **konsep embedding** dan mengimplementasikan Voyage AI `embed()` di project Next.js.
2. Mendesain skema **vector database** dengan pgvector + index HNSW + function semantic search.
3. Menjalankan **backfill embedding** untuk data historis dan auto-embed di pipeline insert baru.
4. Memahami **konsep RAG** (halusinasi, closed/open book, alur Retrieval-Augmented-Generation).
5. Mengintegrasikan **RAG ke chatbot** AI Advisor end-to-end dengan anti-halusinasi guidance.
6. Membedakan **chatbot biasa** vs **AI Agent** dari sisi pola interaksi, inisiatif, dan akses dunia luar.
7. Menerapkan pola **ReAct (Reasoning + Acting)** sebagai cetak biru perancangan agent.
8. (Section lanjutan) Mengimplementasi ReAct loop konkret pakai Claude API tool use, multi-tool orchestration, memory + error recovery.

## Outline Modul

| Modul | Judul | Estimasi |
|---|---|---|
| **10** | **Embedding** — 3 section: Implementasi Voyage AI → Database Vector (pgvector + HNSW + match_transactions) → Save Embedding ke `transactions` (auto-embed + backfill + search helper) | 2,5–3 jam |
| **11** | **RAG** — 3 section: Retrieval Helper → Implementasi RAG di Chatbot (prompt builder + route handler + verifikasi) → Mode Toggle (Personal vs General) | 2,5–3 jam |
| **12** | **AI Agent** — Konsep ReAct + Multi-Tool di quick-add bertahap: definisi tools (save+delete+update) → wire single → upgrade ke parallel (3 prompt) | 2–2,5 jam |

Total estimasi: **±7–8,5 jam efektif** untuk Module 10–12 (di luar break & diskusi).

> ➡️ Module 13 (Multimodal) dan Module 14 (Generative Dashboard) dilanjutkan di **[Day 5 — Multimodal & Generative](../Day%205%20-%20Multimodal%20%26%20Generative/)**.
>
> ⚠️ Section implementasi lanjutan di Module 12 (ReAct loop konkret, multi-tool, memory, error recovery, multi-agent coordination) akan ditambah di iterasi berikutnya.

## Prasyarat

- **Module 08–09 dari [Day 3](../Day%203%20-%20System%20Prompt%20Engineering/)** sudah selesai. Khususnya:
  - Module 08 Section 5 (Streaming) — route `/api/advisor` siap di-modifikasi untuk RAG.
  - Module 09 Section 3 (RCI) — konstanta `ADVISOR_ROLE / CONTEXT / FORMAT` siap di-reuse di builder RAG.
  - Module 09 Section 5 (Structured Output) — `quickAddTransaction` siap di-extend dengan auto-embed.
- Akun **Supabase** dengan pgvector siap (project Fin-App dari Day 2 Module 01).
- API key **Voyage AI** (`VOYAGE_API_KEY` di `.env.local`) — daftar gratis di voyageai.com.
- Claude Code aktif di terminal kedua.

## Struktur Folder

```
Day 4 - AI Agent & Tools/
├── README.md                              (file ini)
├── Module-10-Embedding/                   ✅ siap (3 section)
│   ├── materi.md                          (konsep + Section 1/2/3 implementation overview)
│   ├── latihan.md                         (index 3 section)
│   ├── latihan-1-implementasi-embedding.md  (Section 1 — Voyage embed() + caching)
│   ├── latihan-2-database-vector.md         (Section 2 — pgvector + ALTER + HNSW + match_transactions)
│   └── latihan-3-save-embedding-db.md       (Section 3 — auto-embed quickAdd + backfill + searchTransactions)
├── Module-11-RAG/                         ✅ siap (3 section)
│   ├── materi.md                          (Konsep RAG + Section 1/2/3 overview)
│   ├── latihan.md                         (index 3 section)
│   ├── latihan-1-retrieval.md             (Section 1 — retrieveContextForChatbot helper)
│   ├── latihan-2-rag-chatbot.md           (Section 2 — Implementasi RAG di chatbot end-to-end)
│   └── latihan-3-mode-toggle.md           (Section 3 — Mode toggle Personal vs General)
└── Module-12-AI-Agent/                    ✅ siap (Section 3+ menyusul)
    ├── materi.md                          (Konsep AI Agent + ReAct + Tools & Function Calling)
    └── latihan.md                         (3 prompt progresif — Prompt 1: definisi tools delete+update. Prompt 2: wire ke quick-add (single). Prompt 3: upgrade ke parallel)
```

> ➡️ Module 13 (Multimodal) dan Module 14 (Generative Dashboard) ada di **[Day 5 — Multimodal & Generative](../Day%205%20-%20Multimodal%20%26%20Generative/)**.

## Alur Belajar

```
Day 3 Module 09 (Prompt Engineering selesai)
        ↓  ADVISOR_SYSTEM RCI + structured output + quickAddTransaction
Day 4 Module 10 — Embedding
        ↓  embed() Voyage + tabel transactions ber-embedding + searchTransactions
Day 4 Module 11 — RAG
        ↓  chatbot grounded di transaksi nyata + mode toggle Personal/General
Day 4 Module 12 — AI Agent (Konsep + Parallel + Multi-Tool di quick-add)
        ↓  quick-add bisa handle multi-save + delete + mixed dalam 1 kalimat
Day 5 Module 13 — Multimodal & Document Understanding
        ↓  upload foto kwitansi → auto-extract → insert ke transactions
Day 5 Module 14 — Generative Dashboard
        ↓  user ketik instruksi → Claude query DB via tools → render chart dinamis
Section 3+ Module 12 menyusul
        → implementasi ReAct loop konkret runtime
        → memory + error recovery
        → multi-agent coordination
```

🚀 **Mulai**: [Module 10 — Embedding](./Module-10-Embedding/materi.md) · **Lanjut ke Day 5**: [Day 5 — Multimodal & Generative](../Day%205%20-%20Multimodal%20%26%20Generative/)
