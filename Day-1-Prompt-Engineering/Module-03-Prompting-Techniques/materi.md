# Module 3 — Prompting Techniques

**Durasi**: 90 menit
**Posisi**: Modul ketiga Day 1; memperluas anatomi (Module 2) ke teknik lanjutan.
**Mode**: Lecture + demo perbandingan + lab.

---

## Learning Outcomes

Setelah modul ini, peserta mampu:

1. **Membedakan** kapan menggunakan zero-shot, few-shot, dan chain-of-thought (CoT) berdasarkan kompleksitas task & ketersediaan contoh.
2. **Menyusun** prompt few-shot dengan contoh berkualitas tinggi (diverse, balanced, formatted).
3. **Memandu** model melalui reasoning step-by-step dan menangkap rantai berpikir untuk audit.
4. **Menerapkan** persona-based prompting dan structured prompting untuk skenario kompleks.
5. **Mengevaluasi** trade-off antara token cost, latency, dan akurasi untuk setiap teknik.

---

## 1. Pengantar — Spectrum Prompting

### Apa Itu Spectrum Prompting?

**Spectrum Prompting** adalah cara berpikir yang menempatkan berbagai teknik prompting dalam sebuah **rentang (spectrum)** — dari yang paling sederhana hingga paling kompleks. Tujuannya: agar Anda **tidak langsung menggunakan teknik kompleks** padahal teknik sederhana sudah cukup.

Analoginya seperti memilih alat di kotak peralatan: untuk memasang paku, Anda tidak perlu palu godam — palu kecil sudah cukup. Begitu pula dengan prompt: untuk task sederhana, jangan langsung pakai teknik berlapis-lapis. Mulailah dari yang paling ringan.

```mermaid
flowchart LR
    Z[Zero-Shot<br/>0 contoh] --> F[Few-Shot<br/>2-8 contoh]
    F --> C[Chain-of-Thought<br/>contoh + reasoning]
    C --> S[Structured<br/>multi-section, role-mixed]
    Z -.->|task sederhana| Z
    S -.->|task kompleks| S
```

### Mengapa Berpikir dalam Bentuk Spectrum?

Setiap teknik prompting memiliki **trade-off** antara tiga hal:

1. **Biaya token** — semakin banyak teks dalam prompt, semakin tinggi biaya API.
2. **Latency** — prompt yang lebih panjang membutuhkan waktu pemrosesan yang lebih lama.
3. **Akurasi & konsistensi** — teknik yang lebih kompleks umumnya menghasilkan output yang lebih konsisten untuk task yang rumit.

Jika Anda langsung memilih teknik paling kompleks, Anda **membayar biaya tinggi tanpa selalu mendapatkan hasil yang lebih baik**. Sebaliknya, jika Anda menggunakan teknik terlalu sederhana untuk task kompleks, akurasi akan rendah dan Anda akan terus mengulang prompt.

### Empat Tingkat dalam Spectrum

| Tingkat | Teknik | Karakteristik | Biaya |
|---------|--------|--------------|-------|
| **1** | **Zero-Shot** | Instruksi saja, tanpa contoh | Paling rendah |
| **2** | **Few-Shot** | Instruksi + 2 hingga 8 contoh input→output | Sedang |
| **3** | **Chain-of-Thought (CoT)** | Few-shot + minta model menjelaskan reasoning | Sedang–tinggi |
| **4** | **Structured Prompting** | Multi-section dengan peran, sumber, dan format yang dikombinasikan | Tertinggi |

Catatan penting: angka tingkat **bukan** tingkat kualitas. Tingkat 4 bukan otomatis "lebih baik" dari tingkat 1 — ia hanya **lebih cocok untuk task yang lebih kompleks**.

### Aturan Naik Tingkat

Pendekatan yang direkomendasikan: **mulai dari tingkat paling rendah, naik hanya jika hasilnya belum memadai.**

1. **Mulai dengan Zero-Shot.** Coba lebih dulu — paling cepat, paling murah, dan banyak task umum yang sudah berhasil di tingkat ini.
2. **Naik ke Few-Shot jika output tidak konsisten** atau format tidak sesuai harapan. Tambahkan 2–3 contoh untuk "mengunci" pola yang diinginkan.
3. **Naik ke Chain-of-Thought jika task membutuhkan penalaran multi-step** — misalnya kalkulasi bertahap, analisis kausalitas, atau pengambilan keputusan dengan beberapa kriteria.
4. **Naik ke Structured Prompting jika ada beberapa peran atau sumber** yang harus dikombinasikan — misalnya menggabungkan dokumen referensi, riwayat percakapan, dan aturan bisnis dalam satu prompt.

### Bagaimana Memutuskan Titik Awal?

Gunakan tiga pertanyaan diagnostik berikut:

| Pertanyaan | Jika "ya" | Mulai dari |
|-----------|-----------|-----------|
| Apakah task ini umum dan well-known (ringkasan, terjemahan, klasifikasi standar)? | Ya | **Zero-Shot** |
| Apakah ada format khusus atau taksonomi internal yang harus diikuti? | Ya | **Few-Shot** |
| Apakah task membutuhkan reasoning bertahap atau perhitungan yang dapat salah? | Ya | **Chain-of-Thought** |
| Apakah perlu menggabungkan beberapa peran (analis + reviewer) atau beberapa sumber dokumen? | Ya | **Structured** |

### Prinsip Penting

**Naik tingkat = naik biaya dan latency.** Karena itu, keputusan untuk naik tingkat harus berbasis **bukti dari evaluasi**, bukan asumsi. Module 4 (Structured Output & Evaluasi) akan membahas cara mengukur kualitas prompt secara objektif sehingga Anda tahu **kapan benar-benar perlu naik tingkat**, dan kapan teknik yang lebih sederhana sudah memadai.

Bagian selanjutnya akan membahas masing-masing tingkat secara mendalam.

---

## 2. Zero-Shot Prompting

Zero-shot = model diberi instruksi tanpa contoh. Modern LLM (Sonnet, Opus) sangat capable di zero-shot untuk task umum.

### Kapan dipakai

- Task umum yang well-documented (ringkasan, terjemahan, klasifikasi standar).
- Eksplorasi awal sebelum investasi waktu menulis contoh.
- Volume tinggi di mana setiap token contoh = biaya berlipat.

### Contoh

```text
Klasifikasikan sentimen kalimat berikut sebagai POSITIF, NEGATIF, atau NETRAL.

Kalimat: "Saya cukup puas dengan layanannya, walau pengiriman agak lambat."
Sentimen:
```

### Limitasi

- Performa drop pada domain-specific (medical, legal jargon, internal taxonomy).
- Variansi output lebih tinggi tanpa pattern anchor.

---

## 3. Few-Shot Prompting

Few-shot = prompt menyertakan **2–8 contoh** input→output. Model belajar pattern dari contoh (in-context learning).

### Prinsip Contoh yang Baik

| Prinsip      | Penjelasan                                                              |
|--------------|-------------------------------------------------------------------------|
| Diverse      | Cover edge case, bukan hanya kasus mudah.                               |
| Balanced     | Distribusi label seimbang (mis. positif/negatif/netral 1/1/1).          |
| Consistent   | Format input & output sama persis di semua contoh.                       |
| Realistic    | Mirror data produksi (panjang, gaya, noise).                            |
| Labeled clearly | Pakai delimiter konsisten (XML / `###` / newline).                   |

### Contoh Format

```text
Klasifikasikan sentimen kalimat sebagai POSITIF, NEGATIF, atau NETRAL.

<example>
Kalimat: "Produknya sangat membantu pekerjaan saya."
Sentimen: POSITIF
</example>

<example>
Kalimat: "Saya kecewa, fitur yang dijanjikan tidak ada."
Sentimen: NEGATIF
</example>

<example>
Kalimat: "Aplikasinya berfungsi seperti seharusnya."
Sentimen: NETRAL
</example>

<example>
Kalimat: "Bagus sih, tapi mahal."
Sentimen: NETRAL
</example>

Kalimat: "Awalnya senang, tapi setelah update jadi sering crash."
Sentimen:
```

### Trade-off

- Lebih banyak contoh ≠ selalu lebih baik. Setelah 5–8 contoh, marginal gain biasanya turun, tapi cost naik linear.
- Bias contoh = bias output. Jika 4 dari 5 contoh POSITIF, model condong POSITIF.

---

## 4. Chain-of-Thought (CoT) — Step-by-Step Reasoning

CoT = memaksa model menulis langkah berpikir sebelum jawaban akhir. Studi menunjukkan akurasi naik signifikan pada task matematika, logika, dan multi-hop reasoning.

### Pola

```text
{task description}

Pikirkan langkah demi langkah sebelum menjawab.

Jawaban akhir: ...
```

### Contoh

```text
Sebuah toko menjual 3 produk:
- Produk A: harga 50.000, terjual 12 unit
- Produk B: harga 75.000, terjual 8 unit
- Produk C: harga 100.000, terjual 5 unit

Berapa total revenue?

Pikirkan langkah demi langkah:
1. Hitung revenue per produk.
2. Jumlahkan total.

Jawaban akhir dalam format: "Total revenue: Rp X"
```

### CoT + Structured

Untuk audit, pisahkan reasoning dan jawaban:

```text
<thinking>
{model menulis reasoning di sini}
</thinking>

<answer>
{jawaban final}
</answer>
```

Ini memudahkan parsing dan logging untuk evaluasi.

### Catatan untuk Claude

- Claude **Extended Thinking** (Sonnet/Opus 4.x) menyediakan CoT native dengan budget yang dapat dikontrol. Tidak perlu prompt CoT manual untuk task kompleks — cukup aktifkan extended thinking di Console.
- Untuk Haiku, CoT manual via prompt tetap relevan.

---

## 5. Persona-Based Prompting

Persona-based = role prompting tingkat lanjut yang membentuk **karakter konsisten** lintas turn (multi-turn conversation).

### Komponen Persona

```text
<persona>
Nama: AskAura
Peran: Financial wellness coach untuk gig workers Indonesia
Karakter:
  - Empati tinggi, bahasa percakapan
  - Tidak menggurui, tidak judgmental
  - Selalu beri 1 action item konkret di akhir
Pengetahuan:
  - Familiar dengan platform Gojek, Grab, Maxim, Shopee Food
  - Memahami konsep budgeting 50/30/20
Larangan:
  - Tidak memberi rekomendasi investasi spesifik (compliance)
  - Tidak berbicara tentang politik atau agama
</persona>
```

### Use case
- Chatbot dengan brand voice konsisten.
- Persona untuk multiple "agen" dalam sistem yang sama (Day 3 — agentic patterns).

---

## 6. Structured Prompting

Structured prompting = prompt yang menggabungkan **multiple sections** dengan tag XML untuk skenario kompleks. Pattern ini menjadi tulang punggung Day 2–4.

### Template

```text
<system_context>
{deskripsi sistem & tujuan keseluruhan}
</system_context>

<persona>
{role + karakter}
</persona>

<knowledge_base>
{dokumen, glossary, FAQ}
</knowledge_base>

<examples>
<example>
<input>...</input>
<output>...</output>
</example>
</examples>

<task>
{instruksi spesifik untuk turn ini}
</task>

<rules>
{constraint}
</rules>

<output_format>
{schema}
</output_format>
```

### Keuntungan

- Setiap bagian dapat di-versioning terpisah.
- Mudah diubah menjadi template dinamis (variabel `{...}` diisi runtime).
- Mendukung observability — bagian mana yang berubah saat ada regression.

### Contoh Prompt — Structured Prompting dalam Praktik

Berikut tiga contoh yang menunjukkan kekuatan structured prompting untuk skenario yang benar-benar kompleks.

#### Contoh 1 — Customer Service Agent dengan Knowledge Base

Skenario: chatbot CS yang harus menjawab pertanyaan pelanggan **berdasarkan FAQ resmi**, mengikuti **persona yang konsisten**, dan **belajar dari contoh-contoh respons terbaik** yang dikurasi tim CS.

```text
<system_context>
Anda adalah asisten Customer Service untuk Toko Buku Online Cendekia.
Tujuan: menjawab pertanyaan pelanggan secara akurat, ramah, dan efisien
berdasarkan FAQ resmi. Jika di luar cakupan, eskalasi ke agen manusia.
</system_context>

<persona>
Nama: Asti.
Karakter: ramah, sabar, profesional, dan suka memberikan tips singkat
seputar buku. Sapa pelanggan dengan "Halo Kak". Tutup setiap balasan dengan
"Senang membantu Kak. Ada lagi yang bisa Asti bantu?"
</persona>

<knowledge_base>
FAQ Cendekia (versi 2025-06):

- Pengiriman reguler: 2-5 hari kerja. Express: 1-2 hari kerja (+Rp 25.000).
- Pembayaran: transfer bank, e-wallet (OVO, GoPay, Dana), kartu kredit.
- Pengembalian: maksimal 7 hari setelah barang diterima, kondisi masih segel.
- Buku diskon flash sale TIDAK dapat dikembalikan.
- Member Cendekia Plus: diskon 10% semua buku, gratis ongkir minimal pembelian Rp 200.000.
- Pelacakan paket: melalui email atau menu "Pesanan Saya" di akun pelanggan.
</knowledge_base>

<examples>
<example>
<input>Berapa lama pengirimannya kak?</input>
<output>
Halo Kak! Pengiriman reguler kami 2-5 hari kerja, sedangkan express 1-2 hari kerja
(tambahan ongkir Rp 25.000). Estimasi spesifik akan muncul saat checkout sesuai
alamat tujuan ya Kak.

💡 Tips: kalau pesannya buku tebal untuk weekend, pilih express biar sampai
tepat waktu.

Senang membantu Kak. Ada lagi yang bisa Asti bantu?
</output>
</example>

<example>
<input>Buku saya datang sobek di sampul, bisa dikembalikan?</input>
<output>
Halo Kak! Tentu bisa Kak. Untuk buku rusak saat pengiriman, silakan ajukan
pengembalian maksimal 7 hari setelah barang diterima. Lampirkan foto kondisi
buku dan resi pengiriman ya Kak.

Catatan: ketentuan ini tidak berlaku untuk buku diskon flash sale.

Senang membantu Kak. Ada lagi yang bisa Asti bantu?
</output>
</example>
</examples>

<task>
Pelanggan baru saja menulis:
"Halo, saya member cendekia plus mau order 3 buku totalnya 350rb, masih gratis ongkir ga?"
</task>

<rules>
- Jawab HANYA berdasarkan informasi di <knowledge_base>.
- Jika informasi tidak ada, jangan mengarang. Jawab: "Untuk hal ini Asti perlu
  bantu cek dulu Kak. Boleh Asti hubungkan dengan tim Cendekia agar dijawab lebih lengkap?"
- Pertahankan persona Asti — ramah, ada tips singkat jika relevan.
- Maksimal 100 kata.
</rules>

<output_format>
Balasan dalam format chat — tanpa tag XML, tanpa markdown header. Hanya teks
balasan yang siap dikirim ke pelanggan.
</output_format>
```

**Mengapa contoh ini bagus:**
- **`<knowledge_base>`** memberi sumber resmi → tidak ada halusinasi.
- **`<persona>`** memastikan suara brand konsisten.
- **`<examples>`** mengunci pola balasan (sapaan, tips, penutup).
- **`<rules>`** menyediakan **fallback** spesifik untuk kasus di luar knowledge base.

---

#### Contoh 2 — Analisis Kontrak Multi-Dokumen

Skenario: legal counsel meninjau **kontrak vendor baru** dengan membandingkan terhadap **kebijakan internal**, **riwayat negosiasi sebelumnya**, dan **standar industri**.

```text
<system_context>
Sistem ini membantu legal counsel menganalisis kontrak vendor IT.
Output akan digunakan sebagai bahan diskusi internal sebelum negosiasi final.
</system_context>

<persona>
Anda adalah senior legal counsel dengan 10+ tahun pengalaman di kontrak IT.
Pendekatan Anda: tegas pada risiko, namun konstruktif dalam memberikan jalan keluar.
</persona>

<knowledge_base>
DOKUMEN A — Kontrak Vendor (draft yang akan dianalisis):
{tempel teks draft kontrak vendor}

DOKUMEN B — Kebijakan Internal Pengadaan IT:
- Termin pembayaran maksimal 60 hari setelah serah terima.
- Garansi minimal 12 bulan untuk hardware, 6 bulan untuk software.
- Klausul force majeure WAJIB mencakup gangguan listrik dan internet.
- Penalti keterlambatan: 0,1% per hari, maksimal 5% dari nilai kontrak.
- Klausul kerahasiaan mengikat selama 5 tahun setelah kontrak berakhir.

DOKUMEN C — Riwayat Negosiasi dengan Vendor Sebelumnya:
- 2024: vendor X menolak klausul penalti 0,1%/hari, disepakati 0,05%/hari.
- 2024: vendor Y menyetujui semua klausul standar tanpa revisi.
- 2025 Q1: vendor Z meminta termin pembayaran 90 hari, ditolak.
</knowledge_base>

<task>
Lakukan analisis lengkap dalam 4 tahap:

1. ASESMEN: identifikasi semua klausul di DOKUMEN A yang berdeviasi dari DOKUMEN B.
2. KONTEKS: cocokkan deviasi dengan pola di DOKUMEN C — apakah vendor ini
   memiliki riwayat preseden?
3. PRIORITAS: kelompokkan deviasi ke tingkat risiko (TINGGI/SEDANG/RENDAH).
4. STRATEGI: rekomendasikan posisi negosiasi untuk tiap deviasi tingkat TINGGI.
</task>

<rules>
- Setiap temuan harus merujuk ke **pasal/section spesifik** di DOKUMEN A.
- Jika informasi yang dibutuhkan tidak ada di knowledge_base, tandai
  sebagai "PERLU KLARIFIKASI".
- Hindari saran yang menuntut perubahan struktural besar — fokus pada
  revisi klausul yang realistis dinegosiasikan.
</rules>

<output_format>
## Ringkasan Eksekutif
{paragraf, maksimal 100 kata}

## Tabel Deviasi & Risiko
| No | Pasal Kontrak | Deviasi dari Policy | Risk Level | Preseden Vendor |
|----|---------------|--------------------|-----------|----------------|

## Rekomendasi Negosiasi (Risk TINGGI saja)
1. **{topik}** — Posisi pembuka: ... | Posisi mundur acceptable: ...
2. ... (dst.)

## Item Perlu Klarifikasi
- ...
</output_format>
```

**Mengapa contoh ini bagus:**
- **Menggabungkan 3 sumber dokumen** (kontrak + policy + history) dalam satu prompt.
- **Task didekomposisi** menjadi 4 tahap yang membentuk reasoning chain.
- **Output format hibrida** (markdown + tabel) — siap dipakai langsung sebagai briefing.
- **Rules eksplisit** mencegah saran yang tidak realistis ("hindari perubahan struktural besar").

---

#### Contoh 3 — Multi-Role Code Review (Reviewer + Security + Performance)

Skenario: review pull request yang menggabungkan **tiga perspektif** dalam satu output — kualitas kode umum, keamanan, dan performa.

```text
<system_context>
Anda akan melakukan code review terhadap pull request berikut.
Output digunakan untuk memberikan feedback kepada developer junior.
</system_context>

<personas>
Anda akan beralih peran sesuai tahap analisis:

PERAN 1 — Senior Engineer (Code Quality):
  Fokus: readability, maintainability, naming, code organization.
  Tone: konstruktif, edukatif.

PERAN 2 — Security Engineer:
  Fokus: input validation, authentication, secret handling, OWASP top 10.
  Tone: tegas, tidak kompromi pada celah kritikal.

PERAN 3 — Performance Engineer:
  Fokus: query efficiency, N+1 problems, caching, memory usage.
  Tone: pragmatis, berbasis trade-off.
</personas>

<knowledge_base>
KONTEKS PROYEK:
- Stack: Next.js 16 (App Router) + TypeScript + Supabase (Postgres + pgvector).
- Akses DB: server-side only via Server Actions / Route Handlers menggunakan
  service-role key. Browser hanya melihat data yang dikirim balik dari server.
- Skala: ~10.000 active users, traffic puncak 200 req/detik.
- Convention internal:
  - camelCase untuk variable & function, PascalCase untuk type & React component.
  - Zod untuk validasi input dari client ke server.
  - Tidak boleh ada import `process.env` di komponen client (`"use client"`).

PR YANG AKAN DI-REVIEW:
```typescript
{tempel kode dari pull request — 50–100 baris,
 mis. Server Action handler atau API Route Handler}
```
</knowledge_base>

<task>
Lakukan review dalam 3 babak berurutan:

BABAK 1 (sebagai Senior Engineer): review kualitas kode umum.
BABAK 2 (sebagai Security Engineer): review aspek keamanan.
BABAK 3 (sebagai Performance Engineer): review aspek performa.

Akhiri dengan SINTESIS: rekomendasi prioritas perbaikan.
</task>

<rules>
- Setiap temuan harus merujuk ke **baris kode spesifik**.
- Bedakan severity: 🔴 Blocker | 🟡 Should Fix | 🟢 Nice to Have.
- Jangan ulang temuan yang sama di babak berbeda — jika tumpang tindih,
  letakkan di babak pertama yang relevan.
- Berikan saran kode pengganti jika memungkinkan, bukan hanya kritik.
</rules>

<output_format>
## 🧑‍💻 Babak 1 — Code Quality Review
{daftar temuan dengan severity emoji, baris kode, dan saran perbaikan}

## 🔒 Babak 2 — Security Review
{...}

## ⚡ Babak 3 — Performance Review
{...}

## 📋 Sintesis & Prioritas Perbaikan
1. {Blocker pertama} — alasan singkat
2. ...
3. ...

## Ringkasan Skor
- Code Quality: {1-5}
- Security: {1-5}
- Performance: {1-5}
</output_format>
```

**Mengapa contoh ini bagus:**
- **Multi-persona** memungkinkan satu prompt menghasilkan **3 sudut pandang berbeda** tanpa harus run terpisah.
- **Knowledge base proyek-spesifik** (Next.js + TypeScript + Supabase, convention internal) menyesuaikan saran.
- **Rules anti-duplikasi** ("jangan ulang temuan yang sama di babak berbeda") mencegah noise.
- **Sintesis akhir** mengubah 3 review terpisah menjadi prioritas tindakan yang dapat ditindaklanjuti.

---

### Kapan Structured Prompting Sebenarnya Diperlukan?

Structured prompting adalah tingkat paling kompleks — gunakan **hanya jika** task Anda memenuhi minimal salah satu kriteria berikut:

| Kriteria | Contoh |
|----------|--------|
| Menggabungkan **multiple sources** | Kontrak + policy + history + standar industri |
| Membutuhkan **multiple perspectives** | Code review dari sudut quality, security, performance |
| Output **dikonsumsi sistem produksi** | Chatbot enterprise, agent autonomous, workflow orkestrasi |
| Persona dan knowledge base **harus konsisten lintas conversation** | Brand voice, compliance assistant |

Jika task Anda hanya membutuhkan beberapa contoh dan instruksi sederhana, **few-shot atau CoT sudah cukup** — tidak perlu structured. Ingat aturan main spectrum: naik tingkat hanya jika ada bukti dibutuhkan.

---

## 7. Pemilihan Teknik — Decision Matrix

| Skenario                                       | Rekomendasi teknik              |
|------------------------------------------------|---------------------------------|
| Klasifikasi 3 label, domain umum               | Zero-shot                       |
| Klasifikasi domain-specific (taxonomy internal)| Few-shot (3–5 contoh)           |
| Ekstraksi field terstruktur                    | Few-shot + JSON schema          |
| Soal matematika / logika multi-step            | CoT (atau Extended Thinking)    |
| Customer-facing chatbot                        | Persona-based + structured      |
| Multi-document analysis & synthesis            | Structured + CoT                |
| High-volume tagging                            | Zero-shot Haiku                 |

---

## Demo Live (15 menit)

**Skenario**: bandingkan 3 teknik pada task klasifikasi sentimen tweet bahasa Indonesia bercampur slang.

### Langkah

1. **Buka claude.ai** (free tier, model default Sonnet 4.x). Karena claude.ai tidak memungkinkan set `temperature=0`, **jalankan setiap teknik 2–3 kali** dan ambil output yang mayoritas. Variansi minor antar run adalah hal normal dan justru menjadi pelajaran tentang reproducibility.
2. Siapkan 5 tweet test (sertakan 1 sarkastik, 1 mixed sentiment, 1 slang berat).
3. **Run zero-shot**: prompt klasifikasi dasar tanpa contoh.
4. **Run few-shot**: tambahkan 5 contoh terbalanced.
5. **Run CoT**: tambahkan instruksi "pikirkan langkah demi langkah, identifikasi kata kunci sentimen, baru beri label".
6. Catat output ke tabel perbandingan. Diskusikan: kapan jump dari zero ke few-shot worth? Kapan CoT worth?

> 💡 **Catatan untuk Day 2+**: Saat Anda mengintegrasikan ke kode (Day 2), pemanggilan via Anthropic API dapat menerima parameter `temperature: 0` sehingga A/B test menjadi deterministik. Untuk Day 1, eksplorasi via claude.ai sudah cukup untuk mendapatkan intuisi pola perbedaan antar teknik.

---

## Contoh Konkret: Poor → Good → Better

### Contoh 1 — Klasifikasi Domain-Specific

```text
[POOR / zero-shot naive]
Klasifikasikan tiket: "Mau redeem promo cashback 50K untuk transaksi GoFood"
Kategori: ?
```

```text
[GOOD / zero-shot + taxonomy]
Klasifikasikan tiket ke salah satu kategori:
PROMO, PAYMENT, ORDER_ISSUE, ACCOUNT, OTHER.

Tiket: "Mau redeem promo cashback 50K untuk transaksi GoFood"
Kategori:
```

```text
[BETTER / few-shot]
Klasifikasikan tiket ke salah satu kategori:
PROMO, PAYMENT, ORDER_ISSUE, ACCOUNT, OTHER.

<example>
Tiket: "Kartu kredit saya ditolak waktu bayar"
Kategori: PAYMENT
</example>
<example>
Tiket: "Voucher diskon ulang tahun belum masuk"
Kategori: PROMO
</example>
<example>
Tiket: "Pesanan sampai tapi kurang 1 item"
Kategori: ORDER_ISSUE
</example>
<example>
Tiket: "Lupa password dan email lama sudah tidak aktif"
Kategori: ACCOUNT
</example>

Tiket: "Mau redeem promo cashback 50K untuk transaksi GoFood"
Kategori:
```

### Contoh 2 — Reasoning Matematika

```text
[POOR]
Jika saya beli 3 kg apel @25rb, 2 kg jeruk @30rb, dan dapat diskon 10%,
berapa total yang harus dibayar?
```

```text
[GOOD / CoT manual]
Hitung total pembayaran dengan langkah berikut:
1. Subtotal apel.
2. Subtotal jeruk.
3. Total sebelum diskon.
4. Diskon (10%).
5. Total akhir.

Soal: 3 kg apel @25rb + 2 kg jeruk @30rb, diskon 10%.

Tulis langkah lalu jawaban akhir.
```

```text
[BETTER / CoT + structured + abstain]
<task>
Hitung total pembayaran customer.
</task>

<order>
- Apel: 3 kg @ Rp 25.000
- Jeruk: 2 kg @ Rp 30.000
- Diskon: 10% dari subtotal
</order>

<rules>
- Tunjukkan perhitungan langkah demi langkah di dalam <thinking>.
- Jawaban final dalam <answer> dengan format "Rp X".
- Jika ada ambiguitas, jelaskan di <thinking> dan minta klarifikasi di <answer>.
</rules>

<thinking>
{kerjakan langkah di sini}
</thinking>

<answer>
{jawaban final}
</answer>
```

### Contoh 3 — Persona Customer Service Multi-Turn

```text
[POOR]
Kamu adalah CS. Balas: "kenapa pengiriman saya lama?"
```

```text
[GOOD]
Anda adalah CS officer e-commerce yang ramah dan solutif.
Balas keluhan: "kenapa pengiriman saya lama?"
Maks 80 kata.
```

```text
[BETTER]
<persona>
Nama: Mira, CS Senior di e-commerce ABCMart.
Karakter: empati tinggi, lugas, tidak menggurui, selalu tawarkan langkah konkret.
Larangan: tidak menjanjikan refund tanpa eskalasi ke supervisor.
</persona>

<sop>
Untuk keluhan pengiriman lama:
1. Akui & empati (1 kalimat).
2. Minta nomor resi.
3. Janjikan investigasi 1x24 jam.
4. Tawarkan kompensasi voucher 25K untuk delay > 5 hari.
</sop>

<task>
Balas pesan pelanggan dalam <message> mengikuti <sop>. Maks 100 kata.
Format markdown: salam, body, closing dengan nomor tiket [#PLACEHOLDER].
</task>

<message>
Kenapa pengiriman saya lama?
</message>
```

---

## Hands-on Lab

[`lab-02-zero-few-cot/`](./lab-02-zero-few-cot/) — Praktik 3 teknik (zero-shot, few-shot, CoT) pada 3 task: klasifikasi sentimen, ekstraksi entitas, reasoning matematika. Lengkap dengan tabel evaluasi.

**Durasi**: 45 menit
**Mode**: Individual, peer-comparison di akhir.

---

## Wrap-up & Q&A

1. Kapan few-shot tidak worth dibanding zero-shot?
2. Mengapa CoT bisa **menurunkan** kualitas untuk task tertentu? (hint: task sederhana)
3. Apa risiko mempublikasikan reasoning chain ke end user?
4. Bagaimana Anda memilih jumlah contoh few-shot — 2, 5, 8?
5. Apa beda persona-based dengan system prompt biasa?

---

## Bacaan Lanjutan

- Anthropic — *Multishot prompting*: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/multishot-prompting
- Anthropic — *Chain of thought*: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-of-thought
- Anthropic — *Extended thinking*: https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking
- Wei et al. — *Chain-of-Thought Prompting Elicits Reasoning in LLMs*: https://arxiv.org/abs/2201.11903
- Anthropic — *Prompt library — Roleplay*: https://docs.anthropic.com/en/prompt-library/library
