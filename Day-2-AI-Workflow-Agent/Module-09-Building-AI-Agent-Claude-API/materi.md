# Module 9 — Building AI Agent with Claude API

**Durasi:** 120 menit (capstone Day 2)
**Posisi:** Day 2, sesi penutup
**Prasyarat:** Modul 5–8 (prompt, workflow, agent konsep, tool calling)

---

## Learning Outcomes

Setelah modul ini, peserta mampu:

1. Mengintegrasikan **Claude API** secara aman: autentikasi, env var, retry, timeout, rate limit handling.
2. Mengelola **conversation loop** dengan state (messages, memory, tool use) yang bersih.
3. Membangun **input/output handling** robust: validasi user input, parsing output, streaming.
4. Mendesain **agent interaction flow** lengkap (system prompt + tools + memory + termination).
5. Memahami **deployment basics** untuk agent: secrets, observability, cost guard, scaling pattern.

---

## Konsep Inti

### 1. Claude API Essentials

Endpoint utama: `client.messages.create(...)`.

| Parameter | Penjelasan |
|---|---|
| `model` | `claude-sonnet-4-5`, `claude-haiku-4-5`, dst. |
| `max_tokens` | Cap output. Wajib. |
| `system` | System prompt (string atau list of blocks). |
| `messages` | List of `{role, content}`. role: user/assistant. |
| `tools` | List tool schema (optional). |
| `tool_choice` | `auto`, `any`, `{type:"tool", name}`. |
| `temperature` | 0–1. Lebih rendah = lebih deterministik. |
| `stream` | bool, streaming SSE. |
| `metadata` | `{user_id: "..."}` untuk audit. |

### 2. Autentikasi & API Key Management

- **JANGAN hardcode** `sk-ant-...` di source code.
- Pakai env var: `os.environ["ANTHROPIC_API_KEY"]` atau `.env` + `python-dotenv`.
- Di production: gunakan secret manager (AWS Secrets Manager, GCP Secret Manager, Vault).
- Rotasi key berkala. Beri key per service / environment (dev/stg/prod).
- Untuk multi-user app: gunakan **per-user metadata.user_id** untuk tracking abuse.

```python
# .env
ANTHROPIC_API_KEY=sk-ant-xxxxx
```
```python
# code
from dotenv import load_dotenv
load_dotenv()
client = Anthropic()  # otomatis baca env
```

### 3. Backend Integration Pattern

```mermaid
flowchart LR
    UI[Web/Mobile UI] -->|HTTPS| API[Backend API<br/>FastAPI/Express]
    API --> Auth[Auth & Rate Limit]
    Auth --> Orch[Agent Orchestrator]
    Orch --> Claude[Claude API]
    Orch --> Tools[Internal Tools<br/>DB / 3rd party API]
    Orch --> Mem[Memory Store<br/>Redis / Postgres]
    Claude --> Orch
    Tools --> Orch
    Orch --> API
    API --> UI
    Orch -.logs.-> Obs[Observability<br/>OpenTelemetry / Log]
```

Komponen wajib:
- **Auth layer**: jangan ekspos Anthropic key ke frontend.
- **Rate limit** per user (token bucket).
- **Memory store** untuk multi-turn lintas request.
- **Observability**: log request, token usage, latency, error rate.

### 4. Conversation Loop dengan State

State minimum:
- `messages: list[dict]`
- `session_id: str`
- `user_id: str`
- `iter_count: int`
- `budget_tokens: int` (sisa budget)

Pola:

```python
def turn(session_id, user_input):
    state = load_state(session_id)        # dari Redis/Postgres
    state["messages"].append({"role":"user","content":user_input})
    reply = run_agent_loop(state)
    state["messages"].append({"role":"assistant","content":reply})
    save_state(session_id, state)
    return reply
```

### 5. Input/Output Handling

**Input validation**:
- Panjang max (cegah token bomb).
- Strip / sanitize karakter aneh.
- Deteksi prompt injection sederhana (regex keyword).

**Output handling**:
- Parse JSON dengan try-except.
- Validasi schema (pydantic, zod).
- Streaming: gunakan `client.messages.stream(...)` untuk UX responsif.

### 6. Agent Interaction Flow (Helpdesk IT contoh)

```mermaid
sequenceDiagram
    participant U as User
    participant A as Agent App
    participant C as Claude
    participant KB as KB Tool
    participant TS as Ticket System

    U->>A: "Laptop saya tidak bisa konek VPN"
    A->>C: messages + tools
    C-->>A: tool_use search_kb
    A->>KB: query "VPN connection issue"
    KB-->>A: [3 docs]
    A->>C: tool_result
    C-->>A: text + follow-up question
    A->>U: "Coba langkah 1-2. Berhasil?"
    U->>A: "Masih gagal"
    A->>C: messages
    C-->>A: tool_use create_ticket
    A->>TS: create(category=VPN, priority=P2)
    TS-->>A: {ticket_id: "INC123"}
    A->>C: tool_result
    C-->>A: final text
    A->>U: "Saya buatkan tiket INC123, tim akan follow up <24 jam."
```

### 7. Deployment Basics

| Aspek | Praktik |
|---|---|
| **Hosting** | Docker container di Cloud Run / ECS / VM |
| **Secrets** | Secret manager, bukan env file di disk |
| **Observability** | Structured log JSON; trace per session_id |
| **Cost guard** | Budget cap per user per hari; alert > threshold |
| **Reliability** | Retry dengan backoff (429/5xx); circuit breaker untuk tool |
| **Safety** | Content filter, audit log untuk action irreversible |
| **Versioning** | Pin model version; track perubahan prompt sebagai code |

### 8. Pola Production yang Sering Lupa

- **Idempotency key** untuk action eksternal (kirim email, create ticket).
- **Timeout** di setiap tool call (jangan biarkan hang).
- **Graceful degradation**: kalau Claude down → fallback response.
- **PII redaction** di log.
- **Compliance**: regional data residency, retention policy.

---

## Demo Live (20 menit)

Trainer mendemokan agent **IT Helpdesk** sederhana end-to-end:

1. **Bootstrap proyek**: struktur folder (`agent.py`, `tools.py`, `memory.py`, `.env`).
2. **Definisikan 3 tool**: `search_kb`, `create_ticket`, `escalate_to_human`.
3. **System prompt agent**: role IT helpdesk + policy + format.
4. **Jalankan conversation loop CLI**: input user di terminal → agent reply → loop.
5. **Skenario uji**:
   - User: "Password saya lupa" → agent search KB → jawab dengan langkah reset.
   - User: "Laptop tidak menyala" → agent search KB → kalau buntu, create ticket.
   - User: "Saya butuh akses admin" → escalate ke human (policy: tidak self-serve).
6. **Tunjukkan log**: token usage per turn, latency, tool dipakai.

---

## Contoh Konkret

### Contoh 1 — Minimal Agent App (Python)

```python
# agent.py
import os, json, time
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()
MODEL = "claude-sonnet-4-5"

SYSTEM = """Anda adalah Asisten IT Helpdesk Internal "Multimatics IT".
Kebijakan:
- Selalu cek KB dulu sebelum buat tiket.
- Untuk request akses admin/finance: langsung escalate, jangan self-serve.
- Bahasa: Indonesia, sopan, ringkas.
"""

TOOLS = [
    {"name":"search_kb","description":"Cari di knowledge base IT. Gunakan untuk pertanyaan how-to & troubleshoot umum.",
     "input_schema":{"type":"object","properties":{"query":{"type":"string"}},"required":["query"]}},
    {"name":"create_ticket","description":"Buat tiket helpdesk. Gunakan kalau KB tidak menyelesaikan masalah.",
     "input_schema":{"type":"object","properties":{
         "title":{"type":"string"},"description":{"type":"string"},
         "category":{"type":"string","enum":["ACCESS","HARDWARE","SOFTWARE","NETWORK","OTHER"]},
         "priority":{"type":"string","enum":["P1","P2","P3"]}},
       "required":["title","description","category","priority"]}},
    {"name":"escalate_to_human","description":"Eskalasi ke human agent. Gunakan untuk akses admin/finance atau permintaan sensitif.",
     "input_schema":{"type":"object","properties":{"reason":{"type":"string"}},"required":["reason"]}},
]

# Mock implementations
KB = {
    "vpn": "1) Reconnect VPN. 2) Restart adapter. 3) Cek credential di portal.",
    "password": "Reset di https://reset.multimatics.local",
}
def search_kb(query):
    q = query.lower()
    for k,v in KB.items():
        if k in q: return {"hits":[{"title":k,"content":v}]}
    return {"hits":[]}
def create_ticket(**kw):
    tid = f"INC-{int(time.time())%100000}"
    return {"ticket_id":tid, **kw}
def escalate_to_human(reason):
    return {"status":"escalated","queue":"L2","reason":reason}

def execute_tool(name, args):
    if name=="search_kb": return search_kb(**args)
    if name=="create_ticket": return create_ticket(**args)
    if name=="escalate_to_human": return escalate_to_human(**args)
    raise ValueError(name)

def agent_turn(messages, max_iter=8):
    for _ in range(max_iter):
        r = client.messages.create(
            model=MODEL, max_tokens=1024, system=SYSTEM, tools=TOOLS, messages=messages
        )
        if r.stop_reason == "end_turn":
            text = "".join(b.text for b in r.content if b.type=="text")
            messages.append({"role":"assistant","content":r.content})
            return text, messages
        if r.stop_reason == "tool_use":
            messages.append({"role":"assistant","content":r.content})
            results = []
            for b in r.content:
                if b.type=="tool_use":
                    try: out = execute_tool(b.name, b.input)
                    except Exception as e:
                        results.append({"type":"tool_result","tool_use_id":b.id,
                                        "content":str(e),"is_error":True}); continue
                    results.append({"type":"tool_result","tool_use_id":b.id,
                                    "content":json.dumps(out)})
            messages.append({"role":"user","content":results})
    return "[STOP] Max iter", messages

def main():
    messages = []
    print("IT Helpdesk Agent — ketik 'exit' untuk keluar.\n")
    while True:
        user = input("You: ").strip()
        if user.lower() in ("exit","quit"): break
        messages.append({"role":"user","content":user})
        reply, messages = agent_turn(messages)
        print(f"Agent: {reply}\n")

if __name__ == "__main__":
    main()
```

### Contoh 2 — Wrapper dengan Retry & Budget Guard

```python
import time
from anthropic import APIError, RateLimitError

def safe_create(messages, system, tools, max_retries=3, budget_left=10000):
    if budget_left < 500:
        return {"text":"[Budget exhausted]","stop_reason":"end_turn"}
    for attempt in range(max_retries):
        try:
            return client.messages.create(
                model=MODEL, max_tokens=min(1024, budget_left),
                system=system, tools=tools, messages=messages,
                metadata={"user_id":"u_123"},
            )
        except RateLimitError:
            time.sleep(2 ** attempt)
        except APIError as e:
            if attempt == max_retries-1: raise
            time.sleep(1)
```

> **Paralel JS**: pakai `@anthropic-ai/sdk`, struktur identik. Express/Fastify untuk backend; simpan state di Redis (`ioredis`).

---

## Hands-on Lab

Lanjut ke: [`lab-07-build-agent/`](./lab-07-build-agent/)

Capstone Day 2: bangun mini AI Agent IT Helpdesk dengan 3 tool (`search_kb`, `create_ticket`, `escalate`) dan CLI conversation loop.

---

## Wrap-up & Q&A

1. Sebutkan 3 hal yang TIDAK boleh terjadi di kode agent Anda terkait API key.
2. Apa perbedaan menyimpan state di context window vs di Redis untuk multi-turn?
3. Mengapa idempotency key penting untuk tool `create_ticket`?
4. Apa indikator observability minimal yang harus Anda log per turn?
5. Bagaimana strategi cost-guard sederhana yang bisa Anda terapkan besok?

---

## Bacaan Lanjutan

- Anthropic API Docs: <https://docs.anthropic.com/en/api/messages>
- Anthropic — Streaming: <https://docs.anthropic.com/en/docs/build-with-claude/streaming>
- Anthropic — Errors & rate limits: <https://docs.anthropic.com/en/api/errors>
- Anthropic — Prompt caching: <https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching>
- Anthropic Cookbook — Customer Support Agent example
- Anthropic — Building effective agents: <https://www.anthropic.com/research/building-effective-agents>
