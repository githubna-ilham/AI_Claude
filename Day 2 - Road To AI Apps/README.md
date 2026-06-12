# Day 2 — Road To AI Apps

> **Catatan**: Folder ini berisi materi pendamping berbasis **studi kasus**. Project yang dibangun: **Fina App** — financial tracker single-user dengan Next.js 16, Supabase, dan TanStack Query.

## Tujuan

Setelah menyelesaikan materi ini, peserta diharapkan mampu:

1. **Scaffolding** project Next.js 16 modern (App Router, Turbopack, Tailwind v4) dengan Shadcn UI.
2. **Setup Supabase**: project, schema, RLS, pgvector — siap dipakai sebagai backend Fin-App.
3. **Mengintegrasikan** Next.js + Supabase dengan pola modern (`@supabase/ssr`, client/server split, proxy.ts).
4. Memakai **TanStack Query** untuk data fetching dari client + Server Actions.
5. Memahami paradigma **AI-Assisted Coding** dengan Claude Code dan dapat mempraktikkannya untuk membangun fitur nyata (dokumentasi & CRUD).
6. Memanggil **Claude API** secara programmatic untuk memulai integrasi AI pada aplikasi.

## Outline Modul

| Modul | Judul | Estimasi |
|---|---|---|
| **01** | Setup Project & Claude Code (+ Supabase + migration + sample data) | 90 menit |
| **02** | AI-Assisted Coding (konsep) + Latihan: Generate Dokumentasi + Build CRUD Transactions | 180 menit |
| **03** | Claude API — Koneksi Pertama (SDK + file eksperimen + console output) | 30 menit (section 1) |
| **04** | Content Generation — 7 section inkremental: UI Chatbot → Integrasi API → Text Generation → Thinking → Switching Mode → Streaming → Multi-Turn | 4–5 jam (total) |
| **05** | Prompt Engineering — 6 section: System Instruction → Parameter & Output Control → Prompt Guides → Zero/Few-Shot → Role-Context-Instruction → Agentic Workflow | 5–6 jam (total) |

Total estimasi sementara: **±14–15 jam efektif** untuk Module 01–05 (di luar break & diskusi).

## Stack Hasil Akhir

- **Next.js 16.2.6** (App Router, Server Actions, Turbopack)
- **Tailwind CSS v4** + **Shadcn UI** (Radix base, preset Nova)
- **Supabase** — Postgres + pgvector + RLS
- **@supabase/supabase-js** + **@supabase/ssr** (modern auth-ready pattern)
- **TanStack Query v5** (client-side cache + devtools)
- **@anthropic-ai/sdk** (Claude API)
- **TypeScript**, **lucide-react** icons

## Prasyarat

- Tools terpasang: Node.js ≥ 20, Git, VS Code.
- Akun Supabase aktif (free tier).
- Akun Anthropic Console (untuk API key Claude — dibutuhkan di Module 03).

## Project Referensi

Source code starter project Fin-App ada di repository terpisah:

```
github.com/githubna-ilham/fina-app-starter
├── branch: main      (akan berkembang seiring waktu)
└── branch: starter   (titik mulai workshop — frozen)
```

## Struktur Folder

```
Day 2 - Road To AI Apps/
├── README.md                                       (file ini)
├── Module-01-Setup-Project/                        ✅ siap
│   ├── materi.md                                   (setup + Supabase + migration + sample data)
│   └── latihan.md                                  (verifikasi + eksplorasi + eksperimen data)
├── Module-02-AI-Assisted-Coding/                   ✅ siap
│   ├── materi.md                                   (konsep AI-assisted coding + anatomi Claude + prompting + etika)
│   └── latihan.md                                  (Latihan 1: Generate Dokumentasi · Latihan 2: Build CRUD)
├── Module-03-Claude-API/                           🔨 in progress
│   ├── materi.md                                   (section 1: koneksi pertama via SDK + console output)
│   └── latihan.md                                  (6 eksperimen: prompt, max_tokens, model, biaya, error)
├── Module-04-Content-Generation/                   ✅ siap (7 section lengkap)
│   ├── materi.md                                   (overview + Section 1–7 detail)
│   └── latihan.md                                  (23 prompt eksekusi siap copy-paste)
└── Module-05-Prompt-Engineering/                   ✅ siap (6 section lengkap)
    ├── materi.md                                   (outline + Section 1–6 detail)
    └── latihan.md                                  (20 prompt eksekusi siap copy-paste)
    ├── materi.md                                   (outline 7 section + prinsip kontinuitas + Section 1 detail)
    └── latihan.md                                  (Section 1: 5 prompt UI Chatbot · Section 2–7: stub)
```

## Struktur Section di Module 04

Module 04 dirancang sebagai **rangkaian inkremental** — satu fitur chatbot dibangun lapis-demi-lapis:

| Section | Fokus | Status |
|---|---|---|
| **1** | UI Chatbot (panel kanan + markdown + toggle) | ✅ Siap |
| **2** | Integrasi Claude API ke chatbot (server action + loading + error + welcome) | ✅ Siap |
| **3** | Text generation (system prompt + format output + refactor ke prompts.ts) | ✅ Siap |
| **4** | Thinking / thought (extended thinking visible + collapsible UI) | ✅ Siap |
| **5** | Switching thinking mode (toggle + budget low/medium/high + branching model) | ✅ Siap |
| **6** | Streaming process (route handler + ReadableStream + typewriter) | ✅ Siap |
| **7** | Multi-turn conversation (riwayat + windowing + reset) | ✅ Siap |

> 💡 **Prinsip kontinuitas**: setiap section memperluas kode dari section sebelumnya — bukan project baru. Pada akhir Module 04, Anda memiliki satu fitur AI Financial Advisor yang utuh dan fungsional.
