# Module 07 — Latihan

> Module 07 ini **konseptual** — tidak ada latihan coding eksekusi seperti module lain. Materi RAG ditujukan untuk membangun **intuisi** sebelum Anda memilih path implementasi yang sesuai dengan use case.

## Apa yang Harus Anda Lakukan

1. Baca `materi.md` secara penuh — terutama bagian:
   - **Kelemahan Terbesar LLM: Halusinasi**
   - **Analogi Closed Book vs Open Book**
   - **Alur Kerja RAG: Contoh "Pengeluaran Bulan Ini"**
   - **Kapan RAG TIDAK Tepat?**
2. Renungkan pertanyaan refleksi di bawah ini.
3. Lanjut ke **Module 08 — AI Agent & Tools** apabila kasus Anda lebih cocok dengan **function calling** (akses data terstruktur, action ke DB).

## Refleksi

Tuliskan jawaban di catatan pribadi atau diskusikan dengan rekan:

1. **Pernahkah Anda menjumpai halusinasi LLM** di tools yang Anda pakai sehari-hari (ChatGPT, Claude.ai, Copilot)? Bagaimana Anda menyadarinya, dan apa dampaknya kalau tidak Anda sadari?
2. Dari analogi **closed book vs open book**, di skenario Fin-App: pertanyaan user **apa saja** yang lebih cocok dijawab dengan RAG (open book = perlu konteks dari knowledge base), dan **apa saja** yang lebih cocok dijawab dengan function calling (struktural — query DB)?
3. Apa **risiko terbesar** dari implementasi RAG yang **buruk** menurut Anda? (mis. chunks tidak relevan masuk konteks → Claude tetap halusinasi, atau citation yang salah membuat user lebih percaya jawaban yang salah)
4. Apabila Fin-App Anda akan menambah fitur **RAG di iterasi berikutnya**, source dokumen apa yang paling berguna untuk di-embed jadi knowledge base? (mis. FAQ keuangan, panduan internal, regulasi OJK, dll.)
5. Apa perbedaan **mental model** antara membangun aplikasi LLM **tanpa RAG** vs **dengan RAG**? Apa yang berubah dalam cara Anda mendesain sistem prompt + flow data?

---

🏠 Kembali: **[Day 3 — System Prompt Engineering](../README.md)** · ➡️ Lanjut: **[Module 08 — AI Agent & Tools](../../Day%204%20-%20AI%20Agent%20%26%20Tools/Module-08-AI-Agent/materi.md)** (function calling untuk akses data terstruktur)
