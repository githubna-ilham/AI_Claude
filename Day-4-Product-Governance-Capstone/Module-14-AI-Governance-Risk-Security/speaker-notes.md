# Speaker Notes — Module 14 (Governance, Risk & Security)

**Total**: 120 menit. Modul berat secara konten — disiplin time-keeping wajib.

---

## Segmen 1 — Pembuka (0:00 – 0:08, 8 menit)

**Cue**: Buka dengan headline berita yang relate.

**Pertanyaan pembuka**:
> "Siapa di sini yang sudah pernah denger 'karyawan Samsung paste kode ke ChatGPT lalu bocor'? Apa yang sebenarnya terjadi?"

Mayoritas peserta tahu cerita, sedikit yang tahu detail. Pakai ini untuk mengangkat: governance bukan soal compliance kosmetik, tapi tentang melindungi organisasi.

**Anekdot**: "Module 13 mengajarkan Anda merancang AI. Module 14 mengajarkan Anda tidur nyenyak setelah AI-nya rilis."

**Common pitfall**: Peserta menganggap topik ini "urusan legal". Tegaskan: engineer dan PM adalah lini pertama, legal datang belakangan.

---

## Segmen 2 — Governance Framework (0:08 – 0:25, 17 menit)

**Cue**: Diagram 5 pilar.

**Alokasi**:
- 10 menit penjelasan pilar
- 7 menit aktivitas: peserta menulis 1 risiko nyata di proyek mereka untuk tiap pilar (sticky note)

**Jawaban kunci**:

*"Siapa yang harusnya jadi AI Governance Owner di perusahaan?"*
> "Tidak ada jawaban universal. Pattern yang berhasil: CTO/CIO + Chief Compliance Officer co-own, dengan komite cross-functional bulanan. Yang gagal: dititip ke 1 orang junior."

**Common pitfall**: Bingung memisahkan governance vs security. Bedakan: governance = *kebijakan & akuntabilitas*; security = *implementasi teknis perlindungan*.

---

## Segmen 3 — Bias & Fairness (0:25 – 0:40, 15 menit)

**Cue**: Tampilkan contoh klasik — bias gender pada job recommendation.

**Demo singkat**: Minta Claude men-generate "10 nama untuk CEO startup". Amati distribusi gender/etnis nama. Lalu ulangi dengan instruksi eksplisit "ensure diverse representation across gender and ethnicity". Bandingkan.

**Anekdot**: Cerita Amazon resume screener (2018) yang harus dihentikan karena bias gender.

**Common pitfall**: Peserta technical menganggap bias adalah "masalah data". Sebagian benar, tapi prompt design + retrieval bisa memperburuk atau memperbaiki.

---

## Segmen 4 — Security Risk & OWASP LLM Top 10 (0:40 – 0:55, 15 menit)

**Cue**: Tabel OWASP LLM Top 10.

**Alokasi**: Lewati cepat, fokus pada LLM01 (prompt injection) dan LLM08 (excessive agency) — paling sering muncul di project peserta.

**Jawaban kunci**:

*"Apakah Claude lebih aman dari GPT?"*
> "Setiap vendor punya alignment training masing-masing. Anthropic punya Constitutional AI + RSP. Tapi *tidak ada model yang kebal* prompt injection. Asumsi default: vendor menyediakan baseline, Anda wajib menambahkan layer defense aplikasi."

**Common pitfall**: Tergantung penuh pada vendor. Tekankan: prompt injection adalah masalah aplikasi, bukan masalah model.

---

## Segmen 5 — Demo Live Prompt Injection (0:55 – 1:25, 30 menit)

**Cue**: Buka terminal + Claude API. Siapkan dua file: `naive_prompt.py` dan `hardened_prompt.py` sebelumnya.

**Alokasi**:
- 5 menit setup + naive prompt
- 5 menit attack demo (direct injection)
- 5 menit indirect injection via dokumen
- 10 menit hardened version walkthrough
- 5 menit output filter + logging

**Anekdot**: "Saya pernah lihat developer yang yakin system prompt-nya aman karena 'sudah pakai delimiter XML'. Saya butuh 3 menit untuk bypass. Lesson: jangan pernah PD."

**Common pitfall**:
- Demo terlalu cepat — peserta tidak sempat baca prompt. Pelan-pelan, baca keras-keras setiap baris attack.
- Lupa menunjukkan log. Pastikan log struktur ditampilkan di akhir.

**Safety note**: Pastikan API key demo bukan production. Demo attack bisa men-generate output yang sensitif.

---

## Segmen 6 — Privacy & Compliance (1:25 – 1:45, 20 menit)

**Cue**: Slide UU PDP Indonesia (UU 27/2022) dengan highlight Pasal 20, 46, 57.

**Alokasi**:
- 8 menit UU PDP
- 5 menit GDPR (untuk peserta dengan customer EU)
- 7 menit EU AI Act + diskusi klasifikasi use case peserta

**Anekdot**: "Per Oktober 2024, UU PDP Indonesia sudah full enforcement. Sanksi 2% revenue bukan main-main untuk korporasi besar."

**Jawaban kunci**:

*"Apakah kirim data customer ke API Anthropic boleh?"*
> "Boleh jika: (1) ada dasar pemrosesan yang sah, (2) ada DPA dengan vendor, (3) sudah dilakukan minimisasi/redaksi data sensitif, (4) ada notifikasi/transparansi ke subjek data. Anthropic punya enterprise tier dengan data residency option — verifikasi dengan legal."

**Common pitfall**: Anggap UU PDP = GDPR. Mirip tapi tidak identik. Misal: notifikasi breach UU PDP = 3×24 jam, GDPR = 72 jam.

---

## Segmen 7 — Studi Kasus + Checklist (1:45 – 2:05, 20 menit)

**Cue**: Buka folder `studi-kasus-prompt-injection.md` dan `checklist-responsible-AI.md`.

**Aktivitas**:
- 10 menit kelompok kecil (3–4 orang) bahas 1 studi kasus + identifikasi mitigation
- 10 menit isi checklist untuk use case canvas masing-masing

**Common pitfall**: Peserta mengisi checklist sebagai compliance theater. Tegaskan: kalau "tidak siap" → tulis "tidak siap" dan jadikan backlog Capstone.

---

## Segmen 8 — Wrap-up & Q&A (2:05 – 2:00... eh, 1:45 – 2:00, 15 menit)

**Cue**: Slide 5 pertanyaan refleksi.

**Tutup dengan**:
> "Module 13 + 14 adalah kerangka. Capstone berikutnya adalah ujian apakah Anda bisa menerapkannya dalam tekanan waktu. Tim yang bisa pamer governance awareness di presentasi akan menonjol."

---

## Catatan Tambahan

- Pastikan slide UU PDP terupdate jika ada PP turunannya yang sudah keluar.
- Jika peserta dari sektor regulated (banking, healthcare, telco), sediakan 5–10 menit ekstra di segmen compliance.
- Bawa printout OWASP LLM Top 10 1 lembar — peserta suka membawa pulang sebagai referensi.
