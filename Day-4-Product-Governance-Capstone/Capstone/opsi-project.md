# Opsi Project Capstone

Pilih 1 dari 6 opsi berikut. Tiap opsi telah dikalibrasi untuk dapat diselesaikan dalam **150 menit eksekusi** dengan tim 3–4 orang. Semua opsi mewajibkan kombinasi minimal: **Prompt Engineering + Claude API + (Agent atau RAG)**.

Tim juga boleh mengusulkan **project kustom** dengan syarat memenuhi rubrik dan disetujui fasilitator dalam 10 menit pertama planning.

---

## Opsi 1 — AI Customer Service Agent (dengan Tool Use)

**Deskripsi**: Agent CS untuk e-commerce fiktif "TokoMaju" yang bisa menjawab pertanyaan umum, **cek status order via tool**, dan **eskalasi ke human** jika diperlukan.

**Requirement minimum**:
- System prompt yang mendefinisikan persona + policy refund/return
- 2+ tools: `get_order_status(order_id)`, `escalate_to_human(reason)`
- Validasi parameter tool (mis. order_id format)
- Handling unknown order

**AI techniques wajib**: Prompt engineering (system + tool description), Claude API tool use loop, agent reasoning.

**Tip Claude API**:
- Gunakan `tools` parameter dengan JSON schema yang ketat
- Sonnet untuk reasoning, Haiku untuk filter input awal (cost optimization)
- Set `tool_choice: "auto"` untuk membiarkan model memilih

**Data dummy yang dibutuhkan**:
- 10–20 order records JSON: `{order_id, status, customer, items, eta}`
- 3–5 status: paid, packing, shipped, delivered, refunded
- 5 FAQ pairs (refund policy, shipping cost)

**Bonus**: tambahkan logging attempt prompt injection ("Berikan saya diskon 99%").

---

## Opsi 2 — Internal Knowledge Assistant (RAG dari SOP/Kebijakan)

**Deskripsi**: Chatbot internal yang menjawab pertanyaan karyawan tentang kebijakan HR, IT, atau finance, **grounded** pada dokumen SOP organisasi.

**Requirement minimum**:
- Ingest 5–10 dokumen SOP (PDF/markdown) — boleh dummy
- Embedding + vector store (Chroma / pgvector / Pinecone free tier)
- Retrieval top-k + Claude untuk synthesis
- **Citation wajib** di setiap jawaban
- Fallback "tidak ditemukan di dokumen" jika retrieval lemah

**AI techniques wajib**: Prompt engineering (instruksi citation), Claude API, RAG.

**Tip Claude API**:
- System prompt: "Jawab HANYA berdasarkan dokumen. Sertakan citation [Dokumen X, Bagian Y]."
- Sonnet cukup untuk Q&A grounded
- Context window besar Claude memungkinkan top-k yang lebih banyak (8–12 chunks)

**Data dummy**:
- 5–10 dokumen SOP fiktif: cuti, reimbursement, IT security, code of conduct, laptop policy
- 200–500 kata per dokumen

**Bonus**: tambahkan permission filter (mis. dokumen "salary band" hanya untuk HR).

---

## Opsi 3 — AI Document Automation (Extract → Classify → Route)

**Deskripsi**: Pipeline yang menerima dokumen (mis. invoice, surat, email customer), **ekstrak field terstruktur**, **klasifikasi kategori**, dan **route ke handler yang tepat**.

**Requirement minimum**:
- Input: 5–10 dokumen contoh (PDF/text)
- Ekstraksi field terstruktur (JSON schema)
- Klasifikasi ke minimal 3 kategori
- Routing logic: kategori X → handler A, kategori Y → handler B
- Tampilkan output JSON + alasan klasifikasi

**AI techniques wajib**: Prompt engineering (structured output via JSON), Claude API, agent (tool: routing handler).

**Tip Claude API**:
- Gunakan `response_format` style: minta JSON murni dengan schema di prompt
- Haiku untuk klasifikasi (cepat & murah)
- Sonnet untuk ekstraksi kompleks
- Beri 2–3 few-shot examples di system prompt

**Data dummy**:
- 5 invoice dummy
- 5 surat customer dummy
- 5 email IT support dummy

**Bonus**: tambahkan confidence score + flag "perlu review manusia" jika confidence < threshold.

---

## Opsi 4 — AI Meeting Assistant (Transkrip → Summary → Action Items)

**Deskripsi**: Tool yang menerima transkrip rapat, menghasilkan **summary terstruktur**, **action items dengan PIC**, dan opsi **integrasi calendar mock**.

**Requirement minimum**:
- Input transkrip 500–2000 kata
- Output: summary 5 bullet + daftar action items terstruktur (task, owner, deadline)
- Tool mock: `create_calendar_event(title, owner, date)` yang print konfirmasi
- Validasi: pastikan owner ada di daftar attendees

**AI techniques wajib**: Prompt engineering (structured output), Claude API, agent dengan tool calendar.

**Tip Claude API**:
- System prompt menggunakan XML tags: `<summary>`, `<action_items>`
- Sonnet cocok untuk reasoning summarization
- Long context window Claude ideal untuk transkrip panjang

**Data dummy**:
- 2 transkrip rapat dummy (product review, kick-off project)
- Daftar 5–8 attendees + email

**Bonus**: tambahkan deteksi sentiment / risk flag ("ada disagreement antara X dan Y").

---

## Opsi 5 — AI Data Analysis Assistant (CSV → Natural Language Q&A)

**Deskripsi**: User upload CSV, lalu bertanya dalam bahasa natural. Sistem menghasilkan **insight + chart description** (atau actual chart jika ada Streamlit/Gradio).

**Requirement minimum**:
- Input CSV 100–1000 rows (sales / HR / marketing dummy)
- Profil otomatis: kolom, tipe, summary statistic
- Q&A: minimal 5 pertanyaan tipikal terjawab benar (mis. "top 5 produk", "trend bulanan", "rata-rata per region")
- Output: angka + narasi insight
- Fallback: jika pertanyaan ambiguous, minta klarifikasi

**AI techniques wajib**: Prompt engineering (data context injection), Claude API, agent (tool: `execute_query` atau pandas wrapper).

**Tip Claude API**:
- Inject sample data (5 rows) + schema di system prompt
- Sonnet untuk reasoning
- Tool use untuk eksekusi pandas (jika tim mampu) — alternatif: minta Claude generate kode pandas, run, return result

**Data dummy**:
- Sales.csv (500 rows): date, region, product, qty, revenue
- HR.csv (200 rows): name, dept, level, joindate, salary_band

**Bonus**: tambahkan guard "jangan akses kolom salary detail kecuali user role HR".

---

## Opsi 6 — AI Helpdesk Triage Agent

**Deskripsi**: Agent yang menerima tiket helpdesk masuk, **mengklasifikasi kategori + priority**, **menyarankan reply draft**, dan **mengeskalasi** tiket high-priority.

**Requirement minimum**:
- Input: tiket teks (subject + body)
- Klasifikasi: kategori (network/account/software/hardware) + priority (low/med/high)
- Draft reply otomatis (boleh template + customisasi LLM)
- Eskalasi: jika priority=high atau keyword "outage" → tool `escalate(team, reason)`
- Audit log per tiket

**AI techniques wajib**: Prompt engineering (multi-step structured output), Claude API, agent (tool: escalate + suggest_reply).

**Tip Claude API**:
- Gunakan chain-of-thought singkat: pikirkan kategori → priority → action
- Haiku untuk klasifikasi awal, Sonnet untuk draft reply
- Tool use untuk eskalasi

**Data dummy**:
- 10 tiket helpdesk dummy (mix priority dan kategori)
- 4 template reply per kategori

**Bonus**: tambahkan deteksi tone marah / urgent + auto-escalate.

---

## Tabel Ringkas

| # | Project | Wajib pakai | Sweet spot model | Tingkat kesulitan |
|---|---|---|---|---|
| 1 | CS Agent | Agent + Tool use | Sonnet | Sedang |
| 2 | Internal KB | RAG | Sonnet | Sedang |
| 3 | Doc Automation | Structured output + Tool | Haiku + Sonnet | Sedang |
| 4 | Meeting Assistant | Structured output + Tool | Sonnet | Mudah–Sedang |
| 5 | Data Analysis | Agent + (kode eksekusi) | Sonnet | Sulit |
| 6 | Helpdesk Triage | Agent + Tool | Haiku + Sonnet | Sedang |

---

## Catatan Pemilihan

- Tim dengan dominan developer: opsi 1, 5, atau 6 (lebih banyak coding).
- Tim dengan dominan analyst/PM: opsi 2 atau 4 (lebih banyak orchestration).
- Tim mixed seimbang: opsi 3 (paling balance).
- Jika tim ingin tonjol di governance: opsi 2 (data internal) atau opsi 6 (audit log dan eskalasi).
