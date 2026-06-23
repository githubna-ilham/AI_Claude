# Module 05 — Latihan

> Module ini terdiri dari **4 section** yang membangun di atas hasil Module 04. Setiap section menambah satu kemampuan prompt engineering pada AI Financial Advisor. **Kode dari section sebelumnya akan digunakan dan diperluas di section berikutnya** — bukan ditulis ulang.
>
> Total estimasi seluruh section: ±3–4 jam efektif.

## Prinsip Kontinuitas (Wajib Diperhatikan)

- ✅ **Lanjutkan kode yang sudah ada**. Setiap prompt secara eksplisit menyebut file mana yang akan diperluas.
- ❌ **Jangan hapus** komponen yang sudah jadi di section sebelumnya, kecuali Claude / latihan secara eksplisit memintanya.
- ✅ **Verifikasi setelah setiap prompt** — pastikan section sebelumnya tidak rusak sebelum lanjut.

---

## Daftar Section

| #  | Section | Fokus | Estimasi |
|----|---------|-------|----------|
| 1  | **[System Instruction](./latihan-system-instruction.md)** | Migrasi dari prompt prefixing ke parameter `system` (3 prompt) | 40–50 menit |
| 2  | **[Sample Parameter & Output Control](./latihan-output-control.md)** | `top_p`, `stop_sequences`, structured output + parser transaksi (4 prompt) | 50–60 menit |
| 3  | **[Role, Context, & Instruction](./latihan-rci.md)** | Refactor RCI + fitur Insight Mingguan (3 prompt) | 50–60 menit |
| 4  | **[Agentic Workflow](./latihan-agentic.md)** | Tool use — `get_transactions`, `get_balance_summary` (4 prompt) | 60–70 menit |

---

## Urutan yang Disarankan

Kerjakan section secara berurutan — tiap section mengandalkan output section sebelumnya. Pada akhir Section 4, AI Financial Advisor Anda akan mampu mengakses data transaksi user secara mandiri lewat tool use.

🚀 Mulai: **[Section 1 — System Instruction](./latihan-system-instruction.md)** (asumsi Module 04 sudah selesai).
