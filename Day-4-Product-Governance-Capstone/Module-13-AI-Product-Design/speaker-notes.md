# Speaker Notes — Module 13 (AI Product Design)

**Total**: 120 menit. Toleransi geser ±5 menit per segmen.

---

## Segmen 1 — Pembuka (0:00 – 0:10, 10 menit)

**Cue**: Tampilkan slide pembuka "AI Product Design", buka dengan pertanyaan provokatif.

**Pertanyaan pembuka**:
> "Berapa banyak proyek AI di kantor Anda yang mati di POC?"

Biasanya 70–80% peserta mengangkat tangan. Gunakan momentum ini untuk masuk ke pesan utama:
> "Modul ini bukan tentang model. Ini tentang memastikan use case Anda tidak masuk ke pemakaman POC."

**Anekdot**: Cerita singkat klien yang membakar Rp 2 miliar untuk RAG internal yang tidak pernah dipakai user — karena tidak melibatkan user di tahap discovery. Jangan sebut nama klien, cukup industri ("salah satu BUMN energi").

**Common pitfall**: Peserta technical sering skeptis dengan modul "product". Tekankan: 3 hari kemarin Anda belajar *how*, hari ini belajar *what & why*. Tanpa itu, skill teknis tidak ter-monetize.

---

## Segmen 2 — Use Case Selection (0:10 – 0:30, 20 menit)

**Cue**: Slide framework Value × Feasibility 2×2.

**Alokasi**:
- 10 menit penjelasan kriteria
- 10 menit aktivitas cepat: minta tiap peserta menulis 3 ide AI di unit kerjanya, plot di kuadran

**Jawaban kunci untuk pertanyaan sering muncul**:

*"Bagaimana kalau bos saya yang nyuruh pakai AI padahal tidak cocok?"*
> "Tunjukkan tabel kriteria. Bukan menolak — tapi reframe: 'Use case A tidak cocok untuk LLM, tapi use case B dengan profil mirip cocok'. Selalu tawarkan alternatif."

*"Bagaimana kalau data tidak tersedia?"*
> "Jangan mulai dengan AI. Mulai dengan data pipeline 4 minggu, baru AI 4 minggu berikutnya. Honest scoping > overpromise."

**Common pitfall**: Peserta over-focus ke aspek teknis ("modelnya mau pakai apa?") padahal belum jelas value. Tahan diskusi model sampai segmen 4.

---

## Segmen 3 — Business Value & Metric (0:30 – 0:45, 15 menit)

**Cue**: Tampilkan template "value calculation worksheet" sederhana di slide.

**Latihan singkat (5 menit)**: Hitung bersama:
> CS team 12 orang × 2 jam/hari menangani FAQ × 20 hari × Rp 60rb/jam = Rp 28.8jt/bulan potensi penghematan.

Tekankan bahwa angka kasar lebih baik daripada tidak ada angka.

**Anekdot**: PM yang mempresentasikan AI initiative tanpa angka selalu kalah dari PM yang membawa estimasi (meskipun ±30%).

**Common pitfall**: Peserta technical alergi angka. Yakinkan: cukup estimasi order-of-magnitude — ini bukan IRR audit BPK.

---

## Segmen 4 — Solution Architecture (0:45 – 1:05, 20 menit)

**Cue**: Diagram arsitektur di mermaid. Gambar ulang manual di whiteboard sambil bicara — peserta lebih ingat ketika tergambar live.

**Alokasi waktu**:
- 12 menit walkthrough komponen
- 8 menit diskusi pemilihan model variant (Haiku/Sonnet/Opus)

**Jawaban kunci**:

*"Kapan pakai Haiku vs Sonnet vs Opus?"*
> "Aturan praktis: classification, routing, ekstraksi sederhana → Haiku. Reasoning umum, RAG, agent → Sonnet. Reasoning kompleks multi-step, drafting strategis → Opus. Production yang dewasa biasanya *mix*: Haiku gateway → Sonnet/Opus untuk yang lolos filter."

*"Vector DB pilih apa?"*
> "Untuk pilot: pgvector cukup. Untuk scale: Qdrant, Weaviate, atau Pinecone. Jangan mulai dengan yang termahal."

**Common pitfall**: Lupa observability. Tekankan: tanpa logging prompt+response+cost+feedback, Anda tidak punya basis untuk iterasi.

---

## Segmen 5 — Roadmap & UX (1:05 – 1:25, 20 menit)

**Cue**: Slide Crawl-Walk-Run dengan kriteria graduasi.

**Anekdot UX**: Cerita ChatGPT awal yang tidak punya "stop button" dan user frustrasi. Sekarang streaming + stop adalah standar.

**Diskusi cepat**: Minta 2–3 peserta menyebutkan satu UX cue AI yang mereka temui terakhir kali — sukses atau gagal.

**Common pitfall**: Roadmap diisi fitur, bukan kriteria graduasi. Tekankan: kriteria graduasi = kontrak antar fase.

---

## Segmen 6 — Demo Live: Use Case Canvas (1:25 – 1:50, 25 menit)

**Cue**: Ambil contoh HR Knowledge Assistant. Isi canvas live di flipchart/Miro.

**Skenario fasilitator**:
1. Tunjuk 1 peserta yang dari HR/People Ops (kalau ada). Wawancara singkat 2 menit untuk grounding.
2. Tulis problem statement di flipchart.
3. Isi kolom demi kolom sambil meminta input peserta.
4. Sengaja tinggalkan kolom "Risk" untuk diisi peserta — ini menjadi jembatan ke Module 14.

**Anekdot**: "Canvas ini bukan dokumen. Ini *alat berpikir*. Anda akan revisi 3–5 kali sebelum production."

**Common pitfall**: Demo terlalu didikte fasilitator. Buat 50% input dari peserta agar mereka merasa memiliki.

---

## Segmen 7 — Lab 12 Briefing + Wrap-up (1:50 – 2:00, 10 menit)

**Cue**: Buka folder `lab-12-use-case-canvas/README.md` di proyektor.

**Instruksi**:
- Tiap peserta mengisi 1 canvas untuk use case organisasi mereka (15 menit)
- Lalu pitching 5 menit ke peer di sebelahnya (round-robin 2 ronde = 10 menit)
- Output canvas akan dipakai di sesi Capstone sebagai kandidat

**Tutup dengan**: "Module 14 berikutnya akan menambahkan satu kolom yang sering hilang: governance & risk. Setelah itu Anda siap merancang Capstone."

---

## Catatan Tambahan

- Jika kelas didominasi developer, perpanjang segmen 4 (architecture) hingga 25 menit.
- Jika kelas didominasi PM/business, perpanjang segmen 3 (value) hingga 20 menit, persingkat segmen 4 jadi 15 menit.
- Siapkan 2–3 contoh canvas pre-filled untuk industri berbeda (banking, e-commerce, manufacturing) sebagai referensi peserta.
