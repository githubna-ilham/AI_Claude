# Lab 01 — Anatomy of a Prompt (Konteks Jalin)

**Modul**: Module 2 — Prompt Engineering Basics
**Durasi**: 40 menit
**Mode**: Individual atau berpasangan (maks 2 orang)
**Tools**: claude.ai (free tier sudah memadai) + editor teks atau Google Docs
**Output**: dokumen berisi 3–5 prompt hasil refactor + 2 screenshot output (sebelum vs sesudah)

---

## Tujuan

Setelah lab ini, Anda mampu:

1. Mengidentifikasi kelemahan prompt buruk berdasarkan 5 komponen anatomi (Role, Context, Task, Constraint, Output Format).
2. Me-refactor prompt menjadi versi reliable yang siap dipakai di lingkungan kerja Jalin.
3. Memverifikasi peningkatan kualitas dengan menjalankan prompt baru di claude.ai dan membandingkan hasilnya secara empiris.

---

## Prasyarat

- Telah mengikuti Module 1 (Introduction to LLM & Claude) dan Module 2 (Prompt Engineering Basics).
- Akun **claude.ai** aktif (free tier memadai; Pro lebih nyaman karena rate limit lebih longgar).
- Editor teks lokal (VS Code / Notepad) atau Google Docs untuk menyimpan hasil.

> ℹ️ **Catatan tool**: Lab ini sepenuhnya dapat dijalankan menggunakan **claude.ai gratis**. Tidak ada bagian lab yang mewajibkan akses Anthropic Console / Workbench berbayar.

---

## Langkah

### Langkah 1 — Pilih Use Case (5 menit)

Pilih **3 dari 5** use case di bawah. Jika waktu memungkinkan, kerjakan kelima-limanya. Seluruh use case berlatar konteks operasional Jalin Pembayaran Nusantara.

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

Tulis ulang setiap prompt buruk dengan template berikut. Tambahkan `<context>` yang masuk akal untuk konteks Jalin (misalnya SOP fiktif penanganan dispute, tabel tarif transaksi, daftar bank peserta, dan sejenisnya). Jika Anda tidak yakin akan angka spesifik, **gunakan placeholder yang realistis** — hal terpenting adalah struktur anatominya benar.

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

> 💡 **Tips refactor**: Hindari over-prompt pada percobaan pertama. Mulailah dari versi minimum-viable, lalu **tambahkan constraint** jika output masih kurang. Sering kali 80% peningkatan kualitas datang dari penambahan Role + Context saja.

### Langkah 4 — Verifikasi di claude.ai (10 menit)

Pilih **minimal 2 use case** dari yang Anda kerjakan, lalu lakukan A/B test berikut:

1. Jalankan **prompt buruk original** di claude.ai → screenshot output.
2. Jalankan **prompt hasil refactor** Anda → screenshot output.
3. Catat perbandingan dalam 2–3 bullet:
   - Apakah output lebih relevan dengan konteks Jalin?
   - Apakah format konsisten dan mudah diproses (oleh manusia maupun sistem)?
   - Apakah terdapat peningkatan empati atau profesionalisme (untuk use case komunikasi)?
   - Apakah ada aspek yang justru menjadi lebih buruk setelah refactor? Hal ini wajar dan dapat diperbaiki pada iterasi berikutnya.

---

## Kriteria Selesai (Definition of Done)

- [ ] Minimal 3 prompt sudah di-refactor mengikuti template anatomi.
- [ ] Setiap prompt hasil refactor mengandung minimal **4 dari 5** komponen secara eksplisit.
- [ ] Minimal **2 prompt** sudah dijalankan di claude.ai dan output di-screenshot (sebelum vs sesudah).
- [ ] Catatan perbandingan kualitas (sebelum/sesudah) ditulis untuk minimal 2 use case.

---

## Tips Penting

- **Hindari over-prompt** pada percobaan pertama. Mulailah dari minimum viable, lalu tambahkan constraint jika output masih kurang.
- **Gunakan XML tags** (`<context>`, `<task>`, `<rules>`, dan sejenisnya) untuk memisahkan instruksi dari data — Claude dilatih untuk memperhatikan struktur ini.
- **Tulis prompt dalam Bahasa Indonesia** jika audiens lokal. Claude memiliki kemampuan bilingual yang sangat baik — tidak diperlukan penerjemahan ke bahasa Inggris demi "kualitas".
- **Cobalah 2–3 variasi** untuk satu use case lalu bandingkan. Salah satu variasi umumnya akan menghasilkan output yang lebih baik dari perkiraan awal.
- Jika output JSON tidak konsisten, hal tersebut wajar — topik tersebut akan dibahas secara mendalam pada Module 4 (Structured Output). Fokuskan terlebih dahulu pada anatomi prompt.
- Jika Anda merasa salah satu use case tidak memiliki SOP referensi di dunia nyata, hal tersebut tidak menjadi masalah. Buat SOP fiktif yang masuk akal. Tujuan lab ini adalah melatih **kerangka berpikir**, bukan menghafal prosedur internal.

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

Lab ini merupakan **fondasi paling penting** sepanjang pelatihan. Anatomi prompt yang dikuasai di sini akan dipakai berulang pada:

- **Module 3 (Day 1)** — Anda akan menambahkan teknik lanjutan (few-shot, chain-of-thought) di atas anatomi yang sama.
- **Module 4 (Day 2 — pembuka)** — Anda akan memperketat **Output Format** menjadi JSON yang valid dan dapat dievaluasi secara otomatis.
- **Day 2 dan seterusnya** — Saat menulis prompt untuk fitur AI di `fin-app` (Next.js + Supabase), anatomi yang sama akan menjadi struktur dasar dari setiap prompt yang Anda definisikan dalam kode.

Investasi waktu pada lab ini akan terasa manfaatnya selama 3 hari ke depan.
