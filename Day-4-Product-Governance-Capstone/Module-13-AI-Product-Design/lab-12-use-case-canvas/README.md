# Lab 12 — AI Use Case Canvas

**Durasi**: 60 menit (15 menit briefing + 30 menit pengisian + 15 menit pitching)
**Output**: 1 halaman canvas + 5 menit pitching per peserta
**Format**: Individu (canvas) → berpasangan (pitching)

---

## Tujuan

Mengubah ide AI yang masih kabur di kepala menjadi satu halaman canvas yang **bisa dipresentasikan ke decision-maker** dan menjadi kandidat project Capstone.

---

## AI Use Case Canvas

Isi tujuh kolom berikut. Total ±1 halaman A4/A3.

```
┌──────────────────────────────────────────────────────────────────┐
│ JUDUL USE CASE: ______________________________________________   │
│ Diisi oleh: ____________________   Unit kerja: _______________   │
├──────────────────────────────────────────────────────────────────┤
│ 1. PROBLEM                                                       │
│ Apa masalah konkret yang dialami? Siapa yang menderita?          │
│ Berapa frekuensi/volumenya?                                      │
│ Contoh: "Tim CS menerima 800 tiket/hari, 60% pertanyaan FAQ"     │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│ 2. USER                                                          │
│ Primary user (yang berinteraksi langsung):                       │
│ Secondary user (yang terdampak):                                 │
│ Persona singkat (1–2 baris):                                     │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│ 3. BUSINESS VALUE                                                │
│ Penghematan biaya (Rp/bulan) — estimasi order-of-magnitude:      │
│ Peningkatan revenue / NPS / lainnya:                             │
│ Strategic rationale (mengapa sekarang?):                         │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│ 4. AI CAPABILITY NEEDED                                          │
│ Q&A grounded? Classification? Summarization? Agent + tools?      │
│ Variant Claude (Haiku/Sonnet/Opus) yang dipertimbangkan:         │
│ Komponen tambahan (RAG, tool use, memory):                       │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│ 5. DATA SOURCE                                                   │
│ Sumber data (SOP PDF, DB internal, CSV, API):                    │
│ Volume & format:                                                 │
│ Status akses & izin:                                             │
│ Data sensitif (PII, finansial, kesehatan)? Ya / Tidak — apa?     │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│ 6. SUCCESS METRIC                                                │
│ Leading indicator (mis. deflection rate, citation accuracy):     │
│ Lagging indicator (mis. CSAT, cost/request, hours saved):        │
│ Target angka 90 hari:                                            │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│ 7. RISK & MITIGATION                                             │
│ Risiko data (kebocoran PII):                                     │
│ Risiko output (hallucination, bias):                             │
│ Risiko security (prompt injection):                              │
│ Risiko regulasi (UU PDP, sektoral):                              │
│ Mitigasi awal:                                                   │
└──────────────────────────────────────────────────────────────────┘
```

---

## Instruksi Pengisian

1. **Pilih satu use case dari organisasi Anda** yang benar-benar nyata. Hindari ide hipotetis "AI untuk smart city".
2. Isi tujuh kolom secara berurutan, **jangan loncat**. Urutan disusun agar memaksa Anda memvalidasi value sebelum memikirkan teknis.
3. Jika satu kolom kosong/sulit diisi, itu bukan kegagalan — itu sinyal bahwa ada riset/wawancara lanjutan yang dibutuhkan. Tulis "perlu validasi" di kolom tersebut.
4. Estimasi angka boleh kasar (±30%). Tidak ada angka = tidak ada business case.

---

## Aturan Pitching (5 menit/orang)

Berpasangan dengan peserta di sebelah Anda. Bergantian pitching dengan struktur:

| Menit | Konten |
|---|---|
| 0:00–0:30 | Hook: problem statement + dampak |
| 0:30–1:30 | User + business value (angka!) |
| 1:30–3:00 | Solusi AI: capability + data + arsitektur singkat |
| 3:00–4:00 | Success metric + risk utama |
| 4:00–5:00 | Q&A dari peer reviewer |

**Reviewer wajib memberi**:
- 1 hal yang paling kuat dari pitching
- 1 pertanyaan kritis yang belum terjawab
- 1 saran untuk diperbaiki sebelum Capstone

---

## Output Lab 12

- Canvas terisi (foto + simpan digital)
- Catatan feedback peer reviewer
- **Tandai**: apakah canvas ini akan dijadikan kandidat project Capstone? (Ya/Tidak)

---

## Tips

- Hindari godaan menulis "AI agent multi-modal dengan RAG hybrid search + reranker". Mulai dari problem.
- Jika problem Anda bisa diselesaikan dengan SQL query atau spreadsheet, **jangan pakai AI**.
- Risk kolom 7 akan diperdalam di Module 14 — isi seadanya dulu, revisi setelah Module 14.
- Canvas yang baik bisa dibaca oleh manajer non-teknis Anda dalam 2 menit.
