# Module 05 — Latihan

> Module ini terdiri dari **5 section** yang membangun di atas hasil Module 04. Setiap section menambah satu kemampuan prompt engineering pada AI Financial Advisor. **Kode dari section sebelumnya akan digunakan dan diperluas di section berikutnya** — bukan ditulis ulang.
>
> Total estimasi seluruh section: ±4–5 jam efektif.

## Prinsip Kontinuitas (Wajib Diperhatikan)

- ✅ **Lanjutkan kode yang sudah ada**. Setiap prompt secara eksplisit menyebut file mana yang akan diperluas.
- ❌ **Jangan hapus** komponen yang sudah jadi di section sebelumnya, kecuali Claude / latihan secara eksplisit memintanya.
- ✅ **Verifikasi setelah setiap prompt** — pastikan section sebelumnya tidak rusak sebelum lanjut.

---

## Daftar Section

| #  | Section | Fokus | Estimasi |
|----|---------|-------|----------|
| 1  | **[System Instruction](./latihan-1-system-instruction.md)** | Migrasi dari prompt prefixing ke parameter `system` (2 prompt) | 30–40 menit |
| 2  | **[Output Control](./latihan-2-output-control.md)** | Tighten system prompt + `stop_sequences` + `max_tokens` strategy + test konsistensi (4 prompt) | 45–60 menit |
| 3  | **[Role, Context, & Instruction](./latihan-3-rci.md)** | Refactor RCI + fitur Insight Mingguan (3 prompt) | 50–60 menit |
| 4  | **[Agentic Workflow](./latihan-4-agentic.md)** | 5-step workflow + test konsistensi (2 prompt) | 40–50 menit |
| 5  | **[Structured Output (JSON)](./latihan-5-structured-output.md)** | Quick-add transaksi via natural language — tool use Claude → insert Supabase (3 prompt). Pengenalan agentic AI. | 60–75 menit |

---

## Urutan yang Disarankan

Kerjakan section secara berurutan — tiap section mengandalkan output section sebelumnya. Pada akhir Section 5, AI Financial Advisor Anda akan memiliki **5-step reasoning workflow** + **fitur quick-add transaksi natural language** (Claude mem-parse "ngopi 5000" → JSON terstruktur → insert ke Supabase) yang menjadi fondasi paradigma **agentic AI** di module berikutnya.

🚀 Mulai: **[Section 1 — System Instruction](./latihan-1-system-instruction.md)** (asumsi Module 04 sudah selesai).
