# Rubrik Penilaian Capstone

**Total skor**: 100 poin (bobot kategori sebagai berikut)
**Penilai**: 2–3 juri (fasilitator + tamu)
**Skor akhir**: rata-rata juri per kategori → dijumlahkan dengan bobot.

---

## Bobot Kriteria

| Kriteria | Bobot | Fokus |
|---|---|---|
| 1. Use Case Clarity & Business Value | 25% | Apakah problem nyata & value jelas? |
| 2. Technical Implementation | 30% | Apakah prototype bekerja & arsitektur sehat? |
| 3. Prompt Engineering Quality | 20% | Apakah prompt design profesional? |
| 4. Demo & Presentation | 15% | Apakah pitching meyakinkan? |
| 5. Governance & Safety Awareness | 10% | Apakah tim sadar risiko & mitigasi? |
| **Total** | **100%** | — |

---

## Level Deskriptor

Tiap kategori dinilai pada salah satu level berikut, dengan poin sesuai bobot.

| Level | Rentang | Karakter umum |
|---|---|---|
| **Excellent** | 90–100% dari bobot | Setara standar profesional; siap pilot di organisasi |
| **Good** | 75–89% dari bobot | Solid, ada area minor untuk diperbaiki |
| **Adequate** | 60–74% dari bobot | Memenuhi requirement minimum |
| **Needs Improvement** | < 60% dari bobot | Ada gap signifikan |

---

## Detail per Kategori

### 1. Use Case Clarity & Business Value (25 poin)

| Level | Poin | Deskriptor |
|---|---|---|
| Excellent | 23–25 | Problem nyata, terbukti volume/dampak; user persona spesifik; angka business value plausible dengan asumsi yang dijelaskan; strategic fit jelas. |
| Good | 19–22 | Problem jelas dan masuk akal; ada angka value walau kasar; user teridentifikasi. |
| Adequate | 15–18 | Problem teridentifikasi tapi argumen value masih lemah / kualitatif. |
| Needs Improvement | < 15 | Solution-first thinking; problem tidak jelas; tidak ada angka. |

### 2. Technical Implementation (30 poin)

| Level | Poin | Deskriptor |
|---|---|---|
| Excellent | 27–30 | Prototype berjalan mulus end-to-end; arsitektur jelas dan tepat; integrasi Claude API + (Agent dan RAG) keduanya; error handling + observability terlihat. |
| Good | 23–26 | Prototype berjalan untuk happy path; arsitektur jelas; minimal 1 dari Agent / RAG terimplementasi baik. |
| Adequate | 18–22 | Prototype jalan dengan beberapa kekurangan; arsitektur dasar; integrasi Claude API ada. |
| Needs Improvement | < 18 | Demo tidak berjalan / banyak error; arsitektur tidak jelas. |

### 3. Prompt Engineering Quality (20 poin)

| Level | Poin | Deskriptor |
|---|---|---|
| Excellent | 18–20 | Prompt menggunakan struktur jelas (role + context + constraint + format + delimiter/XML); few-shot bila perlu; ada bukti iterasi (sebelum vs sesudah); robust terhadap input aneh. |
| Good | 15–17 | Prompt terstruktur dan jelas; ada beberapa teknik prompt engineering yang diterapkan. |
| Adequate | 12–14 | Prompt fungsional tapi sederhana; tidak ada bukti iterasi. |
| Needs Improvement | < 12 | Prompt ad-hoc; tidak ada struktur; rentan misinterpretasi. |

### 4. Demo & Presentation (15 poin)

| Level | Poin | Deskriptor |
|---|---|---|
| Excellent | 14–15 | Pitching persuasif, terstruktur, time-managed; live demo lancar; semua anggota berbicara; menjawab Q&A dengan baik. |
| Good | 11–13 | Pitching jelas, demo berjalan, ada minor stumble; Q&A tertangani sebagian besar. |
| Adequate | 9–10 | Pitching cukup; demo jalan tapi kurang impresif; Q&A jawaban lemah. |
| Needs Improvement | < 9 | Pitching tidak terstruktur; demo gagal; Q&A defensive/tidak menjawab. |

### 5. Governance & Safety Awareness (10 poin)

| Level | Poin | Deskriptor |
|---|---|---|
| Excellent | 9–10 | Minimal 5 item checklist dibahas dengan substansi; menyebut UU PDP / OWASP LLM Top 10 secara relevan; ada implementasi mitigasi nyata (PII redaction, prompt hardening, logging). |
| Good | 7–8 | Beberapa risiko dibahas; minimal 1 mitigasi diimplementasi. |
| Adequate | 6 | Menyebut governance sambil lalu; tidak ada implementasi. |
| Needs Improvement | < 6 | Tidak menyentuh governance / safety. |

---

## Lembar Penilaian (Juri)

| Kategori | Skor (poin) | Catatan |
|---|---|---|
| 1. Use Case Clarity & Business Value (/25) | | |
| 2. Technical Implementation (/30) | | |
| 3. Prompt Engineering Quality (/20) | | |
| 4. Demo & Presentation (/15) | | |
| 5. Governance & Safety Awareness (/10) | | |
| **Total (/100)** | | |
| Highlight tim (1 hal terkuat) | | |
| Saran perbaikan (1 hal prioritas) | | |

---

## Klasifikasi Akhir Tim

| Total | Predikat |
|---|---|
| 90–100 | Excellent — siap dilanjutkan ke pilot real |
| 75–89 | Good — fondasi kuat, butuh hardening sebelum pilot |
| 60–74 | Adequate — perlu iterasi sebelum produksi |
| < 60 | Needs Improvement — gunakan sebagai pembelajaran |

---

## Catatan Juri

- Berikan **feedback tertulis** minimal 2 kalimat per tim (1 strength + 1 improvement).
- Jika ada gap besar antar juri (> 15 poin), kalibrasi 5 menit sebelum mengumumkan.
- Hindari penalisasi karena scope kecil — scope yang selesai > scope ambisius yang tidak selesai.
- Apresiasi tim yang menampilkan **failure case** dengan jujur dan **trade-off thinking** — ini ciri tim matang.

---

## Penghargaan (Opsional)

Fasilitator dapat menambahkan kategori penghargaan non-kompetitif:

- **Best Business Case**
- **Best Technical Implementation**
- **Best Prompt Engineering**
- **Best Governance Awareness**
- **People's Choice** (voting peserta)

Tujuan: setiap tim merasa dihargai pada area kekuatannya.
