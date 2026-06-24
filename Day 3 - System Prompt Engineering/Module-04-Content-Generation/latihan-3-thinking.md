# Section 3 — Thinking / Thought

> Bagian dari **[Module 04 — Latihan](./latihan.md)**. Lanjutan dari **[Section 2](./latihan-2-text-generation.md)**.

> Latihan untuk mengaktifkan **extended thinking** pada model Claude Opus, dan menampilkan blok pemikiran di chatbot sebagai section yang dapat dilipat. Empat prompt siap copy-paste.
>
> **Estimasi Section 3**: 40–50 menit.

## Prasyarat Section 3

- [ ] Section 1–2 selesai (+ Latihan UI Module 03). Chatbot konsisten dengan persona AI Financial Advisor.
- [ ] Anda sudah membaca bagian Section 3 di `materi.md` dan memahami konsep extended thinking.

---

## 📚 Referensi Dokumentasi

Section ini bekerja dengan **extended thinking** — fitur khusus Claude Opus untuk menampilkan proses reasoning. Pahami dokumentasi resminya dulu:

- **[Extended Thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking)** — overview fitur, model yang mendukung, billing thinking tokens.
- **[Thinking content blocks](https://docs.claude.com/en/api/messages#response-content)** — struktur block `{ type: "thinking", thinking: "..." }` dan `{ type: "text", text: "..." }` di `response.content[]`.
- **[Output config & effort levels](https://docs.claude.com/en/api/messages)** — parameter `output_config.effort` (`"low"`, `"medium"`, `"high"`, `"xhigh"`, `"max"`) untuk Opus 4.7+.
- **[Models overview](https://docs.claude.com/en/docs/about-claude/models/overview)** — model mana yang punya extended thinking (Opus & Sonnet 4.x).

> 📌 **Versi API**: Module ini pakai format **Opus 4.7** (`type: "adaptive"` + `output_config.effort`). Format lama (`type: "enabled"` + `budget_tokens`) sudah deprecated — kalau lihat di tutorial luar yang masih pakai itu, ganti ke format baru.

---

## Prompt 1 — Aktifkan Extended Thinking di Server Action

### Walkthrough Manual (sebelum pakai prompt)

Perubahan besar di `advisor.ts`: ganti model, naikkan `max_tokens`, tambah parameter `thinking`, dan ubah return type. Pahami struktur `response.content[]` yang berubah jadi multi-block.

📂 **File yang diubah**: `src/features/advisor.ts` (modifikasi)

**1. Ganti model + tambah parameter `thinking` + naikkan `max_tokens`**

📍 Lokasi: **di dalam `client.messages.create({...})`**.

```ts
// src/features/advisor.ts — di dalam askAdvisor
const response = await client.messages.create({
  model: "claude-opus-4-7",                                    // ← UBAH dari haiku
  max_tokens: 4096,                                            // ← UBAH dari 1024
  temperature: 1,                                              // ← UBAH dari 0.5 (constraint thinking, lihat catatan di bawah)
  thinking: { type: "adaptive", display: "summarized" },       // ← BARU
  output_config: { effort: "max" },                            // ← BARU ('low' | 'medium' | 'high' | 'xhigh' | 'max')
  messages: [{ role: "user", content: INSTRUCTION_PREFIX + message }],
});
```

> ⚠️ **Constraint API thinking**: saat `thinking` aktif (`type: "adaptive"`), `temperature` **wajib `1`** (atau dihilangkan untuk pakai default 1). Apabila Anda biarkan `temperature: 0.5` peninggalan Section 2, API akan menolak dengan error 400 `"temperature may only be set to 1 when thinking is enabled or in adaptive mode"`. Alasannya: extended thinking butuh kreativitas maksimum model untuk menghasilkan chain-of-thought yang baik. Lihat [docs.claude.com extended-thinking](https://docs.claude.com/en/docs/build-with-claude/extended-thinking#important-considerations-when-using-extended-thinking).

**2. Ubah return type dan iterasi `content[]`**

📍 Lokasi: **di dalam function `askAdvisor`**, ganti logika `response.content[0]` dengan loop, dan ubah signature jadi return object.

```ts
// src/features/advisor.ts — signature + iterasi
export async function askAdvisor(message: string): Promise<{
  text: string;
  thinking: string | null;
}> {
  if (!message.trim()) throw new Error("Pesan tidak boleh kosong");

  const response = await client.messages.create({ /* ...lihat langkah 1... */ });

  let text = "";
  let thinking: string | null = null;
  for (const block of response.content) {
    if (block.type === "thinking") thinking = block.thinking;
    if (block.type === "text") text = block.text;
  }
  if (!text) throw new Error("Respons tidak berisi teks");
  return { text, thinking };
}
```

**3. Update JSDoc**

📍 Lokasi: **di atas function `askAdvisor`**. Sebutkan return type baru.

### Yang TIDAK perlu

- ❌ Menambah parameter `system` — Module 04 belum pakai.
- ❌ Menghapus `temperature` atau `INSTRUCTION_PREFIX` dari Section 2.
- ❌ Mengembalikan `response.content` mentah ke caller.
- ❌ Throw error kalau thinking kosong — `thinking: null` itu valid (mis. saat thinking off di masa depan).

### Verifikasi setelah file diubah

1. Jalankan `npx tsx --env-file=.env.local experiments/test-advisor.ts` dengan pertanyaan kompleks (mis. "Bandingkan reksadana vs deposito untuk DP rumah").
2. Output `result.thinking` berisi paragraf panjang penalaran Claude.
3. Output `result.text` berisi jawaban final ringkas.
4. Latensi terasa lebih lama (~10–20 detik) — wajar untuk Opus + thinking.

---

**Salin prompt berikut:**

```
Saya ingin mengaktifkan extended thinking di askAdvisor agar
Claude dapat menampilkan proses berpikirnya.

GOAL:
- Modifikasi src/features/advisor.ts.
- Ganti model dari "claude-haiku-4-5" menjadi "claude-opus-4-7"
  (extended thinking butuh Opus).
- Tambahkan parameter thinking + output_config:
  thinking: { type: "adaptive", display: "summarized" }
  output_config: { effort: "max" }   // 'low' | 'medium' | 'high' | 'xhigh' | 'max'
- Naikkan max_tokens jadi minimal 4096 (karena thinking +
  text dihitung bersama).

- Ubah return type askAdvisor dari `Promise<string>` menjadi
  Promise<{ text: string; thinking: string | null }>.
- Iterasi response.content array:
  - Untuk block type "thinking", simpan ke variabel thinking.
  - Untuk block type "text", simpan ke variabel text.
- Return object { text, thinking }.

CONTEXT:
- SDK Anthropic mengembalikan thinking block dengan field
  `thinking: string` (bukan `text`).
- Apabila thinking tidak aktif / tidak ada, thinking = null.

GUARDRAIL:
- Pertahankan validasi kosong, parameter temperature, dan
  prompt prefixing dari Section 2.
- JANGAN buang text content block — itu jawaban utama yang
  dipakai UI.
- JANGAN tambah parameter system — Module 04 belum pakai.
- Tambahkan JSDoc yang menjelaskan return type baru.
```

**Verifikasi:**

1. Test cepat dari `experiments/test-advisor.ts`:
   ```ts
   const result = await askAdvisor("Bandingkan menabung di reksadana vs deposito untuk DP rumah 5 tahun.");
   console.log("THINKING:\n", result.thinking);
   console.log("\nTEXT:\n", result.text);
   ```
2. Output thinking seharusnya berisi pemikiran panjang Claude tentang trade-off, sebelum jawaban final di text.

---

## Prompt 2 — Update Handler Chatbot untuk Terima Thinking

### Walkthrough Manual (sebelum pakai prompt)

Sekarang `askAdvisor` return object `{ text, thinking }`. Handler chatbot harus disesuaikan: tipe `Message` extended, dan push message dengan field baru.

📂 **File yang diubah**: `src/components/chat/ai-chat-panel.tsx` (modifikasi)

**1. Update tipe `Message`**

📍 Lokasi: **bagian atas file**, di deklarasi `type Message`.

```tsx
// src/components/chat/ai-chat-panel.tsx — bagian atas
type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
  thinking?: string | null;          // ← BARU
};
```

**2. Sesuaikan call `askAdvisor` di `runAdvisor` / `handleSend`**

📍 Lokasi: **di dalam function component**, di tempat `await askAdvisor(text)` dipanggil. Sekarang destructure result-nya.

```tsx
// src/components/chat/ai-chat-panel.tsx — di dalam handler
const { text, thinking } = await askAdvisor(text);                 // ← UBAH
setMessages((prev) => [
  ...prev,
  { id: crypto.randomUUID(), role: "assistant", content: text, thinking },  // ← BARU field
]);
```

> 💡 Lakukan hal yang sama di `handleRetry` (kalau Anda implementasikan di Section 1 Prompt 3).

### Yang TIDAK perlu

- ❌ Render thinking di UI — itu Prompt 3.
- ❌ Memberi thinking ke welcome message — biarkan `undefined`/null.
- ❌ Mengubah indikator typing / loading — itu Prompt 4.
- ❌ Membuat hook custom untuk state messages — overengineering.

### Verifikasi setelah file diubah

1. Reload, kirim pertanyaan kompleks.
2. Buka React DevTools → state `messages` → pesan assistant terakhir punya field `thinking` (string panjang).
3. UI belum berubah secara visual (thinking belum dirender).
4. Tidak ada TypeScript error di file.

---

**Salin prompt berikut:**

```
Sesuaikan handler di AIChatPanel agar dapat menerima return
type baru dari askAdvisor.

GOAL:
- Modifikasi src/components/chat/ai-chat-panel.tsx.
- Update tipe Message agar dapat menampung thinking:
  type Message = {
    id: string;
    role: "user" | "assistant";
    content: string;
    thinking?: string | null;  // ← baru
  };
- Handler kirim:
  - askAdvisor sekarang return { text, thinking }.
  - Push assistant message dengan content = text dan
    thinking = thinking.

CONTEXT:
- File yang dimodifikasi: ai-chat-panel.tsx.
- Hanya pesan dari assistant yang punya thinking — user
  tidak.

GUARDRAIL:
- Pertahankan loading state, error handling, dan welcome
  message dari Section 1.
- Welcome message tidak memiliki thinking (thinking = null
  atau undefined).
- JANGAN render thinking di UI dulu — itu di prompt 3.
```

**Verifikasi:**

1. Reload browser. Kirim pertanyaan kompleks.
2. Buka React DevTools → cari state messages → pesan assistant terbaru harus memiliki field `thinking` yang berisi string panjang.
3. Belum ada perubahan visual di chatbot (rendering thinking di prompt berikutnya).

---

## Prompt 3 — Render Thinking sebagai Collapsible Section

### Walkthrough Manual (sebelum pakai prompt)

Render thinking sebagai box collapsible di atas bubble assistant — default tertutup supaya tidak menggangu reading flow.

📂 **File yang diubah**: `src/components/chat/ai-chat-panel.tsx` (modifikasi). Mungkin juga: install Shadcn `collapsible`.

**1. Install Collapsible (kalau belum ada)**

```bash
npx shadcn@latest add collapsible
```

**2. Import komponen + ikon**

📍 Lokasi: **bagian import** di atas file.

```tsx
// src/components/chat/ai-chat-panel.tsx — import
import { Brain, ChevronDown, ChevronUp } from "lucide-react";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
```

**3. Render thinking box di atas content assistant**

📍 Lokasi: **di bagian JSX `messages.map(...)`**, di dalam bubble assistant — render hanya jika `m.role === "assistant" && m.thinking`. Default tertutup.

```tsx
// src/components/chat/ai-chat-panel.tsx — di dalam map render assistant
{m.role === "assistant" && m.thinking && (
  <Collapsible className="mb-2">
    <CollapsibleTrigger className="flex items-center gap-2 text-xs text-muted-foreground hover:text-foreground">
      <Brain className="h-3.5 w-3.5" />
      <span>Proses berpikir</span>
      <ChevronDown className="h-3 w-3 data-[state=open]:hidden" />
      <ChevronUp className="h-3 w-3 data-[state=closed]:hidden" />
    </CollapsibleTrigger>
    <CollapsibleContent className="mt-2 max-h-96 overflow-y-auto rounded-md bg-muted/50 p-3 text-xs italic text-muted-foreground">
      {m.thinking}
    </CollapsibleContent>
  </Collapsible>
)}
{/* content text dirender di bawah, sudah ada */}
```

### Yang TIDAK perlu

- ❌ Auto-expand thinking saat pesan baru datang.
- ❌ Markdown parsing untuk thinking — plain text saja (italic).
- ❌ Animasi typing untuk thinking.
- ❌ Render box thinking untuk welcome message atau user message.

### Verifikasi setelah file diubah

1. Reload, kirim pertanyaan kompleks.
2. Bubble assistant memiliki box "Proses berpikir" tertutup dengan ikon Brain di atas content.
3. Klik header → thinking muncul dengan styling italic abu-abu, ada scroll kalau panjang.
4. Welcome message tetap tampil normal tanpa box.

---

**Salin prompt berikut:**

```
Sekarang tampilkan thinking di UI sebagai section collapsible
di atas bubble jawaban assistant.

GOAL:
- Saat render pesan assistant yang memiliki thinking != null:
  - Di atas content text, tampilkan box collapsible berisi
    thinking.
  - Box header: ikon Brain (lucide-react) + label "Proses
    berpikir" + ikon chevron (ChevronDown saat tertutup,
    ChevronUp saat terbuka).
  - Default state: tertutup (terlipat).
  - Klik header → buka/tutup body.
  - Body collapsible: render thinking dengan styling text-
    muted-foreground italic, font-size text-sm, padding kecil,
    background bg-muted/50, rounded corner.
  - Thinking ditampilkan apa adanya (plain text, tanpa
    markdown parsing).

- Pesan tanpa thinking ditampilkan seperti biasa.

CONTEXT:
- File: ai-chat-panel.tsx.
- Pakai komponen Collapsible dari Shadcn apabila sudah
  ter-install. Apabila belum:
  npx shadcn@latest add collapsible
- Ikon Brain dari lucide-react.

GUARDRAIL:
- Default tertutup — user yang ingin lihat thinking buka
  manual.
- JANGAN auto-expand thinking saat pesan baru datang
  (mengganggu reading flow).
- Animasi expand/collapse harus smooth (Collapsible Shadcn
  sudah ini).
- Thinking dapat panjang sekali — pastikan ada scroll
  internal max-h-96 + overflow-y-auto.
```

**Verifikasi:**

1. Reload. Kirim pertanyaan kompleks.
2. Bubble assistant baru memiliki box "🧠 Proses berpikir ▼" di atasnya.
3. Klik header → thinking muncul dengan styling italic abu-abu.
4. Klik lagi → tertutup.
5. Welcome message dan pesan tanpa thinking tampil normal tanpa box.

---

## Prompt 4 — Indikator Visual Saat Thinking Aktif

### Walkthrough Manual (sebelum pakai prompt)

Ganti indikator typing generik dengan indikator khusus mode thinking + estimasi durasi — supaya user paham mengapa respons lebih lambat.

📂 **File yang diubah**: `src/components/chat/ai-chat-panel.tsx` (modifikasi)

**1. Import ikon `Brain`**

📍 Lokasi: **bagian import**. Kalau sudah di-import di Prompt 3, lewati.

```tsx
// src/components/chat/ai-chat-panel.tsx — import
import { Brain } from "lucide-react";
```

**2. Ganti indikator typing**

📍 Lokasi: **di JSX body messages area**, di blok `{isWaiting && (...)}` dari Section 1 Prompt 2. Ganti label + ikon, tambah baris estimasi.

```tsx
// src/components/chat/ai-chat-panel.tsx — di JSX body
{isWaiting && (
  <div className="flex flex-col gap-1">
    <div className="flex items-center gap-2 text-sm text-muted-foreground">
      <Brain className="h-4 w-4 animate-pulse" />
      <span>🧠 Sedang menganalisis...</span>
    </div>
    <p className="ml-6 text-xs text-muted-foreground/80">
      Mode thinking aktif — respons mungkin butuh 10-20 detik.
    </p>
  </div>
)}
```

### Yang TIDAK perlu

- ❌ Mengubah tata letak header atau footer.
- ❌ Menambah parameter baru ke `askAdvisor`.
- ❌ Animasi countdown — pesan estimasi statis cukup.
- ❌ Ganti warna utama panel.

### Verifikasi setelah file diubah

1. Reload, kirim pertanyaan kompleks.
2. Indikator baru muncul: "🧠 Sedang menganalisis..." + ikon Brain animate-pulse.
3. Baris estimasi "Mode thinking aktif — respons mungkin butuh 10-20 detik." tampil di bawah.
4. Setelah respons datang, indikator hilang, bubble assistant tampil dengan thinking section.

---

**Salin prompt berikut:**

```
Tambahkan indikator visual saat Claude sedang dalam mode
thinking — supaya user paham mengapa respons lebih lambat.

GOAL:
- Ganti pesan "AI sedang mengetik..." dari Section 1 menjadi
  dua tahap:
  1. Saat sedang menunggu (isWaiting = true), tampilkan:
     "🧠 Sedang menganalisis..."
     dengan ikon Brain + animate-pulse.
  2. (Akan diupdate di Section 5 saat streaming masuk.)

- Tambahkan estimasi: "Mode thinking aktif — respons mungkin
  butuh 10-20 detik."

CONTEXT:
- File: ai-chat-panel.tsx.
- Pesan ini tetap berada di bawah daftar pesan, sama posisi
  dengan typing indicator Section 2.

GUARDRAIL:
- HANYA tampilkan pesan estimasi ini saat thinking aktif
  (sekarang selalu aktif sejak Prompt 1; akan dikondisikan
  di Section 4 berdasarkan toggle).
- JANGAN ganti tata letak atau warna utama.
```

**Verifikasi:**

1. Kirim pertanyaan. Indikator baru muncul: "🧠 Sedang menganalisis..." + estimasi durasi.
2. Setelah respons datang, indikator hilang, bubble assistant + thinking section tampil.

---

## Validasi Akhir Section 3

- [ ] Server action mengaktifkan extended thinking dengan budget 2000.
- [ ] Return type askAdvisor adalah `{ text, thinking }`.
- [ ] Pesan assistant menampilkan box "Proses berpikir" collapsible.
- [ ] Default state box: tertutup.
- [ ] Indikator "Sedang menganalisis" muncul saat menunggu.
- [ ] Tidak ada regresi dari Section 1–2 (+ Latihan UI Module 03).

## Refleksi Section 3

1. Apakah thinking Claude **konsisten** dengan jawaban akhirnya? Atau ada divergensi?
2. Berapa kali Anda membuka thinking section dari curiosity vs dari kebutuhan praktis?
3. Apakah Anda merasa thinking section **mengganggu UX** atau **memperkaya**?
4. Adakah jenis pertanyaan di mana thinking menurut Anda **tidak diperlukan**?

---

⬅️ Kembali: **[Section 2](./latihan-2-text-generation.md)** · ➡️ Lanjut: **[Section 4 — Switching Thinking Mode](./latihan-4-switching-thinking.md)**
