# Module 01 — Latihan

> Latihan untuk memastikan kesiapan Anda sebelum melanjutkan ke Module 02. Estimasi waktu: 20–25 menit.

---

## Latihan 1 — Verifikasi Toolchain

Jalankan perintah berikut satu per satu, lalu **catat** outputnya pada kolom isian. Apabila ada yang gagal, silakan kembali ke bagian Troubleshooting pada `materi.md`.

| Perintah | Output yang Anda peroleh |
|---|---|
| `node -v` | |
| `npm -v` | |
| `git --version` | |
| `claude --version` | |

✅ **Lulus** apabila keempat perintah menampilkan nomor versi (bukan error).

---

## Latihan 2 — Bertanya kepada Claude Code Mengenai Project

Masuk ke folder project, lalu jalankan `claude`. Berikan prompt-prompt berikut, kemudian **tuliskan ringkasan jawabannya** (1–2 kalimat per pertanyaan):

1. **Prompt**: `apa stack utama yang digunakan project ini?`
   **Ringkasan**:

2. **Prompt**: `apa perbedaan antara src/lib/supabase/client.ts dan src/lib/supabase/server.ts?`
   **Ringkasan**:

3. **Prompt**: `mengapa file ini bernama proxy.ts dan bukan middleware.ts?`
   **Ringkasan**:

> 💡 **Tujuan latihan**: membiasakan diri **bertanya kepada Claude** sebagai langkah pertama dalam mengeksplorasi codebase yang baru bagi Anda.

---

## Latihan 3 — Modifikasi Sederhana

Buka `claude` di project, lalu berikan prompt:

```
> ubah judul tab browser di project ini menjadi "Fina App — Personal Finance"
```

Claude akan:

1. Mencari file yang mengatur metadata (`src/app/layout.tsx`).
2. Mengubah nilai `title` di dalam `export const metadata`.
3. Mengonfirmasi perubahan yang telah dilakukan.

**Verifikasi**: muat ulang `http://localhost:3000`. Tab browser kini menampilkan judul baru.

> 💡 Catatan: apabila dev server sedang berjalan, perubahan akan langsung di-*hot reload*. Anda tidak perlu me-restart server.

---

## Latihan 4 — Eksplorasi Struktur Folder Secara Mandiri

Tanpa membuka Claude, **jelajahi sendiri** isi folder berikut, kemudian jawab pertanyaannya:

| Folder / File | Pertanyaan | Jawaban |
|---|---|---|
| `src/app/page.tsx` | Halaman ini menampilkan apa? | |
| `src/components/dashboard/stat-cards.tsx` | Komponen ini dipanggil di mana? | |
| `src/features/action.ts` | Apa nama fungsi yang diekspor? | |
| `supabase/migrations/0001_init.sql` | Berapa banyak tabel yang dibuat di migration ini? | |
| `src/lib/dummy-data.ts` | Apakah file ini masih digunakan di dashboard saat ini? | |

> 💡 Anda diperbolehkan mengonfirmasi jawaban kepada Claude setelah menjawab secara mandiri.

---

## Latihan 5 — Eksperimen Data di Supabase

Setelah seluruh setup di materi.md selesai (project Supabase aktif, migration berjalan, data sample masuk, dan dashboard menampilkan angka), kerjakan eksperimen ringan berikut:

1. **Tambah satu transaksi baru** lewat SQL Editor:

   ```sql
   insert into public.transactions (type, category, amount, description, date) values
     ('expense', 'Coffee', 35000, 'Kopi pagi', '2026-06-12');
   ```

   Muat ulang dashboard. Angka pada card **Expenses** dan **Savings** seharusnya berubah.

2. **Edit langsung di Table Editor**: buka Table Editor → transactions, pilih satu baris, ubah nilai `amount`. Muat ulang dashboard — angka kembali berubah.

3. **Hapus satu baris** lewat Table Editor. Muat ulang dashboard — angka menyesuaikan.

> 💡 **Tujuan latihan**: meyakinkan diri bahwa **dashboard benar-benar membaca dari Supabase secara real time** (tanpa data dummy hard-coded). Apabila perubahan tidak muncul, ada yang salah pada konfigurasi `.env.local` atau RLS policy.

---

## Latihan 6 — Validasi Akhir

Pastikan checklist berikut tercentang sebelum melanjutkan ke Module 02:

- [ ] Latihan 1: seluruh tool menampilkan versinya.
- [ ] Latihan 2: dapat bertanya kepada Claude mengenai codebase.
- [ ] Latihan 3: berhasil mengubah title tab melalui Claude Code.
- [ ] Latihan 4: memahami peran struktur folder utama.
- [ ] Latihan 5: perubahan data di Supabase langsung terlihat di dashboard.
- [ ] Project Supabase Anda aktif, kedua migration berhasil, dan tabel `transactions` berisi minimal 6 baris.
- [ ] `.env.local` terisi dengan URL dan publishable key dari project Anda sendiri.
- [ ] `npm run dev` berjalan; browser menampilkan sidebar dan 3 stat card dengan **angka aktual** (bukan Rp 0).

---

## Refleksi (Opsional)

Silakan tuliskan pada catatan pribadi Anda:

1. **Hal baru** apa yang Anda pelajari pada modul ini?
2. **Hal yang masih membingungkan** — akan dibahas pada sesi tanya-jawab atau pada modul berikutnya.
3. **Hal yang menarik perhatian Anda** dari Claude Code — apa yang ingin Anda coba selanjutnya?
