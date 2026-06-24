# Section 2 — Output Control

> Bagian dari **[Module 05 — Latihan](./latihan.md)**. Lanjutan dari **[Section 1 — System Instruction](./latihan-1-system-instruction.md)**.

> Latihan ini fokus mengontrol *bagaimana* AI Financial Advisor merespons di chatbot — panjang, format, gaya, dan apa yang tidak boleh dijawab. Anda akan **memperketat `ADVISOR_SYSTEM`** + tambah guardrail `stop_sequences` + tune `max_tokens`, lalu verifikasi konsistensi dengan 5 test case. Teori sudah dibahas di `materi.md`; di sini fokus eksekusi.
>
> **Estimasi**: 45–60 menit.

## Prasyarat Section 2

- [ ] Section 1 selesai. AI Advisor pakai parameter `system` lewat `ADVISOR_SYSTEM` di `src/features/prompts.ts`.
- [ ] Anda sudah membaca bagian Section 2 di `materi.md` (tiga lapis kontrol output, `stop_sequences`, `max_tokens` strategy, refusal pattern).

---

## 📚 Referensi Dokumentasi

Sebelum mulai, buka tab dokumentasi resmi untuk referensi cepat:

- **[Messages API parameters](https://docs.claude.com/en/api/messages)** — `max_tokens`, `stop_sequences`, `stop_reason`, dan parameter terkait output control.
- **[Stop sequences](https://docs.claude.com/en/api/messages)** — cara pakai `stop_sequences` untuk batasi output di marker tertentu, dan apa yang muncul di `stop_reason`.
- **[Prompt engineering — be clear and direct](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/be-clear-and-direct)** — instruksi format yang ketat agar output konsisten.
- **[System prompts](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/system-prompts)** — pola refusal sopan via system instruction.

---

## Prompt 1 — Tighten `ADVISOR_SYSTEM` (Format & Batasan)

### Walkthrough Manual (sebelum pakai prompt)

Sebelum copy-paste prompt ke Claude, pahami dulu **bagian mana** dari `ADVISOR_SYSTEM` yang akan diperketat. Section 1 sudah membuat draft `ADVISOR_SYSTEM` dengan empat sub-section (Persona, Lingkup, Format Output, Batasan). Di Prompt 1 ini Anda **hanya memperketat dua sub-section**: `## Format Output` dan `## Batasan`. Persona dan Lingkup **tidak diubah**.

📂 **File yang diubah**: `src/features/prompts.ts` (modifikasi konstanta existing, BUKAN file baru)

**1. Perketat sub-section `## Format Output`**

📍 Lokasi: **di dalam template literal `ADVISOR_SYSTEM`**, ganti isi `## Format Output` dengan instruksi yang lebih spesifik dan eksplisit.

```ts
// src/features/prompts.ts — bagian Format Output (SESUDAH diperketat)
## Format Output
- Pertanyaan ringan: jawab **3–6 kalimat**. Pertanyaan kompleks: maksimal **8 bullet point**.
- TIDAK menulis prose mengalir lebih dari 1 paragraf.
- Format Rupiah: \`Rp 1.500.000\` (titik pemisah ribuan, TANPA "rupiah" atau "IDR").
- Format persen: \`15%\` (tanpa spasi sebelum %).
- Angka penting selalu **bold**.
- TIDAK memulai jawaban dengan filler: "Tentu", "Tentu saja", "Baik", "Tentunya", "Pertanyaan bagus" — langsung ke jawaban.
- TIDAK menulis disclaimer hukum / pajak / "konsultasi profesional" kecuali user secara eksplisit menanyakan aspek tersebut.
```

**2. Perketat sub-section `## Batasan` dengan refusal pattern**

📍 Lokasi: **di dalam template literal `ADVISOR_SYSTEM`**, ganti isi `## Batasan` agar berisi refusal pattern yang **elegan & in-character**.

```ts
// src/features/prompts.ts — bagian Batasan (SESUDAH diperketat)
## Batasan
- Untuk pertanyaan di luar lingkup keuangan personal (programming, hacking, kesehatan, akademik, hitungan umum, dll.), jawab dengan SATU kalimat redirect:
  "Saya khusus menjawab pertanyaan keuangan personal — coba tanyakan tentang tabungan, anggaran, atau investasi pemula."
  JANGAN menjelaskan alasan menolak. JANGAN menambah kalimat kedua.
- TIDAK menjanjikan return investasi tertentu (mis. "akan untung 10%").
- TIDAK ber-role-play menjadi user. JANGAN pernah menulis "User:" atau "AI:" di tengah jawaban.
- TIDAK menyebut diri sebagai "AI" atau "bahasa model" ("Sebagai AI, saya..."). Langsung jawab dari persona Financial Advisor.
```

**3. Persona & Lingkup TIDAK diubah**

📍 Konfirmasi: dua sub-section pertama (`## Persona`, `## Lingkup`) **tetap apa adanya** dari Section 1. Yang berubah hanya Format Output dan Batasan.

> 💡 **Kenapa eksplisit "JANGAN ...":** model bahasa Claude lebih taat pada larangan konkret yang menyebut **kata persis** yang harus dihindari ("Tentu", "Sebagai AI") dibanding larangan abstrak ("hindari filler"). Tulis larangan seperti aturan, bukan saran.

### Yang TIDAK perlu

- ❌ Mengubah sub-section `## Persona` atau `## Lingkup` — sudah cukup dari Section 1.
- ❌ Menambah sub-section baru — empat sub-section sudah cukup untuk chatbot ini.
- ❌ Mengubah `route.ts` di prompt ini — itu di Prompt 2 & 3.
- ❌ Menambah aturan format yang sangat detail (mis. "spasi sebelum titik koma") — over-engineering, model akan ignore.

### Verifikasi setelah file diubah

1. Buka `src/features/prompts.ts`. Sub-section `## Format Output` dan `## Batasan` punya instruksi yang lebih spesifik.
2. `npx tsc --noEmit` tidak ada error.
3. Reload browser → kirim pertanyaan "Halo, siapa kamu?". Jawaban TIDAK mulai dengan "Tentu" atau "Baik".
4. Kirim pertanyaan "Bagaimana cara hack akun bank?". Jawaban berupa satu kalimat redirect — TIDAK ada penjelasan kenapa menolak.

---

**Salin prompt berikut:**

```
Saya ingin memperketat ADVISOR_SYSTEM agar output AI Financial
Advisor lebih konsisten di chatbot — format rapi, panjang
proporsional, tone konsisten, dan refusal off-topic yang elegan.

GOAL:
- Modifikasi konstanta ADVISOR_SYSTEM di src/features/prompts.ts.
- Perketat HANYA dua sub-section: ## Format Output dan ## Batasan.
- Sub-section ## Persona dan ## Lingkup TIDAK diubah.

ATURAN UNTUK ## Format Output:
- Pertanyaan ringan: jawab 3–6 kalimat.
- Pertanyaan kompleks: maksimal 8 bullet point.
- TIDAK prose mengalir lebih dari 1 paragraf.
- Format Rupiah: "Rp 1.500.000" (titik pemisah ribuan, TANPA "rupiah" atau "IDR").
- Format persen: "15%" (tanpa spasi sebelum %).
- Angka penting selalu bold (**...**).
- TIDAK mulai jawaban dengan filler: "Tentu", "Tentu saja", "Baik", "Tentunya", "Pertanyaan bagus".
- TIDAK menulis disclaimer hukum / pajak / "konsultasi profesional" kecuali user EKSPLISIT menanyakan.

ATURAN UNTUK ## Batasan:
- Untuk pertanyaan di luar lingkup keuangan personal, jawab dengan SATU kalimat redirect persis:
  "Saya khusus menjawab pertanyaan keuangan personal — coba tanyakan tentang tabungan, anggaran, atau investasi pemula."
  JANGAN menjelaskan alasan menolak.
- TIDAK menjanjikan return investasi tertentu.
- TIDAK role-play sebagai user (tidak pernah menulis "User:" atau "AI:").
- TIDAK menyebut diri "Sebagai AI" — langsung jawab dari persona Advisor.

GUARDRAIL:
- JANGAN ubah Persona atau Lingkup.
- JANGAN tambah sub-section baru.
- JANGAN ubah file lain di prompt ini (route.ts dikerjakan terpisah).
- Tulis larangan dengan kata persis yang harus dihindari ("Tentu", "Sebagai AI") — bukan abstraksi.
```

**Verifikasi:**

1. Sub-section `## Format Output` dan `## Batasan` di `ADVISOR_SYSTEM` sudah diperketat sesuai walkthrough.
2. Reload browser → "Halo, siapa kamu?" → jawaban TIDAK mulai dengan "Tentu/Baik".
3. "Bagaimana cara hack akun bank?" → satu kalimat redirect, tanpa penjelasan tambahan.
4. `npx tsc --noEmit` clean.

---

## Prompt 2 — Tambah `stop_sequences` di Route Handler

### Walkthrough Manual (sebelum pakai prompt)

Sebelum copy-paste prompt, pahami kenapa kita tambah `stop_sequences` walau system prompt sudah ketat. `stop_sequences` adalah **brake darurat** — kalau Claude tetap "bocor" dan mulai mengeluarkan pattern terlarang (mis. "Disclaimer:", "Sebagai AI,"), generation berhenti **tepat sebelum** string itu masuk ke output user. Lapis kedua di atas system prompt.

📂 **File yang diubah**: `src/app/api/advisor/route.ts` (modifikasi, BUKAN file baru)

**1. Tambah parameter `stop_sequences` di `client.messages.stream(...)`**

📍 Lokasi: **di dalam handler `POST`**, di pemanggilan `client.messages.stream({ ... })` (yang sudah Anda set up di Module 04 + Section 1). Tambahkan parameter `stop_sequences` di samping `system` & `messages`.

```ts
// src/app/api/advisor/route.ts — di dalam POST handler
const stream = client.messages.stream({
  model: selectedModel,
  max_tokens: 1024,
  system: ADVISOR_SYSTEM,
  messages,
  stop_sequences: ["User:", "AI:", "Disclaimer:", "Sebagai AI,"],  /* ← BARU */
  // ...temperature, thinking, dst. dari Module 04 + Section 1 — pertahankan
});
```

**2. Apabila ada branching Opus (thinking) yang pakai `.create()` terpisah, tambahkan parameter yang sama di sana**

📍 Lokasi: kalau di route Anda ada cabang Opus dengan thinking aktif yang panggil API lewat method berbeda, pastikan `stop_sequences` ditambahkan **di kedua cabang** supaya konsisten.

> 💡 **Kenapa pilih 4 marker ini?** `"User:"` & `"AI:"` cegah role-play; `"Disclaimer:"` cegah disclaimer hukum yang user tidak minta; `"Sebagai AI,"` cegah AI-talk yang merusak persona. Marker ini cocok untuk chatbot finansial Bahasa Indonesia — kalau Anda buat domain lain, daftar markernya akan beda.

> ⚠️ **Hati-hati**: `stop_sequences` mengandalkan **string persis** (case-sensitive). `"Disclaimer:"` (D besar) berbeda dari `"disclaimer:"`. Untuk produksi, pertimbangkan menambah variasi kapitalisasi kalau muncul kebocoran.

### Yang TIDAK perlu

- ❌ Mengubah `ADVISOR_SYSTEM` lagi — itu sudah dikerjakan di Prompt 1.
- ❌ Menambah retry loop kalau `stop_sequences` ketrigger — kalau system prompt + `stop_sequences` sudah berjalan, brake-nya cukup.
- ❌ Mengubah struktur streaming — pertahankan persis dari Module 04 Section 6 + Section 1.
- ❌ Logging `stop_reason` di production — boleh saja untuk dev, tapi jangan jadi noise.

### Verifikasi setelah file diubah

1. `npx tsc --noEmit` tidak ada error.
2. Reload browser → kirim "Berikan tips menghemat pengeluaran bulanan". Jawaban TIDAK ada blok "Disclaimer: ..." di akhir.
3. (Opsional) Buka DevTools → Network → request `/api/advisor` → cek payload mengandung `stop_sequences` array.
4. Multi-turn tetap berfungsi normal (tidak ada regresi dari Section 1).

---

**Salin prompt berikut:**

```
Saya ingin menambahkan stop_sequences sebagai guardrail brake
darurat di route handler advisor — jaring pengaman kalau Claude
tetap "bocor" mengeluarkan pattern terlarang walau system prompt
sudah ketat.

GOAL:
- Modifikasi src/app/api/advisor/route.ts.
- Tambah parameter stop_sequences ke pemanggilan
  client.messages.stream({...}):
    stop_sequences: ["User:", "AI:", "Disclaimer:", "Sebagai AI,"]
- Apabila ada cabang Opus / thinking yang pakai method API
  berbeda (mis. .create), tambahkan parameter yang sama di sana
  supaya konsisten.

CONTEXT:
- ADVISOR_SYSTEM sudah diperketat di prompt sebelumnya
  (Format Output + Batasan).
- stop_sequences = lapis kedua. Yang utama tetap system prompt.

GUARDRAIL:
- JANGAN ubah ADVISOR_SYSTEM.
- JANGAN ubah struktur streaming atau penanganan thinking.
- JANGAN tambah retry kalau ketrigger.
- Apabila stop_reason tampil di log development, biarkan saja —
  TIDAK perlu dijadikan production log.
```

**Verifikasi:**

1. Reload browser → "Tips menghemat" → jawaban TIDAK ada bagian "Disclaimer:".
2. DevTools Network → request body mengandung `stop_sequences` array.
3. Multi-turn dari Section 1 masih jalan normal.

---

## Prompt 3 — Tune `max_tokens` (Default 512)

### Walkthrough Manual (sebelum pakai prompt)

Sebelum copy-paste prompt, pahami **kenapa 512 untuk default**. Pertanyaan chatbot finansial umumnya butuh jawaban ringkas (3–6 kalimat atau 8 bullet maksimum — sesuai aturan Format Output yang sudah Anda set di Prompt 1). 512 token cukup untuk jawaban itu, dan secara aktif **mencegah Claude menulis lebih panjang dari yang diminta**. Hemat biaya + hemat waktu user baca.

**Pengecualian**: saat thinking aktif (mode Opus), thinking token + final answer dihitung bersama dalam `max_tokens`. Di mode ini, biarkan 4096.

📂 **File yang diubah**: `src/app/api/advisor/route.ts` (modifikasi, BUKAN file baru)

**1. Ubah `max_tokens` default dari 1024 → 512**

📍 Lokasi: **di dalam handler `POST`**, di pemanggilan API saat thinking **TIDAK** aktif (mode Haiku default).

```ts
// src/app/api/advisor/route.ts — di dalam POST handler (non-thinking branch)
const stream = client.messages.stream({
  model: selectedModel,
  max_tokens: 512,                       /* ← DARI 1024 jadi 512 */
  system: ADVISOR_SYSTEM,
  messages,
  stop_sequences: ["User:", "AI:", "Disclaimer:", "Sebagai AI,"],
  temperature: 0.5,
});
```

**2. Apabila ada cabang thinking (Opus dengan extended thinking), pertahankan `max_tokens: 4096`**

📍 Lokasi: cabang yang aktif saat user menyalakan toggle thinking di UI (dari Module 04).

```ts
// src/app/api/advisor/route.ts — di dalam POST handler (thinking branch, Opus)
const stream = client.messages.stream({
  model: "claude-opus-4-5",
  max_tokens: 4096,                      /* ← TETAP 4096 saat thinking */
  thinking: { type: "enabled", budget_tokens: 2000 },
  system: ADVISOR_SYSTEM,
  messages,
  stop_sequences: ["User:", "AI:", "Disclaimer:", "Sebagai AI,"],
  temperature: 1,                        /* ← thinking wajib temperature: 1 (Module 04 constraint) */
});
```

> 💡 **Cara kerja `max_tokens` + system prompt**: dua kontrol ini saling perkuat. System prompt bilang "3–6 kalimat", `max_tokens: 512` adalah hard ceiling. Kalau system prompt gagal (Claude lupa aturan), `max_tokens` tetap memotong. Kalau `max_tokens` terlalu agresif (jawaban terpotong di tengah), system prompt yang akan keep things short sehingga `max_tokens` jarang ketrigger.

> ⚠️ **Sinyal `max_tokens` terlalu rendah**: kalau `stop_reason` di response sering = `"max_tokens"` (bukan `"end_turn"`), artinya Claude kena potong. Naikkan ke 768 atau 1024 dan periksa apakah system prompt-nya yang masih membiarkan jawaban kepanjangan.

### Yang TIDAK perlu

- ❌ Mengubah `temperature` — `0.5` (advisor non-thinking) & `1` (thinking) tetap dari Module 04.
- ❌ Mengubah model selection logic — `selectedModel` tetap ditentukan dari Module 04 (toggle Opus/Haiku).
- ❌ Menambah parameter dinamis `max_tokens` berdasarkan panjang pertanyaan — over-engineering untuk sekarang.
- ❌ Mengubah `stop_sequences` lagi — sudah dari Prompt 2.

### Verifikasi setelah file diubah

1. `npx tsc --noEmit` tidak ada error.
2. Reload browser → "Berapa idealnya dana darurat?" → jawaban masuk ke layar dalam **±1 detik streaming**, ringkas (sekitar 3–6 kalimat atau bullet pendek).
3. Coba pertanyaan panjang yang ideally butuh detail: "Jelaskan strategi reksadana untuk pensiun 30 tahun ke depan." → jawaban tetap di bawah 512 token, terstruktur dalam bullet.
4. (Opsional) DevTools Network → response → field `stop_reason` ideally = `"end_turn"` (Claude selesai sendiri sebelum kena cap), BUKAN `"max_tokens"`.
5. Toggle thinking (Opus) → kirim pertanyaan kompleks → jawaban tetap mengalir lengkap (karena `max_tokens: 4096` saat thinking).

---

**Salin prompt berikut:**

```
Saya ingin mengubah max_tokens default agar jawaban advisor
lebih ringkas dan hemat. Saat thinking aktif (Opus), max_tokens
tetap besar karena thinking token + final answer dihitung
bersama.

GOAL:
- Modifikasi src/app/api/advisor/route.ts.
- Ubah max_tokens dari 1024 menjadi 512 di cabang TANPA thinking
  (mode Haiku default).
- Pada cabang Opus + thinking (kalau ada), max_tokens TETAP 4096.

CONTEXT:
- ADVISOR_SYSTEM sudah membatasi jawaban: 3–6 kalimat untuk
  ringan, max 8 bullet untuk kompleks. 512 token CUKUP.
- temperature: 0.5 (advisor non-thinking), 1 (thinking). Tidak diubah.
- stop_sequences sudah ditambahkan di prompt sebelumnya — JANGAN
  diubah lagi.

GUARDRAIL:
- JANGAN ubah temperature.
- JANGAN ubah model selection / branching logic.
- JANGAN tambah max_tokens dinamis (over-engineering).
- Apabila ada cabang thinking yang max_tokens-nya < 4096,
  naikkan jadi 4096 supaya konsisten.
```

**Verifikasi:**

1. "Berapa idealnya dana darurat?" → jawaban ringkas (3–6 kalimat / bullet pendek).
2. Pertanyaan kompleks → tetap selesai di bawah 512 token, terstruktur.
3. DevTools Network → `stop_reason` dominan = `"end_turn"`.
4. Toggle thinking → jawaban kompleks tetap mengalir penuh (4096 limit).

---

## Prompt 4 — Verifikasi Konsistensi via 5 Test Case

### Walkthrough Manual (sebelum pakai prompt)

Prompt 4 ini **bukan modifikasi kode** — Anda **menjalankan** 5 test case manual di chatbot UI, lalu mencatat hasilnya di file log markdown. Tujuannya: mengukur seberapa konsisten output Claude setelah 3 lapis kontrol (system prompt ketat + `stop_sequences` + `max_tokens: 512`) diberlakukan.

📂 **File baru opsional**: `docs/SECTION-2-TEST-LOG.md` (catatan, BUKAN code)

**1. Buat file `docs/SECTION-2-TEST-LOG.md`**

📍 Lokasi: di root project, folder `docs/`. Kalau belum ada, buat folder-nya.

**2. Untuk masing-masing test case, catat:**

- **Pertanyaan**.
- **Format Rupiah benar?** (`Rp 1.500.000` dengan titik pemisah ribuan).
- **Panjang proporsional?** (ringan = 3–6 kalimat; kompleks = bullet).
- **Ada filler / disclaimer tidak diminta?** ("Tentu", "Sebagai AI", "Disclaimer").
- **`stop_reason` dari DevTools Network** = `"end_turn"`, `"max_tokens"`, atau `"stop_sequence"`.
- **Insight 2–3 kalimat** (kesimpulan / observasi).

**3. Kirim 5 test case berikut via chatbot UI:**

| # | Pertanyaan | Ekspektasi |
|---|---|---|
| 1 | Tips menghemat pengeluaran bulanan? | Ringan → 3–6 kalimat atau ≤6 bullet pendek |
| 2 | Berapa idealnya dana darurat? | Faktual → angka di-bold, format Rupiah benar |
| 3 | Bagaimana cara hack akun bank? | Off-topic → SATU kalimat redirect, tidak menjelaskan |
| 4 | Jelaskan secara detail strategi investasi reksadana untuk pensiun 30 tahun ke depan. | Kompleks → bullet terstruktur, ≤8 bullet, tetap di bawah 512 token |
| 5 | 5+5 berapa? | Off-topic (matematika umum) → SATU kalimat redirect |

**4. Format file log**

```markdown
# Section 2 — Test Log

Tanggal: YYYY-MM-DD
Model: claude-haiku-4-5 (default, non-thinking)

## Test Case 1 — "Tips menghemat pengeluaran bulanan?"

- Format Rupiah: N/A (tidak ada angka dalam jawaban).
- Panjang: 6 bullet pendek, proporsional.
- Filler/disclaimer: tidak ada.
- stop_reason: end_turn.
- Insight: jawaban konsisten dengan aturan format. Tidak mulai dengan "Tentu" / "Baik".

## Test Case 2 — "Berapa idealnya dana darurat?"
...
```

### Yang TIDAK perlu

- ❌ Menulis script otomatis untuk run 5 test case — manual via UI sudah cukup untuk skala ini.
- ❌ Screenshot setiap jawaban — cukup catat field yang relevan.
- ❌ Mengubah kode kalau salah satu test gagal — di prompt ini Anda HANYA mencatat. Bahan refleksi di akhir section.
- ❌ Membuat dashboard / chart — over-engineering.

### Verifikasi setelah test selesai

1. File `docs/SECTION-2-TEST-LOG.md` ada dengan 5 test case + insight.
2. Mayoritas (4 dari 5) `stop_reason` = `"end_turn"` (Claude selesai sendiri, bukan kena cap).
3. Tidak ada test case yang mengandung filler ("Tentu", "Sebagai AI") atau disclaimer tidak diminta.
4. Test case 3 dan 5 (off-topic) menggunakan kalimat redirect persis seperti yang ditulis di `## Batasan`.

---

**Salin prompt berikut:**

```
Saya ingin memverifikasi konsistensi output AI Financial Advisor
setelah memperketat ADVISOR_SYSTEM + menambah stop_sequences +
menurunkan max_tokens jadi 512. Hasil verifikasi dicatat di file
markdown.

GOAL:
- Buat file docs/SECTION-2-TEST-LOG.md.
- Format: satu sub-section per test case dengan field:
  Pertanyaan, Format Rupiah, Panjang, Filler/disclaimer,
  stop_reason, Insight (2–3 kalimat).
- Isi log dengan 5 test case di bawah ini berdasarkan pengujian
  manual via chatbot UI.

TEST CASES:
1. "Tips menghemat pengeluaran bulanan?" (ringan)
2. "Berapa idealnya dana darurat?" (faktual, butuh angka)
3. "Bagaimana cara hack akun bank?" (off-topic — redirect)
4. "Jelaskan secara detail strategi investasi reksadana untuk pensiun 30 tahun ke depan." (kompleks)
5. "5+5 berapa?" (off-topic — redirect singkat)

CARA:
- Saya akan jalankan satu per satu di chatbot UI.
- Untuk masing-masing, saya ambil stop_reason dari DevTools
  Network response.
- Setelah 5 selesai, log akan saya isi.

GUARDRAIL:
- File log = CATATAN, bukan code yang dieksekusi.
- JANGAN buat script otomatis runner — manual cukup.
- JANGAN modifikasi kode advisor di prompt ini.
- Apabila salah satu test menunjukkan filler atau disclaimer
  bocor, CATAT itu — jangan langsung patch di sini (bahan
  refleksi & iterasi prompt).
```

**Verifikasi:**

1. File `docs/SECTION-2-TEST-LOG.md` ada dengan 5 entri test case.
2. Setiap entri punya field lengkap (Pertanyaan, Format Rupiah, Panjang, Filler, stop_reason, Insight).
3. Mayoritas `stop_reason` = `"end_turn"`.
4. Test case 3 & 5 dijawab dengan kalimat redirect persis (atau sangat dekat) dengan yang ditulis di `## Batasan`.

---

## Validasi Akhir Section 2

- [ ] `ADVISOR_SYSTEM` di `src/features/prompts.ts` punya instruksi format yang ketat (panjang, Rupiah, anti-filler, refusal pattern).
- [ ] `stop_sequences` aktif di route handler advisor (`["User:", "AI:", "Disclaimer:", "Sebagai AI,"]`).
- [ ] `max_tokens` default 512 (Haiku), 4096 (Opus dengan thinking).
- [ ] 5 test case di `docs/SECTION-2-TEST-LOG.md` menunjukkan output konsisten.
- [ ] Build production sukses (`npm run build`).
- [ ] Tidak ada regresi: Module 04 features (streaming, multi-turn, toggle thinking) tetap jalan.

## Refleksi Section 2

1. Saat tighten `ADVISOR_SYSTEM`, instruksi mana yang Claude paling sulit patuhi? (mis. "jangan mulai dengan 'Tentu'" sering bocor.)
2. `stop_sequences` Anda kena trigger berapa kali di 5 test case? Itu sinyal `system prompt` Anda masih kurang ketat di area mana?
3. Default `max_tokens: 512` — apakah ada pertanyaan yang malah jadi terlalu pendek karena terpotong? Bagaimana Anda akan handle (raise limit conditional? minta user follow-up?)
4. Pertanyaan off-topic dijawab dengan refusal yang singkat — apakah UX-nya cukup ramah, atau terasa "robotic"? Bagaimana Anda akan tune?
5. Apa risiko terbesar dari output control terlalu ketat? (mis. Claude jadi tidak fleksibel saat user butuh format khusus.)

---

⬅️ Kembali: **[Section 1](./latihan-1-system-instruction.md)** · ➡️ Lanjut: **[Section 3 — Role, Context, Instruction](./latihan-3-rci.md)**
