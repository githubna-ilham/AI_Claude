# Lab 01 — Anatomy of a Prompt (Konteks Jalin)

**Modul**: Module 2 — Prompt Engineering Basics
**Durasi**: 40 menit
**Mode**: Individual atau berpasangan (maks 2 orang)
**Tools**: claude.ai (free tier sudah cukup) + editor teks atau Google Docs
**Output**: dokumen berisi 3–5 prompt hasil refactor + 2 screenshot output (sebelum vs sesudah)

---

## Tujuan

Setelah lab ini, peserta mampu:

1. Mengidentifikasi kelemahan prompt buruk berdasarkan 5 komponen anatomi (Role, Context, Task, Constraint, Output Format).
2. Me-refactor prompt menjadi versi reliable yang siap dipakai di lingkungan kerja Jalin.
3. Memverifikasi peningkatan kualitas dengan menjalankan prompt baru di claude.ai dan membandingkan hasilnya secara empiris.

---

## Prasyarat

- Sudah mengikuti Module 1 (Introduction to LLM & Claude) dan Module 2 (Prompt Engineering Basics).
- Akun **claude.ai** aktif (free tier cukup; Pro lebih nyaman karena rate limit lebih longgar).
- Editor teks lokal (VS Code / Notepad) atau Google Docs untuk menyimpan hasil.

> ℹ️ **Catatan tool**: Lab ini sepenuhnya dapat dijalankan menggunakan **claude.ai gratis**. Tidak ada bagian lab yang mewajibkan akses Anthropic Console / Workbench berbayar.

---

## Langkah

### Langkah 1 — Pilih Use Case (5 menit)

Pilih **3 dari 5** use case di bawah. Jika waktu cukup, kerjakan kelima. Semua use case berlatar konteks operasional Jalin Pembayaran Nusantara.

| # | Use Case                                            | Prompt Buruk (yang harus Anda refactor)                                                                                       |
|---|-----------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| 1 | Balasan Keluhan Nasabah — Transaksi Gagal           | `Balas keluhan ini: "Saya transfer Rp 5 juta via BI-FAST tapi gagal, saldo sudah terdebit, sudah 3 hari belum balik"`          |
| 2 | Ringkasan Notulen Rapat Operasional Switching       | `Ringkas notulen rapat berikut: {tempel transkrip rapat operasional 2 halaman}`                                               |
| 3 | Klasifikasi Tiket Incident Sistem Pembayaran        | `Tiket ini kategori apa: "Transaksi tarik tunai di ATM Link gagal tapi mesin keluarkan struk sukses sejak pukul 22.00 kemarin"` |
| 4 | Email Komunikasi Internal — Maintenance Window      | `Tulis email pemberitahuan maintenance jaringan ATM Link kepada bank peserta`                                                 |
| 5 | Generate FAQ Internal — Produk QRIS untuk Merchant  | `Buat FAQ tentang biaya dan limit QRIS dari dokumen produk ini: {tempel spec produk QRIS}`                                    |

### Langkah 2 — Audit Anatomi (5 menit)

Untuk setiap prompt buruk yang Anda pilih, isi tabel audit berikut. Tujuannya: melatih mata Anda mengenali komponen yang hilang.

| Komponen        | Ada? (Y/N) | Catatan kelemahan                              |
|-----------------|------------|------------------------------------------------|
| Role            |            |                                                |
| Context         |            |                                                |
| Task            |            |                                                |
| Constraint      |            |                                                |
| Output Format   |            |                                                |

### Langkah 3 — Refactor Prompt (20 menit)

Tulis ulang setiap prompt buruk dengan template berikut. Tambahkan `<context>` yang masuk akal untuk konteks Jalin (mis. SOP fiktif penanganan dispute, tabel tarif transaksi, daftar bank peserta, dll). Jika Anda tidak yakin angka spesifik, **gunakan placeholder yang realistis** — yang penting struktur anatominya benar.

```text
<role>
Anda adalah {peran spesifik di Jalin, mis. CS officer / Network Engineer /
Product Manager} dengan {expertise / pengalaman}. Audiens: {target pembaca}.
</role>

<context>
{informasi domain, SOP internal, tabel tarif, daftar bank peserta,
glossary singkat — secukupnya, jangan over-stuff}
</context>

<task>
{instruksi utama; jika kompleks, pecah menjadi 3-4 langkah berurutan}
</task>

<rules>
- {constraint 1, mis. tone profesional, maks 120 kata}
- {constraint 2, mis. wajib sebut SLA, jangan janjikan kompensasi spesifik}
- Jika informasi yang dibutuhkan tidak tersedia di context, jawab "INFO_KURANG".
</rules>

<output_format>
{struktur output yang diinginkan — markdown / JSON / hibrida.
Beri contoh field & isi jika perlu.}
</output_format>
```

> 💡 **Tips refactor**: Jangan over-prompt di percobaan pertama. Mulai dari versi minimum-viable, lalu **tambah constraint** kalau output masih kurang. Anda akan terkejut betapa sering 80% peningkatan datang dari menambah Role + Context saja.

### Langkah 4 — Verifikasi di claude.ai (10 menit)

Pilih **minimal 2 use case** dari yang Anda kerjakan, lalu lakukan A/B test berikut:

1. Jalankan **prompt buruk original** di claude.ai → screenshot output.
2. Jalankan **prompt hasil refactor** Anda → screenshot output.
3. Catat perbandingan dalam 2–3 bullet:
   - Apakah output lebih relevan ke konteks Jalin?
   - Apakah format konsisten dan mudah diproses (manusia / sistem)?
   - Apakah ada peningkatan empati / profesionalisme (untuk use case komunikasi)?
   - Apakah ada hal yang justru menjadi lebih buruk setelah refactor? (Jujur saja — ini wajar dan bisa diperbaiki di iterasi berikutnya.)

---

## Kriteria Selesai (Definition of Done)

- [ ] Minimal 3 prompt sudah di-refactor mengikuti template anatomi.
- [ ] Setiap prompt hasil refactor mengandung minimal **4 dari 5** komponen secara eksplisit.
- [ ] Minimal **2 prompt** sudah dijalankan di claude.ai dan output di-screenshot (sebelum vs sesudah).
- [ ] Catatan perbandingan kualitas (sebelum/sesudah) ditulis untuk minimal 2 use case.

---

## Tips Penting

- **Jangan over-prompt** pada percobaan pertama. Mulai dari minimum viable, lalu tambah constraint kalau output masih kurang.
- **Gunakan XML tags** (`<context>`, `<task>`, `<rules>`, dst.) untuk memisahkan instruksi dari data — Claude dilatih untuk memperhatikan struktur ini.
- **Tulis prompt dalam Bahasa Indonesia** jika audiens lokal. Claude bilingual yang sangat baik — Anda tidak perlu menerjemahkan ke bahasa Inggris demi "kualitas".
- **Coba 2–3 variasi** untuk satu use case dan bandingkan. Salah satunya pasti lebih baik dari yang Anda kira awal.
- Jika output JSON tidak konsisten, **jangan panik** — topik tersebut akan dibahas mendalam di Module 4 (Structured Output). Fokus dulu pada anatomi prompt.
- Bila Anda merasa salah satu use case "tidak tahu apa SOP-nya di dunia nyata" — itu **OK**. Buat SOP fiktif yang masuk akal. Tujuan lab ini adalah melatih **kerangka berpikir**, bukan menghafal prosedur internal.

---

## Deliverable

Simpan dalam file Markdown (atau Google Doc) dengan struktur berikut:

```
# Lab 01 — {Nama Anda}

## Use Case 1: {nama use case}
### Audit anatomi prompt buruk
{tabel}

### Prompt hasil refactor
{prompt}

### Screenshot output sebelum vs sesudah
{link / image}

### Catatan perbandingan
- ...

## Use Case 2: ...
...
```

Kirim ke fasilitator via channel yang ditentukan (LMS / Slack / Telegram).

---

## Catatan Penutup

Lab ini adalah **fondasi paling penting** sepanjang pelatihan. Anatomi prompt yang Anda kuasai di sini akan dipakai berulang di:

- **Module 3 (Day 1)** — Anda akan menambahkan teknik lanjutan (few-shot, chain-of-thought) di atas anatomi yang sama.
- **Module 4 (Day 2 — pembuka)** — Anda akan memperketat **Output Format** menjadi JSON yang valid dan dapat dievaluasi otomatis.
- **Day 2+** — Saat menulis prompt untuk fitur AI di `fin-app` (Next.js + Supabase), anatomi yang sama akan menjadi struktur dasar dari setiap prompt yang Anda definisikan dalam kode.

Investasi waktu di sini akan terasa manfaatnya selama 3 hari ke depan.
