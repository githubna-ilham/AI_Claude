# Module 1 — Mengenal LLM & Claude

**Durasi belajar**: ±90 menit
**Posisi**: Modul pembuka Day 1
**Format**: Baca konsep → coba sendiri → refleksi

---

## Apa yang Akan Anda Bisa Setelah Modul Ini

Setelah selesai membaca dan mempraktikkan modul ini, Anda akan mampu:

1. **Menjelaskan** cara kerja LLM menggunakan analogi yang masuk akal, tanpa perlu memahami rumus matematika.
2. **Memilih** model Claude yang tepat (Opus, Sonnet, atau Haiku) sesuai kebutuhan: mana yang cepat, mana yang ekonomis, mana yang paling cerdas.
3. **Mengenali** empat keterbatasan utama LLM (halusinasi, batas pengetahuan, batas memori, dan bias) serta cara mengatasinya melalui prompt.
4. **Memutuskan** kapan sebaiknya menggunakan model "pemikir" dibanding model "cepat" untuk kebutuhan bisnis Anda.

---

## 1. Apa Itu LLM?

**LLM (Large Language Model)** pada intinya adalah **mesin penebak kata berikutnya — dalam skala raksasa**.

Bayangkan fitur *autocomplete* pada keyboard ponsel Anda. Ketika Anda mengetik "selamat", ponsel menebak kata berikutnya: "pagi", "siang", "malam", atau "datang". LLM bekerja dengan prinsip yang sama, hanya saja **jauh lebih besar dan jauh lebih memahami konteks**. LLM tidak hanya menebak satu kata, melainkan terus-menerus menebak kata demi kata hingga membentuk paragraf, esai, bahkan kode program.

Namun jika LLM hanya "autocomplete raksasa", mengapa ia mampu menulis esai dan menjawab pertanyaan rumit? Karena terdapat **tiga ciri khas** yang membuatnya jauh lebih unggul dari autocomplete biasa.

### Ciri Khas #1 — Skala Pengetahuan yang Sangat Luas

- **Autocomplete ponsel**: hanya mempelajari pola dari pesan-pesan yang pernah Anda ketik sebelumnya.
- **LLM**: dilatih dari **triliunan kata** — mencakup seluruh Wikipedia, jutaan buku, miliaran baris kode program, artikel berita, dan forum diskusi.

**Dampaknya**: LLM mengetahui banyak hal, mulai dari resep rendang hingga sintaks Python, karena pernah membaca semuanya. Ibarat seseorang yang telah membaca seluruh isi perpustakaan terbesar di dunia.

### Ciri Khas #2 — Mampu Belajar dari Contoh dalam Prompt *(in-context learning)*

- **Autocomplete ponsel**: tidak dapat Anda ajari hal baru secara langsung. Polanya tetap, tidak berkembang.
- **LLM**: Anda cukup memberikan **2–3 contoh** dalam prompt, dan model langsung memahami pola yang Anda inginkan — tanpa perlu dilatih ulang dari awal.

**Contoh nyata**: misalnya Anda ingin model mengubah judul menjadi gaya formal. Cukup tulis:

```
Ubah judul berikut menjadi gaya formal:
"Cara cepat menjadi kaya" → "Strategi Akumulasi Kekayaan yang Efisien"
"Tips diet ampuh" → "Panduan Penurunan Berat Badan yang Efektif"
"Trik mempercepat belajar" →
```

Model akan langsung memahami polanya dan melanjutkan dengan: `"Teknik Optimalisasi Proses Pembelajaran"`. Padahal Anda tidak pernah mengajarkan istilah "gaya formal" secara eksplisit — model memahaminya hanya dari **dua contoh** di atas.

### Ciri Khas #3 — Mampu Mengikuti Instruksi Bahasa Manusia *(instruction following)*

- **Autocomplete ponsel**: tidak memahami perintah seperti "tolong ringkas pesan ini menjadi 3 poin". Ia hanya menebak kata berikutnya, bukan menjalankan perintah.
- **LLM**: setelah dilatih khusus dengan jutaan contoh pasangan "instruksi → jawaban yang benar", model menjadi paham bahwa kalimat seperti:

```
Ringkas paragraf ini menjadi 3 poin dengan bahasa formal.
```

…adalah sebuah perintah yang harus dijalankan, bukan sekadar kalimat yang perlu dilanjutkan. Inilah yang membuat LLM dapat berfungsi sebagai "asisten" — Anda memberi instruksi, model menjalankannya.

---

**Kesimpulannya**: secara teknis, LLM melakukan hal yang sama dengan autocomplete ponsel — menebak kata berikutnya. Yang membedakan adalah: (1) pengetahuannya yang jauh lebih luas, (2) kemampuan beradaptasi dari contoh dalam prompt, dan (3) kemampuan mengikuti instruksi natural manusia. Tiga hal inilah yang membuat LLM terasa "cerdas".

### Alur Kerja Sederhana

```mermaid
flowchart LR
    A[Teks Anda<br/>'Apa ibu kota Indonesia?'] --> B[Tokenizer<br/>Pecah jadi potongan kecil]
    B --> C[Token IDs<br/>Angka unik tiap potongan]
    C --> D[Embedding<br/>Ubah jadi koordinat]
    D --> E[Transformer<br/>Memahami konteks]
    E --> F[Hitung probabilitas<br/>kata berikutnya]
    F --> G[Pilih satu kata]
    G -->|loop sampai selesai| C
    G --> I[Jawaban final<br/>'Jakarta']
```

Tiga hal penting yang perlu Anda ingat:

- **LLM tidak benar-benar "memahami"** seperti manusia. Yang dilakukan adalah menghitung probabilitas: "kata apa yang paling mungkin muncul setelah ini?"
- **LLM tidak memiliki memori antar percakapan** *(stateless)*. Setiap kali Anda mengirim pesan, seluruh konteks harus disertakan kembali. Ibarat berbicara dengan seseorang yang kehilangan ingatan setiap satu menit — Anda harus selalu mengingatkan apa topik pembicaraan sebelumnya.
- **LLM tidak selalu memberikan jawaban yang sama** *(non-deterministik)*. Pertanyaan yang sama, jika diajukan dua kali, dapat menghasilkan jawaban berbeda. Hal ini merupakan fitur, bukan kesalahan — kecuali Anda secara sengaja mengaturnya agar deterministik.

---

## 2. Transformer — "Mesin" di Balik LLM

**Transformer** adalah arsitektur (semacam cetak biru) yang menjadi dasar bagi seluruh LLM modern. Diperkenalkan pada tahun 2017 melalui paper berjudul *"Attention Is All You Need"*.

Anda tidak perlu memahami matematikanya secara mendalam. Cukup pahami **analogi rapat tim** berikut:

> Bayangkan setiap kata dalam kalimat Anda adalah seorang peserta rapat. Untuk memahami konteks, setiap peserta **mendengarkan seluruh peserta lain** secara bersamaan, kemudian memberi bobot: "siapa yang paling relevan untuk saya saat ini?". Mekanisme inilah yang disebut **Self-Attention** — komponen jantung dari Transformer.

Itulah alasan mengapa Claude mampu memahami konteks panjang. Ketika Anda memberikan dokumen 50 halaman lalu bertanya tentang isi halaman 47, model dapat "melihat kembali" seluruh halaman secara serempak dan memfokuskan perhatian pada bagian yang relevan.

Komponen-komponen lainnya (sebagai pengenalan istilah):

| Istilah | Fungsi singkat |
|---------|---------------|
| **Token Embedding** | Mengubah kata menjadi koordinat angka agar dapat diproses komputer |
| **Positional Encoding** | Menandai posisi: "kata ini di awal", "kata itu di tengah" |
| **Self-Attention** | Mekanisme rapat seperti dijelaskan di atas |
| **Feed-Forward** | Lapisan pemrosesan tambahan |
| **Output Head** | Lapisan pengambil keputusan: kata apa berikutnya? |

---

## 3. Token & Context Window — Konsep yang Wajib Dipahami

### Apa Itu Token?

LLM tidak membaca kalimat per kalimat atau kata per kata. Ia membaca **token** — potongan-potongan teks yang dapat berupa kata utuh, suku kata, atau bahkan satu huruf.

| Teks yang Anda tulis | Perkiraan jumlah token |
|----------------------|------------------------|
| `Hello` | 1 token |
| `Halo` | 1 token |
| `Multimatics` | 3–4 token (dipecah menjadi `Multi` + `matics`) |
| `claude-sonnet-4-5` | 5–6 token |
| 1 kalimat Bahasa Indonesia (10 kata) | 15–25 token |

**Rumus praktis yang berguna**:
- 1 token ≈ 4 huruf bahasa Inggris ≈ 3/4 kata
- Bahasa Indonesia umumnya **menggunakan 20–30% lebih banyak token** dibanding bahasa Inggris.

**Mengapa hal ini penting?** Karena ketika menggunakan API, Anda **dibayar berdasarkan jumlah token**. Kalimat yang panjang berarti jumlah token yang banyak, yang berujung pada biaya yang lebih tinggi.

### Apa Itu Context Window?

**Context window** adalah "kapasitas memori jangka pendek" model, yaitu total token (input + output) yang dapat diproses dalam **satu kali pengiriman pesan**.

| Model | Context Window | Catatan |
|-------|---------------|---------|
| Claude Haiku | 200.000 token | Cepat & ekonomis |
| Claude Sonnet | 200.000 (hingga 1 juta untuk tier khusus) | Pilihan serbaguna |
| Claude Opus | 200.000 (hingga 1 juta untuk tier khusus) | Reasoning terbaik |

**Analogi**: bayangkan context window sebagai **meja kerja** model. 200.000 token berarti meja yang sangat luas, mampu menampung buku-buku tebal sekaligus. Namun jika Anda meletakkan terlalu banyak buku, meja akan penuh dan model harus mulai mengabaikan yang lebih lama.

**Implikasi praktisnya**:
- Dokumen yang sangat panjang (misalnya PDF 500 halaman) yang melebihi context window perlu **dipecah** *(chunking)* atau diringkas terlebih dahulu.
- Semakin banyak token input, semakin tinggi biaya dan semakin lambat respons. Prinsipnya: **menghemat konteks berarti menghemat biaya**.

---

## 4. Claude — Kapabilitas dan Keterbatasan

### Keluarga Model Claude

Claude memiliki tiga varian utama. Ibarat menu di restoran: tersedia paket hemat, paket reguler, dan paket premium.

| Model | Cocok untuk | Kecepatan | Biaya |
|-------|------------|-----------|-------|
| **Haiku** | Pekerjaan ringan dan bervolume tinggi: klasifikasi email, penandaan artikel, ekstraksi data sederhana | Sangat cepat | Ekonomis ($) |
| **Sonnet** | Chatbot customer service, coding, RAG, agent umum | Cepat | Menengah ($$) |
| **Opus** | Tugas berat: analisis riset, perencanaan multi-langkah, pemecahan masalah kompleks | Lebih lambat | Premium ($$$) |

**Panduan pemilihan**:
- Tugas berulang, sederhana, dan bervolume tinggi → **Haiku**
- Mayoritas kebutuhan enterprise → **Sonnet** (titik optimal)
- Membutuhkan kemampuan reasoning terbaik → **Opus**

### Kemampuan Inti Claude

- Menulis teks panjang: artikel, laporan, email, kode program.
- Memahami berbagai bahasa, termasuk Bahasa Indonesia dengan baik.
- Berpikir bertahap (terutama Opus).
- Memahami gambar *(vision)* — untuk varian multimodal.
- Menggunakan alat bantu eksternal *(tool use)* — akan dibahas pada Day 3.

### Keterbatasan yang Wajib Dipahami

Bagian ini sangat penting untuk Anda pahami sebelum menggunakan Claude untuk pekerjaan produksi:

| Keterbatasan | Wujud nyata | Cara mengatasi melalui prompt |
|--------------|-------------|-------------------------------|
| **Halusinasi** | Mengarang fakta, membuat sitasi palsu yang tampak kredibel | Sertakan sumber asli; instruksikan model untuk mengaku "tidak tahu" jika informasi tidak tersedia |
| **Knowledge cutoff** | Tidak mengetahui peristiwa setelah tanggal pelatihan | Sertakan informasi terbaru melalui prompt atau alat pencarian |
| **Context window terbatas** | Konteks yang terlalu panjang akan dipotong | Ringkas atau pecah dokumen menjadi bagian-bagian kecil |
| **Bias** | Mencerminkan bias dari data internet | Audit output, sertakan instruksi netralitas secara eksplisit |
| **Tidak konsisten** | Jawaban berbeda pada percobaan yang berbeda | Atur `temperature=0`, lakukan evaluasi pada banyak sampel |
| **Lemah pada perhitungan rumit** | Salah aritmatika padahal tampak yakin | Minta model berpikir bertahap, atau delegasikan ke kalkulator |

---

## 5. Reasoning & Halusinasi — Dua Konsep Kunci

### Apa Sebenarnya "Reasoning" pada LLM?

Ketika orang menyebut "Claude mampu reasoning", maksudnya **bukan** model benar-benar berpikir layaknya seorang matematikawan profesional. Yang sebenarnya terjadi: Claude **menghasilkan rangkaian kata yang menyerupai langkah-langkah berpikir manusia**.

Analoginya seperti seorang murid pintar yang menuliskan langkah "diketahui... ditanya... jawab..." pada kertas — bukan karena memahami hakikat matematika, melainkan karena mengenali pola jawaban yang umumnya benar dari ribuan contoh yang pernah dipelajari.

Claude Opus, terutama dengan mode *extended thinking*, dilatih khusus agar rantai berpikir ini **lebih panjang, lebih konsisten, dan dapat diaudit**.

### Mengapa LLM Sering "Mengarang" (Halusinasi)?

Karena tugas dasar LLM adalah **"melanjutkan kalimat dengan probabilitas tertinggi"** — bahkan ketika seharusnya model menyatakan "saya tidak tahu". Halusinasi sering muncul karena beberapa faktor:

- Prompt Anda **ambigu** atau kurang detail.
- Anda meminta fakta **spesifik** yang tidak ada dalam data pelatihan.
- Anda memaksa format tertentu (misal: "buatkan tabel dengan 10 baris") sehingga model terpaksa mengisi sel kosong dengan tebakan.

**Empat strategi anti-halusinasi pada level prompt**:

1. **Grounding (menyertakan sumber)**: lampirkan teks asli, lalu instruksikan model untuk "menjawab hanya berdasarkan teks di atas".
2. **Izin untuk mengaku tidak tahu**: "jika informasi tidak tersedia di sumber, tulis `INFO_TIDAK_TERSEDIA`".
3. **Memaksa kutipan**: "kutip kalimat yang persis dari sumber sebelum menyimpulkan".
4. **Berpikir bertahap** *(chain-of-thought)*: minta model menjelaskan logikanya sebelum memberi jawaban akhir.

---

## Praktik Mandiri (15 menit)

Daripada hanya membaca teori, **buka claude.ai sekarang** dan jalankan empat eksperimen berikut. Tujuannya adalah agar Anda merasakan sendiri perbedaan antara prompt biasa dan prompt yang ditulis dengan benar.

### Eksperimen A — Bertanya Tanpa Sumber

Buka **claude.ai**, pilih model Sonnet, lalu kirim:

```
Siapa CEO Multimatics saat ini dan kapan beliau menjabat?
```

Amati jawabannya. Apakah model mengarang? Atau secara jujur menyatakan tidak tahu? Catat respons yang Anda dapatkan.

### Eksperimen B — Bertanya dengan Sumber

Kunjungi website Multimatics, salin satu paragraf "About Us", lalu kirim:

```
Berdasarkan teks di atas saja, siapa CEO Multimatics dan kapan menjabat?
Jika tidak disebut dalam teks, jawab "TIDAK DISEBUTKAN".
```

Bandingkan dengan hasil Eksperimen A. Apa perbedaannya?

### Eksperimen C — Menghitung Token

Buka https://platform.openai.com/tokenizer, ketik nama Anda dan beberapa kata Bahasa Indonesia. Lihat jumlah token yang terhitung — ini akan menjadi dasar perhitungan biaya saat Anda menggunakan API.

### Eksperimen D — Membandingkan Tiga Model Claude

Buka https://console.anthropic.com (Workbench), jalankan satu soal logika cerita yang sama pada **Haiku, Sonnet, dan Opus**. Bandingkan: model mana yang paling cepat? Mana yang paling masuk akal? Berapa selisih biayanya?

**Refleksi**: mengapa jawabannya berbeda? Apa implikasinya terhadap pilihan model Anda di pekerjaan nyata?

---

## Contoh Konkret: Prompt Kurang Baik → Baik → Lebih Baik

Tiga contoh berikut menunjukkan **evolusi cara menulis prompt**, dari yang seadanya hingga yang siap produksi.

### Contoh 1 — Pertanyaan Faktual

```text
[KURANG BAIK]
Jelaskan tentang regulasi perlindungan data di Indonesia.
```
Masalah: tidak ada batasan waktu, sumber, maupun format. Risiko halusinasi tinggi.

```text
[BAIK]
Jelaskan UU Perlindungan Data Pribadi (UU PDP) Indonesia No. 27 Tahun 2022.
Fokus pada: definisi data pribadi, hak subjek data, dan sanksi.
Jika ada poin yang tidak yakin, tandai dengan [UNCERTAIN].
```
Lebih baik: batasan sudah jelas, model diizinkan mengakui keraguan.

```text
[LEBIH BAIK]
<sumber>
{tempel teks UU PDP pasal 1, 4-16, 57-67 di sini}
</sumber>

Berdasarkan <sumber> di atas saja, jelaskan dalam 5 bullet:
1. Definisi data pribadi (Pasal berapa?)
2. 3 hak utama subjek data
3. Sanksi administratif vs pidana

Format: bullet markdown, sertakan referensi pasal di akhir tiap poin.
Jika informasi tidak ada di <sumber>, tulis "TIDAK ADA DI SUMBER".
```
Mengapa lebih baik: sumber jelas, model diizinkan mengaku tidak tahu, format terstruktur, dan wajib mencantumkan pasal.

### Contoh 2 — Membuat Ringkasan

```text
[KURANG BAIK]
Ringkas dokumen ini.
```

```text
[BAIK]
Ringkas dokumen ini menjadi 3 paragraf untuk audiens eksekutif.
```

```text
[LEBIH BAIK]
Anda adalah analis bisnis senior. Ringkas dokumen <doc> di bawah untuk
CFO yang tidak memiliki waktu membaca detail teknis.

Format output:
- Paragraf 1: Konteks dan masalah (maks 60 kata)
- Paragraf 2: Temuan utama (3 bullet, angka penting di-bold)
- Paragraf 3: Rekomendasi dan risiko (maks 80 kata)

Hindari jargon teknis. Jika ada angka, sertakan satuan.
```

### Contoh 3 — Klasifikasi Tiket Support

```text
[KURANG BAIK]
Tiket ini tentang apa: "Aplikasi crash setiap saya buka menu profil"
```

```text
[BAIK]
Klasifikasikan tiket berikut ke salah satu kategori: Bug, Feature Request, Question.
Tiket: "Aplikasi crash setiap saya buka menu profil"
```

```text
[LEBIH BAIK]
Anda adalah triager tim support tier-1. Klasifikasikan tiket ke salah satu:
- BUG (error fungsional / crash)
- FEATURE_REQUEST (permintaan fitur baru)
- QUESTION (cara penggunaan)
- COMPLAINT (keluhan kepuasan, bukan teknis)

Output dalam JSON:
{"category": "...", "severity": "low|medium|high|critical", "rationale": "<=20 kata"}

Tiket: "Aplikasi crash setiap saya buka menu profil"
```

---

## Latihan & Refleksi

Modul 1 ini bersifat **konseptual** — belum disertai lab coding. Namun sebelum melanjutkan ke Module 2, pastikan Anda mampu menjawab lima pertanyaan refleksi berikut. Anda dapat menuliskan jawaban di buku catatan, atau mendiskusikannya dengan rekan:

1. Jika Claude pada dasarnya adalah "mesin penebak kata berbasis probabilitas", **apa konsekuensinya** terhadap cara Anda menulis instruksi?
2. **Kapan** Anda akan memilih Haiku (lebih ekonomis dan cepat) dibanding Sonnet untuk pekerjaan Anda?
3. Sebutkan **satu pekerjaan harian** Anda yang berisiko jika LLM-nya berhalusinasi. Bagaimana cara mengantisipasinya?
4. **Mengapa** context window yang besar tidak otomatis menghasilkan jawaban yang lebih baik?
5. Apa perbedaan **"reasoning" pada LLM dan reasoning pada manusia** menurut pemahaman Anda saat ini?

Untuk diskusi kelompok yang lebih terstruktur, lihat [`diskusi.md`](./diskusi.md).

---

## Bacaan Lanjutan

- Anthropic — *Introduction to Claude*: https://docs.anthropic.com/en/docs/intro-to-claude
- Anthropic — *Models overview*: https://docs.anthropic.com/en/docs/about-claude/models
- Anthropic — *Glossary*: https://docs.anthropic.com/en/docs/resources/glossary
- *Attention Is All You Need* (Vaswani et al., 2017): https://arxiv.org/abs/1706.03762
- Anthropic — *Constitutional AI*: https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback
- Anthropic — *Reducing hallucinations*: https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
