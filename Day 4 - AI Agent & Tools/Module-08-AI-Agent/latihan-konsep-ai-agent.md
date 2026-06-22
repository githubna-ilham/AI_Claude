# Section 1 — Konsep AI Agent

> Bagian dari **[Module 08 — Latihan](./latihan.md)**. Lanjutan dari **[Module 07 — Reranking & Hybrid Search](../../Day%203%20-%20Prompt%20Engineering/Module-07-RAG/latihan-reranking.md)**.

> Latihan **konseptual** untuk memperkuat intuisi pola ReAct sebelum coding agent di section berikutnya. Dua prompt — satu manual (no-code), satu di Claude Code untuk dokumentasi.
>
> **Estimasi Section 1**: 45–60 menit.

## Prasyarat Section 1

- [ ] Module 07 selesai. AI Advisor sudah RAG-aware (atau setidaknya streaming + multi-turn dari Module 04 Section 6).
- [ ] Anda sudah membaca `materi.md` bagian Section 1 — paham definisi AI Agent + tiga kemampuan inti + pola ReAct.
- [ ] Akses ke Claude Code di terminal terpisah (untuk Prompt 2).

---

## Prompt 1 — Sketsa ReAct Manual (No-Code)

Latihan ini **tidak melibatkan Claude Code** — Anda menulis sendiri di notes/markdown. Tujuannya membangun intuisi sebelum berinteraksi dengan API.

**Tugas Anda:**

Pilih **dua goal** dari daftar di bawah ini, lalu untuk masing-masing tulis transcript ReAct lengkap (Thought → Action → Observation → Reflect, beberapa iterasi sampai Final Answer). Tools yang tersedia bebas Anda definisikan (mis. `search_x`, `get_y`, dll.) — yang penting masuk akal untuk task.

**Pilihan goal** (pilih 2):

1. _"Bantu saya pindah kos dari Jakarta Selatan ke Bandung bulan depan."_
2. _"Saya mau bikin presentasi tentang AI Agent untuk klien minggu depan."_
3. _"Cari produk laptop yang cocok untuk video editing dengan budget 25 juta."_
4. _"Bantu saya membuat rencana belajar untuk persiapan TOEFL dalam 2 bulan."_
5. _"Saya ingin mulai investasi reksadana dengan modal Rp 5 juta — saran portfolio?"_

**Format yang diharapkan** untuk masing-masing goal:

```
=== Goal: [tuliskan goal yang dipilih] ===

=== Iterasi 1 ===
Thought: [reasoning Anda sebagai agent — apa yang harus dilakukan dulu?]
Action: [tool call konkret, mis. search_apartments(location="Bandung", budget=2000000)]
Observation: [hasil hipotetis dari tool — boleh Anda karang yang masuk akal]
Reflect: [evaluasi: cukup info? lanjut iterasi atau selesai?]

=== Iterasi 2 ===
...

=== Final Answer ===
[respons final agent ke user — ringkasan rencana atau jawaban]
```

**Verifikasi diri Anda:**

1. Apakah setiap **Thought** Anda menjawab "apa yang masih kurang untuk capai goal?"
2. Apakah setiap **Action** memanggil tool yang masuk akal (bukan tindakan yang seharusnya jadi Thought atau jawaban langsung)?
3. Apakah **Reflect** sungguh mengevaluasi (bukan sekadar transisi otomatis)?
4. Apakah ada minimal **3 iterasi** untuk masing-masing goal? (kalau kurang, mungkin goal terlalu sederhana untuk agent — pertimbangkan apakah agent overkill di sini)

> 💡 **Tip**: setelah selesai, baca ulang transcript Anda dengan mata kritis — apakah ada Thought yang seharusnya bisa langsung jadi Final Answer (artinya tool call-nya overkill)? Atau sebaliknya, ada Action yang langsung dilakukan tanpa Thought yang jelas (artinya reasoning Anda lompat)?

---

## Prompt 2 — Dokumentasi ReAct Pattern di Project

Sekarang manfaatkan Claude Code untuk membuat dokumentasi internal di project Fin-App tentang pola ReAct, sebagai persiapan implementasi di section berikutnya.

**Salin prompt berikut, paste ke Claude Code:**

```
Saya sedang mempelajari pola ReAct (Reasoning + Acting) untuk
membangun AI Agent di Fin-App. Tolong buatkan dokumentasi
internal di project.

GOAL:
- Buat file baru docs/AGENT-PATTERNS.md di project Fin-App.
- Isi:
  1. Section "ReAct (Reasoning + Acting)" — definisi singkat
     + diagram loop dalam Mermaid + tabel anatomi 4 langkah.
  2. Section "Mapping ke Claude API" — bagaimana ReAct
     diimplementasi via tool_use + tool_result block. Beri
     contoh TypeScript skeleton (tidak perlu kode jalan,
     cukup struktur).
  3. Section "Decision Checklist: Kapan Pakai Agent?" — 5
     pertanyaan ya/tidak yang membantu developer memutuskan
     apakah suatu fitur cocok pakai agent atau cukup tool
     use sederhana.

CONTEXT:
- Project Fin-App sudah ada Module 05 Section 4 (tool use
  dasar) dan Module 07 (RAG). Module 08 akan tambahkan
  agent loop di atasnya.
- Format file: markdown dengan heading konsisten + Mermaid
  diagram + code block TypeScript.

GUARDRAIL:
- JANGAN membuat file di src/ atau implementasi runtime.
  Cukup dokumentasi di docs/.
- JANGAN copy-paste materi.md Module 08 — tulis ulang
  dengan kata-kata Anda sendiri (developer yang baca akan
  bingung kalau ada duplikasi).
- Mermaid diagram harus render valid (tidak ada syntax
  error). Setelah selesai, jelaskan singkat 1-2 kalimat
  tujuan setiap section.

Setelah selesai, beri saya path file + ringkasan
3 baris isi.
```

**Verifikasi:**

1. File `docs/AGENT-PATTERNS.md` ada di project.
2. Buka file, cek 3 section ada: ReAct, Mapping ke Claude API, Decision Checklist.
3. Diagram Mermaid render valid (preview di IDE atau push ke GitHub untuk cek render).
4. Decision Checklist berisi 5 pertanyaan konkret, bukan filler.
5. Code block TypeScript di section Mapping menunjukkan struktur (interface, function signature) — tidak perlu logic lengkap.

---

## Validasi Akhir Section 1

Pastikan checklist berikut tercapai sebelum lanjut ke section berikutnya (atau menutup section kalau hanya Section 1 yang tersedia):

- [ ] Anda menulis transcript ReAct untuk **dua goal** (Prompt 1) — minimum 3 iterasi per goal.
- [ ] File `docs/AGENT-PATTERNS.md` ada di project (Prompt 2).
- [ ] Anda paham perbedaan **chatbot biasa** vs **AI Agent** (tabel di materi.md).
- [ ] Anda dapat menjelaskan dengan kata-kata sendiri: apa peran Thought, Action, Observation, Reflect.
- [ ] Anda paham hubungan ReAct dengan `tool_use` di Claude API (Module 05 Section 4).
- [ ] Anda dapat menyebutkan **minimal 2 alasan** kapan TIDAK pakai agent.

## Refleksi Section 1

Tuliskan pada catatan pribadi:

1. **Saat menulis transcript ReAct manual** (Prompt 1), bagian mana yang paling sulit — Thought, Action, atau Reflect? Mengapa?
2. Adakah goal di Prompt 1 yang setelah Anda sketsa, ternyata **tidak butuh agent** (cukup single prompt biasa)? Apa indikatornya?
3. Apa **risiko terbesar** menurut Anda dari sebuah agent yang otonom di production? (mis. infinite loop, salah pakai tool destruktif, halusinasi action)
4. Apabila Anda harus bangun agent untuk satu fitur di Fin-App, **fitur apa** yang paling masuk akal? (mis. "agent perencana budget", "agent rekonsiliasi transaksi", dll.)
5. Bagaimana cara Anda **membatasi otonomi** agent di production agar tidak melakukan action destruktif tanpa konfirmasi user?

---

⬅️ Kembali: **[Module 07 — Reranking & Hybrid Search](../../Day%203%20-%20Prompt%20Engineering/Module-07-RAG/latihan-reranking.md)** · 🏠 Index: **[Module 08 — Latihan](./latihan.md)** · ➡️ Lanjut: **[Section 2 — Tools & Function Calling](./latihan-tools-function-calling.md)**
