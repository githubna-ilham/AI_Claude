# Speaker Notes — Module 12: Advanced AI Applications

**Durasi total**: 90 menit
**Format**: 45' materi + 45' lab walkthrough

---

## Alokasi Waktu

| Menit | Segmen | Aktivitas |
|-------|--------|-----------|
| 0–5 | Pembuka | Recap Module 10–11, framing "production reality" |
| 5–15 | Konsep 1.1–1.2 | Tiga pola + arsitektur enterprise |
| 15–25 | Konsep 1.3–1.4 | Performance + cost optimization (demo kalkulasi) |
| 25–35 | Konsep 1.5–1.7 | Scaling + reliability + audit |
| 35–45 | Demo live | Router intent + caching + cost tracker |
| 45–85 | Lab 11 | Walkthrough + coaching |
| 85–90 | Wrap-up Day 3 | Bridge ke Day 4 (deployment & evaluation) |

---

## Cue Fasilitator

### Pembuka

"Demo lab 08–10 berjalan bagus. Tapi semua itu di laptop kita. Sekarang bayangkan 5000 karyawan pakai bersamaan, finance tanya cost, security tanya audit log. Itu Module 12."

### Tiga pola

- Minta peserta angkat tangan: siapa yang use case-nya cocok ke mana?
- PM dan IT Architect biasanya sangat resonate di sini.

### Arsitektur enterprise

- Tekankan **Router** sebagai single point of governance: cost, audit, model selection.
- Anekdot: tim yang langsung pakai Sonnet untuk semua → bill 10x lipat dari prediksi. Setelah routing Haiku → 70% reduksi.

### Performance + cost (demo kalkulasi)

- Buka spreadsheet/whiteboard. Hitung live: HR bot 1000 query/hari × 8K system prompt × 1000 turn × 30 hari.
- Tunjukkan dengan/ tanpa caching. Angka konkret membuat audience non-teknis sadar urgensi.
- **Common pitfall**: caching hanya berlaku jika prefix prompt **identik byte-by-byte**. Variabel di awal merusak cache.

### Scaling

- Diagram horizontal scale. Tekankan **stateless backend** + Redis.
- Tanya: "Berapa replica yang Anda butuhkan untuk 100 QPS?" → ajak hitung dengan asumsi 1 RPS per replica, p95 latency 3s.

### Reliability + audit

- Tegaskan UU PDP Indonesia & GDPR — log prompt user adalah **data pribadi** kalau berisi PII.
- PII redaction sebelum log. Pakai library seperti `presidio` atau regex sederhana untuk PoC.

### Demo live (35–45')

- Tunjukkan classify → branch → RAG → tool → audit dalam satu file.
- **Pitfall yang sengaja didemo**: cache miss karena timestamp ikut di system prompt. Fix dengan memindahkan timestamp ke user message.

### Lab 11

- Lab paling kompleks. Bagi tim 3–4 orang dengan peran: developer, PM/spec writer, QA.
- Checkpoint 20' lab: arsitektur sudah di-sketsa di whiteboard/Excalidraw.
- Checkpoint 40' lab: minimal 1 end-to-end query jalan (chat + RAG, tool boleh mock).

---

## Jawaban Kunci Q&A

1. **Haiku vs Sonnet** — Haiku: classification, intent, simple extraction, reranking, summarization. Sonnet: reasoning multi-step, synthesis RAG dengan banyak source, code generation, tool orchestration kompleks. Aturan: coba Haiku dulu, naikkan ke Sonnet jika quality eval gagal.
2. **Batches API** — Saat tidak butuh real-time (ingestion enrichment, evaluasi offline, generate report bulanan). Diskon 50%, latency 24 jam SLA. Jangan untuk chat user-facing.
3. **Metrik utama** — Latency p50/p95/p99, error rate, cost/jam dan cost/user, cache hit rate, retrieval recall (untuk RAG), user satisfaction (thumbs).
4. **Graceful degradation** — Circuit breaker → return cached answer atau "saya sedang sibuk, coba lagi 1 menit". Queue request untuk retry async. Pernah pertimbangkan fallback ke model lain (lock-in vs reliability trade-off).
5. **Risiko audit log** — PII bocor, retention compliance. Mitigasi: redaction sebelum store, encryption at rest, retention policy (mis. 90 hari), access control ke log.

---

## Common Pitfalls

- **Cache miss tidak disadari** — variabel dinamis di prefix.
- **Tidak ada budget alert** — bill kaget di akhir bulan.
- **Audit log tanpa redaction** — kena audit security.
- **Tool use tanpa human-in-the-loop** untuk destructive action.
- **Tidak ada eval set** — tidak tahu kapan quality regress.

---

## Anekdot

- Tim e-commerce yang pakai 1 ukuran prompt untuk semua → 90% bisa di-Haiku → setelah split bill turun dari $40K → $9K/bulan.
- Insiden compliance: bot HR menyimpan log lengkap termasuk gaji karyawan → kena temuan audit → harus rebuild dengan redaction.

---

## Closing Day 3

"Hari ini kita bangun chat app, tambah RAG, lalu jadikan enterprise-grade. Day 4 fokus: deployment, evaluation, dan governance jangka panjang. Lab 11 silakan dilanjutkan tadi malam — Day 4 kita lanjut dengan deploy artifact Anda."
