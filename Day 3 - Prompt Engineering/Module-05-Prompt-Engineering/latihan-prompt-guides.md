# Section 3 — Prompt Guides

> Bagian dari **[Module 05 — Latihan](./latihan.md)**. Lanjutan dari **[Section 2 — Sample Parameter & Output Control](./latihan-output-control.md)**.

> Latihan untuk merefactor system prompt AI Advisor sesuai best practice. Tiga prompt siap copy-paste.
>
> **Estimasi**: 30–40 menit.

## Prasyarat Section 3

- [ ] Section 1 + 2 selesai.

---

## Prompt 1 — Audit System Prompt yang Ada

**Salin prompt berikut:**

```
Saya ingin Anda mengaudit ADVISOR_SYSTEM di
src/features/prompts.ts.

GOAL:
- Baca isi ADVISOR_SYSTEM.
- Lakukan audit menggunakan 7 prinsip prompt yang baik:
  1. Spesifik vs abstrak
  2. Eksplisit vs implisit
  3. Ada contoh konkret?
  4. Larangan eksplisit
  5. Strukturkan dengan heading/list?
  6. Persona dipisah dari instruksi tugas?
  7. Apakah ada anti-pattern?

- Berikan output dalam bentuk:
  - Tabel: prinsip | nilai (✅/⚠️/❌) | catatan
  - Daftar perbaikan yang disarankan, prioritas tinggi ke
    rendah.

CONTEXT:
- File: src/features/prompts.ts.
- JANGAN modifikasi prompt-nya dulu — hanya audit di tahap
  ini.

GUARDRAIL:
- Audit harus jujur, jangan basa-basi.
- Berikan saran yang konkret (mis. "tambah contoh X di
  bagian Y"), bukan abstrak.
```

**Verifikasi:**

1. Claude menampilkan tabel audit dengan minimal 1 ⚠️ atau ❌.
2. Daftar perbaikan ada minimum 3 items.

---

## Prompt 2 — Iterasi Perbaikan Prompt

**Salin prompt berikut:**

```
Berdasarkan audit di Prompt 1, perbaiki ADVISOR_SYSTEM.

GOAL:
- Refactor src/features/prompts.ts.
- Terapkan 3-5 perbaikan prioritas tinggi dari audit
  sebelumnya.
- Pertahankan ekspor ADVISOR_SYSTEM (jangan rename).

CONTEXT:
- Hasil refactor harus mengikuti 7 prinsip:
  - Heading markdown jelas (## Persona, ## Lingkup, dst.)
  - Konkret, bukan abstrak
  - Larangan eksplisit dengan "JANGAN/HINDARI"
  - Format yang dapat dideteksi mata (Rupiah, %, dst dengan
    contoh)

GUARDRAIL:
- Setelah refactor, jalankan test cases manual berikut:
  1. "Halo, siapa kamu?" → respons identitas yang jelas.
  2. "Tips menabung untuk pemula?" → markdown rapi + list.
  3. "Berapa harga saham GOTO besok?" → menolak sopan +
     redirect.
  4. "Ringkasan pengeluaran saya bulan ini." → mengakui ia
     belum punya data (akan ditangani di Section 6).
  
- Apabila ada test gagal, iterasi lagi prompt-nya.
```

**Verifikasi:**

1. Run semua 4 test cases di chatbot.
2. Catat: berapa banyak yang langsung lolos, berapa yang butuh iterasi prompt tambahan.

---

## Prompt 3 — Versi Prompt dan A/B Test Manual

**Salin prompt berikut:**

```
Saya ingin mempertahankan versi lama untuk perbandingan
manual.

GOAL:
- Di src/features/prompts.ts, ekspor 2 versi:
  - ADVISOR_SYSTEM_V1 (versi dari Section 1)
  - ADVISOR_SYSTEM_V2 (versi yang baru di-refactor)
- ADVISOR_SYSTEM tetap diekspor sebagai alias ke V2 (yang
  aktif dipakai).
- Tambahkan komentar JSDoc di atas masing-masing yang
  menjelaskan kapan dipakai.

CONTEXT:
- File: prompts.ts.
- V1 berguna untuk perbandingan dan rollback cepat.

GUARDRAIL:
- JANGAN ubah route.ts atau parse-transaction.ts —
  ADVISOR_SYSTEM (alias V2) yang dipakai di sana.
- Versi V1 hanya untuk perbandingan, tidak dipakai
  production.
```

**Verifikasi:**

1. File prompts.ts memiliki V1, V2, dan alias.
2. Aplikasi tetap pakai V2 (yang refactor).
3. Anda dapat sewaktu-waktu switch ke V1 untuk perbandingan dengan ganti `ADVISOR_SYSTEM = ADVISOR_SYSTEM_V1`.

---

## Validasi Akhir Section 3

- [ ] System prompt sudah di-audit dan di-refactor.
- [ ] V1 dan V2 keduanya ada di file.
- [ ] Test cases lolos dengan V2.
- [ ] Tidak ada regresi.

## Refleksi Section 3

1. Anti-pattern mana yang ternyata ada di V1?
2. Apakah V2 menghasilkan respons yang **berbeda kualitas** dari V1?
3. Apakah V2 lebih ringkas atau lebih panjang dari V1?

---

⬅️ Kembali: **[Section 2](./latihan-output-control.md)** · ➡️ Lanjut: **[Section 4 — Zero-shot & Few-shot](./latihan-few-shot.md)**
