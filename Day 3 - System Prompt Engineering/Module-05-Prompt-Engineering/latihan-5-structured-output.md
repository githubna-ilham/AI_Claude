# Section 5 — Structured Output (JSON) untuk Quick-Add Transaksi

> Bagian dari **[Module 05 — Latihan](./latihan.md)**. Lanjutan dari **[Section 4 — Agentic Workflow](./latihan-4-agentic.md)**.

> Latihan pertama yang menjembatani dari **chatbot** ke **agentic AI**: Claude tidak lagi sekadar menjawab teks, tapi mem-parse input natural language user ("ngopi 5000") menjadi **struktur data JSON** yang langsung ter-insert ke Supabase. Ini fondasi semua fitur agentic berikutnya (tool use, function calling, multi-step actions).
>
> **Estimasi**: 60–75 menit.

## Prasyarat Section 5

- [ ] Section 1–4 selesai.
- [ ] Tabel `transactions` di Supabase sudah ada (dari Module sebelumnya) dengan kolom minimal: `id`, `user_id`, `date`, `category`, `type` (`expense` / `income`), `amount`, `note`, `created_at`.
- [ ] Halaman transaksi (`src/app/transactions/page.tsx` atau path setara) sudah render daftar transaksi.

---

## 📚 Referensi Dokumentasi

Sebelum mulai, akan sangat membantu kalau Anda buka tab dokumentasi resmi untuk referensi cepat:

- **[Tool use (function calling)](https://docs.claude.com/en/docs/build-with-claude/tool-use)** — cara mendapatkan output **terstruktur** (JSON) yang dijamin valid schema, bukan teks bebas yang harus di-`JSON.parse` dengan harap-harap cemas.
- **[Forcing tool use](https://docs.claude.com/en/docs/build-with-claude/tool-use#forcing-tool-use)** — `tool_choice: { type: "tool", name: "..." }` agar Claude **wajib** memanggil tool spesifik (cocok untuk parser).
- **[Input schemas (JSON Schema)](https://docs.claude.com/en/docs/build-with-claude/tool-use#tool-input-json-schema)** — cara mendefinisikan `input_schema` untuk tool.
- **[Next.js Server Actions](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations)** — pola form action untuk submit dari client tanpa bikin API route manual.

> 💡 **Mengapa tool use, bukan "minta JSON di prompt"?**
> Minta JSON di prompt (`return JSON only`) bisa bekerja, tapi **rapuh** — Claude kadang membungkus dengan ` ```json ... ``` `, kadang menambah kata pengantar, kadang field hilang. **Tool use** memberi Claude *function signature* yang harus dipatuhi — output `tool_use.input` dijamin valid terhadap schema. Inilah fondasi agentic AI: AI memanggil "tool" (fungsi) dengan argumen terstruktur.

---

## Pengenalan: Apa Itu Tools di Claude API?

**Tools** (atau *function calling*) adalah cara memberi Claude daftar "fungsi" yang bisa dipanggil — lengkap dengan nama, deskripsi, dan schema input-nya. Alih-alih menjawab teks bebas, Claude akan merespons dengan memanggil tool tersebut menggunakan argumen terstruktur yang valid sesuai schema.

### Alur Tool Use

```
User input → Claude API (+ tools definition)
                    ↓
           Claude memilih tool yang tepat
                    ↓
           response.content[0].type === "tool_use"
           response.content[0].input === { ... JSON terstruktur ... }
                    ↓
           Kode kita eksekusi fungsi dengan input tersebut
```

### Anatomi Definisi Tool

```ts
const tools = [
  {
    name: "add_transaction",           // nama fungsi
    description: "Parse teks natural language user menjadi data transaksi terstruktur",
    input_schema: {
      type: "object",
      properties: {
        amount:   { type: "number",  description: "Nominal dalam Rupiah (tanpa titik/koma)" },
        category: { type: "string",  description: "Kategori: Makanan, Transport, Hiburan, dll." },
        type:     { type: "string",  enum: ["expense", "income"] },
        date:     { type: "string",  description: "Format ISO 8601, default hari ini" },
        note:     { type: "string",  description: "Deskripsi singkat dari input user" },
      },
      required: ["amount", "category", "type", "date"],
    },
  },
];
```

### Tool Choice: Paksa Claude Selalu Pakai Tool Ini

```ts
const response = await client.messages.create({
  model: "claude-haiku-4-5",
  max_tokens: 1024,
  tools,
  tool_choice: { type: "tool", name: "add_transaction" }, // ← wajib panggil tool ini
  messages: [{ role: "user", content: userInput }],
});
```

Dengan `tool_choice: { type: "tool", name: "..." }`, Claude **tidak bisa** menjawab teks biasa — ia wajib memanggil tool `add_transaction` dengan argumen yang valid. Inilah jaminan structured output yang dibutuhkan untuk insert ke database.

### Membaca Hasil Tool Use

```ts
const block = response.content[0];
if (block.type !== "tool_use") throw new Error("Claude tidak memanggil tool");

const data = block.input; // { amount, category, type, date, note }
// → langsung bisa dipakai untuk insert ke Supabase
```

> 💡 **Perbedaan utama dari prompt biasa**: kita tidak perlu `JSON.parse()` string, tidak perlu strip markdown code block, tidak perlu validasi format manual. Schema yang kita definisikan di `input_schema` adalah kontrak — Claude akan memenuhinya.

---

## Prompt 1 — Tambah Field Quick-Add di Halaman Transaksi

### Walkthrough Manual (sebelum pakai prompt)

Sebelum copy-paste prompt, pahami **bentuk akhir UI**: di atas daftar transaksi, ada **1 input teks lebar** + tombol "Tambah". User mengetik bebas seperti "ngopi 5000" atau "gaji bulan ini 8 juta" lalu enter — daftar transaksi auto-refresh.

📂 **File yang diubah**: `src/app/transactions/page.tsx` (atau path setara) + komponen baru `src/components/quick-add-transaction.tsx`.

**1. Komponen `<QuickAddTransaction />` (client component)**

📍 Lokasi: **file baru** `src/components/quick-add-transaction.tsx`. Pakai `"use client"` karena butuh state input + `useFormStatus`.

```tsx
// src/components/quick-add-transaction.tsx
"use client";

import { useRef } from "react";
import { useFormStatus } from "react-dom";
import { quickAddTransaction } from "@/features/quick-add";

function SubmitButton() {
  const { pending } = useFormStatus();
  return (
    <button
      type="submit"
      disabled={pending}
      className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white disabled:opacity-50"
    >
      {pending ? "Memproses..." : "Tambah"}
    </button>
  );
}

export function QuickAddTransaction() {
  const formRef = useRef<HTMLFormElement>(null);

  return (
    <form
      ref={formRef}
      action={async (formData) => {
        const result = await quickAddTransaction(formData);
        if (result.ok) formRef.current?.reset();
        else alert(result.error);
      }}
      className="mb-6 flex gap-2 rounded-xl border border-gray-200 bg-white p-3"
    >
      <input
        name="text"
        type="text"
        required
        placeholder='Contoh: "ngopi 5000" atau "gaji bulanan 8 juta"'
        className="flex-1 rounded-lg border border-gray-300 px-3 py-2 text-sm"
      />
      <SubmitButton />
    </form>
  );
}
```

**2. Pasang di halaman transaksi**

📍 Lokasi: **bagian atas** daftar transaksi di `src/app/transactions/page.tsx`. Tepat di atas tabel/list yang sudah ada.

```tsx
// src/app/transactions/page.tsx — di dalam JSX, sebelum render list
import { QuickAddTransaction } from "@/components/quick-add-transaction";

export default async function TransactionsPage() {
  // ... query transaksi existing
  return (
    <div className="container mx-auto p-6">
      <h1 className="mb-4 text-2xl font-bold">Transaksi</h1>
      <QuickAddTransaction />
      {/* render list existing di bawah */}
    </div>
  );
}
```

> 💡 **Mengapa `useFormStatus` + `formRef.reset()`?** Server action di-await di action handler, jadi kita bisa cek hasil dan reset form. `useFormStatus` memberi tombol "Memproses..." otomatis selama action jalan — UX yang muncul gratis tanpa state manual.

### Yang TIDAK perlu

- ❌ Validasi input di client (regex untuk angka, dsb) — biarkan Claude yang parse, itu fokus latihan ini.
- ❌ Form modal / dropdown kategori manual — quick-add justru menghapus friction tersebut.
- ❌ Real-time streaming response — untuk parser cukup single-shot (tidak ada teks panjang yang ditampilkan).
- ❌ Optimistic update — UI cukup tunggu server action selesai (latensi ~1-2 detik dapat diterima).

### Verifikasi setelah file diubah

1. Reload halaman transaksi — input field muncul di atas list.
2. Ketik teks apapun + klik Tambah → tombol berubah jadi "Memproses..." (action terhubung).
3. Action akan **error** karena `quickAddTransaction` belum ada — itu normal, kita buat di Prompt 2.

---

**Salin prompt berikut:**

```
Tambahkan UI quick-add transaksi di atas daftar transaksi.
User mengetik teks bebas (contoh: "ngopi 5000"), lalu klik
Tambah. Parser & insert ke Supabase akan dibuat di prompt
berikutnya — fokus prompt ini HANYA UI + wiring.

GOAL:
- Buat file baru src/components/quick-add-transaction.tsx
  sebagai client component.
- Komponen berisi:
  - 1 input teks (name="text", placeholder dengan contoh).
  - 1 tombol submit (disabled saat pending pakai useFormStatus).
- Form action memanggil quickAddTransaction(formData) dari
  @/features/quick-add (akan dibuat di prompt 2).
- Hasil action: { ok: true } → reset form; { ok: false, error }
  → alert error.
- Pasang <QuickAddTransaction /> di src/app/transactions/page.tsx
  PERSIS di atas daftar transaksi yang sudah ada.

CONTEXT:
- Halaman transaksi sudah render list dari Supabase.
- Tailwind tersedia.
- React 19 + Next.js 15 (App Router) — gunakan useFormStatus
  dari "react-dom".

GUARDRAIL:
- JANGAN buat features/quick-action.ts di prompt ini —
  hanya import + biarkan error type sementara.
- JANGAN tambah validasi regex di client — Claude yang parse.
- JANGAN modifikasi tabel transaksi / komponen list lain.
- Komponen quick-add WAJIB "use client", halaman transaksi
  TETAP server component.
```

**Verifikasi:**

1. File `src/components/quick-add-transaction.tsx` ada dan render input + tombol.
2. Halaman transaksi menampilkan field di atas daftar.
3. Klik Tambah → tombol berubah jadi "Memproses..." (action terhubung walau belum ada).

### Efek Perubahan — Contoh Konkret

UI quick-add ini adalah **entry point** dari paradigma baru. Bandingkan dua jalur input:

| Aspek | Form klasik | Quick-add (latihan ini) |
|---|---|---|
| **Jumlah field user isi** | 4–5 (tanggal, kategori, type, amount, note) | 1 (teks bebas) |
| **Waktu input per transaksi** | ~15–25 detik | ~3–5 detik |
| **Kategori salah ketik** | Dropdown mencegah | Claude infer dari konteks ("ngopi" → "Makanan & Minuman") |
| **Mobile UX** | Banyak tap | Bisa pakai voice-to-text → langsung jalan |

**Yang Anda rasakan di Prompt 1 ini saja**: belum ada parsing, jadi klik Tambah masih gagal. Tapi UI sudah terasa "ringan" — satu input, satu tombol, tidak ada dropdown yang harus diisi. Ini setup untuk Prompt 2.

---

## Prompt 2 — Server Action `quickAddTransaction` dengan Tool Use (JSON terstruktur)

### Walkthrough Manual (sebelum pakai prompt)

Ini **inti** Section 5. Kita akan minta Claude **memanggil "tool"** `save_transaction` dengan argumen JSON yang sudah valid schema. Tidak ada lagi `JSON.parse` yang berisiko gagal.

📂 **File baru**: `src/features/quick-add.ts` (server action) + tambah konstanta prompt di `src/features/prompts.ts`.

**1. Tambah `QUICK_ADD_SYSTEM` di `prompts.ts`**

📍 Lokasi: **module level** di `src/features/prompts.ts`, di bawah konstanta yang sudah ada. Ini contoh reuse pola RCI dari Section 3 — `ROLE` & `CONTEXT` reuse, `INSTRUCTION` khusus parser.

```ts
// src/features/prompts.ts — module level (tambahan)
export const QUICK_ADD_INSTRUCTION = `
Anda akan menerima teks bebas dari user yang mendeskripsikan SATU transaksi
keuangan. Tugas Anda: panggil tool save_transaction dengan argumen yang
sudah ter-ekstraksi dari teks tersebut.

Aturan ekstraksi:
- amount: angka rupiah. Kata "5k", "5rb", "5ribu" = 5000. "5jt", "5 juta" = 5000000.
- type: "expense" untuk pengeluaran (default kalau tidak jelas), "income" untuk pemasukan
  (kata kunci: gaji, bonus, freelance, terima, dapat, masuk).
- category: pilih SATU dari daftar berikut yang paling cocok:
  - "Makanan & Minuman"  (ngopi, makan, jajan, kopi, nasi, dll)
  - "Transportasi"        (bensin, ojek, grab, parkir, tol)
  - "Belanja"             (baju, sepatu, gadget, kebutuhan rumah)
  - "Tagihan"             (listrik, internet, air, pulsa)
  - "Hiburan"             (nonton, game, langganan streaming)
  - "Kesehatan"           (obat, dokter, gym)
  - "Pendidikan"          (buku, kursus, sekolah)
  - "Gaji & Pemasukan"    (income — gaji, bonus, freelance)
  - "Lainnya"             (kalau tidak masuk kategori di atas)
- date: ISO date (YYYY-MM-DD). Default = hari ini. "kemarin" = H-1.
- note: ringkasan singkat (≤30 karakter) dari teks asli.

WAJIB panggil tool save_transaction — JANGAN balas dengan teks biasa.
`.trim();

export const QUICK_ADD_SYSTEM = `
# ROLE
${ADVISOR_ROLE}

# CONTEXT
${ADVISOR_CONTEXT}

# INSTRUCTION
${QUICK_ADD_INSTRUCTION}
`.trim();
```

**2. Definisikan tool schema + server action**

📍 Lokasi: **file baru** `src/features/quick-add.ts`. Tool schema = JSON Schema; `tool_choice` memaksa Claude memanggil tool ini.

```ts
// src/features/quick-add.ts
"use server";

import Anthropic from "@anthropic-ai/sdk";
import { createClient } from "@/lib/supabase/server";
import { QUICK_ADD_SYSTEM } from "@/features/prompts";

const client = new Anthropic();

const SAVE_TRANSACTION_TOOL: Anthropic.Tool = {
  name: "save_transaction",
  description:
    "Simpan satu transaksi keuangan ke database setelah mengekstrak detail dari teks user.",
  input_schema: {
    type: "object",
    properties: {
      amount: { type: "number", description: "Nominal dalam rupiah (integer)" },
      type: { type: "string", enum: ["expense", "income"] },
      category: { type: "string" },
      date: { type: "string", description: "ISO date YYYY-MM-DD" },
      note: { type: "string", description: "Ringkasan singkat (≤30 char)" },
    },
    required: ["amount", "type", "category", "date", "note"],
  },
};

type ParsedTransaction = {
  amount: number;
  type: "expense" | "income";
  category: string;
  date: string;
  note: string;
};

type ActionResult =
  | { ok: true; transaction: ParsedTransaction }
  | { ok: false; error: string };

export async function quickAddTransaction(formData: FormData): Promise<ActionResult> {
  const text = String(formData.get("text") ?? "").trim();
  if (!text) return { ok: false, error: "Teks tidak boleh kosong." };

  const today = new Date().toISOString().slice(0, 10);

  const resp = await client.messages.create({
    model: "claude-haiku-4-5",
    max_tokens: 512,
    temperature: 0,
    system: QUICK_ADD_SYSTEM,
    tools: [SAVE_TRANSACTION_TOOL],
    tool_choice: { type: "tool", name: "save_transaction" },
    messages: [
      {
        role: "user",
        content: `Hari ini: ${today}\n\nTransaksi: ${text}`,
      },
    ],
  });

  const toolBlock = resp.content.find((b) => b.type === "tool_use");
  if (!toolBlock || toolBlock.type !== "tool_use") {
    return { ok: false, error: "Claude tidak memanggil tool. Coba teks lebih spesifik." };
  }

  const parsed = toolBlock.input as ParsedTransaction;

  // Insert ke Supabase — implementasi penuh di Prompt 3.
  // Untuk sementara, return parsed agar bisa dicek di console.
  console.log("[quickAddTransaction] parsed:", parsed);

  return { ok: true, transaction: parsed };
}
```

> 💡 **Mengapa `temperature: 0`?** Untuk parser deterministik. Tidak butuh kreativitas — butuh konsistensi. Input yang sama → output yang sama.
>
> 💡 **Mengapa `tool_choice: { type: "tool", name: "..." }`?** Default Claude bisa memilih balas teks **atau** panggil tool. Untuk parser, kita **paksa** dia panggil tool spesifik — eliminasi ambiguitas.

### Yang TIDAK perlu

- ❌ Memanggil `JSON.parse(text)` di response Claude — `tool_use.input` sudah parsed object dari SDK.
- ❌ Streaming — parser cepat, tunggu non-stream lebih simple.
- ❌ Retry loop kalau Claude tidak panggil tool — `temperature: 0` + `tool_choice` forced membuat ini hampir tidak pernah terjadi. Kalau gagal, kasih error ke user.
- ❌ Validasi field manual di TypeScript (cek `amount > 0`, dst) — schema sudah dijaga Claude. Tambahkan validasi hanya kalau Anda **observasi** kasus gagal.

### Verifikasi setelah file diubah

1. File `src/features/quick-add.ts` ada dengan `"use server"`.
2. File `prompts.ts` punya ekspor `QUICK_ADD_SYSTEM` dan `QUICK_ADD_INSTRUCTION`.
3. Di halaman transaksi, ketik "ngopi 5000" → Tambah → cek terminal server. Harus muncul:
   ```
   [quickAddTransaction] parsed: {
     amount: 5000,
     type: 'expense',
     category: 'Makanan & Minuman',
     date: '2026-06-25',
     note: 'ngopi'
   }
   ```
4. Coba teks lain: "gaji bulan ini 8 juta" → `type: 'income'`, `amount: 8000000`, `category: 'Gaji & Pemasukan'`.
5. Coba teks ambigu "5000" saja → Claude masih panggil tool, tapi `note` mungkin "transaksi" atau `category` "Lainnya" — observasi behavior-nya.

---

**Salin prompt berikut:**

```
Buat server action quickAddTransaction yang mem-parse teks bebas
user menjadi struktur JSON valid menggunakan Claude tool use.
INI BELUM INSERT KE DB — fokus prompt ini hanya parser + return
hasil parse. Insert akan ditambahkan di Prompt 3.

GOAL:
- Tambahkan QUICK_ADD_INSTRUCTION + QUICK_ADD_SYSTEM di
  src/features/prompts.ts. QUICK_ADD_SYSTEM reuse ADVISOR_ROLE
  & ADVISOR_CONTEXT (pola RCI dari Section 3), instruction
  berisi aturan ekstraksi:
  - amount (5k=5000, 5jt=5000000)
  - type (expense default, income kalau ada kata gaji/bonus/dll)
  - category (pilih 1 dari list fix: Makanan & Minuman,
    Transportasi, Belanja, Tagihan, Hiburan, Kesehatan,
    Pendidikan, Gaji & Pemasukan, Lainnya)
  - date (ISO, default hari ini, "kemarin" = H-1)
  - note (ringkasan ≤30 char)

- Buat src/features/quick-add.ts ("use server"):
  - Definisikan SAVE_TRANSACTION_TOOL dengan input_schema JSON
    Schema (semua field di atas required).
  - quickAddTransaction(formData) returns
    { ok: true, transaction } | { ok: false, error }.
  - Panggil Claude messages.create dengan:
    - model: "claude-haiku-4-5"
    - temperature: 0
    - tools: [SAVE_TRANSACTION_TOOL]
    - tool_choice: { type: "tool", name: "save_transaction" }
    - system: QUICK_ADD_SYSTEM
    - user message berisi "Hari ini: <today>" + teks user
  - Ambil block dengan type === "tool_use", baca .input.
  - console.log hasil parse, return { ok: true, transaction }.

CONTEXT:
- Halaman transaksi & komponen quick-add sudah ada dari Prompt 1.
- Pola server action + createClient supabase sudah dipakai
  di features/insight.ts (Section 3).

GUARDRAIL:
- JANGAN JSON.parse output Claude — tool_use.input sudah object.
- JANGAN insert ke Supabase di prompt ini (Prompt 3).
- JANGAN retry loop — temperature 0 + tool_choice forced
  sudah deterministik.
- JANGAN tambah validasi manual di TS sebelum observasi
  kasus gagal.
- type ANTHROPIC Tool: gunakan Anthropic.Tool dari SDK.
```

**Verifikasi:**

1. Ketik "ngopi 5000" di UI → terminal server log object parsed dengan amount 5000, category "Makanan & Minuman", type "expense".
2. Ketik "gaji 8jt" → type "income", category "Gaji & Pemasukan", amount 8000000.
3. Tidak ada error JSON.parse di console.

### Efek Perubahan — Contoh Konkret

**Tanpa tool use (jalur rapuh):**

```ts
// ❌ Rentan: Claude bisa balas "Berikut JSON: ```json {...} ```"
const resp = await client.messages.create({
  system: "Return ONLY valid JSON with fields amount, type, ...",
  messages: [{ role: "user", content: text }],
});
const raw = resp.content[0].type === "text" ? resp.content[0].text : "";
const json = JSON.parse(raw); // 💥 SyntaxError kalau ada markdown wrapper
```

**Dengan tool use (jalur dijamin schema):**

```ts
// ✅ Output dijamin valid terhadap input_schema
const resp = await client.messages.create({
  tools: [SAVE_TRANSACTION_TOOL],
  tool_choice: { type: "tool", name: "save_transaction" },
  ...
});
const parsed = resp.content.find(b => b.type === "tool_use")!.input;
// parsed sudah object {amount, type, category, date, note}
```

**Contoh input → output yang Anda akan lihat di terminal:**

| Input user | `parsed.amount` | `parsed.type` | `parsed.category` | `parsed.note` |
|---|---|---|---|---|
| `"ngopi 5000"` | 5000 | expense | Makanan & Minuman | ngopi |
| `"bensin 50rb"` | 50000 | expense | Transportasi | bensin |
| `"gaji 8 juta"` | 8000000 | income | Gaji & Pemasukan | gaji |
| `"bayar listrik 350000"` | 350000 | expense | Tagihan | bayar listrik |
| `"kemarin makan padang 25k"` | 25000 | expense | Makanan & Minuman | makan padang |

**Efek yang terukur:**

| Aspek | Free-text JSON | Tool use (latihan ini) |
|---|---|---|
| **Field hilang** | 5–15% case (lupa `date`, dll) | ~0% (schema enforced) |
| **JSON.parse error** | 2–8% case (markdown wrapper, trailing comma) | 0% (sudah object) |
| **Kategori di luar list** | Sering ("Coffee", "Kuliner") | Hampir tidak pernah (enum-like prompt) |
| **Latensi tambahan** | — | +0ms (tool use bukan extra call) |

> 💡 **Inilah momen "agentic"**: Claude bukan sekadar menjawab, tapi **mengambil tindakan terstruktur** (memanggil function `save_transaction`). Di Module berikutnya pola ini berkembang jadi multi-tool, multi-step, dan loop hingga task selesai.

---

## Prompt 3 — Insert ke Supabase + Revalidate

### Walkthrough Manual (sebelum pakai prompt)

Sekarang sambungkan hasil parse ke database. Tabel `transactions` sudah ada — kita tinggal `insert` + `revalidatePath` agar list di halaman auto-refresh.

📂 **File yang diubah**: `src/features/quick-add.ts` (tambah insert + revalidate).

**1. Insert ke Supabase**

📍 Lokasi: **setelah** `console.log` di `quickAddTransaction`. Ambil `user_id` dari session, gabungkan dengan parsed data.

```ts
// src/features/quick-add.ts — di dalam quickAddTransaction, setelah parsed dibuat
const supabase = await createClient();
const {
  data: { user },
} = await supabase.auth.getUser();

if (!user) return { ok: false, error: "Belum login." };

const { error: insertError } = await supabase.from("transactions").insert({
  user_id: user.id,
  amount: parsed.amount,
  type: parsed.type,
  category: parsed.category,
  date: parsed.date,
  note: parsed.note,
});

if (insertError) return { ok: false, error: insertError.message };
```

**2. Revalidate path agar list refresh**

📍 Lokasi: **di atas function** import `revalidatePath`, **di akhir** function panggil sebelum return success.

```ts
// src/features/quick-add.ts — import section
import { revalidatePath } from "next/cache";

// ... di akhir quickAddTransaction (sebelum return ok)
revalidatePath("/transactions");

return { ok: true, transaction: parsed };
```

**3. (Opsional) Hapus `console.log`**

Setelah verifikasi sukses end-to-end, hapus `console.log` di Prompt 2 — tidak perlu di production.

### Yang TIDAK perlu

- ❌ Buat tabel migration baru — schema `transactions` sudah ada dari module sebelumnya. Kalau kolom belum lengkap, **tambahkan via Supabase Studio** manual, bukan di prompt ini.
- ❌ Optimistic update di client — `revalidatePath` cukup cepat (~200ms).
- ❌ Toast notification library — `alert` di Prompt 1 sudah cukup untuk latihan.
- ❌ Rollback / transaction wrapper — single insert, tidak butuh.
- ❌ Buat endpoint REST `/api/transactions` — server action cukup, lebih simple.

### Verifikasi setelah file diubah

1. Login → buka halaman transaksi.
2. Ketik "ngopi 5000" → Tambah.
3. Tombol kembali aktif → list di bawah otomatis menampilkan transaksi baru (kategori "Makanan & Minuman", amount Rp 5.000, type expense, date hari ini).
4. Cek tabel `transactions` di Supabase Studio — row baru ada dengan field lengkap + `user_id` benar.
5. Test edge case: kosongkan input + Tambah → tombol `required` mencegah submit (HTML5 validation).
6. Test parsing edge case: "transferin 100rb ke ibu" → biasanya jadi expense, category "Lainnya" — bisa jadi bahan refleksi.

---

**Salin prompt berikut:**

```
Sambungkan parser dari Prompt 2 ke insert Supabase + revalidate
agar daftar transaksi auto-refresh setelah quick-add sukses.

GOAL:
- Modifikasi src/features/quick-add.ts.
- Setelah dapat parsed object dari tool_use:
  1. Ambil supabase client (createClient dari "@/lib/supabase/server").
  2. Ambil user dari supabase.auth.getUser(). Apabila tidak ada,
     return { ok: false, error: "Belum login." }.
  3. Insert ke tabel transactions dengan field:
     user_id, amount, type, category, date, note.
  4. Apabila insertError, return { ok: false, error: insertError.message }.
  5. revalidatePath("/transactions") (import dari "next/cache").
  6. Return { ok: true, transaction: parsed }.

CONTEXT:
- Tabel transactions sudah ada dengan kolom: id, user_id, date,
  category, type, amount, note, created_at.
- Pattern createClient + auth.getUser sudah dipakai di
  features/action.ts dan features/insight.ts.

GUARDRAIL:
- JANGAN modifikasi schema tabel.
- JANGAN tambah toast library — alert dari Prompt 1 cukup.
- JANGAN hapus console.log dulu, biarkan untuk debug. Hapus
  manual setelah verifikasi sukses.
- Apabila auth.getUser gagal, return error string yang
  human-readable, JANGAN throw.
```

**Verifikasi:**

1. Ketik "bensin 50rb" di UI → daftar transaksi muncul row baru `Transportasi · Rp 50.000 · expense · hari ini · "bensin"`.
2. Cek Supabase Studio: row dengan `user_id` user yang sedang login.
3. Submit ulang teks yang sama → row kedua muncul (no dedup — itu by design).

### Efek Perubahan — Contoh Konkret

Inilah hasil akhir Section 5 — **alur agentic end-to-end** yang utuh:

```
User: "ngopi 5000"
        │
        ▼
┌──────────────────────────────────────────────────────────┐
│ QuickAddTransaction (client) → form action               │
└──────────────────────────────────────────────────────────┘
        │ FormData("text": "ngopi 5000")
        ▼
┌──────────────────────────────────────────────────────────┐
│ quickAddTransaction (server action)                       │
│  1. Claude API + tool_use "save_transaction"             │
│  2. Parse → { amount: 5000, type: "expense", ... }       │
│  3. Supabase insert                                      │
│  4. revalidatePath("/transactions")                      │
└──────────────────────────────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────────────────────────┐
│ Halaman re-render → list menampilkan transaksi baru      │
└──────────────────────────────────────────────────────────┘
```

**Bandingkan dengan form tradisional yang dilewatkan:**

| Langkah user | Form klasik | Quick-add agentic |
|---|---|---|
| 1. Buka form / klik "+" | ✅ | ❌ (langsung input di atas list) |
| 2. Pilih tanggal (date picker) | ✅ | ❌ (auto hari ini) |
| 3. Pilih type (dropdown) | ✅ | ❌ (Claude infer) |
| 4. Pilih category (dropdown) | ✅ | ❌ (Claude infer) |
| 5. Isi amount | ✅ | ❌ (parse dari teks) |
| 6. Isi note | ✅ | ❌ (auto dari teks) |
| 7. Submit | ✅ | ✅ |
| **Total interaksi** | **7** | **2** (ketik + enter) |

**Efek yang terukur (estimasi dari quick-add experience umum):**

- **Waktu input per transaksi**: turun ~70% (20 detik → 5 detik).
- **Drop-off mencatat transaksi harian**: turun signifikan (friction terendah = makin sering catat).
- **Akurasi kategori**: setara atau lebih baik dari user yang sering "asal pilih" di dropdown.
- **Biaya per transaksi**: ~$0.0003 (Haiku 4.5, ~500 input + ~80 output tokens). Untuk 1000 transaksi/bulan = ~$0.30.

> 💡 **Pengenalan agentic AI**: Yang baru saja Anda bangun adalah **agent paling sederhana** — single-tool, single-call. Berikutnya di Module 06+ pola ini berkembang jadi:
> - **Multi-tool**: Claude bisa pilih `save_transaction`, `update_budget`, atau `query_history` tergantung intent user.
> - **Tool loop**: Claude memanggil tool, baca hasilnya, panggil tool lain, hingga task selesai.
> - **Planning + execution**: Claude pecah task kompleks ("rekapkan pengeluaran bulan lalu lalu kirim ke email saya") menjadi rangkaian tool call.
>
> Semua itu **berdiri di atas pola yang baru saja Anda kuasai**: schema JSON + `tool_choice` + server action.

---

## Validasi Akhir Section 5

- [ ] `<QuickAddTransaction />` muncul di atas daftar transaksi.
- [ ] `QUICK_ADD_SYSTEM` di `prompts.ts` reuse `ADVISOR_ROLE` & `ADVISOR_CONTEXT` (pola RCI Section 3).
- [ ] `SAVE_TRANSACTION_TOOL` punya `input_schema` lengkap (5 field required).
- [ ] `quickAddTransaction` pakai `tool_choice: { type: "tool", name: "save_transaction" }` dan `temperature: 0`.
- [ ] Teks "ngopi 5000" → tersimpan ke Supabase dengan field yang benar.
- [ ] List transaksi auto-refresh setelah insert (`revalidatePath`).
- [ ] Build production sukses (`npm run build`).
- [ ] Tidak ada regresi: chatbot Section 1–4 & insight Section 3 tetap jalan.

## Refleksi Section 5

1. Pakai `temperature: 0` di parser membuat output deterministik. Apa risikonya kalau Anda **menaikkan ke 0.7** untuk parser? (Test: ketik teks yang sama 5×, observasi.)
2. Daftar kategori di-hardcode di prompt. Bagaimana skala kalau kategori jadi 50+ (atau user bisa bikin custom)? Pendekatan apa yang Anda pertimbangkan? (Hint: dynamic injection vs separate categorizer call.)
3. Quick-add ini **tidak punya konfirmasi**. Untuk transaksi besar (mis. > 1 juta), apakah perlu step "review parsed result sebelum insert"? Apa trade-off UX-nya?
4. Apa bedanya **tool use** (latihan ini) vs **structured output via `response_format: json_schema`** (kalau API support)? Kapan Anda akan pakai yang mana?
5. Pola ini menumbuhkan ketergantungan ke API call untuk setiap insert. Bagaimana strategi **fallback** kalau Claude API down? (Hint: detect failure → fallback ke form klasik.)
6. Sekarang Anda punya **1 tool**. Sebutkan 3 tool tambahan yang masuk akal untuk Fin-App, dan kapan Claude harus memanggil mana — itu adalah cetak biru fitur agentic berikutnya.

---

⬅️ Kembali: **[Section 4 — Agentic Workflow](./latihan-4-agentic.md)** · 🏠 Index: **[Module 05 — Latihan](./latihan.md)**
