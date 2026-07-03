# Module 07 — Latihan

> Module 07 ini membangun **chatbot AI Advisor yang RAG-aware** di atas fondasi Module 06 (embedding + `match_transactions`) dan Module 05 (chatbot + system prompt RCI). Tiga section, masing-masing dengan prompt copy-paste — pola yang sama dengan Module 06.
>
> Total estimasi seluruh section: ±2,5–3 jam efektif.

## Prinsip Kontinuitas (Wajib Diperhatikan)

- ✅ **Lanjutkan kode yang sudah ada**. Setiap prompt secara eksplisit menyebut file mana yang akan diperluas (mis. `prompts.ts` dari Module 05, `search-transactions.ts` dari Module 06).
- ❌ **Jangan hapus** komponen yang sudah jadi di module sebelumnya, kecuali Claude / latihan secara eksplisit memintanya.
- ✅ **Verifikasi setelah setiap prompt** — pastikan section sebelumnya tidak rusak sebelum lanjut.
- 📖 **Baca dulu** bagian "Konsep RAG" di `materi.md` sebelum mulai Section 1 — intuisi closed-book vs open-book penting supaya implementasi tidak hanya "ikut resep".

---

## Daftar Section

| # | Section | Fokus | Estimasi |
|---|---------|-------|----------|
| — | **[Konsep RAG (Pendahuluan, baca dulu)](./materi.md#konsep-rag)** | Halusinasi, closed vs open book, alur 3 langkah RAG (background, tidak ada latihan) | 15–20 menit baca |
| 1 | **[Retrieval Helper](./latihan-1-retrieval.md)** | Bangun `retrieveContextForChatbot()` yang wrap `searchTransactions` (Module 06) + format hasilnya jadi string konteks (2 prompt) | 30–40 menit |
| 2 | **[Implementasi RAG di Chatbot](./latihan-2-rag-chatbot.md)** | Tambah `ADVISOR_RAG_INSTRUCTION` + builder di `prompts.ts`, wire ke route `/api/advisor` (retrieve + augmented prompt + logging), verifikasi end-to-end via 4 skenario UI (3 prompt) | 70–90 menit |
| 3 | **[Mode Toggle: Personal vs General](./latihan-3-mode-toggle.md)** | Beri user kontrol — toggle mode `🎯 Personal` (RAG, jawab dari transaksi) vs `💬 General` (chatbot biasa tanpa retrieval). Backend branching + frontend toggle dalam 1 prompt + verifikasi A/B (2 prompt) | 40–50 menit |

---

## Urutan yang Disarankan

Setelah membaca pendahuluan konsep di `materi.md`, kerjakan ketiga section secara berurutan. Section 1 menyiapkan retrieval helper, Section 2 langsung mengintegrasikan RAG ke chatbot (prompt builder + route handler + verifikasi end-to-end), Section 3 menambahkan kontrol user untuk memilih mode RAG (Personal) atau chatbot biasa (General).

Pada akhir Section 2, chatbot Fin-App Anda bisa menjawab pertanyaan seperti _"ada pengeluaran kopi minggu lalu?"_ dengan transaksi nyata user — bukan halusinasi. Pada akhir Section 3, user punya **kontrol** kapan ingin jawaban berbasis data pribadi (Personal) dan kapan cukup jawaban umum (General).

🚀 Mulai: **[Section 1 — Retrieval Helper](./latihan-1-retrieval.md)** (asumsi konsep di materi.md sudah dibaca + Module 06 sudah selesai).

---

🏠 Kembali: **[Day 4 — AI Agent & Tools](../README.md)** · ➡️ Lanjut: **[Module 08 — AI Agent](../Module-08-AI-Agent/materi.md)** (function calling untuk akses data terstruktur)
