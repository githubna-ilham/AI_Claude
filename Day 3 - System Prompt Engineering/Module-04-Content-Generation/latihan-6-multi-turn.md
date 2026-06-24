# Section 6 — Multi-Turn Conversation

> Bagian dari **[Module 04 — Latihan](./latihan.md)**. Lanjutan dari **[Section 5](./latihan-5-streaming.md)**.

> Latihan untuk menjadikan chatbot **memahami pertanyaan lanjutan** dengan mengirim riwayat percakapan ke Claude pada setiap request. Tiga prompt siap copy-paste.
>
> **Estimasi Section 6**: 30–40 menit.

## Prasyarat Section 6

- [ ] Section 1–5 selesai (+ Latihan UI Module 03). Streaming bekerja dengan toggle thinking.
- [ ] Anda sudah membaca bagian Section 6 di `materi.md`.

---

## 📚 Referensi Dokumentasi

Section ini membangun **multi-turn conversation** dengan windowing. Referensi yang relevan:

- **[Messages array format](https://docs.claude.com/en/api/messages#body-messages)** — struktur `messages[]`: aturan alternasi `user`/`assistant`, role mana yang boleh duluan, last message harus `user`.
- **[Conversation patterns](https://docs.claude.com/en/docs/build-with-claude/conversations)** — pola multi-turn, context length management, kapan reset.
- **[Context windows](https://docs.claude.com/en/docs/build-with-claude/context-windows)** — limit token per model (Haiku/Sonnet/Opus), strategi truncation.
- **[Prompt caching (opsional)](https://docs.claude.com/en/docs/build-with-claude/prompt-caching)** — kalau riwayat percakapan panjang & berulang, prompt caching bisa hemat biaya signifikan (di luar scope module ini, tapi worth bookmark).

---

## Prompt 1 — Route Handler Terima Array `messages`

### Walkthrough Manual (sebelum pakai prompt)

Route handler perlu menerima array `messages` (riwayat) dan apply: (a) validasi role terakhir = "user", (b) windowing 10 terakhir, (c) prefix hanya ke user message terakhir.

📂 **File yang diubah**: `src/app/api/advisor/route.ts` (modifikasi)

**1. Update destructure body + validasi**

📍 Lokasi: **di awal function `POST`**.

```ts
// src/app/api/advisor/route.ts — awal POST
const body = await request.json();
const { messages, thinking: useThinking, budget } = body ?? {};

if (!Array.isArray(messages) || messages.length === 0) {
  return new Response("messages harus array non-kosong", { status: 400 });
}
const last = messages[messages.length - 1];
if (!last || last.role !== "user" || typeof last.content !== "string" || !last.content.trim()) {
  return new Response("Pesan terakhir harus role user dengan content non-kosong", { status: 400 });
}
for (const m of messages) {
  if (m.role !== "user" && m.role !== "assistant") {
    return new Response(`Role tidak valid: ${m.role}`, { status: 400 });
  }
}
```

**2. Windowing + apply prefix ke user message terakhir**

📍 Lokasi: **tepat di bawah validasi**, sebelum pemanggilan `client.messages.stream(...)`.

```ts
// src/app/api/advisor/route.ts
const recent = messages.slice(-10);
const apiMessages = recent.map((m, i) =>
  i === recent.length - 1
    ? { role: m.role, content: INSTRUCTION_PREFIX + m.content }
    : { role: m.role, content: m.content }
);
```

**3. Pakai `apiMessages` di `client.messages.stream(...)`**

📍 Lokasi: **di pemanggilan stream**.

```ts
// src/app/api/advisor/route.ts — di stream call
messages: apiMessages,
```

### Yang TIDAK perlu

- ❌ Mengubah logika streaming itu sendiri (loop chunk, ReadableStream).
- ❌ Validasi schema dengan Zod — manual check sudah cukup.
- ❌ Menyimpan riwayat di server / DB.
- ❌ Apply `INSTRUCTION_PREFIX` ke setiap user message (boros + bisa membingungkan model).

### Verifikasi setelah file diubah

1. Test curl dengan array messages:
   ```bash
   curl -N -X POST http://localhost:3000/api/advisor \
     -H "Content-Type: application/json" \
     -d '{"messages":[{"role":"user","content":"Berikan 3 tip menabung."},{"role":"assistant","content":"1. Audit pengeluaran tetap..."},{"role":"user","content":"Detailkan tip pertama."}]}'
   ```
2. Respons mendetail tip pertama (paham konteks).
3. Body tanpa `messages` atau elemen terakhir bukan user → 400.
4. Streaming behaviour Section 5 tidak berubah.

---

**Salin prompt berikut:**

```
Saya ingin route handler /api/advisor menerima riwayat
percakapan, bukan single message.

GOAL:
- Modifikasi src/app/api/advisor/route.ts.
- Body request baru:
  {
    messages: Array<{ role: "user" | "assistant"; content: string }>;
    thinking?: boolean;
    budget?: "low" | "medium" | "high";
  }
- Validasi: messages harus array non-kosong, dan ELEMENT
  TERAKHIR harus role: "user" (kalau bukan, return 400).
- Pass messages array langsung ke client.messages.stream().

- Tambah safety net: windowing 10 pesan terakhir saja yang
  dikirim ke API. Pesan lebih lama di-skip (tetap di client
  state tetapi tidak dikirim) untuk hemat token.

CONTEXT:
- Helper: const recentMessages = messages.slice(-10);
- INSTRUCTION_PREFIX (dari Section 2) dipasang di pesan user
  TERAKHIR sebelum dikirim ke API — bukan di setiap pesan
  user di riwayat.

GUARDRAIL:
- JANGAN ubah behaviour streaming dari Section 5 — hanya
  ubah input format.
- Validasi role: setiap pesan harus role "user" atau
  "assistant" (bukan "system").
- Welcome message dari Section 1 TIDAK perlu dikirim ke API
  (akan dijelaskan strateginya di prompt 2).
```

**Verifikasi:**

1. Test cepat dengan curl menggunakan array:
   ```bash
   curl -N -X POST http://localhost:3000/api/advisor \
     -H "Content-Type: application/json" \
     -d '{"messages":[{"role":"user","content":"Berikan 3 tip menabung."},{"role":"assistant","content":"1. Audit pengeluaran tetap..."},{"role":"user","content":"Detailkan tip pertama."}]}'
   ```
2. Respons Claude seharusnya mendetail tip nomor 1 (bukan minta klarifikasi).

---

## Prompt 2 — Client Kirim Riwayat Lengkap

### Walkthrough Manual (sebelum pakai prompt)

Client sekarang kirim seluruh state messages (kecuali welcome) sebagai array. Strategi paling sederhana: flag `isWelcome` di initial state, lalu filter.

📂 **File yang diubah**: `src/components/chat/ai-chat-panel.tsx` (modifikasi)

**1. Tambah flag `isWelcome` di tipe + initial state**

📍 Lokasi: **bagian atas file**, di `type Message` dan `INITIAL_MESSAGES`.

```tsx
// src/components/chat/ai-chat-panel.tsx
type Message = {
  id: string;
  role: "user" | "assistant";
  content: string;
  thinking?: string | null;
  isWelcome?: boolean;                          // ← BARU
};

const INITIAL_MESSAGES: Message[] = [
  {
    id: "welcome",
    role: "assistant",
    content: `Halo! Saya **AI Financial Advisor** Anda...`,
    isWelcome: true,                            // ← BARU
  },
];
```

**2. Helper strip + filter sebelum fetch**

📍 Lokasi: **di luar function component**.

```tsx
// src/components/chat/ai-chat-panel.tsx — helper
function toApiMessage(m: Message): { role: "user" | "assistant"; content: string } {
  return { role: m.role, content: m.content };
}
```

**3. Susun array di handler kirim**

📍 Lokasi: **di dalam handler kirim**, sebelum `fetch("/api/advisor", ...)`. Susun array dulu, **setelah itu** push user + placeholder ke state.

```tsx
// src/components/chat/ai-chat-panel.tsx — di handler kirim
const apiMessages = [
  ...messages.filter((m) => !m.isWelcome).map(toApiMessage),
  { role: "user" as const, content: text },
];

// push user + placeholder ke state SETELAH apiMessages disusun
setMessages((prev) => [
  ...prev,
  { id: crypto.randomUUID(), role: "user", content: text },
  { id: crypto.randomUUID(), role: "assistant", content: "", thinking: thinkingEnabled ? "" : null },
]);
setIsWaiting(true);

const res = await fetch("/api/advisor", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ messages: apiMessages, thinking: thinkingEnabled, budget: thinkingBudget }),
});
```

### Yang TIDAK perlu

- ❌ Kirim field `thinking` content ke API (boros + mengubah behaviour).
- ❌ Kirim field `id`, `isWelcome` ke API.
- ❌ Filter berdasarkan substring "AI Financial Advisor" — flag lebih reliable.
- ❌ Server-side history storage.

### Verifikasi setelah file diubah

1. Reload, welcome muncul.
2. Kirim "Berikan 3 tip menabung." → respons 3 tip.
3. Follow-up "Detailkan tip pertama." → Claude mendetail tip 1, bukan minta klarifikasi.
4. Lanjut "Yang ketiga?" → Claude tahu yang dimaksud tip 3.

---

**Salin prompt berikut:**

```
Sekarang ubah client agar mengirim seluruh state messages
sebagai riwayat percakapan.

GOAL:
- Di src/components/chat/ai-chat-panel.tsx, modifikasi handler
  kirim.
- Sebelum fetch:
  1. Susun array messages yang akan dikirim:
     - Filter: skip welcome message (yang content-nya
       mengandung "AI Financial Advisor" atau yang punya
       flag isWelcome).
     - Map: format hanya { role, content } — buang field
       thinking, id, dll.
  2. Append user message baru ke array tersebut.
- Body fetch: { messages: filteredArray, thinking, budget }.

- Tipe Message di state tetap punya field id, thinking, dll.
  — hanya saat KIRIM ke API yang di-strip.

CONTEXT:
- Welcome message biasanya pesan PERTAMA dengan role
  "assistant". Strategi paling sederhana: tambahkan flag
  isWelcome: true di initial state, lalu filter berdasarkan
  flag.
- Helper: function toApiMessage(m: Message) {
    return { role: m.role, content: m.content };
  }

GUARDRAIL:
- JANGAN kirim thinking content ke API (akan boros token
  dan mengubah behaviour model).
- JANGAN kirim placeholder assistant kosong yang baru saja
  di-push (push setelah API request dimulai).
- Pertahankan streaming behaviour Section 5 sepenuhnya.
```

**Verifikasi:**

1. Reload browser. Welcome message muncul.
2. Kirim pertanyaan A: "Berikan 3 tip menabung." → respons dengan 3 tip.
3. Kirim pertanyaan follow-up: "Detailkan tip pertama."
4. Respons seharusnya **mendetail tip nomor 1** dari pertanyaan A — bukan minta klarifikasi.
5. Lanjut: "Yang ketiga?" → Claude tahu yang dimaksud tip ketiga dari konteks A.

---

## Prompt 3 — Indikator Riwayat & Tombol "Mulai Percakapan Baru"

### Walkthrough Manual (sebelum pakai prompt)

UX terakhir: badge jumlah pesan + tombol reset (dengan konfirmasi). Hitung jumlah pesan **tidak termasuk welcome**, dan tampilkan warning windowing kalau > 8.

📂 **File yang diubah**: `src/components/chat/ai-chat-panel.tsx` (modifikasi)

**1. Install AlertDialog (kalau belum)**

```bash
npx shadcn@latest add alert-dialog
```

**2. Import komponen + ikon**

📍 Lokasi: **bagian import**.

```tsx
// src/components/chat/ai-chat-panel.tsx — import
import { RotateCcw } from "lucide-react";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";
```

**3. Hitung jumlah pesan (excluding welcome)**

📍 Lokasi: **di dalam function component**, di atas return JSX.

```tsx
// src/components/chat/ai-chat-panel.tsx — di dalam component
const conversationCount = messages.filter((m) => !m.isWelcome).length;
```

**4. Render badge + warning windowing di header**

📍 Lokasi: **di JSX header**, di bawah subtitle / di sebelah indikator mode dari Section 4 Prompt 4.

```tsx
// src/components/chat/ai-chat-panel.tsx — di header
<div className="flex items-center gap-2 text-xs text-muted-foreground">
  <span className="rounded-full bg-muted px-2 py-0.5">
    {conversationCount} pesan
  </span>
  {conversationCount > 8 && (
    <span>📜 windowing aktif — hanya 10 terakhir dikirim.</span>
  )}
</div>
```

**5. Tombol reset + AlertDialog**

📍 Lokasi: **di JSX header**, di area kanan (bersama Switch, Settings, Close dari Section 4).

```tsx
// src/components/chat/ai-chat-panel.tsx — di header right group
<AlertDialog>
  <AlertDialogTrigger asChild>
    <Button variant="ghost" size="icon" aria-label="Mulai percakapan baru">
      <RotateCcw className="h-4 w-4" />
    </Button>
  </AlertDialogTrigger>
  <AlertDialogContent>
    <AlertDialogHeader>
      <AlertDialogTitle>Hapus seluruh riwayat percakapan?</AlertDialogTitle>
      <AlertDialogDescription>
        Riwayat percakapan saat ini akan dihapus. Tindakan ini tidak bisa dibatalkan.
      </AlertDialogDescription>
    </AlertDialogHeader>
    <AlertDialogFooter>
      <AlertDialogCancel>Batal</AlertDialogCancel>
      <AlertDialogAction
        onClick={() => {
          setMessages(INITIAL_MESSAGES);
          setLastError(null);
        }}
      >
        Hapus
      </AlertDialogAction>
    </AlertDialogFooter>
  </AlertDialogContent>
</AlertDialog>
```

### Yang TIDAK perlu

- ❌ Reset tanpa konfirmasi.
- ❌ Persist riwayat ke localStorage.
- ❌ Animasi badge bertambah.
- ❌ Menampilkan welcome ke dalam hitungan.

### Verifikasi setelah file diubah

1. Reload, badge "0 pesan", warning windowing tidak tampil.
2. Kirim beberapa pertanyaan → badge naik.
3. Kirim hingga > 8 pesan → warning windowing muncul.
4. Klik RotateCcw → dialog konfirmasi muncul; klik Hapus → state kembali ke welcome saja.
5. Setelah reset, follow-up tidak paham konteks lama.

---

**Salin prompt berikut:**

```
Tambahkan UX untuk transparansi riwayat dan kemampuan reset.

GOAL:
- Di header chatbot (sebelah subtitle), tampilkan badge
  kecil: "{n} pesan" — di mana n adalah jumlah PESAN yang
  dikirim ke API (excluding welcome).
- Tambahkan tombol kecil "Mulai percakapan baru" di header
  (ikon RotateCcw dari lucide-react, ghost button).
- Saat tombol di-klik:
  - Konfirmasi via AlertDialog: "Hapus seluruh riwayat
    percakapan?"
  - Konfirm → reset state messages ke initial (hanya welcome
    message).

- Apabila jumlah pesan > 8, tambahkan keterangan kecil di
  badge: "📜 windowing aktif — hanya 10 terakhir dikirim."

CONTEXT:
- File: ai-chat-panel.tsx.
- Pakai AlertDialog yang sudah ter-install dari Module 02.
- Ikon: RotateCcw dari lucide-react.

GUARDRAIL:
- Tombol reset HARUS via konfirmasi — jangan langsung hapus
  (frustrasi user).
- Saat reset, kembali ke initial state dengan welcome
  message yang sama persis.
- Badge jumlah pesan TIDAK menghitung welcome message.
```

**Verifikasi:**

1. Reload. Badge menunjukkan "0 pesan".
2. Kirim beberapa pertanyaan → badge menghitung naik.
3. Kirim hingga > 8 pesan → indikator windowing muncul.
4. Klik tombol reset → dialog konfirmasi muncul.
5. Konfirmasi → chat kembali ke welcome message.
6. Setelah reset, follow-up question tidak lagi memahami konteks lama (sudah benar-benar fresh).

---

## Validasi Akhir Section 6 (Akhir Module 04)

- [ ] Route handler menerima array messages dan mengirim sebagai context.
- [ ] Client kirim seluruh riwayat (kecuali welcome) ke API.
- [ ] Pertanyaan follow-up dipahami dengan konteks pertanyaan sebelumnya.
- [ ] Windowing 10 pesan terakhir berfungsi (tidak crash di percakapan panjang).
- [ ] Badge jumlah pesan dan tombol reset tampil di header.
- [ ] Reset benar-benar membersihkan konteks.
- [ ] Build production sukses.

## Refleksi Section 6

1. Apakah pengalaman follow-up sekarang **terasa natural**?
2. Berapa pesan rata-rata sebelum Anda merasa perlu reset?
3. Apakah Anda akan mengganti windowing dengan **summarization** di project nyata? Kapan?
4. Adakah privasi concern dengan menyimpan riwayat? Bagaimana Anda menanganinya di production?

---

## 🎉 Validasi Akhir Module 04 (Seluruh 6 Section)

Selamat — Anda telah menyelesaikan Module 04! Pada akhir module ini, fitur AI Financial Advisor di Fin-App Anda seharusnya:

- [ ] **Panel chatbot** tampil di sisi kanan, dapat dibuka/tutup, dengan welcome message.
- [ ] **Markdown** ter-render rapi (bold, list, heading).
- [ ] **Pertanyaan user** dijawab oleh Claude API (bukan mock).
- [ ] **Parameter generation**: `temperature` conditional (0.5 untuk Haiku, 1 saat Opus + thinking aktif) + prompt prefixing aktif. Respons konsisten dalam Bahasa Indonesia dengan format yang diinstruksikan.
- [ ] **TIDAK ADA** parameter `system` di seluruh codebase Module 04 (system instruction adalah modul terpisah).
- [ ] **Toggle thinking** di header berfungsi; thinking block muncul saat aktif.
- [ ] **Budget low/medium/high** mempengaruhi kedalaman jawaban.
- [ ] **Streaming** kata-demi-kata berjalan smooth.
- [ ] **Multi-turn**: pertanyaan follow-up memahami konteks.
- [ ] **Reset percakapan** berfungsi via konfirmasi.
- [ ] **Tidak ada regresi** pada Dashboard / Transactions.

Apabila seluruh checklist tercapai, Anda telah membangun fitur AI percakapan production-grade dari nol — dengan pola yang dapat dipakai ulang untuk aplikasi lain di masa depan.

---

⬅️ Kembali: **[Section 5](./latihan-5-streaming.md)** · 🏠 Index: **[Module 04 — Latihan](./latihan.md)**
