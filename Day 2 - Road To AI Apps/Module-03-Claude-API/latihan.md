# Module 03 — Latihan: Koneksi Pertama ke Claude API

> Latihan untuk memperdalam pemahaman dari section pertama `materi.md`. Setiap eksperimen sederhana, dapat selesai dalam beberapa menit, dan langsung menghasilkan **bukti pemahaman** di terminal Anda.
>
> **Estimasi waktu**: 30 menit.

---

## Prasyarat

- [ ] Materi section pertama Module 03 sudah dibaca.
- [ ] File `experiments/claude-test.ts` sudah dibuat dan berhasil dijalankan minimal sekali.
- [ ] Anda sudah melihat respons Claude muncul di terminal.

---

## Latihan 1 — Ganti Prompt dan Bandingkan Hasil

**Goal**: melatih intuisi bagaimana perubahan prompt mempengaruhi respons.

**Langkah:**

1. Buka `experiments/claude-test.ts`.
2. Ganti isi `content` di pesan `user` menjadi salah satu prompt berikut, satu per satu. Jalankan ulang setiap kali, lalu catat respons yang Anda terima.

| # | Prompt | Catatan respons Anda |
|---|---|---|
| a | "Jelaskan apa itu API dalam satu paragraf untuk anak SMA." | |
| b | "Berikan tiga ide nama startup di bidang keuangan personal." | |
| c | "Tulis pseudocode untuk fungsi yang menghitung total pengeluaran bulanan." | |
| d | "Apa perbedaan TypeScript dan JavaScript?" | |

> 💡 Perhatikan: respons Claude untuk topik teknis cenderung lebih panjang. Apabila terpotong, periksa `stop_reason` — kemungkinan `max_tokens`.

---

## Latihan 2 — Eksperimen dengan `max_tokens`

**Goal**: memahami pengaruh `max_tokens` terhadap output dan biaya.

**Langkah:**

1. Gunakan prompt: `"Jelaskan sejarah singkat Indonesia dari masa kerajaan hingga kemerdekaan."`
2. Jalankan dengan tiga nilai berbeda untuk `max_tokens`:

| Nilai `max_tokens` | `output_tokens` (yang Anda lihat) | `stop_reason` | Catatan |
|---|---|---|---|
| 100 | | | |
| 500 | | | |
| 2000 | | | |

3. **Analisis**: pada nilai mana output terasa lengkap? Pada nilai mana terlihat terpotong?

> 💡 Trade-off: `max_tokens` lebih tinggi → output lebih lengkap → biaya lebih besar. Pilih nilai yang **cukup**, jangan asal besar.

---

## Latihan 3 — Coba Model yang Berbeda

**Goal**: memahami perbedaan model dalam keluarga Claude.

**Langkah:**

1. Gunakan prompt sederhana: `"Tulis haiku tentang kopi pagi."`
2. Jalankan tiga kali dengan model yang berbeda:

| Model | Output (haiku Anda) | `input_tokens` | `output_tokens` |
|---|---|---|---|
| `claude-haiku-4-5` | | | |
| `claude-sonnet-4-6` | | | |
| `claude-opus-4-7` | | | |

3. **Refleksi**: model mana yang menurut Anda menghasilkan haiku paling menyentuh? Apakah selalu yang termahal?

> 💡 Untuk task kreatif yang singkat, perbedaan kualitas antar model sering tidak signifikan. Sonnet atau Haiku biasanya cukup. Opus dipakai ketika reasoning kompleks benar-benar dibutuhkan.

---

## Latihan 4 — Tampilkan Estimasi Biaya

**Goal**: melatih kesadaran biaya saat memakai API.

**Langkah:**

1. Tambahkan fungsi sederhana di akhir `claude-test.ts` untuk menghitung estimasi biaya (perkiraan kasar):

```ts
function estimateCost(model: string, inputTokens: number, outputTokens: number) {
  // Harga per 1M token (referensi — periksa harga terbaru di pricing page Anthropic).
  const pricing: Record<string, { input: number; output: number }> = {
    "claude-haiku-4-5":  { input: 1.0,  output: 5.0  },
    "claude-sonnet-4-6": { input: 3.0,  output: 15.0 },
    "claude-opus-4-7":   { input: 15.0, output: 75.0 },
  };
  const p = pricing[model];
  if (!p) return "(harga tidak diketahui)";
  const cost = (inputTokens / 1_000_000) * p.input + (outputTokens / 1_000_000) * p.output;
  return `$${cost.toFixed(6)} (≈ Rp ${(cost * 16000).toFixed(2)})`;
}
```

2. Panggil fungsi ini setelah blok statistik token:

```ts
console.log(`   Estimasi biaya: ${estimateCost(response.model, response.usage.input_tokens, response.usage.output_tokens)}`);
```

3. Jalankan ulang dan amati estimasi biaya yang muncul.

> 💡 Angka per-request memang kecil. Tetapi pada aplikasi production dengan ribuan request/hari, jumlah ini cepat membengkak. Membiasakan diri memantau token sejak awal adalah disiplin yang baik.

---

## Latihan 5 — Tangani Kesalahan dengan Jelas

**Goal**: membangun kebiasaan menangani error secara graceful.

**Langkah:**

1. Eksperimen 1 — **API key salah**: ubah `ANTHROPIC_API_KEY` di `.env.local` menjadi nilai yang salah (misalnya tambah "x" di akhir). Jalankan. Catat pesan error yang muncul.
   **Error yang Anda lihat**:

2. Eksperimen 2 — **Tanpa env file**: jalankan tanpa flag `--env-file`:
   ```bash
   npx tsx experiments/claude-test.ts
   ```
   Catat error yang muncul.
   **Error yang Anda lihat**:

3. Eksperimen 3 — **Model tidak valid**: ubah `model: "claude-haiku-4-5"` menjadi `model: "claude-imaginary-99"`. Jalankan. Catat error.
   **Error yang Anda lihat**:

4. Setelah eksperimen, **kembalikan** semua konfigurasi ke nilai yang benar.

> 💡 Tujuannya: ketika di production Anda menemui error tersebut, Anda sudah familiar dengan pola pesannya — bukan baru kali pertama melihat.

---

## Latihan 6 — Validasi Akhir

Pastikan checklist berikut tercentang sebelum melanjutkan ke section/material berikutnya:

- [ ] Latihan 1: telah mencoba minimal 3 prompt berbeda dan mengamati respons.
- [ ] Latihan 2: telah memahami pengaruh `max_tokens` terhadap output.
- [ ] Latihan 3: telah membandingkan minimal 2 model yang berbeda.
- [ ] Latihan 4: estimasi biaya muncul di terminal.
- [ ] Latihan 5: telah sengaja membuat 3 jenis error dan membaca pesannya.
- [ ] File `experiments/claude-test.ts` sekarang dapat dijalankan ulang sewaktu-waktu tanpa error.

---

## Refleksi (Opsional)

Tuliskan pada catatan pribadi Anda:

1. Hal yang **paling mengejutkan** dari respons Claude di Latihan 1?
2. Apakah Anda mendapati **batasan** yang menurut Anda penting untuk diperhatikan (misalnya respons yang tidak sesuai harapan)?
3. Apabila harus memilih satu model untuk fitur Fin-App nanti, **model mana** yang akan Anda pilih dan **mengapa**?
4. Pertanyaan apa yang **belum terjawab** dari section pertama ini, yang ingin Anda tanyakan lebih lanjut?

---

## Apa Selanjutnya?

Section berikutnya dari Module 03 akan membahas:

- **System prompt** — mengontrol kepribadian dan gaya jawaban Claude.
- **Multi-turn conversation** — membangun percakapan yang memorable.
- **Streaming** — menampilkan respons kata-demi-kata seperti aplikasi chat.
- **Tool use** — memungkinkan Claude memanggil fungsi Anda sendiri.
- **Integrasi ke Fin-App** — akhirnya menyambungkan API ini ke aplikasi nyata.

Untuk sekarang, pastikan koneksi pertama Anda sudah solid. Selamat — Anda sudah resmi memanggil Claude API.

---

## Latihan Tambahan — Persiapan Module 04

- **[Latihan UI Chatbot — Bangun Panel Chatbot AI Financial Advisor](./latihan-ui-chatbot.md)** (45–60 menit)
  Latihan pure-UI tanpa logic API. Hasilnya jadi panel chatbot kosong yang siap dihubungkan ke Claude API di Module 04.
