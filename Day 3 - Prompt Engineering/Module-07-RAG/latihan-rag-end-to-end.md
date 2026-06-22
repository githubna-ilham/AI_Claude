# Section 2 — RAG End-to-End: Integrasi ke AI Advisor

> Bagian dari **[Module 07 — Latihan](./latihan.md)**. Lanjutan dari **[Section 1 — Pencarian Semantik](./latihan-pencarian-semantik.md)**.

> Latihan untuk **menghubungkan `searchKnowledge` (Section 1)** ke route handler `/api/advisor` dan AI Advisor UI yang sudah dibangun di Module 05. Empat prompt siap copy-paste — pada akhirnya, AI Advisor menjawab berdasarkan FAQ ter-embed dan menampilkan sumber kutipan.
>
> **Estimasi**: 70–90 menit.

## Prasyarat Section 2

- [ ] Section 1 selesai. `searchKnowledge()` jalan dengan baik.
- [ ] Module 05 selesai. AI Advisor `/api/advisor` + `AIChatPanel` jalan.
- [ ] File `src/lib/prompts.ts` (dari Module 05 Section 1) sudah ada — berisi system instruction lama.
- [ ] Anda sudah membaca bagian Section 2 di `materi.md`.

---

## Prompt 1 — Modify System Prompt jadi RAG-aware

**Salin prompt berikut, paste ke Claude Code:**

```
Sekarang siapkan builder system prompt yang menyisipkan
konteks hasil retrieval ke dalam persona AI Advisor.

GOAL:
- Buka src/lib/prompts.ts (dari Module 05).
- TAMBAHKAN (jangan hapus yang lama) export function:
  
  import type { KnowledgeChunk } from "@/features/knowledge";
  
  export function buildAdvisorSystemPrompt(
    retrievedChunks: KnowledgeChunk[]
  ): string

- Struktur output string:
  
  1. Persona dasar AI Advisor (gunakan teks system
     instruction yang sudah ada di prompts.ts — copy
     atau referensikan konstanta lama).
  2. Instruksi penggunaan konteks (paragraf):
     "Anda diberi konteks pengetahuan berikut yang relevan
      dengan pertanyaan user. JIKA konteks tidak cukup
      untuk menjawab, katakan terus terang — JANGAN
      mengarang."
  3. Block KONTEKS:
     === KONTEKS ===
     [1] {chunk 1 content}
     [2] {chunk 2 content}
     ...
     === AKHIR KONTEKS ===
  4. Kalimat penutup:
     "Pertanyaan user akan datang sebagai message
      berikutnya. Apabila Anda menggunakan informasi dari
      konteks, sebutkan nomor referensi [n] di jawaban
      agar dapat dilacak."

- Apabila retrievedChunks kosong, GANTI block KONTEKS
  dengan:
  
  === KONTEKS ===
  (Tidak ada konteks yang relevan ditemukan untuk
  pertanyaan ini.)
  === AKHIR KONTEKS ===

CONTEXT:
- Function ini akan dipanggil di route handler di Prompt 2.
- Persona dasar tidak boleh berubah — kita hanya
  menyisipkan KONTEKS block.

GUARDRAIL:
- JANGAN hapus konstanta system instruction lama yang
  sudah ada di prompts.ts.
- JANGAN tambah dependency apa pun.
- Function harus deterministik — input sama → output sama.
```

**Verifikasi:**

1. `src/lib/prompts.ts` punya export `buildAdvisorSystemPrompt`.
2. Konstanta system instruction lama masih ada (untuk backward compat / referensi).
3. Output function untuk `retrievedChunks = []` mengandung kalimat "(Tidak ada konteks ...)".
4. `npx tsc --noEmit` clean.

---

## Prompt 2 — Modify Route Handler `/api/advisor`

**Salin prompt berikut, paste ke Claude Code:**

```
Sekarang hubungkan searchKnowledge + buildAdvisorSystemPrompt
ke route handler /api/advisor.

GOAL:
- Buka file route handler AI Advisor (kemungkinan
  src/app/api/advisor/route.ts dari Module 05).
- Di handler POST, SEBELUM memanggil client.messages.stream:
  
  1. Ekstrak latest user message dari array messages.
  2. Panggil searchKnowledge(latestUserMessage, 5, 0.5).
  3. Panggil buildAdvisorSystemPrompt(retrievedChunks)
     untuk dapat system string baru.
  4. Pass system string baru ini ke client.messages.stream
     sebagai parameter `system` (override system lama).

- LOG di server (console.log) untuk debug:
  
  console.log("[RAG] query:", latestUserMessage);
  console.log("[RAG] retrieved:", retrievedChunks.map(
    c => ({ id: c.id, distance: c.distance })
  ));

- Pass retrievedChunks ke response stream agar UI bisa
  tampilkan citation. Pilih SALAH SATU pendekatan:
  
  Opsi A (paling sederhana): kirim header HTTP custom
  `x-rag-sources` berisi JSON.stringify dari
  retrievedChunks (hanya id + content snippet pertama
  100 char + metadata).
  
  Opsi B: wrap response sebagai JSON {sources, stream} —
  butuh refactor lebih besar.
  
  REKOMENDASI: pakai Opsi A untuk MVP. Catat trade-off di
  comment singkat di kode.

CONTEXT:
- Streaming dari Claude tetap dipertahankan — RAG hanya
  menambah retrieval step di awal.
- Latensi tambahan ~200ms dari embed query + SQL — masih
  imperceptible relatif terhadap latensi LLM.

GUARDRAIL:
- JANGAN ubah tool use yang sudah dibangun di Module 05
  Section 4 (Agentic) — system prompt baru harus tetap
  kompatibel dengan tool calling.
- JANGAN hapus error handling yang sudah ada.
- Apabila searchKnowledge throw, JANGAN crash request —
  log error dan fallback ke system prompt tanpa konteks
  (panggil buildAdvisorSystemPrompt([])).
```

**Verifikasi:**

1. Route handler memanggil `searchKnowledge` + `buildAdvisorSystemPrompt` sebelum streaming.
2. Header `x-rag-sources` (Opsi A) atau wrapper JSON (Opsi B) ada di response.
3. Server log menunjukkan query + retrieved chunk IDs setiap request.
4. Chatbot tetap jalan end-to-end — kirim pertanyaan dapat respons streaming.
5. `npx tsc --noEmit` clean.

---

## Prompt 3 — Tampilkan Sumber (Citations) di UI

**Salin prompt berikut, paste ke Claude Code:**

```
Sekarang tampilkan sumber chunk yang dipakai di bawah bubble
respons asisten — citation user-facing.

GOAL:
- Modifikasi komponen AIChatPanel (kemungkinan
  src/components/AIChatPanel.tsx atau path serupa dari
  Module 05).
- Baca header response `x-rag-sources` dari fetch / streaming
  client. Parse JSON ke array {id, content, metadata}.
- Simpan ke state per-message (mis. tambah field `sources`
  ke struct message asisten).
- Render di bawah bubble asisten (HANYA kalau sources.length
  > 0):
  
  📚 Sumber:
  [1] {content snippet ~80 char}...
  [2] {content snippet ~80 char}...
  
  Tampilkan dengan style yang lebih kecil / muted (mis.
  text-xs text-muted-foreground) agar tidak dominan.

- Apabila tidak ada source (mis. handler fallback ke
  konteks kosong), JANGAN tampilkan section 📚 sama sekali
  — biarkan bubble seperti biasa.

CONTEXT:
- Tujuan UX: user tahu jawaban Claude berbasis fakta apa.
- Citation membantu trust + memudahkan user verifikasi.

GUARDRAIL:
- JANGAN ubah logic streaming token — citation muncul di
  AKHIR (setelah stream selesai), tidak per-token.
- JANGAN fetch ulang ke server untuk dapat sources — pakai
  yang sudah dikirim via header.
- Apabila parse JSON gagal, fail silently (citation
  disembunyikan) — JANGAN crash UI.
```

**Verifikasi:**

1. Kirim pertanyaan ke chatbot → respons muncul dengan section "📚 Sumber" di bawahnya.
2. Jumlah sumber sesuai retrieved chunk (max 5 default).
3. Untuk pertanyaan yang tidak related ke FAQ, section sumber tidak muncul (atau muncul kosong, tergantung threshold).
4. UI tidak crash kalau header `x-rag-sources` absen.

---

## Prompt 4 — Test End-to-End

**Salin prompt berikut, paste ke Claude Code:**

```
Sekarang verifikasi RAG end-to-end dengan tiga skenario
kontras.

GOAL:
- BUKAN buat kode — minta saya untuk mencoba 3 pertanyaan
  di chatbot dan verifikasi behavior yang diharapkan.
- Berikan saya tabel verifikasi seperti ini:
  
  | Skenario | Pertanyaan | Ekspektasi jawaban | Ekspektasi sumber |
  |---|---|---|---|
  | (a) Persis di FAQ | "Apa itu emergency fund?" | Jawab persis sesuai FAQ #2 | 1–2 sumber, top distance < 0.3 |
  | (b) Related tapi tidak persis | "Saya newbie investasi, mulai dari mana?" | Jawab adaptasi dari FAQ investasi pemula | 2–3 sumber, distance 0.3–0.5 |
  | (c) Sama sekali tidak related | "Apa resep rendang Padang?" | Claude jujur bilang tidak tahu / di luar konteks | 0 sumber (atau "Tidak ada konteks...") |

- Untuk tiap skenario, beri 1 baris "Tanda RAG bekerja":
  - (a) jawaban mengandung angka/istilah persis dari FAQ
        (mis. "3-6 kali pengeluaran")
  - (b) jawaban relevan tapi punya tambahan reasoning
        Claude
  - (c) Claude TIDAK mengarang — bilang konteks tidak
        cukup atau topik di luar finance

- Tambahkan 1 instruksi cek server log: pastikan log
  "[RAG] query: ..." dan "[RAG] retrieved: ..." muncul
  untuk tiap request.

CONTEXT:
- Ini smoke test manual untuk validasi end-to-end pipeline.
- Tidak perlu kode tambahan — hanya verifikasi behavior.

GUARDRAIL:
- JANGAN modifikasi kode apa pun di prompt ini.
- Apabila salah satu skenario gagal (Claude mengarang di
  (c), atau citation kosong di (a)), JANGAN langsung
  patch — diagnosa dulu: threshold? prompt? handler? Beri
  saya hipotesis akar masalah.
```

**Verifikasi:**

1. Skenario (a): jawaban Claude mengandung fakta spesifik dari FAQ + citation muncul dengan distance rendah.
2. Skenario (b): jawaban relevan dengan citation 2–3 sumber.
3. Skenario (c): Claude jujur bilang tidak tahu / di luar topik — TIDAK mengarang fakta.
4. Server log menampilkan `[RAG] query` + `[RAG] retrieved` untuk setiap request.
5. Tidak ada error 500 / crash di chatbot.

---

## Validasi Akhir Section 2

- [ ] `src/lib/prompts.ts` punya `buildAdvisorSystemPrompt`.
- [ ] Route handler `/api/advisor` memanggil `searchKnowledge` + `buildAdvisorSystemPrompt`.
- [ ] Header `x-rag-sources` (atau wrapper JSON) ada di response.
- [ ] `AIChatPanel` render section "📚 Sumber" di bawah respons asisten.
- [ ] 3 skenario test (a/b/c) pass.
- [ ] `npx tsc --noEmit` clean.

## Refleksi Section 2

1. Pada skenario (c), apabila Claude tetap mengarang meskipun konteks kosong, di mana letak kesalahannya — prompt, model, atau parameter?
2. Mengapa kami pakai `system` parameter untuk inject konteks, bukan menambahkan sebagai user message?
3. Apakah retrieve setiap turn (multi-turn chat) atau hanya turn pertama? Apa trade-off-nya?
4. Bagaimana Anda akan ukur "tingkat halusinasi" secara kuantitatif setelah RAG aktif? (Hint: faithfulness, answer relevance — pikirkan metrik, tidak perlu implementasi.)

---

⬅️ Kembali: **[Section 1 — Pencarian Semantik](./latihan-pencarian-semantik.md)** · 🏠 Index: **[Module 07 — Latihan](./latihan.md)** · ➡️ Lanjut: **[Section 3 — Chunking Strategy](./latihan-chunking.md)**
