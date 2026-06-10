# DAY 1 — Prompt Engineering Fundamentals + Advanced

**Program**: Prompt Engineering, AI Agent & AI App Development with Claude
**Penyelenggara**: Multimatics
**Durasi total program**: 4 hari (40 jam)
**Durasi Day 1**: 8 jam efektif (4 modul × 90 menit + lab + break)
**Target audiens**: Software Developer, AI/ML Engineer, Data Analyst, Product Manager, Innovation Team, IT Architect

---

## Ringkasan Day 1

Day 1 membangun fondasi mental model peserta tentang Large Language Model (LLM), cara Claude bekerja, dan bagaimana berkomunikasi efektif dengannya melalui prompt. Hari ini sengaja **tidak menyentuh kode API** — fokus pada *prompt craft* menggunakan Claude web (claude.ai) dan Anthropic Console (console.anthropic.com). Tujuannya: setiap peserta, terlepas dari latar belakang teknis, mampu menulis prompt yang reliable, terukur, dan siap diintegrasikan ke sistem.

Filosofi Day 1: **"Prompt adalah spesifikasi, bukan obrolan."** Peserta diajak berpikir seperti seorang technical writer + product analyst yang menulis instruksi untuk junior cerdas tapi tanpa konteks.

---

## Learning Outcomes Day 1

Setelah menyelesaikan Day 1, peserta diharapkan mampu:

1. **Menjelaskan** cara kerja LLM (tokenization, transformer, context window) dan keterbatasannya (hallucination, knowledge cutoff, bias) dalam bahasa yang dapat dimengerti stakeholder non-teknis.
2. **Mengidentifikasi** kapabilitas dan batas Claude (Opus, Sonnet, Haiku) serta memilih model yang tepat untuk use case tertentu.
3. **Menyusun prompt** menggunakan anatomi standar: Role + Context + Task + Constraint + Output Format.
4. **Menerapkan** teknik prompting lanjutan: zero-shot, few-shot, chain-of-thought, persona, dan structured prompting.
5. **Memproduksi** structured output (JSON) yang valid dan menyusun framework evaluasi prompt (kriteria, rubrik, error handling).

---

## Alur Module

```mermaid
flowchart LR
    M1[Module 1<br/>Introduction LLM & Claude<br/>90 min] --> M2[Module 2<br/>Prompt Engineering Basics<br/>90 min]
    M2 --> L1[Lab 01<br/>Anatomy of Prompt<br/>45 min]
    L1 --> M3[Module 3<br/>Prompting Techniques<br/>90 min]
    M3 --> L2[Lab 02<br/>Zero/Few/CoT<br/>45 min]
    L2 --> M4[Module 4<br/>Structured Output & Optimization<br/>90 min]
    M4 --> L3[Lab 03<br/>JSON Output & Evaluation<br/>60 min]
    L3 --> WRAP[Wrap-up & Refleksi Day 1]
```

---

## Jadwal Harian (indikatif, dapat disesuaikan fasilitator)

| Waktu         | Aktivitas                                               | Durasi |
|---------------|---------------------------------------------------------|--------|
| 08.30 – 09.00 | Registrasi, perkenalan, ice breaker                     | 30 m   |
| 09.00 – 10.30 | **Module 1**: Introduction to LLM & Claude              | 90 m   |
| 10.30 – 10.45 | Coffee break                                            | 15 m   |
| 10.45 – 12.15 | **Module 2**: Prompt Engineering Basics                 | 90 m   |
| 12.15 – 13.15 | Lunch break                                             | 60 m   |
| 13.15 – 14.00 | **Lab 01**: Anatomy of a Prompt                         | 45 m   |
| 14.00 – 15.30 | **Module 3**: Prompting Techniques                      | 90 m   |
| 15.30 – 15.45 | Coffee break                                            | 15 m   |
| 15.45 – 16.30 | **Lab 02**: Zero-shot, Few-shot, Chain-of-Thought       | 45 m   |
| 16.30 – 18.00 | **Module 4** + **Lab 03**: Structured Output + JSON Eval| 90 m   |
| 18.00 – 18.30 | Wrap-up, refleksi, pre-read Day 2                       | 30 m   |

---

## Struktur Folder

```
Day-1-Prompt-Engineering/
├── README.md                                       <- file ini
├── Module-01-Introduction-LLM-Claude/
│   ├── materi.md
│   └── latihan.md
├── Module-02-Prompt-Engineering-Basics/
│   ├── materi.md
│   └── lab-01-anatomy-prompt/README.md
├── Module-03-Prompting-Techniques/
│   ├── materi.md
│   └── lab-02-zero-few-cot/README.md
└── Module-04-Structured-Output-Optimization/
    ├── materi.md
    └── lab-03-json-output-evaluation/README.md
```

---

## Prasyarat Peserta

- Laptop dengan browser modern (Chrome/Edge/Firefox).
- Akun **claude.ai** (free atau Pro) — disarankan Pro untuk akses Sonnet 4.x.
- Akun **console.anthropic.com** (untuk mencoba Workbench, tidak wajib untuk Day 1).
- Pemahaman dasar penggunaan komputer dan editor teks. Tidak perlu pengalaman coding.

## Prasyarat Fasilitator

- Akun Anthropic Console dengan kredit API (untuk demo Workbench).
- Proyektor + koneksi internet stabil.
- Salinan slide, dataset contoh (sentimen, invoice teks, tiket support).
- Stopwatch / timer untuk lab.

---

## Bahan Bacaan Pra-Day 1

- Anthropic — *Introduction to Claude*: https://docs.anthropic.com/en/docs/intro-to-claude
- Anthropic — *Prompt engineering overview*: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
- Anthropic — *Prompt library*: https://docs.anthropic.com/en/prompt-library/library

---

## Catatan

Day 1 sengaja membatasi cakupan ke *prompt craft*. Topik **API integration, tool use, dan agent loop** akan dibahas pada Day 2–4. Peserta diminta menahan godaan untuk "loncat ke kode" — disiplin prompt yang dibangun hari ini akan menjadi tulang punggung kualitas agent yang dibangun di hari berikutnya.
