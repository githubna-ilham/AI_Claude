# Panduan Import Pretest ke Google Form

Dokumen ini menjelaskan cara memindahkan isi `PRETEST-AI-Claude.md` ke Google Form.

## Pemetaan Tipe Pertanyaan

| No.       | Tipe di Markdown                  | Tipe di Google Form                             |
| --------- | --------------------------------- | ----------------------------------------------- |
| 1–3       | Isian singkat                     | **Short answer**                                |
| 4         | Role                              | **Multiple choice** (+ opsi "Lainnya")          |
| 5–6       | Pengalaman / fokus role           | **Multiple choice**                             |
| 7         | Bahasa (boleh >1)                 | **Checkboxes**                                  |
| 8–9       | Skala 1–5                         | **Linear scale (1–5)**                          |
| 10        | REST API familiarity              | **Multiple choice**                             |
| 11        | Database (boleh >1)               | **Checkboxes**                                  |
| 12        | Git                               | **Multiple choice**                             |
| 13        | AI tools (boleh >1)               | **Checkboxes**                                  |
| 14        | Frekuensi AI                      | **Multiple choice**                             |
| 15        | Tugas AI (boleh >1)               | **Checkboxes**                                  |
| 16        | Skala prompt engineering          | **Linear scale (1–5)**                          |
| 17        | Claude API experience             | **Multiple choice**                             |
| 18        | Konsep familiar (checklist)       | **Checkboxes**                                  |
| 19        | Pengalaman build (checklist)      | **Checkboxes**                                  |
| 20        | Adopsi AI organisasi              | **Multiple choice**                             |
| 21        | Use case (boleh >1)               | **Checkboxes**                                  |
| 22        | Kebijakan AI                      | **Multiple choice**                             |
| 23        | Sumber data RAG (boleh >1)        | **Checkboxes**                                  |
| 24–30     | Baseline knowledge                | **Multiple choice** (1 jawaban)                 |
| 31–36     | Isian panjang                     | **Paragraph**                                   |

> **Tip efisiensi:** Soal 8–9 & 16 (skala) sebaiknya digabung ke **satu Grid pertanyaan** (Multiple-choice grid) — baris = area, kolom = nilai 1–5.

## Pembagian Section (Halaman) di Google Form

1. **Section 1** — Identitas & Profil (soal 1–6)
2. **Section 2** — Latar Belakang Teknis (soal 7–12)
3. **Section 3** — Pengalaman AI / LLM (soal 13–19)
4. **Section 4** — Konteks Organisasi & Use Case (soal 20–23)
5. **Section 5** — Baseline Knowledge (soal 24–30)
6. **Section 6** — Ekspektasi & Pain Points (soal 31–36)

## Setting yang Disarankan

- **Pengaturan → Respons:** ✅ Collect email, ✅ Limit to 1 response, ❌ Allow response editing
- **Pengaturan → Presentasi:** ✅ Show progress bar
- **Quiz mode:** Aktifkan **HANYA** jika ingin auto-grade Bagian 5 sebagai indikator (jangan tampilkan skor ke peserta).

### Kunci Jawaban Bagian 5 (untuk fasilitator)

| Soal | Jawaban Benar                                                                            |
| ---- | ---------------------------------------------------------------------------------------- |
| 24   | LLM memprediksi token berikutnya berdasarkan pola dari data training                     |
| 25   | Jumlah token maksimum yang bisa diproses dalam satu request (input + output)             |
| 26   | Beberapa contoh input-output di dalam prompt agar model meniru polanya                   |
| 27   | Mencari dokumen relevan → menyisipkan ke prompt → LLM menjawab berdasar dokumen          |
| 28   | Bisa merencanakan, memilih tool, mengeksekusi action multi-step untuk mencapai tujuan    |
| 29   | Attacker menyisipkan instruksi berbahaya lewat input user agar LLM mengabaikan instruksi sistem |
| 30   | Gunakan retrieval relevan, sanitize input, simpan API key di backend, audit log          |

## Analisis Hasil

Kelompokkan per dimensi:

- **Profil teknis (soal 7–12)** → tentukan kedalaman koding di Day 2–3 (Claude API & RAG)
- **AI literacy (soal 13–19)** → tentukan kecepatan pacing Day 1
- **Konsep familiar (soal 18)** → identifikasi konsep yang perlu emphasis ekstra
- **Adopsi organisasi (soal 20–23)** → bahan studi kasus Module 13–14
- **Use case (soal 21, 33)** → bahan demo Module 5 + opsi Capstone
- **Pain points (soal 32)** → bahan diskusi pembuka Module 13

## Estimasi Waktu Distribusi

| Aktivitas                       | Waktu                       |
| ------------------------------- | --------------------------- |
| Pretest dikirim ke peserta      | H-7 sebelum hari pertama    |
| Deadline pengisian              | H-3                         |
| Analisis hasil oleh fasilitator | H-2 (2-3 jam)               |
| Penyesuaian materi & contoh     | H-1                         |
