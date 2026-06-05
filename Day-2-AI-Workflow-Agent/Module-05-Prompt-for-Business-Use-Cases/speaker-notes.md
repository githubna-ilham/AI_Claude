# Speaker Notes — Module 5

**Durasi total:** 90 menit
**Energi audiens:** Sesi pagi, peserta masih fresh. Manfaatkan untuk konsep yang padat.

## Alokasi Waktu

| Segmen | Menit | Cue |
|---|---|---|
| Opening + recap Day 1 | 5 | "Kemarin kita craft prompt. Hari ini kita pakai untuk problem bisnis nyata." |
| Konsep 5 use case | 20 | Pakai whiteboard, gambar pipa input→prompt→output untuk tiap use case |
| Anatomi prompt template | 10 | Tunjukkan diagram mermaid dari materi.md |
| Demo live CS reply | 15 | Live coding via Console Anthropic, jangan pakai IDE supaya fokus prompt |
| Output format & guardrails | 10 | Diskusi cepat: kapan JSON vs Markdown vs XML |
| Lab 04 briefing | 5 | Bagi peserta jadi grup 3–4 orang |
| Lab 04 kerja mandiri | 20 | Trainer keliling, jawab pertanyaan |
| Wrap-up | 5 | Tunjuk 2 grup share hasil singkat |

## Jawaban Kunci untuk Q&A

1. **ROI tertinggi**: biasanya CS reply (volume tinggi, repetitif) atau document automation (efisiensi besar). Tapi *jawaban benar tergantung konteks audiens* — gali dulu.
2. **JSON vs Markdown**: JSON kalau output dipakai sistem (CRM, ticketing). Markdown kalau langsung dibaca manusia. XML enak untuk multi-section yang perlu di-parse parsial.
3. **Cara tahu prompt production-ready**: test set 20–50 contoh (positif + edge case), metric kuantitatif (akurasi label / BLEU / human rating), review human sampling. Tidak ada "gut feeling" di produksi.
4. **JSON invalid**: (a) instruksi tegas, (b) contoh schema di prompt, (c) parser dengan retry, (d) gunakan tool use / Structured Outputs jika tersedia, (e) prefill `{` di awal response assistant.
5. **Risiko CS prod tanpa guardrail**: janji palsu (refund), leak data, brand damage, regulatory issue.

## Anekdot / Cerita

- Cerita case di mana bot CS pernah janji refund $1 untuk product mahal karena disuruh user — gunakan untuk highlight pentingnya guardrail.
- Tunjukkan contoh prompt 50 baris yang sebenarnya **lebih buruk** dari prompt 15 baris yang fokus — lawan asumsi "lebih panjang = lebih baik".

## Common Pitfalls Peserta

- **Pitfall 1**: mencampur context dan task. Solusi: pisahkan dengan heading atau XML tag.
- **Pitfall 2**: minta JSON tapi tidak kasih contoh schema → model invent struktur.
- **Pitfall 3**: prompt asumsikan data bersih, padahal email customer real penuh typo/emoji. Suruh peserta test pakai email "kotor".
- **Pitfall 4**: tidak ada fallback "kalau tidak yakin, katakan tidak yakin" → halusinasi.
- **Pitfall 5**: ngetes 1 input lalu nyatakan "berhasil". Tekankan minimum 10 input.

## Transisi ke Modul 6

> "Sekarang Anda bisa bikin satu prompt yang bagus untuk satu task. Tapi proses bisnis nyata punya banyak step. Bagaimana kalau output prompt A jadi input prompt B? Itu yang kita bahas di Modul 6: **Workflow Automation**."
