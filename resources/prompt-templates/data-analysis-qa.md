# Template: Data Analysis Q&A (Natural Language → Insight)

## System Prompt

```
Anda adalah analis data yang membantu user memahami dataset melalui pertanyaan natural language.

Aturan:
- HANYA menjawab berdasarkan data yang diberikan. Jangan menebak.
- Jika data tidak cukup, katakan "data tidak menyediakan informasi tersebut".
- Sebut angka SPESIFIK (jumlah, persentase, rentang) saat tersedia.
- Jika user meminta prediksi/rekomendasi, beri DISCLAIMER bahwa ini berdasarkan data historis dan bukan jaminan.
- Format: jawaban → angka pendukung → catatan/limitations.
```

## Pola Implementasi

### Pola 1: Data kecil masuk prompt langsung

```python
import pandas as pd
from anthropic import Anthropic

df = pd.read_csv("sales_q3.csv")
data_str = df.to_markdown(index=False)  # tabel markdown

resp = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    system=SYSTEM_PROMPT,
    messages=[{
        "role": "user",
        "content": f"Dataset:\n{data_str}\n\nPertanyaan: <pertanyaan user>"
    }],
)
```

**Batas**: ~5000 baris (tergantung lebar kolom). Di atas itu, switch ke Pola 2.

### Pola 2: Tool use untuk query SQL/pandas

Claude memilih tool, eksekusi, lalu kembalikan jawaban.

```python
tools = [
    {
        "name": "run_sql",
        "description": "Eksekusi query SQL pada database. Schema tersedia di system prompt.",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    },
    {
        "name": "describe_table",
        "description": "Tampilkan struktur kolom + 5 baris sample.",
        "input_schema": {
            "type": "object",
            "properties": {"table": {"type": "string"}},
            "required": ["table"],
        },
    },
]
```

System prompt tambahan:

```
Anda punya akses tool `run_sql` dan `describe_table`.

Schema database:
- sales(id, date, region, product, qty, revenue)
- customers(id, name, segment, region, joined_at)

Aturan SQL:
- SELECT saja. JANGAN gunakan INSERT, UPDATE, DELETE, DROP.
- Limit hasil max 1000 baris.
- Pakai parameter terikat (anti SQL injection).
```

### Pola 3: Chart generation (Claude generate Vega-Lite spec)

```
Output untuk pertanyaan analitis WAJIB sertakan:
1. Penjelasan singkat (text)
2. Visualisasi sebagai Vega-Lite JSON spec dalam blok ```vega-lite
3. Caveat / limitations
```

## Contoh Q&A

```
USER: "Region mana yang revenue-nya tumbuh tertinggi Q3 vs Q2?"

CLAUDE:
Region Jakarta tumbuh tertinggi: +18.4% (Rp 4.2 M → Rp 4.97 M).
Disusul Surabaya +12.1% dan Medan +8.7%.

Angka:
| Region   | Q2 (Rp)    | Q3 (Rp)    | Growth |
|----------|------------|------------|--------|
| Jakarta  | 4,200,000  | 4,973,000  | +18.4% |
| Surabaya | 3,100,000  | 3,475,000  | +12.1% |
| Medan    | 2,300,000  | 2,500,000  | +8.7%  |

Catatan: Q3 hanya mencakup data Jul-Sep. Data Q4 belum tersedia.
```

## Test Cases

| ID  | Input                                              | Verifikasi                                          |
| --- | -------------------------------------------------- | --------------------------------------------------- |
| TC1 | "Total penjualan bulan ini?"                       | Angka spesifik + currency                           |
| TC2 | "Customer terbaik tahun lalu?"                     | Top-N, pakai metric eksplisit (revenue/order count) |
| TC3 | "Prediksi bulan depan?"                            | Disclaimer "berdasarkan data historis"              |
| TC4 | "Kenapa revenue turun?"                            | Hipotesis dari data + caveat                        |
| TC5 | "Berapa karyawan kita?" (data tidak ada)           | "Data tidak menyediakan informasi tersebut"         |
| TC6 | SQL injection attempt ("'; DROP TABLE...")         | Tolak, gunakan parameter binding                    |
