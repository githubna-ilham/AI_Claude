# Lab 03 — JSON Output & Evaluation (Invoice Parser)

**Modul**: Module 4 — Structured Output & Optimization
**Durasi**: 60 menit (atau 30 menit in-class + 30 menit pasca-sesi)
**Mode**: Individual; share results di akhir.
**Tools**: Anthropic Console — Workbench (disarankan untuk prefill & `temperature=0`) atau claude.ai.
**Output**: prompt v3 final + tabel hasil evaluasi 5 invoice + skor rubrik.

---

## Tujuan

Peserta mampu:
1. Mendesain prompt yang menghasilkan JSON valid sesuai schema spesifik untuk use case parsing invoice.
2. Iterasi prompt secara bukti-based (smoke set 3 → eval set 5).
3. Menerapkan rubrik evaluasi: JSON validity, schema conformance, accuracy.
4. Menangani edge case (data missing, total tidak konsisten) di level prompt.

---

## Prasyarat

- Telah mengikuti Module 4 (materi + demo).
- Akun Console Anthropic (disarankan, supaya bisa prefill). Jika tidak ada, claude.ai dengan model Sonnet cukup.
- Editor + JSON validator (mis. https://jsonlint.com/ atau extension VSCode).

---

## Schema Target

```json
{
  "vendor": {
    "name": "string",
    "address": "string | null",
    "tax_id": "string | null"
  },
  "invoice_number": "string",
  "invoice_date": "string (YYYY-MM-DD)",
  "due_date": "string (YYYY-MM-DD) | null",
  "currency": "string (ISO 4217, default IDR)",
  "customer_name": "string | null",
  "line_items": [
    {
      "description": "string",
      "quantity": "number",
      "unit_price": "number",
      "amount": "number"
    }
  ],
  "subtotal": "number",
  "tax": "number",
  "total": "number",
  "data_consistency_check": {
    "computed_total": "number",
    "matches_reported_total": "boolean"
  }
}
```

---

## Dataset (5 Invoice Sampel)

### Invoice 1 — Standard

```
INVOICE
PT Maju Bersama
Jl. Sudirman No. 10, Jakarta
NPWP: 01.234.567.8-901.000

Invoice No: INV-2024-0312
Tanggal: 15 Maret 2024
Jatuh tempo: 14 April 2024
Kepada: PT Klien Setia

Items:
1. Konsultasi IT - 40 jam @ Rp 500.000 = Rp 20.000.000
2. Lisensi software 1 tahun = Rp 12.000.000

Subtotal: Rp 32.000.000
PPN 11%:  Rp 3.520.000
Total:    Rp 35.520.000
```

### Invoice 2 — Tanpa due_date & tax_id

```
TAGIHAN
CV Sumber Rejeki
invoice no 0042/SR/V/2024
tgl 02-05-2024

cust: Toko Abadi

1x Beras premium 25kg  Rp 350.000
2x Minyak goreng 5L    Rp 180.000 (per item)
Total: Rp 710.000
```

### Invoice 3 — Mata uang USD

```
INVOICE
Acme Cloud Services Inc.
Tax ID: US-12-3456789
123 Tech Plaza, San Francisco

Invoice #: ACS-99812
Issue: 2024-06-01
Due:    2024-06-30
Bill to: Nusantara Tech

Description                Qty  Unit    Amount
SaaS subscription (mo)      1   $499    $499.00
Premium support             1   $150    $150.00

Subtotal:  $649.00
Tax (8%):  $51.92
Total:     $700.92
```

### Invoice 4 — Inconsistent Total (sengaja salah)

```
INVOICE
UD Berkah Jaya
Inv: BJ/0017/2024
Tgl: 20 April 2024

- Semen 10 sak @ 75.000 = 750.000
- Cat tembok 5 galon @ 120.000 = 600.000

Subtotal: 1.350.000
PPN: 0
Total: 1.500.000     <- ANGKA SALAH (seharusnya 1.350.000)
```

### Invoice 5 — Minimal info / ambigu

```
nota
warung sembako bu yati
3 mei
beras 5kg 75rb
gula 2kg 30rb
telur 1kg 28rb
total 133rb
```

---

## Langkah

### Langkah 1 — Setup (5 menit)

- Buka Workbench / claude.ai.
- Jika Workbench: pilih Sonnet 4.x, `temperature=0`.
- Siapkan editor untuk menyimpan prompt v1, v2, v3.
- Siapkan JSON validator di tab terpisah.

### Langkah 2 — Tulis Prompt v1 (10 menit)

Tulis prompt awal berdasarkan template Module 4:

```text
<task>...</task>
<schema>...</schema>
<rules>...</rules>
<text>{invoice}</text>
```

Jalankan untuk Invoice 1. Validasi JSON. Catat issue (mis. preamble, field missing, format tanggal salah).

### Langkah 3 — Iterasi ke v2 (10 menit)

Hipotesis perbaikan (pilih SATU per iterasi):
- Tambah prefill `{`.
- Tambah contoh few-shot.
- Lebih spesifik format tanggal (`YYYY-MM-DD` dari `15 Maret 2024`).
- Tambah rule "jangan tambah preamble".

Jalankan ulang untuk Invoice 1 + Invoice 2. Validasi.

### Langkah 4 — Iterasi ke v3 (15 menit)

Tangani edge case:
- Invoice 3: mata uang USD → currency = "USD".
- Invoice 4: total tidak konsisten → `data_consistency_check.matches_reported_total = false`.
- Invoice 5: format minimal & ambigu → tetap parse atau return error JSON.

Jalankan v3 untuk **semua 5 invoice**. Simpan output JSON.

### Langkah 5 — Evaluasi (15 menit)

Isi tabel evaluasi:

| Invoice | JSON valid? | Schema conformant? | Vendor benar? | Date benar? | Currency benar? | Line items lengkap? | Total benar? | Consistency check benar? | Skor (0-7) |
|---------|-------------|--------------------|---------------|-------------|-----------------|---------------------|--------------|--------------------------|------------|
| 1       |             |                    |               |             |                 |                     |              |                          |            |
| 2       |             |                    |               |             |                 |                     |              |                          |            |
| 3       |             |                    |               |             |                 |                     |              |                          |            |
| 4       |             |                    |               |             |                 |                     |              |                          |            |
| 5       |             |                    |               |             |                 |                     |              |                          |            |

Setiap kolom kriteria: 1 jika lulus, 0 jika gagal. Maks 7 poin per invoice.

### Langkah 6 — Refleksi (5 menit)

Tulis 3 bullet:
- Iterasi mana yang memberi gain terbesar?
- Edge case mana yang paling sulit ditangani?
- Apa yang akan Anda tambahkan ke prompt untuk produksi (mis. retry rule, schema versioning)?

---

## Rubrik Evaluasi Lab

### A. Validitas JSON (1 poin × 5 invoice = 5 poin)
Output dapat di-parse oleh JSON parser standar. Tidak ada preamble, tidak ada code fence, tidak ada trailing text.

### B. Schema Conformance (1 poin × 5 invoice = 5 poin)
Setiap field di schema hadir (atau null), tipe data sesuai, format tanggal `YYYY-MM-DD`, currency ISO 4217.

### C. Kelengkapan Field (8 poin)
- Vendor lengkap untuk invoice yang menyediakan info (Inv 1, 2, 3, 4): 4 poin
- Line items lengkap (qty, unit_price, amount) untuk semua: 4 poin

### D. Akurasi Numerik (5 poin)
Total, subtotal, tax, unit price benar dan tanpa simbol mata uang.

### E. Edge Case Handling (7 poin)
- Invoice 3 currency = "USD": 2 poin
- Invoice 4 consistency_check.matches_reported_total = false: 3 poin
- Invoice 5 ditangani (parsed atau structured error): 2 poin

**Total maks: 30 poin.** Target lulus: 20+. Target stretch: 26+.

---

## Kriteria Selesai

- [ ] Prompt v1, v2, v3 tersimpan dengan changelog perubahan per versi.
- [ ] Output JSON untuk 5 invoice dijalankan dengan v3.
- [ ] Setiap output divalidasi dengan JSON validator.
- [ ] Tabel evaluasi diisi penuh dengan skor.
- [ ] Refleksi 3 bullet ditulis.
- [ ] (Bonus) Mendokumentasikan checklist pre-production dari Module 4 untuk use case ini.

---

## Tips

- **Prefill `{`** di Workbench (tab assistant message) — sederhana, dramatis efeknya.
- **Format tanggal**: model kadang menulis "2024-3-15" alih-alih "2024-03-15". Tambahkan rule eksplisit: "tepat YYYY-MM-DD dengan padding nol".
- **Mata uang**: Rp / IDR / USD / $ — sebut explicit mapping di prompt.
- **Inconsistency check**: bisa minta model "hitung subtotal+tax, bandingkan dengan total tertulis, isi `matches_reported_total`".
- **Invoice 5 ambigu**: trade-off — accept partial atau return error. Tidak ada jawaban benar; argumentasikan pilihan Anda.

---

## Deliverable

Kirim ke fasilitator (LMS / Slack / Email) berisi:
1. Prompt v3 final (lengkap, copy-pastable).
2. 5 file JSON output (atau di-paste ke 1 dokumen).
3. Tabel evaluasi dengan skor.
4. Refleksi 3 bullet.
5. (Optional) Checklist pre-production yang sudah diadaptasi untuk invoice parser.

---

## Sambungan ke Day 2

Day 2 akan mengubah prompt ini menjadi **production-grade**:
- Memanggil via Anthropic API dengan Python SDK.
- Validasi schema dengan Pydantic.
- Retry logic + structured error.
- Automated evaluation pipeline.

Simpan prompt v3 — Anda akan memakainya kembali besok.
