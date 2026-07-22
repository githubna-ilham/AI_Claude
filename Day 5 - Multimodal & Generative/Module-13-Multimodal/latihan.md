# Module 09 — Latihan

> Module 09 membangun **kemampuan multimodal** di Fin-App: upload foto kwitansi → Claude vision membaca → ekstrak transaksi via tool use → insert ke `transactions`. Tiga section, pola yang sama dengan Module 06/07/08.
>
> Total estimasi seluruh section: ±2,5–3 jam efektif.

## Prinsip Kontinuitas (Wajib Diperhatikan)

- ✅ **Lanjutkan kode yang sudah ada** dari Module 05 Section 5 (pattern tool use untuk save_transaction) dan Module 08 Section 2 (`TOOLS` array di `src/lib/tools.ts` + dispatcher pattern).
- ❌ **Jangan hapus** komponen yang sudah jadi di module sebelumnya, kecuali Claude / latihan secara eksplisit memintanya.
- ✅ **Verifikasi setelah setiap prompt** — pastikan section sebelumnya tidak rusak sebelum lanjut.
- 📖 **Baca dulu** bagian "Konsep Multimodal" di `materi.md` sebelum mulai Section 1 — intuisi vision API (cara kirim image + cost token + model support) penting supaya implementasi tidak hanya "ikut resep".

---

## Daftar Section

| # | Section | Fokus | Estimasi |
|---|---------|-------|----------|
| — | **[Konsep Multimodal (Pendahuluan, baca dulu)](./materi.md#konsep-multimodal)** | Apa itu multimodal, format input image/PDF, model yang support vision, biaya, use case Fin-App (background, tidak ada latihan) | 15–20 menit baca |
| 1 | **[Vision API Basics (Script PoC)](./latihan-1-vision-basics.md)** | Script terminal: baca file foto kwitansi lokal → base64 → Claude vision → cetak deskripsi. Bukti API + encoding bekerja sebelum membangun UI (2 prompt) | 30–40 menit |
| 2 | **[Upload UI + Base64 Pipeline](./latihan-2-upload-ui.md)** | Komponen `<UploadKwitansi />` di halaman transaksi dengan `FileReader` → base64 → server action `parseReceipt` (skeleton, belum parse). Verifikasi delivery path browser → server (2 prompt) | 30–40 menit |
| 3 | **[Receipt Extraction + Auto-Insert](./latihan-3-receipt-extraction.md)** | Lengkapi `parseReceipt`: tool `save_receipt_transactions` (force tool choice) → Claude vision baca struk → array items → insert paralel ke `transactions`. Test 3 skenario foto (3 prompt) | 70–90 menit |

---

## Urutan yang Disarankan

Setelah membaca pendahuluan konsep di `materi.md`, kerjakan ketiga section secara berurutan. Section 1 memastikan vision API bekerja via script terminal (tanpa UI/DB), Section 2 membangun delivery path dari browser ke server (tanpa parsing), Section 3 menggabungkan keduanya menjadi pipeline lengkap.

Pada akhir Section 3, user dapat upload foto kwitansi → Claude membaca struk → array items ter-ekstrak → semua transaksi insert paralel ke `transactions`. UX-nya: klik tombol upload, pilih foto, tunggu 2–3 detik, dapat konfirmasi `"3 transaksi tercatat dari Starbucks"`.

🚀 Mulai: **[Section 1 — Vision API Basics](./latihan-1-vision-basics.md)** (asumsi konsep di materi.md sudah dibaca + Module 05 Section 5 sudah selesai).

---

🏠 Kembali: **[Day 4 — AI Agent & Tools](../README.md)** · ➡️ Lanjut: **Module 10+** (akan datang)
