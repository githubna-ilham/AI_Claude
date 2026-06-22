# Materi Tambahan — UI Chatbot AI Financial Advisor

> **Konteks**: Materi pendamping untuk **[`latihan-ui-chatbot.md`](./latihan-ui-chatbot.md)** — latihan persiapan menuju Module 04.
>
> **Tujuan**: membangun panel chatbot di sisi kanan aplikasi Fin-App sebagai antarmuka untuk fitur AI Financial Advisor. Pada latihan ini isinya masih *mock content* — wiring ke Claude API dilakukan di Module 04.

## Apa yang Akan Anda Bangun?

Tampilan akhir aplikasi yang Anda tuju kurang lebih seperti berikut (deskripsi tekstual):

```
┌───────────────┬─────────────────────────────┬──────────────────────┐
│               │                             │  AI Financial Adv.  ✕│
│  Fina App     │   Transaction               │  Get personalized.. │
│               │   View and manage your...   │ ───────────────────  │
│ ▸ Dashboard   │                             │ [pesan AI: markdown │
│ ▸ Transaction │   ┌─────────────────────┐   │  dengan bold + list]│
│               │   │ Recent Transaction  │   │                     │
│               │   │ ─────────────────── │   │                     │
│               │   │ ...                 │   │                     │
│               │   └─────────────────────┘   │                     │
│               │                             │ ────────────────── │
│               │                             │ [Ask AI Advisor   ➤]│
└───────────────┴─────────────────────────────┴──────────────────────┘
```

**Karakteristik panel chatbot di sisi kanan:**

- **Lebar tetap** sekitar 380–400px, selalu terlihat di sisi kanan layar (sticky).
- **Header**: judul "AI Financial Advisor" warna emerald + subtitle "Get personalized financial advice." + tombol close (✕) di pojok kanan.
- **Area pesan**: scrollable, mendukung markdown rendering (**bold**, list, paragraf).
- **Input area** di bawah: text input dengan placeholder "Ask AI Advisor here" + tombol kirim berupa ikon pesawat (paper plane).
- **Toggle visibility**: tombol ✕ menutup panel; nantinya akan ada tombol di header untuk membuka kembali.

> 💡 **Pada latihan ini fokus hanya pada UI** — belum ada koneksi ke Claude API. Pesan-pesan masih *mock data* yang ditulis manual. Wiring ke API akan dilakukan di Module 04 Section 1.

## Alur Latihan

Anda akan mengeksekusi **5 prompt** ke Claude Code secara berurutan. Setiap prompt menghasilkan satu lapis UI:

| # | Prompt | Hasil |
|---|---|---|
| 1 | Setup layout 3-kolom | Layout root menampung sidebar kiri + main + panel kanan |
| 2 | Buat komponen `<AIChatPanel />` shell | Header + body kosong + footer input (struktur saja) |
| 3 | Render pesan dengan markdown | Area pesan menampilkan mock chat dengan bold/list |
| 4 | Input area interaktif | Input + tombol kirim, state lokal untuk menampung typing |
| 5 | Toggle open/close | Tombol close menyembunyikan panel; tombol toggle membuka kembali |

## Prasyarat

- [ ] Module 01–03 latihan inti selesai. Halaman Dashboard + Transactions berfungsi penuh. File `experiments/claude-test.ts` sudah berhasil dipanggil minimal sekali.
- [ ] Dev server jalan: `npm run dev`.
- [ ] Claude Code aktif di terminal terpisah.
- [ ] Sudah install `react-markdown` (Claude akan menambahkan otomatis di Prompt 3, atau Anda dapat install duluan: `npm install react-markdown remark-gfm`).

Lanjutkan ke [`latihan-ui-chatbot.md`](./latihan-ui-chatbot.md) untuk mulai mengeksekusi prompt-promptnya.

---

➡️ Setelah latihan ini selesai, lanjut: **[Module 04 — Section 1: Integrasi Claude API](../Module-04-Content-Generation/latihan-section-1.md)**
