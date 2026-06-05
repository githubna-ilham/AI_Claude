# Speaker Notes — Module 10: Build AI Application

**Durasi total**: 120 menit
**Format**: 60' materi + 60' lab walkthrough/coaching

---

## Alokasi Waktu

| Menit | Segmen | Aktivitas |
|-------|--------|-----------|
| 0–5 | Pembuka | Recap Day 2, transisi ke "production AI app" |
| 5–20 | Konsep 1.1–1.3 | Arsitektur referensi + lapisan state |
| 20–35 | Konsep 1.4–1.6 | Context management + frontend choices + backend checklist |
| 35–55 | Demo live | Bangun chat app FastAPI + HTML dari nol |
| 55–60 | Q&A singkat | 2–3 pertanyaan klarifikasi |
| 60–120 | Lab 08 | Coaching peserta, walk between tables |

---

## Cue Fasilitator per Segmen

### Pembuka (0–5')

Buka dengan pertanyaan provokatif: **"Berapa banyak dari Anda yang sudah pernah panggil API Claude dari Postman? Bagus. Sekarang berapa yang sudah jalankan itu di produksi melayani 1000 user?"** Tujuannya membangun urgency bahwa "wrap API" ≠ "build app".

### Konsep arsitektur (5–20')

- Tunjuk diagram mermaid. Tekankan **dua arah streaming**: peserta sering lupa bahwa SSE Anthropic harus di-relay, bukan di-buffer.
- Anekdot: ceritakan kasus tim yang menyimpan history di memory backend, lalu deploy 3 replica di Kubernetes — user complain "kok bot lupa". Pelajaran: state harus eksternal.

### Context window (20–35')

- Jangan jualan "context 1M jadi tidak perlu summarization". Tegaskan: **biaya berbanding lurus dengan token**.
- Tunjukkan kalkulasi cepat: 100K input token × 100 panggilan/hari × $3/MTok ≈ $30/hari hanya untuk satu user power. Multiply by user count.
- Sebutkan **prompt caching** sebagai mitigasi utama untuk system prompt statis.

### Demo live (35–55')

- Buka terminal + editor split screen.
- Jalankan `uvicorn main:app --reload` lalu buka browser.
- **Common pitfall**: lupa set `Content-Type: text/event-stream`, browser tidak streaming. Sengaja buat error ini lalu fix di depan peserta — momen belajar.
- Pitfall kedua: append assistant message ke history **setelah** stream selesai, bukan saat mulai. Jika gagal di tengah, history tidak korup.

### Lab 08 (60–120')

- Bagi peserta ke pair (developer + non-developer kalau memungkinkan).
- Checkpoint di menit 30 lab: semua peserta harus sudah dapat respon non-streaming. Jika belum, bantu setup.
- Checkpoint di menit 50: streaming jalan.
- 10 menit terakhir: minta 2 peserta demo singkat.

---

## Jawaban Kunci Q&A

1. **History mentah vs sliding+summary** — 50 turn × ±200 token = 10K input token tiap call. Dengan sliding 10 + summary 200 token = ±2.2K. Hemat ~78%, dan lebih cepat. Trade-off: kehilangan detail.
2. **Streamlit vs Next.js** — Streamlit untuk internal, audience teknis, iterasi cepat, tidak butuh auth canggih. Next.js untuk customer-facing, butuh SEO/marketing page, design system, multi-tenant auth.
3. **Session store tahan restart** — eksternal (Redis/Postgres), idempotent message append, TTL untuk cleanup, backup berkala.
4. **API key di frontend** — JANGAN. Risiko: key di-scrape via DevTools → abuse → bill explode. Mitigasi: backend proxy + per-user rate limit + short-lived token untuk frontend.
5. **Kualitas chat** — gabungan: (a) human eval sample mingguan, (b) LLM-as-judge dengan rubrik, (c) user feedback (thumbs up/down), (d) task completion rate.

---

## Common Pitfalls untuk Dihindari Peserta

- **Hardcode API key** di kode commit ke GitHub → cabut + rotate key segera.
- **Tidak set `max_tokens`** → respon tidak terkontrol, bisa habiskan budget.
- **Append message duplikat** saat retry → conversation history korup.
- **Tidak menutup stream connection** → resource leak di FastAPI.
- **Mencampur system prompt dan user message** → model bingung peran.

---

## Anekdot

- Cerita kasus chatbot HR yang menyimpan history selamanya tanpa retention → tabel Postgres 200GB dalam 3 bulan → bill database lebih mahal dari Anthropic.
- Kasus startup yang membayar $8K/bulan untuk Claude, setelah audit ternyata 70% biaya dari system prompt 5K token yang tidak di-cache.

---

## Hand-off ke Module 11

Tutup dengan: **"Sekarang chat app sudah jalan. Tapi Claude hanya tahu yang ada di training data. Bagaimana kalau user tanya kebijakan internal perusahaan kemarin? Itu masuk Module 11: RAG."**
