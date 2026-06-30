# Module 3 — Prompting Techniques

**Durasi**: 90 menit
**Posisi**: Modul ketiga Day 1; memperluas anatomi (Module 2) ke teknik lanjutan.
**Format**: Baca konsep → telaah perbandingan → kerjakan Lab 02.

---

## Learning Outcomes

Setelah modul ini, Anda mampu:

1. **Membedakan** kapan menggunakan zero-shot, few-shot, dan chain-of-thought (CoT) berdasarkan kompleksitas task & ketersediaan contoh.
2. **Menyusun** prompt few-shot dengan contoh berkualitas tinggi (diverse, balanced, formatted).
3. **Memandu** model melalui reasoning step-by-step dan menangkap rantai berpikir untuk audit.
4. **Menerapkan** persona-based prompting dan structured prompting untuk skenario kompleks.
5. **Mengevaluasi** trade-off antara token cost, latency, dan akurasi untuk setiap teknik.

---

## 1. Pengantar — Spectrum Prompting

### Apa Itu Spectrum Prompting?

**Spectrum Prompting** adalah cara berpikir yang menempatkan berbagai teknik prompting dalam sebuah **rentang (spectrum)** — dari yang paling sederhana hingga paling kompleks. Tujuannya agar Anda **tidak langsung menggunakan teknik kompleks** ketika teknik sederhana sudah memadai.

Analoginya seperti memilih alat di kotak peralatan: untuk memasang paku tidak diperlukan palu godam — palu kecil sudah memadai. Demikian pula dengan prompt: untuk task sederhana, hindari penggunaan teknik berlapis-lapis. Mulailah dari yang paling ringan.

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

Jika Anda langsung memilih teknik paling kompleks, Anda **membayar biaya tinggi tanpa selalu memperoleh hasil yang lebih baik**. Sebaliknya, jika menggunakan teknik yang terlalu sederhana untuk task kompleks, akurasi akan rendah dan prompt akan terus perlu diulang.

### Empat Tingkat dalam Spectrum

| Tingkat | Teknik | Karakteristik | Biaya |
|---------|--------|--------------|-------|
| **1** | **Zero-Shot** | Instruksi saja, tanpa contoh | Paling rendah |
| **2** | **Few-Shot** | Instruksi + 2 hingga 8 contoh input→output | Sedang |
| **3** | **Chain-of-Thought (CoT)** | Few-shot + minta model menjelaskan reasoning | Sedang–tinggi |
| **4** | **Structured Prompting** | Multi-section dengan peran, sumber, dan format yang dikombinasikan | Tertinggi |

Catatan penting: angka tingkat **bukan** tingkat kualitas. Tingkat 4 tidak otomatis "lebih baik" dibanding tingkat 1 — ia hanya **lebih cocok untuk task yang lebih kompleks**.

### Aturan Naik Tingkat

Pendekatan yang direkomendasikan: **mulailah dari tingkat paling rendah, naik hanya jika hasilnya belum memadai.**

1. **Mulai dengan Zero-Shot.** Cobalah terlebih dahulu — paling cepat, paling ekonomis, dan banyak task umum yang sudah berhasil di tingkat ini.
2. **Naik ke Few-Shot jika output tidak konsisten** atau format tidak sesuai harapan. Tambahkan 2–3 contoh untuk "mengunci" pola yang diinginkan.
3. **Naik ke Chain-of-Thought jika task membutuhkan penalaran multi-step** — misalnya kalkulasi bertahap, analisis kausalitas, atau pengambilan keputusan dengan beberapa kriteria.
4. **Naik ke Structured Prompting jika terdapat beberapa peran atau sumber** yang harus dikombinasikan — misalnya menggabungkan dokumen referensi, riwayat percakapan, dan aturan bisnis dalam satu prompt.

### Bagaimana Memutuskan Titik Awal?

Gunakan tiga pertanyaan diagnostik berikut:

| Pertanyaan | Jika "ya" | Mulai dari |
|-----------|-----------|-----------|
| Apakah task ini umum dan well-known (ringkasan, terjemahan, klasifikasi standar)? | Ya | **Zero-Shot** |
| Apakah ada format khusus atau taksonomi internal yang harus diikuti? | Ya | **Few-Shot** |
| Apakah task membutuhkan reasoning bertahap atau perhitungan yang dapat salah? | Ya | **Chain-of-Thought** |
| Apakah perlu menggabungkan beberapa peran (analis + reviewer) atau beberapa sumber dokumen? | Ya | **Structured** |

### Prinsip Penting

**Naik tingkat berarti naik biaya dan latency.** Oleh karena itu, keputusan untuk naik tingkat harus berbasis **bukti dari evaluasi**, bukan asumsi. Module 4 (Structured Output & Evaluasi) akan membahas cara mengukur kualitas prompt secara objektif sehingga Anda dapat menentukan **kapan benar-benar perlu naik tingkat** dan kapan teknik yang lebih sederhana sudah memadai.

Bagian selanjutnya akan membahas masing-masing tingkat secara mendalam.

---

## 2. Zero-Shot Prompting

Zero-shot adalah pendekatan ketika model diberi instruksi tanpa contoh. LLM modern (Sonnet, Opus) memiliki kapabilitas tinggi pada zero-shot untuk task umum.

### Kapan dipakai

- Task umum yang well-documented (ringkasan, terjemahan, klasifikasi standar).
- Eksplorasi awal sebelum berinvestasi waktu menulis contoh.
- Volume tinggi di mana setiap token contoh berarti biaya yang berlipat.

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

Few-shot adalah pendekatan ketika prompt menyertakan **2–8 contoh** input→output. Model belajar pattern dari contoh tersebut (in-context learning).

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

- Lebih banyak contoh tidak selalu berarti lebih baik. Setelah 5–8 contoh, marginal gain umumnya menurun, sementara cost meningkat linear.
- Bias contoh menghasilkan bias output. Jika 4 dari 5 contoh berlabel POSITIF, model akan condong ke POSITIF.

---

## 4. Chain-of-Thought (CoT) — Step-by-Step Reasoning

CoT adalah teknik yang memaksa model menulis langkah berpikir sebelum jawaban akhir. Studi menunjukkan akurasi naik signifikan pada task matematika, logika, dan multi-hop reasoning.

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

Untuk keperluan audit, pisahkan reasoning dan jawaban:

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

- Claude **Extended Thinking** (Sonnet/Opus 4.x) menyediakan CoT native dengan budget yang dapat dikontrol. Tidak diperlukan prompt CoT manual untuk task kompleks — cukup aktifkan extended thinking di Console.
- Untuk Haiku, CoT manual melalui prompt tetap relevan.

---

## 5. Persona-Based Prompting

Persona-based adalah role prompting tingkat lanjut yang membentuk **karakter konsisten** lintas turn (multi-turn conversation).

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

Structured prompting adalah prompt yang menggabungkan **multiple sections** dengan tag XML untuk skenario kompleks. Pattern ini menjadi tulang punggung Day 2–4.

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
- **`<rules>`** menyediakan **fallback** spesifik untuk kasus di luar cakupan knowledge base.

---

### Kapan Structured Prompting Sebenarnya Diperlukan?

Structured prompting adalah tingkat paling kompleks — gunakan **hanya jika** task Anda memenuhi minimal salah satu kriteria berikut:

| Kriteria | Contoh |
|----------|--------|
| Menggabungkan **multiple sources** | Kontrak + policy + history + standar industri |
| Membutuhkan **multiple perspectives** | Code review dari sudut quality, security, performance |
| Output **dikonsumsi sistem produksi** | Chatbot enterprise, agent autonomous, workflow orkestrasi |
| Persona dan knowledge base **harus konsisten lintas conversation** | Brand voice, compliance assistant |

Jika task Anda hanya membutuhkan beberapa contoh dan instruksi sederhana, **few-shot atau CoT sudah memadai** — tidak diperlukan structured. Ingat aturan main spectrum: naik tingkat hanya jika terdapat bukti yang membenarkannya.

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

## Demonstrasi Mandiri (15 menit)

**Skenario**: bandingkan 3 teknik pada task klasifikasi sentimen tweet bahasa Indonesia yang bercampur slang.

### Langkah

1. **Buka [Anthropic Console — Workbench](https://console.anthropic.com/workbench)**. Pilih model **Sonnet 4.x** dan set **`temperature = 0`** di panel kanan. Dengan temperature 0, eksperimen A/B menjadi deterministik — sangat penting untuk membandingkan kualitas antar teknik secara objektif.
2. Siapkan 5 tweet test (sertakan 1 yang bersifat sarkastik, 1 mixed sentiment, dan 1 dengan slang yang dominan).
3. **Jalankan zero-shot**: prompt klasifikasi dasar tanpa contoh.
4. **Jalankan few-shot**: tambahkan 5 contoh yang terdistribusi seimbang.
5. **Jalankan CoT**: tambahkan instruksi "pikirkan langkah demi langkah, identifikasi kata kunci sentimen, kemudian berikan label".
6. Catat output pada tabel perbandingan. Refleksi: kapan transisi dari zero ke few-shot bermanfaat? Kapan CoT bermanfaat?

> 💰 **Akses Workbench**: berbeda dengan claude.ai yang gratis, Workbench memerlukan **kredit API** karena setiap "Run" memanggil endpoint Messages. Fasilitator telah membuat **Workspace pelatihan Jalin** di Anthropic Console dan mengundang Anda sebagai member. Selama sesi Module 3, pastikan dropdown workspace di kanan atas Console menunjuk ke workspace pelatihan — seluruh usage akan otomatis ditagihkan ke billing pelatihan, bukan ke akun pribadi Anda.

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

## Refleksi Akhir

1. Kapan few-shot tidak sepadan dibanding zero-shot?
2. Mengapa CoT dapat **menurunkan** kualitas untuk task tertentu? (petunjuk: task sederhana)
3. Apa risiko mempublikasikan reasoning chain kepada end user?
4. Bagaimana Anda memilih jumlah contoh few-shot — 2, 5, atau 8?
5. Apa perbedaan persona-based dengan system prompt biasa?

---

## Bacaan Lanjutan

- Anthropic — *Multishot prompting*: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/multishot-prompting
- Anthropic — *Chain of thought*: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/chain-of-thought
- Anthropic — *Extended thinking*: https://docs.anthropic.com/en/docs/build-with-claude/extended-thinking
- Wei et al. — *Chain-of-Thought Prompting Elicits Reasoning in LLMs*: https://arxiv.org/abs/2201.11903
- Anthropic — *Prompt library — Roleplay*: https://docs.anthropic.com/en/prompt-library/library
