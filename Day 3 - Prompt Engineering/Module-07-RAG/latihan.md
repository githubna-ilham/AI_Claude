# Module 07 — Latihan

> Module ini terdiri dari **4 section** yang membangun RAG end-to-end di Fin-App di atas fondasi embedding dari Module 06. **Kode dari section sebelumnya akan digunakan dan diperluas di section berikutnya** — bukan ditulis ulang.
>
> Total estimasi seluruh section: ±4–5 jam efektif.

## Prinsip Kontinuitas (Wajib Diperhatikan)

- ✅ **Lanjutkan kode yang sudah ada**. Setiap prompt secara eksplisit menyebut file mana yang akan diperluas.
- ❌ **Jangan hapus** komponen yang sudah jadi di section sebelumnya, kecuali Claude / latihan secara eksplisit memintanya.
- ✅ **Verifikasi setelah setiap prompt** — pastikan section sebelumnya tidak rusak sebelum lanjut.

---

## Daftar Section

| # | Section | Fokus | Estimasi |
|---|---------|-------|----------|
| 1 | **[Pencarian Semantik](./latihan-pencarian-semantik.md)** | Helper `searchKnowledge()` + SQL query operator (3 prompt) | 50–60 menit |
| 2 | **[RAG End-to-End](./latihan-rag-end-to-end.md)** | Integrasi ke AI Advisor (system prompt + handler + citation) (4 prompt) | 70–90 menit |
| 3 | **[Chunking Strategy](./latihan-chunking.md)** | Splitter + ingest dokumen panjang ke `knowledge_chunks` (3 prompt) | 50–60 menit |
| 4 | **[Reranking & Hybrid Search](./latihan-reranking.md)** | Voyage rerank + PostgreSQL full-text + RRF (3 prompt) | 60–70 menit |

---

## Urutan yang Disarankan

Kerjakan section secara berurutan — tiap section mengandalkan output section sebelumnya. Section 1–2 membangun **RAG end-to-end minimal yang jalan**. Section 3 menambah kemampuan ingest dokumen panjang. Section 4 mengoptimalkan kualitas retrieval (opsional untuk MVP, wajib untuk production).

Pada akhir Section 4, AI Advisor di Fin-App Anda menjawab berdasarkan basis pengetahuan, menampilkan sumber kutipan, jujur saat tidak tahu, dan punya retrieval pipeline yang dapat di-tune untuk production.

🚀 Mulai: **[Section 1 — Pencarian Semantik](./latihan-pencarian-semantik.md)** (asumsi Module 06 selesai — `knowledge_chunks` sudah terisi FAQ ter-embed).
