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
Siapa nama Direktur Utama BPJS Ketenagakerjaan saat ini,
kapan beliau menjabat, dan apa pencapaian utamanya dalam 12 bulan terakhir?
```

Catat respons model. Perhatikan:
- Apakah model memberi jawaban detail dengan nama, tanggal, dan angka spesifik?
- Apakah model menyatakan ketidaktahuan dengan jelas?
- Apakah ada qualifier seperti "saya tidak yakin" atau "berdasarkan informasi terbatas saya"?

### Round 2 — Dengan Sumber Eksplisit

Kunjungi https://www.bpjsketenagakerjaan.go.id, salin satu paragraf dari halaman "Tentang Kami" / "Profil". Lalu kirim prompt:

```
Berikut adalah cuplikan dari website resmi BPJS Ketenagakerjaan:

"""
[tempel paragraf di sini]
"""

Berdasarkan teks di atas SAJA, siapa Direktur Utama BPJS Ketenagakerjaan dan kapan menjabat?
Jika informasi tersebut tidak ada di dalam teks, jawab: "TIDAK DISEBUTKAN".
```

### Pertanyaan Refleksi

1. Apakah respons Round 2 lebih "aman" daripada Round 1? Apa yang membuatnya aman?
2. Teknik apa di Round 2 yang membuat model lebih sulit berhalusinasi?
3. Bagaimana Anda akan menerapkan pola ini pada use case pengelolaan data peserta atau klaim di BPJS Ketenagakerjaan?

---

## Latihan 3 — Reasoning vs Recall (6 menit)

Banyak orang mengira LLM "tahu" semua. Padahal LLM lebih kuat dalam **reasoning** (menalar dari informasi yang diberi) dibanding **recall** (mengingat fakta).

Bayangkan Anda sedang membangun **fitur kalkulator simulasi iuran BPJS Ketenagakerjaan untuk sistem HR internal perusahaan**. Anda perlu memastikan logika perhitungannya akurat — dan sebelum mempercayai hasil dari LLM, Anda harus memahami kapan model sekadar "menebak" dan kapan model benar-benar "menalar".

### Soal A — Murni Recall

Kirim prompt di claude.ai:

```
Berapa besaran iuran BPJS Ketenagakerjaan yang berlaku saat ini untuk
program JHT, JKK, JKM, dan JP?

Sebutkan tarif berikut:
- Persentase iuran yang ditanggung pekerja
- Persentase iuran yang ditanggung pemberi kerja
- Dasar perhitungan upah yang digunakan
```

Amati respons model:
- Apakah model memberi angka spesifik (mis. "2%", "3,7%")?
- Apakah model membedakan iuran pekerja dan pemberi kerja untuk setiap program?
- Apakah Anda 100% yakin angkanya **akurat dan paling baru**?
- Apakah angka tersebut dapat dipakai sebagai dasar logika produksi?

### Soal B — Reasoning dengan Konteks

Untuk keperluan latihan ini, gunakan **tabel iuran referensi** di bawah. Tabel ini disusun berdasarkan ketentuan yang berlaku pada saat materi disusun — angka eksak dapat berubah dan **bukan pengganti data resmi terbaru** saat membangun sistem produksi.

#### Tabel Referensi — Iuran BPJS Ketenagakerjaan (untuk latihan)

| Program | Iuran Pekerja | Iuran Pemberi Kerja | Total | Keterangan |
|---------|--------------|-------------------|-------|------------|
| JHT | 2% | 3,7% | 5,7% | Dasar: upah (gaji pokok + tunjangan tetap) |
| JKK | — | 0,24%–1,74% | 0,24%–1,74% | Sesuai tingkat risiko pekerjaan |
| JKM | — | 0,3% | 0,3% | Dasar: upah |
| JP | 1% | 2% | 3% | Batas upah maks Rp 9.559.600/bulan |

> ℹ️ Sumber acuan: situs resmi BPJS Ketenagakerjaan (`bpjsketenagakerjaan.go.id`) dan Peraturan Pemerintah terkait. URL spesifik dapat berubah — periksa halaman "Iuran" atau "Kepesertaan" di portal resmi untuk angka terbaru saat di lapangan.

Kirim prompt berikut ke claude.ai (tempel tabel di atas pada bagian yang ditandai):

```
Berikut tabel iuran BPJS Ketenagakerjaan yang berlaku untuk skenario perhitungan ini:

[tempel Tabel Referensi di sini]

Sebuah perusahaan memiliki seorang karyawan dengan data berikut:
- Gaji pokok: Rp 7.000.000
- Tunjangan tetap: Rp 1.000.000
- Total upah: Rp 8.000.000
- Tingkat risiko pekerjaan: menengah (JKK 0,54%)

Hitung:
1. Iuran JHT per bulan: bagian pekerja dan bagian pemberi kerja (rinci terpisah).
2. Iuran JKK per bulan (pemberi kerja).
3. Iuran JKM per bulan (pemberi kerja).
4. Iuran JP per bulan: bagian pekerja dan bagian pemberi kerja.
   Perhatikan: upah JP menggunakan nilai aktual jika di bawah batas maksimum.
5. Total iuran yang dibayar perusahaan (pemberi kerja) per bulan.
6. Total potongan iuran dari slip gaji karyawan per bulan.

Tunjukkan langkah perhitungannya secara eksplisit.
```

### Pertanyaan Refleksi

1. Manakah jawaban yang lebih dapat diaudit — Soal A atau Soal B? Mengapa?
2. Jika kalkulator iuran ini dibangun untuk sistem payroll, dari mana sebaiknya tarif iuran diambil: ingatan LLM, hard-coded, atau tabel yang di-attach? Apa implikasinya saat Pemerintah mengubah tarif?
3. Sebutkan minimal 3 jenis informasi di lingkup BPJS Ketenagakerjaan (atau organisasi Anda) yang wajib di-attach sebagai konteks, bukan mengandalkan ingatan model. Contoh: tarif iuran terbaru, batas upah JP, daftar dokumen klaim JHT.
4. Bagaimana Anda akan merancang prompt pattern yang memaksa model selalu menjawab "TIDAK ADA DI TABEL" jika data yang ditanyakan tidak tercakup dalam konteks yang diberikan?

---

## Lembar Output (Self-Check)

Setelah menyelesaikan ketiga latihan, periksa apakah Anda dapat menjawab pertanyaan-pertanyaan berikut dengan kalimat Anda sendiri:

- [ ] Saya memahami mengapa Bahasa Indonesia cenderung lebih banyak token dibanding Bahasa Inggris.
- [ ] Saya mampu menyusun prompt yang memaksa model jujur saat tidak tahu jawaban — misalnya saat ditanya tentang data peserta atau kebijakan iuran BPJS Ketenagakerjaan yang mungkin berubah.
- [ ] Saya akan selalu memilah: ini pertanyaan yang butuh **reasoning** atau **recall** — dan menyiapkan konteks (seperti tabel iuran atau SLA klaim) yang sesuai agar hasil LLM dapat diaudit.

---

## Pengumpulan & Tindak Lanjut

- Foto atau screenshot output dari Latihan 1, 2, dan 3 dapat diunggah ke channel pelatihan dengan format `M1-L[1/2/3]-NamaAnda.png`.
- Refleksi tertulis (1 paragraf) mengenai **use case AI di pekerjaan Anda** akan menjadi referensi pribadi pada Module 5 (Prompt for Business Use Cases) di Day 2.

> **Penutup**: Module 1 secara sengaja membatasi diri pada pemahaman cara kerja LLM. Mulai Module 2, Anda akan masuk ke **prompt craft** — bagaimana menulis instruksi yang membuat model bekerja sesuai keinginan Anda secara konsisten, termasuk untuk kebutuhan operasional BPJS Ketenagakerjaan seperti pemrosesan klaim, pengelolaan kepesertaan, dan pelaporan iuran.
