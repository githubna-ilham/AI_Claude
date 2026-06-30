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
| **03** | Claude API — Koneksi Pertama (SDK + file eksperimen + console output) + Latihan UI Chatbot (prasyarat Day 3) | 30–90 menit |

Total estimasi: **±5–6 jam efektif** untuk Module 01–03 (di luar break & diskusi).

> ➡️ **Lanjutan**: Module 04 (Content Generation) dan Module 05 (Prompt Engineering) ada di **[Day 3 — System Prompt Engineering](../Day%203%20-%20System%20Prompt%20Engineering/)**.

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
└── Module-03-Claude-API/                           ✅ siap
    ├── materi.md                                   (koneksi pertama via SDK + console output)
    ├── latihan.md                                  (Latihan 1 — 6 eksperimen: prompt, max_tokens, model, biaya, error)
    ├── materi-ui-chatbot.md                        (materi pendamping Latihan 2)
    └── latihan-2-ui-chatbot.md                     (Latihan 2 — 5 prompt UI Chatbot, prasyarat Day 3 Module 04)
```
