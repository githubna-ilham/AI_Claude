# Template: Information Extraction → JSON

## System Prompt

```
Anda adalah ekstraktor data terstruktur.

Aturan:
- Output HANYA JSON valid, tanpa teks pembuka/penutup, tanpa markdown fence.
- Ikuti schema yang diberikan persis. Jangan tambah field baru.
- Field tidak ditemukan → null (bukan string kosong).
- Tanggal: format ISO 8601 (YYYY-MM-DD).
- Angka uang: number, bukan string (hilangkan separator).
- Jangan menebak. Bila ragu antara 2 nilai, ambil yang muncul lebih dulu.
```

## User Message

```
Schema:
<paste JSON schema atau contoh struktur>

Teks sumber:
"""
<paste teks>
"""

Ekstrak ke JSON sesuai schema.
```

## Contoh Konkret — Ekstrak Invoice

### Schema

```json
{
  "invoice_number": "string",
  "issue_date": "string (YYYY-MM-DD)",
  "due_date": "string (YYYY-MM-DD)",
  "vendor": {
    "name": "string",
    "tax_id": "string|null"
  },
  "buyer": {
    "name": "string",
    "address": "string|null"
  },
  "line_items": [
    {
      "description": "string",
      "qty": "number",
      "unit_price": "number",
      "total": "number"
    }
  ],
  "subtotal": "number",
  "tax": "number",
  "total_due": "number",
  "currency": "string (ISO 4217)"
}
```

### Best Practices

- **Selalu set `temperature=0`** untuk extraction.
- **Validasi schema** di sisi aplikasi (pydantic / zod / JSON Schema).
- **Re-prompt 1x** jika JSON invalid: kirim ulang dengan error message.
- **Caching prompt** untuk schema yang sering dipakai (Day 2 Module 4).
- **Stop sequences**: bisa pakai `["\n}\n"]` untuk pastikan output berakhir bersih.

### Snippet Python

```python
import json
from anthropic import Anthropic
from pydantic import BaseModel, ValidationError

client = Anthropic()

class LineItem(BaseModel):
    description: str
    qty: float
    unit_price: float
    total: float

class Invoice(BaseModel):
    invoice_number: str
    issue_date: str
    # ... dst sesuai schema

def extract_invoice(text: str) -> Invoice:
    resp = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2048,
        temperature=0,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": f"Schema:\n{SCHEMA}\n\nTeks:\n{text}"}],
    )
    data = json.loads(resp.content[0].text)
    return Invoice(**data)  # raises ValidationError if invalid
```

## Test Cases

| ID  | Input                                       | Verifikasi                                              |
| --- | ------------------------------------------- | ------------------------------------------------------- |
| TC1 | Invoice lengkap rapi                        | Semua field terisi, tanggal ISO, angka number           |
| TC2 | Invoice tanpa tax_id vendor                 | `vendor.tax_id = null`                                  |
| TC3 | Invoice dengan diskon line item             | Schema tidak punya diskon → jangan tambah field         |
| TC4 | Teks bukan invoice (mis. email biasa)       | Field utama null, tidak error                           |
| TC5 | Invoice currency campuran (IDR & USD)       | Ambil yang dominan, log ambiguitas                      |
