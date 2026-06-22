# Section 1 — Bangun UI Chatbot AI Financial Advisor

> Bagian dari **[Module 04 — Latihan](./latihan.md)**. Pastikan baca [Prinsip Kontinuitas](./latihan.md#prinsip-kontinuitas-wajib-diperhatikan) sebelum mulai.

> Latihan untuk membangun **panel chatbot sisi kanan** di aplikasi Fin-App. Lima prompt siap copy-paste yang akan menghasilkan UI lengkap — masih tanpa AI logic, siap untuk disambungkan ke Claude API di Section 2.
>
> **Estimasi Section 1**: 45–60 menit.

## Prasyarat Section 1

- [ ] Aplikasi Fin-App jalan di `http://localhost:3000`.
- [ ] Claude Code aktif (`claude` di terminal kedua).
- [ ] Anda sudah membaca bagian Section 1 di `materi.md` dan memahami target visual.

---

## Prompt 1 — Setup Layout 3-Kolom

**Salin prompt berikut, paste ke Claude Code:**

```
Saya ingin menambahkan panel chatbot AI di sisi kanan aplikasi.
Mulai dengan menyiapkan layout-nya dulu.

GOAL:
- Update src/app/layout.tsx supaya isinya jadi 3-kolom:
  (1) AppSidebar di kiri (sudah ada).
  (2) Main content di tengah (children, sudah ada).
  (3) Panel chatbot di kanan dengan lebar tetap 380px,
      selalu sticky di sisi kanan layar.

CONTEXT:
- Saat ini layout sudah pakai SidebarProvider + AppSidebar +
  SidebarInset.
- Komponen panel chatbot baru bernama AIChatPanel di
  src/components/chat/ai-chat-panel.tsx.
- Untuk section ini, AIChatPanel cukup return sebuah div kosong
  dengan background card dan border-left — ISI akan diisi di
  prompt berikutnya.

GUARDRAIL:
- Layout main content TIDAK boleh berubah lebarnya secara
  drastis — pakai flex layout sehingga main mengambil sisa
  ruang setelah sidebar (kiri) dan AIChatPanel (kanan).
- Panel chatbot harus tetap terlihat saat di-scroll halaman
  (sticky atau h-screen + overflow internal).
- JANGAN mengubah komponen di dashboard atau transactions.

Setelah selesai, jelaskan singkat perubahan yang dilakukan.
```

**Verifikasi:**

1. Buka `http://localhost:3000`. Sidebar kiri, main content di tengah, dan **area kosong di kanan** (panel chatbot) seharusnya terlihat.
2. Resize browser — layout tetap rapi (panel kanan tidak melompat).
3. Scroll halaman — panel kanan tetap stay di tempatnya.

---

## Prompt 2 — Komponen AIChatPanel: Header + Body + Footer

**Salin prompt berikut:**

```
Sekarang isi komponen AIChatPanel dengan struktur dasar:
header, body, dan footer input.

GOAL:
- AIChatPanel terdiri dari tiga area vertikal:

  HEADER (atas, padding p-4, border-bottom):
  - Judul "AI Financial Advisor" — text-emerald-600 (dark:
    text-emerald-400), font-semibold text-base.
  - Subtitle "Get personalized financial advice." —
    text-sm text-muted-foreground.
  - Tombol close (ikon X dari lucide-react) di pojok kanan-atas,
    ghost button variant.

  BODY (tengah, flex-1, padding p-4, overflow-y-auto):
  - Untuk sekarang isi placeholder: <p className="text-sm
    text-muted-foreground">Belum ada percakapan. Mulai dengan
    bertanya di bawah.</p>
  - Siapkan struktur ini agar nanti dapat diisi list pesan.

  FOOTER (bawah, padding p-4, border-top):
  - Untuk sekarang placeholder kosong; akan diisi input di
    prompt berikutnya.

CONTEXT:
- File yang diubah: src/components/chat/ai-chat-panel.tsx.
- Pakai komponen Button dari Shadcn untuk tombol close.
- Pakai ikon X dari lucide-react.
- Struktur HTML: <aside class="flex flex-col h-full"> di akar.

GUARDRAIL:
- JANGAN bikin komponen Header / Body / Footer terpisah —
  cukup div di dalam satu file untuk sekarang.
- Tombol close belum perlu fungsional, cukup onClick dummy
  (akan diisi di prompt 5).
```

**Verifikasi:**

1. Reload browser. Panel kanan kini menampilkan:
   - Header "AI Financial Advisor" warna emerald.
   - Subtitle abu-abu.
   - Tombol ✕ di kanan-atas.
   - Body kosong dengan teks placeholder.
2. Layout 3-area (header / body / footer) terlihat rapi.

---

## Prompt 3 — Render Pesan dengan Markdown

**Salin prompt berikut:**

```
Tambahkan rendering pesan chat di body panel, dengan dukungan
markdown.

GOAL:
- Buat tipe Message: { id: string; role: "user" | "assistant";
  content: string }.
- Di AIChatPanel, definisikan array mock 3-4 pesan:
  - User: "Berikan tips menghemat pengeluaran bulanan."
  - Assistant: balasan dengan markdown — heading kecil, list
    bertanda, beberapa kata yang **bold**.
  - User: pertanyaan follow-up singkat.
  - Assistant: balasan singkat lagi.

- Render list pesan di body. Setiap pesan ditampilkan dalam
  bubble:
  - User: bubble emerald muda (bg-emerald-50, dark:
    bg-emerald-950/40), text-foreground, align right
    (ml-auto), max-w-[85%].
  - Assistant: tanpa bubble background — cukup text dengan
    padding, full width.
- Untuk pesan assistant, render content menggunakan
  react-markdown. Apabila package belum ter-install, jalankan:
  npm install react-markdown remark-gfm

CONTEXT:
- File: src/components/chat/ai-chat-panel.tsx.
- Konfigurasi react-markdown: pakai remarkPlugins=[remarkGfm]
  untuk dukungan tabel, strikethrough, dan lainnya.
- Style markdown elements (h1-h6, p, ul, ol, strong) dengan
  Tailwind class via components prop di ReactMarkdown.

GUARDRAIL:
- Pakai prose-sm dari @tailwindcss/typography APABILA sudah
  ter-install. Apabila belum, JANGAN install — cukup style
  manual lewat className di components prop ReactMarkdown.
- User bubble berbeda visual dari assistant bubble agar mudah
  dibedakan sekilas.
- Spacing antar pesan: gap-4 atau space-y-4.
```

**Verifikasi:**

1. Reload. Body panel sekarang menampilkan 3–4 mock pesan.
2. Pesan **assistant** memiliki:
   - Teks bold yang ter-render (tebal).
   - List berpoin/bernomor yang ter-render rapi.
3. Pesan **user** berada di kanan dengan background emerald muda.
4. Tidak ada bug rendering (raw `**` atau `1.` yang tidak ter-render).

---

## Prompt 4 — Input Area dengan Tombol Kirim

**Salin prompt berikut:**

```
Tambahkan input area di footer panel.

GOAL:
- Di footer AIChatPanel, render:
  - Textarea (atau Input) dengan placeholder "Ask AI Advisor here".
  - Tombol kirim ikon pesawat (Send dari lucide-react), warna
    emerald, di pojok kanan input.
- State lokal: useState untuk menampung teks yang sedang
  diketik.
- Tombol kirim:
  - Disabled saat input kosong (atau hanya whitespace).
  - Saat di-klik: untuk sekarang cukup PUSH satu pesan dummy
    ke array messages (role: "user", content: isi input),
    lalu KOSONGKAN input. Belum ada panggilan API.
- Enter key juga harus submit (bukan newline). Shift+Enter
  membuat newline (jika pakai Textarea).
- Auto-scroll body ke bawah saat pesan baru ditambahkan.

CONTEXT:
- Pakai komponen Textarea dari Shadcn (apabila ada) atau Input.
- Tombol kirim: ikon Send dari lucide-react, ukuran size="icon".
- Struktur footer: <div className="flex gap-2 items-end"> dengan
  textarea grow + button.
- Auto-scroll: useRef pada body div + useEffect yang panggil
  ref.current.scrollTo({ top: scrollHeight, behavior: "smooth" }).

GUARDRAIL:
- Mock messages dari prompt 3 jadikan initial state useState
  (bukan const) supaya bisa di-append.
- Tombol kirim TIDAK menampilkan loading state untuk sekarang
  (belum ada API call).
- Apabila Textarea belum ada di project, pakai:
  npx shadcn@latest add textarea
```

**Verifikasi:**

1. Reload. Footer panel menampilkan input + tombol kirim.
2. Ketik teks → tombol kirim aktif (tidak disabled).
3. Klik kirim → pesan muncul di body sebagai bubble user.
4. Input kosong otomatis.
5. Body auto-scroll ke bawah saat pesan baru muncul.
6. Tekan Enter saat fokus di input → ikut submit.

---

## Prompt 5 — Toggle Open/Close Panel

**Salin prompt berikut:**

```
Tambahkan kemampuan menutup dan membuka kembali panel
chatbot.

GOAL:
- State global atau context yang menyimpan apakah panel sedang
  open. Default: open.
- Tombol close (X) di header AIChatPanel: menutup panel.
- Saat panel tertutup, tampilkan tombol kecil di pojok kanan-
  bawah layar (floating action button) berisi ikon
  MessageCircle dari lucide-react, warna emerald — klik untuk
  membuka panel kembali.
- Animasi transition: panel slide dari kanan saat close/open
  (pakai Tailwind transition-transform translate-x-full).

CONTEXT:
- File yang berubah: src/app/layout.tsx,
  src/components/chat/ai-chat-panel.tsx, dan satu file baru
  untuk context (misal src/components/chat/chat-context.tsx).
- Pakai React Context untuk state open/close, karena diakses
  dari beberapa tempat (layout + panel + FAB).
- Provider letakkan di layout.tsx, di sekitar SidebarProvider.

GUARDRAIL:
- Panel TETAP berada di DOM saat tertutup — cukup translate
  off-screen, jangan unmount (supaya state percakapan tidak
  hilang).
- Floating button hanya muncul saat panel tertutup.
- Main content area mendapat ruang lebih saat panel tertutup
  (panel keluar dari flex flow saat closed — pakai conditional
  className width 0 atau absolute positioning).

Setelah selesai, jelaskan singkat strategi state management
yang dipilih (Context vs Zustand vs prop drilling), dan
mengapa.
```

**Verifikasi:**

1. Klik tombol ✕ di header panel → panel slide ke kanan, hilang.
2. Floating button (ikon chat) muncul di pojok kanan-bawah.
3. Klik floating button → panel kembali muncul dengan animasi slide.
4. Pesan yang sudah pernah dikirim **masih ada** setelah close-open (state tidak reset).
5. Main content (Dashboard / Transactions) mendapat ruang lebih saat panel tertutup.

---

## Validasi Akhir Section 1

Pastikan checklist berikut tercapai sebelum lanjut ke Section 2:

- [ ] Layout 3-kolom (sidebar · main · chatbot) bekerja rapi.
- [ ] Header chatbot menampilkan judul + subtitle + tombol close.
- [ ] Body menampilkan mock pesan dengan markdown ter-render.
- [ ] Input dapat diisi; tombol kirim push pesan dummy ke body.
- [ ] Enter di input juga mengirim.
- [ ] Auto-scroll ke bawah saat pesan baru muncul.
- [ ] Tombol close menutup panel; floating button membuka kembali.
- [ ] State pesan tidak reset saat panel di-close/open.
- [ ] Tidak ada error di console browser.
- [ ] Responsif (di lebar layar normal); panel kanan tidak menutupi sidebar atau main.

## Refleksi Section 1

Tuliskan pada catatan pribadi:

1. **Berapa iterasi prompt** rata-rata yang Anda butuhkan untuk setiap fitur?
2. **Prompt mana** yang paling mudah dipahami Claude (output sekali jadi)?
3. **Prompt mana** yang paling sering perlu Anda iterasi?
4. Adakah momen Claude mengusulkan pendekatan **berbeda dari guardrail** Anda? Bagaimana Anda memutuskannya?
5. Apakah Anda menambahkan **CLAUDE.md** baru selama latihan ini untuk konvensi tertentu?

---

➡️ Lanjut: **[Section 2 — Integrasi Claude API ke Chatbot](./latihan-section-2.md)**
