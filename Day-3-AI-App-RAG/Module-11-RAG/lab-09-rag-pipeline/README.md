# Lab 09 — Membangun RAG Pipeline End-to-End

**Modul induk**: Module 11 — RAG
**Durasi**: 60 menit
**Tingkat**: Intermediate

---

## Tujuan

Membangun pipeline RAG lengkap dari nol:

1. Chunking dokumen.
2. Embedding (Voyage AI default, opsi OpenAI atau sentence-transformers).
3. Penyimpanan ke vector DB (Chroma lokal default; pgvector sebagai opsi).
4. Semantic search top-k.
5. Augmented prompt ke Claude dengan sitasi.

Output akhir: script `rag.py` yang dapat menerima pertanyaan dan menjawab berdasar 3 dokumen sample.

---

## Prasyarat

- Lab 08 selesai (atau setidaknya environment Python siap).
- `pip install anthropic chromadb voyageai pypdf python-docx pandas tiktoken`
- (Opsional) `VOYAGE_API_KEY`. Jika tidak ada, gunakan fallback sentence-transformers:
  `pip install sentence-transformers`
- Catatan: **Anthropic tidak punya embedding model sendiri**. Voyage AI direkomendasikan resmi.

---

## Struktur Direktori Target

```
lab-09-rag-pipeline/
├── README.md
├── sample_docs/
│   ├── kebijakan_cuti.pdf
│   ├── sop_pengadaan.docx
│   └── faq_karyawan.csv
├── rag.py                (skeleton + TODO)
├── ingest.py             (skeleton + TODO)
└── chroma_db/            (auto-created)
```

> Sample dokumen disediakan fasilitator di awal lab (bisa dummy berisi 3–5 halaman per file).

---

## Langkah

1. **Pilih embedding backend**
   - Default: `voyage-3` via `voyageai`.
   - Fallback offline: `intfloat/multilingual-e5-large` via `sentence-transformers`.
   - Implement fungsi `embed(texts, input_type)` yang abstraksi pilihan ini.

2. **Implement chunking** di `ingest.py`
   - Strategi recursive 1500 char + 200 overlap.
   - Sertakan metadata: `source` (nama file), `chunk_index`, dan jika memungkinkan `page`.

3. **Loop ingestion** untuk 3 dokumen
   - PDF: `pypdf.PdfReader`, ekstrak per halaman.
   - DOCX: `docx.Document`, gabung paragraf, pisahkan per heading.
   - CSV: `pandas.read_csv`, satu baris = satu chunk dengan teks `f"Q: {row.q}\nA: {row.a}"`.

4. **Simpan ke Chroma**
   - Collection `hr_docs`, distance `cosine`.
   - `upsert` dengan id deterministik (`f"{source}_{chunk_index}"`).

5. **Implement query** di `rag.py`
   - `embed([question], input_type="query")`.
   - `col.query(n_results=5)`.
   - Susun prompt dengan label sumber + halaman.
   - Panggil `claude-sonnet-4-5` dengan system prompt yang melarang hallucination.

6. **Uji minimal 5 pertanyaan**
   - 3 yang ada di dokumen (mis. "Berapa cuti tahunan?").
   - 1 yang ambigu (jawaban di 2 dokumen).
   - 1 yang tidak ada → harus dijawab "tidak ditemukan".

7. **(Bonus 1) Threshold guard**
   - Jika skor distance top-1 > 0.6 (cosine distance), langsung return "tidak ditemukan" tanpa panggil Claude → hemat biaya.

8. **(Bonus 2) Rerank dengan Haiku**
   - Top-10 dari Chroma → rerank top-3 dengan Haiku → kirim ke Sonnet.

9. **(Bonus 3) Logging retrieval**
   - Simpan per query: pertanyaan, top-k chunk id, skor, jawaban, latency.

---

## Kriteria Selesai

- [ ] `python ingest.py` berjalan tanpa error, mengisi `chroma_db/`.
- [ ] `python rag.py "Berapa cuti tahunan?"` menghasilkan jawaban + sitasi.
- [ ] Pertanyaan out-of-scope dijawab "tidak ditemukan".
- [ ] Tidak ada API key hardcoded.
- [ ] (Bonus untuk peserta lanjutan.)

---

## Rubrik

| Kriteria | Bobot |
|----------|-------|
| Ingestion sukses 3 format | 25% |
| Query mengembalikan top-k dengan metadata | 25% |
| Jawaban Claude faithful + sitasi | 25% |
| Penanganan no-answer | 15% |
| Bonus | 10% |

---

## Skeleton `rag.py` (snippet awal)

```python
import os, sys
from anthropic import Anthropic
import chromadb

# TODO: impor embed() dari ingest.py
client = Anthropic()
col = chromadb.PersistentClient(path="./chroma_db").get_collection("hr_docs")

SYSTEM = (
    "Anda asisten HR Multimatics. Jawab HANYA berdasar KONTEKS. "
    "Jika tidak ada, katakan 'Saya tidak menemukan informasi tersebut'. "
    "Sertakan sitasi [Sumber: <file> hal.<n>] di setiap fakta."
)

def answer(question: str, k: int = 5) -> str:
    # TODO: embed query, similarity search, susun context, panggil Claude
    ...

if __name__ == "__main__":
    print(answer(" ".join(sys.argv[1:])))
```

---

## Troubleshooting

| Gejala | Penyebab | Fix |
|--------|----------|-----|
| Voyage `401` | API key tidak ter-set | `export VOYAGE_API_KEY=...` atau pakai fallback ST |
| Chroma `embedding dimension mismatch` | Ganti model tengah jalan | Hapus folder `chroma_db/` dan re-ingest |
| Jawaban mengarang | Tidak ada instruksi anti-hallucination | Perkuat system prompt + threshold |
| Retrieval irrelevant | `input_type` tertukar | Pakai `"document"` di ingestion, `"query"` di search |
| PDF teks kosong | PDF scanned image | Pakai OCR (Tesseract) — di luar scope lab |
