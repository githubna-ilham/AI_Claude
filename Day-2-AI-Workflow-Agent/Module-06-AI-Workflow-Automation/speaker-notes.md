# Speaker Notes — Module 6

**Durasi total:** 90 menit
**Energi audiens:** Menjelang siang, mulai turun. Sisipkan demo live di tengah untuk angkat energi.

## Alokasi Waktu

| Segmen | Menit | Cue |
|---|---|---|
| Hook + recap M5 | 5 | Tanya: "Pernah pipeline rules-based pecah karena edge case? AI workflow membantu fleksibilitas, tapi punya jebakan baru." |
| Workflow vs Single vs Agent | 10 | Tulis tabel di whiteboard, ajak peserta isi |
| Prompt chaining + pola | 15 | Pakai diagram mermaid, beri contoh map-reduce untuk dokumen panjang |
| Tool integration concept | 10 | Tekankan: di workflow, *developer* yang pilih tool. Di agent, *model* yang pilih |
| Demo live pipeline 3-step | 15 | Jalankan code, suntik error sengaja di JSON |
| Error handling + cost opt | 10 | Diskusi: model mixing, caching, parallel |
| Lab 05 briefing + kerja | 20 | Trainer keliling |
| Wrap-up | 5 | Highlight: kalau urutan masih bisa Anda gambar di whiteboard → workflow cukup |

## Jawaban Kunci Q&A

1. **Single prompt cukup**: task atomic (1 klasifikasi, 1 ringkasan pendek), input pendek, output sederhana.
2. **Risiko chain panjang**: error di step awal merembet ke akhir; latency = total of all steps; cost berlipat; debugging kompleks.
3. **Pilih model per step**: gunakan Haiku untuk klasifikasi/router/ekstraksi sederhana; Sonnet untuk generasi panjang atau reasoning multi-step.
4. **Workflow vs Agent — predictability**: workflow deterministik di level kontrol; agent membiarkan model memilih next step. Trade-off: fleksibilitas vs predictability.
5. **JSON invalid**: (a) retry dengan instruksi tegas, (b) prefill `{` di assistant message, (c) parser tolerant + extract substring JSON, (d) fallback ke model lebih besar, (e) human handover untuk edge case.

## Anekdot

- Cerita: tim yang awalnya pakai 1 prompt monolitik gagal di kasus dokumen panjang; setelah dipecah jadi map-reduce, akurasi naik 30% dan latency turun 40% (karena parallel).
- Tunjukkan: chain 7 step yang sebenarnya bisa diciutkan jadi 3 — "lebih banyak step ≠ lebih baik".

## Common Pitfalls

- **Pitfall 1**: tidak validasi output antar step. Akibat: step 2 menerima JSON rusak, error misterius.
- **Pitfall 2**: pakai Sonnet untuk semua step → mahal & lambat tanpa benefit.
- **Pitfall 3**: tidak ada logging per step → debugging mimpi buruk.
- **Pitfall 4**: campuradukkan workflow dan agent terlalu cepat. Saran: bangun workflow dulu, baru promote ke agent kalau urutan benar-benar variabel.
- **Pitfall 5**: lupa idempotency. Kalau step 3 gagal dan kita retry, jangan double-charge atau double-send email.

## Transisi ke Modul 7

> "Sampai sini, Andalah yang mendesain urutan. Tapi bagaimana kalau task-nya: 'cek apakah customer X eligible upgrade, kalau ya kirim penawaran, kalau tidak buatkan rekomendasi lain'? Urutan tergantung kondisi. Itu wilayah **AI Agent** — yang kita masuki di Modul 7."
