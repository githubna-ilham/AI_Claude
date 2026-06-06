# Module 1 — Mengenal LLM & Claude

**Durasi belajar**: ±90 menit
**Posisi**: Modul pembuka Day 1
**Format**: Baca konsep → coba sendiri → refleksi

---

## Apa yang Akan Anda Bisa Setelah Modul Ini

Setelah selesai membaca dan mempraktikkan modul ini, Anda akan bisa:

1. **Menjelaskan** bagaimana LLM bekerja — pakai analogi yang masuk akal, tidak perlu rumus.
2. **Memilih** model Claude yang tepat (Opus, Sonnet, Haiku) sesuai kebutuhan — mana yang cepat, mana yang murah, mana yang pintar.
3. **Mengenali** 4 keterbatasan utama LLM (ngarang, info kadaluarsa, batas memori, bias) dan cara mengatasinya lewat prompt.
4. **Memutuskan** kapan harus pakai model "pemikir" vs model "cepat" untuk kasus bisnis Anda sendiri.

---

## 1. Apa Itu LLM?

**LLM (Large Language Model)** itu intinya adalah **mesin tebak kata berikutnya — versi raksasa**.

Bayangkan fitur *autocomplete* di keyboard HP Anda. Saat Anda mengetik "selamat", HP menebak kata berikutnya: "pagi", "siang", "malam", "datang". LLM bekerja persis seperti itu — hanya saja **jauh lebih besar dan jauh lebih pintar konteks**. Ia tidak hanya menebak 1 kata, tapi terus-menerus menebak kata demi kata sampai membentuk paragraf, esai, bahkan kode program.

Tapi kalau LLM cuma "autocomplete raksasa", kenapa bisa nulis esai dan jawab pertanyaan rumit? Karena ada **3 hal yang bikin dia jauh lebih hebat** dari autocomplete HP:

### Ciri Khas #1 — Skala Raksasa (banyak banget yang sudah "dibaca")

- **Autocomplete HP**: hanya hafal pola dari pesan-pesan yang pernah Anda ketik.
- **LLM**: dilatih dari **triliunan kata** — seluruh Wikipedia, jutaan buku, miliaran baris kode program, artikel berita, forum diskusi, dst.

**Akibatnya**: LLM "tahu" banyak hal — dari resep rendang sampai sintaks Python — karena pernah membaca semuanya. Ibarat seseorang yang sudah baca seluruh isi perpustakaan terbesar di dunia.

### Ciri Khas #2 — Bisa Belajar dari Contoh di Prompt *(in-context learning)*

- **Autocomplete HP**: tidak bisa Anda "ajari" hal baru di tempat. Pola lama, gitu-gitu aja.
- **LLM**: Anda kasih **2-3 contoh** di prompt, dia langsung paham pola yang Anda mau — tanpa perlu "dilatih ulang" dari nol.

**Contoh nyata**: kalau Anda mau dia ubah judul jadi gaya formal, cukup tulis:

```
Ubah judul berikut jadi gaya formal:
"Cara cepet kaya raya" → "Strategi Akumulasi Kekayaan yang Efisien"
"Tips diet ampuh" → "Panduan Penurunan Berat Badan yang Efektif"
"Trik nge-hack belajar" →
```

LLM langsung "nangkep" polanya dan lanjut: `"Teknik Optimalisasi Proses Pembelajaran"`. Padahal Anda tidak pernah ngajarin dia istilah "ubah ke formal" — dia paham hanya dari **2 contoh** di atas.

### Ciri Khas #3 — Bisa Diperintah dengan Bahasa Manusia *(instruction following)*

- **Autocomplete HP**: tidak ngerti kalau Anda ketik "tolong ringkas pesan ini jadi 3 poin" — dia cuma nebak kata berikutnya, bukan ngikutin perintah.
- **LLM**: setelah **dilatih khusus** dengan jutaan contoh pasangan "instruksi → jawaban yang benar", dia jadi paham kalau Anda nulis:

```
Ringkas paragraf ini jadi 3 poin pakai bahasa formal.
```

…dia benar-benar akan **ringkas jadi 3 poin** — bukan sekadar melanjutkan kalimat Anda. Inilah yang membuat LLM bisa dipakai sebagai "asisten" — Anda kasih instruksi, dia ikuti.

---

**Ringkasannya**: autocomplete HP cuma nebak kata berikutnya berbasis pola sederhana. LLM melakukan hal yang sama secara teknis, **tapi** dengan: (1) pengetahuan jauh lebih luas, (2) kemampuan adaptasi dari contoh di prompt, dan (3) kemampuan mengikuti instruksi natural manusia. Inilah yang membuatnya terasa "pintar".

### Bagaimana Cara Kerjanya? (Alur Sederhana)

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

Tiga hal penting untuk diingat:

- **LLM tidak benar-benar "mengerti"** seperti manusia. Ia menghitung peluang. "Kata apa yang paling mungkin muncul setelah ini?"
- **LLM tidak punya memori antar percakapan** *(stateless)*. Setiap kali Anda kirim pesan, semua konteks harus disertakan ulang. Ibarat ngobrol dengan orang yang amnesia setiap 1 menit — Anda harus selalu ngingetin "tadi kita lagi bahas X ya".
- **LLM tidak selalu kasih jawaban sama** *(non-deterministik)*. Tanya pertanyaan yang sama 2x, jawabannya bisa beda. Ini fitur, bukan bug — kecuali Anda sengaja set agar deterministik.

---

## 2. Transformer — "Mesin" di Balik LLM

**Transformer** adalah arsitektur (semacam blueprint) yang membuat LLM modern bisa eksis. Diperkenalkan tahun 2017 lewat paper berjudul *"Attention Is All You Need"*.

Anda tidak perlu paham matematikanya. Cukup paham **analogi rapat tim** ini:

> Bayangkan setiap kata di kalimat Anda adalah seorang peserta rapat. Saat mereka harus memahami konteks, setiap orang **mendengarkan semua peserta lain** sekaligus, lalu memberi bobot: "siapa yang paling relevan untuk saya saat ini?". Mekanisme inilah yang disebut **Self-Attention** — jantung dari Transformer.

Itulah kenapa Claude bisa memahami konteks panjang. Saat Anda kasih dokumen 50 halaman lalu nanya soal halaman 47, model bisa "melihat balik" semua halaman sekaligus dan fokus ke bagian yang relevan.

Komponen lainnya (sekadar untuk Anda tahu istilahnya):

| Istilah | Fungsi singkat |
|---------|---------------|
| **Token Embedding** | Ubah kata jadi koordinat angka, supaya komputer bisa "hitung" |
| **Positional Encoding** | Tandai posisi: "kata ini di awal", "kata itu di tengah" |
| **Self-Attention** | Mekanisme rapat yang sudah dijelaskan di atas |
| **Feed-Forward** | Lapisan pemrosesan tambahan |
| **Output Head** | Pengambil keputusan: kata apa berikutnya? |

---

## 3. Token & Context Window — Yang Wajib Dipahami

### Apa Itu Token?

LLM **tidak baca kalimat per kalimat** atau kata per kata. Ia baca **token** — potongan-potongan yang bisa berupa kata utuh, suku kata, atau bahkan satu huruf.

| Teks yang Anda tulis | Kira-kira jadi berapa token? |
|----------------------|------------------------------|
| `Hello` | 1 token |
| `Halo` | 1 token |
| `Multimatics` | 3–4 token (dipecah jadi `Multi` + `matics` dll.) |
| `claude-sonnet-4-5` | 5–6 token |
| 1 kalimat Bahasa Indonesia (10 kata) | 15–25 token |

**Rumus kasar yang berguna**:
- 1 token ≈ 4 huruf bahasa Inggris ≈ 3/4 kata
- Bahasa Indonesia umumnya **20-30% lebih boros token** dibanding Inggris

**Kenapa ini penting buat Anda?** Karena Anda **dibayar per token** saat pakai API. Kalimat panjang = token banyak = biaya tinggi.

### Apa Itu Context Window?

**Context window** = "kapasitas memori jangka pendek" model. Total token yang bisa diproses (input + output) dalam **satu kali kirim pesan**.

| Model | Context Window | Catatan |
|-------|---------------|---------|
| Claude Haiku | 200.000 token | Cepat & murah |
| Claude Sonnet | 200.000 (sampai 1 juta untuk tier khusus) | Kuda kerja serbaguna |
| Claude Opus | 200.000 (sampai 1 juta untuk tier khusus) | Pemikir terbaik |

**Analogi**: anggap context window itu **meja kerja** model. 200.000 token = meja super luas, bisa naro buku tebal di atasnya. Tapi kalau Anda taro 5 buku tebal sekaligus, mejanya penuh dan model harus mulai "membuang" yang lama.

**Implikasi praktisnya**:
- Dokumen super panjang (PDF 500 halaman) yang melebihi context window harus **dipotong-potong** *(chunk)* atau **diringkas dulu**.
- Semakin banyak token input → semakin mahal & semakin lambat. Jadi: **hemat konteks = hemat biaya**.

---

## 4. Claude — Apa Saja yang Bisa & Tidak Bisa

### Keluarga Model Claude

Claude punya 3 "varian" utama. Ibarat menu di restoran: ada paket hemat, paket reguler, paket premium.

| Model | Cocok untuk | Kecepatan | Biaya |
|-------|------------|-----------|-------|
| **Haiku** 🐰 | Pekerjaan ringan & banyak: klasifikasi email, tag artikel, ekstraksi data sederhana | Sangat cepat | Murah ($) |
| **Sonnet** 🐎 | Chatbot customer service, coding, RAG, agent biasa | Cepat | Sedang ($$) |
| **Opus** 🦉 | Tugas berat: analisis riset, perencanaan multi-langkah, problem solving kompleks | Lebih lambat | Mahal ($$$) |

**Rule of thumb**:
- Tugas berulang, simpel, volume tinggi → **Haiku**
- Mayoritas use case enterprise → **Sonnet** (sweet spot)
- Butuh "otak" terbaik untuk reasoning → **Opus**

### Yang Claude Bisa

- Tulis teks panjang: artikel, laporan, email, kode program
- Pahami banyak bahasa (Indonesia juga OK)
- Berpikir bertahap (terutama Opus)
- Baca gambar *(vision)* — untuk varian multimodal
- Pakai "alat bantu" eksternal *(tool use)* — akan dibahas hari ke-3

### Yang Claude TIDAK Bisa (atau Berisiko)

Ini bagian penting. **Wajib paham** sebelum pakai untuk pekerjaan beneran:

| Keterbatasan | Wujud nyatanya | Cara mengatasi lewat prompt |
|--------------|---------------|---------------------------|
| **Halusinasi** | Ngarang fakta, bikin sitasi palsu yang kelihatannya kredibel | Kasih sumber asli, suruh dia bilang "tidak tahu" kalau memang tidak ada |
| **Knowledge cutoff** | Tidak tahu kejadian setelah tanggal training-nya | Suplai info terbaru lewat prompt atau tool pencarian |
| **Context window terbatas** | Konteks kepanjangan akan dipotong | Ringkas dulu, atau potong jadi bagian-bagian |
| **Bias** | Mencerminkan bias dari data internet | Audit output, kasih instruksi netral secara eksplisit |
| **Tidak konsisten** | Jawaban beda di run yang berbeda | Set `temperature=0`, evaluasi banyak sampel |
| **Lemah hitung-hitungan rumit** | Salah aritmatika padahal kelihatan yakin | Suruh dia berpikir bertahap, atau delegasikan ke kalkulator |

---

## 5. Reasoning & Halusinasi — Dua Konsep Kunci

### "Reasoning" pada LLM Itu Apa?

Saat orang bilang "Claude bisa reasoning", maksudnya **bukan** dia benar-benar berpikir seperti matematikawan profesional. Yang sebenarnya terjadi: Claude **menghasilkan rangkaian kata yang menyerupai langkah-langkah berpikir manusia**.

Analoginya: seperti murid pintar yang menulis "diketahui... ditanya... jawab..." di kertas — bukan karena dia paham hakikat matematika, tapi karena dia tahu pola jawaban yang biasanya benar dari ribuan contoh yang pernah dia lihat.

Claude Opus (apalagi mode *extended thinking*) dilatih khusus agar rantai berpikir ini **lebih panjang, lebih konsisten, dan bisa diaudit**.

### Kenapa LLM Suka "Mengarang" (Halusinasi)?

Karena tugas dasar LLM adalah **"lanjutkan kalimat dengan probabilitas tertinggi"** — bahkan saat seharusnya dia bilang "saya tidak tahu". Halusinasi sering muncul karena:

- Prompt Anda **ambigu** atau kurang detail
- Anda minta fakta **spesifik** yang tidak ada di data training-nya
- Anda paksa format tertentu (misal: "buat tabel 10 baris") sehingga model **terpaksa ngisi** sel kosong dengan tebakan

**4 Senjata Anti-Halusinasi (level prompt)**:

1. **Grounding (kasih sumber)**: lampirkan teks asli, suruh "jawab hanya berdasarkan teks di atas"
2. **Izinkan mengaku tidak tahu**: "kalau info tidak ada di sumber, tulis `INFO_TIDAK_TERSEDIA`"
3. **Paksa kutip**: "kutip kalimat persis dari sumber sebelum menyimpulkan"
4. **Suruh berpikir bertahap** *(chain-of-thought)*: paksa model menjelaskan logika sebelum memberi jawaban final

---

## Coba Sendiri (15 menit)

Daripada hanya membaca teori, **buka claude.ai sekarang** dan ikuti 4 eksperimen berikut. Tujuannya: rasakan sendiri bedanya prompt biasa vs prompt yang ditulis dengan benar.

### Eksperimen A — Bertanya Tanpa Sumber

Buka **claude.ai**, pilih model Sonnet, lalu kirim:

```
Siapa CEO Multimatics saat ini dan kapan beliau menjabat?
```

Amati jawabannya. Apakah model ngarang? Atau jujur bilang tidak tahu? Catat respons Anda.

### Eksperimen B — Bertanya dengan Sumber

Kunjungi website Multimatics, copy 1 paragraf "About Us", lalu prompt:

```
Berdasarkan teks di atas saja, siapa CEO Multimatics dan kapan menjabat?
Kalau tidak disebut di teks, jawab "TIDAK DISEBUTKAN".
```

Bandingkan dengan Eksperimen A. Apa bedanya?

### Eksperimen C — Lihat Token dengan Mata Sendiri

Buka https://platform.openai.com/tokenizer, ketik nama Anda dan beberapa kata bahasa Indonesia. Lihat berapa token yang terhitung — ini akan jadi dasar perhitungan biaya saat Anda pakai API nanti.

### Eksperimen D — Bandingkan 3 Model Claude

Buka https://console.anthropic.com (Workbench), jalankan 1 soal logika cerita yang sama di **Haiku, Sonnet, dan Opus**. Bandingkan: jawaban siapa paling cepat? Siapa paling masuk akal? Berapa selisih biayanya?

**Refleksi**: kenapa jawabannya beda? Apa implikasinya buat pilihan Anda di pekerjaan nyata?

---

## Contoh Konkret: Prompt Jelek → Bagus → Lebih Bagus

Tiga contoh berikut menunjukkan **evolusi cara nulis prompt**, dari yang seadanya sampai yang siap produksi.

### Contoh 1 — Pertanyaan Faktual

```text
[JELEK]
Jelaskan tentang regulasi perlindungan data di Indonesia.
```
Masalah: tidak ada batas waktu, sumber, atau format. Risiko ngarang tinggi.

```text
[BAGUS]
Jelaskan UU Perlindungan Data Pribadi (UU PDP) Indonesia No. 27 Tahun 2022.
Fokus pada: definisi data pribadi, hak subjek data, sanksi.
Kalau ada poin yang Anda tidak yakin, tandai [UNCERTAIN].
```
Sudah mendingan: batasan jelas, model boleh ngaku ragu.

```text
[LEBIH BAGUS]
<sumber>
{tempel teks UU PDP pasal 1, 4-16, 57-67 di sini}
</sumber>

Berdasarkan <sumber> di atas saja, jelaskan dalam 5 bullet:
1. Definisi data pribadi (Pasal berapa?)
2. 3 hak utama subjek data
3. Sanksi administratif vs pidana

Format: bullet markdown, sebut pasal di akhir tiap poin.
Kalau info tidak ada di <sumber>, tulis "TIDAK ADA DI SUMBER".
```
Kenapa lebih bagus: sumber jelas, model boleh mengaku tidak tahu, format terstruktur, wajib sebut pasal.

### Contoh 2 — Membuat Ringkasan

```text
[JELEK]
Ringkas dokumen ini.
```

```text
[BAGUS]
Ringkas dokumen ini jadi 3 paragraf untuk audiens eksekutif.
```

```text
[LEBIH BAGUS]
Anda adalah analis bisnis senior. Ringkas dokumen <doc> di bawah untuk
CFO yang tidak punya waktu baca detail teknis.

Format output:
- Paragraf 1: Konteks & masalah (maks 60 kata)
- Paragraf 2: Temuan utama (3 bullet, angka penting di-bold)
- Paragraf 3: Rekomendasi & risiko (maks 80 kata)

Hindari jargon teknis. Kalau ada angka, sertakan satuan.
```

### Contoh 3 — Klasifikasi Tiket Support

```text
[JELEK]
Tiket ini tentang apa: "Aplikasi crash setiap saya buka menu profil"
```

```text
[BAGUS]
Klasifikasikan tiket berikut ke salah satu: Bug, Feature Request, Question.
Tiket: "Aplikasi crash setiap saya buka menu profil"
```

```text
[LEBIH BAGUS]
Anda adalah triager tim support tier-1. Klasifikasikan tiket ke salah satu:
- BUG (error fungsional / crash)
- FEATURE_REQUEST (minta fitur baru)
- QUESTION (cara penggunaan)
- COMPLAINT (keluhan kepuasan, bukan teknis)

Output dalam JSON:
{"category": "...", "severity": "low|medium|high|critical", "rationale": "<=20 kata"}

Tiket: "Aplikasi crash setiap saya buka menu profil"
```

---

## Latihan & Refleksi

Modul 1 ini sifatnya **konseptual** — belum ada lab coding. Tapi sebelum lanjut ke Module 2, pastikan Anda bisa menjawab 5 pertanyaan refleksi berikut (tulis jawaban Anda di buku catatan, atau diskusikan dengan teman sebelah):

1. Kalau Claude itu pada dasarnya "mesin tebak kata berbasis probabilitas", **apa konsekuensinya** terhadap cara Anda menulis instruksi?
2. **Kapan** Anda akan pilih Haiku (lebih murah & cepat) dibanding Sonnet untuk pekerjaan Anda?
3. Sebutkan **1 pekerjaan harian** Anda yang bisa berbahaya kalau LLM-nya ngarang. Apa cara mengantisipasinya?
4. **Kenapa** context window besar tidak otomatis = jawaban lebih bagus?
5. Apa beda **"reasoning" LLM vs "reasoning" manusia** menurut pemahaman Anda sekarang?

Untuk diskusi kelompok yang lebih terstruktur, lihat [`diskusi.md`](./diskusi.md).

---

## Bacaan Lanjutan

- Anthropic — *Introduction to Claude*: https://docs.anthropic.com/en/docs/intro-to-claude
- Anthropic — *Models overview*: https://docs.anthropic.com/en/docs/about-claude/models
- Anthropic — *Glossary*: https://docs.anthropic.com/en/docs/resources/glossary
- *Attention Is All You Need* (Vaswani et al., 2017): https://arxiv.org/abs/1706.03762
- Anthropic — *Constitutional AI*: https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback
- Anthropic — *Reducing hallucinations*: https://docs.anthropic.com/en/docs/test-and-evaluate/strengthen-guardrails/reduce-hallucinations
