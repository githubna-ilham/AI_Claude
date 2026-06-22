# Section 5 — Switching Thinking Mode

> Bagian dari **[Module 04 — Latihan](./latihan.md)**. Lanjutan dari **[Section 4](./latihan-section-4.md)**.

> Latihan untuk memberi user kontrol mengaktifkan / menonaktifkan extended thinking dan memilih budget effort. Empat prompt siap copy-paste.
>
> **Estimasi Section 5**: 30–40 menit.

## Prasyarat Section 5

- [ ] Section 1–4 selesai. Extended thinking aktif default; thinking block tampil di UI.
- [ ] Anda sudah membaca bagian Section 5 di `materi.md`.

---

## Prompt 1 — Tambah State Thinking di ChatContext

**Salin prompt berikut:**

```
Tambahkan state thinking config di ChatContext yang sudah ada.

GOAL:
- Modifikasi src/components/chat/chat-context.tsx (atau file
  context yang dibuat di Section 1).
- Tambah state baru:
  - thinkingEnabled: boolean (default: false)
  - thinkingBudget: "low" | "medium" | "high" (default: "medium")
- Ekspos setter: setThinkingEnabled, setThinkingBudget.
- Update tipe ChatContextValue.

CONTEXT:
- Mapping budget ke token count (untuk dipakai di prompt
  berikutnya):
  low    → 1024
  medium → 2048
  high   → 4096
- Default thinkingEnabled = false → respons cepat & murah
  untuk pertanyaan biasa.

GUARDRAIL:
- Pertahankan state isOpen dan toggleOpen dari Section 1.
- JANGAN export budget mapping ke component — dipakai
  internal di Prompt 3.
- Tambah JSDoc singkat di tipe baru.
```

**Verifikasi:**

1. Buka React DevTools → cari ChatProvider → state baru terlihat: `thinkingEnabled: false`, `thinkingBudget: "medium"`.
2. Belum ada perubahan visual (UI control di Prompt 2).

---

## Prompt 2 — Toggle UI di Header Chatbot

**Salin prompt berikut:**

```
Tambahkan tombol toggle thinking dan pemilih budget di header
chatbot.

GOAL:
- Di header AIChatPanel, tambahkan dua kontrol baru di kiri
  tombol close:
  1. Switch (Shadcn Switch component) berlabel "Thinking" —
     bound ke thinkingEnabled di context.
  2. Saat thinkingEnabled = true, tampilkan DropdownMenu
     dengan trigger ikon Settings (lucide-react).
     - Item menu: 3 radio button untuk budget (Low / Medium / High).
     - Bound ke thinkingBudget di context.

- Tata letak: <div className="flex items-center gap-2"> dengan
  switch, settings (kalau aktif), separator, close button.

CONTEXT:
- Pakai Switch dari Shadcn (apabila belum: npx shadcn@latest
  add switch).
- Pakai DropdownMenu yang sudah ter-install.
- Gunakan useChatContext hook untuk akses state.

GUARDRAIL:
- Switch dan settings TIDAK boleh shift judul "AI Financial
  Advisor" — gunakan ukuran kecil dan posisinya konsisten.
- Saat thinking dimatikan, settings hilang dengan smooth.
- Label "Thinking" boleh disembunyikan di mobile (sr-only).
```

**Verifikasi:**

1. Header chatbot kini memiliki switch "Thinking" + (saat aktif) ikon gear ⚙️ + tombol close ✕.
2. Klik switch → switch berubah state, tombol gear muncul/hilang.
3. Klik gear → menu Low / Medium / High muncul. Pilih satu → state thinkingBudget berubah.

---

## Prompt 3 — Pass Thinking Config ke Server Action

**Salin prompt berikut:**

```
Sekarang sambungkan toggle dari UI ke server action agar
benar-benar mempengaruhi panggilan API.

GOAL:
- Modifikasi signature askAdvisor di src/features/advisor.ts:
  askAdvisor(message: string, opts?: {
    thinking?: boolean;
    budget?: "low" | "medium" | "high";
  })

- Di dalam askAdvisor:
  - Apabila opts.thinking !== true: panggil API TANPA
    parameter thinking, dan gunakan model "claude-haiku-4-5"
    (hemat).
  - Apabila opts.thinking === true: gunakan model
    "claude-opus-4-7" + parameter thinking dengan budget
    sesuai opts.budget (default: medium = 2048).
  - Mapping budget: low=1024, medium=2048, high=4096.

- Return type tetap { text: string; thinking: string | null }.
  Saat thinking = false, thinking field selalu null.

- Modifikasi handler di AIChatPanel:
  - Baca thinkingEnabled & thinkingBudget dari useChatContext.
  - Pass sebagai opts saat memanggil askAdvisor.

CONTEXT:
- File: src/features/advisor.ts dan
  src/components/chat/ai-chat-panel.tsx.
- max_tokens: 1024 saat thinking off, 4096+ saat on.

GUARDRAIL:
- JANGAN hardcode model di luar branching. Setiap mode pakai
  model yang sesuai.
- Pertahankan validasi kosong, prompt prefixing, parameter
  temperature, dan error handling dari section sebelumnya.
- JANGAN tambah parameter system — Module 04 belum pakai.
- Indikator "Sedang menganalisis" dari Section 4 hanya
  tampil saat thinkingEnabled = true. Saat off, kembalikan
  ke "AI sedang mengetik..." dari Section 2.
```

**Verifikasi:**

1. Switch off → kirim pertanyaan → respons CEPAT (~3 detik) tanpa box thinking. Indikator "sedang mengetik...".
2. Switch on, budget medium → respons LEBIH LAMBAT (~10 detik) dengan box "Proses berpikir". Indikator "sedang menganalisis...".
3. Ganti budget ke high → respons lebih panjang & dalam, thinking lebih luas.
4. Switch off lagi → kembali ke mode cepat tanpa thinking.

---

## Prompt 4 — Indikator Konfigurasi Saat ini di Header

**Salin prompt berikut:**

```
Tambahkan indikator visual kecil di header agar user paham
konfigurasi current.

GOAL:
- Di bawah subtitle "Get personalized financial advice.",
  tambahkan satu baris keterangan kecil tentang mode aktif:

  Saat thinkingEnabled = false:
  "💡 Mode: cepat (Haiku)"

  Saat thinkingEnabled = true:
  "🧠 Mode: thinking · budget {budget}"

  (Pakai capitalize untuk budget: Low / Medium / High)

CONTEXT:
- File: ai-chat-panel.tsx.
- Style: text-xs text-muted-foreground, padding minimal.

GUARDRAIL:
- Indikator tidak boleh berukuran besar — fungsinya hint, bukan
  call-to-action.
- JANGAN tambah jargon teknis di indikator (mis. "budget_tokens")
  — gunakan kata yang dipahami user awam.
```

**Verifikasi:**

1. Toggle off → indikator: "💡 Mode: cepat (Haiku)".
2. Toggle on, budget Low → "🧠 Mode: thinking · budget Low".
3. Ganti budget → indikator update real-time.

---

## Validasi Akhir Section 5

- [ ] State thinkingEnabled & thinkingBudget ada di ChatContext.
- [ ] Switch + dropdown setting tampil di header chatbot.
- [ ] Server action menggunakan model & parameter berbeda berdasarkan toggle.
- [ ] Respons benar-benar lebih cepat saat thinking off.
- [ ] Indikator mode aktif tampil di header.
- [ ] Tidak ada regresi dari Section 1–4.

## Refleksi Section 5

1. Default off — apakah ini pilihan yang Anda setujui? Atau lebih baik default on?
2. Apakah user awam paham perbedaan budget low/medium/high? Cara menjelaskannya?
3. Pertanyaan tipe apa yang paling sering Anda toggle thinking?
4. Apakah perbedaan kualitas jawaban antara low vs high terasa signifikan?

---

⬅️ Kembali: **[Section 4](./latihan-section-4.md)** · ➡️ Lanjut: **[Section 6 — Streaming Process](./latihan-section-6.md)**
