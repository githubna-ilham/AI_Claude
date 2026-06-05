# External References

Kumpulan artikel, tutorial, dan dokumentasi eksternal yang relevan dengan materi pelatihan AI Claude. Bisa dibagikan ke peserta sebagai bacaan lanjutan atau dipakai fasilitator untuk memperdalam contoh.

---

## RAG (Retrieval Augmented Generation)

### How to Build an AI-Powered RAG Search Application with Next.js, Supabase, and OpenAI
- **Sumber:** freeCodeCamp
- **URL:** https://www.freecodecamp.org/news/how-to-build-an-ai-powered-rag-search-application-with-nextjs-supabase-and-openai/
- **Ditambahkan:** 2026-05-31
- **Relevan untuk:** Day 3 — Module 10 (Build AI Application) & Module 11 (RAG)
- **Catatan adaptasi untuk pelatihan Claude:**
  - Artikel pakai **OpenAI** sebagai LLM → ganti dengan **Claude API** (`anthropic` SDK). Pola request response berbeda (Claude pakai `messages.create`, format tool use juga beda).
  - **Embedding model** di artikel pakai OpenAI `text-embedding-3-small` → di pelatihan kita pakai **Voyage AI** (`voyage-3`) sebagai default, atau `sentence-transformers/multilingual-e5-large` untuk offline.
  - **Vector store** di artikel pakai **Supabase pgvector** → di pelatihan default **Chroma lokal** (lebih cepat setup), tapi pgvector tetap valid untuk production. Bisa dipakai sebagai contoh kedua di Module 11.
  - **Frontend Next.js** → relevan langsung untuk Lab 08 (Chat App) sebagai alternatif dari Streamlit/HTML minimal yang ada di starter code kita.
  - **Pola yang transferable**: server actions untuk endpoint RAG, streaming response, chunking strategy, similarity search.
- **Saran pemakaian:**
  - Fasilitator: gunakan sebagai contoh stack alternatif (Next.js + Supabase) saat audiens dominan frontend developer.
  - Peserta: bacaan H+1 setelah Module 11 untuk melihat implementasi RAG di stack berbeda dari yang dipraktikkan di lab.
  - Capstone Day 4: bisa jadi referensi untuk peserta yang pilih opsi **Internal Knowledge Assistant** dengan stack JS/TS.

---

## Cara Menambah Referensi

Format entry:

```markdown
### <Judul Artikel>
- **Sumber:** <Publisher>
- **URL:** <link>
- **Ditambahkan:** YYYY-MM-DD
- **Relevan untuk:** <Day X Module Y>
- **Catatan adaptasi:** <bagaimana mengaitkan dengan materi pelatihan>
- **Saran pemakaian:** <fasilitator / peserta / capstone>
```

Kelompokkan per topik utama: **Prompt Engineering**, **AI Agent**, **RAG**, **AI App**, **Governance & Safety**, **Use Case Bisnis**.
