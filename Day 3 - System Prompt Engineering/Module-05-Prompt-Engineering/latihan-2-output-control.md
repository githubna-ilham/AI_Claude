# Section 2 — Sample Parameter & Output Control

> Bagian dari **[Module 05 — Latihan](./latihan.md)**. Lanjutan dari **[Section 1 — System Instruction](./latihan-1-system-instruction.md)**.

> Latihan eksplorasi parameter sampling dan teknik structured output. Empat prompt siap copy-paste.
>
> **Estimasi**: 45–60 menit.

## Prasyarat Section 2

- [ ] Section 1 selesai. AI Advisor pakai parameter `system`.

---

## 📚 Referensi Dokumentasi

Sebelum mulai, akan sangat membantu kalau Anda buka tab dokumentasi resmi untuk referensi cepat:

- **[Messages API parameters](https://docs.claude.com/en/api/messages)** — `temperature`, `top_p`, `top_k`, `stop_sequences`, dan kapan satu lebih cocok dari yang lain.
- **[Structured outputs](https://docs.claude.com/en/docs/build-with-claude/structured-outputs)** — JSON mode, schema enforcement, pola prompting agar Claude return JSON murni.
- **[Zod docs](https://zod.dev/)** — schema validation TypeScript yang akan dipakai untuk verifikasi output Claude.
- **[Stop sequences guide](https://docs.claude.com/en/api/messages)** — cara pakai `stop_sequences` untuk batasi output di marker tertentu (mis. `---END---`).

---

## Prompt 1 — Eksperimen `top_p` vs `temperature`

### Walkthrough Manual (sebelum pakai prompt)

Sebelum copy-paste prompt ke Claude, pahami dulu struktur file eksperimen `experiments/sampling-test.ts`. Tujuan: **rasakan** efek `temperature` vs `top_p` secara empiris.

📂 **File baru**: `experiments/sampling-test.ts` (script eksperimen)

**1. Import SDK + system prompt**

📍 Lokasi: **paling atas file**.

```ts
// experiments/sampling-test.ts — bagian import
import Anthropic from "@anthropic-ai/sdk";
import { ADVISOR_SYSTEM } from "../src/features/prompts";
```

**2. Definisikan 4 kombinasi sebagai array config**

📍 Lokasi: **module level**, supaya mudah loop.

```ts
// experiments/sampling-test.ts — module level
const CONFIGS = [
  { label: "A: temp=0, top_p=default",      temperature: 0.0 },
  { label: "B: temp=0.5, top_p=default",    temperature: 0.5 },
  { label: "C: temp=default, top_p=0.5",    top_p: 0.5 },
  { label: "D: temp=default, top_p=0.9",    top_p: 0.9 },
];
```

> ⚠️ **Anti-pattern**: JANGAN set `temperature` DAN `top_p` bersamaan dalam satu request. Per dokumentasi Anthropic, ini menghasilkan perilaku yang sulit diprediksi. Pilih satu.

**3. Loop tiap config, jalankan 2 kali untuk lihat variasi**

📍 Lokasi: **dalam async function `main()`**. Untuk setiap config: 2x `client.messages.create(...)` dengan pertanyaan yang sama. Print hasil di bawah label.

```ts
// experiments/sampling-test.ts — di main()
for (const cfg of CONFIGS) {
  console.log(`--- ${cfg.label} ---`);
  for (let i = 1; i <= 2; i++) {
    const resp = await client.messages.create({
      model: "claude-haiku-4-5",
      max_tokens: 200,
      system: ADVISOR_SYSTEM,
      messages: [{ role: "user", content: "Berikan 3 ide nama unik untuk celengan digital saya." }],
      ...(cfg.temperature !== undefined && { temperature: cfg.temperature }),
      ...(cfg.top_p !== undefined && { top_p: cfg.top_p }),
    });
    console.log(`Run ${i}:`, (resp.content[0] as any).text);
  }
}
```

### Yang TIDAK perlu

- ❌ Set `temperature` DAN `top_p` bersamaan (anti-pattern Anthropic).
- ❌ Test dengan ratusan iterasi — 2 run per config sudah cukup untuk lihat pattern.
- ❌ Visualisasi grafik — console output sudah cukup informatif.
- ❌ Simpan hasil ke file — fokus pada observasi langsung di terminal.

### Verifikasi setelah file dibuat

1. Jalankan: `npx tsx --env-file=.env.local experiments/sampling-test.ts`.
2. Output muncul 4 blok (A, B, C, D), masing-masing 2 run.
3. **A (temp=0)**: Run 1 ≈ Run 2 (konsisten — sampling deterministik).
4. **D (top_p=0.9)**: Run 1 ≠ Run 2 (variatif — sampling luas).
5. Catat observasi pribadi: setting mana paling cocok untuk **brainstorming**? Untuk **answer-the-same-question**?

---

**Salin prompt berikut:**

```
Bantu saya memahami beda top_p dan temperature.

GOAL:
- Buat file experiments/sampling-test.ts.
- Pertanyaan: "Berikan 3 ide nama unik untuk celengan
  digital saya."
- Jalankan 4 kombinasi:
  A: temperature=0.0, top_p tidak diset
  B: temperature=0.5, top_p tidak diset
  C: temperature tidak diset (default 1.0), top_p=0.5
  D: temperature tidak diset (default 1.0), top_p=0.9

- Untuk setiap kombinasi, jalankan 2 kali dan print hasil.
- Format output:
  --- A: temp=0, top_p=default ---
  Run 1: <hasil>
  Run 2: <hasil>
  ---

CONTEXT:
- Pakai Anthropic SDK langsung.
- Model: claude-haiku-4-5.
- max_tokens: 200.
- Boleh pakai system: ADVISOR_SYSTEM.

GUARDRAIL:
- JANGAN set temperature dan top_p bersamaan (anti-pattern
  per dokumentasi Anthropic).
- Catat observasi: pada setting mana hasilnya paling variatif?
  Paling konsisten?
```

**Verifikasi:**

1. Jalankan file.
2. Bandingkan output A vs D. A seharusnya konsisten antara Run 1 dan 2; D paling variatif.

---

## Prompt 2 — `stop_sequences` untuk Format Terkontrol

### Walkthrough Manual (sebelum pakai prompt)

Sebelum copy-paste prompt, pahami bagaimana `stop_sequences` bekerja. Tujuan: **batasi** output Claude di marker tertentu agar parsing downstream mudah.

📂 **File baru**: `experiments/stop-sequences-test.ts` (script eksperimen)

**1. Import + setup client**

📍 Lokasi: **paling atas file**.

```ts
// experiments/stop-sequences-test.ts — bagian import
import Anthropic from "@anthropic-ai/sdk";
import { ADVISOR_SYSTEM } from "../src/features/prompts";

const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });
```

**2. Definisikan prompt template + user message**

📍 Lokasi: **module level**, sebagai const string.

```ts
// experiments/stop-sequences-test.ts — module level
const USER_MSG = `Bulan ini income Rp 8.000.000, expense Rp 6.500.000.
Berikan ringkasan keuangan saya dengan format:

RINGKASAN:
<ringkasan singkat>

REKOMENDASI:
<rekomendasi>

---END---`;
```

**3. Dua pemanggilan API — dengan dan tanpa `stop_sequences`**

📍 Lokasi: **di async function `main()`**. Panggil dua kali pertanyaan yang sama, satu pakai `stop_sequences: ["---END---"]`, satu tidak. Print hasil + `stop_reason`.

```ts
// experiments/stop-sequences-test.ts — di main()
const withStop = await client.messages.create({
  model: "claude-haiku-4-5",
  max_tokens: 500,
  system: ADVISOR_SYSTEM,
  messages: [{ role: "user", content: USER_MSG }],
  stop_sequences: ["---END---"],          /* ← KEY */
});

const withoutStop = await client.messages.create({
  model: "claude-haiku-4-5",
  max_tokens: 500,
  system: ADVISOR_SYSTEM,
  messages: [{ role: "user", content: USER_MSG }],
});

console.log("=== DENGAN stop_sequences ===");
console.log("stop_reason:", withStop.stop_reason);    // expect: "stop_sequence"
console.log((withStop.content[0] as any).text);

console.log("\n=== TANPA stop_sequences ===");
console.log("stop_reason:", withoutStop.stop_reason); // expect: "end_turn"
console.log((withoutStop.content[0] as any).text);
```

### Yang TIDAK perlu

- ❌ Multiple stop sequences di array — satu marker `---END---` sudah cukup untuk eksperimen.
- ❌ Parse hasil output ke object — fokus pada **observasi** stop_reason saja.
- ❌ Loop puluhan kali — satu run per skenario sudah jelas.
- ❌ Test dengan model lain — Haiku cukup hemat untuk demo ini.

### Verifikasi setelah file dibuat

1. Jalankan: `npx tsx --env-file=.env.local experiments/stop-sequences-test.ts`.
2. **Dengan stop_sequences**: output berhenti tepat sebelum `---END---`, `stop_reason === "stop_sequence"`.
3. **Tanpa stop_sequences**: output mungkin terus menulis "kesimpulan tambahan", `stop_reason === "end_turn"`.
4. Output **tidak mengandung** `---END---` sendiri di skenario dengan stop_sequences — Claude berhenti sebelum mengeluarkannya.

---

**Salin prompt berikut:**

```
Saya ingin Claude menghasilkan output yang berhenti di
penanda tertentu.

GOAL:
- Buat file experiments/stop-sequences-test.ts.
- Minta Claude menghasilkan ringkasan finansial dengan
  format:
  
  RINGKASAN:
  <ringkasan singkat>
  
  REKOMENDASI:
  <rekomendasi>
  
  ---END---

- Tambahkan stop_sequences: ["---END---"].
- Print hasil + stop_reason.
- Bandingkan: dengan dan tanpa stop_sequences.

CONTEXT:
- User message contoh: "Bulan ini income Rp 8.000.000,
  expense Rp 6.500.000. Berikan ringkasan keuangan saya."
- Pakai system ADVISOR_SYSTEM.

GUARDRAIL:
- Tanpa stop_sequences: Claude mungkin terus menulis setelah
  ---END---. Dengan stop_sequences, berhenti tepat di sana.
- Print stop_reason: dengan stop_sequences = "stop_sequence";
  tanpa = "end_turn".
```

**Verifikasi:**

1. Dengan stop_sequences: output berhenti di ---END---, stop_reason = "stop_sequence".
2. Tanpa: output mungkin lanjut bercerita, stop_reason = "end_turn".

---

## Prompt 3 — Structured Output: Parse Transaksi dari Teks Natural

### Walkthrough Manual (sebelum pakai prompt)

Sebelum copy-paste prompt, pahami pola **structured output** yang akan dibuat. Tujuan: minta Claude return **JSON valid** yang langsung bisa di-validate dengan Zod.

📂 **File baru**: `src/features/parse-transaction.ts` (server action)

**1. Directive `"use server"` di baris pertama**

📍 Lokasi: **baris 1 file**. Wajib karena ini server action yang dipanggil dari client (UI di Prompt 4).

```ts
// src/features/parse-transaction.ts — baris pertama
"use server";
```

**2. Import SDK + Zod**

📍 Lokasi: **bagian import** setelah directive.

```ts
// src/features/parse-transaction.ts — bagian import
import Anthropic from "@anthropic-ai/sdk";
import { z } from "zod";
```

**3. Zod schema untuk validasi output Claude**

📍 Lokasi: **module level**, sebelum function. Schema ini = kontrak antara Claude dan app.

```ts
// src/features/parse-transaction.ts — module level
const TransactionSchema = z.object({
  type: z.enum(["income", "expense"]),
  amount: z.number().positive(),
  category: z.string().min(1),
  description: z.string().min(1),
});
```

**4. System instruction yang menekankan "JSON murni, tidak ada teks lain"**

📍 Lokasi: **module level**, const string.

```ts
// src/features/parse-transaction.ts — module level
const PARSER_SYSTEM = `Anda parser transaksi. Ekstrak data dari teks user dan return JSON dengan struktur:
{ "type": "income" | "expense", "amount": number, "category": string, "description": string }

Output WAJIB JSON valid murni. JANGAN tulis penjelasan, markdown, atau apapun di luar JSON.`;
```

**5. Function `parseTransaction(userText)`**

📍 Lokasi: **module level**, exported async function. Alur:

- Panggil Claude dengan `temperature: 0.0` (deterministik) + `system: PARSER_SYSTEM`.
- Ambil `response.content[0].text`.
- `JSON.parse(text)` di try/catch — kalau gagal, throw error.
- Validate hasil dengan `TransactionSchema.parse(...)` — Zod throw kalau tidak sesuai.
- Return parsed object.

```ts
// src/features/parse-transaction.ts — module level
export async function parseTransaction(userText: string) {
  const resp = await client.messages.create({
    model: "claude-haiku-4-5",
    max_tokens: 300,
    temperature: 0.0,
    system: PARSER_SYSTEM,
    messages: [{ role: "user", content: `Parse transaksi dari teks berikut: ${userText}` }],
  });
  const block = resp.content[0];
  if (block.type !== "text") throw new Error("Response bukan text block");
  const raw = JSON.parse(block.text);
  return TransactionSchema.parse(raw);
}
```

### Yang TIDAK perlu

- ❌ Retry otomatis kalau parse gagal — biarkan caller (UI) yang putuskan retry atau fallback manual.
- ❌ Markdown stripping — `temperature: 0.0` + system prompt yang tegas sudah cukup.
- ❌ Caching hasil — setiap input unik, tidak ada gain.
- ❌ Logger — cukup throw error message yang jelas.

### Verifikasi setelah file dibuat

1. Cek `"use server"` di baris 1.
2. Buat `experiments/test-parser.ts`:
   ```ts
   import { parseTransaction } from "../src/features/parse-transaction";
   async function main() {
     console.log(await parseTransaction("habis grab ke kantor 25 ribu"));
   }
   main().catch(console.error);
   ```
3. Jalankan: `npx tsx --env-file=.env.local experiments/test-parser.ts`.
4. Output: `{ type: 'expense', amount: 25000, category: 'Transport', description: 'Grab ke kantor' }`.
5. Coba input ambigu: "tagihan listrik 500rb" → harus `expense`, amount 500000.

---

**Salin prompt berikut:**

```
Saya ingin Claude mengekstrak data terstruktur dari pesan
casual user.

GOAL:
- Buat server action src/features/parse-transaction.ts.
- Function parseTransaction(userText: string): Promise<{
    type: "income" | "expense";
    amount: number;
    category: string;
    description: string;
  }>

- Gunakan Claude API dengan setting:
  - model: claude-haiku-4-5
  - temperature: 0.0 (deterministik)
  - system: instruksi singkat untuk parse ke JSON
  - User message: "Parse transaksi dari teks berikut: {text}"

- System instruction:
  "Anda parser. Ekstrak data transaksi dari teks user dan
  return JSON dengan struktur:
  { type: 'income' | 'expense', amount: number, category:
  string, description: string }
  Output WAJIB JSON valid, tidak ada teks lain."

- Validasi output dengan Zod schema.
- Return parsed object.

CONTEXT:
- Pakai Anthropic SDK dengan parameter system.
- Pakai zod yang sudah ter-install (kalau belum: npm install zod).
- Contoh input: "kemarin saya beli kopi 35rb di starbucks"
- Expected output: { type: "expense", amount: 35000, category:
  "Food & Drink", description: "Kopi di Starbucks" }.

GUARDRAIL:
- Apabila JSON tidak valid, throw error dengan pesan jelas.
- Apabila amount tidak ditemukan, throw error.
- File ini "use server".
```

**Verifikasi:**

1. Test cepat:
   ```ts
   // experiments/test-parser.ts
   const result = await parseTransaction("habis grab ke kantor 25 ribu");
   console.log(result);
   // Expected: { type: "expense", amount: 25000, category: "Transport"/"Transportation", description: "Grab ke kantor" }
   ```
2. Coba berbagai input casual: "gajian 5jt", "beli baju 200rb", "freelance 1.5jt".

---

## Prompt 4 — Integrasikan Parser ke UI

### Walkthrough Manual (sebelum pakai prompt)

Sebelum copy-paste prompt, pahami struktur UI baru yang akan ditambahkan ke halaman Transactions. Pola: **preview before commit** — user lihat hasil parse dulu, baru confirm.

📂 **File yang diubah**: `src/app/(app)/transactions/page.tsx` (atau komponen turunannya — sesuaikan dengan struktur Module 02). Plus mungkin komponen baru `quick-add-dialog.tsx`.

**1. Tombol "✨ Quick Add (AI)" di header Transactions**

📍 Lokasi: **JSX header** halaman Transactions, **di samping tombol "+ Add transaction"** yang sudah dibuat di Module 02.

```tsx
// src/app/(app)/transactions/page.tsx — di area header
<div className="flex gap-2">
  <Button onClick={() => setQuickAddOpen(true)} variant="outline">
    ✨ Quick Add (AI)
  </Button>
  <Button onClick={() => setAddOpen(true)}>+ Add transaction</Button>
</div>
```

**2. State untuk dialog + hasil parse**

📍 Lokasi: **di dalam komponen client** (`"use client"`).

```tsx
// di dalam komponen
const [quickAddOpen, setQuickAddOpen] = useState(false);
const [naturalText, setNaturalText] = useState("");
const [parsed, setParsed] = useState<ParsedTransaction | null>(null);
const [isParsing, setIsParsing] = useState(false);
const [parseError, setParseError] = useState<string | null>(null);
```

**3. Dialog Shadcn dengan dua mode: input vs preview**

📍 Lokasi: **JSX di dalam komponen**. Saat `parsed === null` → tampilkan textarea + tombol Parse. Saat `parsed !== null` → tampilkan preview + tombol Confirm/Edit Manual.

```tsx
// di JSX
<Dialog open={quickAddOpen} onOpenChange={setQuickAddOpen}>
  <DialogContent>
    {!parsed ? (
      <>
        <Textarea
          value={naturalText}
          onChange={(e) => setNaturalText(e.target.value)}
          placeholder="Ketik transaksi natural language Anda..."
        />
        {parseError && <p className="text-sm text-rose-600">{parseError}</p>}
        <Button onClick={handleParse} disabled={isParsing || !naturalText.trim()}>
          {isParsing ? "Parsing..." : "Parse & Add"}
        </Button>
      </>
    ) : (
      <>
        <div className="space-y-1 rounded border p-3 text-sm">
          <p><b>Type:</b> {parsed.type}</p>
          <p><b>Amount:</b> Rp {parsed.amount.toLocaleString("id-ID")}</p>
          <p><b>Category:</b> {parsed.category}</p>
          <p><b>Description:</b> {parsed.description}</p>
        </div>
        <div className="flex gap-2">
          <Button onClick={handleConfirm}>Confirm Add</Button>
          <Button variant="outline" onClick={handleEditManual}>Edit Manual</Button>
        </div>
      </>
    )}
  </DialogContent>
</Dialog>
```

**4. Handler `handleParse`**

📍 Lokasi: **function di dalam komponen**.

```tsx
async function handleParse() {
  setIsParsing(true);
  setParseError(null);
  try {
    const result = await parseTransaction(naturalText);
    setParsed(result);
  } catch (err) {
    setParseError(err instanceof Error ? err.message : "Gagal parse");
  } finally {
    setIsParsing(false);
  }
}
```

**5. Handler `handleConfirm` — panggil `createTransaction` dari Module 02**

📍 Lokasi: **function di dalam komponen**. Setelah sukses, reset state + tutup dialog.

### Yang TIDAK perlu

- ❌ **Langsung create tanpa preview** — selalu tunjukkan hasil parse dulu agar user verify.
- ❌ **Toast untuk error parsing** — error harus inline di dialog supaya user bisa edit text dan retry.
- ❌ **Auto-submit kalau confidence tinggi** — Claude tidak return confidence score, dan preview manual lebih aman.
- ❌ **Rewrite dialog Add Transaction** — tombol "Edit Manual" cukup tutup quick-add lalu buka dialog manual yang sudah ada, pre-fill kalau perlu.

### Verifikasi setelah file diubah

1. Reload halaman Transactions.
2. Klik "✨ Quick Add (AI)" → dialog terbuka dengan textarea.
3. Ketik "beli sepatu lari 850 ribu" → klik **Parse & Add**.
4. Preview muncul: type=expense, amount=850000, category=Shopping/Sports, description="Sepatu lari".
5. Klik **Confirm Add** → transaksi masuk ke tabel, dialog tertutup.
6. Test error: ketik teks aneh "asdf asdf" → error inline muncul, dialog tetap terbuka.

---

**Salin prompt berikut:**

```
Sekarang sambungkan parser ke UI Transactions agar user
bisa input dengan natural language.

GOAL:
- Di halaman /transactions, tambahkan tombol "✨ Quick Add
  (AI)" di samping tombol "+ Add transaction" yang sudah
  ada.
- Klik tombol → buka dialog kecil dengan:
  - Textarea: "Ketik transaksi natural language Anda..."
  - Tombol "Parse & Add"
- Saat di-klik:
  1. Tampilkan loading state.
  2. Panggil parseTransaction(text).
  3. Hasil parse di-preview di bawah textarea: type, amount,
     category, description.
  4. Tombol "Confirm Add" dan "Edit Manual".
  5. Klik Confirm → panggil createTransaction (yang sudah ada
     dari Module 02).

CONTEXT:
- Dialog dan komponen Shadcn sudah ter-install dari modul
  sebelumnya.
- Pakai useMutation untuk parseTransaction dan
  createTransaction.

GUARDRAIL:
- Apabila parsing gagal, tampilkan pesan error inline (bukan
  toast).
- Tombol "Edit Manual" → tutup dialog dan buka dialog Add
  Transaction biasa dengan field yang sudah pre-filled.
- JANGAN langsung create tanpa konfirmasi user — selalu
  preview dulu.
```

**Verifikasi:**

1. Klik "Quick Add (AI)" → dialog terbuka.
2. Ketik "beli sepatu lari 850 ribu" → klik Parse.
3. Preview menunjukkan: type=expense, amount=850000, category=Shopping/Sports, description="Sepatu lari".
4. Confirm → transaksi masuk ke tabel.

---

## Validasi Akhir Section 2

- [ ] File eksperimen sampling-test dan stop-sequences-test jalan.
- [ ] Server action `parseTransaction` ada di `src/features/parse-transaction.ts`.
- [ ] Validasi output JSON dengan Zod schema.
- [ ] Halaman Transactions punya tombol "Quick Add (AI)" yang berfungsi.
- [ ] Tidak ada regresi dari Section 1.

## Refleksi Section 2

1. Pada parameter mana Anda merasa **kontrol paling kuat**?
2. Apakah parser AI lebih cepat dari mengisi form manual?
3. Berapa kali parser memberikan hasil yang **salah**? Apa pattern kesalahannya?

---

⬅️ Kembali: **[Section 1](./latihan-1-system-instruction.md)** · ➡️ Lanjut: **[Section 3 — Role, Context, Instruction](./latihan-3-rci.md)**
