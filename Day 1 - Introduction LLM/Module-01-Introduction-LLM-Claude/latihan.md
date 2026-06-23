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

## Latihan 3 — Pilih Model Claude untuk Skenario Jalin (6 menit)

Bayangkan: Anda anggota tim AI Lab Jalin. Atasan Anda baru saja meminta rekomendasi model Claude untuk 3 ide fitur AI internal yang akan masuk roadmap. Latihan ini melatih **keputusan**, bukan riset — Anda akan berlatih memilih model dengan cepat berdasarkan profil use case, persis seperti yang akan Anda lakukan di rapat tim sungguhan.

### Bagian 1 — Cheat Sheet 30 Detik

Hafal pola sederhana ini sebelum memutuskan apapun:

| Model      | Kecepatan      | Kualitas reasoning  | Harga relatif (vs Sonnet) | Sweet spot                                        |
| ---------- | -------------- | ------------------- | ------------------------- | ------------------------------------------------- |
| **Haiku**  | Paling cepat   | Cukup               | ~1/4×                     | Volume tinggi, task pendek dan terstandar         |
| **Sonnet** | Sedang         | Tinggi              | 1× (baseline)             | Default workhorse untuk hampir semua use case     |
| **Opus**   | Paling lambat  | Sangat tinggi       | ~5×                       | Dokumen panjang, reasoning rumit, stakes tinggi   |

> 💡 **Aturan praktis cepat**: kalau ragu, pilih **Sonnet** dulu. Turunkan ke Haiku kalau volume tinggi dan task sederhana. Naikkan ke Opus hanya kalau Sonnet gagal di benchmark Anda sendiri.

### Bagian 2 — Pilih Model untuk 3 Skenario Jalin (3 menit)

Untuk masing-masing skenario, **tulis 1 baris saja**: model pilihan + alasan 1 kalimat. Tidak perlu mencari angka — pakai intuisi dari cheat sheet di atas.

**Skenario A — Auto-Tagging Notifikasi Transaksi**
> Tim CS ingin notifikasi push ("Transfer Rp X ke Bank Y berhasil") di-tag otomatis ke salah satu dari 5 kategori: `TRANSFER_SUKSES`, `TRANSFER_GAGAL`, `TARIK_TUNAI`, `DISPUTE`, `LAINNYA`. Volume: **50.000 notifikasi per hari**. Input: 1 kalimat. Output: 1 label.

→ Model: ____________  | Alasan: __________________________________

**Skenario B — Asisten Internal SOP**
> Staff CS sering bingung mencari prosedur penanganan dispute di dokumen SOP. Tim ingin chat assistant internal yang membaca SOP (25 halaman) dan menjawab pertanyaan staff dengan akurat. Volume: ~200 query per hari. Input: pertanyaan + seluruh SOP. Output: jawaban pendek dengan kutipan.

→ Model: ____________  | Alasan: __________________________________

**Skenario C — Analisis Root Cause Incident Switching**
> Saat terjadi lonjakan failure rate di jaringan switching, network engineer butuh "asisten analis" yang membaca log error (~30 menit, 40.000 baris) + konfigurasi route + tren trafik, lalu mengusulkan hipotesis penyebab utama. Volume: **1–2 kali per minggu** saat ada insiden. Input: dokumen besar (50.000+ token). Output: paragraf analisis terstruktur.

→ Model: ____________  | Alasan: __________________________________

### Bagian 3 — Validasi Cepat di claude.ai (3 menit)

Buka **claude.ai** dan jalankan **versi mini Skenario A** berikut untuk merasakan output model default (Sonnet):

```
Klasifikasikan setiap notifikasi berikut ke salah satu kategori:
TRANSFER_SUKSES, TRANSFER_GAGAL, TARIK_TUNAI, DISPUTE, LAINNYA.

Output: kembalikan dalam format "no. notifikasi → kategori".

1. "Transfer Rp 2.000.000 ke Bank Mandiri berhasil. Saldo: Rp 5.123.000"
2. "Tarik tunai Rp 500.000 di ATM Link berhasil. Biaya: Rp 7.500"
3. "Maaf, transfer Anda gagal karena melewati batas harian"
4. "Saya komplain, transfer Rp 1jt tadi gagal tapi saldo terdebit"
5. "Selamat! Anda mendapat cashback Rp 50.000"
```

Amati output. Lalu tanya diri sendiri:
- Apakah outputnya **rapi dan konsisten**? Kalau iya → bisa jadi Sonnet sudah overkill, **Haiku** kemungkinan besar sanggup juga.
- Apakah masih ada satu yang salah klasifikasi (mis. nomor 5)? Kalau iya → Anda butuh prompt yang lebih ketat (bahasan Module 2), **bukan** naik ke Opus.

### Pertanyaan Refleksi (kerjakan setelah pelatihan)

1. Untuk Skenario A (50.000/hari): kira-kira berapa biaya per bulan kalau pakai **Haiku** vs **Sonnet**? Tidak perlu angka eksak — cukup "kira-kira beda berapa kali lipat".
2. Adakah use case di tim Anda sendiri yang **mirip Skenario C** (low-volume tapi high-stakes reasoning)? Sebutkan satu.
3. Kalau atasan Anda meminta "**satu model default** untuk semua proof-of-concept AI Jalin di kuartal ini", mana yang Anda usulkan dan kenapa?

---

> 🎯 **Kunci jawaban (untuk fasilitator / self-check)**:
> - **Skenario A → Haiku.** Volume tinggi, task pendek dan terstandar, cocok untuk model murah dan cepat.
> - **Skenario B → Sonnet.** Q&A dokumen butuh reasoning yang andal tapi tidak ekstrem. Sonnet default workhorse.
> - **Skenario C → Opus.** Dokumen panjang, jarang dipakai, dan keputusan downstream-nya penting. Trade-off harga pantas dibayar.
>
> Tidak ada jawaban "salah mutlak" — yang penting Anda bisa **menjelaskan reasoning Anda**.

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
