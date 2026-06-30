# Latihan — Module 1: Introduction to LLM & Claude

**Durasi**: 18 menit (3 latihan × ~6 menit)
**Mode**: Individu atau berpasangan
**Tools**: claude.ai (free tier sudah cukup) + browser + tokenizer web
**Output**: catatan singkat atau screenshot per latihan, dikumpulkan ke channel pelatihan

> ℹ️ **Catatan akses tool**: Seluruh latihan ini dirancang agar dapat dijalankan **gratis** menggunakan claude.ai tanpa perlu top-up Anthropic Console. Tidak ada bagian latihan yang mewajibkan akses ke Workbench berbayar.

---

## Tujuan Latihan

Setelah materi Module 1 yang dominan konsep, latihan ini membantu Anda **merasakan langsung** perbedaan antara teori dan realita. Tidak ada coding — seluruh latihan dijalankan melalui UI claude.ai (free tier). Tujuannya bukan menghasilkan jawaban "benar", melainkan membangun intuisi mengenai cara LLM berperilaku.

Setelah latihan ini Anda akan mampu:

1. Memperkirakan jumlah token sebuah teks dan menyadari implikasi biayanya.
2. Mengenali kapan model "tidak tahu" vs "mengarang dengan percaya diri".
3. Membedakan reasoning vs recall — dan tahu kapan harus tidak mempercayai jawaban model.

---

## Latihan 1 — Eksplorasi Tokenization (6 menit)

Buka https://platform.openai.com/tokenizer (tokenizer ini menggunakan sistem yang mirip dengan Claude untuk perkiraan kasar).

Ketik tiga input berikut secara bergantian, lalu **catat jumlah token** masing-masing:

| Input                                                       | Karakter | Token (catat) |
| ----------------------------------------------------------- | -------- | ------------- |
| `Selamat pagi semuanya`                                     | 21       | …             |
| `Good morning everyone`                                     | 21       | …             |
| `def hello_world(): print("Halo dunia")`                    | 38       | …             |

### Pertanyaan Refleksi

1. Mana yang menggunakan lebih banyak token: kalimat Bahasa Indonesia atau Bahasa Inggris dengan panjang karakter yang sama? Menurut Anda mengapa?
2. Jika harga API dihitung per token, bahasa mana yang lebih "mahal" untuk volume teks yang sama?
3. Hitung perkiraan biaya untuk memproses 10.000 dokumen Bahasa Indonesia berukuran 500 karakter masing-masing menggunakan model Haiku (lihat https://www.anthropic.com/pricing).

---

## Latihan 2 — Mendeteksi Halusinasi (6 menit)

Buka **claude.ai** dan pilih model **Sonnet 4.x**.

### Round 1 — Tanpa Sumber

Kirim prompt berikut:

```
Siapa nama Direktur Utama PT Jalin Pembayaran Nusantara saat ini,
kapan beliau menjabat, dan apa pencapaian utamanya dalam 12 bulan terakhir?
```

Catat respons model. Perhatikan:
- Apakah model memberi jawaban detail dengan nama, tanggal, dan angka spesifik?
- Apakah model menyatakan ketidaktahuan dengan jelas?
- Apakah ada qualifier seperti "saya tidak yakin" atau "berdasarkan informasi terbatas saya"?

### Round 2 — Dengan Sumber Eksplisit

Kunjungi https://www.jalin.co.id, salin satu paragraf dari halaman "Tentang Kami" / "About Us" / "Perusahaan". Lalu kirim prompt:

```
Berikut adalah cuplikan dari website resmi PT Jalin Pembayaran Nusantara:

"""
[tempel paragraf di sini]
"""

Berdasarkan teks di atas SAJA, siapa Direktur Utama Jalin dan kapan menjabat?
Jika informasi tersebut tidak ada di dalam teks, jawab: "TIDAK DISEBUTKAN".
```

### Pertanyaan Refleksi

1. Apakah respons Round 2 lebih "aman" daripada Round 1? Apa yang membuatnya aman?
2. Teknik apa di Round 2 yang membuat model lebih sulit berhalusinasi?
3. Bagaimana Anda akan menerapkan pola ini pada use case di pekerjaan Anda?

---

## Latihan 3 — Reasoning vs Recall (6 menit)

Banyak orang mengira LLM "tahu" semua. Padahal LLM lebih kuat dalam **reasoning** (menalar dari informasi yang diberi) dibanding **recall** (mengingat fakta).

Bayangkan Anda sedang membangun **fitur kalkulator biaya transaksi antar bank** untuk aplikasi internal Jalin. Anda perlu memastikan logika perhitungannya akurat — dan sebelum mempercayai hasil dari LLM, Anda harus memahami kapan model sekadar "menebak" dan kapan model benar-benar "menalar".

### Soal A — Murni Recall

Kirim prompt di claude.ai:

```
Berapa biaya transaksi transfer antar bank di Indonesia melalui
jaringan BI-FAST, ATM Bersama, dan Link saat ini?

Sebutkan tarif per jenis transaksi berikut:
- Transfer antar bank
- Tarik tunai di ATM bank lain
- Cek saldo di ATM bank lain
```

Amati respons model:
- Apakah model memberi angka spesifik (mis. "Rp 2.500", "Rp 6.500")?
- Apakah model membedakan jaringan satu dengan lainnya?
- Apakah Anda 100% yakin angkanya **akurat dan paling baru**?
- Apakah angka tersebut dapat dipakai sebagai dasar logika produksi?

### Soal B — Reasoning dengan Konteks

Untuk keperluan latihan ini, gunakan **tabel tarif referensi** di bawah. Tabel ini disusun berdasarkan pola umum tarif yang berlaku di industri pada saat materi disusun — angka eksak dapat berubah dan **bukan pengganti data resmi terbaru** saat membangun sistem produksi.

#### Tabel Referensi — Tarif Transaksi Antar Bank (untuk latihan)

| Jaringan       | Transfer antar bank | Tarik tunai ATM bank lain | Cek saldo ATM bank lain | Limit per transaksi |
| -------------- | ------------------- | ------------------------- | ----------------------- | ------------------- |
| **BI-FAST**    | Rp 2.500            | —                         | —                       | Rp 250.000.000      |
| **ATM Bersama**| Rp 6.500            | Rp 7.500                  | Rp 4.000                | Rp 25.000.000       |
| **Link**       | Rp 6.500            | Rp 7.500                  | Rp 4.000                | Rp 25.000.000       |

> ℹ️ Sumber acuan umum: situs resmi Bank Indonesia (`bi.go.id`), PT Jalin Pembayaran Nusantara (`jalin.co.id`), dan publikasi tarif masing-masing bank penerbit. URL spesifik dapat berubah — gunakan kata kunci pencarian seperti *"tarif BI-FAST resmi"*, *"biaya ATM Bersama transfer"*, atau periksa pengumuman tarif di internet banking bank Anda untuk angka terbaru saat di lapangan.

Kirim prompt berikut ke claude.ai (tempel tabel di atas pada bagian yang ditandai):

```
Berikut tabel tarif resmi transaksi antar bank di jaringan Link, ATM Bersama,
dan BI-FAST yang berlaku untuk skenario perhitungan ini:

[tempel Tabel Referensi di sini]

Seorang nasabah Bank A melakukan transaksi sebagai berikut dalam 1 hari:
- 3× transfer Rp 5.000.000 ke rekening Bank B via BI-FAST
- 2× tarik tunai Rp 1.000.000 di ATM Bank C (jaringan ATM Bersama)
- 5× cek saldo di ATM Bank D (jaringan Link)
- 1× transfer Rp 25.000.000 ke rekening Bank E via BI-FAST

Hitung:
1. Total biaya yang dibebankan ke nasabah (rinci per transaksi).
2. Total nominal yang didebit dari rekening nasabah (nominal + biaya).
3. Apakah ada transaksi yang melampaui limit per transaksi?
   Jika ya, sebutkan dan jelaskan implikasinya.

Tunjukkan langkah perhitungannya secara eksplisit.
```

### Pertanyaan Refleksi

1. Manakah jawaban yang lebih dapat diaudit dan diintegrasikan ke sistem produksi — Soal A atau Soal B? Mengapa?
2. Jika kalkulator biaya transaksi ini benar-benar dibangun, dari mana sumber tarif sebaiknya berasal: ingatan LLM, hard-coded di kode, atau tabel referensi yang di-attach setiap kali request? Apa implikasi pilihan tersebut terhadap maintenance saat tarif berubah?
3. Sebutkan **minimal 3 jenis informasi** di lingkup pekerjaan Anda di Jalin (atau di organisasi Anda) yang **tidak boleh** mengandalkan ingatan model dan **wajib** di-attach sebagai konteks. Contoh: tarif, SLA dispute, daftar bank peserta, batas limit harian, kebijakan internal terbaru.
4. Skenario praktis: bagaimana Anda akan merancang **prompt pattern** yang memaksa model selalu menjawab "TIDAK ADA DI TABEL" jika data yang ditanyakan tidak tercakup dalam konteks yang Anda berikan?

---

## Lembar Output (Self-Check)

Setelah menyelesaikan ketiga latihan, periksa apakah Anda dapat menjawab pertanyaan-pertanyaan berikut dengan kalimat Anda sendiri:

- [ ] Saya memahami mengapa Bahasa Indonesia cenderung lebih banyak token dibanding Bahasa Inggris.
- [ ] Saya mampu menyusun prompt yang memaksa model jujur saat tidak tahu jawaban.
- [ ] Saya akan selalu memilah: ini pertanyaan yang butuh **reasoning** atau **recall** — dan menyiapkan konteks yang sesuai.

---

## Pengumpulan & Tindak Lanjut

- Foto atau screenshot output dari Latihan 1, 2, dan 3 dapat diunggah ke channel pelatihan dengan format `M1-L[1/2/3]-NamaAnda.png`.
- Refleksi tertulis (1 paragraf) mengenai **use case AI di pekerjaan Anda** akan menjadi referensi pribadi pada Module 5 (Prompt for Business Use Cases) di Day 2.

> **Penutup**: Module 1 secara sengaja membatasi diri pada pemahaman cara kerja LLM. Mulai Module 2, Anda akan masuk ke **prompt craft** — bagaimana menulis instruksi yang membuat model bekerja sesuai keinginan Anda secara konsisten.
