# Section 3 — Mode Toggle: Personal (RAG) vs General (Chatbot Biasa)

> Bagian dari **[Module 07 — Latihan](./latihan.md)**. Lanjutan dari **[Section 2 — Implementasi RAG di Chatbot](./latihan-2-rag-chatbot.md)**.

> Di section ini kita memberi user **kontrol** atas perilaku chatbot: mode **Personal** (RAG — jawaban berdasarkan transaksi nyata) atau mode **General** (chatbot biasa — jawaban dari training Claude tanpa konteks transaksi). Dua prompt siap copy-paste.
>
> **Alur belajarnya**: backend + frontend dirombak dalam satu prompt (route handler menerima `mode` param dengan branching + UI segmented control) → verifikasi A/B di kedua mode.
>
> **Estimasi waktu**: 40–50 menit.

## Kenapa Butuh Mode Toggle?

Setelah Section 2, chatbot **selalu** retrieve transaksi user setiap pertanyaan. Ini bagus untuk pertanyaan tentang keuangan personal — tapi **boros** untuk pertanyaan general seperti _"apa itu inflasi?"_, _"jelaskan reksadana"_. Token retrieval terbuang, latency naik tanpa manfaat.

Solusinya: user memilih mode di awal percakapan (atau per pesan):

- **🎯 Personal** — chatbot RAG dengan akses transaksi user. Cocok untuk: _"kopi minggu lalu"_, _"transport ke kantor"_, _"berapa total belanja"_.
- **💬 General** — chatbot biasa tanpa konteks transaksi. Cocok untuk: _"apa itu inflasi"_, _"perbedaan saham vs reksadana"_, _"tips menabung umum"_.

Default kita pilih **General** — chatbot terbuka untuk pertanyaan apa pun terlebih dulu (konsep umum, tips edukatif), lalu user **opt-in** ke Personal ketika butuh jawaban berbasis transaksi pribadinya. Pola ini lebih ramah privasi: user secara sadar memilih "ya, saya mau Claude membaca transaksi saya".

## Prasyarat Section 3

- [ ] Section 1 & 2 selesai. Chatbot RAG sudah jalan dengan baik.
- [ ] Module 05 selesai. Konstanta `ADVISOR_SYSTEM_V3` masih ada di `src/features/prompts.ts` (kita akan reuse untuk mode General).
- [ ] UI chatbot di Fin-App sudah render daftar pesan + input field (dari Module 04/05).

---

## 📚 Referensi Dokumentasi

- **[React Server Components & Client Components](https://nextjs.org/docs/app/building-your-application/rendering/composition-patterns)** — pattern toggle di client component.
- **[Anthropic system prompts](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/system-prompts)** — perbedaan respons saat system prompt berubah.

---

## Prompt 1 — Backend + Frontend: Pasang Mode Toggle End-to-End

### Walkthrough Manual

Kita akan memodifikasi **dua file sekaligus** dalam satu prompt:

1. **Backend** (`src/app/api/advisor/route.ts`) — menerima `mode` param, branching system prompt berdasarkan `"personal"` vs `"general"`.
2. **Frontend** (komponen chatbot client) — segmented control dengan 2 pill button untuk pilih mode, lalu kirim `mode` di setiap POST body.

📂 **File yang dimodifikasi**:
- `src/app/api/advisor/route.ts` (sudah dimodifikasi di Section 2)
- Komponen chatbot client (mis. `src/components/advisor-chat.tsx`)

---

### Bagian A — Backend: Route Handler Menerima Param `mode`

**A.1. Type definition untuk `mode`**

📍 Lokasi: di atas function POST. Pakai type literal supaya typesafe.

```ts
// src/app/api/advisor/route.ts — di atas POST
type ChatMode = "personal" | "general";
```

**A.2. Ekstrak `mode` dari request body**

📍 Lokasi: di dalam POST, di baris `await req.json()`.

```ts
const { messages, mode: rawMode } = await req.json();
const mode: ChatMode = rawMode === "personal" ? "personal" : "general"; // default general
```

> 💡 Defensive default: kalau `mode` undefined atau invalid → fallback ke `"general"`. Tidak crash request, dan privacy-friendly (tidak otomatis baca transaksi user).

**A.3. Branch logic system prompt**

📍 Lokasi: ganti blok retrieve + build dari Section 2 dengan branching.

```ts
// src/app/api/advisor/route.ts — branching
import { ADVISOR_SYSTEM_V3 } from "@/features/prompts";

let system: string;

if (mode === "personal") {
  // Mode personal: RAG flow seperti Section 2
  const t0 = Date.now();
  const context = lastUserMessage
    ? await retrieveContextForChatbot(lastUserMessage, { threshold: 0.5, limit: 5 })
    : "(belum ada pertanyaan)";
  const tRetrieve = Date.now() - t0;

  system = buildAdvisorRAGSystem(context);

  console.log("[advisor/RAG]", {
    mode,
    query: lastUserMessage?.slice(0, 80),
    retrieveMs: tRetrieve,
    contextChars: context.length,
    hasContext: !context.startsWith("(tidak ada"),
  });
} else {
  // Mode general: chatbot biasa, tidak ada retrieval
  system = ADVISOR_SYSTEM_V3;

  console.log("[advisor/RAG]", {
    mode,
    query: lastUserMessage?.slice(0, 80),
  });
}
```

> 💡 Mode `general` tidak panggil `embed()` atau `match_transactions` — hemat latency (skip ~200ms) + hemat 1 Voyage API call per request.

**A.4. Stream Claude (tidak berubah)**

```ts
const stream = client.messages.stream({
  model: "claude-haiku-4-5",
  max_tokens: 1024,
  system,
  messages,
});
```

---

### Bagian B — Frontend: Segmented Control + Kirim `mode` di POST

**B.1. State untuk mode**

📍 Lokasi: di dalam component client, dekat state pesan.

```tsx
// src/components/advisor-chat.tsx — di dalam component
"use client";

import { useState } from "react";

type ChatMode = "personal" | "general";

export function AdvisorChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [mode, setMode] = useState<ChatMode>("general");  // ← state baru, default general
  // ... existing logic
}
```

**B.2. Komponen segmented control**

📍 Lokasi: di JSX, tepat di atas input field.

```tsx
// src/components/advisor-chat.tsx — di JSX
<div className="mb-3 flex gap-1 rounded-lg border border-gray-200 bg-gray-50 p-1">
  <button
    type="button"
    onClick={() => setMode("personal")}
    className={`flex-1 rounded px-3 py-1.5 text-sm font-medium transition ${
      mode === "personal"
        ? "bg-white text-blue-600 shadow-sm"
        : "text-gray-500 hover:text-gray-700"
    }`}
  >
    🎯 Personal
  </button>
  <button
    type="button"
    onClick={() => setMode("general")}
    className={`flex-1 rounded px-3 py-1.5 text-sm font-medium transition ${
      mode === "general"
        ? "bg-white text-blue-600 shadow-sm"
        : "text-gray-500 hover:text-gray-700"
    }`}
  >
    💬 General
  </button>
</div>

<p className="mb-2 text-xs text-gray-500">
  {mode === "personal"
    ? "Jawaban berdasarkan transaksi Anda."
    : "Chatbot umum tanpa konteks transaksi."}
</p>
```

**B.3. Kirim `mode` di POST body**

📍 Lokasi: di fetch / streaming call yang sudah ada.

```tsx
// src/components/advisor-chat.tsx — di handleSubmit atau setara
const response = await fetch("/api/advisor", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    messages: [...messages, { role: "user", content: input }],
    mode,                                       // ← tambahan
  }),
});
```

> 💡 **Mode boleh berubah di tengah percakapan**. User pakai personal untuk nanya transaksi, lalu switch ke general untuk nanya konsep umum. Tidak perlu reset history.

### Yang sebaiknya tidak dilakukan

**Backend**:
- ❌ Bikin route handler baru untuk general mode — branching di route yang sama lebih simple dan reuse pattern streaming.
- ❌ Pakai magic string `"PERSONAL"` / `"GENERAL"` (uppercase) atau angka (0/1) — string literal `"personal"`/`"general"` lebih readable + typesafe via union type.
- ❌ Default ke `"personal"` — di kursus ini kita pilih `"general"` agar privacy-friendly (user opt-in baru retrieval jalan). Kalau Anda override ke `"personal"`, pastikan ada onboarding yang jelas tentang akses transaksi.
- ❌ Lupa logging di branch general — kalau gagal debugging, susah mencari tahu kenapa Claude jawab "generic" padahal user mau personal.

**Frontend**:
- ❌ Bikin dropdown / dialog setting — toggle inline lebih cepat di-akses, mode adalah pilihan utama bukan settings tersembunyi.
- ❌ Auto-deteksi mode dari isi pesan user — kompleksitas tinggi (model perlu klasifikasi), keputusan harusnya user yang punya kendali.
- ❌ Reset history saat ganti mode — tidak perlu, biarkan percakapan lanjut.
- ❌ Lupa indikator visual mode aktif — user harus tahu mode mana yang sedang dipakai dari sekilas pandang.

### Verifikasi setelah file diubah

1. `npx tsc --noEmit` clean.
2. Dev server jalan tanpa error.
3. Reload chatbot UI di browser → segmented control muncul, default `💬 General` aktif.
4. Kirim pesan `"apa itu inflasi?"` di mode General → jawaban umum dari Claude, terminal log `mode: "general"` tanpa `retrieveMs`.
5. Klik `🎯 Personal` → pill aktif berpindah, tagline berubah ke "Jawaban berdasarkan transaksi Anda."
6. Kirim pesan `"kopi minggu lalu?"` di mode Personal → jawaban grounded di transaksi, terminal log `mode: "personal"` + `retrieveMs` + `hasContext`.
7. Klik kembali `💬 General` → tagline berubah jadi "Chatbot umum tanpa konteks transaksi."
8. (Opsional) POST manual via curl tanpa field `mode` → fallback ke general (default).

---

**Silakan salin prompt berikut, lalu paste ke Claude Code:**

```
Pasang mode toggle Personal vs General di chatbot AI Advisor
end-to-end. Modifikasi DUA file sekaligus: route handler
(backend branching) + komponen chatbot client (UI toggle).

=== BAGIAN A — BACKEND ===

GOAL A: Modifikasi src/app/api/advisor/route.ts (yang sudah
dimodifikasi di Section 2 untuk RAG).
- Tambahkan:
  1. Type literal: type ChatMode = "personal" | "general".
  2. Ekstrak dari req.json():
     const { messages, mode: rawMode } = await req.json();
     const mode: ChatMode = rawMode === "personal" ? "personal" : "general";
     // Defensive default: general kalau undefined/invalid
     // (privacy-friendly — user harus opt-in untuk RAG).
  3. Branch:
     - mode === "personal" → existing RAG flow Section 2
       (retrieve + buildAdvisorRAGSystem + log dengan
       mode, query, retrieveMs, contextChars, hasContext).
     - mode === "general" → import ADVISOR_SYSTEM_V3 dari
       @/features/prompts, set system = ADVISOR_SYSTEM_V3,
       SKIP retrieval. Log: { mode, query }.
  4. Stream Claude pakai variable `system`.

=== BAGIAN B — FRONTEND ===

GOAL B: Modifikasi komponen chatbot client (cari file
dengan pattern advisor-chat / chatbot / advisor.tsx di
src/components/ atau src/app).
- Tambahkan:
  1. Type literal: type ChatMode = "personal" | "general".
  2. State: const [mode, setMode] = useState<ChatMode>("general"). // default general
  3. JSX segmented control DI ATAS input field:
     - 2 pill button: "🎯 Personal" dan "💬 General".
     - Style Tailwind: container border + bg-gray-50 + p-1,
       button aktif bg-white + text-blue-600 + shadow-sm,
       button inactive text-gray-500 + hover:text-gray-700.
     - Klik = setMode("...").
  4. Tagline kecil di bawah toggle:
     - mode personal: "Jawaban berdasarkan transaksi Anda."
     - mode general: "Chatbot umum tanpa konteks transaksi."
  5. Sertakan `mode` di body fetch ke /api/advisor:
     body: JSON.stringify({ messages: [...], mode })

CONTEXT:
- Route handler sudah dimodifikasi di Section 2 untuk RAG
  (retrieve + buildAdvisorRAGSystem + log).
- ADVISOR_SYSTEM_V3 sudah ada di src/features/prompts.ts
  (Module 05 Section 3 RCI) — import dari sana.
- retrieveContextForChatbot + buildAdvisorRAGSystem sudah ada
  dari Section 1 & 2 Module 07.
- Komponen chatbot pakai "use client".
- Default mode: "general" (privacy-friendly default, user opt-in baru retrieve).
- Mode boleh berubah di tengah percakapan, tidak perlu reset
  history.

GUARDRAIL:
- JANGAN bikin route baru /api/advisor-general — branching
  di route yang sama lebih simple.
- JANGAN default ke "personal" — di kursus ini default
  WAJIB "general" (privacy-friendly, user opt-in baru
  retrieval jalan). Frontend useState awal "general",
  backend defensive fallback ke "general".
- JANGAN pakai magic string uppercase atau angka untuk mode.
  Pakai "personal"/"general" lowercase + union type.
- JANGAN panggil embed() / match_transactions di branch
  general — hemat latency & API call.
- JANGAN bikin dropdown / dialog terpisah untuk UI mode —
  toggle inline lebih cepat di-akses.
- JANGAN auto-deteksi mode dari isi pesan — user yang
  pegang kendali.
- JANGAN reset messages history saat ganti mode.
- Pastikan field `mode` ikut dikirim DI SETIAP request,
  bukan hanya sekali di awal.
- Pertahankan logging di kedua branch backend (untuk debugging).
- WAJIB indikator visual jelas (warna + tagline) untuk mode
  yang aktif.
```

**Verifikasi singkat:**

1. `npx tsc --noEmit` clean.
2. Reload UI → segmented control muncul, default `💬 General` aktif.
3. Kirim pesan di mode General → terminal log `mode: "general"` tanpa `retrieveMs`, jawaban Claude umum.
4. Klik `🎯 Personal` → visual berubah (warna + tagline).
5. Kirim pesan di mode Personal → terminal log `mode: "personal"` + `retrieveMs` + `hasContext`, jawaban dari konteks transaksi.
6. POST manual tanpa field `mode` → fallback ke general (default).

---

## Prompt 2 — (Opsional) Verifikasi A/B: Pertanyaan yang Sama, Mode Berbeda

### Walkthrough Manual

Untuk benar-benar merasakan perbedaan kedua mode, coba **pertanyaan yang sama** di kedua mode dan bandingkan jawabannya.

📂 **Tidak ada file yang dimodifikasi** — semua eksekusi manual di browser.

**1. Skenario A/B**

📍 Lokasi: chatbot UI Fin-App.

| Pertanyaan | Personal (RAG) | General (Biasa) |
|---|---|---|
| `"berapa pengeluaran kopi saya?"` | Sebutkan transaksi kopi spesifik dengan angka. | Generic — "tergantung kebiasaan Anda..." atau minta data. |
| `"apa itu inflasi?"` | Jawab umum (konteks tidak relevan, marker muncul). | Jawab umum dari training Claude. |
| `"transport ke kantor minggu lalu?"` | Sebutkan transaksi bensin/ojek dari data. | Generic — "biasanya orang naik motor / mobil / kendaraan umum..." |
| `"jelaskan reksadana saham"` | Jawab umum (konteks tidak relevan, marker muncul). | Jawab umum dari training Claude — biasanya lebih fokus & detail karena tidak terganggu konteks kosong. |

**2. Yang harus Anda perhatikan**

- ✅ **Untuk pertanyaan transaksi spesifik** (kopi, transport): mode Personal **jauh lebih akurat** dibanding General.
- ✅ **Untuk pertanyaan konsep umum** (inflasi, reksadana): mode General lebih **fokus & cepat** (skip retrieval).
- ⚠️ **Untuk pertanyaan transaksi di mode General**: Claude mungkin **minta data** atau jawab generic — itulah trade-off-nya.
- ⏱️ **Mode General lebih cepat ~200–500ms** karena skip retrieval.

**3. Refleksi UX**

Pertanyaannya: kapan default General cocok, kapan default Personal cocok? Untuk Fin-App di kursus ini, default General dipilih karena lebih **privacy-friendly** — user perlu opt-in eksplisit ke Personal sebelum chatbot membaca transaksi mereka. Untuk app dengan user yang sudah pasti ingin "asisten keuangan pribadi", default Personal masuk akal supaya value-add langsung terasa tanpa langkah ekstra.

### Yang sebaiknya tidak dilakukan

- ❌ Bikin script automation — verifikasi manual via UI cukup untuk merasakan UX bedanya.
- ❌ Bandingkan latency dengan stopwatch presisi — perkiraan kasar cukup.

### Verifikasi setelah eksperimen

1. Pertanyaan transaksi spesifik di mode Personal **selalu lebih akurat** dibanding mode General.
2. Pertanyaan konsep umum di kedua mode terasa setara, tapi General **lebih cepat**.
3. Anda paham trade-off-nya dan bisa menjelaskan ke user / stakeholder kapan mode mana cocok.

---

**Silakan salin prompt berikut, lalu paste ke Claude Code:**

```
Bantu saya menyusun test plan A/B untuk merasakan
perbedaan mode Personal vs General di chatbot, plus
panduan diagnose kalau hasilnya tidak sesuai harapan.

GOAL:
- Beri saya tabel skenario A/B (4 pertanyaan, masing-masing
  dicoba di kedua mode):
  1. Pertanyaan transaksi spesifik ("kopi", "transport").
  2. Pertanyaan konsep umum ("inflasi", "reksadana").

- Untuk tiap skenario, beri ekspektasi:
  - Mode Personal: bagaimana harapan jawaban + apakah ada
    angka spesifik atau marker no-context.
  - Mode General: bagaimana harapan jawaban + apakah
    generic atau detail dari training.
  - Latency: estimasi perbedaan (Personal lebih lambat
    ~200-500ms karena retrieval).

- Panduan diagnose:
  - Kalau mode Personal jawaban generic juga → cek apakah
    embed() jalan, cek log retrieveMs / hasContext.
  - Kalau mode General masih kelihatan "tahu" transaksi → cek
    apakah ADVISOR_SYSTEM_V3 yang dipakai (jangan sampai
    nyangkut di prompt RAG).
  - Kalau mode tidak berpengaruh sama sekali → cek apakah
    field `mode` benar-benar dikirim di fetch body (Network
    tab).

CONTEXT:
- Toggle UI + branching backend sudah jalan (Prompt 1).
- Saya akan jalankan manual di browser.

GUARDRAIL:
- JANGAN bikin script automation — manual cukup.
- JANGAN modifikasi kode di prompt ini — fokus verifikasi.
- Format jawaban sebagai test plan markdown, bukan kode.
```

**Verifikasi singkat:**

1. Anda menerima dari Claude: tabel skenario + ekspektasi + diagnostic guide.
2. Anda jalankan 4 skenario manual di kedua mode.
3. Perbedaan mode terasa jelas: Personal grounded di data, General lebih umum.
4. Latency Personal lebih lambat (~200-500ms) karena retrieval.

---

## Validasi Akhir Section 3

Sebelum Anda menutup Module 07, mari pastikan toggle bekerja end-to-end:

- [ ] Route `/api/advisor` menerima param `mode` dan branch berdasarkan `"personal"` / `"general"`.
- [ ] Default mode `"general"` (fallback untuk request tanpa field `mode`) — privacy-friendly.
- [ ] Mode `"general"` **tidak** panggil `embed()` atau `match_transactions` (verifikasi via log tidak ada `retrieveMs`).
- [ ] UI chatbot punya segmented control 2 pill (Personal / General) dengan indikator visual jelas.
- [ ] Tagline di bawah toggle berubah sesuai mode aktif.
- [ ] Mode dikirim di setiap POST body — bukan sekali di awal.
- [ ] `npx tsc --noEmit` clean.
- [ ] A/B test manual: pertanyaan transaksi di Personal lebih akurat; pertanyaan konsep umum di General lebih fokus.

## Refleksi Section 3

Refleksikan pertanyaan berikut secara mendalam sebelum melanjutkan ke section berikutnya:

1. Default mode kita `"general"` untuk privacy. Apa konsekuensi UX-nya — apakah user pemula mungkin "nyasar" bertanya transaksi di mode General lalu mendapat jawaban generic? Bagaimana cara menjembatani gap ini lewat onboarding atau hint kontekstual?
2. Mode toggle adalah keputusan **user**. Bagaimana kalau alternatifnya: Claude **sendiri** memutuskan kapan retrieve via tool use (agentic RAG)? Apa kelebihan/kekurangan kedua pendekatan?
3. Mode `general` mem-bypass retrieval — hemat ~200-500ms. Tapi kalau user nyasar ke mode general saat sebenarnya butuh data transaksi, jawaban jadi kurang berguna. Bagaimana cara mendeteksi mismatch ini di analytics?
4. Kalau Anda menambah mode ketiga (mis. `"savings-coach"` yang fokus pada saran menabung dengan system prompt khusus), bagaimana refactor route handler-nya supaya tetap clean? (hint: map dari mode → builder function)
5. UI toggle pakai pill button. Alternatif lain: dropdown, slider, voice command. Mana yang paling cocok untuk audience Fin-App, kenapa?
6. Sekarang chatbot punya 2 mode. Bagaimana cara Anda mengkomunikasikan ke user pemula bahwa kedua mode ini ada dan kapan pakai mana? (mis. onboarding tooltip, contoh pertanyaan, dst.)

---

⬅️ Kembali: **[Section 2 — Implementasi RAG di Chatbot](./latihan-2-rag-chatbot.md)** · 🏠 Index: **[Module 07 — Latihan](./latihan.md)** · ➡️ Lanjut: **[Module 08 — AI Agent](../Module-08-AI-Agent/materi.md)** (function calling)
