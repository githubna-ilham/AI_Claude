# Section 3 — Thinking / Thought

> Bagian dari **[Module 04 — Latihan](./latihan.md)**. Lanjutan dari **[Section 2](./latihan-2-text-generation.md)**.

> Latihan untuk mengaktifkan **extended thinking** pada model Claude Opus, dan menampilkan blok pemikiran di chatbot sebagai section yang dapat dilipat. Empat prompt siap copy-paste.
>
> **Estimasi Section 3**: 40–50 menit.

## Prasyarat Section 3

- [ ] Section 1–2 selesai (+ Latihan UI Module 03). Chatbot konsisten dengan persona AI Financial Advisor.
- [ ] Anda sudah membaca bagian Section 3 di `materi.md` dan memahami konsep extended thinking.

---

## Prompt 1 — Aktifkan Extended Thinking di Server Action

**Salin prompt berikut:**

```
Saya ingin mengaktifkan extended thinking di askAdvisor agar
Claude dapat menampilkan proses berpikirnya.

GOAL:
- Modifikasi src/features/advisor.ts.
- Ganti model dari "claude-haiku-4-5" menjadi "claude-opus-4-7"
  (extended thinking butuh Opus).
- Tambahkan parameter thinking:
  thinking: { type: "enabled", budget_tokens: 2000 }
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
