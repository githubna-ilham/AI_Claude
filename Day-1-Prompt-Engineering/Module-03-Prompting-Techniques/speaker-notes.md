# Speaker Notes — Module 3: Prompting Techniques

**Total alokasi**: 90 menit
**Mode**: Lecture 45% + demo perbandingan 30% + workshop singkat 25%

---

## Anekdot Pembuka (3 menit)

> "Saya pernah menghabiskan 2 minggu fine-tuning sebuah model untuk klasifikasi tiket. Akurasi naik dari 78% ke 85%. Bos saya senang. Lalu kolega saya datang, tambah 5 contoh few-shot di prompt Claude — akurasi 91%. Tanpa training, tanpa GPU, tanpa MLOps. Itulah magic in-context learning. Module ini mengajarkan Anda kapan dan bagaimana mengeksploitasinya."

---

## Alokasi Waktu

| Bagian                                | Durasi | Tipe              |
|---------------------------------------|--------|-------------------|
| Pembuka + anekdot                     | 3 m    | Cerita            |
| 1. Spectrum prompting                 | 5 m    | Lecture           |
| 2. Zero-shot                          | 8 m    | Lecture + contoh  |
| 3. Few-shot                           | 15 m   | Lecture + demo    |
| 4. Chain-of-thought                   | 15 m   | Lecture + demo    |
| 5. Persona-based                      | 8 m    | Lecture           |
| 6. Structured prompting               | 8 m    | Lecture           |
| 7. Decision matrix                    | 3 m    | Walkthrough       |
| Demo live perbandingan 3 teknik       | 15 m   | Demo              |
| Walkthrough contoh + Q&A              | 5 m    | Diskusi           |
| Handoff ke Lab 02                     | 5 m    | Transisi          |

Total: 90 menit.

---

## Cue Fasilitator per Bagian

### Zero-shot
- Tekankan: ini default, jangan langsung loncat ke few-shot.
- Demo cepat: zero-shot ringkasan paragraf di claude.ai — biasanya sudah cukup.

### Few-shot
- Tunjukkan **A/B**: zero-shot vs few-shot pada task yang sama, biarkan peserta lihat perubahan output.
- Bahas **bias contoh**: tunjukkan apa yang terjadi jika 4 dari 5 contoh positif → model condong positif.
- Hint penting: **format consistency** lebih penting dari kuantitas.

### Chain-of-Thought
- Tunjukkan dampak CoT pada soal matematika sedang (misal: word problem 3 langkah).
- Sebutkan: Claude Extended Thinking (Sonnet/Opus 4.x) sering membuat CoT manual obsolete untuk model besar — tapi tetap berguna untuk Haiku.
- **Warning**: CoT bisa **memburuk** untuk task sederhana (overthinking). Tunjukkan satu kasus.

### Persona
- Pertanyaan: "Apa beda persona dengan role di Module 2?" Jawaban: persona lebih kaya, multi-dimensi, konsisten lintas turn.

### Structured
- Sebutkan: ini blueprint untuk Day 2+. Tahan dulu mengajarkan tool-use; cukup tunjukkan template.

---

## Jawaban Kunci untuk Pertanyaan Refleksi

1. **Few-shot tidak worth**: ketika model sudah menjawab konsisten di zero-shot (uji 20–50 sampel), atau ketika volume tinggi membuat 5 contoh × tiap request = biaya besar.
2. **CoT bisa menurunkan kualitas**: pada task sederhana (klasifikasi 1-step), CoT memperkenalkan noise & over-reasoning. Studi menunjukkan inverse scaling pada beberapa benchmark.
3. **Risiko publikasi reasoning chain**: bisa bocor data internal (jika reasoning menyebut context), atau memberi end-user kesan over-confidence. Best practice: simpan untuk log, jangan tampil ke user.
4. **Memilih jumlah few-shot**: mulai 3, ukur akurasi pada eval set; tambah hingga marginal gain < 1 poin per contoh. Biasanya plateau di 5–8.
5. **Persona vs system prompt**: system prompt = lokasi; persona = isi. Persona-based prompting biasanya **menjalankan** persona di dalam system prompt + reinforcement di tiap turn.

---

## Common Pitfall Peserta

| Pitfall                                                              | Respons fasilitator |
|----------------------------------------------------------------------|---------------------|
| Mengira "lebih banyak contoh = lebih baik" tanpa batas               | Tunjukkan diminishing return + biaya. |
| Contoh few-shot semua sama jenisnya (mis. semua positif)             | Latih diversity & balance. |
| CoT di task simple → output bertele-tele                             | Tunjukkan satu kasus over-reasoning. |
| Persona terlalu generik atau dramatis                                | Latih persona drilling 3 dimensi (peran, karakter, larangan). |
| Mencampur instruksi & contoh tanpa delimiter                         | Wrap dalam `<example>` tag. |
| Mengira CoT = lebih akurat untuk segala hal                          | Bahas inverse scaling. |
| Lupa `temperature=0` ketika membandingkan teknik                     | Selalu set deterministic untuk eval. |

---

## Demo Live — Persiapan

Siapkan 5 tweet sample (boleh fiktif, mirror produksi):

```
1. "GoFood paling oke kalau lagi laper malam-malam"
2. "Ya bagus sih appsnya, tapi kok sekarang lemot banget update terbaru"
3. "ga ngerti deh, transaksi gagal mulu tapi saldo kepotong"
4. "Lumayan lah, harga normal pengiriman tepat waktu"
5. "Wah keren banget, ga nyangka bisa secepet ini! /sarc"
```

Jalankan ketiga teknik bergantian, tabulasi hasil di whiteboard / shared doc.

---

## Transisi ke Lab 02

> "Sekarang Anda akan mereplikasi eksperimen ini sendiri. 3 teknik × 3 task. Catat hasilnya di tabel evaluasi. Ini adalah miniatur dari prompt engineering pipeline produksi — pilih teknik berbasis bukti, bukan opini."
