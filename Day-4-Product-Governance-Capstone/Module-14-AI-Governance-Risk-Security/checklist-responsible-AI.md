# Checklist Responsible AI — Pre-Deployment Gate

**Gunakan checklist ini sebagai gate sebelum sistem AI Anda go-live ke user produksi.**
Tandai `[x]` jika sudah siap, `[ ]` jika belum, dan tulis catatan/owner di samping setiap item.

---

## 1. Data Privacy

- [ ] Inventaris data yang dikonsumsi sistem (sumber, format, sensitivitas)
- [ ] Klasifikasi data: Public / Internal / Confidential / Restricted
- [ ] PII redaction layer aktif sebelum data dikirim ke LLM API (email, no HP, NIK, no rekening, alamat)
- [ ] Secret/credential filter pada input dan output (API key, password, token)
- [ ] Retention policy log prompt + response (default rekomendasi: 30–90 hari, lebih ketat untuk PII)
- [ ] Mekanisme deletion request sesuai hak subjek data (UU PDP Pasal 5–13)
- [ ] DPA (Data Processing Agreement) dengan vendor LLM terverifikasi legal
- [ ] Verifikasi zero-retention / no-training opt-out di tier yang digunakan
- [ ] Dasar pemrosesan data jelas (consent / kontrak / kepentingan sah) — UU PDP Pasal 20
- [ ] Privacy notice di UI menjelaskan bahwa user berinteraksi dengan AI dan data digunakan untuk apa

## 2. Bias Monitoring

- [ ] Eval dataset berisi minimal 50–200 prompt representatif (gender, usia, daerah, bahasa)
- [ ] Counterfactual testing dijalankan: ganti atribut sensitif → ukur delta output
- [ ] Metric fairness didefinisikan (mis. equal refusal rate, equal tone rating)
- [ ] System prompt menyertakan instruksi non-discrimination eksplisit jika relevan
- [ ] Periodic audit (kuartalan) dengan reviewer manusia lintas latar
- [ ] Hasil audit terdokumentasi dan accessible untuk stakeholder

## 3. Output Safety

- [ ] Moderation API (Anthropic / external) aktif untuk konten yang dikonsumsi end-user
- [ ] Regex / classifier untuk PII leak detection pada output
- [ ] Blacklist topik (sesuai kebijakan organisasi: politik, religi, medical advice, legal advice)
- [ ] Hallucination guard: citation wajib untuk RAG, fallback "tidak menemukan jawaban" tersedia
- [ ] Markdown/URL sanitization untuk mencegah exfiltration via image/link
- [ ] Test set adversarial (minimal 20 prompt jailbreak / injection) lolos baseline

## 4. Audit Log

- [ ] Setiap request di-log: timestamp, user_id (hashed), input, output, model, latency, cost
- [ ] Flag attempt suspicious (instruction override, PII leak attempt, abuse) tersimpan terpisah
- [ ] Log di-encrypt at rest dan in transit
- [ ] Akses log ter-role-based; audit trail akses log juga di-log
- [ ] Retention log sesuai kebijakan (umumnya 1 tahun untuk compliance, lebih untuk regulated industry)
- [ ] Dashboard observability tersedia untuk owner sistem

## 5. Human-in-the-Loop

- [ ] Aksi destruktif (kirim email, transaksi, hapus data, eskalasi) wajib confirmation user atau approver
- [ ] Tombol "eskalasi ke manusia" tersedia di setiap layar user-facing
- [ ] SLA respon human-fallback didefinisikan (mis. 15 menit office hour)
- [ ] Reviewer manusia dilatih untuk mengenali output yang patut di-flag
- [ ] Feedback loop (thumbs up/down, "report this response") terhubung ke pipeline eval
- [ ] Sampling: minimal X% output di-review manusia per minggu untuk QA

## 6. Compliance

### UU PDP Indonesia (UU No. 27/2022)

- [ ] Dasar pemrosesan teridentifikasi (Pasal 20)
- [ ] Hak subjek data dapat dilayani: akses, koreksi, penghapusan, portabilitas (Pasal 5–13)
- [ ] Mekanisme notifikasi kegagalan perlindungan tersedia: 3×24 jam ke otoritas + subjek data (Pasal 46)
- [ ] Khusus data sensitif (kesehatan, biometrik, anak, keuangan pribadi): proteksi tambahan (Pasal 4)
- [ ] DPO / focal point compliance ditunjuk dan dikomunikasikan
- [ ] Transfer data lintas batas sesuai ketentuan (Pasal 56)

### GDPR (jika ada user EU)

- [ ] Legal basis Article 6 teridentifikasi
- [ ] DPIA dijalankan untuk high-risk processing
- [ ] Mekanisme breach notification 72 jam siap

### EU AI Act (jika operasi di EU atau use case high-risk)

- [ ] Klasifikasi risiko sistem dilakukan (unacceptable / high / limited / minimal)
- [ ] Untuk high-risk: dokumentasi teknis, dataset governance, human oversight, post-market monitoring tersedia
- [ ] Transparency obligation: user tahu mereka berinteraksi dengan AI

### Sektoral (jika relevan)

- [ ] POJK / SEOJK terkait (financial services)
- [ ] Permenkes terkait (healthcare)
- [ ] Standar industri lain yang berlaku

## 7. Security

- [ ] System prompt hardening (delimiter, trust separation, refusal instruction)
- [ ] Input length cap dan rate limiting per user
- [ ] Cost cap per user per hari (anti DoS-by-prompt)
- [ ] Tool whitelist + parameter validation untuk agent
- [ ] Red-team test rutin (minimal kuartalan)
- [ ] Vulnerability disclosure channel terbuka
- [ ] Secret management (API key tidak hardcoded, rotation policy ada)
- [ ] Network egress dari komponen AI dibatasi ke domain whitelist

## 8. Incident Response

- [ ] Runbook incident response AI tersedia (siapa dihubungi, bagaimana isolate)
- [ ] Kill switch / feature flag untuk men-disable AI cepat
- [ ] Rollback procedure ke versi prompt/model sebelumnya
- [ ] Communication template untuk stakeholder internal + user
- [ ] Post-mortem template + komitmen blameless review
- [ ] Drill incident response minimal 1×/tahun

---

## Cara Memakai Checklist Ini

1. **Pre-launch**: isi seluruh checklist; minimal 80% item terisi `[x]` sebelum go-live ke user eksternal.
2. **Quarterly review**: tinjau ulang setiap kuartal — item bisa "regress" karena perubahan code/model.
3. **Capstone**: untuk presentasi capstone, tunjukkan minimal 10 item yang sudah dipertimbangkan untuk skor governance.
4. **Stakeholder sign-off**: minta tanda tangan owner produk + security/compliance officer.

---

## Catatan

- Checklist ini bukan substitusi untuk legal review. Konsultasikan ke tim legal untuk konteks regulatori spesifik.
- Setiap "[ ]" yang tertinggal saat go-live wajib didokumentasikan sebagai *known risk* dengan owner + target tanggal penyelesaian.
