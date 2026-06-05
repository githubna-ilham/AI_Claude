# Template: Document Summarization

## System Prompt

```
Anda adalah analis yang membuat ringkasan eksekutif yang ringkas dan akurat.

Aturan:
- Hanya gunakan informasi dari dokumen yang diberikan. Jangan menambah fakta dari pengetahuan umum.
- Jika informasi tidak ada di dokumen, tulis "tidak disebutkan di dokumen".
- Pisahkan FAKTA dan OPINI penulis. Tandai opini dengan "(penulis berpendapat: ...)".
- Bahasa Indonesia formal. Tanpa emoji.
```

## User Message (Generic)

```
Audiens ringkasan: <executive / teknis / umum>
Panjang target: <100 / 200 / 500> kata
Fokus topik: <topik utama yang harus muncul, atau "umum">

Dokumen:
"""
<paste dokumen>
"""

Tugas:
1. Ringkasan singkat 1 paragraf.
2. 5 poin utama (bullet).
3. Action items (jika ada di dokumen).
4. Open questions / hal yang perlu diklarifikasi.
```

## Variasi: Long Document (Map-Reduce)

Untuk dokumen panjang > context window, gunakan pola **map-reduce**:

```python
# 1. Chunk dokumen
chunks = split_text(long_doc, chunk_size=8000, overlap=500)

# 2. Map: ringkas tiap chunk
chunk_summaries = []
for chunk in chunks:
    resp = client.messages.create(
        model="claude-haiku-4-5",  # Haiku untuk map (hemat)
        max_tokens=512,
        system="Ringkas chunk berikut dalam 3-5 bullet poin faktual.",
        messages=[{"role": "user", "content": chunk}],
    )
    chunk_summaries.append(resp.content[0].text)

# 3. Reduce: gabungkan jadi ringkasan akhir
final = client.messages.create(
    model="claude-sonnet-4-5",  # Sonnet untuk reduce (kualitas)
    max_tokens=1024,
    system=SYSTEM_PROMPT,
    messages=[{"role": "user", "content": "\n\n".join(chunk_summaries)}],
)
```

## Variasi: Multi-Document Comparison

```
Anda akan menerima 3 dokumen tentang topik <X>. Tugas:
1. Ringkas masing-masing dokumen (1 paragraf).
2. Identifikasi PERSAMAAN antar dokumen.
3. Identifikasi PERBEDAAN penting.
4. Jika ada KONFLIK fakta, tampilkan dalam tabel.

Output format: markdown dengan heading per bagian.
```

## Test Cases

| ID  | Input                                      | Verifikasi                                           |
| --- | ------------------------------------------ | ---------------------------------------------------- |
| TC1 | Notulen rapat 5 halaman                    | Action items terekstrak, deadline disertakan         |
| TC2 | Whitepaper teknis 30 halaman               | Map-reduce, ringkasan tetap konsisten                |
| TC3 | Berita pendek 1 halaman                    | Ringkasan tidak lebih panjang dari sumber            |
| TC4 | Dokumen kontroversial dengan opini kuat    | Opini terpisah dari fakta                            |
| TC5 | Dokumen multi-bahasa (Indonesia + Inggris) | Output konsisten Indonesia                           |
