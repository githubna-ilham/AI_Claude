# Module 06 — Latihan

> Module ini terdiri dari **3 section implementasi** yang membangun fondasi RAG di Fin-App. Konsep embedding dibahas sebagai **pendahuluan teori** di `materi.md` (tanpa latihan terpisah) — latihan dimulai langsung dari implementasi. **Kode dari section sebelumnya akan digunakan dan diperluas di section berikutnya** — bukan ditulis ulang.
>
> Total estimasi seluruh section: ±2,5–3 jam efektif.
>
> ⚠️ Module ini akan diperluas dengan section tambahan (query, prompt injection, reranking) di iterasi berikutnya.

## Prinsip Kontinuitas (Wajib Diperhatikan)

- ✅ **Lanjutkan kode yang sudah ada**. Setiap prompt secara eksplisit menyebut file mana yang akan diperluas.
- ❌ **Jangan hapus** komponen yang sudah jadi di section sebelumnya, kecuali Claude / latihan secara eksplisit memintanya.
- ✅ **Verifikasi setelah setiap prompt** — pastikan section sebelumnya tidak rusak sebelum lanjut.
- 📖 **Baca dulu** bagian "Konsep Embedding (Pendahuluan)" di `materi.md` sebelum mulai Section 1.

---

## Daftar Section

| #  | Section | Fokus | Estimasi |
|----|---------|-------|----------|
| —  | **[Konsep Embedding (Pendahuluan, baca dulu)](./materi.md#konsep-embedding-pendahuluan)** | Intuisi vektor, distance metrics, dimensi (background, tidak ada latihan) | 15–20 menit baca |
| 1  | **[Implementasi Embedding](./latihan-1-implementasi-embedding.md)** | Setup Voyage AI + `src/lib/embeddings.ts` + test similarity (3 prompt) | 50–60 menit |
| 2  | **[Database Vector](./latihan-2-database-vector.md)** | Verifikasi pgvector + eksplorasi 3 distance operator + ALTER tabel `transactions` (embedding + index HNSW + function `match_transactions`) (3 prompt) | 40–50 menit |
| 3  | **[Save Embedding ke Transactions](./latihan-3-save-embedding-db.md)** | Modifikasi `quickAddTransaction` agar auto-embed `note` + backfill transaksi lama + test semantic search end-to-end (3 prompt) | 60–70 menit |

---

## Urutan yang Disarankan

Setelah membaca pendahuluan konsep di `materi.md`, kerjakan ketiga section secara berurutan. Section 1 setup tools (Voyage `embed()`), Section 2 modifikasi schema tabel `transactions` (kolom embedding + index HNSW + function `match_transactions`), Section 3 sambungkan keduanya via auto-embed di `quickAddTransaction` + backfill + verifikasi semantic search.

Pada akhir Section 3, Fin-App Anda bisa **mencari transaksi user dengan natural language** ("kopi minggu lalu", "transport ke kantor") — fondasi untuk Module 07 (RAG) yang menggabungkan hasil ini dengan AI Financial Advisor.

🚀 Mulai: **[Section 1 — Implementasi Embedding](./latihan-1-implementasi-embedding.md)** (asumsi konsep di materi.md sudah dibaca).
