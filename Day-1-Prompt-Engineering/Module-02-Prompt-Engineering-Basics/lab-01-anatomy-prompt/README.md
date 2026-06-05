# Lab 01 — Anatomy of a Prompt

**Modul**: Module 2 — Prompt Engineering Basics
**Durasi**: 45 menit
**Mode**: Individual atau pair (max 2 orang)
**Tools**: claude.ai (model Sonnet 4.x disarankan) atau Anthropic Console — Workbench
**Output**: dokumen berisi 5 prompt hasil refactor + 1 screenshot output untuk minimal 2 prompt.

---

## Tujuan

Peserta mampu:
1. Mengidentifikasi kelemahan prompt buruk berdasarkan 5 komponen anatomi.
2. Me-refactor menjadi prompt yang reliable dengan struktur **Role + Context + Task + Constraint + Output Format**.
3. Memverifikasi peningkatan kualitas dengan menjalankan prompt baru di Claude.

---

## Prasyarat

- Sudah mengikuti Module 1 & Module 2.
- Akun claude.ai aktif (free tier cukup; Pro lebih nyaman karena rate limit lebih longgar).
- Editor teks lokal atau Google Docs untuk menyimpan hasil.

---

## Langkah

### Langkah 1 — Pilih Use Case (5 menit)

Pilih **3 dari 5** use case di bawah. Jika waktu cukup, kerjakan kelima.

| # | Use Case                          | Prompt Buruk (refactor ini)                                                                 |
|---|-----------------------------------|---------------------------------------------------------------------------------------------|
| 1 | Customer Service Reply            | `Balas keluhan pelanggan ini: "Order saya sudah seminggu belum dikirim"`                    |
| 2 | Ringkasan Rapat (notulen)         | `Ringkas notulen rapat ini: {tempel transkrip rapat 2 halaman}`                             |
| 3 | Klasifikasi Tiket Support         | `Tiket ini kategori apa: "Saya tidak bisa login setelah update aplikasi kemarin malam"`     |
| 4 | Email Penolakan Kandidat (HR)     | `Tulis email penolakan untuk kandidat yang gagal interview`                                 |
| 5 | Generate FAQ dari Dokumen Produk  | `Buat FAQ dari dokumen produk ini: {tempel spec produk}`                                    |

### Langkah 2 — Audit Anatomi (5 menit)

Untuk setiap prompt buruk, isi tabel audit:

| Komponen        | Ada? (Y/N) | Catatan kelemahan                              |
|-----------------|------------|------------------------------------------------|
| Role            |            |                                                |
| Context         |            |                                                |
| Task            |            |                                                |
| Constraint      |            |                                                |
| Output Format   |            |                                                |

### Langkah 3 — Refactor Prompt (20 menit)

Tulis ulang prompt dengan template:

```text
<role>
{Anda adalah ... dengan expertise ...; audiens ...}
</role>

<context>
{informasi domain, dokumen referensi, SOP, glossary}
</context>

<task>
{instruksi utama, decompose menjadi langkah jika perlu}
</task>

<rules>
- {constraint 1}
- {constraint 2}
- Jika informasi tidak cukup, jawab "INFO_KURANG".
</rules>

<output_format>
{struktur output, contoh bila perlu}
</output_format>
```

Tambah `<context>` yang masuk akal jika perlu (misal SOP customer service fiktif).

### Langkah 4 — Verifikasi di Claude (10 menit)

1. Jalankan **prompt buruk** original di claude.ai → screenshot output.
2. Jalankan **prompt hasil refactor** Anda → screenshot output.
3. Catat perbedaan kualitas dalam 2-3 bullet:
   - Apakah output lebih relevan?
   - Apakah format konsisten?
   - Apakah ada peningkatan empati/profesionalisme (untuk use case komunikasi)?

### Langkah 5 — Peer Review (5 menit)

Tukar hasil dengan rekan / peserta lain. Beri 1 saran perbaikan untuk salah satu prompt mereka.

---

## Kriteria Selesai (Definition of Done)

- [ ] Minimal 3 prompt telah di-refactor mengikuti template anatomi.
- [ ] Setiap prompt refactor mengandung minimal 4 dari 5 komponen secara eksplisit.
- [ ] Minimal 2 prompt telah dijalankan di Claude dan output di-screenshot.
- [ ] Catatan perbandingan kualitas (sebelum/sesudah) ditulis untuk 2 use case.
- [ ] Telah memberi/menerima peer review minimal 1 kali.

---

## Rubrik Evaluasi (skala 0–4 per kriteria)

| Kriteria                                         | 0 (kurang)        | 2 (cukup)             | 4 (excellent)                          |
|--------------------------------------------------|-------------------|-----------------------|----------------------------------------|
| Kejelasan Role                                   | Tidak ada / generik | Disebut tapi vague   | Spesifik + expertise + audiens         |
| Kekayaan Context                                 | Hampa             | Minimal               | Lengkap, terstruktur (XML/tag)         |
| Spesifisitas Task                                | Ambigu            | Jelas tapi monolitik  | Decomposed, action verb, granular      |
| Konkretness Constraint                           | Tidak ada         | 1-2 constraint        | Multi-dimensi (length, tone, safety)   |
| Ketepatan Output Format                          | Tidak disebut     | Disebut tapi longgar  | Schema/struktur eksplisit + contoh     |
| Improvement output (bukti empiris)               | Tidak ada bukti   | Sedikit lebih baik    | Jauh lebih relevan, terformat, andal   |

**Total maksimal**: 24 poin. Target lulus: 16 poin (target stretch: 20+).

---

## Tips

- **Jangan over-prompt** pada percobaan pertama. Mulai dari minimum viable, tambah constraint kalau output masih kurang.
- **Gunakan XML tags** untuk memisahkan instruksi dari data.
- **Tulis dalam bahasa Indonesia** jika audiens lokal — Claude bilingual yang sangat baik.
- **Coba 2-3 variasi** untuk satu use case dan bandingkan.
- Jika output JSON tidak konsisten, **akan dibahas mendalam di Module 4** — fokus dulu pada anatomi.

---

## Deliverable

Simpan dalam file (atau Google Doc) dengan struktur:

```
# Lab 01 — {Nama Anda}

## Use Case 1: {nama use case}
### Audit anatomi prompt buruk
{tabel}
### Prompt hasil refactor
```
{prompt}
```
### Screenshot output sebelum vs sesudah
{link / image}
### Catatan perbandingan
- ...

## Use Case 2: ...
...
```

Kirim ke fasilitator via channel yang ditentukan (LMS / Slack / Email).
