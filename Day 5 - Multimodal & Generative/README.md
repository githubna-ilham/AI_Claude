# Day 5 — Multimodal & Generative

> **Catatan**: Lanjutan dari **[Day 4 — AI Agent & Tools](../Day%204%20-%20AI%20Agent%20%26%20Tools/)**. Day 5 membangun kemampuan AI untuk memproses **input gambar/dokumen** (Multimodal) dan menghasilkan **visualisasi data dinamis** dari instruksi natural language (Generative Dashboard).

## Tujuan

Setelah menyelesaikan materi ini, peserta diharapkan mampu:

1. Memahami **konsep multimodal** dan cara Claude memproses input gambar via Vision API.
2. Membangun **pipeline upload gambar** (base64) + ekstraksi data terstruktur dari kwitansi/dokumen.
3. Mengintegrasikan hasil ekstraksi Vision ke **database transactions** secara otomatis.
4. Memahami konsep **Generative UI** — menghasilkan komponen/chart secara dinamis dari instruksi pengguna.
5. Membangun pipeline **Natural Language → Query DB via Tools → Render Chart** menggunakan Claude API + Recharts.

## Outline Modul

| Modul | Judul | Estimasi |
|---|---|---|
| **13** | **Multimodal & Document Understanding** — 3 section: Vision API basics → Upload UI + base64 pipeline → Receipt extraction + auto-insert ke `transactions` | 2,5–3 jam |
| **14** | **Generative Dashboard** — Natural Language → Chart: user ketik instruksi bebas → Claude analisis + query Supabase via tools → app render chart (pie/bar/line/area) dinamis di Dashboard (3 prompt) | 2–3 jam |

Total estimasi: **±4,5–6 jam efektif** untuk Module 13–14 (di luar break & diskusi).

## Prasyarat

- **Module 10–12 dari [Day 4](../Day%204%20-%20AI%20Agent%20%26%20Tools/)** sudah selesai.
- RAG chatbot dan AI Agent quick-add sudah berjalan di Fin-App.
- Claude Code aktif di terminal kedua.

## Struktur Folder

```
Day 5 - Multimodal & Generative/
├── README.md                                  (file ini)
├── Module-13-Multimodal/                      ✅ siap (3 section)
│   ├── materi.md                              (Konsep multimodal + vision API + use case Fin-App)
│   ├── latihan.md                             (index 3 section)
│   ├── latihan-1-vision-basics.md             (Section 1 — script PoC vision via terminal)
│   ├── latihan-2-upload-ui.md                 (Section 2 — komponen UploadKwitansi + base64 pipeline)
│   └── latihan-3-receipt-extraction.md        (Section 3 — Claude vision + tool save_receipt_transactions + insert paralel)
└── Module-14-Generative-Dashboard/            ✅ siap (3 prompt)
    ├── materi.md                              (Konsep Generative UI + arsitektur 2-tool + Recharts)
    └── latihan.md                             (3 prompt: tools + server action → komponen → wire ke Dashboard)
```

## Alur Belajar

```
Day 4 Module 12 (AI Agent selesai)
        ↓  quick-add handle multi-save + delete + mixed dalam 1 kalimat
Day 5 Module 13 — Multimodal & Document Understanding
        ↓  upload foto kwitansi → auto-extract → insert ke transactions
Day 5 Module 14 — Generative Dashboard
        ↓  user ketik instruksi → Claude query DB via tools → render chart dinamis
```

🚀 **Mulai**: [Module 13 — Multimodal](./Module-13-Multimodal/materi.md)
