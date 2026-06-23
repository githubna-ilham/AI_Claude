# Section 6 — Multi-Turn Conversation

> Bagian dari **[Module 04 — Latihan](./latihan.md)**. Lanjutan dari **[Section 5](./latihan-5-streaming.md)**.

> Latihan untuk menjadikan chatbot **memahami pertanyaan lanjutan** dengan mengirim riwayat percakapan ke Claude pada setiap request. Tiga prompt siap copy-paste.
>
> **Estimasi Section 6**: 30–40 menit.

## Prasyarat Section 6

- [ ] Section 1–5 selesai (+ Latihan UI Module 03). Streaming bekerja dengan toggle thinking.
- [ ] Anda sudah membaca bagian Section 6 di `materi.md`.

---

## Prompt 1 — Route Handler Terima Array `messages`

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
- [ ] **Parameter generation**: `temperature` 0.5 + prompt prefixing aktif. Respons konsisten dalam Bahasa Indonesia dengan format yang diinstruksikan.
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
