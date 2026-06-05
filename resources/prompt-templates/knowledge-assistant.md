# Template: Internal Knowledge Assistant (RAG-based)

## System Prompt

```
Anda adalah asisten pengetahuan internal <ORGANISASI>.

Aturan:
- HANYA jawab berdasarkan dokumen yang disertakan di context. Jangan menambah pengetahuan umum.
- Jika informasi tidak ada di dokumen, jawab: "Maaf, informasi tersebut belum tersedia di knowledge base kami."
- SELALU sertakan SUMBER (nama dokumen + bagian/halaman) untuk setiap klaim.
- Format sumber: [Sumber: <nama_dokumen>, bagian <X>].
- Jika dokumen kontradiktif, sebut kontradiksinya dan minta klarifikasi.
- Bahasa Indonesia formal-ramah.
```

## User Message (setelah retrieval)

```
Konteks dokumen yang relevan:
---
[DOC 1: SOP_Cuti_2024.pdf, halaman 3]
<isi chunk 1>

[DOC 2: Panduan_HRIS.docx, bagian "Pengajuan Cuti"]
<isi chunk 2>

[DOC 3: Kebijakan_2024.pdf, halaman 12]
<isi chunk 3>
---

Pertanyaan user: <pertanyaan>

Jawab sesuai aturan di system prompt.
```

## Pola Implementasi Lengkap

```python
from anthropic import Anthropic
from chromadb import Client as ChromaClient

client = Anthropic()
chroma = ChromaClient()
collection = chroma.get_collection("internal_kb")

def answer_with_rag(question: str, top_k: int = 5) -> str:
    # 1. Embed pertanyaan & cari chunk relevan
    results = collection.query(query_texts=[question], n_results=top_k)
    
    # 2. Format context dari chunks
    context_parts = []
    for i, (chunk, meta) in enumerate(zip(results["documents"][0], results["metadatas"][0])):
        context_parts.append(
            f"[DOC {i+1}: {meta['source']}, {meta.get('section', '')}]\n{chunk}"
        )
    context = "\n\n".join(context_parts)
    
    # 3. Panggil Claude
    resp = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": f"Konteks dokumen yang relevan:\n---\n{context}\n---\n\nPertanyaan user: {question}"
        }],
    )
    return resp.content[0].text
```

## Variasi: Multi-turn dengan Memory

Untuk chat berkelanjutan:

```python
def chat_with_rag(history: list[dict], new_question: str):
    # Retrieve berdasarkan pertanyaan baru + 1-2 turn terakhir (untuk context resolution)
    query = " ".join([m["content"] for m in history[-2:]] + [new_question])
    chunks = retrieve(query)
    
    # Sisipkan context ke message terbaru
    history.append({
        "role": "user",
        "content": f"Konteks:\n{format_chunks(chunks)}\n\nPertanyaan: {new_question}"
    })
    
    resp = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=history,
    )
    return resp
```

## Variasi: Hybrid Search (Semantic + Keyword)

Untuk dokumen dengan jargon teknis / nama produk, gabungkan:

1. **Semantic search** (vector) — paham makna
2. **BM25 / keyword** — paham nama persis

Lalu rerank pakai Cross-Encoder atau biarkan Claude memilih chunk paling relevan dari union top-K.

## Anti-Hallucination Checklist

- [ ] System prompt menekankan "HANYA berdasarkan dokumen".
- [ ] Setiap klaim wajib bersumber.
- [ ] Jawaban "tidak tahu" eksplisit ada di system prompt.
- [ ] Logging: simpan question, retrieved chunks, dan answer untuk audit.
- [ ] Validation layer: cek bahwa sumber yang disebut Claude memang ada di context.
- [ ] User testing: 50+ pertanyaan dengan ground truth → ukur faithfulness rate.

## Test Cases

| ID  | Input                                              | Verifikasi                                                   |
| --- | -------------------------------------------------- | ------------------------------------------------------------ |
| TC1 | Pertanyaan yang jawabannya ada di KB               | Jawaban benar + sumber tersedia                              |
| TC2 | Pertanyaan yang TIDAK ada di KB                    | "Belum tersedia" — tidak halusinasi                          |
| TC3 | Pertanyaan ambigu (multi-tafsir)                   | Sebut multiple sumber, atau minta klarifikasi                |
| TC4 | Pertanyaan dengan konflik antar dokumen            | Sebut kontradiksi eksplisit                                  |
| TC5 | Pertanyaan provokatif / prompt injection           | Tetap mengikuti aturan system prompt                         |
| TC6 | Pertanyaan multi-step (perlu reasoning)            | Reasoning step-by-step, sumber tiap step                     |
