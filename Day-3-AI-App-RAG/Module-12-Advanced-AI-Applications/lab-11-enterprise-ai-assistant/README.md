# Lab 11 — Enterprise AI Assistant (HR Q&A)

**Modul induk**: Module 12 — Advanced AI Applications
**Durasi**: 45 menit di kelas + lanjutan mandiri menuju Day 4
**Tingkat**: Advanced (capstone Day 3)

---

## Tujuan

Menggabungkan capaian Lab 08–10 menjadi satu **Enterprise AI Assistant** untuk use case **HR Q&A**, lengkap dengan:

- Chat backend (dari Lab 08).
- RAG terhadap dokumen HR (dari Lab 09/10).
- Tool use minimal (mis. `get_leave_balance(employee_id)` mock).
- **Caching** (prompt caching + result cache).
- **Rate limiting** per user.
- **Cost tracking** per request dan agregat harian.
- **Audit log** terstruktur.

---

## Use Case

**HR Q&A Assistant untuk karyawan Multimatics:**
- "Berapa cuti saya tahun ini?" → tool `get_leave_balance` + summary.
- "Bagaimana proses claim reimbursement?" → RAG ke handbook.
- "Apa kebijakan WFH terbaru?" → RAG ke policy notes.
- Pertanyaan luar topik → respon sopan "di luar cakupan".

---

## Prasyarat

- Lab 08, 09 selesai.
- Lab 10 disarankan (opsional).
- Tambahan: `pip install redis fastapi[all]` (Redis lokal via Docker boleh).

---

## Struktur Direktori Target

```
lab-11-enterprise-ai-assistant/
├── README.md
├── app/
│   ├── main.py               (FastAPI orchestrator, TODO)
│   ├── router.py             (intent classifier, TODO)
│   ├── rag.py                (reuse dari Lab 09)
│   ├── tools.py              (mock HR tools, TODO)
│   ├── cache.py              (Redis result cache, TODO)
│   ├── ratelimit.py          (per-user limiter, TODO)
│   ├── audit.py              (JSONL audit logger, TODO)
│   └── cost.py               (cost tracker, TODO)
├── prompts/
│   └── enterprise_system.md
├── docs/                     (sample HR docs dari Lab 09/10)
└── tests/
    └── golden_qa.jsonl       (10–20 Q&A untuk eval)
```

---

## Checklist Arsitektur (sebelum coding)

- [ ] Sketsa flow di whiteboard: user → API gateway → router → branch (RAG / tool / fallback) → response.
- [ ] Tentukan **3 intent**: `faq`, `leave_balance`, `other`.
- [ ] Tentukan **rate limit**: 20 req/menit per user.
- [ ] Tentukan **cache policy**: prompt caching untuk system + 5-menit Redis TTL untuk answer.
- [ ] Tentukan **audit fields**: `ts, user_id, request_id, intent, model, tokens_in, tokens_out, cached_in, cost_usd, latency_ms, retrieval_ids, response_summary`.

---

## Langkah

1. **Intent router** (`router.py`)
   - Pakai `claude-haiku-4-5` untuk klasifikasi.
   - Output: salah satu dari `faq | leave_balance | other`.

2. **Branch handlers** (`main.py`)
   - `faq` → panggil `rag.answer(question)`.
   - `leave_balance` → panggil `tools.get_leave_balance(user_id)` lalu format jawaban.
   - `other` → polite refusal.

3. **Tool mock** (`tools.py`)
   - `get_leave_balance(employee_id)` return dict static `{"annual": 12, "sick": 5}`.
   - Definisi tool schema untuk Anthropic tool use jika Anda pilih route via Sonnet tool use.

4. **Prompt caching** di system prompt
   - System prompt > 1024 token agar caching aktif.
   - Gunakan `cache_control: ephemeral`.
   - Verifikasi via `usage.cache_read_input_tokens` di response kedua.

5. **Result cache** (`cache.py`)
   - Redis key = SHA256(intent + question + user_role).
   - TTL 600 detik.

6. **Rate limit** (`ratelimit.py`)
   - Sliding window counter di Redis.
   - Return 429 jika exceed.

7. **Audit log** (`audit.py`)
   - Append JSONL ke `audit.jsonl` (production: ganti dengan logging structured ke ELK/CloudWatch).
   - PII redaction sederhana: regex untuk NIK/NIP, email, no HP.

8. **Cost tracker** (`cost.py`)
   - Lihat snippet di materi.md §3.4.
   - Endpoint `GET /admin/cost?day=YYYY-MM-DD` ringkas total.

9. **Endpoint utama** `POST /assist`
   - Input: `{user_id, message}`.
   - Output: `{intent, answer, citations, cost_usd, request_id}`.

10. **Eval ringan**
    - Siapkan `tests/golden_qa.jsonl` 10–20 pasang.
    - Script `python tests/eval.py` jalankan semua, ukur (a) intent accuracy, (b) faithfulness (LLM-as-judge dengan Haiku).

11. **(Bonus) Streaming** ke frontend Lab 08 — gabungkan ke UI yang sudah ada.

12. **(Bonus) Circuit breaker** — jika 3 panggilan Anthropic gagal beruntun dalam 60 detik, return cached/static fallback selama 2 menit.

---

## Kriteria Selesai

- [ ] 3 intent terhandle dengan benar pada golden set.
- [ ] Prompt caching aktif (terlihat di `cache_read_input_tokens > 0` mulai request kedua).
- [ ] Rate limit memberi 429 saat di-stress test sederhana.
- [ ] Audit log terisi dengan field lengkap, tidak ada PII mentah.
- [ ] Cost endpoint mengembalikan agregat harian.
- [ ] Eval script jalan dan menghasilkan ringkasan metrik.

---

## Rubrik

| Kriteria | Bobot |
|----------|-------|
| Integrasi chat + RAG + tool | 25% |
| Caching (prompt + result) berfungsi | 15% |
| Rate limit + audit + cost tracking | 25% |
| Eval golden set + metrik dilaporkan | 15% |
| Kebersihan kode, security (no hardcoded secret) | 10% |
| Bonus (streaming, circuit breaker) | 10% |

---

## Skeleton `main.py`

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time, uuid

from app.router import classify
from app.rag import answer as rag_answer
from app.tools import get_leave_balance
from app.cache import get_cached, set_cached
from app.ratelimit import allow
from app.audit import audit
from app.cost import cost_of

app = FastAPI()

class Req(BaseModel):
    user_id: str
    message: str

@app.post("/assist")
def assist(r: Req):
    if not allow(r.user_id):
        raise HTTPException(429, "Rate limit exceeded")
    rid, t0 = str(uuid.uuid4()), time.time()

    intent = classify(r.message)
    cache_hit = get_cached(intent, r.message, r.user_id)
    if cache_hit:
        audit({"id": rid, "user_id": r.user_id, "intent": intent,
               "cached": True, "latency_ms": int((time.time()-t0)*1000)})
        return {**cache_hit, "request_id": rid, "cached": True}

    if intent == "faq":
        result = rag_answer(r.message)  # returns dict with answer, citations, usage
    elif intent == "leave_balance":
        bal = get_leave_balance(r.user_id)
        result = {"answer": f"Saldo cuti Anda: tahunan {bal['annual']}, sakit {bal['sick']}.",
                  "citations": [], "usage": None, "model": "tool-static"}
    else:
        result = {"answer": "Pertanyaan di luar cakupan asisten HR.",
                  "citations": [], "usage": None, "model": "none"}

    set_cached(intent, r.message, r.user_id, result)
    cost = cost_of(result["usage"], result["model"]) if result["usage"] else 0.0
    audit({"id": rid, "user_id": r.user_id, "intent": intent,
           "cost_usd": cost, "latency_ms": int((time.time()-t0)*1000),
           "model": result["model"]})
    return {**result, "request_id": rid, "cost_usd": cost}
```

---

## Troubleshooting

| Gejala | Penyebab | Fix |
|--------|----------|-----|
| Cache hit selalu 0 | Prefix prompt dinamis | Pindah variabel ke user message |
| Redis connection refused | Tidak running | `docker run -p 6379:6379 redis:7` |
| Intent classifier salah | Prompt terlalu ambigu | Tambah few-shot examples |
| Audit log membengkak | Tidak ada rotation | Pisah per hari `audit-YYYY-MM-DD.jsonl` |
| Cost tidak nol meski cached | Lupa skip Anthropic call saat hit | Return early sebelum panggil Claude |

---

## Hand-off ke Day 4

Hasil Lab 11 menjadi artifact untuk **Day 4: Deployment, Evaluation, Governance**. Persiapkan:
- Repo Git bersih
- Dockerfile (akan dibuat Day 4)
- Daftar metrik yang ingin dipantau di production
