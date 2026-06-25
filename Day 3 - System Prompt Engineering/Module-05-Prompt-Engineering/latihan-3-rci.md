# Section 3 — Role, Context, & Instruction

> Bagian dari **[Module 05 — Latihan](./latihan.md)**. Lanjutan dari **[Section 2 — Output Control](./latihan-2-output-control.md)**.

> Latihan restrukturisasi system prompt dengan pola RCI dan demonstrasi reuse. Tiga prompt siap copy-paste.
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

**2. Komposisi `ADVISOR_SYSTEM_V3` dengan template literal**

📍 Lokasi: **module level**, setelah 4 konstanta di atas. Pakai heading `# ROLE`, `# CONTEXT`, dst. agar Claude bisa "membaca" struktur.

```ts
// src/features/prompts.ts — module level
export const ADVISOR_SYSTEM_V3 = `
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
export const ADVISOR_SYSTEM = ADVISOR_SYSTEM_V3;
// (opsional) pertahankan V1, V2 untuk perbandingan
```

> 💡 **Diskriminasi blok**: `ROLE` = identitas Claude. `CONTEXT` = situasi user. `FORMAT` = aturan output. `INSTRUCTION` = tugas + batasan. Kalau bingung mana blok mana, anggap blok = jawaban untuk satu pertanyaan: siapa? di mana? bagaimana? apa?

### Yang TIDAK perlu

- ❌ Mengubah **konten** prompt — hanya restrukturisasi tata letak.
- ❌ `ADVISOR_ROLE` mengandung instruksi tugas (itu bagian INSTRUCTION).
- ❌ `ADVISOR_CONTEXT` mengandung aturan format (itu bagian FORMAT).
- ❌ Modifikasi `route.ts` — alias `ADVISOR_SYSTEM` jaga backward-compat, route tidak perlu diubah.

### Verifikasi setelah file diubah

1. File `prompts.ts` punya 4 konstanta terpisah + `ADVISOR_SYSTEM_V3` + alias `ADVISOR_SYSTEM`.
2. Jalankan `npx tsc --noEmit` — tidak ada error.
3. Reload chatbot, kirim pertanyaan persona ("Halo, siapa kamu?") — respons konsisten dengan Section 1–2.
4. Kirim pertanyaan format ("Berikan 3 tips menabung") — format markdown + bullet tetap rapi.
5. Inspect `ADVISOR_SYSTEM_V3` dengan `console.log` — strukturnya jelas terbagi 4 blok.

---

**Salin prompt berikut:**

```
Saya ingin merestrukturisasi system prompt dengan pola
Role-Context-Instruction yang modular.

GOAL:
- Refactor src/features/prompts.ts.
- Pecah ADVISOR_SYSTEM_V2 menjadi 4 konstanta terpisah:
  - ADVISOR_ROLE: persona Claude (1 paragraf).
  - ADVISOR_CONTEXT: konteks user dan domain (1-2 paragraf).
  - ADVISOR_FORMAT: aturan format output (list).
  - ADVISOR_INSTRUCTION: tugas dan batasan utama.

- Komposisi: ekspor ADVISOR_SYSTEM_V3 dengan template
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

- Update alias ADVISOR_SYSTEM = ADVISOR_SYSTEM_V3.

CONTEXT:
- Pertahankan ADVISOR_SYSTEM_V1 dan V2 untuk perbandingan.

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
2. ADVISOR_SYSTEM_V3 menggabungkan keempatnya.
3. Aplikasi pakai V3 (alias).
4. Chatbot tetap berfungsi seperti di Section 1–2.

### Efek Perubahan — Contoh Konkret

Refactor ini **tidak mengubah jawaban Claude secara dramatis** (konten prompt sama), tapi mengubah dua hal: (a) cara Claude "membaca" struktur, dan (b) cara Anda mengembangkan fitur selanjutnya.

**Sebelum (V2 — monolitik):**

```ts
export const ADVISOR_SYSTEM_V2 = `
Anda adalah AI Financial Advisor untuk Fin-App. Gaya ramah,
to-the-point, profesional. Bahasa Indonesia. User adalah pengguna
aplikasi pencatat keuangan personal... Format markdown rapi,
mata uang Rp 1.500.000... Jawab pertanyaan user. JANGAN beri
nasihat hukum...
`.trim();
```

**Sesudah (V3 — RCI terstruktur):**

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

| Aspek | Sebelum (V2) | Sesudah (V3) |
|---|---|---|
| **Konsistensi format** | Kadang Claude lupa bold angka pada jawaban panjang | Lebih konsisten — heading `# OUTPUT FORMAT` membuat aturan format "menonjol" |
| **Tambah aturan baru** | Edit string panjang, takut nabrak instruksi lain | Edit 1 konstanta (mis. `ADVISOR_FORMAT`) tanpa sentuh blok lain |
| **Reuse untuk fitur lain** | Harus copy-paste seluruh prompt, lalu edit | Tinggal ganti 1 blok (lihat Prompt 2) |
| **Debug prompt** | Sulit lokalisir bagian mana yang "bocor" | Bisa toggle 1 blok at-a-time untuk isolasi |

**Contoh jawaban yang sama dari user prompt "Berapa idealnya dana darurat?":**

- **V2**: kadang muncul tanpa bold di angka (`Rp 30.000.000` plain text), kadang dengan bold.
- **V3**: lebih sering konsisten — angka di-bold (`**Rp 30.000.000**`), bullet rapi, tidak ada paragraf panjang.

> 💡 **Catatan**: Perubahan ini lebih "developer experience" daripada "user experience". User hampir tidak melihat bedanya untuk 1 fitur — payoff sesungguhnya muncul di Prompt 2 saat kita reuse blok untuk fitur kedua.

---

## Prompt 2 — Buat Varian Prompt: Insight Mingguan

### Walkthrough Manual (sebelum pakai prompt)

Sebelum copy-paste prompt, pahami **payoff** dari refactor Prompt 1: sekarang kita bisa buat fitur baru dengan **reuse 3 dari 4 blok**.

📂 **File yang diubah**: `src/features/prompts.ts` (tambah ekspor baru, tidak ubah yang lama)

**1. Tambah `INSIGHT_INSTRUCTION` (khusus untuk fitur insight)**

📍 Lokasi: **module level**, di bawah `ADVISOR_INSTRUCTION`. Konten = instruksi spesifik untuk meringkas data transaksi.

```ts
// src/features/prompts.ts — module level (tambahan baru)
export const INSIGHT_INSTRUCTION = `
Berdasarkan data transaksi minggu ini yang akan diberikan user,
berikan 3 insight penting tentang pola pengeluaran mereka.

Format:

### Insight Minggu Ini

1. **Insight 1**: [observasi konkret dengan angka]
2. **Insight 2**: [observasi konkret dengan angka]
3. **Insight 3**: [observasi konkret dengan angka]

Akhiri dengan 1 saran actionable.
`.trim();
```

**2. Compose `INSIGHT_SYSTEM` dengan reuse 3 blok ADVISOR**

📍 Lokasi: **module level**, setelah `INSIGHT_INSTRUCTION`. Template literal yang interpolate `ADVISOR_ROLE`, `ADVISOR_CONTEXT`, `ADVISOR_FORMAT`, plus `INSIGHT_INSTRUCTION` (yang berbeda dari advisor).

```ts
// src/features/prompts.ts — module level
export const INSIGHT_SYSTEM = `
# ROLE
${ADVISOR_ROLE}

# CONTEXT
${ADVISOR_CONTEXT}

# OUTPUT FORMAT
${ADVISOR_FORMAT}

# INSTRUCTION
${INSIGHT_INSTRUCTION}
`.trim();
```

> 💡 **Inilah keuntungan RCI**: 3 blok reused, 1 blok diganti. Kalau Anda nanti tambah `BUDGET_PLANNER_INSTRUCTION` atau `CATEGORY_SUGGESTER_INSTRUCTION`, polanya sama.

### Yang TIDAK perlu

- ❌ Duplikasi role/context/format — **harus** reuse via string interpolation.
- ❌ `INSIGHT_INSTRUCTION` menyebut `ADVISOR_INSTRUCTION` — harus standalone, self-contained.
- ❌ Modifikasi `ADVISOR_SYSTEM` — fitur insight punya komposisi sendiri.
- ❌ Buat file terpisah `insight-prompts.ts` — keep semua prompts di satu file untuk overview cepat.

### Verifikasi setelah file diubah

1. File `prompts.ts` punya ekspor baru: `INSIGHT_INSTRUCTION`, `INSIGHT_SYSTEM`.
2. `console.log(INSIGHT_SYSTEM)` di REPL: 4 blok terstruktur, blok ROLE/CONTEXT/FORMAT **identik** dengan `ADVISOR_SYSTEM`, blok INSTRUCTION berbeda.
3. `npx tsc --noEmit` — clean.
4. Tidak ada perubahan perilaku di chatbot (route.ts masih pakai `ADVISOR_SYSTEM`).

---

**Salin prompt berikut:**

```
Demonstrasi keuntungan RCI: reuse role/context/format untuk
fitur lain.

GOAL:
- Di src/features/prompts.ts, tambahkan ekspor baru:
  INSIGHT_SYSTEM untuk fitur "Insight Mingguan".

- Struktur INSIGHT_SYSTEM:
  # ROLE
  ${ADVISOR_ROLE}                  ← reuse
  
  # CONTEXT
  ${ADVISOR_CONTEXT}               ← reuse
  
  # OUTPUT FORMAT
  ${ADVISOR_FORMAT}                ← reuse
  
  # INSTRUCTION
  ${INSIGHT_INSTRUCTION}           ← khusus

- INSIGHT_INSTRUCTION:
  "Berdasarkan data transaksi minggu ini yang akan diberikan
  user, berikan 3 insight penting tentang pola pengeluaran
  mereka. Format:
  
  ### Insight Minggu Ini
  
  1. **Insight 1**: [observasi konkret dengan angka]
  2. **Insight 2**: ...
  3. **Insight 3**: ...
  
  Akhiri dengan 1 saran actionable."

CONTEXT:
- File: prompts.ts.
- Ekspor: INSIGHT_SYSTEM, INSIGHT_INSTRUCTION.

GUARDRAIL:
- JANGAN duplikasi role/context/format — gunakan
  string interpolation untuk reuse.
- INSIGHT_INSTRUCTION harus standalone (tidak menyebut
  ADVISOR_INSTRUCTION).
```

**Verifikasi:**

1. File prompts.ts memiliki INSIGHT_SYSTEM yang reuse 3 konstanta dari ADVISOR.
2. File mengekspor: ADVISOR_SYSTEM, INSIGHT_SYSTEM, dan konstanta-konstanta penyusun.

### Efek Perubahan — Contoh Konkret

Inilah momen **payoff RCI** terlihat jelas. Anda menambah fitur baru (Insight) dengan **menulis 1 blok** (instruction) — bukan 1 prompt utuh dari nol.

**Tanpa RCI (jalur duplikasi):**

```ts
// ❌ Anda akan copy-paste ~20 baris, lalu edit instruction.
export const INSIGHT_SYSTEM_LAMA = `
Anda adalah AI Financial Advisor untuk Fin-App. Gaya ramah...
User adalah pengguna aplikasi pencatat keuangan...
Format markdown rapi, mata uang Rp 1.500.000...
Berdasarkan data transaksi minggu ini, berikan 3 insight...
`.trim();
// Kalau ADVISOR_ROLE berubah → harus update di 2 tempat. Mudah lupa.
```

**Dengan RCI (jalur reuse):**

```ts
// ✅ Anda menulis HANYA blok instruction baru.
export const INSIGHT_INSTRUCTION = `
Berdasarkan data transaksi minggu ini, berikan 3 insight...
`.trim();

export const INSIGHT_SYSTEM = `
# ROLE
${ADVISOR_ROLE}        ← reuse, single source of truth
# CONTEXT
${ADVISOR_CONTEXT}     ← reuse
# OUTPUT FORMAT
${ADVISOR_FORMAT}      ← reuse
# INSTRUCTION
${INSIGHT_INSTRUCTION} ← khusus
`.trim();
```

**Efek yang terukur:**

| Aspek | Tanpa RCI | Dengan RCI |
|---|---|---|
| **Baris kode untuk fitur baru** | ~25 baris (full prompt) | ~8 baris (instruction + composition) |
| **Persona drift** | Insight bisa terdengar "beda orang" dari Advisor | Insight & Advisor terdengar **persona yang sama** (ramah, profesional, Bahasa Indonesia) |
| **Update format** | Edit 2 tempat (ADVISOR + INSIGHT) | Edit 1 tempat (`ADVISOR_FORMAT`), fitur baru ikut |
| **Penambahan fitur ke-3** | Copy-paste lagi ~25 baris | Cukup tulis instruction baru |

**Contoh output `INSIGHT_SYSTEM` saat Anda `console.log`:**

```
# ROLE
Anda adalah AI Financial Advisor untuk Fin-App.
Gaya: ramah, to-the-point, profesional. Bahasa Indonesia.

# CONTEXT
User adalah pengguna aplikasi pencatat keuangan personal.
Domain: pengeluaran, tabungan, budget, investasi pemula.

# OUTPUT FORMAT
- Markdown rapi (list bertanda, bold untuk angka penting).
- Format mata uang: Rp 1.500.000.
...

# INSTRUCTION
Berdasarkan data transaksi minggu ini yang akan diberikan user,
berikan 3 insight penting tentang pola pengeluaran mereka.
...
```

**Bandingkan jawaban Claude (dengan data dummy transaksi):**

- **Advisor** (`ADVISOR_SYSTEM`) untuk "Tips menghemat?" → tips umum, bullet, tidak menyebut angka spesifik user.
- **Insight** (`INSIGHT_SYSTEM`) untuk data transaksi minggu ini → 3 insight numbered yang **konkret menyebut angka & kategori** dari data user, ditutup 1 saran actionable.

Persona, tone, dan format Rupiah **identik** — karena blok ROLE/CONTEXT/FORMAT sama. Hanya **fokus tugasnya** yang berbeda.

---

## Prompt 3 — Server Action `getWeeklyInsight`

### Walkthrough Manual (sebelum pakai prompt)

Sebelum copy-paste prompt, pahami alur server action `getWeeklyInsight`: **fetch data → format → call Claude → return string**.

📂 **File baru**: `src/features/insight.ts` (server action)

**1. Directive `"use server"` di baris pertama**

📍 Lokasi: **baris 1**. Wajib karena query Supabase di sisi server.

```ts
// src/features/insight.ts — baris pertama
"use server";
```

**2. Import dependensi**

📍 Lokasi: **bagian import**.

```ts
// src/features/insight.ts — bagian import
import Anthropic from "@anthropic-ai/sdk";
import { createClient } from "@/lib/supabase/server";
import { INSIGHT_SYSTEM } from "@/features/prompts";
```

**3. Function `getWeeklyInsight()`**

📍 Lokasi: **module level**, exported async function. Alur:

- Hitung tanggal 7 hari ke belakang (`Date.now() - 7 * 24 * 60 * 60 * 1000`).
- Query Supabase: `select * from transactions where date >= sevenDaysAgo`.
- **Early return** kalau kosong — hemat biaya.
- Format ke string readable: list dengan tanggal, kategori, amount per baris.
- Panggil Claude dengan `system: INSIGHT_SYSTEM`, user content = data formatted.
- Return text content block.

```ts
// src/features/insight.ts — module level
export async function getWeeklyInsight(): Promise<string> {
  const supabase = await createClient();
  const sevenDaysAgo = new Date(Date.now() - 7 * 86400 * 1000).toISOString();
  const { data, error } = await supabase
    .from("transactions")
    .select("*")
    .gte("date", sevenDaysAgo);

  if (error) throw new Error(error.message);
  if (!data || data.length === 0) {
    return "Belum ada transaksi minggu ini. Mulai catat untuk dapat insight.";
  }

  const formatted = data
    .map((t) => `- ${t.date} | ${t.category} | ${t.type} | Rp ${t.amount.toLocaleString("id-ID")}`)
    .join("\n");

  const resp = await client.messages.create({
    model: "claude-haiku-4-5",
    max_tokens: 1024,
    temperature: 0.5,
    system: INSIGHT_SYSTEM,
    messages: [{ role: "user", content: `Data transaksi saya minggu ini:\n\n${formatted}` }],
  });

  const block = resp.content[0];
  if (block.type !== "text") throw new Error("Response bukan text block");
  return block.text;
}
```

### Yang TIDAK perlu

- ❌ Modifikasi `prompts.ts` — `INSIGHT_SYSTEM` sudah lengkap di Prompt 2.
- ❌ Panggil Claude saat data kosong — early return string statis, hemat biaya.
- ❌ Cache hasil di memory — Next.js server action akan re-execute tiap call (mau cache, pakai `unstable_cache` terpisah).
- ❌ Widget dashboard — Prompt 3 hanya server action; widget akan dipanggil di section terpisah.

### Verifikasi setelah file dibuat

1. File `src/features/insight.ts` ada dengan `"use server"` di baris 1.
2. Buat `experiments/test-insight.ts`:
   ```ts
   import { getWeeklyInsight } from "../src/features/insight";
   async function main() { console.log(await getWeeklyInsight()); }
   main().catch(console.error);
   ```
3. Jalankan: `npx tsx --env-file=.env.local experiments/test-insight.ts`.
4. Output: markdown dengan heading `### Insight Minggu Ini` + 3 numbered insight + 1 saran actionable.
5. Kosongkan data transaksi 7 hari terakhir → jalankan ulang → output string statis "Belum ada transaksi...".

---

**Salin prompt berikut:**

```
Buat server action yang menggunakan INSIGHT_SYSTEM untuk
hasilkan insight dari data transaksi.

GOAL:
- Buat file baru src/features/insight.ts.
- Server action getWeeklyInsight(): Promise<string>.
- Logic:
  1. Query Supabase: ambil transaksi 7 hari terakhir.
     (Pakai pola createClient + select yang sudah ada di
     features/action.ts.)
  2. Format data ke string yang readable: misalnya
     daftar transaksi dengan tanggal, kategori, amount.
  3. Panggil Claude API:
     - system: INSIGHT_SYSTEM
     - messages: [{ role: "user", content: "Data transaksi
       saya minggu ini:\n\n" + formattedData }]
     - temperature: 0.5
     - max_tokens: 1024.
  4. Return text content.

CONTEXT:
- File "use server".
- Import INSIGHT_SYSTEM dari "@/features/prompts".
- Import createClient dari "@/lib/supabase/server".

GUARDRAIL:
- Apabila transaksi 7 hari terakhir kosong, return string
  "Belum ada transaksi minggu ini. Mulai catat untuk
  dapat insight." (TANPA panggil API — hemat).
- JANGAN ubah prompts.ts — sudah selesai di prompt 2.
- Apabila Claude response.content[0].type !== "text", throw
  error.
```

**Verifikasi:**

1. Test cepat dari `experiments/test-insight.ts`:
   ```ts
   const result = await getWeeklyInsight();
   console.log(result);
   ```
2. Output berupa string markdown dengan 3 insight + 1 saran.
3. (Opsional) Tambahkan tombol di dashboard untuk trigger insight ini — biarkan saya yang minta di section terpisah.

### Efek Perubahan — Contoh Konkret

Server action ini adalah **integrasi end-to-end** dari prompt engineering ke produk: data nyata dari DB → di-format → dikirim ke Claude dengan `INSIGHT_SYSTEM` → hasil insight yang relevan dengan kondisi user.

**Contoh data transaksi user (yang ter-format sebelum dikirim ke Claude):**

```
- 2026-06-18 | Makanan | expense | Rp 85.000
- 2026-06-19 | Transport | expense | Rp 45.000
- 2026-06-20 | Makanan | expense | Rp 120.000
- 2026-06-21 | Hiburan | expense | Rp 250.000
- 2026-06-22 | Makanan | expense | Rp 95.000
- 2026-06-23 | Tabungan | income | Rp 500.000
- 2026-06-24 | Makanan | expense | Rp 110.000
```

**Contoh output `getWeeklyInsight()` (saat ada data):**

```markdown
### Insight Minggu Ini

1. **Pengeluaran Makanan dominan**: Total **Rp 410.000** untuk
   makanan dalam 7 hari (4 transaksi). Ini ~62% dari total
   pengeluaran mingguan Anda.
2. **Spike di kategori Hiburan**: Pengeluaran **Rp 250.000**
   dalam satu transaksi — angka tertinggi minggu ini.
3. **Surplus mingguan tipis**: Income **Rp 500.000** vs
   total expense **Rp 705.000** → defisit **Rp 205.000**.

**Saran**: Coba batasi makan di luar maksimal 3x minggu depan
dan alokasikan selisihnya ke tabungan.
```

**Contoh output saat data kosong (early return, TANPA panggil API):**

```
Belum ada transaksi minggu ini. Mulai catat untuk dapat insight.
```

**Efek yang terukur:**

| Aspek | Implementasi naif | Dengan early return + RCI |
|---|---|---|
| **API call saat data kosong** | 1 call (boros ~$0.001) | 0 call (string statis) |
| **Konsistensi persona** | Bisa beda dari chatbot advisor | Identik (reuse ROLE/CONTEXT/FORMAT) |
| **Format angka Rupiah** | Tergantung Claude "ingat" | Konsisten via `ADVISOR_FORMAT` |
| **Maintenance** | Update prompt = edit di sini | Update `ADVISOR_FORMAT` → otomatis ikut |

**Yang Anda rasakan saat menjalankan:**

- **Run pertama (ada data)**: ~2-3 detik, output structured persis seperti template di `INSIGHT_INSTRUCTION`.
- **Run kedua (kosongkan tabel)**: instant (<100ms), tidak ada billing API.
- **Ubah `ADVISOR_FORMAT`** (mis. tambah aturan "selalu sertakan emoji 💰 di depan angka") → re-run → **chatbot DAN insight** sama-sama ikut aturan baru. Inilah bukti reuse bekerja.

---

## Validasi Akhir Section 3

- [ ] Konstanta ROLE, CONTEXT, FORMAT, INSTRUCTION ada terpisah.
- [ ] ADVISOR_SYSTEM_V3 dan INSIGHT_SYSTEM komposisi modular.
- [ ] Server action `getWeeklyInsight` ada dan return insight string.
- [ ] Tidak ada regresi: chatbot tetap berfungsi dengan V3.

## Refleksi Section 3

1. Apakah refactor RCI lebih mudah di-iterasi vs prompt monolitik?
2. Apa keuntungan praktis dari komposisi modular yang Anda rasakan?
3. Apakah Anda akan menambah lapis lain selain RCI? (Mis. Examples, Guardrails)

---

⬅️ Kembali: **[Section 2](./latihan-2-output-control.md)** · ➡️ Lanjut: **[Section 4 — Agentic Workflow](./latihan-4-agentic.md)**
