# DAY 3 — AI App Development + RAG

**Program**: Prompt Engineering, AI Agent & AI App Development with Claude
**Penyelenggara**: Multimatics
**Durasi total**: 4 hari (40 jam)
**Fokus Day 3**: Membangun aplikasi AI end-to-end, RAG pipeline, dan advanced enterprise patterns
**Target audiens**: Software Developer, AI/ML Engineer, Data Analyst, Product Manager, Innovation Team, IT Architect

---

## Ringkasan Day 3

Setelah Day 1 (fundamental prompt engineering) dan Day 2 (agent & tool use), Day 3 mengangkat peserta dari level "prototype di playground" ke level "production AI application". Peserta akan membangun chat app berbasis Claude, menambahkan kemampuan retrieval-augmented generation (RAG) untuk knowledge grounding, dan akhirnya menggabungkan semuanya menjadi Enterprise AI Assistant siap-pakai dengan pertimbangan cost, observability, dan scaling.

Day 3 sangat hands-on: 3 module materi + 4 lab implementasi. Peserta yang berlatar non-developer (PM, analyst) tetap dapat mengikuti karena setiap lab menyediakan skeleton kode dan checkpoint review.

---

## Learning Outcomes

Pada akhir Day 3, peserta akan mampu:

1. **Mendesain arsitektur AI application** end-to-end (frontend, backend, state, observability) dengan Claude sebagai reasoning core.
2. **Mengimplementasikan chat app** dengan session management, conversation history, dan streaming response.
3. **Membangun RAG pipeline** lengkap: ingestion → chunking → embedding → vector store → retrieval → augmented prompt.
4. **Memilih komponen RAG** (vector DB, embedding model, chunking strategy) berdasarkan kebutuhan use case.
5. **Mengoptimalkan AI application** dari sisi performance, biaya, dan skalabilitas (caching, batching, model routing, rate limiting).
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
| 10 | AI application architecture, frontend integration, chat interface, backend AI integration, session & context management | 120 menit | Lab 08 — Chat App |
| 11 | RAG architecture, embeddings, vector DB, semantic search, knowledge retrieval, document ingestion pipeline | 120 menit | Lab 09 — RAG Pipeline, Lab 10 — Document Ingestion |
| 12 | Internal AI assistant, knowledge management, automation, performance & cost optimization, scaling | 90 menit | Lab 11 — Enterprise AI Assistant |

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
| 16.00 – 17.00 | Module 12 — materi + Lab 11 walkthrough |
| 17.00 – 17.15 | Wrap-up Day 3 & briefing Day 4 |

> Lab 11 sebagian dilanjutkan sebagai pekerjaan rumah / kelanjutan ke Day 4 (deployment).

---

## Prasyarat Teknis

- Python 3.11+
- API key Anthropic (sudah disiapkan dari Day 1)
- Optional: API key Voyage AI atau OpenAI (untuk embeddings)
- Docker Desktop (untuk pgvector opsional) atau Chroma lokal
- Editor: VS Code atau Cursor
- Browser modern untuk frontend chat

Install dependencies dasar:

```bash
pip install anthropic fastapi uvicorn chromadb voyageai \
            pypdf python-docx pandas tiktoken sentence-transformers \
            streamlit python-multipart
```

---

## Model Default

| Use case | Model |
|----------|-------|
| Reasoning utama, RAG synthesis | `claude-sonnet-4-5` |
| Chat ringan, classification, rerank | `claude-haiku-4-5` |
| Embedding (mitra Anthropic) | `voyage-3` |
| Embedding offline | `sentence-transformers/all-MiniLM-L6-v2` |

> Catatan: Anthropic **tidak menyediakan model embedding sendiri**. Untuk embedding gunakan Voyage AI (rekomendasi resmi Anthropic), OpenAI, atau model open-source.

---

## Checklist Persiapan Fasilitator

- [ ] Vector DB Chroma sudah ter-install di mesin peserta
- [ ] Sample dataset (PDF kebijakan HR, CSV FAQ, DOCX SOP) tersedia di `lab-10`
- [ ] Cost dashboard Anthropic console di-share screen
- [ ] Backup API key proxy jika rate limit
- [ ] Slack/Discord channel untuk Q&A async
