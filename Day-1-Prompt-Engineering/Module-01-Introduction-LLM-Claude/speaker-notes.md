# Speaker Notes — Module 1: Introduction to LLM & Claude

**Total alokasi**: 90 menit
**Mode**: Lecture (60%) + demo (25%) + diskusi cepat (15%)

---

## Anekdot Pembuka (5 menit)

> "Tahun 2022 saya minta GPT-3 menulis bio singkat saya. Ia memberi jawaban yang sangat meyakinkan: lulusan universitas X, bekerja di perusahaan Y, dengan pencapaian Z. Masalahnya: tidak satupun benar. Tapi saya hampir percaya — itulah PR kita hari ini: belajar berbicara dengan mesin yang sangat fasih tapi tidak tahu kapan ia ngarang."

Gunakan untuk membangun rasa hormat sehat terhadap kapabilitas + limitasi LLM.

---

## Alokasi Waktu per Bagian

| Bagian materi                              | Durasi | Tipe        |
|--------------------------------------------|--------|-------------|
| Pembuka + anekdot                          | 5 m    | Cerita      |
| 1. Apa itu LLM                             | 10 m   | Lecture     |
| 2. Transformer architecture                | 10 m   | Lecture + analogi |
| 3. Tokenization & context window           | 10 m   | Lecture + live tokenizer |
| 4. Claude — kapabilitas & limitasi         | 10 m   | Lecture + tabel |
| 5. AI reasoning & hallucination            | 10 m   | Lecture     |
| Demo Live (A, B, C, D)                     | 20 m   | Demo        |
| Contoh konkret poor→good→better            | 5 m    | Walkthrough |
| Wrap-up + Q&A                              | 10 m   | Diskusi     |

Total: 90 menit.

---

## Cue Fasilitator per Bagian

### Bagian 1 — Apa itu LLM
- Tanya audiens: "Siapa pernah pakai autocomplete keyboard di HP?" → bridge ke konsep next-token prediction.
- Tekankan: "stateless" — penting untuk modul berikutnya.

### Bagian 2 — Transformer
- **Jangan masuk matematika**. Gunakan analogi rapat (self-attention = saling mendengarkan).
- Audiens campuran: developer akan kurang puas, manager akan over-cognitive load. Tarik garis tengah dengan tetap di level intuisi.

### Bagian 3 — Tokenization
- **Live demo wajib**: buka tokenizer online, paste "Multimatics adalah perusahaan training IT". Tunjukkan jumlah token. Bandingkan dengan teks Inggris ekuivalen.
- Anekdot: "Bahasa Indonesia umumnya 20–30% lebih boros token = 20–30% lebih mahal di API."

### Bagian 4 — Claude family
- Minta audiens **menebak** kapan pakai Haiku vs Opus sebelum Anda jawab.
- Hindari menjual model tertentu; framing harus "trade-off engineering".

### Bagian 5 — Hallucination
- Pertanyaan provokatif: "Apakah hallucination adalah bug atau fitur?" → diskusi 2 menit. Jawaban kunci: ia adalah konsekuensi langsung dari arsitektur generatif, bukan bug yang bisa "diperbaiki" 100%.

---

## Jawaban Kunci untuk Pertanyaan Refleksi

1. **Konsekuensi autocomplete probabilistik**: kita harus memberi spesifikasi, bukan inspirasi. Prompt = kontrak. Output tergantung penuh pada framing.
2. **Haiku vs Sonnet**: Haiku untuk volume tinggi, latency-sensitive (auto-tagging, classification), low-stakes. Sonnet untuk customer-facing, reasoning sedang. Opus untuk reasoning kompleks atau ketika kualitas > biaya.
3. **Pekerjaan berisiko + mitigasi**: laporan compliance, advice legal, diagnosis. Mitigasi: human-in-the-loop, grounding ke sumber, abstain rule, dan logging untuk audit.
4. **Context window besar ≠ jawaban lebih baik**: "lost in the middle" effect, biaya naik, sinyal-noise ratio turun. Lebih besar bukan lebih baik tanpa context engineering.
5. **Reasoning LLM vs manusia**: LLM = pattern continuation, manusia = simbolik + grounded + embodied. LLM bisa convincing tanpa coherent.

---

## Common Pitfall Peserta

| Pitfall                                                    | Cara fasilitator merespons |
|------------------------------------------------------------|----------------------------|
| "Berarti LLM tidak bisa dipercaya sama sekali?"            | Bedakan trust vs verify. Trustworthy with guardrails. |
| "Apa beda LLM dengan search engine?"                       | Search = retrieval, LLM = generation. Bisa digabung (RAG, Day 3). |
| "Kalau saya kasih semua data ke context window, selesai dong?" | Lost-in-the-middle + cost. Tunjukkan studi singkat. |
| "Claude lebih baik dari GPT?"                              | Hindari debat fanboy. Framing: tools, fit-for-purpose. |
| "Kenapa output beda tiap run?"                             | Temperature & sampling. Kenalkan deterministik mode untuk eval. |
| Skeptis berlebihan ("ini hype semua")                       | Akui keterbatasan; tunjukkan use case ROI nyata dari pengalaman. |
| Antusias berlebihan ("ganti semua karyawan")               | Realitas: cost, error rate, edge case. Bangun ekspektasi sehat. |

---

## Catatan Teknis Demo

- Pastikan koneksi internet stabil; siapkan screenshot backup jika claude.ai down.
- Sebelum sesi, **pre-load** prompt di Console Workbench untuk demo perbandingan model — akan lebih cepat dan terlihat profesional.
- Jika peserta minta lihat extended thinking: tunjukkan di Console (toggle Extended Thinking pada Sonnet/Opus 4.x). Ingatkan ini akan dibahas dalam di Day 3.

---

## Transisi ke Module 2

> "Sekarang kita tahu LLM adalah mesin autocomplete probabilistik yang stateless dan finit. Konsekuensinya: kualitas output ditentukan 80% oleh kualitas input. Mari kita pelajari anatomi input — alias prompt — yang baik."
