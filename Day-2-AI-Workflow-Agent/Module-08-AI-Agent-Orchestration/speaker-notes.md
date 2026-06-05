# Speaker Notes — Module 8

**Durasi total:** 90 menit
**Energi audiens:** Sore, mulai lelah. Tetap perlu fokus karena ini modul teknis penting → demo live menjadi anchor.

## Alokasi Waktu

| Segmen | Menit | Cue |
|---|---|---|
| Recap M7 + hook | 5 | "Kemarin kita gambar agent loop. Sekarang kita beneran kode." |
| Single vs multi-agent | 10 | Tunjukkan tabel. Tekankan: mulai single dulu |
| Tool calling siklus + sequence diagram | 15 | Bahas detail step by step pakai mermaid sequence |
| Tool schema best practice | 10 | Anti-pattern: deskripsi vague, schema longgar |
| Demo live tool calling 3-tool | 15 | Live coding. Mulai dari 1 tool, naik ke 2-3 |
| Decision making + multi-agent sketch | 10 | Whiteboard supervisor diagram |
| Lab 06 briefing + kerja | 20 | Trainer keliling |
| Wrap-up | 5 | Bridge ke Modul 9: bangun agent end-to-end |

## Jawaban Kunci Q&A

1. **Model "minta", app eksekusi.** Tekankan bahwa Claude tidak punya akses internet/sistem; tool execution adalah tanggung jawab developer.
2. **Lupa append tool_result**: API akan tolak / model akan stuck mengira tool belum dijalankan. Selalu cek `stop_reason`.
3. **Single-agent dipilih**: lebih murah, predictable, lebih mudah di-debug, cukup untuk < 10 tools.
4. **Cegah stuck di tool yang sama**: max_iter, deteksi `last_n_tool_calls`, perbaiki description tool, tambahkan tool `give_up`, tambahkan instruksi system prompt.
5. **Paralel tool call membantu**: ketika 2+ tool independen (cuaca + harga). **Merepotkan**: kalau tool kedua butuh hasil tool pertama → harus serial.

## Anekdot

- Cerita: tool description vague ("get info") bikin model panggil tool itu untuk SEGALA pertanyaan → kacau. Setelah deskripsi diperketat ("use ONLY for stock price queries") → akurasi naik drastis.
- Cerita: tim yang langsung bangun 5-agent system tanpa coba single-agent dulu — debugging mimpi buruk dua minggu.

## Common Pitfalls

- **Pitfall 1**: tool description copy-paste dari function docstring engineer → tidak optimal untuk LLM.
- **Pitfall 2**: tidak handle `is_error=True` di tool_result → model tidak tahu telah gagal.
- **Pitfall 3**: schema tanpa `required` → model panggil tool tanpa argumen penting.
- **Pitfall 4**: lupa loop, hanya 1 call → tool_use tidak diproses.
- **Pitfall 5**: campuran content block (text + tool_use) tidak di-append apa adanya → history rusak.
- **Pitfall 6**: tool yang return data besar (10MB JSON) → context meledak. Truncate atau simpan reference.

## Transisi ke Modul 9

> "Anda sudah punya tool calling jalan. Sekarang waktunya bungkus jadi **aplikasi agent nyata** — dengan auth, conversation loop, deployment basics. Itu di Modul 9, dan lab capstone Day 2."
