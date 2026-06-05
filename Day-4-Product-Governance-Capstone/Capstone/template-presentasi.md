# Template Presentasi Capstone

**Format**: 7–9 slide, 15 menit pitching + demo, 10 menit Q&A
**Filosofi**: bayangkan Anda mempresentasikan ke Head of Data / CTO di organisasi Anda — bukan ke kelas pelatihan.

---

## Struktur Slide

### Slide 1 — Cover

- Nama project + tagline 1 kalimat
- Nama tim + role tiap anggota
- Logo organisasi (opsional)

**Goal**: menjelaskan dalam 10 detik "ini apa, siapa yang bikin".

---

### Slide 2 — Problem

- **Problem statement**: 1–2 kalimat. Hindari jargon.
- **Siapa yang menderita**: persona + volume.
- **Bukti masalah**: 1 angka / kutipan / observasi nyata.

**Goal**: meyakinkan juri bahwa ini masalah nyata, bukan solusi mencari masalah.

**Contoh**:
> "Tim CS TokoMaju menangani 800 tiket/hari, 60% pertanyaan FAQ berulang. Rata-rata response time 18 jam, NPS turun 12 poin dalam 6 bulan terakhir."

---

### Slide 3 — User & Business Value

- Primary + secondary user (persona 1 baris).
- **Estimasi value**: cost saved / revenue uplift / risk reduced — dalam angka.
- "Mengapa sekarang" — strategic rationale.

**Goal**: jawab pertanyaan CFO "kenapa saya kasih budget?"

---

### Slide 4 — Solution Architecture

- Diagram arsitektur (mermaid / drawio / hand-drawn — yang penting jelas).
- Komponen utama: UI, orchestration, Claude model variant, RAG/tools, guardrails, observability.
- Tech stack singkat.

**Goal**: tunjukkan tim paham anatomy sistem AI production-grade.

---

### Slide 5 — Prompt Engineering

- Tampilkan **1 system prompt aktual** (boleh dipotong agar muat).
- Highlight teknik yang dipakai: role + context + constraint + format + delimiter / XML tag / few-shot.
- 1 contoh sebelum/sesudah refinement prompt.

**Goal**: tunjukkan prompt engineering bukan "asal tulis instruksi", tapi engineering discipline.

---

### Slide 6 — AI Agent / Tool Use (jika dipakai)

- Daftar tools yang di-expose.
- 1 contoh tool call dengan parameter aktual.
- Bagaimana validasi parameter dilakukan.
- Bagaimana failure case ditangani.

**Atau** —

### Slide 6 (alt) — RAG (jika dipakai)

- Pipeline: ingest → chunk → embed → store → retrieve → generate.
- Strategi chunking + embedding model.
- Bagaimana citation di-render.
- Top-k strategi.

**Goal**: kedalaman teknis di area kompetensi inti tim.

---

### Slide 7 — Demo (live)

- Tidak banyak teks di slide — ini cue untuk **live demo**.
- Path demo: 1 happy path + 1 edge case + 1 attempted attack/abuse (jika ada).
- **Wajib live**, slide screenshot hanya jika koneksi gagal.

**Goal**: bukti bahwa prototype benar-benar berjalan.

---

### Slide 8 — Governance Considerations

- Minimal 5 item dari `checklist-responsible-AI.md` yang sudah dipertimbangkan tim.
- 1 risiko utama + mitigasi yang sudah diimplement.
- 1 risiko yang masih backlog + rencana penanganan.
- Penyebutan compliance relevan (UU PDP, sektoral).

**Goal**: tunjukkan kematangan — tim sadar trade-off, bukan techno-utopian.

---

### Slide 9 — Lessons Learned + Roadmap

- 2–3 pelajaran kunci dari proses Capstone.
- Roadmap Crawl–Walk–Run jika tim akan melanjutkan ini ke pilot di organisasi.
- Call to action: "ini langkah berikutnya jika diberi 4 minggu + Rp X".

**Goal**: tinggalkan kesan bahwa ini bukan one-shot demo, tapi awal sesuatu yang serius.

---

## Tips Presentasi

- **Time-keeper wajib**. 15 menit cepat berlalu.
- **1 orang 1 slide besar** — bagi peran. Jangan ada anggota tim yang tidak bicara.
- **Demo dulu, baru penjelasan** — jika berani. Demo yang mulus = 50% kemenangan.
- **Tampilkan 1 failure** dengan rendah hati. Juri akan respect.
- **Hindari**: "AI-powered", "next-gen", "revolusi" — kata-kata yang kosong tanpa angka.
- **Pakai**: "kami pilih Sonnet karena...", "cost kami Rp X/request berdasarkan...", "fallback kami adalah..."

---

## Q&A — Pertanyaan yang Mungkin Muncul

Persiapkan jawaban untuk:

1. Berapa cost per request? Proyeksi bulanan kalau scale ke 10× user?
2. Bagaimana jika model down / API rate limit?
3. Apa fallback ketika model salah?
4. Bagaimana Anda meng-handle PII / data sensitif?
5. Apa bedanya dengan rule-based / search biasa?
6. Bagaimana Anda mengukur sukses di pilot 4 minggu pertama?
7. Bagaimana approach Anda terhadap prompt injection?
8. Skenario mana yang Anda **tidak** target di v1, dan kenapa?

---

## Format File Slide

- Google Slides / PowerPoint / Keynote / Markdown (mis. Marp, Slidev) — bebas.
- Ekspor PDF di akhir sesi untuk arsip Multimatics.
- Sertakan link demo / repo (jika ada) di slide cover atau penutup.
