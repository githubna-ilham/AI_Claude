# Lab 02 — Zero-Shot, Few-Shot, Chain-of-Thought

**Modul**: Module 3 — Prompting Techniques
**Durasi**: 45 menit (3 task × ~15 menit)
**Mode**: Individual
**Tools**: **Anthropic Console — Workbench** (https://console.anthropic.com/workbench) + Google Spreadsheet
**Output**: Spreadsheet berisi output 3 teknik × 3 task + insight singkat per task

---

## Tujuan

Setelah lab ini Anda mampu:

1. Membandingkan akurasi 3 teknik prompting (zero-shot, few-shot, CoT) pada task yang identik.
2. Memilih teknik yang tepat untuk masing-masing task berdasarkan data, bukan opini.
3. Mengidentifikasi kapan CoT membantu dan kapan justru menjadi overhead yang tidak perlu.

---

## Prasyarat

- Telah menyelesaikan Module 3 (materi).
- Akun **Anthropic Console** pribadi aktif (https://console.anthropic.com).
- Anda telah menerima undangan untuk bergabung ke **Workspace pelatihan Jalin** yang disiapkan fasilitator. Seluruh usage Workbench selama lab ini akan otomatis ditagihkan ke billing pelatihan.
- Google Spreadsheet kosong untuk mencatat hasil.

> ℹ️ **Mengapa Workbench, bukan claude.ai?** Lab 02 memerlukan parameter **`temperature=0`** agar hasil eksperimen reproducible — output yang sama setiap kali prompt dijalankan ulang. claude.ai tidak mengekspos parameter `temperature`, sedangkan Workbench memberikan kontrol penuh. Hal ini krusial saat membandingkan kualitas zero-shot vs few-shot vs CoT secara objektif.

---

## Setup Workbench (3 menit)

1. Login ke https://console.anthropic.com.
2. Pada dropdown **workspace** (pojok kanan atas), pilih workspace pelatihan yang diinformasikan fasilitator.
3. Buka tab **Workbench** dari sidebar kiri.
4. Pada panel kanan, set:
   - **Model**: `claude-sonnet-4-5`
   - **Temperature**: `0`
   - **Max tokens**: `1024`
5. Kosongkan **System Prompt**. Seluruh prompt lab ini ditempel ke kolom **User**.
6. Setiap klik **Run** = 1 API call = memotong saldo workspace pelatihan. Susun draft prompt di editor teks dulu, baru tempel ke Workbench saat siap dieksekusi.

---

## Task 1 — Klasifikasi Sentimen Komentar Nasabah Jalin

### 1.1 Dataset

Klasifikasikan ke `POSITIF`, `NEGATIF`, atau `NETRAL`.

```
S1: "Transfer via BI-FAST cepat banget, sampai dalam 2 detik, mantap!"
S2: "Sudah seminggu komplain dispute saldo terdebit tapi belum diproses, kecewa."
S3: "Aplikasinya update lagi, layoutnya berubah, tapi fungsi utamanya masih sama."
S4: "Awalnya senang karena ATM Link gratis tarik tunai, tapi ternyata limitnya kecil banget."
S5: "Wah keren ya tiap mau transfer harus loading 30 detik, hemat waktu sekali /sarcasm"
```

**Ground truth** (untuk self-check):
S1 POSITIF | S2 NEGATIF | S3 NETRAL | S4 NEGATIF (mixed dengan letdown) | S5 NEGATIF (sarkasme).

### 1.2 Prompt Templates

Jalankan ketiga template berikut untuk S1–S5. Ganti `{kalimat}` dengan tiap sampel.

<details>
<summary>👉 Zero-Shot Template</summary>

```text
Klasifikasikan sentimen kalimat berikut sebagai POSITIF, NEGATIF, atau NETRAL.

Kalimat: "{kalimat}"
Sentimen:
```

</details>

<details>
<summary>👉 Few-Shot Template</summary>

```text
Klasifikasikan sentimen kalimat sebagai POSITIF, NEGATIF, atau NETRAL.

<example>
Kalimat: "Aplikasi makin enak dipakai setelah update."
Sentimen: POSITIF
</example>
<example>
Kalimat: "Customer service-nya jutek banget, males balik."
Sentimen: NEGATIF
</example>
<example>
Kalimat: "Aplikasi berfungsi sebagaimana mestinya."
Sentimen: NETRAL
</example>
<example>
Kalimat: "Wah keren bisa ngabisin kuota saya, makasih ya /sarcasm"
Sentimen: NEGATIF
</example>

Kalimat: "{kalimat}"
Sentimen:
```

</details>

<details>
<summary>👉 Chain-of-Thought Template</summary>

```text
Klasifikasikan sentimen kalimat sebagai POSITIF, NEGATIF, atau NETRAL.

Langkah berpikir:
1. Identifikasi kata kunci sentimen.
2. Periksa indikator sarkasme (/sarc, kontras berlebihan, konteks yang tidak masuk akal).
3. Tentukan polaritas dominan.
4. Beri label.

<thinking>
{tulis langkah di sini}
</thinking>

<answer>
Sentimen: {LABEL}
</answer>

Kalimat: "{kalimat}"
```

</details>

### 1.3 Spreadsheet Task 1

| Sampel | Ground Truth | Output Zero-Shot | Z benar? | Output Few-Shot | F benar? | Output CoT | CoT benar? |
|--------|--------------|------------------|----------|-----------------|----------|------------|------------|
| S1     | POSITIF      |                  |          |                 |          |            |            |
| S2     | NEGATIF      |                  |          |                 |          |            |            |
| S3     | NETRAL       |                  |          |                 |          |            |            |
| S4     | NEGATIF      |                  |          |                 |          |            |            |
| S5     | NEGATIF      |                  |          |                 |          |            |            |
| **Akurasi (%)** | —    |                  |          |                 |          |            |            |

### 1.4 Insight Task 1

Tulis 1–2 kalimat: teknik mana yang paling akurat, dan mengapa?

---

## Task 2 — Reasoning Matematika (Kalkulasi Biaya Transaksi)

### 2.1 Dataset

```
M1: Seorang nasabah melakukan 4 transaksi dalam satu hari:
- 3× transfer Rp 5.000.000 ke bank lain via BI-FAST (biaya Rp 2.500/transaksi)
- 2× tarik tunai Rp 1.000.000 di ATM Bank lain via Link (biaya Rp 7.500/transaksi)
- 5× cek saldo di ATM bank lain via Link (biaya Rp 4.000/transaksi)
- 1× transfer Rp 25.000.000 ke bank lain via BI-FAST (biaya Rp 2.500/transaksi)
Berapa total biaya yang dibebankan ke nasabah?

M2: Andi pinjam Rp 5.000.000 dengan bunga sederhana 12% per tahun, jangka 6 bulan.
Berapa total yang harus dibayar di akhir periode?

M3: Tim project switching punya 5 task. Task A & B masing-masing 3 hari, dapat
dikerjakan paralel. Task C butuh A & B selesai, durasi 2 hari. Task D & E
masing-masing 4 hari dan dapat dikerjakan paralel setelah C selesai.
Berapa total waktu minimum project?
```

**Ground truth** (untuk self-check):
- **M1**: Total biaya = **Rp 45.000** (BI-FAST: 4 × 2.500 = 10.000; Link tarik tunai: 2 × 7.500 = 15.000; Link cek saldo: 5 × 4.000 = 20.000).
- **M2**: Total = **Rp 5.300.000** (bunga = 5.000.000 × 12% × 6/12 = 300.000).
- **M3**: Total waktu minimum = **9 hari** (A & B paralel 3 hari → C 2 hari → D & E paralel 4 hari).

### 2.2 Prompt Templates

Ganti `{soal}` dengan teks M1, M2, atau M3.

<details>
<summary>👉 Zero-Shot Template</summary>

```text
Selesaikan soal berikut. Berikan jawaban akhirnya secara singkat.

Soal: "{soal}"
Jawaban:
```

</details>

<details>
<summary>👉 Few-Shot Template</summary>

```text
Selesaikan soal berikut. Berikan jawaban akhirnya secara singkat.

<example>
Soal: "Bu Sari membeli 3 kg apel @ Rp 25.000/kg dan 2 kg jeruk @ Rp 30.000/kg. Berapa total yang harus dibayar?"
Jawaban: Apel 3 × 25.000 = 75.000; Jeruk 2 × 30.000 = 60.000; Total = Rp 135.000.
</example>
<example>
Soal: "Pak Budi menabung Rp 50 juta di deposito dengan bunga sederhana 5% per tahun selama 2 tahun. Berapa saldo akhir?"
Jawaban: Bunga = 50 juta × 5% × 2 = 5 juta. Saldo akhir = Rp 55 juta.
</example>

Soal: "{soal}"
Jawaban:
```

</details>

<details>
<summary>👉 Chain-of-Thought Template</summary>

```text
Selesaikan soal berikut. Pikirkan langkah demi langkah.

Langkah berpikir:
1. Identifikasi data yang diketahui dari soal.
2. Tentukan rumus atau metode yang relevan.
3. Lakukan perhitungan satu per satu, tulis hasil tiap langkah.
4. Simpulkan jawaban akhir dengan satuan yang sesuai.

<thinking>
{tulis langkah perhitungan di sini}
</thinking>

<answer>
Jawaban: {jawaban akhir}
</answer>

Soal: "{soal}"
```

</details>

### 2.3 Spreadsheet Task 2

| Sampel | Ground Truth     | Output Zero-Shot | Z benar? | Output Few-Shot | F benar? | Output CoT | CoT benar? |
|--------|------------------|------------------|----------|-----------------|----------|------------|------------|
| M1     | Rp 45.000        |                  |          |                 |          |            |            |
| M2     | Rp 5.300.000     |                  |          |                 |          |            |            |
| M3     | 9 hari           |                  |          |                 |          |            |            |
| **Akurasi (%)** | —     |                  |          |                 |          |            |            |

### 2.4 Insight Task 2

Tulis 1–2 kalimat: pada soal mana CoT memberikan keunggulan paling nyata? Mengapa?

---

## Task 3 — Klasifikasi Tiket Incident Sistem Pembayaran

### 3.1 Dataset

Klasifikasikan tiket ke salah satu kategori berikut:

| Kategori                              | Deskripsi                                                  |
|---------------------------------------|------------------------------------------------------------|
| `ATM_DISPENSE_ERROR_FALSE_SUCCESS`    | Uang tidak keluar tetapi sistem mencatat sukses.           |
| `ATM_NETWORK_TIMEOUT`                 | Koneksi ke switch terputus saat transaksi.                 |
| `ATM_RECEIPT_PRINTER_ISSUE`           | Mesin gagal mencetak struk.                                |
| `BIFAST_REVERSAL_DELAY`               | Reversal BI-FAST melewati SLA.                             |
| `OTHER`                               | Tidak masuk kategori di atas.                              |

```
T1: "Transaksi tarik tunai di ATM Link Bank C gagal sejak pukul 22.00 kemarin,
     namun mesin tetap mengeluarkan struk SUKSES. Saldo nasabah terdebit."

T2: "Nasabah komplain transfer BI-FAST Rp 2 juta gagal 5 hari lalu,
     reversal belum masuk hingga sekarang."

T3: "ATM di cabang Jakarta Selatan tidak mengeluarkan struk transaksi,
     padahal transaksi dispense uang berhasil."

T4: "Beberapa transaksi di ATM Bank D timeout terus sejak 30 menit lalu,
     diduga koneksi ke switch bermasalah."

T5: "Aplikasi mobile banking saya error saat buka menu QRIS."
```

**Ground truth** (untuk self-check):
T1 `ATM_DISPENSE_ERROR_FALSE_SUCCESS` | T2 `BIFAST_REVERSAL_DELAY` | T3 `ATM_RECEIPT_PRINTER_ISSUE` | T4 `ATM_NETWORK_TIMEOUT` | T5 `OTHER`.

### 3.2 Prompt Templates

Ganti `{tiket}` dengan T1–T5.

<details>
<summary>👉 Zero-Shot Template</summary>

```text
Klasifikasikan tiket berikut ke salah satu kategori:
ATM_DISPENSE_ERROR_FALSE_SUCCESS, ATM_NETWORK_TIMEOUT,
ATM_RECEIPT_PRINTER_ISSUE, BIFAST_REVERSAL_DELAY, OTHER.

Tiket: "{tiket}"
Kategori:
```

</details>

<details>
<summary>👉 Few-Shot Template</summary>

```text
Klasifikasikan tiket berikut ke salah satu kategori:
ATM_DISPENSE_ERROR_FALSE_SUCCESS, ATM_NETWORK_TIMEOUT,
ATM_RECEIPT_PRINTER_ISSUE, BIFAST_REVERSAL_DELAY, OTHER.

<example>
Tiket: "ATM Bank A keluar struk gagal padahal nasabah sudah terima uang."
Kategori: ATM_RECEIPT_PRINTER_ISSUE
</example>
<example>
Tiket: "Transfer BI-FAST 7 hari lalu gagal, dana belum kembali ke saldo."
Kategori: BIFAST_REVERSAL_DELAY
</example>
<example>
Tiket: "Koneksi ATM ke switch putus sejak pagi tadi."
Kategori: ATM_NETWORK_TIMEOUT
</example>

Tiket: "{tiket}"
Kategori:
```

</details>

<details>
<summary>👉 Chain-of-Thought Template</summary>

```text
Klasifikasikan tiket berikut ke salah satu kategori:
ATM_DISPENSE_ERROR_FALSE_SUCCESS, ATM_NETWORK_TIMEOUT,
ATM_RECEIPT_PRINTER_ISSUE, BIFAST_REVERSAL_DELAY, OTHER.

Langkah berpikir:
1. Identifikasi gejala utama dari tiket (apa yang gagal? di mana?).
2. Cocokkan gejala dengan deskripsi tiap kategori.
3. Pilih kategori yang paling sesuai. Jika tidak ada yang cocok, pilih OTHER.

<thinking>
{tulis langkah di sini}
</thinking>

<answer>
Kategori: {LABEL}
</answer>

Tiket: "{tiket}"
```

</details>

### 3.3 Spreadsheet Task 3

| Sampel | Ground Truth                         | Output Zero-Shot | Z benar? | Output Few-Shot | F benar? | Output CoT | CoT benar? |
|--------|--------------------------------------|------------------|----------|-----------------|----------|------------|------------|
| T1     | ATM_DISPENSE_ERROR_FALSE_SUCCESS     |                  |          |                 |          |            |            |
| T2     | BIFAST_REVERSAL_DELAY                |                  |          |                 |          |            |            |
| T3     | ATM_RECEIPT_PRINTER_ISSUE            |                  |          |                 |          |            |            |
| T4     | ATM_NETWORK_TIMEOUT                  |                  |          |                 |          |            |            |
| T5     | OTHER                                |                  |          |                 |          |            |            |
| **Akurasi (%)** | —                          |                  |          |                 |          |            |            |

### 3.4 Insight Task 3

Tulis 1–2 kalimat: apakah few-shot sudah cukup untuk task taxonomy-driven seperti ini, atau CoT masih memberi nilai tambah?

---

## Insight Akhir (5 menit)

Setelah ketiga task selesai, tulis 3–5 bullet menjawab:

- Pada task mana zero-shot sudah memadai? Mengapa few-shot tidak memberi gain berarti?
- Pada task mana CoT memberikan keunggulan paling nyata?
- Adakah task di mana CoT justru memperburuk output (over-reasoning, langkah halusinasi)?
- Untuk masing-masing 3 task, teknik mana yang akan Anda pilih untuk produksi? Dengan alasan apa?

---

## Kriteria Selesai (Definition of Done)

- [ ] 3 task × 3 teknik = 9 kombinasi telah dijalankan di Workbench.
- [ ] Spreadsheet evaluasi terisi untuk seluruh sampel di setiap task (5 + 3 + 5 = 13 baris × 3 teknik).
- [ ] Akurasi per teknik per task dihitung (gunakan `=COUNTIF` di Google Sheets).
- [ ] Insight per task ditulis (1–2 kalimat tiap task).
- [ ] Insight akhir (3–5 bullet) ditulis.

---

## Tips

- Dengan `temperature=0`, output yang sama akan keluar setiap kali Anda klik Run — manfaatkan untuk eksperimen reproducible.
- Pada Task 1 S5 (sarkasme) dan Task 2 M3 (project scheduling dengan dependensi paralel), CoT sangat membantu apabila langkah berpikir dirumuskan secara eksplisit.
- Simpan prompt yang berhasil di Workbench (tombol **Save** di kanan atas) agar dapat dimuat ulang tanpa menulis ulang.
- Jika output inkonsisten meskipun `temperature=0`, biasanya **prompt-nya yang ambigu** — bukan modelnya. Perketat instruksi sebelum berpindah ke model yang lebih mahal.

---

## Deliverable

Satu Google Spreadsheet berisi 3 sheet (Task 1, Task 2, Task 3) sesuai template di atas + 1 sheet "Insight Akhir". Atur sharing ke **"Anyone with the link — Viewer"**, kirim tautannya ke channel pelatihan.
