# Panduan Capstone — Day 4

**Total slot**: 360 menit (180 menit eksekusi + 180 menit presentasi)
**Format tim**: 3–4 orang per tim, 5–6 tim per kelas
**Output**: Use case canvas + working prototype demo + slide presentasi (+ GitHub repo opsional)

---

## Brief

Anda telah belajar prompt engineering (Day 1), Claude API & tool use (Day 2), agent & RAG (Day 3), dan product design + governance (Day 4 pagi). **Sekarang waktunya menjahit semuanya menjadi satu prototype yang bisa Anda bawa pulang dan presentasikan ke atasan/stakeholder Anda Senin depan.**

Capstone bukan ujian akademis. Ini adalah **simulasi pitching internal**: tim juri (fasilitator + tamu) akan menilai sebagaimana Head of Data/CTO menilai proposal AI di organisasi nyata.

---

## Aturan Tim

- 3–4 orang per tim. Sebaiknya **mix profil** (developer + PM + analyst) — refleksi tim AI di dunia nyata.
- Setiap tim memilih satu **Project Lead** (yang akan moderasi presentasi).
- Setiap tim memilih satu **Tech Lead** (yang akan mendemo).
- Diversifikasi role internal: prompt engineer, RAG/agent engineer, governance reviewer, slide owner.
- Tim memilih 1 dari 6 opsi project di `opsi-project.md` (atau usul kustom dengan persetujuan fasilitator).

---

## Timeline Detail

| Slot | Durasi | Aktivitas | Output |
|---|---|---|---|
| 1 | 30 menit | **Planning**: pilih project, breakdown task, definisikan minimum demo path | Project plan 1 halaman |
| 2 | 150 menit | **Eksekusi**: build prototype + isi canvas + draft slide | Working demo + 7–9 slide |
| Break | 15 menit | Coffee + setup demo | — |
| 3 | 180 menit | **Presentasi**: 6 tim × 25 menit (15 menit pitch + demo + 10 menit Q&A) | Pitch + Q&A |
| 4 | (overlap) | Penilaian juri + closing | Pemenang + feedback |

> Jika hanya 5 tim, perpanjang Q&A jadi 12–15 menit per tim.
> Jika 7 tim, kompres jadi 22 menit per tim dengan disiplin keras.

---

## Deliverable Wajib

1. **AI Use Case Canvas terisi** (boleh memakai canvas dari Lab 12 atau membuat baru untuk project tim)
2. **Working prototype** yang bisa di-demo live (minimal happy path berjalan)
3. **Slide presentasi 7–9 slide** sesuai `template-presentasi.md`
4. **Daftar mitigasi governance** minimal 5 item dari `checklist-responsible-AI.md`

## Deliverable Opsional (Bonus Score)

- GitHub repo public/private dengan README jelas
- Recording demo (video 1–2 menit)
- Cost estimation per request dan proyeksi bulanan
- Diagram arsitektur (mermaid / drawio)

---

## Kebutuhan Teknis Minimal

Tim wajib menggunakan minimum:

- **Prompt engineering** (system + user prompt yang terstruktur, dengan tag/delimiter)
- **Claude API** (model bebas — Haiku/Sonnet/Opus sesuai kebutuhan)
- **Minimal salah satu**: Tool use (agent) **atau** RAG (retrieval over dokumen)

Tim bintang menggunakan **keduanya** (agent + RAG).

---

## Penilaian

Lihat `rubrik-penilaian.md`. Bobot:

| Kriteria | Bobot |
|---|---|
| Use Case Clarity & Business Value | 25% |
| Technical Implementation | 30% |
| Prompt Engineering Quality | 20% |
| Demo & Presentation | 15% |
| Governance & Safety Awareness | 10% |

Juri akan mengisi rubrik tertulis untuk feedback pasca-presentasi.

---

## Aturan Demo

- **Live demo wajib**. Slide screenshot diizinkan hanya sebagai backup jika ada kendala koneksi.
- **Tunjukkan minimal 1 prompt aktual** yang tim gunakan (paste di slide atau buka di editor).
- **Tunjukkan minimal 1 contoh failure case** dan bagaimana ditangani — ini menunjukkan kematangan tim.
- **Estimasi cost** disebutkan walau kasar.
- **Disclosure governance**: minimal sebutkan 1 risiko yang tim sadari + mitigasi yang sudah/akan dilakukan.

---

## Tips Sukses

1. **Pilih scope kecil yang selesai > scope besar yang setengah jadi.** Demo 1 happy path yang mulus mengalahkan 5 fitur yang error.
2. **Bagi peran sejak menit pertama.** Hindari semua orang di laptop yang sama.
3. **Siapkan data dummy realistis.** "Customer X menanyakan status order #123" lebih persuasif daripada "test 1 2 3".
4. **Latih pitching 1× sebelum naik panggung.** 15 menit terlihat panjang sampai Anda mulai.
5. **Antisipasi pertanyaan juri**: cost? scaling? governance? failure mode? ROI?
6. **Jangan sembunyikan kelemahan.** Juri menghargai tim yang sadar limitasi prototype dan punya roadmap perbaikan.

---

## Pasca-Pelatihan

Prototype Anda adalah **artefak portfolio**. Setelah pelatihan:

- Bawa deck + demo ke 1-on-1 dengan atasan minggu depan.
- Gunakan canvas + governance checklist sebagai lampiran proposal.
- Jika diberi green light, gunakan struktur roadmap Crawl–Walk–Run dari Module 13.

Multimatics menyarankan follow-up coaching session 2–4 minggu pasca-pelatihan untuk tim yang serius melanjutkan ke pilot.

---

## Aturan Fair Play

- Boleh menggunakan kode dari Lab Day 1–3 sebagai starter.
- Boleh menggunakan library open source.
- **Tidak boleh** menampilkan demo yang sebenarnya hasil pekerjaan pre-pelatihan (rubrik menilai pekerjaan tim hari ini).
- Boleh memakai data dummy / synthetic — **jangan** memakai data internal organisasi yang sensitif/confidential di environment training.
