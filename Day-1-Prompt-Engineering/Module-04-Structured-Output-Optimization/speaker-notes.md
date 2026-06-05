# Speaker Notes — Module 4: Structured Output & Optimization

**Total alokasi**: 90 menit
**Mode**: Lecture 40% + demo 20% + Lab 03 in-class 40%

---

## Anekdot Pembuka (3 menit)

> "Tahun lalu saya bantu sebuah tim yang punya prompt ekstraksi kontrak — JSON output. Live di produksi 3 minggu, semua baik. Suatu Senin pagi, parsing pipeline error massal. Penyebab: model upgrade otomatis dari Sonnet 3 ke 3.5, output JSON tiba-tiba diawali markdown ```json. Tidak ada regression test. Itulah pelajaran modul ini: prompt produksi butuh evaluasi seperti kode produksi."

---

## Alokasi Waktu

| Bagian                                | Durasi | Tipe        |
|---------------------------------------|--------|-------------|
| Pembuka + anekdot                     | 3 m    | Cerita      |
| 1. Mengapa structured output          | 5 m    | Lecture     |
| 2. JSON generation best practices     | 12 m   | Lecture + demo prefill |
| 3. Controlled responses               | 6 m    | Lecture     |
| 4. Prompt refinement loop             | 8 m    | Lecture     |
| 5. Prompt testing strategy            | 8 m    | Lecture     |
| 6. Error handling                     | 6 m    | Lecture     |
| 7. Evaluation framework               | 6 m    | Lecture     |
| Demo live invoice extraction v0→v3    | 10 m   | Demo        |
| Walkthrough contoh + Q&A              | 6 m    | Diskusi     |
| **Lab 03 in-class**                   | 30 m   | Lab         |
| Wrap-up + handoff ke Day 2            | (5 m sisa, ke wrap-up Day 1) | — |

Total: 90 menit (Lab 03 dibatasi 30 menit in-class; sisanya dapat diselesaikan setelah sesi atau dilanjut sebagai pre-work Day 2).

> **Catatan jadwal alternatif**: jika fasilitator memilih jadwal pada README (Lab 03 60 menit terpisah), Module 4 fokus penuh ke teori 60 menit, lalu Lab 03 60 menit setelahnya.

---

## Cue Fasilitator per Bagian

### JSON Generation
- **Demo prefill** harus dilakukan di Workbench (claude.ai tidak expose prefill). Tunjukkan beda output dengan dan tanpa prefill `{`.
- Tunjukkan: "instruction `output hanya JSON` saja kadang gagal — preamble masih muncul. Prefill = jaminan struktur."

### Controlled Responses
- Tekankan refusal mode yang **structured** (return JSON error, bukan natural language). Ini agar pipeline downstream tidak crash.

### Refinement Loop
- Pertanyaan: "Berapa kali Anda biasanya iterasi sebelum berhenti?" Bahas anti-pattern: tweak satu kalimat lalu langsung deploy.
- Aturan emas: **satu hipotesis per iterasi**.

### Testing Strategy
- Banyak peserta kaget bahwa prompt butuh test set. Bridge: "kalau Anda commit code, ada unit test. Prompt = code semu, butuh test sebanding."
- Sebutkan tooling: Anthropic Console **Evaluate** tab.

### Error Handling
- Provokasi: "Apa yang terjadi kalau Claude balas natural language di prompt yang seharusnya JSON?" Jawaban: pipeline crash. Solusi: validation layer + retry.

### Evaluation Framework
- Bagikan checklist pre-production. Minta peserta foto / simpan.

---

## Jawaban Kunci untuk Pertanyaan Refleksi

1. **Prefill lebih reliable**: instruksi text masih bisa di-misinterpret (model menambah preamble). Prefill = konstrain mekanik token pertama. Tidak ada negosiasi.
2. **JSON valid vs schema-conformant**: JSON valid = parsable secara sintaks. Schema-conformant = juga match field, tipe, dan constraint. Yang penting di produksi adalah yang kedua.
3. **Test set invoice**: minimum 50 sampel, distribusi mencakup format vendor berbeda, single vs multi-item, dengan/tanpa pajak, mata uang berbeda, edge case (negatif, diskon, bahasa campur).
4. **Drift detection**: monitoring rate of: JSON validity, schema conformance, distribution shift label, mean confidence. Alert jika ada deviasi > threshold.
5. **Validasi prompt vs kode**: prompt = guardrail awal (cheap), kode = ground truth (definitive). Best: keduanya. Prompt menahan obvious error, kode menangkap struktural.

---

## Common Pitfall Peserta

| Pitfall                                                             | Respons fasilitator |
|---------------------------------------------------------------------|---------------------|
| Pakai markdown code fence di output JSON (\`\`\`json)               | Prefill `{` atau rule "JANGAN gunakan code fence". |
| Schema deskripsi terlalu vague ("data invoice")                     | Schema literal dengan tipe & format. |
| Lupa null untuk field optional → output skip field                  | Eksplisit "field tidak ditemukan = null, jangan dihilangkan". |
| Mengubah 5 hal sekaligus saat refinement → tidak tahu apa yang work | Disiplin satu hipotesis per iterasi. |
| Tidak ada test set, evaluasi spontan dari 1-2 sample                | Buat smoke + eval set. |
| Mengandalkan model "tahu" struktur                                  | Selalu show schema + 1-2 contoh. |
| Halusinasi field tambahan ("ekstra_info")                           | Rule eksplisit larang field tambahan. |
| Mengira upgrade model = drop-in replacement                         | Bahas insiden upgrade Sonnet 3→3.5. |

---

## Demo Invoice Extraction — Persiapan

Siapkan teks invoice fiktif sebagai input. Contoh:

```
INVOICE
PT Maju Bersama
Jl. Sudirman No. 10, Jakarta
NPWP: 01.234.567.8-901.000

Invoice No: INV-2024-0312
Tanggal: 15 Maret 2024
Jatuh tempo: 14 April 2024

Kepada:
PT Klien Setia

Items:
1. Konsultasi IT - 40 jam @ Rp 500.000 = Rp 20.000.000
2. Lisensi software - 1 tahun = Rp 12.000.000

Subtotal:  Rp 32.000.000
PPN 11%:   Rp 3.520.000
Total:     Rp 35.520.000
```

Tampilkan output v0 (acak), v1 (struktur ada), v2 (clean JSON), v3 (dengan error handling).

---

## Lab 03 Facilitation

- 30 menit in-class: peserta kerja paralel di laptop.
- Roving fasilitator: bantu peserta yang stuck. Common blocker: peserta lupa wrap input dengan tag, atau schema kurang spesifik.
- 5 menit terakhir: minta 1-2 peserta share screen prompt mereka. Walkthrough rubrik.

---

## Transisi ke Wrap-up Day 1

> "Hari ini Anda berkembang dari 'nge-chat dengan Claude' menjadi 'menulis spec untuk Claude'. Day 2 kita akan mengubah spec ini menjadi kode — API integration, automated evaluation, dan tool use. Bawa pulang: ketiga lab Anda + checklist pre-production. Itu adalah aset Anda."

---

## Material untuk Closing Day 1 (jika fasilitator merangkap closing)

- Recap learning outcomes ke-4 modul (slide ringkas).
- Tanya kelas: 1 hal yang akan langsung saya pakai besok di kantor.
- Distribute pre-read Day 2: Anthropic API quickstart, Pydantic basics.
