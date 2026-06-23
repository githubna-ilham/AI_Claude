# Module 04 — Latihan

> Module ini terdiri dari **6 section** (+ 1 latihan UI di Module 03 sebagai prasyarat) yang dirangkai berurutan. Setiap section adalah lapis inkremental pada fitur AI Financial Advisor di Fin-App. **Kode dari section sebelumnya akan digunakan dan diperluas di section berikutnya** — bukan ditulis ulang.
>
> Total estimasi seluruh section: ±4–5 jam efektif.

## Prinsip Kontinuitas (Wajib Diperhatikan)

Sebelum mulai, pahami prinsip ini agar tidak menulis ulang kode tanpa perlu:

- ✅ **Lanjutkan kode yang sudah ada**. Setiap prompt secara eksplisit menyebut file mana yang akan diperluas dan komponen mana yang akan dimodifikasi.
- ❌ **Jangan hapus** komponen yang sudah jadi di section sebelumnya, kecuali Claude / latihan secara eksplisit memintanya.
- ✅ **Verifikasi setelah setiap prompt** — pastikan section sebelumnya tidak rusak sebelum lanjut ke prompt berikutnya.

---

## Daftar Section

| #  | Section | Fokus | Estimasi |
|----|---------|-------|----------|
| 0  | **[Latihan UI Chatbot (Module 03)](../../Day 2 - Road To AI Apps/Module-03-Claude-API/latihan-ui-chatbot.md)** | Layout 3-kolom + panel chatbot statis (5 prompt) — prasyarat | 45–60 menit |
| 1  | **[Integrasi Claude API ke Chatbot](./latihan-1-integrasi-api.md)** | Server action `askAdvisor` + welcome + error handling (4 prompt) | 40–50 menit |
| 2  | **[Text Generation](./latihan-2-text-generation.md)** | `temperature`, `max_tokens`, prompt prefixing (4 prompt) | 35–45 menit |
| 3  | **[Thinking / Thought](./latihan-3-thinking.md)** | Extended thinking + collapsible UI (4 prompt) | 40–50 menit |
| 4  | **[Switching Thinking Mode](./latihan-4-switching-thinking.md)** | Toggle thinking + budget low/medium/high (4 prompt) | 30–40 menit |
| 5  | **[Streaming Process](./latihan-5-streaming.md)** | Route handler streaming + client consume `ReadableStream` (3 prompt) | 50–60 menit |
| 6  | **[Multi-Turn Conversation](./latihan-6-multi-turn.md)** | Kirim riwayat percakapan + reset (3 prompt) | 30–40 menit |

---

## Urutan yang Disarankan

Kerjakan section secara berurutan — tiap section mengandalkan output section sebelumnya. Setelah selesai semua, kembali ke akhir **[Section 6](./latihan-6-multi-turn.md#-validasi-akhir-module-04-seluruh-6-section)** untuk **Validasi Akhir Module 04**.

🚀 Mulai: **[Latihan UI Chatbot (Module 03)](../../Day 2 - Road To AI Apps/Module-03-Claude-API/latihan-ui-chatbot.md)** — lalu lanjut ke Section 1.
