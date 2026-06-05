# Speaker Notes — Module 11: Retrieval Augmented Generation (RAG)

**Durasi total**: 120 menit
**Format**: 60' materi + 60' lab 09 & 10 (paralel/sekuensial)

---

## Alokasi Waktu

| Menit | Segmen | Aktivitas |
|-------|--------|-----------|
| 0–5 | Pembuka | Mengapa RAG, transisi dari Module 10 |
| 5–20 | Konsep 1.1–1.3 | Definisi + arsitektur + embedding fundamental |
| 20–35 | Konsep 1.4–1.6 | Vector DB, chunking, metadata |
| 35–50 | Demo live | Ingest 3 dokumen, query interaktif |
| 50–60 | Konsep 1.7–1.8 | Augmented prompt + anti-pola + Q&A |
| 60–105 | Lab 09 + 10 | Coaching |
| 105–120 | Recap | Showcase 1-2 peserta, transisi ke Module 12 |

---

## Cue Fasilitator

### Pembuka

"Module 10 sudah memberi Claude tubuh (app). Module 11 memberi Claude **memori panjang** yang spesifik perusahaan Anda."

Tanya audiens: **"Siapa pernah dengar bot AI mengarang kebijakan perusahaan? Itu hallucination karena tidak ada grounding. RAG adalah jawabannya."**

### Konsep arsitektur

- Diagram mermaid: tekankan **dua pipeline berbeda**. Ingestion bisa batch nightly; query harus <2 detik.
- **Embedding consistency**: pertanyaan paling sering dari peserta. Tegaskan **"satu model untuk semua, satu corpus untuk satu model"**.

### Embedding fundamental

- Gunakan analogi: embedding seperti GPS koordinat untuk arti. "Mobil" dekat dengan "kendaraan", jauh dari "apel".
- Demo cepat di Python: hitung cosine similarity 3 kata.
- Anekdot: tim yang pakai embedding English-only untuk korpus Bahasa Indonesia → retrieval acak → "kenapa modelnya bodoh?" Bukan modelnya, embedding-nya salah.

### Vector DB

- Tabel pilihan: tekankan **default Chroma** untuk hari ini agar tidak buang waktu setup. Production discussion akan dibahas Day 4.
- Jika ada peserta DBA, sebut pgvector dengan index HNSW + tuning `m` dan `ef_construction`.

### Chunking

- Demo "before vs after": chunk per kalimat vs chunk 500 token. Tunjukkan retrieval untuk pertanyaan yang sama.
- **Common pitfall**: peserta tergoda chunking sangat kecil ("biar presisi"). Tunjukkan justru retrieval miss.

### Metadata

- Tekankan: **metadata = future-proofing**. Tanpa metadata, RAG = blackbox.

### Demo live (35–50')

- Buka notebook/script.
- Ingest 3 dokumen HR sample (kebijakan_cuti.pdf, sop_pengadaan.docx, faq.csv).
- Jalankan query: "Berapa hari cuti tahunan?" → tampilkan top-5 + skor.
- Jalankan query "out of scope": "Resep rendang?" → tunjukkan retrieval skor rendah, model menjawab "tidak ditemukan".
- Pitfall yang sengaja didemo: lupa set `input_type="query"` di Voyage → retrieval menurun. Fix di depan peserta.

### Anti-pola (50–60')

- Bahas "evaluation": jangan judge RAG hanya dari "kelihatan oke". Bangun golden set 30 Q&A → ukur retrieval recall@k dan answer faithfulness.

### Lab 09 + 10

- Bagi peserta ke 2 jalur: **Lab 09 dulu** (mandatory), **Lab 10 paralel** untuk yang lebih cepat (advanced track).
- Checkpoint menit 30 lab: semua peserta sudah berhasil ingest 1 dokumen.
- Checkpoint menit 50 lab: query berhasil mengembalikan jawaban dengan sitasi.

---

## Jawaban Kunci Q&A

1. **Long-context vs RAG** — Long-context untuk dokumen ≤200K token, query satu kali, tidak sering update. RAG saat ada banyak dokumen, sering update, butuh sitasi presisi, multi-user.
2. **Ganti embedding model** — Harus re-embed seluruh corpus. Tidak bisa partial. Maintenance window perlu. Mitigasi: versi collection (mis. `docs_v1_voyage3`, `docs_v2_voyage3.5`).
3. **Evaluasi RAG** — Dua level: (a) **Retrieval**: recall@k, precision@k, MRR pada golden set. (b) **Generation**: faithfulness (apakah jawaban di-support context), answer relevance. Tools: Ragas, custom LLM-as-judge.
4. **Metadata & ACL** — Filter retrieval per user role (`where={"confidentiality": {"$in": user.roles}}`). Hindari "retrieve all, filter at LLM" — bocor di prompt.
5. **No-answer handling** — System prompt eksplisit: "Jika tidak ada di konteks, katakan tidak tahu." Threshold similarity: jika skor top-1 < 0.5, return "tidak ditemukan".

---

## Common Pitfalls

- **Embedding inconsistency** ingestion vs query (model atau `input_type`).
- **Chunk tanpa header context** → model tidak tahu chunk dari dokumen mana.
- **k terlalu besar** → biaya naik, noise naik.
- **Tidak ada deduplication** chunk → top-k berisi konten serupa.
- **Tidak ada filter metadata** → bocor data antar departemen.
- **Index tidak di-build** di pgvector → query lambat.

---

## Anekdot

- Bank yang RAG-kan policy 5GB PDF → tagihan embedding sekali $1200, lupa caching. Pelajaran: hitung dulu.
- Tim legal yang minta sitasi dengan halaman + paragraf → tanpa metadata page, mustahil. Pelajaran: metadata sejak hari pertama.
- Startup yang ganti embedding "biar lebih baru" tanpa re-embed → retrieval rusak total selama seminggu.

---

## Hand-off ke Module 12

"Sekarang chat + RAG sudah jalan. Module 12 menggabungkan keduanya jadi Enterprise AI Assistant dengan tool use, plus pertimbangan production: cost, scaling, observability."
