# Speaker Notes — Module 2: Prompt Engineering Basics

**Total alokasi**: 90 menit
**Mode**: Lecture 50% + demo 25% + workshop singkat 25%

---

## Anekdot Pembuka (3 menit)

> "Saya pernah punya intern yang sangat pintar. IPK 3.95, fasih 3 bahasa. Tapi minggu pertama, saya minta dia 'tolong buatkan laporan keuangan bulanan' dan saya pergi meeting. Dua jam kemudian saya kembali — dia menyerahkan laporan untuk perusahaan dengan format yang dia bayangkan, untuk audiens yang dia tebak, dengan asumsi yang tidak pernah saya ucapkan. Itulah Claude bagi Anda — jenius tanpa konteks. Module ini adalah cara Anda menjadi atasan yang baik bagi intern itu."

---

## Alokasi Waktu per Bagian

| Bagian                                | Durasi | Tipe         |
|---------------------------------------|--------|--------------|
| Pembuka + anekdot                     | 3 m    | Cerita       |
| 1. Mengapa anatomi penting            | 7 m    | Lecture      |
| 2. Role prompting                     | 10 m   | Lecture + contoh |
| 3. Context engineering                | 12 m   | Lecture + XML demo |
| 4. Task / Instruction design          | 10 m   | Lecture      |
| 5. Constraint                         | 8 m    | Lecture      |
| 6. Output format                      | 7 m    | Lecture      |
| 7. Prompt template & versioning       | 8 m    | Lecture      |
| Demo live (CS reply refactor)         | 15 m   | Demo         |
| Walkthrough contoh poor→good→better   | 5 m    | Walkthrough  |
| Q&A + handoff ke Lab 01               | 5 m    | Diskusi      |

Total: 90 menit.

---

## Cue Fasilitator per Bagian

### Bagian 2 — Role Prompting
- Demonstrasikan **A/B test**: jalankan prompt tanpa role vs dengan role di Workbench. Tunjukkan vocabulary shift.
- Hindari role yang berlebihan dramatis ("Anda adalah dewa coding"). Jelaskan kenapa: bisa memicu over-confidence.

### Bagian 3 — Context Engineering
- Tunjukkan **live** penggunaan XML tag. Banyak peserta tidak tahu Claude punya bias positif terhadap struktur XML.
- Pertanyaan kepada peserta: "Mengapa kita pakai `<document>` bukan markdown `# Document`?" Jawaban: lebih unambiguous, tidak bentrok dengan markdown rendering, dilatih eksplisit.

### Bagian 4 — Task Design
- Latihan cepat 2 menit: minta peserta menulis ulang "Analisis dokumen ini" menjadi task yang spesifik. Bahas 2-3 jawaban.

### Bagian 5 — Constraint
- Tekankan positive framing. Ada studi (Anthropic blog) yang menunjukkan negation kadang diabaikan.

### Bagian 6 — Output Format
- Bridge ke Module 4 (JSON output) — "kita akan kembali ke ini lebih mendalam di module akhir hari ini".

### Bagian 7 — Template & Versioning
- Pertanyaan provokatif: "Siapa di tim Anda yang **memiliki** prompt produksi saat ini?" → biasanya jawabannya "tidak ada / semua orang" = red flag.

---

## Jawaban Kunci untuk Pertanyaan Refleksi

1. **Komponen yang sering dilupa**: biasanya **Constraint** dan **Output Format**. Dampak: output panjang/short tak terduga, parsing gagal, tone inkonsisten.
2. **Role efektif vs kosmetik**: efektif = expertise + audience eksplisit, konsisten dengan task. Kosmetik = generik, tidak mempengaruhi distribusi output.
3. **Positive vs negative framing**: model dilatih next-token prediction; "jangan X" tetap menampilkan token "X" dalam konteks, yang bisa men-trigger pola tersebut. Positive framing memberi arah jelas.
4. **Versioning**: idealnya prompt disimpan di Git, ada owner (PM atau ML engineer), dengan changelog dan suite eval — paralel dengan praktik code review.
5. **Risiko over-constrained**: brittle, gagal di edge case yang tidak diantisipasi, output robotik. Solusi: tier constraint (must-have vs nice-to-have).

---

## Common Pitfall Peserta

| Pitfall                                                              | Respons fasilitator |
|----------------------------------------------------------------------|----|
| Prompt terlalu panjang ("over-prompt")                               | Aturan 80/20: paretto. Mulai dari minimum viable prompt, tambahkan constraint hanya ketika ada bukti masalah. |
| Mencampur instruksi & data dalam satu paragraf                       | Tunjukkan XML wrapping. |
| Menulis "Anda adalah expert" tanpa spesialisasi                      | Latih persona drilling. |
| Mengandalkan model "tahu" istilah internal organisasi                | Lampirkan glossary. |
| Memberi multiple task dalam 1 prompt tanpa numbering                 | Decompose & numbering eksplisit. |
| Negation excessive ("jangan X, jangan Y, jangan Z")                  | Refactor ke positive. |
| Output format markdown padahal akan di-parse program                 | Pindah ke JSON / XML strict. |

---

## Catatan untuk Demo CS Reply

Siapkan 3 versi prompt sebagai snippet di clipboard manager. Jalankan beruntun di tab claude.ai yang sama agar peserta lihat regression/improvement.

Variasi cadangan jika audiens lebih tertarik internal use case: ganti CS reply dengan "tulis ulang notulen rapat menjadi action items".

---

## Transisi ke Lab 01

> "Sekarang giliran Anda. Saya akan beri 5 prompt buruk dari use case nyata di organisasi. Tugas Anda: refactor dengan 5 komponen anatomi. 45 menit, individual atau pair. Kita akan peer-review 2 prompt terbaik di akhir."
