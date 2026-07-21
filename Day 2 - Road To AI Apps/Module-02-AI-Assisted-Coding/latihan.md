# Module 02 — Latihan

> Modul ini memiliki **dua latihan** yang dirancang untuk mempraktikkan konsep dari `materi.md`:
>
> - **Latihan 1: Generate Dokumentasi Project** — workflow eksplorasi + pola iteratif + plan-then-execute.
> - **Latihan 2: Bangun Fitur CRUD Transactions** — workflow pengembangan fitur dengan prompt 3-komponen (Goal/Context/Guardrail).
>
> **Estimasi total**: 90–120 menit. Kedua latihan menghasilkan *artifact* nyata di project Fin-App Anda.

---

# Latihan 1 — Generate Dokumentasi Project Fin-App

> **Goal**: Mempraktikkan **workflow eksplorasi + dokumentasi** dengan Claude Code. Output akhirnya adalah sebuah file `docs/PROJECT.md` yang lengkap menjelaskan Fin-App — dibuat seluruhnya melalui prompt ke Claude.
>
> **Estimasi waktu**: 30–45 menit.

---

## Mengapa Latihan Ini?

Sebagai developer, Anda akan sering menghadapi dua situasi:

1. **Onboarding ke project asing** — perlu cepat paham apa yang sedang terjadi.
2. **Menjelaskan project kepada orang lain** — colleague baru, klien, atau diri Anda sendiri 6 bulan kemudian.

Dokumentasi yang baik menyelesaikan keduanya. Tetapi menulis dokumentasi dari nol itu memakan waktu. Inilah salah satu titik di mana AI assist sangat berguna: Claude Code dapat **membaca seluruh codebase**, lalu **menyusun dokumentasi terstruktur** dari pemahamannya — dalam waktu beberapa menit.

Latihan ini akan melatih:
- Workflow **Eksplorasi** (§4.1 di materi).
- Pola prompt **iteratif** (§3.4).
- Pola **Plan Then Execute** (§3.6) — kita minta Claude menyusun rencana dulu sebelum menulis.
- Kemampuan **review output AI** secara kritis.

---

## Prasyarat

Pastikan poin-poin berikut sudah siap:

- [ ] Module 01 selesai. Project Fin-App ter-clone di folder kerja Anda.
- [ ] `npm install` selesai tanpa error.
- [ ] Anda berada di folder project: `cd ~/Projek/fina-app` (atau wherever Anda meng-clone-nya).
- [ ] Folder `docs/` belum ada (atau kosong). Apabila sudah ada `docs/PROJECT.md`, pindahkan sementara — biar bisa membandingkan dengan hasil baru.

Buka terminal di folder project, jalankan:

```bash
claude
```

---

## Prompt 1 — Eksplorasi Awal (Plan Mode)

Sebelum Claude menulis apapun, kita ingin ia **memahami project** dulu dan **mengajukan rencana** struktur dokumentasi. Tujuannya: menghindari output asal-asalan, dan memberi Anda kesempatan mengoreksi arah.

**Salin prompt berikut, paste ke Claude Code:**

```
Saya ingin membuat file dokumentasi project di `docs/PROJECT.md`.
Sebelum menulis file, tolong:

1. Eksplorasi project ini dulu. Baca file-file kunci seperti
   package.json, src/app/layout.tsx, src/app/page.tsx, lalu
   skim folder src/ dan supabase/.
2. JANGAN tulis atau edit file apapun di tahap ini.
3. Berikan saya outline struktur `docs/PROJECT.md` yang akan
   Anda tulis — dalam bentuk daftar section + ringkasan 1
   kalimat per section.

Setelah saya setujui outline-nya, baru kita lanjut ke
penulisan file sebenarnya.
```

**Apa yang akan terjadi:**
- Claude akan memanggil tool `Read` beberapa kali untuk membaca file kunci.
- Setelah eksplorasi, ia akan kembali dengan outline berupa daftar section.

**Yang perlu Anda lakukan:**
1. **Baca outline-nya** — apakah masuk akal untuk Anda?
2. Outline-nya seharusnya mencakup setidaknya: Overview, Tech Stack, Struktur Folder, Database Schema, Data Flow, Development Workflow.
3. Apabila ada section yang menurut Anda **tidak perlu** atau **kurang**, beritahu Claude untuk koreksi.

> 💡 **Pengamatan**: amati bagaimana Claude menggunakan permission system. Pada Default mode, eksplorasi (Read) biasanya berjalan otomatis tanpa konfirmasi karena tidak destruktif.

---

## Prompt 2 — Setujui Outline & Tulis Section Awal

Setelah outline disetujui, kita minta Claude menulis **3 section pertama**: Overview, Tech Stack, Struktur Folder.

**Salin prompt berikut:**

```
Outline-nya bagus. Mulai tulis `docs/PROJECT.md` sekarang —
tetapi cukup section AWAL dulu, yaitu:

1. # Overview
   - 2 paragraf: tujuan project, target user, status iterasi.

2. ## Tech Stack
   - Tabel dengan kolom: Layer | Tool | Versi | Peran.
   - Layer yang dicakup: Framework, UI, Database, State Mgmt,
     Auth (kalau ada), AI (preview).
   - Versi diambil dari package.json — JANGAN dikira-kira.

3. ## Struktur Folder
   - Tree visual dari folder src/ dan supabase/.
   - Setiap folder/file utama diberi komentar 1 baris.

Setelah ketiga section ini selesai, berhenti — saya akan
review dulu sebelum lanjut section berikutnya.
```

**Apa yang akan terjadi:**
- Claude pakai tool `Write` untuk membuat file `docs/PROJECT.md`.
- Tergantung permission mode, Anda mungkin perlu confirm.

**Yang perlu Anda lakukan:**
1. Buka file `docs/PROJECT.md` di editor.
2. **Verifikasi versi** di tabel Tech Stack benar-benar sama dengan `package.json` (deteksi halusinasi — §7.3 di materi).
3. **Verifikasi tree folder** sesuai dengan kondisi nyata `src/` Anda.
4. Apabila ada yang salah, beri umpan balik ke Claude.

---

## Prompt 3 — Tulis Section Database Schema

Sekarang section yang lebih teknis. Anda akan minta Claude membaca migration SQL dan menjelaskannya dalam bentuk yang ramah developer.

**Salin prompt berikut:**

```
Lanjutkan ke section berikutnya di `docs/PROJECT.md`:

## Database Schema

Baca file:
- `supabase/migrations/0001_init.sql`
- `supabase/migrations/0002_match_transactions.sql`

Lalu dokumentasikan:

1. **Tabel `transactions`** — tabel kolom dalam bentuk markdown
   table: Kolom | Tipe | Nullable | Default | Keterangan.
2. **Extension yang dibutuhkan** — daftar singkat (pgcrypto,
   vector) + 1 baris alasan kenapa dipakai.
3. **Index** — daftar dan tujuannya.
4. **RLS Policy** — sebut nama policy dan implikasinya untuk
   keamanan (1 paragraf).
5. **Function `match_transactions`** — signature, input, output,
   dan use case singkat.

Tulis dengan asumsi pembacanya **developer baru** yang belum
familiar dengan pgvector. Berikan analogi singkat untuk
istilah teknis seperti "embedding" dan "HNSW".
```

**Apa yang akan terjadi:**
- Claude `Read` kedua file migration.
- Append ke `docs/PROJECT.md` dengan tool `Edit`.

**Yang perlu Anda lakukan:**
1. Verifikasi nama kolom & tipe data sesuai migration SQL.
2. Verifikasi analogi yang dipakai Claude **masuk akal** (contoh: "embedding seperti array koordinat di ruang makna").
3. Apabila analogi terlalu rumit / terlalu sederhana, minta Claude perbaiki.

---

## Prompt 4 — Tulis Section Data Flow + Diagram

Section ini menjelaskan **bagaimana data mengalir** dari user → UI → server action → Supabase → kembali ke UI. Ini paling berguna untuk onboarding orang baru.

**Salin prompt berikut:**

```
Lanjutkan ke section berikutnya di `docs/PROJECT.md`:

## Data Flow

Jelaskan alur data untuk **satu skenario konkret**: "user
membuka halaman dashboard dan melihat saldo".

Bentuk:

1. Narasi 1 paragraf yang menjelaskan alur urutan.
2. Diagram **mermaid sequence diagram** dengan participant:
   Browser, StatCards (Client Component), getBalanceSummary
   (Server Action), Supabase, dan TanStack Query Cache.
3. Catatan singkat tentang peran `proxy.ts` dan
   `@supabase/ssr` di alur ini.

Baca file `src/components/dashboard/stat-cards.tsx`,
`src/features/action.ts`, dan `src/lib/supabase/server.ts`
untuk memastikan diagramnya akurat.
```

**Apa yang akan terjadi:**
- Claude membaca 3 file tersebut.
- Tulis section dengan diagram mermaid (yang akan render otomatis di VS Code preview / GitHub).

**Yang perlu Anda lakukan:**
1. Buka preview Markdown di VS Code (`Cmd+Shift+V` atau `Ctrl+Shift+V`).
2. Lihat apakah diagram mermaid ter-render dengan benar.
3. Verifikasi urutan langkah di diagram cocok dengan kode sebenarnya.

---

## Prompt 5 — Tulis Section Development Workflow

Section ini berisi **perintah-perintah sehari-hari** dan konvensi project.

**Salin prompt berikut:**

```
Lanjutkan ke section berikutnya di `docs/PROJECT.md`:

## Development Workflow

Cakup:

1. **Quick start** — list perintah dari clone sampai dev server
   jalan (lihat README.md & package.json untuk script yang
   tersedia).
2. **Available npm scripts** — tabel: Script | Apa yang dia lakukan.
3. **Environment variables** — list dari `.env.example` dengan
   keterangan singkat tiap key.
4. **Git workflow** — branch `starter` untuk titik mulai
   workshop, branch `main` untuk perkembangan terbaru.
5. **Konvensi penamaan** — observe pattern di src/ (mis. apakah
   pakai kebab-case atau PascalCase untuk file) dan
   dokumentasikan.

Jangan bikin asumsi: kalau ragu, baca file-nya dulu.
```

**Apa yang akan terjadi:**
- Claude mengeksplorasi `package.json`, `.env.example`, dan struktur folder untuk menggali konvensi.

**Yang perlu Anda lakukan:**
1. Verifikasi script di tabel cocok dengan `package.json` Anda.
2. Apabila Claude membuat "konvensi" yang sebenarnya tidak konsisten di codebase, beritahu untuk koreksi.

---

## Prompt 6 — Polish & Final Review

Setelah semua section ada, minta Claude melakukan **review akhir**: konsistensi gaya, table of contents, dan ringkasan eksekutif.

**Salin prompt berikut:**

```
Sekarang lakukan polish final pada `docs/PROJECT.md`:

1. Tambahkan **Table of Contents** di bagian atas (setelah
   judul utama) — link ke setiap section.
2. Pastikan gaya bahasa konsisten — gunakan "Anda" (formal,
   friendly), bukan "kamu" atau "lo".
3. Pastikan semua tabel rapi (alignment kolom).
4. Tambahkan **catatan singkat di akhir** tentang status
   project: iterasi mana sekarang dan fitur apa saja yang
   masih belum diimplementasikan.
5. Apabila ada section yang **terlalu panjang** (>3 paragraf
   tanpa heading), pecah dengan sub-heading.
```

**Apa yang akan terjadi:**
- Claude akan melakukan beberapa edit pada file untuk merapikan.

**Yang perlu Anda lakukan:**
1. Buka file final `docs/PROJECT.md` di VS Code.
2. Scroll dari atas ke bawah — baca seperti pembaca baru.
3. **Apakah dokumen ini cukup** untuk onboard developer baru?
4. Apabila ada gap, tambahkan prompt iteratif untuk Claude memperbaikinya.

---

## Validasi Akhir

Setelah seluruh prompt di atas dijalankan, pastikan checklist berikut tercapai:

- [ ] File `docs/PROJECT.md` ada di repository Anda.
- [ ] Section **Overview, Tech Stack, Struktur Folder** lengkap dan akurat.
- [ ] Section **Database Schema** mencantumkan kolom yang sama dengan migration SQL.
- [ ] Section **Data Flow** memiliki diagram mermaid yang ter-render.
- [ ] Section **Development Workflow** mencantumkan script yang ada di `package.json`.
- [ ] **Table of Contents** lengkap dan link-nya berfungsi (klik di preview).
- [ ] Tidak ada **placeholder** seperti `TODO` atau `TBD` yang tertinggal.
- [ ] Anda telah **membaca seluruh dokumen sekali** dari atas ke bawah.

---

## Refleksi

Setelah selesai, tuliskan jawaban singkat (boleh di catatan pribadi atau di akhir `docs/PROJECT.md` sebagai komentar):

1. Berapa **iterasi prompt** yang Anda butuhkan sampai output-nya memuaskan?
2. Adakah momen di mana Claude membuat **halusinasi** (misalnya menyebut file yang tidak ada, atau salah versi)? Bagaimana Anda menanganinya?
3. Bandingkan: **kalau Anda menulis dokumentasi ini dari nol manual**, berapa lama estimasi Anda? Berapa lama dengan Claude?
4. Apabila harus melakukan ulang, **prompt mana yang akan Anda ubah**?
5. Adakah **prompt baru yang ingin Anda tambahkan** ke alur ini? (Misalnya: bagian troubleshooting, contributing guide, dll.)

---

## Bonus (Opsional) — Commit Dokumentasi

Apabila Anda merasa hasilnya cukup baik, **commit ke repository**:

```bash
git add docs/PROJECT.md
git commit -m "docs: add project documentation generated with Claude Code"
```

> 💡 **Catatan**: konvensi yang baik adalah menyebut tools yang dipakai dalam pesan commit ketika sebagian besar konten dibuat dengan AI. Ini transparansi yang bagus untuk team dan code reviewer.

---

Lanjutkan ke **Latihan 2** di bawah untuk membangun fitur CRUD lengkap menggunakan workflow pengembangan fitur. Dokumentasi yang baru Anda buat akan menjadi **peta jalan** ketika Claude perlu memahami struktur project.

---

# Latihan 2 — Bangun Fitur CRUD Transactions

> **Goal**: Membangun halaman `/transactions` yang lengkap dengan **list (limit), pagination, search, insert, update, delete** — semuanya melalui prompt iteratif ke Claude Code. Praktik nyata workflow **pengembangan fitur** (§4.2 di materi).
>
> **Estimasi waktu**: 60–75 menit.

---

## Apa yang Akan Anda Bangun?

Pada akhir latihan ini, halaman `/transactions` Anda akan memiliki:

```
┌─────────────────────────────────────────────────────────────────┐
│  Transactions                            [+ Add transaction]   │
│                                                                 │
│  [🔍 Cari deskripsi atau kategori...]   Show: [10 ▼]           │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ Tanggal │ Tipe    │ Kategori   │ Catatan   │ Jumlah  │⋮│    │
│  ├─────────────────────────────────────────────────────────┤    │
│  │ 11 Jun  │ Expense │ Food       │ Kopi pagi │ -Rp 35k │⋮│    │
│  │ ...                                                   │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│       ‹ Prev          Page 1 of 4          Next ›               │
└─────────────────────────────────────────────────────────────────┘
```

Enam fitur akan dibangun **secara bertahap**, satu prompt per fitur:

| # | Fitur | Server Action | Komponen UI |
|---|---|---|---|
| 1 | List dengan limit | `getTransactions({ limit })` | `<TransactionTable />` |
| 2 | Pagination | `getTransactions({ page, limit })` | `<PaginationControls />` |
| 3 | Search | `getTransactions({ search })` | `<SearchInput />` |
| 4 | Insert | `createTransaction(data)` | `<AddTransactionDialog />` |
| 5 | Update | `updateTransaction(id, data)` | `<EditTransactionDialog />` |
| 6 | Delete | `deleteTransaction(id)` | `<DeleteConfirmDialog />` |

> 💡 **Tip**: setelah setiap prompt, **buka browser di http://localhost:3000/transactions** dan verifikasi hasilnya berjalan sebelum lanjut ke prompt berikutnya. Pola ini menerapkan prinsip "validasi tiap iterasi" yang Anda pelajari di §3.4 materi.

---

## Prasyarat Latihan 2

- [ ] Latihan 1 selesai. File `docs/PROJECT.md` ada (akan dipakai Claude sebagai konteks).
- [ ] Halaman `/transactions` ada (dari setup awal — masih placeholder kosong).
- [ ] Tabel `transactions` di Supabase Anda berisi minimal **15 baris** data (kalau perlu, tambah lewat SQL Editor — pagination tidak akan terasa kalau cuma 6 baris).
- [ ] `npm install zod` (sudah ter-install atau perlu ditambah — Claude akan menambahkan jika belum ada).

---

## Prompt 1 — List dengan Limit

**Salin prompt berikut, paste ke Claude Code:**

```
Saya ingin membangun halaman /transactions menampilkan daftar
transaksi. Mulai dengan fitur list dasar dulu.

GOAL:
- Tambahkan server action getTransactions({ limit }) di
  src/features/action.ts.
- Buat komponen TransactionTable di
  src/components/transactions/transaction-table.tsx (client
  component, pakai useQuery).
- Update src/app/transactions/page.tsx untuk render
  TransactionTable.

CONTEXT:
- Pola server action mengikuti getBalanceSummary yang sudah ada.
- Pola useQuery mengikuti StatCards di dashboard.
- Tabel pakai komponen Shadcn Table (sudah ter-install).
- Format jumlah pakai formatIDR (sudah ada di src/lib/format.ts).
- Tipe income/expense pakai Badge berwarna (emerald/rose).

GUARDRAIL:
- Default limit = 10.
- Urutkan by date desc, lalu created_at desc.
- JANGAN ubah getBalanceSummary atau komponen dashboard lain.
- Tampilkan skeleton saat loading, pesan "Belum ada transaksi"
  saat data kosong.

Setelah selesai, jelaskan singkat apa saja yang Anda buat.
```

**Setelah Claude selesai, verifikasi:**

1. Buka **http://localhost:3000/transactions**.
2. Tabel menampilkan 10 baris transaksi.
3. Format jumlah benar (`Rp 130.000`, bukan `130000`).
4. Skeleton muncul saat refresh, lalu data hadir.

---

## Prompt 2 — Pagination

**Salin prompt berikut:**

```
Sekarang tambahkan pagination ke halaman /transactions.

GOAL:
- Update getTransactions agar menerima { page, limit }.
- Kembalikan { rows, totalCount } untuk hitung total halaman.
- Buat komponen PaginationControls dengan tombol Prev/Next dan
  info "Page X of Y".
- State page disimpan di src/app/transactions/page.tsx dengan
  useState.

CONTEXT:
- Pakai Supabase .range(from, to) — dokumentasinya:
  https://supabase.com/docs/reference/javascript/range
- Gunakan { count: "exact" } di .select().
- Komponen Button dari Shadcn untuk Prev/Next.

GUARDRAIL:
- Default limit tetap 10.
- Disable tombol Prev di halaman 1, Next di halaman terakhir.
- Query key TanStack Query: ["transactions", { page, limit }].
- JANGAN ubah komponen di luar yang disebut.
```

**Verifikasi:**

1. Tombol Next aktif → klik → data berganti, indikator "Page 2 of N".
2. Tombol Prev di Page 1 disabled.
3. Tombol Next di halaman terakhir disabled.

---

## Prompt 3 — Search

**Salin prompt berikut:**

```
Tambahkan fitur search ke halaman /transactions.

GOAL:
- Update getTransactions agar menerima { search?: string }.
- Search di kolom description DAN category (case-insensitive,
  partial match).
- Buat komponen SearchInput dengan debounce 300ms.
- State search di-pass ke query key.

CONTEXT:
- Supabase .or() untuk multi-column filter dengan ilike.
- Pola: `description.ilike.%query%,category.ilike.%query%`
- Pakai Input component dari Shadcn dengan icon Search dari
  lucide-react.

GUARDRAIL:
- Saat search berubah, reset page ke 1 (pakai useEffect).
- Trim whitespace dari input search.
- Apabila search kosong, tampilkan semua transaksi (tanpa
  filter).
- Debounce dengan setTimeout di useEffect — jangan instal
  package debounce baru.
```

**Verifikasi:**

1. Ketik di kotak search → tunggu 300ms → tabel terfilter.
2. Cari "kopi" — hanya transaksi yang mengandung "kopi" yang muncul.
3. Setelah search, kembali ke halaman 1 otomatis.
4. Hapus search → kembali ke seluruh data.

---

## Prompt 4 — Insert Transaction

**Salin prompt berikut:**

```
Tambahkan fitur Insert untuk transaksi baru.

GOAL:
- Buat Zod schema TransactionInput di src/features/schema.ts.
- Server action createTransaction(input) dengan validasi Zod.
- Komponen AddTransactionDialog (Shadcn Dialog) berisi form:
  type (Select income/expense), category (Input), amount
  (Input number), description (Input opsional), date (Input
  date, default today).
- Tombol "+ Add transaction" di header halaman /transactions
  membuka dialog.
- Setelah submit sukses: dialog tutup, toast sukses, tabel
  refresh otomatis.

CONTEXT:
- Pakai useMutation dari TanStack Query.
- onSuccess: invalidate query keys "transactions" dan
  "balance-summary" (supaya dashboard juga update).
- Toast pakai sonner (sudah ter-install).
- Form state cukup pakai useState per field (jangan tambah
  react-hook-form).

GUARDRAIL:
- Validasi: amount > 0, category wajib, date format YYYY-MM-DD.
- Apabila error dari server, tampilkan toast error dengan
  pesan dari error.message.
- Tombol Submit disabled saat mutation sedang pending.
- Reset form ke state awal setelah submit sukses.
```

**Verifikasi:**

1. Klik "+ Add transaction" → dialog terbuka.
2. Coba submit dengan amount 0 → error validasi muncul.
3. Submit dengan data valid → dialog tutup, toast sukses, data baru muncul di tabel.
4. Buka dashboard `/` → angka stat card ikut update.

---

## Prompt 5 — Update Transaction

**Salin prompt berikut:**

```
Tambahkan fitur Update transaksi.

GOAL:
- Server action updateTransaction(id, input) dengan validasi.
- Refactor: AddTransactionDialog jadi TransactionFormDialog
  yang menerima prop mode: "create" | "edit" dan initialValue
  opsional.
- Tambahkan kolom Actions di tabel dengan dropdown menu
  (Shadcn DropdownMenu) yang punya item "Edit".
- Klik Edit → buka dialog mode "edit" dengan field terisi
  data row tersebut.

CONTEXT:
- Operasi Supabase: .update(parsed).eq("id", id).
- Zod schema yang sama dipakai (transactionSchema).
- DropdownMenu sudah ter-install di project.

GUARDRAIL:
- Form harus pre-fill seluruh field dari initialValue saat
  mode "edit".
- Tombol submit menampilkan "Save" untuk edit, "Add" untuk
  create.
- Invalidate query keys yang sama (transactions, balance-summary).
- JANGAN duplikasi komponen form — refactor jadi satu komponen.
```

**Verifikasi:**

1. Klik ikon ⋮ di salah satu baris → menu muncul.
2. Klik Edit → dialog terbuka dengan data baris ter-isi.
3. Ubah amount → Save → tabel update, toast sukses.
4. Dashboard angka ikut menyesuaikan.

---

## Prompt 6 — Delete Transaction

**Salin prompt berikut:**

```
Tambahkan fitur Delete transaksi dengan konfirmasi.

GOAL:
- Server action deleteTransaction(id).
- Item "Delete" di DropdownMenu actions (warna merah untuk
  visual cue).
- Klik Delete membuka AlertDialog (Shadcn) untuk konfirmasi.
- Confirm hapus → eksekusi mutation → toast sukses → tabel
  refresh.

CONTEXT:
- Apabila AlertDialog belum ter-install, jalankan:
  npx shadcn@latest add alert-dialog
- Operasi Supabase: .delete().eq("id", id).
- Pesan konfirmasi: "Transaksi '<description>' akan dihapus
  permanen. Tindakan ini tidak dapat dibatalkan."

GUARDRAIL:
- JANGAN hapus tanpa konfirmasi.
- Tombol "Hapus" di AlertDialog pakai variant destructive
  (warna merah).
- Tombol "Batal" jelas posisinya, sebagai opsi default.
- Invalidate query keys: transactions, balance-summary.
```

**Verifikasi:**

1. Klik Delete pada salah satu baris → AlertDialog muncul.
2. Klik Batal → dialog tutup, data tidak berubah.
3. Klik Delete lagi → Hapus → toast sukses, baris hilang.
4. Cek di Supabase Table Editor — baris benar-benar hilang.

---

## Validasi Akhir Latihan 2

Pastikan checklist berikut tercapai:

- [ ] Halaman `/transactions` menampilkan tabel dengan 10 baris.
- [ ] Pagination (Prev/Next + indikator) berfungsi.
- [ ] Search dengan debounce 300ms berfungsi; reset page ke 1.
- [ ] Tombol "+ Add transaction" membuka dialog form yang berfungsi.
- [ ] Edit lewat dropdown menu membuka dialog dengan data ter-pre-fill.
- [ ] Delete lewat dropdown menu memunculkan konfirmasi dulu.
- [ ] Setelah Insert / Update / Delete, **dashboard `/` ikut update otomatis**.
- [ ] Form di-validasi sebelum submit (amount > 0, category wajib, dan sebagainya).
- [ ] Tidak ada error di console browser.

---

## Refleksi Latihan 2

Tuliskan pada catatan pribadi Anda:

1. **Berapa prompt** yang Anda gunakan untuk masing-masing fitur? (Idealnya: cukup 1 prompt sesuai latihan, tetapi seringkali perlu 2–3 iterasi untuk koreksi.)
2. **Iterasi terbanyak** ada di fitur mana? Mengapa menurut Anda lebih kompleks?
3. Apakah Claude pernah **menyalahi guardrail** yang Anda berikan? Bagaimana Anda menanganinya?
4. Apakah ada **bug halusinasi** yang Anda temui (misalnya import yang salah, nama function tidak ada)? Bagaimana Anda menemukannya?
5. Apakah **dokumentasi dari Latihan 1** membantu Claude memahami project ini? Bagaimana?

---

## Bonus (Opsional) — Commit & Push

Apabila hasilnya bagus, commit ke branch baru di repository lokal Anda:

```bash
git checkout -b feature/transactions-crud
git add src/
git commit -m "feat(transactions): add CRUD with pagination, search, and form validation

Built with Claude Code (Module 02 Latihan 2)."
```

> 💡 Branch terpisah memudahkan Anda membandingkan dengan starter branch (`git diff starter..feature/transactions-crud`) dan mengukur seberapa besar perubahan yang dilakukan dengan bantuan AI.

---

## Apa Selanjutnya?

Dengan halaman Transactions yang sudah lengkap, Anda sudah memiliki aplikasi tracker keuangan yang **fungsional**. Pada modul berikutnya, kita akan menambahkan **fitur AI**: embedding setiap transaksi dengan Gemini, semantic search natural language, dan chat interface untuk tanya jawab keuangan. Itulah jembatan dari "tracker biasa" menjadi "tracker dengan otak".
