# Module 06 — Latihan

> Module ini terdiri dari **4 section** yang membangun fondasi RAG di Fin-App. **Kode dari section sebelumnya akan digunakan dan diperluas di section berikutnya** — bukan ditulis ulang.
>
> Total estimasi seluruh section: ±4–5 jam efektif.
>
> ⚠️ Module ini akan diperluas dengan section tambahan (query, prompt injection, reranking) di iterasi berikutnya.

## Prinsip Kontinuitas (Wajib Diperhatikan)

- ✅ **Lanjutkan kode yang sudah ada**. Setiap prompt secara eksplisit menyebut file mana yang akan diperluas.
- ❌ **Jangan hapus** komponen yang sudah jadi di section sebelumnya, kecuali Claude / latihan secara eksplisit memintanya.
- ✅ **Verifikasi setelah setiap prompt** — pastikan section sebelumnya tidak rusak sebelum lanjut.

---

## Daftar Section

| #  | Section | Fokus | Estimasi |
|----|---------|-------|----------|
| 1  | **[Konsep Embedding](./latihan-konsep-embedding.md)** | Eksplorasi konseptual + hitung cosine similarity manual (2 prompt) | 30–40 menit |
| 2  | **[Implementasi Embedding](./latihan-implementasi-embedding.md)** | Setup Voyage AI + `src/lib/embeddings.ts` + test similarity (3 prompt) | 50–60 menit |
| 3  | **[Database Vector](./latihan-database-vector.md)** | Verifikasi pgvector + bikin table `knowledge_chunks` + query playground (3 prompt) | 40–50 menit |
| 4  | **[Save Embedding To DB Vector](./latihan-save-embedding-db.md)** | Helper save + seed FAQ data + verifikasi roundtrip (3 prompt) | 60–70 menit |

---

## Urutan yang Disarankan

Kerjakan section secara berurutan — tiap section mengandalkan output section sebelumnya. Section 1 bersifat konseptual (sedikit kode, banyak intuisi), sedangkan Section 2–4 bersifat implementasi yang membangun pipeline data.

Pada akhir Section 4, Fin-App Anda memiliki table `knowledge_chunks` yang sudah berisi FAQ keuangan ter-embed dan siap di-query — fondasi untuk iterasi RAG selanjutnya.

🚀 Mulai: **[Section 1 — Konsep Embedding](./latihan-konsep-embedding.md)** (asumsi Module 05 sudah selesai).
