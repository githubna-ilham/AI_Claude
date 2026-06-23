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

## Prompt 1 — Buat Route Handler Streaming

**Salin prompt berikut:**

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

**Salin prompt berikut:**

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

**Verifikasi:**

1. Reload browser. Kirim pertanyaan.
2. Indikator "sedang mengetik" hilang segera, lalu **kata-kata mulai bermunculan satu per satu** di bubble assistant.
3. Markdown ter-render sambil teks masuk (real-time formatting).
4. Saat thinking on, area thinking juga terisi token demi token.

---

## Prompt 3 — Cleanup: Hapus File `askAdvisor` Lama

**Salin prompt berikut:**

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
