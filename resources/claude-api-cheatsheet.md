# Claude API Cheatsheet

Ringkasan endpoint, parameter, dan pola integrasi Claude API untuk dipegang peserta selama pelatihan.

> Dokumentasi resmi: https://docs.anthropic.com/

---

## 1. Setup Awal

### Python

```bash
pip install anthropic
export ANTHROPIC_API_KEY="sk-ant-..."
```

```python
from anthropic import Anthropic

client = Anthropic()  # otomatis baca env ANTHROPIC_API_KEY

resp = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Halo Claude!"}],
)
print(resp.content[0].text)
```

### JavaScript / TypeScript

```bash
npm install @anthropic-ai/sdk
export ANTHROPIC_API_KEY="sk-ant-..."
```

```ts
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const resp = await client.messages.create({
  model: "claude-sonnet-4-5",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Halo Claude!" }],
});
console.log(resp.content[0].text);
```

---

## 2. Pilihan Model

| Model class               | Model ID                   | Cocok untuk                                              |
| ------------------------- | -------------------------- | -------------------------------------------------------- |
| **Frontier (Opus)**       | `claude-opus-4-7`          | Reasoning kompleks, agen multi-step, riset, analisis dalam |
| **Balanced (Sonnet)**     | `claude-sonnet-4-5`        | Default — produksi, chat, code, document analysis        |
| **Fast (Haiku)**          | `claude-haiku-4-5`         | Klasifikasi, tagging, ringkasan singkat, cost-sensitive  |

**Rule of thumb pemilihan model:**

- **Mulai dengan Sonnet**. Evaluasi.
- Bila task ringan & terstruktur (klasifikasi, ekstraksi sederhana, summarisasi pendek) → **turunkan ke Haiku** untuk hemat cost.
- Bila reasoning multi-hop, perencanaan kompleks, atau analisis dokumen panjang → **naikkan ke Opus**.

---

## 3. Parameter Penting

| Parameter         | Default       | Range              | Catatan                                                |
| ----------------- | ------------- | ------------------ | ------------------------------------------------------ |
| `model`           | —             | (model ID)         | Wajib                                                  |
| `max_tokens`      | —             | 1 – context max    | Wajib. Batas output                                    |
| `messages`        | —             | array              | Wajib. Role alternating: user/assistant                |
| `system`          | none          | string             | Instruksi sistem (persona, constraint global)          |
| `temperature`     | 1.0           | 0.0 – 1.0          | 0 = deterministik, 1 = kreatif                         |
| `top_p`           | (auto)        | 0.0 – 1.0          | Alternative sampling. Pakai salah satu, bukan keduanya |
| `top_k`           | (auto)        | int                | Jarang dipakai                                         |
| `stop_sequences`  | none          | array string       | Hentikan generation pada token tertentu                |
| `stream`          | false         | bool               | Streaming response                                     |
| `tools`           | none          | array              | Untuk function calling / tool use                      |
| `tool_choice`     | auto          | auto/any/tool      | Kontrol perilaku tool                                  |
| `metadata.user_id`| none          | string             | Tracking pengguna (untuk safety)                       |

### Temperature guide

| Use case                                | Temperature |
| --------------------------------------- | ----------- |
| Klasifikasi, ekstraksi, JSON output     | 0.0 – 0.2   |
| Q&A faktual, summarisasi                | 0.2 – 0.5   |
| Chat percakapan natural                 | 0.5 – 0.8   |
| Brainstorming, creative writing         | 0.8 – 1.0   |

---

## 4. Pola Pemanggilan

### 4.1 System prompt + user

```python
resp = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    system="Anda adalah customer service profesional Bank XYZ. Jawab singkat, sopan, bahasa Indonesia formal.",
    messages=[{"role": "user", "content": "Bagaimana cara reset PIN?"}],
)
```

### 4.2 Multi-turn conversation

```python
messages = [
    {"role": "user", "content": "Hai"},
    {"role": "assistant", "content": "Halo! Ada yang bisa saya bantu?"},
    {"role": "user", "content": "Saya mau ringkas dokumen ini."},
]
resp = client.messages.create(model="claude-sonnet-4-5", max_tokens=1024, messages=messages)
```

### 4.3 Streaming

```python
with client.messages.stream(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Tulis cerita pendek tentang AI."}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### 4.4 Tool Use (Function Calling)

```python
tools = [{
    "name": "get_weather",
    "description": "Ambil cuaca terkini di lokasi tertentu.",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "Nama kota"},
            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
        },
        "required": ["location"],
    },
}]

resp = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "Cuaca Jakarta hari ini?"}],
)

# Jika Claude memutuskan memanggil tool:
if resp.stop_reason == "tool_use":
    tool_block = next(b for b in resp.content if b.type == "tool_use")
    # Eksekusi fungsi nyata Anda
    result = call_weather_api(**tool_block.input)
    # Kembalikan hasil ke Claude untuk respons final
    resp = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        tools=tools,
        messages=[
            {"role": "user", "content": "Cuaca Jakarta hari ini?"},
            {"role": "assistant", "content": resp.content},
            {"role": "user", "content": [{
                "type": "tool_result",
                "tool_use_id": tool_block.id,
                "content": str(result),
            }]},
        ],
    )
```

### 4.5 Vision (Image Input)

```python
import base64

with open("invoice.png", "rb") as f:
    img_data = base64.standard_b64encode(f.read()).decode("utf-8")

resp = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {"type": "image", "source": {
                "type": "base64", "media_type": "image/png", "data": img_data,
            }},
            {"type": "text", "text": "Ekstrak field invoice ini sebagai JSON."},
        ],
    }],
)
```

### 4.6 PDF Document Input

```python
import base64

with open("contract.pdf", "rb") as f:
    pdf_data = base64.standard_b64encode(f.read()).decode("utf-8")

resp = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=2048,
    messages=[{
        "role": "user",
        "content": [
            {"type": "document", "source": {
                "type": "base64", "media_type": "application/pdf", "data": pdf_data,
            }},
            {"type": "text", "text": "Ringkas dan ekstrak klausul penalti."},
        ],
    }],
)
```

---

## 5. Prompt Caching (Hemat Cost)

Cache prompt yang sering dipakai kembali (system prompt panjang, dokumen referensi).

```python
resp = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    system=[
        {"type": "text", "text": "Anda adalah asisten hukum..."},
        {"type": "text",
         "text": LONG_REFERENCE_DOCUMENT,
         "cache_control": {"type": "ephemeral"}},
    ],
    messages=[{"role": "user", "content": "Pertanyaan saya..."}],
)
```

- **Minimum cache**: 1024 token (Sonnet/Opus), 2048 token (Haiku).
- **TTL default**: 5 menit (refresh otomatis tiap dipakai).
- **Cost hit**: ~10% dari token write; cache write ~25% lebih mahal sekali.
- **Cek metrics**: `resp.usage.cache_read_input_tokens` / `cache_creation_input_tokens`.

---

## 6. Streaming + Tool Use (Agent Loop)

```python
def run_agent(user_message: str, tools: list, executors: dict, max_iter: int = 10):
    messages = [{"role": "user", "content": user_message}]
    for _ in range(max_iter):
        resp = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2048,
            tools=tools,
            messages=messages,
        )
        if resp.stop_reason == "end_turn":
            return resp
        if resp.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": resp.content})
            tool_results = []
            for block in resp.content:
                if block.type == "tool_use":
                    fn = executors[block.name]
                    out = fn(**block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(out),
                    })
            messages.append({"role": "user", "content": tool_results})
    raise RuntimeError("Max iterations reached")
```

---

## 7. Error Handling

| Exception                              | Penyebab umum                            | Tindakan                              |
| -------------------------------------- | ---------------------------------------- | ------------------------------------- |
| `anthropic.APIConnectionError`         | Koneksi internet                         | Retry dengan exponential backoff      |
| `anthropic.RateLimitError`             | Hit rate limit                           | Backoff lalu retry                    |
| `anthropic.AuthenticationError`        | API key invalid                          | Periksa env var                       |
| `anthropic.BadRequestError`            | Schema salah, token over limit           | Periksa payload                       |
| `anthropic.InternalServerError`        | Server Anthropic                         | Retry dengan backoff                  |
| `anthropic.OverloadedError`            | Server sibuk                             | Backoff & coba model lain             |

Contoh retry dengan tenacity:

```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import anthropic

@retry(
    stop=stop_after_attempt(4),
    wait=wait_exponential(multiplier=1, min=2, max=20),
    retry=retry_if_exception_type((anthropic.RateLimitError, anthropic.OverloadedError, anthropic.APIConnectionError)),
)
def call_claude(**kwargs):
    return client.messages.create(**kwargs)
```

---

## 8. Cost & Usage Tracking

```python
resp = client.messages.create(...)
usage = resp.usage
print(f"Input tokens: {usage.input_tokens}")
print(f"Output tokens: {usage.output_tokens}")
print(f"Cache read: {getattr(usage, 'cache_read_input_tokens', 0)}")
```

Logging ke audit table (recommended):

```python
audit_log.insert({
    "ts": now(),
    "user_id": current_user.id,
    "model": resp.model,
    "input_tokens": usage.input_tokens,
    "output_tokens": usage.output_tokens,
    "stop_reason": resp.stop_reason,
    "request_id": resp.id,
})
```

---

## 9. Best Practices Singkat

- **API key di backend saja** — jangan pernah expose ke frontend.
- **Pakai env var / secret manager**, jangan hardcode.
- **Tetapkan `max_tokens` realistis** — hindari biaya berlebih.
- **Pilih model sesuai task** — Haiku untuk yang ringan.
- **Cache prompt sistem panjang** — hemat token 90%.
- **Stream untuk UX** chat interaktif.
- **Log usage** untuk audit & cost tracking.
- **Retry dengan backoff** untuk rate limit & overload.
- **Validate output** terutama JSON (parse + schema check).
- **Sanitize user input** sebelum masuk prompt (anti prompt injection).
- **Set `metadata.user_id`** untuk safety & billing per user.

## 10. Endpoint Lain

| Endpoint                             | Fungsi                                          |
| ------------------------------------ | ----------------------------------------------- |
| `messages.create`                    | Generate (utama)                                |
| `messages.count_tokens`              | Hitung token tanpa generate                     |
| `messages.batches.create`            | Batch processing (50% diskon, async)            |
| `files.create` / `files.list`        | Upload file untuk dipakai lintas request        |

Lihat https://docs.anthropic.com untuk detail lengkap.
