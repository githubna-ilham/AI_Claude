# Latihan — Module 1: Introduction to LLM & Claude

**Durasi**: 30 menit (5 latihan × ~6 menit)
**Mode**: Individu atau berpasangan
**Tools**: claude.ai (free tier sudah cukup) + browser + tokenizer web
**Output**: catatan singkat / screenshot per latihan, dikumpulkan ke channel pelatihan

> ℹ️ **Catatan akses tool**: Seluruh latihan ini dirancang agar dapat dijalankan **gratis** menggunakan claude.ai tanpa perlu top-up Anthropic Console. Tidak ada bagian latihan yang mewajibkan akses ke Workbench berbayar.

---

## Tujuan Latihan

Setelah materi Module 1 yang dominan konsep, latihan ini membantu Anda **merasakan langsung** perbedaan teori dan realita. Tidak ada coding — semua dijalankan lewat UI claude.ai (free tier). Tujuannya bukan menghasilkan jawaban "benar", melainkan membangun intuisi tentang cara LLM berperilaku.

Setelah latihan ini Anda akan mampu:

1. Memperkirakan jumlah token sebuah teks dan menyadari implikasi biayanya.
2. Mengenali kapan model "tidak tahu" vs "mengarang dengan percaya diri".
3. Memilih model Claude (Haiku / Sonnet / Opus) yang tepat berdasarkan trade-off kecepatan, biaya, dan kualitas.
4. Membaca behavior model saat context window mulai penuh.
5. Membedakan reasoning vs recall — dan tahu kapan harus tidak mempercayai jawaban model.

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

## Latihan 3 — Memilih Model yang Tepat untuk Use Case (6 menit)

Berbeda dari latihan lain, latihan ini **lebih analitis** daripada hands-on. Tujuannya: melatih keputusan pemilihan model **sebelum** Anda menulis baris kode pertama di Day 2.

### Langkah 1 — Jalankan 1 Prompt di claude.ai

Buka **claude.ai** (free tier) dan kirim prompt berikut. Catat respons + kira-kira berapa detik model "berpikir":

```
Anda adalah analis bisnis. Berikut transkrip pendek rapat:

Andi: "Pendapatan kuartal ini turun 8% dibanding kuartal lalu."
Bita: "Tetapi biaya akuisisi pelanggan kita turun 22%."
Citra: "Pelanggan baru naik 35%, dan retention juga membaik."

Buat ringkasan eksekutif 3 kalimat: apa yang terjadi, mengapa,
dan apa yang sebaiknya dilakukan kuartal berikutnya?
```

### Langkah 2 — Baca Tabel Karakteristik Model

Buka https://www.anthropic.com/pricing dan cermati harga input/output token untuk **Haiku, Sonnet, dan Opus**. Lalu lengkapi tabel berikut berdasarkan informasi resmi + materi Module 1:

| Model      | Harga input ($/1M token) | Harga output ($/1M token) | Kecepatan relatif | Kelebihan utama |
| ---------- | ------------------------ | ------------------------- | ----------------- | --------------- |
| **Haiku**  | …                        | …                         | Paling cepat      | Volume tinggi, low-cost, task ringan |
| **Sonnet** | …                        | …                         | Sedang            | Default "sweet spot" — kualitas tinggi, harga wajar |
| **Opus**   | …                        | …                         | Paling lambat     | Reasoning terkompleks, dokumen panjang |

### Langkah 3 — Pemetaan Use Case → Model

Berdasarkan tabel di atas dan respons Anda di Langkah 1, **petakan 4 use case berikut** ke model paling sesuai. Tulis alasannya 1 kalimat per use case.

| Use Case Jalin                                                                    | Model pilihan | Alasan |
| --------------------------------------------------------------------------------- | ------------- | ------ |
| **A.** Auto-kategorisasi 100.000 notifikasi transaksi per hari (text → label)     | …             | …      |
| **B.** Chat assistant untuk membaca kontrak SLA 30 halaman dan menarik klausul    | …             | …      |
| **C.** Drafting respons keluhan nasabah di customer service (volume sedang)       | …             | …      |
| **D.** Analisis post-mortem incident sistem pembayaran (1×/minggu, butuh nalar)   | …             | …      |

### Pertanyaan Refleksi

1. Apakah Opus benar-benar memberi jawaban yang **30× lebih bagus** dari Haiku (sesuai selisih harga)? Atau untuk use case sederhana, perbedaannya marginal?
2. Untuk **use case A** (volume 100.000/hari), berapa estimasi biaya bulanan jika memakai Haiku vs Sonnet? (perkiraan kasar: 300 token input + 50 token output per request).
3. Use case apa di organisasi Anda yang **menjustifikasi** biaya Opus — yaitu low-volume tapi high-stakes reasoning?
4. Jika Anda harus memilih **satu model default** untuk semua proyek AI internal Jalin di tahap awal eksplorasi, mana yang akan Anda rekomendasikan dan mengapa?

---

## Latihan 4 — Eksperimen Context Window (6 menit)

Buka **claude.ai** (free tier).

### Skenario A — Konteks Pendek

Kirim prompt singkat:

```
Nama saya Ilham. Saya berusia 30 tahun.
Apa nama saya dan berapa usia saya?
```

Model akan menjawab dengan akurat. Catat.

### Skenario B — Konteks "Diselipi"

Salin **seluruh paragraf di bawah ini apa adanya** ke claude.ai (paragraf sudah berisi "needle" tersembunyi di tengah). Lalu kirim pertanyaan di bagian bawah.

```
PT Jalin Pembayaran Nusantara, yang lebih dikenal sebagai Jalin, merupakan
perusahaan penyelenggara jasa sistem pembayaran nasional di Indonesia. Sejak
beroperasi, Jalin berperan sebagai penghubung antar bank, khususnya pada
jaringan ATM Link yang menyediakan layanan transaksi tarik tunai, transfer,
dan cek saldo lintas-bank dengan tarif yang kompetitif. Posisi Jalin sebagai
penyedia infrastruktur pembayaran membuat perusahaan ini menjadi salah satu
elemen kunci dalam ekosistem keuangan digital nasional, terutama dalam
mendukung interoperabilitas layanan perbankan.

Selain ATM Link, Jalin juga mengembangkan berbagai inisiatif terkait sistem
pembayaran ritel, termasuk integrasi dengan BI-FAST yang merupakan platform
fast payment milik Bank Indonesia. Melalui BI-FAST, masyarakat dapat
melakukan transfer antar bank dengan biaya yang lebih murah dan proses yang
real-time, 24 jam sehari, 7 hari seminggu. Kehadiran BI-FAST mendorong
kompetisi antar bank dalam memberikan layanan transfer yang efisien.

Pada tahun 2026, Jalin menyelenggarakan turnamen olahraga internal tahunan
bertajuk "Jalin Sports Festival 2026" yang melibatkan delapan kantor cabang
di seluruh Indonesia. Maskot resmi turnamen tahun ini adalah seekor burung
merak biru bernama Komeng, yang dipilih oleh karyawan melalui voting daring.
Komeng dipilih karena dianggap merepresentasikan nilai keterhubungan dan
kebanggaan budaya Indonesia. Selain pertandingan futsal dan bulu tangkis,
turnamen ini juga menggelar lomba e-sport dan kategori hiburan bagi keluarga
karyawan.

Di sisi pengembangan produk, Jalin terus mendorong adopsi teknologi terkini
seperti QRIS, layanan transfer berbasis nomor ponsel, hingga eksplorasi
penggunaan AI untuk peningkatan layanan pelanggan. Eksplorasi AI tersebut
mencakup chatbot internal, analitik perilaku transaksi, dan deteksi pola
fraud. Komitmen ini sejalan dengan dorongan Bank Indonesia untuk mempercepat
transformasi digital sektor keuangan.

Sebagai BUMN di bawah HIMBARA, Jalin juga aktif menjalin kerja sama dengan
mitra strategis termasuk fintech, e-commerce, dan platform digital lainnya.
Kerja sama ini bertujuan memperluas akses keuangan kepada masyarakat yang
belum terlayani perbankan tradisional, terutama di wilayah Indonesia bagian
timur. Berbagai program literasi keuangan dan inklusi digital pun dijalankan
secara berkala dalam rangka mendukung agenda pemerintah.
```

Pertanyaan yang dikirim **setelah** paragraf di atas:

```
Berdasarkan seluruh teks di atas, apa nama maskot resmi turnamen
"Jalin Sports Festival 2026"?
```

Catat: apakah model menemukan informasinya dengan tepat? Berapa lama responsnya?

> ⚠️ **Catatan penting — kenapa "needle"-nya benign begini**: Kalau Anda mencoba menyelipkan kalimat seperti *"kode akses brankas adalah 8842-X"*, model justru akan **menolak menjawab** dan mengatakan ini "prompt injection". Itu **bukan bug** — Claude memang dilatih untuk waspada terhadap kredensial/rahasia yang diselipkan di dokumen yang tidak diketahui asal usulnya. Jadi paragraf di atas memakai "fakta sepele" (nama maskot fiktif) supaya safety training tidak ikut campur, dan Anda murni menguji **kemampuan retrieval** model.

### Pertanyaan Refleksi

1. Apakah model masih bisa menemukan informasi yang "tersembunyi" di tengah teks panjang? Ini disebut **needle-in-a-haystack** test.
2. Apa implikasi praktisnya jika Anda ingin model membaca kontrak 50 halaman dan menjawab pertanyaan spesifik?
3. Apakah ada batas panjang di mana akurasi model mulai menurun?
4. **(Bonus)** Coba ulang Skenario B dengan needle berupa "kode akses" atau "password". Amati perilaku safety model. Bagaimana implikasinya jika di Jalin Anda ingin membangun fitur "ringkas dokumen internal" — apakah dokumen yang berisi konfigurasi sistem akan diproses normal, atau ditolak? Apa workaround design-nya?

---

## Latihan 5 — Reasoning vs Recall (6 menit)

Banyak orang mengira LLM "tahu" semua. Padahal LLM lebih kuat dalam **reasoning** (menalar dari informasi yang diberi) dibanding **recall** (mengingat fakta).

Bayangkan Anda sedang membangun **fitur kalkulator biaya transaksi antar bank** untuk aplikasi internal Jalin. Anda perlu memastikan logika perhitungannya akurat — dan sebelum percaya hasil dari LLM, Anda harus memahami kapan model "menebak" dan kapan model "menalar".

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
- Apakah angka tersebut bisa dipakai sebagai dasar logika produksi?

### Soal B — Reasoning dengan Konteks

Untuk keperluan latihan ini, gunakan **tabel tarif referensi** di bawah. Tabel ini disusun berdasarkan pola umum tarif yang berlaku di industri pada saat materi disusun — angka eksak bisa berubah dan **bukan pengganti data resmi terbaru** saat membangun sistem produksi.

#### Tabel Referensi — Tarif Transaksi Antar Bank (untuk latihan)

| Jaringan       | Transfer antar bank | Tarik tunai ATM bank lain | Cek saldo ATM bank lain | Limit per transaksi |
| -------------- | ------------------- | ------------------------- | ----------------------- | ------------------- |
| **BI-FAST**    | Rp 2.500            | —                         | —                       | Rp 250.000.000      |
| **ATM Bersama**| Rp 6.500            | Rp 7.500                  | Rp 4.000                | Rp 25.000.000       |
| **Link**       | Rp 6.500            | Rp 7.500                  | Rp 4.000                | Rp 25.000.000       |

> ℹ️ Sumber acuan umum: situs resmi Bank Indonesia (`bi.go.id`), PT Jalin Pembayaran Nusantara (`jalin.co.id`), dan publikasi tarif masing-masing bank penerbit. URL spesifik dapat berubah — gunakan kata kunci pencarian seperti *"tarif BI-FAST resmi"*, *"biaya ATM Bersama transfer"*, atau cek pengumuman tarif di internet banking bank Anda untuk angka terbaru saat di lapangan.

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

Setelah menyelesaikan kelima latihan, cek apakah Anda dapat menjawab pertanyaan-pertanyaan berikut dengan kalimat Anda sendiri:

- [ ] Saya memahami mengapa Bahasa Indonesia cenderung lebih banyak token dibanding Bahasa Inggris.
- [ ] Saya mampu menyusun prompt yang memaksa model jujur saat tidak tahu jawaban.
- [ ] Saya tahu kapan harus memilih Haiku, Sonnet, atau Opus.
- [ ] Saya menyadari bahwa context window panjang tidak otomatis berarti akurasi sempurna.
- [ ] Saya akan selalu memilah: ini pertanyaan yang butuh **reasoning** atau **recall** — dan menyiapkan konteks yang sesuai.

---

## Pengumpulan & Tindak Lanjut

- Foto/screenshot output dari Latihan 1, 3, dan 4 silakan unggah ke channel pelatihan dengan format `M1-L[1/3/4]-NamaAnda.png`.
- Refleksi tertulis (1 paragraf) tentang **use case AI di pekerjaan Anda dan model Claude yang cocok untuknya** akan menjadi referensi pribadi Anda saat masuk ke Module 5 (Prompt for Business Use Cases) di Day 2.

> **Penutup**: Module 1 sengaja membatasi diri ke pemahaman cara kerja LLM. Mulai Module 2, Anda akan masuk ke **prompt craft** — bagaimana menulis instruksi yang membuat model bekerja sesuai keinginan Anda secara konsisten.
