# Day 4 — AI Agent & Tools

> **Catatan**: Lanjutan dari **[Day 3 — System Prompt Engineering](../Day%203%20-%20System%20Prompt%20Engineering/)**. Day 4 membahas **paradigma AI Agent** — sistem AI otonom yang bisa menjalankan task multi-step dengan reasoning + integrasi tools.
>
> Setelah Day 3 menyiapkan fondasi (Claude API, prompt engineering, embedding, RAG), Day 4 menggabungkan semuanya jadi **agent yang otonom**.

## Tujuan

Setelah menyelesaikan materi ini, peserta diharapkan mampu:

1. Membedakan **chatbot biasa** dengan **AI Agent** dari sisi pola interaksi, inisiatif, dan akses dunia luar.
2. Menjelaskan **tiga kemampuan inti** AI Agent: otonom, reasoning, integrasi tools.
3. Menerapkan pola **ReAct (Reasoning + Acting)** sebagai cetak biru perancangan agent.
4. (Section lanjutan, menyusul) Mengimplementasi ReAct loop konkret pakai Claude API tool use.
5. (Section lanjutan) Mengelola memory, error recovery, dan multi-tool orchestration di agent.

## Outline Modul

| Modul | Judul | Estimasi |
|---|---|---|
| **08** | **AI Agent** — Konsep + ReAct (1 section pendahuluan; section implementasi menyusul) | 45–60 menit |

> ⚠️ Day 4 masih dalam tahap pengembangan. Section implementasi (ReAct loop, multi-tool, memory, error recovery, multi-agent coordination) akan ditambah di iterasi berikutnya.

## Prasyarat

- **Module 04–07 dari [Day 3](../Day%203%20-%20System%20Prompt%20Engineering/)** sudah selesai (atau setidaknya Module 05 Section 4 — Agentic Workflow / tool use dasar).
- Pemahaman dasar tentang `tool_use` di Claude API.
- Claude Code aktif di terminal kedua.

## Struktur Folder

```
Day 4 - AI Agent & Tools/
├── README.md                                       (file ini)
└── Module-08-AI-Agent/                             🚧 Section 1 siap, lanjutan menyusul
    ├── materi.md                                   (Konsep AI Agent + ReAct + diagram Mermaid)
    ├── latihan.md                                  (index 1 section)
    └── latihan-konsep-ai-agent.md                  (Section 1 — sketsa ReAct manual + dokumentasi)
```

## Alur Belajar

```
Day 3 Module 07 (RAG end-to-end)
        ↓  AI Advisor sudah bisa retrieve + augment + generate
Day 4 Module 08 Section 1 — Konsep AI Agent (pendahuluan)
        ↓  pahami AI Agent + ReAct loop sebelum coding
Section 2+ menyusul
        → implementasi ReAct loop konkret
        → multi-tool orchestration
        → memory + error recovery
        → multi-agent coordination
```

🚀 **Mulai**: [Module 08 — AI Agent](./Module-08-AI-Agent/materi.md)
