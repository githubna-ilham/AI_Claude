# Section 3 — Role, Context, & Instruction

> Bagian dari **[Module 05 — Latihan](./latihan.md)**. Lanjutan dari **[Section 2 — Output Control](./latihan-2-output-control.md)**.

> Latihan restrukturisasi system prompt dengan pola RCI dan demonstrasi reuse. Dua prompt siap copy-paste.
>
> **Estimasi**: 35–45 menit.

## Prasyarat Section 3

- [ ] Section 1–2 selesai.

---

## 📚 Referensi Dokumentasi

Sebelum mulai, akan sangat membantu kalau Anda buka tab dokumentasi resmi untuk referensi cepat:

- **[Prompt engineering — system prompts](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/system-prompts)** — best practices struktur system prompt yang scalable.
- **[Prompt composition patterns](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering)** — pola RCI (Role-Context-Instruction) dan structured prompts.
- **[Multi-mode AI (system + variant)](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering)** — cara pisah persona dari instruction agar reuse di banyak fitur.

---

## Prompt 1 — Refactor `prompts.ts` ke Pola RCI

### Walkthrough Manual (sebelum pakai prompt)

Sebelum copy-paste prompt, pahami **mengapa** kita pecah `ADVISOR_SYSTEM` menjadi 4 konstanta: agar **reuse** di fitur lain (Insight, Parser, dst.) tanpa duplikasi.

📂 **File yang diubah**: `src/features/prompts.ts` (refactor, bukan rewrite)

**1. Pecah `ADVISOR_SYSTEM` menjadi 4 konstanta string**

📍 Lokasi: **module level**, di atas konstanta gabungan. Setiap konstanta = satu blok semantik.

```ts
// src/features/prompts.ts — module level
export const ADVISOR_ROLE = `
Anda adalah AI Financial Advisor untuk Fin-App.
Gaya: ramah, to-the-point, profesional. Bahasa Indonesia.
`.trim();

export const ADVISOR_CONTEXT = `
User adalah pengguna aplikasi pencatat keuangan personal.
Domain: pengeluaran, tabungan, budget, investasi pemula.
`.trim();

export const ADVISOR_FORMAT = `
- Markdown rapi (list bertanda, bold untuk angka penting).
- Format mata uang: Rp 1.500.000.
- Persentase: 15%.
- Hindari paragraf panjang — bullet bila memungkinkan.
`.trim();

export const ADVISOR_INSTRUCTION = `
Jawab pertanyaan user tentang keuangan personal mereka.
Batasan:
- JANGAN beri nasihat hukum/pajak spesifik.
- JANGAN janjikan return investasi.
- Apabila pertanyaan di luar lingkup, arahkan kembali.
`.trim();
```

**2. Update `ADVISOR_SYSTEM` dengan template literal RCI**

📍 Lokasi: **module level**, setelah 4 konstanta di atas. Pakai heading `# ROLE`, `# CONTEXT`, dst. agar Claude bisa "membaca" struktur.

```ts
// src/features/prompts.ts — module level
export const ADVISOR_SYSTEM = `
# ROLE
${ADVISOR_ROLE}

# CONTEXT
${ADVISOR_CONTEXT}

# OUTPUT FORMAT
${ADVISOR_FORMAT}

# INSTRUCTION
${ADVISOR_INSTRUCTION}
`.trim();
```

**3. Update alias `ADVISOR_SYSTEM`**

📍 Lokasi: **module level**, di bagian bawah. Pertahankan ekspor lama supaya tidak break import di `route.ts`.

```ts
// src/features/prompts.ts — module level
// ADVISOR_SYSTEM sudah diupdate langsung — tidak perlu alias
```

> 💡 **Diskriminasi blok**: `ROLE` = identitas Claude. `CONTEXT` = situasi user. `FORMAT` = aturan output. `INSTRUCTION` = tugas + batasan. Kalau bingung mana blok mana, anggap blok = jawaban untuk satu pertanyaan: siapa? di mana? bagaimana? apa?

### Yang TIDAK perlu

- ❌ Mengubah **konten** prompt — hanya restrukturisasi tata letak.
- ❌ `ADVISOR_ROLE` mengandung instruksi tugas (itu bagian INSTRUCTION).
- ❌ `ADVISOR_CONTEXT` mengandung aturan format (itu bagian FORMAT).
- ❌ Modifikasi `route.ts` — alias `ADVISOR_SYSTEM` jaga backward-compat, route tidak perlu diubah.

### Verifikasi setelah file diubah

1. File `prompts.ts` punya 4 konstanta terpisah + `ADVISOR_SYSTEM` yang diupdate.
2. Jalankan `npx tsc --noEmit` — tidak ada error.
3. Reload chatbot, kirim pertanyaan persona ("Halo, siapa kamu?") — respons konsisten dengan Section 1–2.
4. Kirim pertanyaan format ("Berikan 3 tips menabung") — format markdown + bullet tetap rapi.
5. Inspect `ADVISOR_SYSTEM` dengan `console.log` — strukturnya jelas terbagi 4 blok.

---

**Salin prompt berikut:**

```
Saya ingin merestrukturisasi system prompt dengan pola
Role-Context-Instruction yang modular.

GOAL:
- Refactor src/features/prompts.ts.
- Pecah ADVISOR_SYSTEM menjadi 4 konstanta terpisah:
  - ADVISOR_ROLE: persona Claude (1 paragraf).
  - ADVISOR_CONTEXT: konteks user dan domain (1-2 paragraf).
  - ADVISOR_FORMAT: aturan format output (list).
  - ADVISOR_INSTRUCTION: tugas dan batasan utama.

- Komposisi: update ADVISOR_SYSTEM dengan template
  literal yang menggabungkan 4 konstanta.

- Struktur final:
  # ROLE
  ${ADVISOR_ROLE}
  
  # CONTEXT
  ${ADVISOR_CONTEXT}
  
  # OUTPUT FORMAT
  ${ADVISOR_FORMAT}
  
  # INSTRUCTION
  ${ADVISOR_INSTRUCTION}

- Update ADVISOR_SYSTEM agar menggabungkan 4 konstanta.

CONTEXT:
- ADVISOR_SYSTEM yang lama akan digantikan langsung.

GUARDRAIL:
- JANGAN ubah konten — hanya restrukturisasi.
- Perilaku chatbot dari Section 1–2 harus tetap lolos.
- ADVISOR_ROLE jangan mengandung instruksi tugas (itu
  bagian INSTRUCTION).
- ADVISOR_CONTEXT jangan mengandung instruksi format
  (itu bagian FORMAT).
```

**Verifikasi:**

1. File prompts.ts memiliki konstanta terpisah: ADVISOR_ROLE, ADVISOR_CONTEXT, ADVISOR_FORMAT, ADVISOR_INSTRUCTION.
2. ADVISOR_SYSTEM menggabungkan keempatnya.
3. Aplikasi tetap pakai ADVISOR_SYSTEM — tidak ada perubahan di route.ts.
4. Chatbot tetap berfungsi seperti di Section 1–2.

### Efek Perubahan — Contoh Konkret

Refactor ini **tidak mengubah jawaban Claude secara dramatis** (konten prompt sama), tapi mengubah dua hal: (a) cara Claude "membaca" struktur, dan (b) cara Anda mengembangkan fitur selanjutnya.

**Sebelum (monolitik):**

```ts
export const ADVISOR_SYSTEM = `
Anda adalah AI Financial Advisor untuk Fin-App. Gaya ramah,
to-the-point, profesional. Bahasa Indonesia. User adalah pengguna
aplikasi pencatat keuangan personal... Format markdown rapi,
mata uang Rp 1.500.000... Jawab pertanyaan user. JANGAN beri
nasihat hukum...
`.trim();
```

**Sesudah (RCI terstruktur):**

```
# ROLE
Anda adalah AI Financial Advisor untuk Fin-App. Gaya: ramah...

# CONTEXT
User adalah pengguna aplikasi pencatat keuangan personal...

# OUTPUT FORMAT
- Markdown rapi (list bertanda, bold untuk angka penting).
- Format mata uang: Rp 1.500.000.
...

# INSTRUCTION
Jawab pertanyaan user tentang keuangan personal mereka.
Batasan: JANGAN beri nasihat hukum/pajak spesifik...
```

**Efek yang terukur:**

| Aspek | Sebelum (monolitik) | Sesudah (RCI) |
|---|---|---|
| **Konsistensi format** | Kadang Claude lupa bold angka pada jawaban panjang | Lebih konsisten — heading `# OUTPUT FORMAT` membuat aturan format "menonjol" |
| **Tambah aturan baru** | Edit string panjang, takut nabrak instruksi lain | Edit 1 konstanta (mis. `ADVISOR_FORMAT`) tanpa sentuh blok lain |
| **Reuse untuk fitur lain** | Harus copy-paste seluruh prompt, lalu edit | Tinggal ganti 1 blok (lihat Prompt 2) |
| **Debug prompt** | Sulit lokalisir bagian mana yang "bocor" | Bisa toggle 1 blok at-a-time untuk isolasi |

**Contoh jawaban yang sama dari user prompt "Berapa idealnya dana darurat?":**

- **Sebelum**: kadang muncul tanpa bold di angka (`Rp 30.000.000` plain text), kadang dengan bold.
- **Sesudah**: lebih sering konsisten — angka di-bold (`**Rp 30.000.000**`), bullet rapi, tidak ada paragraf panjang.

> 💡 **Catatan**: Perubahan ini lebih "developer experience" daripada "user experience". User hampir tidak melihat bedanya untuk 1 fitur — payoff sesungguhnya muncul di Prompt 2 saat kita reuse blok untuk fitur kedua.

---

## Prompt 2 — Buat Varian Prompt: Mode Perencanaan

### Walkthrough Manual (sebelum pakai prompt)

Sebelum copy-paste prompt, pahami **payoff** dari refactor Prompt 1: sekarang kita bisa buat fitur baru dengan **reuse 3 dari 4 blok**.

📂 **File yang diubah**: `src/features/prompts.ts` (tambah ekspor baru, tidak ubah yang lama)

**1. Tambah `PLANNER_INSTRUCTION` (khusus untuk fitur perencanaan)**

📍 Lokasi: **module level**, di bawah `ADVISOR_INSTRUCTION`. Konten = instruksi spesifik untuk membantu user merencanakan keuangan berdasarkan data yang mereka input langsung di chat.

```ts
// src/features/prompts.ts — module level (tambahan baru)
export const PLANNER_INSTRUCTION = `
Bantu user membuat rencana keuangan sederhana berdasarkan data
yang mereka berikan di chat.

Jika informasi belum lengkap, tanya secara bertahap:
- Pendapatan bulanan
- Pengeluaran rutin bulanan (estimasi)
- Target keuangan (jumlah & jangka waktu)

Setelah data lengkap, berikan rencana dengan format:

### Ringkasan Situasi
- Pendapatan: Rp X
- Pengeluaran: Rp Y
- Sisa: Rp Z

### Rencana Mencapai Target
- Target: Rp A dalam B bulan
- Perlu menabung: Rp C/bulan
- [Apakah realistis + 1 saran actionable jika tidak]
`.trim();
```

**2. Compose `PLANNER_SYSTEM` dengan reuse 3 blok ADVISOR**

📍 Lokasi: **module level**, setelah `PLANNER_INSTRUCTION`. Template literal yang interpolate `ADVISOR_ROLE`, `ADVISOR_CONTEXT`, `ADVISOR_FORMAT`, plus `PLANNER_INSTRUCTION` (yang berbeda dari advisor).

```ts
// src/features/prompts.ts — module level
export const PLANNER_SYSTEM = `
# ROLE
${ADVISOR_ROLE}

# CONTEXT
${ADVISOR_CONTEXT}

# OUTPUT FORMAT
${ADVISOR_FORMAT}

# INSTRUCTION
${PLANNER_INSTRUCTION}
`.trim();
```

> 💡 **Inilah keuntungan RCI**: 3 blok reused, 1 blok diganti. Kalau Anda nanti tambah `CATEGORY_SUGGESTER_INSTRUCTION` atau `DEBT_PLANNER_INSTRUCTION`, polanya sama persis.

### Yang TIDAK perlu

- ❌ Duplikasi role/context/format — **harus** reuse via string interpolation.
- ❌ `PLANNER_INSTRUCTION` menyebut `ADVISOR_INSTRUCTION` — harus standalone, self-contained.
- ❌ Modifikasi `ADVISOR_SYSTEM` — fitur planner punya komposisi sendiri.
- ❌ Buat file terpisah `planner-prompts.ts` — keep semua prompts di satu file untuk overview cepat.

### Hasil yang Diharapkan

```ts
// src/features/prompts.ts — tambahan di bawah ADVISOR_INSTRUCTION

export const PLANNER_INSTRUCTION = `
Bantu user membuat rencana keuangan sederhana berdasarkan data
yang mereka berikan di chat.
[... isi instruction ...]
`.trim();

export const PLANNER_SYSTEM = `
# ROLE
${ADVISOR_ROLE}

# CONTEXT
${ADVISOR_CONTEXT}

# OUTPUT FORMAT
${ADVISOR_FORMAT}

# INSTRUCTION
${PLANNER_INSTRUCTION}
`.trim();
```

### Verifikasi setelah file diubah

1. File `prompts.ts` punya ekspor baru: `PLANNER_INSTRUCTION`, `PLANNER_SYSTEM`.
2. `console.log(PLANNER_SYSTEM)` di REPL: 4 blok terstruktur, blok ROLE/CONTEXT/FORMAT **identik** dengan `ADVISOR_SYSTEM`, blok INSTRUCTION berbeda.
3. `npx tsc --noEmit` — clean.
4. Tidak ada perubahan perilaku di chatbot (route.ts masih pakai `ADVISOR_SYSTEM`).

---

<details>
<summary>Salin prompt berikut</summary>

```
Demonstrasi keuntungan RCI: reuse role/context/format untuk
fitur Mode Perencanaan Keuangan.

GOAL:
- Di src/features/prompts.ts, tambahkan ekspor baru:
  PLANNER_SYSTEM untuk fitur perencanaan keuangan.

- Struktur PLANNER_SYSTEM:
  # ROLE
  ${ADVISOR_ROLE}                  ← reuse

  # CONTEXT
  ${ADVISOR_CONTEXT}               ← reuse

  # OUTPUT FORMAT
  ${ADVISOR_FORMAT}                ← reuse

  # INSTRUCTION
  ${PLANNER_INSTRUCTION}           ← khusus

- PLANNER_INSTRUCTION:
  "Bantu user membuat rencana keuangan sederhana berdasarkan
  data yang mereka berikan di chat.

  Jika informasi belum lengkap, tanya secara bertahap:
  - Pendapatan bulanan
  - Pengeluaran rutin bulanan (estimasi)
  - Target keuangan (jumlah & jangka waktu)

  Setelah data lengkap, berikan rencana dengan format:

  ### Ringkasan Situasi
  - Pendapatan: Rp X
  - Pengeluaran: Rp Y
  - Sisa: Rp Z

  ### Rencana Mencapai Target
  - Target: Rp A dalam B bulan
  - Perlu menabung: Rp C/bulan
  - [Apakah realistis + 1 saran actionable jika tidak]"

CONTEXT:
- File: src/features/prompts.ts.
- Ekspor baru: PLANNER_INSTRUCTION, PLANNER_SYSTEM.
- ADVISOR_ROLE, ADVISOR_CONTEXT, ADVISOR_FORMAT sudah ada
  dari Prompt 1 — reuse via string interpolation.

GUARDRAIL:
- JANGAN duplikasi role/context/format — gunakan
  string interpolation untuk reuse.
- PLANNER_INSTRUCTION harus standalone (tidak menyebut
  ADVISOR_INSTRUCTION).
- JANGAN ubah ADVISOR_SYSTEM atau konstanta yang sudah ada.
```

</details>

**Verifikasi:**

1. File `prompts.ts` mengekspor: `ADVISOR_SYSTEM`, `PLANNER_SYSTEM`, dan konstanta-konstanta penyusun.
2. `PLANNER_SYSTEM` reuse 3 konstanta dari ADVISOR — tidak ada duplikasi teks.

### Efek Perubahan — Contoh Konkret

Inilah momen **payoff RCI** terlihat jelas. Anda menambah fitur baru (Planner) dengan **menulis 1 blok** (instruction) — bukan 1 prompt utuh dari nol.

**Tanpa RCI (jalur duplikasi):**

```ts
// ❌ Anda akan copy-paste ~20 baris, lalu edit instruction.
export const PLANNER_SYSTEM_LAMA = `
Anda adalah AI Financial Advisor untuk Fin-App. Gaya ramah...
User adalah pengguna aplikasi pencatat keuangan...
Format markdown rapi, mata uang Rp 1.500.000...
Bantu user membuat rencana keuangan berdasarkan data di chat...
`.trim();
// Kalau ADVISOR_ROLE berubah → harus update di 2 tempat. Mudah lupa.
```

**Dengan RCI (jalur reuse):**

```ts
// ✅ Anda menulis HANYA blok instruction baru.
export const PLANNER_INSTRUCTION = `
Bantu user membuat rencana keuangan berdasarkan data di chat...
`.trim();

export const PLANNER_SYSTEM = `
# ROLE
${ADVISOR_ROLE}        ← reuse, single source of truth
# CONTEXT
${ADVISOR_CONTEXT}     ← reuse
# OUTPUT FORMAT
${ADVISOR_FORMAT}      ← reuse
# INSTRUCTION
${PLANNER_INSTRUCTION} ← khusus
`.trim();
```

**Efek yang terukur:**

| Aspek | Tanpa RCI | Dengan RCI |
|---|---|---|
| **Baris kode untuk fitur baru** | ~25 baris (full prompt) | ~8 baris (instruction + composition) |
| **Persona drift** | Planner bisa terdengar "beda orang" dari Advisor | Planner & Advisor terdengar **persona yang sama** (ramah, profesional, Bahasa Indonesia) |
| **Update format** | Edit 2 tempat (ADVISOR + PLANNER) | Edit 1 tempat (`ADVISOR_FORMAT`), fitur baru ikut otomatis |
| **Penambahan fitur ke-3** | Copy-paste lagi ~25 baris | Cukup tulis instruction baru |

**Bandingkan jawaban Claude:**

- **Advisor** (`ADVISOR_SYSTEM`) untuk "Tips menghemat?" → tips umum, bullet, tidak spesifik ke angka user.
- **Planner** (`PLANNER_SYSTEM`) untuk "Gaji saya Rp 5jt, mau nabung Rp 20jt dalam 8 bulan, bisa?" → tanya dulu pengeluaran, lalu hitung konkret: `Rp 5jt - Rp 3jt = Rp 2jt/bulan → Rp 16jt dalam 8 bulan → tidak cukup → saran potong pengeluaran atau perpanjang jangka waktu`.

Persona, tone, dan format Rupiah **identik** — karena blok ROLE/CONTEXT/FORMAT sama. Hanya **fokus tugasnya** yang berbeda.

---

## Validasi Akhir Section 3

- [ ] Konstanta ROLE, CONTEXT, FORMAT, INSTRUCTION ada terpisah.
- [ ] `ADVISOR_SYSTEM` dan `PLANNER_SYSTEM` komposisi modular — 3 blok reuse, 1 blok berbeda.
- [ ] Tidak ada regresi: chatbot tetap berfungsi (route.ts masih pakai `ADVISOR_SYSTEM`).

## Refleksi Section 3

1. Apakah refactor RCI lebih mudah di-iterasi vs prompt monolitik?
2. Apa keuntungan praktis dari komposisi modular yang Anda rasakan?
3. Apakah Anda akan menambah lapis lain selain RCI? (Mis. Examples, Guardrails)

---

⬅️ Kembali: **[Section 2](./latihan-2-output-control.md)** · ➡️ Lanjut: **[Section 4 — Agentic Workflow](./latihan-4-agentic.md)**
