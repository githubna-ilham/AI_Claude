# Section 2 — Upload UI + Base64 Pipeline

> Bagian dari **[Module 09 — Latihan](./latihan.md)**. Lanjutan dari **[Section 1 — Vision API Basics](./latihan-1-vision-basics.md)**.

> Di section ini kita membangun **delivery path** dari browser ke server: tombol upload di halaman transaksi → user pilih foto → file ter-encode base64 di client → dikirim ke server action `parseReceipt`. **Belum sampai parsing** — server action hanya log size + media type sebagai placeholder. Section 3 akan menambah Claude vision + insert ke DB. Dua prompt siap copy-paste.
>
> **Alur belajarnya**: server action skeleton (placeholder) → komponen UI client (file picker + FileReader) → pasang di halaman transaksi → verifikasi log di terminal server.
>
> **Estimasi waktu**: 30–40 menit.

## Prasyarat Section 2

- [ ] Section 1 selesai. Anda paham cara mengirim image ke Claude via base64.
- [ ] Halaman transaksi Fin-App sudah render daftar transaksi (dari Module 05 Section 5 quick-add).
- [ ] Anda paham server action pattern di Next.js App Router (sudah dipakai di `quickAddTransaction`).

---

## 📚 Referensi Dokumentasi

- **[Next.js Server Actions](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations)** — pattern `"use server"` + call dari client component.
- **[FileReader API (MDN)](https://developer.mozilla.org/en-US/docs/Web/API/FileReader)** — `readAsDataURL` untuk encode file ke base64.
- **[HTML input type="file"](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/file)** — accept attribute untuk filter MIME type.

---

## Prompt 1 — Server Action Skeleton `parseReceipt` (Placeholder)

### Walkthrough Manual

Sebelum kita bikin UI, sediakan dulu **server action skeleton** yang nanti dipanggil dari client. Di section ini hanya log size + media type sebagai bukti delivery path bekerja. Di Section 3 kita lengkapi dengan Claude vision + insert.

📂 **File baru**: `src/features/receipt-parser.ts`.

**1. Directive + signature**

📍 Lokasi: baris awal. `"use server"` wajib karena dipanggil dari client component.

```ts
// src/features/receipt-parser.ts
"use server";

export async function parseReceipt(input: { base64: string; mediaType: string }) {
  const sizeKB = Math.round((input.base64.length * 0.75) / 1024);

  console.log("[parseReceipt] received:", {
    mediaType: input.mediaType,
    sizeKB,
    preview: input.base64.slice(0, 50),  // 50 char pertama untuk sanity check
  });

  // Section 3: panggil Claude vision + tool use + insert
  return {
    message: `Foto diterima (${input.mediaType}, ${sizeKB} KB). Implementasi parsing menyusul di Section 3.`,
  };
}
```

> 💡 **Mengapa hanya log size + preview 50 char?** Logging full base64 = boros + berisiko PII. 50 char awal cukup untuk sanity check ("Yes, base64 received") tanpa mencemari log.

### Yang sebaiknya tidak dilakukan

- ❌ Memanggil Claude API di Section ini — Section 3 yang melengkapi. Fokus dulu pada delivery path.
- ❌ Logging full base64 string — boros log + risiko PII.
- ❌ Insert ke DB di skeleton ini — kalau ada bug delivery path, DB jadi pollutted dengan data placeholder.
- ❌ Memakai `Buffer.from(...)` di server action — pendekatan ini valid kalau Anda terima `File` object, tapi kita pakai pattern base64 string yang lebih simple dan match dengan Section 1 script.

### Verifikasi setelah file dibuat

1. File `src/features/receipt-parser.ts` ada dengan `"use server"` di baris pertama.
2. Export `parseReceipt(input)` dengan signature `{ base64: string; mediaType: string } → { message: string }`.
3. `npx tsc --noEmit` clean.
4. (Belum bisa di-call dari UI — Prompt 2 yang menambah UI.)

---

**Silakan salin prompt berikut, lalu paste ke Claude Code:**

```
Buat server action skeleton untuk receive foto kwitansi dari
client. Hanya log size + media type sebagai placeholder.
Implementasi parse lengkap (Claude vision + insert) di Section 3.

GOAL:
- Buat file baru src/features/receipt-parser.ts.
- Baris pertama: "use server";
- Ekspor async function parseReceipt(input: { base64: string;
  mediaType: string }) yang:
  1. Hitung sizeKB = Math.round((input.base64.length * 0.75) / 1024).
  2. console.log("[parseReceipt] received:", { mediaType,
     sizeKB, preview: input.base64.slice(0, 50) }).
  3. Return { message: "Foto diterima (${mediaType}, ${sizeKB} KB).
     Implementasi parsing menyusul di Section 3." }.

CONTEXT:
- Server action ini dipanggil dari client component
  UploadKwitansi (di Prompt 2).
- Pattern "use server" sama dengan quickAddTransaction Module
  05 Section 5.
- base64.length * 0.75 = perkiraan ukuran file asli (base64
  encoding ~33% lebih besar).

GUARDRAIL:
- JANGAN panggil Claude API di file ini — Section 3 yang
  melengkapi.
- JANGAN log full base64 string — boros + PII risk. Cukup
  50 char awal sebagai sanity check.
- JANGAN insert ke DB di skeleton ini.
- JANGAN bikin type definition kompleks — keep input shape
  simple { base64, mediaType }.
```

**Verifikasi singkat:**

1. File `src/features/receipt-parser.ts` ada dengan `"use server"`.
2. Export `parseReceipt` dengan signature yang benar.
3. `npx tsc --noEmit` clean.

---

## Prompt 2 — Komponen `<UploadKwitansi />` + Pasang di Halaman Transaksi

### Walkthrough Manual

Sekarang sisi client: komponen dengan file picker + `FileReader` untuk encode base64 + state management busy/result.

📂 **File baru**: `src/components/upload-kwitansi.tsx` + modifikasi `src/app/transactions/page.tsx` (atau path setara).

**1. Komponen client**

📍 Lokasi: `src/components/upload-kwitansi.tsx`. `"use client"` wajib karena pakai `useState` + `FileReader`.

```tsx
// src/components/upload-kwitansi.tsx
"use client";

import { useState } from "react";
import { parseReceipt } from "@/features/receipt-parser";

export function UploadKwitansi() {
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<string | null>(null);

  async function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;

    setBusy(true);
    setResult(null);
    try {
      const base64 = await fileToBase64(file);
      const response = await parseReceipt({ base64, mediaType: file.type });
      setResult(response.message);
    } catch (err) {
      setResult(`Error: ${err instanceof Error ? err.message : "unknown"}`);
    } finally {
      setBusy(false);
      // Reset input agar user bisa upload file sama lagi
      e.target.value = "";
    }
  }

  return (
    <div className="mb-4 rounded-lg border border-dashed border-gray-300 p-4">
      <label className="block cursor-pointer text-sm font-medium text-blue-600 hover:text-blue-700">
        📸 {busy ? "Memproses..." : "Upload Kwitansi (foto)"}
        <input
          type="file"
          accept="image/jpeg,image/png,image/webp"
          className="hidden"
          disabled={busy}
          onChange={handleFileChange}
        />
      </label>
      {result && (
        <p className="mt-2 text-sm text-gray-600" data-testid="upload-result">
          {result}
        </p>
      )}
    </div>
  );
}

function fileToBase64(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const dataUrl = reader.result as string;
      // dataUrl format: "data:image/jpeg;base64,/9j/4AAQSkZJ..."
      // Kita hanya butuh bagian setelah koma.
      resolve(dataUrl.split(",")[1]);
    };
    reader.onerror = () => reject(reader.error);
    reader.readAsDataURL(file);
  });
}
```

**2. Pasang di halaman transaksi**

📍 Lokasi: `src/app/transactions/page.tsx` (atau path setara di project Anda). Pasang di atas daftar transaksi, di bawah/dekat `<QuickAddTransaction />` dari Module 05 Section 5.

```tsx
// src/app/transactions/page.tsx — tambahan
import { UploadKwitansi } from "@/components/upload-kwitansi";

export default async function TransactionsPage() {
  // ... existing render
  return (
    <div className="container mx-auto p-6">
      <h1 className="mb-4 text-2xl font-bold">Transaksi</h1>
      <QuickAddTransaction />     {/* dari Module 05 Section 5 */}
      <UploadKwitansi />          {/* ← baru */}
      {/* render daftar transaksi di bawah */}
    </div>
  );
}
```

> 💡 **Mengapa `e.target.value = ""` di finally?** Tanpa reset, kalau user upload foto sama (mis. retry karena gagal), event `onChange` **tidak akan fire lagi** karena value-nya sama. Reset memastikan upload ulang selalu trigger handler.

### Yang sebaiknya tidak dilakukan

- ❌ Memakai `<form>` + submit button — overkill untuk satu file picker. Pattern `<label>` membungkus `<input type="file" hidden />` lebih clean dan native.
- ❌ Mengirim raw `File` object ke server action — server action menerima JSON-serializable saja. Base64 string adalah pendekatan paling kompatibel.
- ❌ Skip type filter di `accept` — tanpa filter, user bisa pilih PDF/MP4/dll. yang tidak didukung Section 1.
- ❌ Membuat preview thumbnail di Section ini — biarkan UX minimal dulu. Preview bisa ditambah di iterasi UI berikutnya.
- ❌ Mengabaikan `busy` state — tanpa disable input saat busy, user bisa spam upload yang membuat race condition.

### Verifikasi setelah file dibuat

1. File `src/components/upload-kwitansi.tsx` ada dengan `"use client"`.
2. Komponen `<UploadKwitansi />` ter-pasang di halaman transaksi.
3. Reload halaman → tombol `📸 Upload Kwitansi (foto)` muncul.
4. Klik tombol → file picker terbuka → pilih foto kwitansi.
5. Tombol berubah jadi `Memproses...`, lalu muncul pesan: `Foto diterima (image/jpeg, XXX KB). Implementasi parsing menyusul di Section 3.`
6. Di terminal dev server muncul log:
   ```
   [parseReceipt] received: { mediaType: 'image/jpeg', sizeKB: 234, preview: '/9j/4AAQSkZJ...' }
   ```
7. Upload foto **sama** lagi → handler fire lagi (bukti reset `value` bekerja).

---

**Silakan salin prompt berikut, lalu paste ke Claude Code:**

```
Buat komponen client UploadKwitansi: file picker yang encode
foto ke base64 via FileReader, lalu call server action
parseReceipt. Pasang di halaman transaksi.

GOAL:
- Buat file baru src/components/upload-kwitansi.tsx.
- "use client" di baris pertama.
- Komponen export function UploadKwitansi() yang berisi:
  1. State: const [busy, setBusy] = useState(false), const
     [result, setResult] = useState<string | null>(null).
  2. async function handleFileChange(e):
     - file = e.target.files?.[0]; if (!file) return.
     - setBusy(true), setResult(null).
     - try: const base64 = await fileToBase64(file);
            const response = await parseReceipt({ base64,
              mediaType: file.type });
            setResult(response.message).
     - catch (err): setResult(`Error: ${err.message}`).
     - finally: setBusy(false); e.target.value = ""
       (reset agar upload file sama lagi tetap trigger).
  3. JSX: <div> dengan <label> sebagai trigger (cursor-pointer,
     text-blue-600), <input type="file" hidden> di dalamnya,
     accept="image/jpeg,image/png,image/webp", disabled saat busy.
     Tampilkan teks tombol: "📸 [busy ? 'Memproses...' :
     'Upload Kwitansi (foto)']".
     Di bawah: <p> dengan result kalau ada.
- Helper function fileToBase64(file): Promise<string>:
  - FileReader.readAsDataURL → onload extract bagian setelah
    koma di dataUrl.

- Modifikasi halaman transaksi (cari src/app/transactions/page.tsx
  atau setara): import { UploadKwitansi } dan render-nya di atas
  daftar transaksi (dekat <QuickAddTransaction /> kalau ada dari
  Module 05 Section 5).

CONTEXT:
- Server action parseReceipt sudah ada di
  @/features/receipt-parser (Prompt 1).
- file.type adalah MIME type asli dari browser
  ("image/jpeg" / "image/png" / "image/webp").
- Tailwind tersedia.
- Pattern UI mengikuti QuickAddTransaction (Module 05 Section 5).

GUARDRAIL:
- JANGAN pakai <form> + submit — pattern <label>+<input hidden>
  lebih clean untuk single file picker.
- JANGAN kirim raw File object ke server action — pakai base64
  string (server action JSON-serializable only).
- WAJIB accept attribute filter MIME (jpeg, png, webp).
- WAJIB reset e.target.value = "" di finally supaya upload
  file sama bisa fire onChange lagi.
- JANGAN tambah preview thumbnail di section ini — keep
  minimal, iterasi UI nanti.
- WAJIB disable input saat busy untuk hindari race condition.
```

**Verifikasi singkat:**

1. Reload halaman transaksi → tombol upload muncul.
2. Pilih foto kwitansi → tombol berubah `Memproses...`.
3. Muncul pesan placeholder `"Foto diterima ..."`.
4. Terminal dev server menampilkan log `[parseReceipt] received: { ... }`.
5. Upload foto sama lagi → handler tetap fire (reset value bekerja).

---

## Validasi Akhir Section 2

Sebelum Anda lanjut ke Section 3, mari pastikan delivery path browser → server kokoh:

- [ ] File `src/features/receipt-parser.ts` ada dengan `"use server"` dan ekspor `parseReceipt(input)`.
- [ ] File `src/components/upload-kwitansi.tsx` ada dengan `"use client"` dan ekspor `<UploadKwitansi />`.
- [ ] Komponen ter-pasang di halaman transaksi.
- [ ] Tombol upload muncul, klik → file picker → pilih foto → pesan placeholder muncul.
- [ ] Terminal dev server menampilkan log `mediaType`, `sizeKB`, `preview` (50 char base64).
- [ ] Upload foto **sama** dua kali berturut-turut → handler fire dua kali (reset `value` bekerja).
- [ ] Input file di-disable saat busy.
- [ ] `npx tsc --noEmit` clean.

## Refleksi Section 2

Refleksikan pertanyaan berikut secara mendalam sebelum melanjutkan ke section berikutnya:

1. Saat ini kita kirim base64 string ke server action. Apa trade-off vs pendekatan **upload ke Supabase Storage dulu**, lalu kirim URL ke server action? Mana yang lebih cocok untuk Fin-App skala kecil vs production besar?
2. Server action menerima `base64: string`. Apa risiko keamanan kalau user upload file 50 MB (server action tidak ada batasan default)? Bagaimana cara client-side guardrail (cek `file.size` sebelum encode)?
3. UI sekarang single-file picker. Bagaimana cara extend ke multi-file upload (mis. user foto 3 struk sekaligus)? Apakah pattern `multiple` di `<input>` cukup, atau perlu re-design UX?
4. `FileReader.readAsDataURL` adalah async via callback. Kalau file besar (> 5 MB), encoding bisa lambat (1–2 detik). Bagaimana cara komunikasikan ke user bahwa "sedang encode" vs "sedang upload" vs "sedang parse di server" — apakah cukup `busy` boolean atau perlu progress state lebih granular?
5. Saat ini upload langsung trigger parsing. Bagaimana cara tambah **konfirmasi preview** sebelum kirim (mis. tampilkan thumbnail + tombol "Kirim untuk diproses" / "Batal") — kapan UX seperti itu masuk akal vs auto-process?

---

⬅️ Kembali: **[Section 1 — Vision API Basics](./latihan-1-vision-basics.md)** · 🏠 Index: **[Module 09 — Latihan](./latihan.md)** · ➡️ Lanjut: **[Section 3 — Receipt Extraction + Auto-Insert](./latihan-3-receipt-extraction.md)**
