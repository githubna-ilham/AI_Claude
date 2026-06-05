# Lab 05 — Multi-Step Pipeline

**Modul:** 6 — AI Workflow Automation
**Durasi:** 25–30 menit
**Mode:** Python (atau pseudocode jika non-developer)

---

## Tujuan

Peserta membangun **pipeline 3 langkah** yang merangkai prompt chaining + non-LLM step + error handling, sebagai blueprint workflow produksi.

## Skenario

Tim marketing punya batch customer feedback (1 paragraf bebas per customer). Anda diminta menghasilkan **laporan harian** berisi ringkasan produk yang disebut + sentimen + rekomendasi tindak lanjut.

Pipeline:

1. **Extract** — daftar produk + sentimen dari feedback (LLM, Haiku).
2. **Enrich** — lookup metadata produk dari mock DB (non-LLM, Python dict).
3. **Report** — generate laporan markdown eksekutif (LLM, Sonnet).

## Prasyarat

- Python 3.10+, `pip install anthropic python-dotenv`.
- `.env` berisi `ANTHROPIC_API_KEY=sk-...`.
  - **Reminder keamanan:** jangan commit `.env` ke git. Tambahkan `.env` ke `.gitignore`.
- File `feedback_samples.json` (disiapkan trainer di `assets/`).
- *Paralel JS*: peserta JS bisa pakai `@anthropic-ai/sdk` + `dotenv`. Struktur kode identik.

## Langkah

1. **Setup proyek**
   ```bash
   mkdir lab-05 && cd lab-05
   python -m venv .venv && source .venv/bin/activate
   pip install anthropic python-dotenv
   echo "ANTHROPIC_API_KEY=sk-..." > .env   # ganti dengan key Anda
   echo ".env" >> .gitignore
   ```

2. **Implementasi `step_extract(text)`** — terima string, return dict `{"items": [{"product","sentiment"}]}`. Pakai model Haiku.

3. **Implementasi `step_enrich(extracted)`** — iterasi items, lookup ke `MOCK_DB` Python dict, tambahkan `sku` & `cat`. Jika produk tidak ditemukan → `sku="UNKNOWN"`.

4. **Implementasi `step_report(enriched)`** — terima dict, return string markdown laporan. Pakai model Sonnet, max_tokens 800.

5. **Implementasi orchestrator `run_pipeline(text)`** dengan:
   - Try–except per step.
   - Retry maks 2 kali untuk step LLM jika JSON invalid.
   - Fallback: jika tetap gagal, return `"[FALLBACK] ..."`.
   - Logging: print latency & token usage per step.

6. **Jalankan terhadap minimal 3 feedback sample** (happy + 1 edge case feedback kosong / typo berat).

7. **(Stretch)** Tambahkan paralelisasi: jika ada N feedback, jalankan `step_extract` paralel pakai `concurrent.futures.ThreadPoolExecutor`.

## Skeleton (silakan dikembangkan)

```python
import os, json, time
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()  # otomatis baca ANTHROPIC_API_KEY dari env

MODEL_LIGHT = "claude-haiku-4-5"
MODEL_HEAVY = "claude-sonnet-4-5"

MOCK_DB = {
    "Galaxy A14": {"sku": "SM-A145", "cat": "smartphone"},
    "iPhone 15":  {"sku": "AP-IP15", "cat": "smartphone"},
    "Logitech MX Master": {"sku": "LG-MXM", "cat": "peripheral"},
}

def _call(model, system, user, max_tokens=600):
    t0 = time.time()
    r = client.messages.create(
        model=model, max_tokens=max_tokens, system=system,
        messages=[{"role": "user", "content": user}],
    )
    dt = round((time.time()-t0)*1000)
    print(f"[{model}] {dt}ms in={r.usage.input_tokens} out={r.usage.output_tokens}")
    return r.content[0].text

def step_extract(text: str) -> dict:
    # TODO: implement
    raise NotImplementedError

def step_enrich(extracted: dict) -> dict:
    # TODO: implement
    raise NotImplementedError

def step_report(enriched: dict) -> str:
    # TODO: implement
    raise NotImplementedError

def run_pipeline(text: str) -> str:
    # TODO: retry + fallback + logging
    raise NotImplementedError

if __name__ == "__main__":
    samples = [
        "Galaxy A14 saya cepat panas, tapi kamera oke. iPhone 15 milik istri saya sangat memuaskan.",
        "asdjkasd ???",  # edge case
        "Logitech MX Master nyaman dipakai seharian, recommended!",
    ]
    for s in samples:
        print("="*60); print("INPUT:", s); print("---")
        print(run_pipeline(s))
```

## Kriteria Selesai (Rubrik)

| Aspek | Cukup (1) | Baik (2) | Sangat Baik (3) |
|---|---|---|---|
| 3 step jalan end-to-end | Hanya 1–2 step | 3 step jalan tapi tanpa error handling | 3 step jalan dengan validasi output |
| Error handling | Tidak ada | Try-except generik | Retry + fallback + logging |
| Model mixing | Sonnet untuk semua | Haiku di step ringan | Haiku + Sonnet + alasan jelas |
| Test edge case | Tidak diuji | Diuji 1 edge case | Diuji 2+ edge case |
| Logging | Tidak ada | Print mentah | Latency + token + step name |

**Lulus lab:** minimum total 10/15, dan pipeline bisa demo live tanpa crash.

## Tips

- Untuk step extract, **selalu instruksi "hanya JSON, tanpa prose"** dan beri contoh skema di system prompt.
- Pakai `try/except json.JSONDecodeError` di sekitar `json.loads`.
- Jangan retry tanpa batas — pakai `for attempt in range(2)`.
- Log token usage; berguna untuk estimasi cost di production.

## Stretch Goal

- Tambah step ke-4: kirim laporan ke email (mock function `send_email(...)`).
- Implementasi map-reduce: 100 feedback → ringkas per kelompok 10 → ringkas global.
