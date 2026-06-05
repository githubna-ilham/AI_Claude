# Template: Ticket Classification

## System Prompt

```
Anda adalah classifier tiket helpdesk untuk <ORGANISASI>.

Kategori yang valid:
- billing       — pertanyaan/keluhan terkait tagihan, pembayaran, refund
- technical     — error, bug, gangguan layanan
- account       — login, password, profil, verifikasi
- product_info  — pertanyaan fitur, harga, cara pakai
- complaint     — keluhan layanan/SLA/sikap staff
- feedback      — saran, request fitur
- spam          — iklan, promosi tidak relevan

Aturan:
- Pilih TEPAT 1 kategori utama. Jika tumpang tindih, pilih yang paling urgent.
- Output JSON: {"category": "<key>", "confidence": <0.0-1.0>, "reason": "<1 kalimat>"}
- Confidence < 0.6 → mark for human review (tetap output JSON, tambah field "review_needed": true).
- Temperature 0.
```

## Few-shot Examples

```
USER: "Aplikasi crash terus kalau saya buka menu transaksi"
A: {"category": "technical", "confidence": 0.95, "reason": "Eksplisit menyebut crash di fitur tertentu"}

USER: "Saya bayar 3 hari lalu tapi status masih unpaid"
A: {"category": "billing", "confidence": 0.92, "reason": "Pembayaran tidak ter-rekonsiliasi"}

USER: "Kapan ada fitur dark mode?"
A: {"category": "feedback", "confidence": 0.88, "reason": "Permintaan fitur"}

USER: "Halo apa kabar"
A: {"category": "product_info", "confidence": 0.3, "reason": "Pesan sapaan, ambiguous", "review_needed": true}
```

## Usage Python

```python
import json
from anthropic import Anthropic

client = Anthropic()

def classify_ticket(text: str) -> dict:
    resp = client.messages.create(
        model="claude-haiku-4-5",   # cukup pakai Haiku untuk klasifikasi
        max_tokens=200,
        temperature=0,
        system=SYSTEM_PROMPT,
        messages=[
            *FEW_SHOT_EXAMPLES,
            {"role": "user", "content": text},
        ],
    )
    return json.loads(resp.content[0].text)
```

## Variasi: Multi-label

Jika satu tiket bisa punya >1 kategori (mis. billing + complaint):

```
Output: {"categories": ["billing", "complaint"], "primary": "billing", "confidence": 0.85, "reason": "..."}
```

## Evaluation

Siapkan **golden set** minimal 100 tiket berlabel manusia. Evaluasi:

- **Accuracy** keseluruhan
- **Per-class precision & recall** (confusion matrix)
- **Calibration**: apakah confidence 0.9 memang ~90% benar?
- **Review queue rate**: berapa % tiket masuk antrian human review

Iterate prompt berdasarkan kategori dengan recall terendah.

## Test Cases

| ID  | Input                                       | Output yang diharapkan                                   |
| --- | ------------------------------------------- | -------------------------------------------------------- |
| TC1 | Keluhan billing                              | category=billing, conf>0.8                               |
| TC2 | Multi-issue (technical + complaint)         | Multi-label atau primary technical                       |
| TC3 | Bahasa campur ID/EN                         | Tetap klasifikasi benar                                  |
| TC4 | Ambiguous / sapaan                          | conf<0.6, review_needed=true                             |
| TC5 | Iklan / spam                                | category=spam                                            |
| TC6 | Pesan provokasi / SARA                      | Tetap klasifikasi, dan tambah flag escalate (lihat aturan internal) |
