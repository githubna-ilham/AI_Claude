# DAY 3 — AI App Development + RAG

**Program**: Prompt Engineering, AI Agent & AI App Development with Claude
**Penyelenggara**: Multimatics
**Durasi total**: 4 hari (40 jam)
**Fokus Day 3**: Membangun aplikasi AI end-to-end, RAG pipeline, dan advanced enterprise patterns
**Target audiens**: Software Developer, AI/ML Engineer, Data Analyst, Product Manager, Innovation Team, IT Architect

---

## Ringkasan Day 3

Setelah Day 1 (fundamental prompt engineering) dan Day 2 (agent & tool use), Day 3 akan membawa Anda dari level "prototype di playground" menuju level "production AI application". Anda akan membangun chat app berbasis Claude, menambahkan kemampuan retrieval-augmented generation (RAG) untuk knowledge grounding, dan pada akhirnya menggabungkan semuanya menjadi sebuah Enterprise AI Assistant yang siap pakai — lengkap dengan pertimbangan biaya, observability, dan skalabilitas.

Day 3 sangat menekankan praktik: tersedia 3 modul materi dan 4 lab implementasi. Jika latar belakang Anda bukan developer (misalnya PM atau analyst), Anda tetap dapat mengikuti karena setiap lab menyediakan kerangka kode awal dan titik pemeriksaan (checkpoint) untuk peninjauan.

---

## Apa yang Akan Anda Bisa Setelah Day Ini

Setelah selesai membaca dan mempraktikkan seluruh materi Day 3, Anda akan mampu:

1. **Mendesain arsitektur AI application** end-to-end (frontend, backend, state, observability) dengan Claude sebagai inti reasoning.
2. **Mengimplementasikan chat app** dengan session management, conversation history, dan streaming response.
3. **Membangun RAG pipeline** lengkap: ingestion → chunking → embedding → vector store → retrieval → augmented prompt.
4. **Memilih komponen RAG** (vector DB, embedding model, strategi chunking) berdasarkan kebutuhan use case Anda.
5. **Mengoptimalkan AI application** dari sisi performa, biaya, dan skalabilitas (caching, batching, model routing, rate limiting).
6. **Menggabungkan chat + RAG + tool use** menjadi Enterprise AI Assistant dengan audit log dan cost tracking.

---

## Alur Module

```
Module 10 (120') ──► Module 11 (120') ──► Module 12 (90')
Build AI App         RAG Architecture     Advanced / Enterprise
   │                     │                     │
   └─ Lab 08            ├─ Lab 09             └─ Lab 11
   Chat App             │  RAG Pipeline       Enterprise Assistant
                        └─ Lab 10
                          Document Ingestion
```

| Module | Topik utama | Durasi materi | Lab |
|--------|-------------|---------------|-----|
| 10 | Arsitektur AI application, integrasi frontend, chat interface, integrasi backend AI, manajemen session & context | 120 menit | Lab 08 — Chat App |
| 11 | Arsitektur RAG, embeddings, vector DB, semantic search, knowledge retrieval, pipeline ingestion dokumen | 120 menit | Lab 09 — RAG Pipeline, Lab 10 — Document Ingestion |
| 12 | Internal AI assistant, knowledge management, automation, optimasi performa & biaya, scaling | 90 menit | Lab 11 — Enterprise AI Assistant |

---

## Jadwal (Indikatif, 8 Jam)

| Waktu | Aktivitas |
|-------|-----------|
| 08.30 – 09.00 | Recap Day 2 + ice breaker |
| 09.00 – 10.00 | Module 10 — materi (60') |
| 10.00 – 10.15 | Coffee break |
| 10.15 – 11.45 | Lab 08 — Chat App (90') |
| 11.45 – 13.00 | ISHOMA |
| 13.00 – 14.00 | Module 11 — materi (60') |
| 14.00 – 15.00 | Lab 09 — RAG Pipeline (60') |
| 15.00 – 15.15 | Coffee break |
| 15.15 – 16.00 | Lab 10 — Document Ingestion (45') |
| 16.00 – 17.00 | Module 12 — materi + walkthrough Lab 11 |
| 17.00 – 17.15 | Wrap-up Day 3 & briefing Day 4 |

> Lab 11 sebagian dapat Anda lanjutkan sebagai pekerjaan rumah atau diteruskan ke Day 4 (deployment).

---

## Prasyarat Teknis

- Python 3.11+
- API key Anthropic (sudah Anda siapkan sejak Day 1)
- Opsional: API key Voyage AI atau OpenAI (untuk embeddings)
- Docker Desktop (untuk pgvector opsional) atau Chroma lokal
- Editor: VS Code atau Cursor
- Browser modern untuk frontend chat

Pasang dependensi dasar:

```bash
pip install anthropic fastapi uvicorn chromadb voyageai \
            pypdf python-docx pandas tiktoken sentence-transformers \
            streamlit python-multipart
```

---

## Model Default

| Use case | Model |
|----------|-------|
| Reasoning utama, sintesis RAG | `claude-sonnet-4-5` |
| Chat ringan, klasifikasi, rerank | `claude-haiku-4-5` |
| Embedding (mitra Anthropic) | `voyage-3` |
| Embedding offline | `sentence-transformers/all-MiniLM-L6-v2` |

> Catatan: Anthropic **tidak menyediakan model embedding sendiri**. Untuk kebutuhan embedding, Anda dapat menggunakan Voyage AI (rekomendasi resmi Anthropic), OpenAI, atau model open-source.

---

## Checklist Persiapan

Sebelum sesi dimulai, pastikan hal-hal berikut sudah siap di lingkungan Anda:

- [ ] Vector DB Chroma sudah terpasang di mesin Anda
- [ ] Sample dataset (PDF kebijakan HR, CSV FAQ, DOCX SOP) tersedia di folder `lab-10`
- [ ] Dashboard biaya pada Anthropic console dapat Anda akses
- [ ] API key cadangan tersedia untuk berjaga-jaga jika terjadi rate limit
- [ ] Channel Slack/Discord untuk tanya-jawab asinkron sudah Anda bergabungi
