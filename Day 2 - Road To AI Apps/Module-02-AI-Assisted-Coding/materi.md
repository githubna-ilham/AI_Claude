# Module 02 — AI-Assisted Coding dengan Claude Code

> **Tujuan modul**: Anda memahami **paradigma AI-assisted coding** secara konseptual, mengenali cara kerja Claude Code, dan memiliki kerangka berpikir untuk berkolaborasi dengannya secara efektif — bukan sekadar "menyuruh AI menulis kode".
>
> **Output akhir modul ini**: Anda dapat membedakan situasi mana yang ideal untuk AI assist, situasi mana yang sebaiknya dikerjakan manual, dan dapat menyusun prompt yang menghasilkan kode berkualitas.

---

## Apa yang Akan Anda Pelajari

Setelah menyelesaikan modul ini, Anda akan mampu:

1. Menjelaskan **evolusi AI-assisted coding** dari autocomplete hingga *AI pair programmer*, beserta implikasinya terhadap peran developer modern.
2. Memahami **anatomi Claude Code**: tools yang dimilikinya, mental model konteks, serta permission modes yang menentukan tingkat kewenangan Claude.
3. Menyusun **prompt yang efektif** untuk konteks coding — dengan pola yang dapat direplikasi, beserta anti-pattern yang harus dihindari.
4. Mengenali **empat pola workflow umum** untuk berkolaborasi dengan Claude Code: eksplorasi, pengembangan fitur, refactoring, dan debugging.
5. Mempraktikkan konsep tersebut melalui dua latihan: (a) generate dokumentasi project, dan (b) membangun fitur CRUD untuk halaman Transactions.
6. Memiliki preview tentang **fitur lanjutan** Claude Code (Skills, Hooks, Slash Commands, MCP) yang akan dibahas pada modul lanjutan.
7. Memahami **batasan etis dan teknis** AI-assisted coding: kapan harus menahan diri, bagaimana mereview output, dan tanggung jawab developer terhadap kode yang dihasilkan AI.

**Durasi belajar**: ±90 menit (santai) atau 60 menit (untuk yang sudah terbiasa dengan tools AI coding).

---

## 1. Apa itu AI-Assisted Coding?

### 1.1 Definisi Singkat

**AI-Assisted Coding** adalah pendekatan menulis software di mana sebuah model AI berperan sebagai *kolaborator aktif* — bukan sekadar autocomplete pasif, melainkan agen yang dapat memahami niat, membuat keputusan teknis, mengeksekusi perintah, dan memodifikasi kode berdasarkan instruksi natural language.

Istilah lain yang sering digunakan:
- **AI Pair Programming** — analogi dari *pair programming* tradisional (dua developer satu komputer), namun salah satunya adalah AI.
- **Vibe Coding** — istilah yang populer di komunitas akhir-akhir ini, merujuk pada gaya "coding sambil ngobrol" dengan AI.
- **Agentic Coding** — penekanan pada sisi *agent* (AI yang mengambil aksi multi-langkah secara mandiri).

Pada modul ini, istilah **AI-Assisted Coding** dipakai sebagai payung untuk seluruh konsep tersebut.

### 1.2 Evolusi dari Autocomplete ke Pair Programmer

Untuk memahami posisi AI-assisted coding hari ini, ada baiknya melihat perjalanannya secara historis.

```
Era 1 (1990–2010): IntelliSense / Autocomplete
   └─ Saran berbasis simbol & sintaks. Tidak ada "pemahaman".

Era 2 (2017–2021): Statistical autocompletion (Kite, TabNine)
   └─ Saran berbasis statistik pola kode. Masih per-baris.

Era 3 (2021–2023): LLM-based autocomplete (GitHub Copilot v1)
   └─ Saran berbasis context jendela kecil. Dapat menyarankan fungsi.

Era 4 (2023–2024): Chat-based assistant (ChatGPT, Copilot Chat)
   └─ Tanya jawab tentang kode. Manual copy-paste antara chat & editor.

Era 5 (2024–sekarang): Agentic coding (Claude Code, Cursor Composer, Aider)
   └─ AI dapat membaca filesystem, mengedit beberapa file, menjalankan
     perintah shell, dan melakukan tugas multi-langkah secara mandiri.
```

Setiap era menghadirkan pergeseran *bukan sekadar kemampuan*, melainkan **bagaimana developer mengonseptualisasikan pekerjaannya**:

| Era | Posisi Developer |
|---|---|
| Autocomplete | Penulis utama; AI menebak akhir kalimat |
| LLM autocomplete | Penulis utama; AI menyarankan blok |
| Chat assistant | Penulis utama; AI sebagai konsultan |
| **Agentic coding** | **Reviewer & arsitek**; AI sebagai eksekutor |

Pergeseran terakhir adalah yang paling signifikan, dan inilah fokus serius modul ini.

### 1.3 Pergeseran Peran Developer

Pada era *agentic coding*, peran Anda sebagai developer mengalami pergeseran nilai (bukan diminished — *berubah*):

**Yang berkurang nilainya:**
- Mengetik boilerplate yang berulang.
- Menghafal sintaks library secara detail.
- Menulis transformasi data sederhana.

**Yang meningkat nilainya:**
- **Memformulasikan masalah dengan jelas** — kemampuan mengubah "yang saya rasakan" menjadi "yang AI dapat eksekusi".
- **Mengevaluasi solusi** — apakah output Claude benar-benar memenuhi kebutuhan, aman, dan maintainable.
- **Memahami sistem secara holistik** — Claude pandai pada potongan, tetapi Anda harus tetap memahami arsitektur.
- **Membuat keputusan trade-off** — performance vs. simplicity, future-proofing vs. YAGNI, dan seterusnya.

> 💡 **Mental model yang berguna**: bayangkan Anda kini berperan seperti seorang **senior engineer yang mendampingi seorang junior yang cepat dan rajin**. Junior tersebut dapat menulis kode dengan sangat cepat, tetapi belum punya pengalaman untuk tahu kapan suatu pendekatan buruk dalam konteks Anda. Tugas Anda adalah memberi arah, mereview, dan menjaga konsistensi.

### 1.4 Apa yang Bukan AI-Assisted Coding?

Penting untuk membedakan AI-assisted coding dari beberapa hal yang sering dikira sama:

| AI-Assisted Coding | Bukan AI-Assisted Coding |
|---|---|
| Anda tetap kontrol arsitektur dan keputusan akhir | Menyerahkan seluruh keputusan ke AI ("kerjain semua, terserah") |
| Anda mereview, menguji, dan memvalidasi setiap output | Menerima output secara buta tanpa membaca |
| AI sebagai *partner*, bukan pengganti | Mengandalkan AI menggantikan pemahaman fundamental |
| Tools dipilih sesuai konteks (chat, autocomplete, agent) | Memaksa satu tool untuk semua skenario |

---

## 2. Anatomi Claude Code

Setelah memahami konsep besar, mari masuk ke alat yang akan Anda gunakan: **Claude Code**. Bagian ini mengupas cara kerjanya — bukan sekadar "command apa untuk apa", melainkan *mental model* yang akan membantu Anda memprediksi perilakunya.

### 2.1 Apa yang Claude "Lihat" dan "Tidak Lihat"

Pemahaman pertama yang paling penting: **Claude Code TIDAK punya akses otomatis ke seluruh codebase**. Konteks yang ia "lihat" terbangun secara bertahap melalui tools.

Saat Anda menjalankan `claude` di folder project:

✅ **Yang Claude tahu otomatis:**
- Working directory (folder tempat Anda menjalankan `claude`).
- Sistem operasi & versi (macOS, Linux, Windows).
- Tanggal & waktu saat ini.
- File `CLAUDE.md`, `AGENTS.md` (di working directory) — sebagai instruksi tambahan.

❌ **Yang Claude TIDAK tahu sampai diberi tahu atau memintanya:**
- Isi file apapun (perlu memanggil tool *Read*).
- Struktur folder dalam (perlu *Bash* `ls` atau tool eksplorasi).
- Riwayat git (perlu *Bash* `git log`).
- Apa yang berjalan di terminal lain Anda.
- Apa yang Anda lihat di browser.

> 💡 Implikasi: apabila Anda bilang "fix bug di file `page.tsx`", Claude akan **pertama-tama membaca file tersebut**. Setiap eksplorasi punya cost (token + waktu). Memberi context yang tepat di prompt dapat mempercepat pekerjaan.

### 2.2 Tools yang Dimiliki Claude Code

Claude Code memiliki sekitar 15+ *tools* (di luar yang Anda tambahkan via MCP atau Skills custom). Yang utama:

| Tool | Fungsi | Kapan dipakai |
|---|---|---|
| **Read** | Membaca isi file | Selalu, untuk memahami kode |
| **Edit** | Modifikasi file (string replacement) | Untuk perubahan presisi |
| **Write** | Tulis file baru / overwrite total | Bikin file baru, atau rewrite besar |
| **Bash** | Jalankan perintah shell | `npm install`, `git`, `mkdir`, dan sebagainya |
| **Grep** | Cari teks dalam files | Mencari simbol, pattern, error |
| **Glob** | Cari file by pattern | Mencari semua `.tsx`, dan sebagainya |
| **WebFetch** | Ambil konten URL spesifik | Baca dokumentasi online yang URL-nya sudah diketahui |
| **WebSearch** | Cari di internet | Cari solusi error, package terbaru |
| **TaskCreate / TaskUpdate** | Kelola task list internal | Multi-step plan |
| **Agent** | Spawn sub-agent untuk task isolated | Riset luas / kerja paralel |

Setiap kali Claude menggunakan sebuah tool, di terminal Anda akan terlihat output ringkasnya. **Inilah yang membuat AI agentic transparan**: Anda dapat menyaksikan apa yang ia kerjakan, langkah demi langkah.

### 2.3 Permission Modes

Salah satu fitur paling penting Claude Code adalah **permission system**. Tujuannya: Anda mengontrol seberapa "bebas" Claude dapat bertindak.

| Mode | Perilaku | Cocok untuk |
|---|---|---|
| **Default** | Setiap aksi yang berdampak (Edit, Write, Bash) butuh persetujuan Anda | Pemula, atau task sensitif |
| **Accept Edits** | Edit & Write otomatis disetujui; Bash tetap konfirmasi | Pekerjaan di branch sendiri, banyak edit kecil |
| **Bypass Permissions** (YOLO) | Seluruh tool berjalan tanpa konfirmasi | Hanya untuk eksperimen di sandbox |
| **Plan Mode** | Claude hanya boleh baca + plan, tidak boleh modifikasi apapun | Saat Anda ingin diskusi rencana dulu |

Anda dapat mengganti mode kapan saja:
- Selama sesi: tekan `Shift+Tab` untuk siklus mode.
- Atau melalui *slash command*: `/permissions`.

> ⚠️ **Penting**: jangan menjalankan **Bypass Permissions** pada project produksi atau di mesin tanpa backup. Mode ini ada untuk skenario *throwaway* — bukan untuk kerja sehari-hari.

### 2.4 Conversation Memory & Compaction

Claude Code menjaga seluruh percakapan Anda dalam satu sesi sebagai *context window*. Beberapa hal yang perlu diketahui:

- **Context window terbatas** (saat ini bisa mencapai 1 juta token untuk model Opus, tetapi tidak tak hingga).
- Ketika hampir penuh, sistem akan **memadatkan** (compact) bagian awal percakapan secara otomatis.
- Hasilnya: percakapan lama disimpan dalam bentuk ringkasan, bukan verbatim.

**Implikasi praktis:**
- Anda dapat bekerja dalam sesi panjang tanpa khawatir "lupa" hal di awal.
- Tetapi setelah compaction, *detail spesifik* dari awal sesi mungkin sudah tidak akurat. Apabila Anda butuh detail awal, sebaiknya simpan di file (bukan di percakapan).
- Memulai sesi baru kadang lebih baik daripada melanjutkan sesi yang sudah sangat panjang dengan banyak topik berbeda.

### 2.5 File `CLAUDE.md` dan `AGENTS.md`

Kedua file ini berperan sebagai **instruksi persisten** yang otomatis terbaca Claude di setiap sesi.

Pada project Fin-App Anda akan menemui:
- `CLAUDE.md` di root — biasanya berisi `@AGENTS.md` (referensi).
- `AGENTS.md` — berisi peringatan tentang Next.js 16 yang punya breaking changes.

> 💡 Apabila ada konvensi spesifik project Anda (misalnya "selalu pakai TypeScript strict", "jangan modifikasi folder `/dist`"), tambahkan ke `CLAUDE.md` agar Claude konsisten mengikutinya tanpa perlu diingatkan setiap kali.

---

## 3. Prompting Efektif untuk Coding

Beralih ke aspek praktis: **bagaimana Anda berbicara dengan Claude Code** agar hasilnya optimal? Bagian ini membahas pola yang terbukti efektif dan beberapa anti-pattern yang sering dijumpai.

### 3.1 Tiga Komponen Prompt yang Baik

Prompt coding yang efektif umumnya memiliki tiga komponen:

```
[GOAL]     Apa yang ingin Anda capai (outcome, bukan langkah)
[CONTEXT]  Informasi yang Claude butuh tahu (lokasi, constraint, preferensi)
[GUARDRAIL] Batasan yang harus dihormati (jangan ubah file X, ikuti pola Y)
```

**Contoh kurang efektif:**

> "Tambah dark mode."

**Contoh efektif:**

> "Tambahkan dark mode toggle di header (`src/app/layout.tsx`).
> Gunakan token Tailwind yang sudah ada (`bg-background`, `text-foreground`).
> Simpan preferensi di `localStorage`.
> **Jangan** instal package baru — pakai built-in saja."

Versi kedua memberi Claude **gambaran yang sama** dengan apa yang Anda bayangkan, sehingga output-nya jauh lebih dekat dengan ekspektasi.

### 3.2 Prinsip "One Concept Per Prompt"

Salah satu pola yang sering gagal adalah menumpuk banyak permintaan dalam satu pesan:

> ❌ "Tambah dark mode, ubah font jadi Inter, perbaiki bug di tabel, dan tambahkan halaman about."

Empat permintaan ini punya konteks berbeda, prioritas berbeda, dan kemungkinan butuh diskusi berbeda. Claude akan mencoba mengerjakan semua, tetapi hasilnya cenderung dangkal.

**Pola yang lebih baik**: pecah jadi prompt terpisah, tunggu satu selesai dan direview, baru lanjut ke berikutnya.

### 3.3 Pola "Show, Don't Tell"

Apabila Anda punya **contoh konkret** dari output yang diinginkan, berikan langsung daripada mendeskripsikannya.

❌ Kurang efektif:
> "Buat fungsi yang format mata uang dengan titik sebagai pemisah ribuan."

✅ Lebih efektif:
> "Buat fungsi `formatIDR(value)` yang mengubah `5000000` menjadi `'Rp 5.000.000'`. Tangani juga `0` → `'Rp 0'` dan `1500` → `'Rp 1.500'`."

Contoh konkret menghilangkan ambiguitas.

### 3.4 Pola "Iteratif, Bukan Sekali Tembak"

Pemula sering mencoba menulis satu prompt panjang berisi spesifikasi lengkap, berharap mendapat output sempurna. Pendekatan ini jarang berhasil dan menghabiskan token.

**Pendekatan iteratif** justru lebih produktif:

```
Iterasi 1: "Bantu saya pahami struktur src/features/ ini."
Iterasi 2: "OK. Sekarang tambahkan action getMonthlyExpenseByCategory."
Iterasi 3: "Tambahkan loading state dan error handling di komponennya."
Iterasi 4: "Refactor: pindahkan logic agregasi ke sql, bukan js."
```

Setiap iterasi Claude mendapat *konteks tambahan* dari yang sebelumnya, dan Anda dapat mengoreksi arah pelan-pelan.

### 3.5 Anti-Pattern yang Harus Dihindari

| Anti-Pattern | Mengapa Bermasalah | Yang Sebaiknya Dilakukan |
|---|---|---|
| Prompt terlalu vague ("perbaiki bug-nya") | Claude tidak tahu bug mana | Jelaskan gejala, error message, file relevan |
| Prompt terlalu micro-managing ("ganti baris 23 dari X jadi Y") | Anda lebih cepat lakukan sendiri | Pakai kalau memang perlu presisi tinggi; gunakan Edit langsung |
| Menerima output tanpa membaca | Bug halusinasi sering luput | Selalu baca diff, jalankan test, validasi |
| Lanjutkan sesi yang sudah berantakan | Konteks kotor menurunkan kualitas | Mulai sesi baru dengan ringkasan kondisi terkini |
| Tidak memberitahu kendala | Output akan melanggar konvensi project | Sebut di awal: "kami pakai TanStack Query bukan SWR" |
| Bypass permission untuk semua | Risiko aksi tidak diinginkan | Mode default cukup nyaman untuk kebanyakan kasus |

### 3.6 Pola "Plan Then Execute"

Untuk task yang besar atau berisiko, ada pola yang sangat berguna:

1. **Plan mode** (atau prompt eksplisit): "Tolong jelaskan rencana langkah-langkahnya **tanpa mengubah file apapun**. Saya akan review dulu."
2. Claude memberi outline.
3. Anda review, mengoreksi, atau menyetujui.
4. Beri lampu hijau: "OK, lanjutkan implementasi rencana di atas."

Pola ini menghemat waktu jauh lebih banyak dibanding harus me-rollback perubahan yang ternyata salah arah.

---

## 4. Empat Workflow Umum

Bagian ini memberi gambaran ringkas empat skenario yang akan Anda hadapi berulang kali. Bukan resep kaku — anggap saja sebagai *kerangka berpikir*.

### 4.1 Workflow Eksplorasi (Memahami Codebase Asing)

**Situasi**: Anda baru kenal codebase, perlu paham arsitektur sebelum mengubah apapun.

**Pendekatan**:
1. "Berikan ringkasan struktur folder project ini dalam 5 kalimat."
2. "File mana yang merupakan entry point?"
3. "Bagaimana data mengalir dari user input ke database?"
4. "Apakah ada konvensi penamaan yang konsisten di codebase ini?"

**Hindari**: langsung minta perubahan sebelum memahami konteks. Output yang baik bermula dari pemahaman yang baik.

### 4.2 Workflow Pengembangan Fitur (Add Feature)

**Situasi**: Anda ingin menambah fitur baru.

**Pendekatan**:
1. **Diskusi requirement**: "Saya ingin fitur X. Apa pertimbangan teknis yang perlu dipikirkan dulu?"
2. **Plan**: "Buat outline langkah implementasinya."
3. **Eksekusi bertahap**: minta Claude mengerjakan satu langkah, review, lalu lanjut.
4. **Validasi**: "Apakah ini berdampak ke X / Y / Z?"

### 4.3 Workflow Refactoring

**Situasi**: Kode bekerja, tetapi struktur perlu dirapikan.

**Pendekatan**:
1. **Definisikan tujuan refactor**: "Saya ingin pisahkan logic data dari komponen UI."
2. **Pastikan ada test atau cara verifikasi** — refactor tanpa safety net berbahaya.
3. **Refactor bertahap**: satu modul / file / fungsi per iterasi.
4. **Verifikasi setelah setiap langkah**: jalankan build/test, pastikan tidak breaking.

### 4.4 Workflow Debugging

**Situasi**: Ada error / behavior tidak sesuai harapan.

**Pendekatan**:
1. **Beri Claude info lengkap**: error message, file, langkah reproduksi.
2. **Jangan langsung minta "fix"** — minta diagnosis dulu: "Apa kemungkinan penyebab?"
3. **Verifikasi hipotesis**: minta Claude tambahkan log atau cek state.
4. **Setelah penyebab jelas**, baru minta solusi.

> 💡 Apabila Anda sudah familiar dengan teknik **systematic debugging**, pola itu tetap berlaku — Claude Code adalah tool, bukan jalan pintas untuk menghindari berpikir.

---

## 5. Praktik di `latihan.md`

Konsep di atas akan Anda praktikkan langsung melalui dua latihan terstruktur di `latihan.md` folder ini:

| Latihan | Apa yang Anda kerjakan | Workflow yang dilatih |
|---|---|---|
| **Latihan 1: Generate Dokumentasi** | Buat file `docs/PROJECT.md` lewat 6 prompt iteratif | Eksplorasi (§4.1) + Iteratif (§3.4) + Plan Then Execute (§3.6) |
| **Latihan 2: Bangun Fitur CRUD Transactions** | Halaman `/transactions` lengkap dengan list, pagination, search, insert, update, delete | Pengembangan Fitur (§4.2) + Prompt 3-komponen (§3.1) |

Kedua latihan menghasilkan **artifact nyata** di project Anda — bukan latihan akademis.

---

## 6. Preview Fitur Lanjutan

Claude Code memiliki banyak fitur lanjutan yang tidak dibahas penuh di Module 02. Berikut preview agar Anda memahami arah eksplorasi selanjutnya.

| Fitur | Singkatnya |
|---|---|
| **Slash Commands** | Pintasan instruksi (`/clear`, `/help`, `/permissions`, `/exit`). Anda juga dapat membuat custom slash command. |
| **Skills** | "Plugin" konseptual: file Markdown yang mengajari Claude pola kerja tertentu (misalnya "writing-plans", "debugging"). |
| **Hooks** | Skrip yang dijalankan otomatis pada event (pre-tool, post-edit, dan sebagainya). Berguna untuk linting otomatis, audit, dan lain-lain. |
| **MCP (Model Context Protocol)** | Cara menyambungkan Claude ke layanan eksternal: Slack, Linear, Atlassian, custom server. |
| **Sub-Agents** | Spawn agent khusus (misalnya `Explore`, `Plan`) untuk task isolated. |
| **Background Tasks** | Jalankan command panjang di background, dapat notifikasi saat selesai. |

Pada Module 02 ini fokusnya adalah **fundamental** — pemahaman yang kuat di sini akan membuat eksplorasi fitur lanjutan jauh lebih mudah.

---

## 7. Etika dan Batasan AI-Assisted Coding

Bagian terakhir ini — kerap diabaikan namun penting — membahas **kapan sebaiknya Anda TIDAK pakai AI assist**, bagaimana Anda tetap bertanggung jawab atas kode yang dihasilkan, dan risiko apa yang harus diwaspadai.

### 7.1 Kapan Sebaiknya TIDAK Pakai AI Assist

Tidak semua situasi cocok untuk AI assist. Beberapa di antaranya:

| Situasi | Alasan |
|---|---|
| **Logic bisnis kritis yang Anda belum pahami** | Anda perlu menderita sedikit untuk benar-benar paham; AI mempercepat output tanpa memperdalam pemahaman |
| **Code review atas kerja orang lain** | Tugas review menuntut judgment manusia; AI dapat membantu *spot*, tetapi tidak boleh menggantikan reviewer |
| **Security-sensitive code** (auth, kriptografi, payment) | AI dapat menghasilkan kode yang *terlihat* benar tetapi punya kerentanan halus |
| **Hal yang akan langsung di-deploy ke production tanpa review** | Selalu ada tahap review; AI tidak menggantikan code review |
| **Saat Anda lelah dan tidak fokus** | Anda perlu *bisa membaca dan menilai* output — apabila terlalu lelah untuk itu, sebaiknya berhenti |

### 7.2 Tanggung Jawab Tetap di Tangan Anda

Hal ini mungkin terdengar seperti formalitas, tetapi penting untuk ditegaskan:

> **Kode yang masuk ke project Anda adalah tanggung jawab Anda — bukan AI, bukan vendor AI.**

Itu artinya:
- Apabila ada bug, **Anda** yang memperbaikinya.
- Apabila ada security incident, **Anda** yang akuntabel.
- Apabila ada licensing issue, **Anda** yang memikul konsekuensinya.

AI assist mempercepat output, tetapi tidak memindahkan tanggung jawab. Pendekatan yang sehat: **review setiap perubahan seperti Anda akan menjelaskan ke manajer mengapa baris ini ada di sini**.

### 7.3 Risiko Halusinasi dan Cara Menghadapinya

**Halusinasi** dalam coding context berarti: Claude memanggil fungsi yang tidak ada, menggunakan API yang sudah deprecated, atau mengimpor package fiktif.

Mitigasi yang efektif:

1. **Jalankan kode** — apabila halusinasi, biasanya langsung error.
2. **Periksa import** — apabila Claude mengimpor sesuatu yang Anda tidak kenal, cari dulu apakah package itu ada.
3. **Gunakan tipe ketat** (TypeScript strict) — type-checker akan menangkap banyak halusinasi.
4. **Hindari API yang sangat baru** atau sangat niche — Claude lebih sering halusinasi di area ini karena training data terbatas.
5. **Selalu baca dokumentasi resmi** ketika ragu — jangan andalkan ingatan Claude.

### 7.4 Risiko Over-Reliance & Kehilangan Pemahaman

Risiko jangka panjang yang sering tidak disadari: **terlalu sering pakai AI assist dapat mengikis pemahaman fundamental Anda**.

Tanda-tanda peringatan:
- Anda lupa cara menulis loop sederhana tanpa Claude.
- Anda tidak dapat menjelaskan kode Anda sendiri saat ditanya.
- Anda kesulitan debug ketika Claude tidak tersedia.

Mitigasi:
- **Sesekali coding tanpa AI** — pertahankan otot dasar.
- **Pahami output Claude** — jangan asal terima.
- **Belajar konsep secara mandiri** — baca dokumentasi, ikuti kursus, dan sebagainya.

> 💡 Anggap AI assist seperti kalkulator: tools yang sangat berguna, tetapi Anda tetap perlu paham matematika dasar untuk tahu kapan jawabannya masuk akal.

### 7.5 Privasi dan Data Sensitif

Saat Anda menggunakan Claude Code, **isi file yang Claude baca berpotensi dikirim ke server Anthropic** sebagai bagian dari context. Beberapa pertimbangan:

- **Jangan paste kredensial** ke prompt (API key, password, dan sebagainya).
- **Hati-hati dengan data customer / PII** — apabila Anda bekerja di domain regulated, konsultasikan dulu kebijakan privasi tim Anda.
- **Periksa kebijakan Anthropic** terkait data retention dan training data — kebijakan dapat berubah; periksa dokumentasi terbaru di [anthropic.com/legal](https://anthropic.com/legal).

---

## Recap & Langkah Selanjutnya

Pada modul ini Anda telah:

1. Memahami evolusi AI-assisted coding dari era autocomplete hingga era *agentic coding*.
2. Mengenali **mental model Claude Code**: tools yang dimilikinya, apa yang ia "lihat", dan permission modes yang menjaga kontrol di tangan Anda.
3. Mempelajari pola **prompting yang efektif** beserta anti-pattern yang sering dijumpai.
4. Mengenali empat workflow umum: eksplorasi, fitur, refactor, debug.
5. Mendapat preview tentang fitur lanjutan Claude Code yang akan dibahas di modul-modul setelahnya.
6. Memahami sisi etika & batasan AI-assisted coding — agar pendekatan Anda *responsible*, bukan asal cepat.

Lanjutkan ke **`latihan.md`** di folder ini untuk **dua latihan praktis**: (1) generate dokumentasi `docs/PROJECT.md`, dan (2) membangun fitur CRUD halaman Transactions.

📂 Lihat: `latihan.md`
