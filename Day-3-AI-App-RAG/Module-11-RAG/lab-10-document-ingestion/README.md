# Lab 10 — Document Ingestion Pipeline

**Modul induk**: Module 11 — RAG
**Durasi**: 45 menit
**Tingkat**: Intermediate (jalur paralel untuk peserta lanjutan setelah Lab 09)

---

## Tujuan

Membangun pipeline ingestion yang **robust** untuk dokumen heterogen:

- Ekstraksi teks dari PDF, DOCX, dan CSV.
- Dua strategi chunking: **fixed-size** dan **semantic**.
- **Metadata enrichment**: source, page, section, date, author, doc_type.
- Output siap dikirim ke vector store (lab 09).

---

## Prasyarat

- Selesaikan Lab 09 (atau setidaknya environment siap).
- `pip install pypdf python-docx pandas tiktoken anthropic`
- (Opsional, untuk semantic chunking) `pip install sentence-transformers numpy`

---

## Struktur Direktori Target

```
lab-10-document-ingestion/
├── README.md
├── sample_docs/
│   ├── handbook_karyawan.pdf
│   ├── kontrak_template.docx
│   ├── product_catalog.csv
│   └── policy_notes.txt
├── extractors/
│   ├── pdf.py            (TODO)
│   ├── docx.py           (TODO)
│   ├── csv.py            (TODO)
│   └── txt.py            (TODO)
├── chunkers/
│   ├── fixed.py          (TODO)
│   └── semantic.py       (TODO)
└── ingest.py             (orchestrator, TODO)
```

---

## Langkah

1. **Extraction layer**
   - `extractors/pdf.py`: gunakan `pypdf.PdfReader`, return list `{text, page}`.
   - `extractors/docx.py`: gunakan `python-docx`, group by heading (level 1 & 2) → return list `{text, section}`.
   - `extractors/csv.py`: setiap baris jadi unit, gunakan `pandas`. Format teks: gabungkan kolom string yang relevan.
   - `extractors/txt.py`: read full + split by `\n\n`.

2. **Chunking layer**
   - `chunkers/fixed.py`: token-based via `tiktoken`, target 500 token, overlap 50.
   - `chunkers/semantic.py`: split per kalimat, hitung embedding antar kalimat, gabungkan saat similarity > threshold (mis. 0.75); pecah saat drop signifikan.

3. **Metadata enrichment**
   - Wajib: `source`, `doc_type`, `chunk_index`, `ingested_at`.
   - Opsional sesuai sumber: `page`, `section`, `row_id`, `author`, `date`, `confidentiality`.
   - Inject **header context** di awal teks chunk: `f"[{source} | {section}]\n{chunk}"` agar embedding tetap kaya konteks.

4. **Orchestrator `ingest.py`**
   - Argumen CLI: `--input-dir`, `--strategy fixed|semantic`, `--out manifest.jsonl`.
   - Loop semua file → pilih extractor by ekstensi → chunk → enrich → tulis manifest JSONL.
   - Manifest entry: `{id, text, metadata}`.

5. **Bandingkan dua strategi**
   - Jalankan dengan `--strategy fixed` dan `--strategy semantic`.
   - Hitung: jumlah chunk, rata-rata panjang, distribusi.
   - Diskusikan: strategi mana lebih cocok untuk dokumen mana?

6. **(Bonus 1) Tabel-aware extraction**
   - Untuk PDF dengan tabel, gunakan `pdfplumber` (`pip install pdfplumber`).
   - Konversi tabel ke Markdown.

7. **(Bonus 2) Deduplication**
   - Hash MD5 dari teks chunk. Skip jika sudah ada.

8. **(Bonus 3) Quality check**
   - Reject chunk dengan < 50 karakter alfabet.
   - Reject chunk yang >80% angka (kemungkinan noise CSV).

---

## Kriteria Selesai

- [ ] Tiga format (PDF/DOCX/CSV) ter-ekstrak ke teks bersih.
- [ ] Dua strategi chunking menghasilkan manifest yang valid.
- [ ] Metadata lengkap untuk semua entry.
- [ ] Output `manifest.jsonl` siap di-feed ke `ingest.py` Lab 09.
- [ ] Peserta dapat menjelaskan kapan pilih fixed vs semantic.

---

## Rubrik

| Kriteria | Bobot |
|----------|-------|
| Extraction multi-format jalan | 30% |
| Chunking dua strategi | 25% |
| Metadata kaya & konsisten | 25% |
| Orchestrator CLI rapi | 10% |
| Bonus | 10% |

---

## Skeleton `ingest.py`

```python
import argparse, json, hashlib, datetime, pathlib

EXTRACTORS = {
    ".pdf":  "extractors.pdf:extract",
    ".docx": "extractors.docx:extract",
    ".csv":  "extractors.csv:extract",
    ".txt":  "extractors.txt:extract",
}

def dispatch(path: pathlib.Path):
    # TODO: resolve extractor dinamis, return list[{text, meta_extra}]
    ...

def chunk(text: str, strategy: str) -> list[str]:
    if strategy == "fixed":
        from chunkers.fixed import chunk_fixed; return chunk_fixed(text)
    if strategy == "semantic":
        from chunkers.semantic import chunk_semantic; return chunk_semantic(text)
    raise ValueError(strategy)

def make_id(source: str, i: int) -> str:
    return hashlib.md5(f"{source}_{i}".encode()).hexdigest()[:16]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input-dir", required=True)
    p.add_argument("--strategy", choices=["fixed","semantic"], default="fixed")
    p.add_argument("--out", default="manifest.jsonl")
    args = p.parse_args()
    now = datetime.datetime.utcnow().isoformat()
    with open(args.out, "w") as f:
        for path in pathlib.Path(args.input_dir).glob("*"):
            for unit in dispatch(path):
                for i, c in enumerate(chunk(unit["text"], args.strategy)):
                    rec = {
                        "id": make_id(path.name, i),
                        "text": f"[{path.name}]\n{c}",
                        "metadata": {
                            "source": path.name,
                            "doc_type": path.suffix.lstrip("."),
                            "chunk_index": i,
                            "ingested_at": now,
                            **{k:v for k,v in unit.items() if k != "text"},
                        }
                    }
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    main()
```

---

## Troubleshooting

| Gejala | Penyebab | Fix |
|--------|----------|-----|
| `pypdf` ekstraksi kosong | PDF scanned | OCR (Tesseract) — di luar scope |
| Heading DOCX tidak ke-detect | Style "Normal" dipakai untuk semua | Inspeksi `paragraph.style.name` |
| Chunk overlap menyebabkan duplikasi | Tidak ada dedup | Bonus 2 |
| Encoding error CSV | BOM / encoding aneh | `pandas.read_csv(..., encoding="utf-8-sig")` |
| Manifest sangat besar | Chunk terlalu kecil | Naikkan target ke 500–800 token |
