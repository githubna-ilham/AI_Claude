# Section 4 — Agentic Workflow

> Bagian dari **[Module 05 — Latihan](./latihan.md)**. Lanjutan dari **[Section 3 — Role, Context, Instruction](./latihan-3-rci.md)**.

> Latihan ini menerapkan **5-step reasoning workflow** (Information Extraction → Thought → Action Planning → Evaluation → Response Generation) ke `ADVISOR_SYSTEM` agar Claude memiliki struktur berpikir terstruktur saat menjawab pertanyaan kompleks. **TIDAK ada tool use / function calling** di section ini — semua dilakukan via prompting di system instruction.
>
> **Estimasi**: 50–70 menit.

## Prasyarat Section 4

- [ ] Section 1–3 selesai. `ADVISOR_SYSTEM` sudah pakai pola RCI.
- [ ] Anda sudah membaca bagian Section 4 di `materi.md` (lima tahap workflow + contoh sebelum/sesudah).
- [ ] AI Advisor saat ini bisa jawab pertanyaan sederhana dengan baik.

---

## 📚 Referensi Dokumentasi

- **[Prompt engineering — Chain of Thought](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/chain-of-thought)** — pola "let's think step by step" dan variannya.
- **[System prompts best practices](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/system-prompts)** — cara menambah workflow instructions tanpa over-engineering.
- **[Extended thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking)** — fitur Opus 4.7 yang berbeda dengan workflow di section ini (perbandingan ada di materi.md).
- **[Evaluating LLM outputs](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering)** — bagaimana mengukur kualitas jawaban setelah perubahan prompt.

---

## Prompt 1 — Tambah 5-Step Workflow ke `ADVISOR_SYSTEM`

### Walkthrough Manual (sebelum pakai prompt)

Sebelum copy-paste prompt, pahami persis instruksi yang akan disisipkan ke `ADVISOR_SYSTEM` (yang sudah dibangun di Section 1 + RCI di Section 3). Workflow ditambahkan sebagai **section baru** di system prompt — tidak mengganti bagian Persona / Format / Batasan yang sudah ada.

📂 **File yang diubah**: `src/features/prompts.ts` (modifikasi `ADVISOR_SYSTEM`)

**1. Tambah subsection "Cara Berpikir Sebelum Menjawab"**

📍 Lokasi: **di dalam string `ADVISOR_SYSTEM`**, sebelum bagian "## Format Output" atau di akhir setelah "## Batasan" — pilih yang paling masuk akal di struktur Anda saat ini.

```ts
// src/features/prompts.ts — di dalam ADVISOR_SYSTEM
export const ADVISOR_SYSTEM = `
[... bagian Persona, Lingkup, Format Output, Batasan dari Section 1+3 ...]

## Cara Berpikir Sebelum Menjawab

Untuk SETIAP pertanyaan user, ikuti workflow berikut secara internal (JANGAN tampilkan langkah 1-4 ke user, HANYA hasilnya di langkah 5):

1. **Information Extraction** — identifikasi:
   - Profil user (pemula? sudah berpengalaman? sedang merencanakan?)
   - Niat sebenarnya (planning / informasi / validation?)
   - Data eksplisit di pertanyaan (angka, jangka waktu, kondisi)
   - Data implisit yang harus diasumsikan atau diminta

2. **Thought** — analisis masalah inti:
   - Apa constraint utama yang user hadapi?
   - Asumsi apa yang harus dieksplisitkan?
   - Trade-off relevan?

3. **Action Planning** — susun kerangka jawaban:
   - Berapa sub-topik yang perlu dibahas?
   - Urutan paling masuk akal?
   - Bagian mana rinci, bagian mana ringkas?

4. **Evaluation** — review rencana sebelum menulis:
   - Apakah semua bagian menjawab pertanyaan user?
   - Adakah kontradiksi internal?
   - Apakah actionable (user tahu apa yang harus dilakukan)?
   - Apakah format sesuai aturan di section "Format Output"?

5. **Response Generation** — tulis jawaban final yang user lihat.

Apabila pertanyaan **sederhana** (faktual, satu kalimat jawabnya cukup), tahap 1-4 boleh Anda lakukan singkat — tetap eksis di pikiran Anda, tetapi tidak perlu mendetail.
`.trim();
```

**2. Posisi yang disarankan di struktur prompt**

📍 Workflow ditempatkan **setelah Batasan** (paling akhir) supaya:

- Persona / Lingkup / Format Output / Batasan tetap dibaca duluan sebagai "identity + rules".
- Workflow menjadi "how to think" — diaplikasikan setelah Claude tahu siapa dirinya dan apa rules-nya.

**3. Eksplisitkan "TIDAK tampilkan ke user"**

💡 Tanpa instruksi eksplisit, Claude kadang bocorkan workflow sebagai bullet list "Step 1: Information Extraction..." di output. Tambahkan klausa tegas:

```
JANGAN tampilkan langkah 1-4 sebagai output ke user.
HANYA hasil langkah 5 yang user lihat.
```

### Yang TIDAK perlu (Prompt 1)

- ❌ Menampilkan chain-of-thought ke user — workflow ada di "pikiran" Claude, output user-facing hanya hasil step 5.
- ❌ Mengubah Persona / Lingkup / Format Output yang sudah ada di Section 1+3.
- ❌ Memodifikasi route handler atau component — perubahan hanya di prompts.ts.
- ❌ Menambah parameter API baru (workflow murni via prompting).
- ❌ Implementasi tool use / function calling — itu modul lanjutan, bukan section ini.

### Verifikasi setelah file diubah (Prompt 1)

1. `npx tsc --noEmit` tanpa error.
2. Buka `src/features/prompts.ts`, pastikan section "Cara Berpikir Sebelum Menjawab" ada di dalam `ADVISOR_SYSTEM`.
3. Section lain (Persona, Lingkup, Format Output, Batasan) tetap utuh.
4. Reload chatbot. Kirim pertanyaan kompleks: "Bagaimana saya nabung Rp 200jt dalam 3 tahun?"
5. Output Claude sekarang **lebih terstruktur** — biasanya ada angka konkret + skenario kondisional + closing yang minta info follow-up. (TIDAK ada teks "Step 1:", "Step 2:" — itu indikator workflow bocor ke output.)

---

**Salin prompt berikut:**

```
Tambahkan 5-step reasoning workflow ke ADVISOR_SYSTEM agar
Claude lebih terstruktur saat menjawab pertanyaan kompleks.

GOAL:
- Modifikasi src/features/prompts.ts.
- Tambah subsection "## Cara Berpikir Sebelum Menjawab"
  di dalam ADVISOR_SYSTEM, di posisi yang masuk akal
  (umumnya setelah Batasan, sebelum/sesudah Format Output —
  pilih yang paling natural).
- Isi subsection 5 langkah workflow:
  1. Information Extraction — identifikasi profil user,
     niat, data eksplisit/implisit.
  2. Thought — analisis masalah inti, constraint, trade-off.
  3. Action Planning — susun kerangka jawaban.
  4. Evaluation — review rencana untuk completeness,
     consistency, actionability, format compliance.
  5. Response Generation — tulis jawaban final.

CONTEXT:
- workflow ini ada di "pikiran" Claude — TIDAK ditampilkan
  ke user. User hanya melihat hasil langkah 5.
- Untuk pertanyaan sederhana, langkah 1-4 boleh dilakukan
  singkat.
- File: src/features/prompts.ts (modifikasi konstanta
  ADVISOR_SYSTEM).

GUARDRAIL:
- JANGAN ubah bagian Persona, Lingkup, Format Output,
  Batasan yang sudah ada di Section 1+3.
- JANGAN tambah parameter API baru di route handler.
- JANGAN implementasi tool use — workflow ini murni via
  prompting.
- Eksplisit instruksikan Claude: "JANGAN tampilkan langkah
  1-4 ke user" — supaya output tidak bocor.
```

**Verifikasi:**

1. File terupdate dengan section workflow baru.
2. Pertanyaan kompleks ("Bagaimana nabung 200jt dalam 3 tahun?") dijawab lebih terstruktur — ada angka, skenario, closing.
3. Tidak ada teks "Step 1:", "Step 2:" di output (workflow tidak bocor).

---

## Prompt 2 — Test Konsistensi via 5 Pertanyaan Kompleks

### Walkthrough Manual (sebelum pakai prompt)

Untuk membuktikan workflow bekerja, kita perlu membandingkan kualitas jawaban **dengan** workflow vs **tanpa** workflow. Catat hasil ke file dokumentasi.

📂 **File baru**: `docs/SECTION-4-WORKFLOW-LOG.md` (markdown log, BUKAN kode)

**1. Siapkan 5 pertanyaan test**

Pilihan yang mencakup berbagai kompleksitas:

```markdown
# Test Cases — Section 4 Workflow

## Pertanyaan
1. (Kompleks planning) "Bagaimana saya bisa nabung Rp 200jt dalam 3 tahun?"
2. (Faktual sederhana) "Berapa idealnya emergency fund?"
3. (Analisis trade-off) "Mendingan beli rumah cash atau KPR?"
4. (Multi-aspek) "Saya pemula investasi, mulai dari mana?"
5. (Off-topic edge) "Cara hack akun bank?"
```

**2. Test setiap pertanyaan via chatbot 2x — sebelum & sesudah workflow**

📍 Cara membandingkan:

- **Sebelum**: revert `ADVISOR_SYSTEM` sementara (atau pakai test akun terpisah / git stash perubahan Prompt 1).
- **Sesudah**: dengan workflow aktif.

Catat output **mentah** ke log untuk masing-masing.

**3. Evaluasi per pertanyaan dengan rubrik**

Untuk setiap pasangan jawaban, nilai:

| Kriteria | Sebelum (1-5) | Sesudah (1-5) | Catatan |
|---|---|---|---|
| **Relevansi konteks** (jawaban adaptif ke user?) | | | |
| **Kedalaman** (dangkal vs solid) | | | |
| **Actionability** (user tahu next step?) | | | |
| **Format compliance** (aturan Rupiah, panjang?) | | | |
| **Structured** (terorganisir?) | | | |

⚠️ Jangan terjebak skor angka — kolom "Catatan" lebih penting karena memuat observasi yang akan dipakai di Prompt 3 (tuning).

### Yang TIDAK perlu (Prompt 2)

- ❌ Eksperimen di `experiments/` folder — log ini adalah dokumentasi, simpan di `docs/`.
- ❌ Test automation — manual review cukup untuk fase ini.
- ❌ Statistik formal — observasi qualitative lebih relevan dari p-value.
- ❌ Test puluhan pertanyaan — 5 yang berkualitas lebih informatif dari 50 yang random.

### Verifikasi setelah dokumentasi dibuat (Prompt 2)

1. `docs/SECTION-4-WORKFLOW-LOG.md` ada dengan 5 pertanyaan + 2 set jawaban + rubrik per pertanyaan.
2. Total skor **sesudah > sebelum** di mayoritas kriteria untuk pertanyaan kompleks (1, 3, 4).
3. Pertanyaan sederhana (2) menunjukkan **sedikit perbaikan** — workflow tidak overkill.
4. Pertanyaan off-topic (5) tetap di-refuse dengan elegan (dari Section 2).

---

**Salin prompt berikut:**

```
Buat dokumentasi pembandingan kualitas jawaban sebelum vs
sesudah menambah 5-step workflow ke ADVISOR_SYSTEM.

GOAL:
- Buat file docs/SECTION-4-WORKFLOW-LOG.md.
- Daftar 5 pertanyaan test (mix kompleksitas):
  1. Pertanyaan planning multi-step (mis. tabungan jangka
     panjang)
  2. Pertanyaan faktual sederhana (mis. ideal emergency fund)
  3. Pertanyaan trade-off (mis. cash vs KPR)
  4. Pertanyaan multi-aspek (mis. mulai investasi)
  5. Pertanyaan off-topic (mis. cara hack)
- Untuk setiap pertanyaan, sediakan template untuk catat:
  - Output Claude SEBELUM workflow (versi pre-Section 4)
  - Output Claude SESUDAH workflow (versi current)
  - Rubrik evaluasi (5 kriteria, skor 1-5)
  - Catatan kualitatif

CONTEXT:
- Workflow sudah aktif dari Prompt 1.
- Manual review oleh developer/AI engineer.

GUARDRAIL:
- File ini di docs/, BUKAN src/.
- JANGAN kode automation testing — manual review.
- Format markdown rapi supaya bisa dilihat di GitHub render.
- Sediakan template kosong supaya peserta latihan bisa isi.
```

**Verifikasi:**

1. File log ada dengan template lengkap.
2. Peserta dapat isi tabel rubrik untuk masing-masing pertanyaan.

---

## Validasi Akhir Section 4

- [ ] `ADVISOR_SYSTEM` di `src/features/prompts.ts` punya section "Cara Berpikir Sebelum Menjawab" dengan 5 langkah.
- [ ] Workflow ada di "pikiran" Claude — TIDAK bocor sebagai "Step 1:", "Step 2:" di output user.
- [ ] `docs/SECTION-4-WORKFLOW-LOG.md` berisi 5 pertanyaan test + rubrik evaluasi sebelum vs sesudah.
- [ ] Pertanyaan kompleks menunjukkan output lebih terstruktur dan actionable.
- [ ] Pertanyaan sederhana tetap proporsional (tidak overengineered).
- [ ] Off-topic tetap di-refuse dengan elegan (dari Section 2 Batasan).
- [ ] Build production sukses (`npm run build`).
- [ ] Tidak ada regresi dari Section 1, 2, 3.

## Refleksi Section 4

1. Manakah dari 5 langkah workflow yang paling sering Claude "skip" atau lakukan dengan dangkal? Mengapa menurut Anda?
2. Untuk pertanyaan sederhana (faktual, satu-kalimat), apakah workflow membuat output jadi terlalu panjang/overthinking? Bagaimana Anda akan handle (toggle workflow, conditional, atau biarkan?)
3. Apa beda kualitatif paling jelas antara **Extended Thinking** (Module 04) dan **Workflow di prompt** (Section 4 ini)? Kapan Anda akan pakai mana?
4. Andai workflow ini di-bocorkan ke user (misal step 1-4 terlihat sebagai output), apa risiko UX-nya? Bagaimana Anda mencegahnya?
5. Bagaimana cara monitor di production apakah workflow konsisten dipatuhi Claude? (mis. sampling output, eval set bulanan, user feedback)

---

⬅️ Kembali: **[Section 3 — Role, Context, Instruction](./latihan-3-rci.md)** · ➡️ Lanjut: **[Section 5 — Structured Output (JSON)](./latihan-5-structured-output.md)** · 🏠 Index: **[Module 05 — Latihan](./latihan.md)**
