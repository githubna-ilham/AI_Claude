# Module 13 — AI Product Design

**Durasi belajar**: 120 menit
**Format**: Baca konsep (50 menit) → Lab 12 praktik mandiri (60 menit) → Latihan & Refleksi (10 menit)
**Prasyarat**: Module 1–12 (foundation LLM, Claude API, agent, RAG)

---

## Apa yang Akan Anda Bisa Setelah Modul Ini

Setelah selesai membaca dan mempraktikkan modul ini, Anda akan mampu:

1. **Menyaring ide AI** menggunakan kerangka *value vs feasibility* sehingga hanya use case bernilai tinggi yang Anda lanjutkan ke tahap prototyping.
2. **Mengisi AI Use Case Canvas** untuk satu permasalahan nyata di organisasi Anda, lengkap dengan success metric dan risk.
3. **Mendesain arsitektur solusi AI** yang menjelaskan komponen: model, prompt layer, memory/RAG, tool, UI, dan observability.
4. **Menyusun AI product roadmap 3 tahap** (Pilot → Scale → Optimize) yang realistis terhadap kapasitas tim Anda.
5. **Mengevaluasi UX khusus AI** (latency, hallucination disclosure, fallback) yang berbeda dari aplikasi deterministik.

---

## Konsep Inti

### 1. AI Use Case Selection: Tidak Semua Masalah Cocok untuk AI

Salah satu kesalahan umum organisasi adalah memaksakan AI ke setiap proses. Berikut filter awal yang dapat Anda gunakan:

| Kriteria | Pertanyaan Kunci | Indikator "Lanjutkan" |
|---|---|---|
| **Value** | Apakah penghematan/peningkatan ≥ 10× biaya pengembangan + ops? | ROI jelas, ada baseline manual |
| **Frequency** | Apakah task dijalankan ratusan kali per hari? | Volume tinggi, repetitif |
| **Tolerance** | Apakah output dengan akurasi 90–95% sudah cukup? | Bukan domain zero-error (misalnya bukan dosis obat) |
| **Data** | Apakah tersedia data berkualitas untuk grounding dan eval? | Minimal 50–200 sampel evaluasi tersedia |
| **Human-in-loop** | Apakah manusia masih dapat me-review keputusan kritis? | Workflow review feasible |

**Anti-pattern**: "Kita ingin menggunakan GPT/Claude untuk apa, ya?" — ini solusi mencari masalah. **Pendekatan yang benar**: "Tim CS kami kewalahan menjawab 800 tiket per hari, di mana 60% pertanyaannya berulang" → ini kandidat use case yang valid.

### 2. Business Value Identification

Gunakan tiga lensa berikut untuk mengartikulasikan value:

- **Cost reduction**: jam yang dihemat × tarif per jam × frekuensi
- **Revenue uplift**: conversion lift, upsell otomatis, retention melalui personalisasi
- **Risk reduction**: deteksi fraud lebih cepat, compliance scanning otomatis

Selalu ekspresikan value dalam **satuan finansial atau metrik bisnis** (NPS, time-to-resolution, throughput) — bukan "AI-powered" sebagai value tersendiri.

### 3. AI Solution Architecture

```mermaid
flowchart TB
    U[User / UI] --> O[Orchestration Layer<br/>prompt + routing]
    O --> M[Claude API<br/>Sonnet/Opus/Haiku]
    O --> R[RAG Layer<br/>Vector DB + Retriever]
    O --> T[Tool Use<br/>API calls, DB, calc]
    M --> G[Guardrails<br/>moderation, PII filter]
    G --> U
    O --> L[Observability<br/>logs, eval, cost]
    R --> D[(Document Store)]
    T --> S[(Backend Systems)]
```

**Komponen wajib pada arsitektur AI production-grade**:

1. **Orchestration** — lapisan yang memutuskan prompt, model, dan tool mana yang dipanggil.
2. **Model layer** — pilih varian sesuai kebutuhan (Haiku untuk klasifikasi cepat, Sonnet untuk reasoning umum, Opus untuk reasoning kompleks).
3. **Retrieval / Memory** — agar jawaban grounded pada data internal Anda.
4. **Tools** — untuk aksi nyata (cek stok, kirim email, query DB).
5. **Guardrails** — input filter (prompt injection), output filter (PII, konten beracun).
6. **Observability** — log prompt, response, latency, cost, dan feedback dari user.

### 4. AI Product Roadmap: Tahap Crawl–Walk–Run

| Tahap | Fokus | Durasi tipikal | Risiko utama |
|---|---|---|---|
| **Pilot** | 1 use case sempit, internal user, evaluasi manual | 4–8 minggu | Over-scoping |
| **Scale** | Multi-tenant, monitoring, integrasi sistem | 2–4 bulan | Cost blow-up |
| **Optimize** | Fine-tune prompt, pemilihan model cerdas, otomasi eval | Continuous | Stagnasi (tidak ada owner) |

Roadmap yang baik selalu menyertakan **kriteria graduasi antar tahap** (misalnya "Pilot lolos ke Scale jika CSAT ≥ 4,2/5 dan biaya ≤ Rp X per request").

### 5. UX untuk Sistem AI

UX untuk AI berbeda dari aplikasi deterministik. Perhatikan beberapa hal berikut:

- **Latency tolerance**: tampilkan streaming/progress, jangan biarkan user "menunggu kotak putih".
- **Hallucination disclosure**: tampilkan source/citation (terutama untuk sistem RAG).
- **Confidence cue**: tunjukkan ketika model tidak yakin ("Saya tidak menemukan dokumen yang relevan, mohon konfirmasi").
- **Graceful fallback**: tombol "eskalasi ke manusia" harus selalu tersedia.
- **Reversibility**: aksi destruktif (kirim email, hapus data) wajib melalui konfirmasi.
- **Feedback loop**: thumbs up/down terintegrasi ke pipeline eval Anda.

---

## Praktik Mandiri: Use Case Canvas Walkthrough

**Skenario**: "Tim HR menghabiskan 4 jam per hari hanya untuk menjawab pertanyaan karyawan seputar kebijakan cuti, BPJS, dan klaim reimbursement."

Mari telusuri tahapan pengisian canvas berikut. Anda dapat menirunya untuk konteks organisasi Anda sendiri.

### Langkah 1 — Tulis Problem Statement (5 menit)

Tuliskan secara spesifik:
> "Karyawan kesulitan menemukan jawaban kebijakan internal, sehingga HR ops kewalahan dan response time rata-rata 18 jam."

### Langkah 2 — Identifikasi User & Business Value (5 menit)

- Primary user: 1.200 karyawan
- Secondary user: 4 staf HR ops
- Value: hemat ~20 jam/minggu × Rp 80rb = Rp 1,6 juta per minggu = ~Rp 80 juta per tahun, sekaligus menaikkan NPS karyawan.

### Langkah 3 — Petakan AI Capability (5 menit)

- **Capability**: Q&A grounded → RAG + Claude Sonnet.
- **Data source**: SK direksi, buku saku karyawan, FAQ existing (PDF, ~300 halaman).
- **Bukan tugas AI**: jangan menghasilkan jawaban tanpa source.

### Langkah 4 — Definisikan Success Metric (5 menit)

- Deflection rate ≥ 50% pertanyaan tier-1
- Citation accuracy ≥ 95%
- CSAT ≥ 4/5
- Cost per query ≤ Rp 200

### Langkah 5 — Risk Identification (5 menit)

- Risiko: bocornya data gaji jika RAG tidak ber-permission.
- Mitigasi: filter dokumen confidential, audit log per query.

Setelah lima langkah ini selesai, canvas Anda sudah memiliki gambaran utuh dari problem hingga mitigasi risiko. Selanjutnya, gunakan template canvas yang sama untuk konteks organisasi Anda di Lab 12.

---

## Contoh Konkret: AI Product Roadmap

### Contoh 1 — Bank Retail: AI Loan Assistant

| Tahap | Cakupan | Metrik graduasi |
|---|---|---|
| Pilot (8 minggu) | 1 cabang Jakarta, KTA saja, 3 RM internal user, Claude Sonnet + RAG dari product sheet | Approval cycle turun 30%, RM CSAT ≥ 4 |
| Scale (4 bulan) | 25 cabang, tambah KPR + Kartu Kredit, integrasi tool SLIK API | Volume 5.000 sesi/bulan, cost ≤ Rp 500/sesi |
| Optimize (6+ bulan) | Auto-routing Haiku untuk FAQ + Sonnet untuk simulasi, eval otomatis 200 prompt/minggu | Cost turun 40%, hallucination rate < 1% |

### Contoh 2 — E-commerce: AI Customer Service Agent

| Tahap | Cakupan | Metrik graduasi |
|---|---|---|
| Pilot (6 minggu) | Tracking + return policy, channel web chat saja, fallback ke human 100% | Deflection 30%, NPS netral |
| Scale (3 bulan) | + Refund tool use, WhatsApp + Instagram DM, multi-bahasa ID/EN | Deflection 55%, AHT turun 40% |
| Optimize (ongoing) | + Recommendation upsell, A/B prompt tuning, eval otomatis transcript | Upsell revenue +8%, cost per chat ≤ Rp 300 |

---

## Hands-on Lab

**Lab 12 — AI Use Case Canvas**
Folder: `./lab-12-use-case-canvas/`

Anda akan mengisi canvas 7-kolom untuk use case dari organisasi Anda sendiri, lalu melakukan **pitching 5 menit** kepada peer reviewer (round-robin antar 2 peserta). Output canvas akan Anda bawa ke sesi Capstone sebagai kandidat project.

---

## Latihan & Refleksi

Untuk memantapkan pemahaman, coba jawab lima pertanyaan refleksi berikut sebelum melanjutkan ke Module 14. Anda dapat menuliskan jawaban di buku catatan atau mendiskusikannya dengan rekan satu tim:

1. Mengapa "AI-powered" bukan merupakan value proposition yang valid di mata seorang CFO?
2. Apa perbedaan kunci antara fase Pilot dan Scale yang sering disepelekan oleh tim AI?
3. Mengapa Haiku, Sonnet, dan Opus tidak saling menggantikan — kapan masing-masing sebaiknya Anda pakai?
4. Bagaimana cara mendeteksi bahwa sebuah use case **tidak cocok** untuk LLM dan lebih baik menggunakan pendekatan rule-based?
5. UX cue apa yang akan Anda tambahkan pada chatbot RAG agar user tidak salah menganggap output sebagai fakta absolut?

---

## Bacaan Lanjutan

- Anthropic — *Building Effective Agents* (engineering.anthropic.com)
- Andrew Ng — *AI Transformation Playbook*
- Google — *People + AI Guidebook* (pair.withgoogle.com)
- HBR — *How to Choose Your First AI Project* (2019, masih sangat relevan)
- Anthropic *Claude model card* untuk panduan pemilihan varian
- OWASP LLM Top 10 (untuk konteks risiko, akan dibahas pada Module 14)
- EU AI Act overview — bagian Annex III (high-risk system) untuk peta regulasi
