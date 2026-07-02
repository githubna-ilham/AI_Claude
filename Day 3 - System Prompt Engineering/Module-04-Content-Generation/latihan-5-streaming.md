# Section 5 — Streaming Process

> Bagian dari **[Module 04 — Latihan](./latihan.md)**. Lanjutan dari **[Section 4](./latihan-4-switching-thinking.md)**.

> Latihan untuk mengubah respons dari Section 1–4 menjadi **streaming** kata-demi-kata. Server action diganti route handler; client component meng-consume `ReadableStream`. Tiga prompt siap copy-paste.
>
> **Estimasi Section 5**: 50–60 menit (paling teknis di Module 04).

## Prasyarat Section 5

- [ ] Section 1–4 selesai (+ Latihan UI Module 03). Toggle thinking berfungsi.
- [ ] Anda sudah membaca bagian Section 5 di `materi.md`.

> ⚠️ **Peringatan**: Section ini melakukan **perubahan arsitektur** — dari server action ke route handler. Pastikan branch git Anda bersih sebelum mulai, supaya mudah rollback apabila bermasalah.

---

## 📚 Referensi Dokumentasi

Section ini bekerja dengan **streaming** + **route handler Next.js**. Tab dokumentasi yang perlu Anda buka:

- **[Streaming Messages](https://docs.claude.com/en/api/streaming)** — `client.messages.stream(...)`, async iterator pattern, SSE event types.
- **[Streaming events](https://docs.claude.com/en/api/messages-streaming)** — daftar event: `message_start`, `content_block_start`, `content_block_delta` (`text_delta`, `thinking_delta`), `message_stop`.
- **[Web Streams API (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/Streams_API)** — `ReadableStream`, `controller.enqueue()`, `TextEncoder`, `TextDecoder`.
- **[Next.js Route Handlers](https://nextjs.org/docs/app/building-your-application/routing/route-handlers)** — `POST(request)`, return `new Response(stream, ...)`, streaming response patterns.

> 💡 Streaming dengan thinking aktif menghasilkan **dua jenis delta**: `text_delta` dan `thinking_delta`. Walkthrough Section ini bungkus thinking dengan marker khusus `[[THINKING_DELTA]]...[[/THINKING_DELTA]]` supaya client dapat membedakan keduanya.

---

## Prompt 1 — Buat Route Handler Streaming

### Walkthrough Manual (sebelum pakai prompt)

Perubahan arsitektur: dari server action sinkron ke route handler streaming. Kunci: `client.messages.stream()` + bungkus dengan `ReadableStream` yang enqueue tiap delta.

📂 **File yang diubah**: `src/app/api/advisor/route.ts` (file baru)

**1. Setup client + helper budget**

📍 Lokasi: **paling atas file**.

```ts
// src/app/api/advisor/route.ts — bagian atas
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

const INSTRUCTION_PREFIX = `Anda menjawab dalam Bahasa Indonesia, ramah dan to-the-point. Pakai markdown: list bertanda untuk poin, bold untuk angka penting. Format Rupiah: "Rp 1.500.000". Persentase: "15%".

Pertanyaan: `;
```

**2. `POST` handler dengan `ReadableStream`**

📍 Lokasi: **di bawah setup**.

```ts
// src/app/api/advisor/route.ts
export async function POST(request: Request) {
  const body = await request.json();
  const { message, thinking: useThinking, budget } = body ?? {};

  if (typeof message !== "string" || !message.trim()) {
    return new Response("Pesan tidak boleh kosong", { status: 400 });
  }

  const encoder = new TextEncoder();
  const stream = new ReadableStream({
    async start(controller) {
      try {
        const sdkStream = client.messages.stream({
          model: useThinking ? "claude-opus-4-7" : "claude-haiku-4-5",
          max_tokens: useThinking ? 4096 : 1024,
          temperature: useThinking ? 1 : 0.5,                       // ← thinking aktif wajib 1
          ...(useThinking && {
            thinking: { type: "adaptive" as const },
            output_config: { effort: budget ?? "medium" },
          }),
          messages: [{ role: "user", content: INSTRUCTION_PREFIX + message }],
        });

        for await (const chunk of sdkStream) {
          if (chunk.type !== "content_block_delta") continue;
          if (chunk.delta.type === "text_delta") {
            controller.enqueue(encoder.encode(chunk.delta.text));
          } else if (chunk.delta.type === "thinking_delta") {
            controller.enqueue(
              encoder.encode(`[[THINKING_DELTA]]${chunk.delta.thinking}[[/THINKING_DELTA]]`)
            );
          }
        }
        controller.close();
      } catch (err) {
        controller.error(err);
      }
    },
  });

  return new Response(stream, {
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      "Cache-Control": "no-store",
    },
  });
}
```

### Yang TIDAK perlu

- ❌ Server-Sent Events (SSE) — plain text stream sudah cukup.
- ❌ Hapus `src/features/advisor.ts` sekarang (itu Prompt 3).
- ❌ Parameter `system` (Module 04 belum pakai).
- ❌ Logging atau telemetry production-grade.

### Verifikasi setelah file diubah

1. Dev server jalan tanpa error.
2. Test curl:
   ```bash
   curl -N -X POST http://localhost:3000/api/advisor \
     -H "Content-Type: application/json" \
     -d '{"message":"Berikan tip menabung."}'
   ```
3. Respons muncul potongan demi potongan, bukan sekaligus di akhir.
4. Test dengan `"thinking": true, "budget": "medium"` → terlihat tag `[[THINKING_DELTA]]...[[/THINKING_DELTA]]` di antara token.

---

<details>
<summary><strong>Salin prompt berikut, paste ke Claude Code</strong></summary>

```
Saya ingin mengganti server action askAdvisor dengan route
handler agar dapat streaming respons.

GOAL:
- Buat file baru src/app/api/advisor/route.ts.
- Ekspor function POST(request: Request).
- Body request: { message: string; thinking?: boolean;
  budget?: "low" | "medium" | "high" }.
- Pakai client.messages.stream() dari SDK Anthropic.
- Stream hasil sebagai ReadableStream berupa text plain
  (text/plain; charset=utf-8), token per token.

- Logic streaming:
  - Iterasi stream:
    for await (const chunk of stream) { ... }
  - Untuk chunk type "content_block_delta" dengan delta type
    "text_delta": enqueue chunk.delta.text ke controller.
  - Untuk chunk type "content_block_delta" dengan delta type
    "thinking_delta": enqueue dengan prefix khusus, mis.
    "[[THINKING_DELTA]]" + content + "[[/THINKING_DELTA]]"
    — agar client dapat membedakan thinking vs text.

- Pertahankan prompt prefixing, temperature, dan branching
  model (Haiku vs Opus) yang sama dengan askAdvisor di
  Section 4.

CONTEXT:
- Sebelum panggil API, gabungkan INSTRUCTION_PREFIX (dari
  Section 2) + message (sama pola dengan askAdvisor).
- Validasi: apabila message kosong atau missing, return
  Response("error message", { status: 400 }).
- Tipe: gunakan const encoder = new TextEncoder() untuk encode
  string ke Uint8Array.

GUARDRAIL:
- Apabila terjadi error di tengah stream, close controller
  dengan controller.error(err) — jangan abaikan.
- Set headers Cache-Control: "no-store" agar tidak ter-cache.
- File askAdvisor di src/features/advisor.ts JANGAN dihapus
  dulu — akan dihapus di prompt 3 setelah handler client
  selesai migrate.
```

</details>

**Verifikasi:**

1. File `src/app/api/advisor/route.ts` ada.
2. Test cepat dengan curl:
   ```bash
   curl -N -X POST http://localhost:3000/api/advisor \
     -H "Content-Type: application/json" \
     -d '{"message":"Berikan tip menabung."}'
   ```
3. Terminal seharusnya menampilkan respons **datang potongan demi potongan** (bukan sekaligus di akhir).

---

## Prompt 2 — Update Client untuk Konsumsi Stream

### Walkthrough Manual (sebelum pakai prompt)

Client konsumsi stream lewat `response.body.getReader()`. Push placeholder assistant dulu, lalu append chunk demi chunk via setState ke pesan terakhir.

📂 **File yang diubah**: `src/components/chat/ai-chat-panel.tsx` (modifikasi)

**1. Helper kecil untuk append ke pesan terakhir**

📍 Lokasi: **di luar function component** (atau di dalam, asal stabil). Helper mempermudah update content & thinking dari pesan placeholder.

```tsx
// src/components/chat/ai-chat-panel.tsx — helper
function appendToLast(
  prev: Message[],
  patch: { content?: string; thinking?: string }
): Message[] {
  if (prev.length === 0) return prev;
  const last = prev[prev.length - 1];
  const updated: Message = {
    ...last,
    content: last.content + (patch.content ?? ""),
    thinking: (last.thinking ?? "") + (patch.thinking ?? ""),
  };
  return [...prev.slice(0, -1), updated];
}
```

**2. Helper parsing chunk → text vs thinking**

```tsx
// src/components/chat/ai-chat-panel.tsx — helper
function parseChunk(chunk: string): { content: string; thinking: string } {
  let content = "";
  let thinking = "";
  const re = /\[\[THINKING_DELTA\]\]([\s\S]*?)\[\[\/THINKING_DELTA\]\]/g;
  let lastIdx = 0;
  let m: RegExpExecArray | null;
  while ((m = re.exec(chunk)) !== null) {
    content += chunk.slice(lastIdx, m.index);
    thinking += m[1];
    lastIdx = m.index + m[0].length;
  }
  content += chunk.slice(lastIdx);
  return { content, thinking };
}
```

**3. Ganti pemanggilan `askAdvisor` di handler kirim**

📍 Lokasi: **di dalam function component**, di `runAdvisor` / `handleSend`. Push placeholder dulu, lalu loop reader.

```tsx
// src/components/chat/ai-chat-panel.tsx — handler kirim
setMessages((prev) => [
  ...prev,
  { id: crypto.randomUUID(), role: "user", content: text },
  { id: crypto.randomUUID(), role: "assistant", content: "", thinking: thinkingEnabled ? "" : null },
]);
setIsWaiting(true);

try {
  const res = await fetch("/api/advisor", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: text, thinking: thinkingEnabled, budget: thinkingBudget }),
  });
  if (!res.ok || !res.body) throw new Error(await res.text());

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    const chunk = decoder.decode(value, { stream: true });
    const { content, thinking } = parseChunk(chunk);
    setMessages((prev) => appendToLast(prev, { content, thinking }));
  }
  setLastError(null);
} catch (err) {
  const m = err instanceof Error ? err.message : "Unknown error";
  setLastError({ message: m, userQuestion: text });
} finally {
  setIsWaiting(false);
}
```

### Yang TIDAK perlu

- ❌ `flushSync` — batching React 18 sudah cukup smooth.
- ❌ Mengubah error bubble / retry button.
- ❌ Mengganti `react-markdown` setup.
- ❌ Manual debounce — biarkan render se-cepat chunk datang.

### Verifikasi setelah file diubah

1. Reload, kirim pertanyaan.
2. Indikator typing hilang segera setelah token pertama datang; kata-kata muncul satu per satu di bubble assistant.
3. Markdown ter-render sambil token mengalir.
4. Thinking on: area "Proses berpikir" terisi token demi token.

---

<details>
<summary><strong>Salin prompt berikut, paste ke Claude Code</strong></summary>

```
Sekarang ubah handler kirim di AIChatPanel agar mengonsumsi
stream dari route handler.

GOAL:
- Di src/components/chat/ai-chat-panel.tsx, ganti pemanggilan
  askAdvisor dengan fetch ke /api/advisor.

- Alur baru saat user kirim:
  1. Push user message (sama seperti Section 1).
  2. PUSH placeholder assistant message ke state dengan
     content: "" dan thinking: thinkingEnabled ? "" : null.
  3. Set isWaiting = true.
  4. fetch POST /api/advisor dengan body { message,
     thinking, budget } dari context.
  5. Baca response.body sebagai stream:
     const reader = response.body.getReader();
     const decoder = new TextDecoder();
  6. Loop while (true) { const {done, value} = await
     reader.read(); ... }
  7. Setiap chunk:
     - Decode jadi string.
     - Parse: apabila chunk mengandung [[THINKING_DELTA]]xxx
       [[/THINKING_DELTA]], extract xxx dan append ke field
       thinking dari pesan placeholder.
     - Else: append ke field content dari pesan placeholder.
     - Update state messages dengan placeholder yang ter-update.
  8. Saat done = true: set isWaiting = false.

CONTEXT:
- File: ai-chat-panel.tsx.
- Trick "mutate last message": gunakan setMessages(prev => {
    const last = prev[prev.length - 1];
    const updated = { ...last, content: last.content + chunk };
    return [...prev.slice(0, -1), updated];
  });
- Error handling: try/catch sekitar fetch + reader loop.

GUARDRAIL:
- JANGAN langsung copy seluruh kode sekaligus ke saya — bantu
  pecah jadi function-function kecil yang mudah dibaca
  (parseChunk, appendToLast, dll.).
- Pertahankan error state, tombol retry, dan welcome message
  dari section sebelumnya.
- React 18: gunakan useTransition atau batching otomatis —
  jangan force flushSync kecuali perlu.
```

</details>

**Verifikasi:**

1. Reload browser. Kirim pertanyaan.
2. Indikator "sedang mengetik" hilang segera, lalu **kata-kata mulai bermunculan satu per satu** di bubble assistant.
3. Markdown ter-render sambil teks masuk (real-time formatting).
4. Saat thinking on, area thinking juga terisi token demi token.

---

## Prompt 3 — Cleanup: Hapus File `askAdvisor` Lama

### Walkthrough Manual (sebelum pakai prompt)

Cleanup file dead code. Manual sebenarnya cepat: grep dulu, hapus kalau bersih.

📂 **File yang diubah**: `src/features/advisor.ts` (hapus) + `src/components/chat/ai-chat-panel.tsx` (hapus import lama jika ada)

**1. Pastikan tidak ada caller `askAdvisor`**

📍 Lokasi: **terminal di root project**.

```bash
grep -rn "askAdvisor" src/ experiments/
```

Hasil yang diharapkan: kosong, atau hanya match di file `experiments/test-advisor.ts` (yang juga akan dihapus).

**2. Hapus file yang sudah tidak dipakai**

```bash
rm src/features/advisor.ts
rm experiments/test-advisor.ts   # apabila ada dari Section 1
```

**3. Bersihkan import di `ai-chat-panel.tsx` jika masih ada**

📍 Lokasi: **bagian import**. Kalau di Prompt 2 sebelumnya Anda lupa hapus baris `import { askAdvisor } from "@/features/advisor"`, hapus sekarang.

### Yang TIDAK perlu

- ❌ Menghapus `INSTRUCTION_PREFIX` constant (sudah dipindah ke route handler).
- ❌ Menghapus file `chat-context.tsx`.
- ❌ Refactor struktur folder.
- ❌ Menghapus file lain di `experiments/` (mis. `temperature-test.ts`) — bukan tujuan cleanup ini.

### Verifikasi setelah file diubah

1. `grep -rn "askAdvisor" src/` → kosong.
2. `npm run build` → sukses tanpa error.
3. Reload, chatbot tetap streaming jawab seperti biasa.
4. Toggle thinking on/off tetap berfungsi.

---

<details>
<summary><strong>Salin prompt berikut, paste ke Claude Code</strong></summary>

```
Sekarang stream sudah jalan. Bersihkan kode lama.

GOAL:
- Cek seluruh project untuk pemakaian function askAdvisor.
- Apabila tidak ada yang memakainya lagi (selain
  experiments/), hapus src/features/advisor.ts dan import-nya.
- File experiments/test-advisor.ts (kalau ada dari Section 2)
  boleh dihapus juga.

CONTEXT:
- Gunakan grep atau ToolSearch untuk pastikan tidak ada
  caller yang tertinggal.

GUARDRAIL:
- HANYA hapus apabila benar-benar tidak ada caller.
- Apabila ada caller di luar yang Anda tahu, beri tahu saya
  dulu sebelum hapus.
- File src/features/prompts.ts JANGAN dihapus — masih dipakai
  route handler.
```

</details>

**Verifikasi:**

1. Project di-build ulang (`npm run build`) tanpa error.
2. Tidak ada referensi `askAdvisor` di codebase.
3. Streaming tetap bekerja setelah cleanup.

---

## Validasi Akhir Section 5

- [ ] Route handler `/api/advisor` mengembalikan respons streaming.
- [ ] Client mengonsumsi stream dan menampilkan kata-demi-kata.
- [ ] Markdown ter-render saat teks masih streaming.
- [ ] Toggle thinking masih berfungsi (Haiku vs Opus).
- [ ] Thinking block juga terisi secara streaming.
- [ ] File `askAdvisor` lama sudah dihapus tanpa breaking caller.
- [ ] Build production sukses (`npm run build`).

## Refleksi Section 5

1. Berapa kira-kira waktu sampai **token pertama** muncul setelah submit? Bandingkan dengan latensi total Section 1.
2. Apakah pengalaman streaming terasa **lebih responsif** secara subjektif?
3. Adakah bug rendering yang Anda temui (mis. markdown salah parse di tengah stream)?
4. Apa kompleksitas baru yang Anda hadapi saat migrasi dari server action ke route handler?

---

⬅️ Kembali: **[Section 4](./latihan-4-switching-thinking.md)** · ➡️ Lanjut: **[Section 6 — Multi-Turn Conversation](./latihan-6-multi-turn.md)**
