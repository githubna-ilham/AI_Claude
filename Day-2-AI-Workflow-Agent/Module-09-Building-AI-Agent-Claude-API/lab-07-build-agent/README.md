# Lab 07 — Build AI Agent (Capstone Day 2)

**Modul:** 9 — Building AI Agent with Claude API
**Durasi:** 30–40 menit
**Mode:** Python (capstone)

---

## Tujuan

Bangun **AI Agent end-to-end** untuk **Internal IT Helpdesk** yang mampu:

1. Menjawab FAQ IT (lookup mock knowledge base).
2. Membuat tiket helpdesk ketika KB tidak menyelesaikan masalah.
3. Eskalasi ke human untuk request sensitif (akses admin/finance).
4. Melakukan conversation multi-turn (CLI).

## Skenario

Anda diminta IT Manager Multimatics untuk membangun *IT Buddy*, agent internal yang menangani gelombang pertama tiket IT, mengurangi beban tim L1.

## Prasyarat

- Python 3.10+, `pip install anthropic python-dotenv`.
- `.env` berisi `ANTHROPIC_API_KEY=sk-...`.
  - **Reminder keamanan:** `.env` masuk `.gitignore`. Jangan paste key di Slack/email.
- Sudah selesai Lab 05 & Lab 06.
- *Paralel JS*: peserta JS pakai `@anthropic-ai/sdk` + `readline` untuk CLI.

## Komponen yang Harus Dibangun

1. **System prompt** agent (role + kebijakan + format).
2. **3 Tools** (schema + implementasi mock):
   - `search_kb(query)` → cari KB mock.
   - `create_ticket(title, description, category, priority)` → buat tiket mock.
   - `escalate_to_human(reason)` → eskalasi mock.
3. **Mock data**:
   - KB minimal 5 entry (password reset, VPN, printer, email setup, software request).
   - Ticket store (in-memory dict).
4. **Conversation loop** CLI multi-turn.
5. **Observability minimum**: print per turn → tool dipakai, latency, token usage.
6. **Termination**: max 10 iter per turn; budget token total per session 20.000.

## Langkah

1. **Setup proyek** (`venv`, install, `.env`, `.gitignore`).
2. **Buat `kb.py`**: dict `KB` minimal 5 entry, fungsi `search_kb(query) -> {"hits":[...]}`.
3. **Buat `tools.py`**: definisikan list `TOOLS` schema + dispatcher `execute_tool(name, args)`.
4. **Buat `agent.py`**:
   - Load env, init `Anthropic()`.
   - System prompt detail.
   - Fungsi `agent_turn(messages, budget)` dengan loop tool_use → tool_result.
   - Handle `is_error`, retry untuk `RateLimitError`.
   - Update sisa budget setelah tiap call (dari `usage.input_tokens + output_tokens`).
5. **Main CLI loop**:
   ```
   You: ...
   Agent: ...
   ```
   Stop dengan `exit`. Cetak ringkasan budget di akhir sesi.
6. **Uji minimal 4 skenario percakapan**:
   - **A. Password lupa** — expect: search_kb hit, jawab steps.
   - **B. Laptop mati total** — expect: search_kb miss → create_ticket (HARDWARE, P2).
   - **C. Minta akses admin Active Directory** — expect: escalate_to_human.
   - **D. Multi-turn**: user awalnya tanya general, lalu lanjut spesifik. Pastikan context dipertahankan.
7. **(Stretch 1)** Simpan transcript ke file `sessions/{session_id}.json`.
8. **(Stretch 2)** Tambah tool `get_ticket_status(ticket_id)` untuk follow up.
9. **(Stretch 3)** Implement streaming output dengan `client.messages.stream(...)`.

## Skeleton (silakan dimodifikasi)

```python
# agent.py
import os, json, time, uuid
from dotenv import load_dotenv
from anthropic import Anthropic, RateLimitError

load_dotenv()
client = Anthropic()
MODEL = "claude-sonnet-4-5"

SYSTEM = """Anda adalah "IT Buddy", asisten IT helpdesk internal Multimatics.
Kebijakan:
- SELALU cek KB lebih dulu sebelum membuat tiket.
- Untuk permintaan akses admin/finance/sistem sensitif: panggil escalate_to_human, JANGAN buat tiket biasa.
- Bahasa: Indonesia, profesional, ringkas (maks 4 kalimat per balasan kecuali user minta detail).
- Jangan menebak prosedur. Jika KB tidak cukup, buat tiket dan minta info tambahan.
"""

# --- KB ---
KB = {
    "password": "Reset password di https://reset.multimatics.local. Token dikirim ke email pribadi.",
    "vpn": "1) Hubungkan ulang VPN. 2) Restart adapter. 3) Update client VPN versi >=4.2.",
    "printer": "Pilih Printer-Lt3 di network. Driver di share \\\\fileserver\\drivers.",
    "email setup": "Tambahkan IMAP imap.multimatics.local:993 SSL.",
    "software request": "Ajukan di portal procurement, butuh approval manager.",
}
def search_kb(query: str):
    q = query.lower()
    hits = [{"key":k,"content":v} for k,v in KB.items() if any(w in q for w in k.split())]
    return {"hits": hits}

# --- Tickets ---
TICKETS = {}
def create_ticket(title, description, category, priority):
    tid = f"INC-{uuid.uuid4().hex[:6].upper()}"
    TICKETS[tid] = {"title":title,"description":description,"category":category,"priority":priority,"status":"OPEN"}
    return {"ticket_id":tid, **TICKETS[tid]}

def escalate_to_human(reason: str):
    return {"status":"escalated","queue":"L2","reason":reason,"ref": f"ESC-{uuid.uuid4().hex[:6].upper()}"}

# --- Tools schema ---
TOOLS = [
    {"name":"search_kb","description":"Cari di knowledge base IT. Gunakan untuk pertanyaan how-to & troubleshoot.",
     "input_schema":{"type":"object","properties":{"query":{"type":"string"}},"required":["query"]}},
    {"name":"create_ticket","description":"Buat tiket helpdesk. Hanya setelah KB tidak menyelesaikan.",
     "input_schema":{"type":"object","properties":{
         "title":{"type":"string"},"description":{"type":"string"},
         "category":{"type":"string","enum":["ACCESS","HARDWARE","SOFTWARE","NETWORK","OTHER"]},
         "priority":{"type":"string","enum":["P1","P2","P3"]}},
       "required":["title","description","category","priority"]}},
    {"name":"escalate_to_human","description":"Eskalasi ke human untuk request akses admin/finance/sensitif.",
     "input_schema":{"type":"object","properties":{"reason":{"type":"string"}},"required":["reason"]}},
]

def execute_tool(name, args):
    if name=="search_kb": return search_kb(**args)
    if name=="create_ticket": return create_ticket(**args)
    if name=="escalate_to_human": return escalate_to_human(**args)
    raise ValueError(name)

# --- Agent loop ---
def safe_create(messages, max_retries=3):
    for i in range(max_retries):
        try:
            return client.messages.create(
                model=MODEL, max_tokens=1024, system=SYSTEM, tools=TOOLS, messages=messages
            )
        except RateLimitError:
            time.sleep(2**i)
    raise RuntimeError("rate limited")

def agent_turn(messages, max_iter=10):
    for it in range(max_iter):
        t0 = time.time()
        r = safe_create(messages)
        dt = round((time.time()-t0)*1000)
        print(f"  [iter {it} stop={r.stop_reason} {dt}ms in={r.usage.input_tokens} out={r.usage.output_tokens}]")
        if r.stop_reason == "end_turn":
            text = "".join(b.text for b in r.content if b.type=="text")
            messages.append({"role":"assistant","content":r.content})
            return text, messages, r.usage.input_tokens + r.usage.output_tokens
        if r.stop_reason == "tool_use":
            messages.append({"role":"assistant","content":r.content})
            results = []
            for b in r.content:
                if b.type=="tool_use":
                    print(f"  -> tool={b.name} args={b.input}")
                    try: out = execute_tool(b.name, b.input)
                    except Exception as e:
                        results.append({"type":"tool_result","tool_use_id":b.id,
                                        "content":str(e),"is_error":True}); continue
                    results.append({"type":"tool_result","tool_use_id":b.id,
                                    "content":json.dumps(out)})
            messages.append({"role":"user","content":results})
    return "[Max iter]", messages, 0

def main():
    print("IT Buddy — ketik 'exit' untuk keluar.\n")
    messages = []
    total_tokens = 0
    BUDGET = 20000
    while True:
        user = input("You: ").strip()
        if user.lower() in ("exit","quit"): break
        if total_tokens >= BUDGET:
            print("Agent: [Budget habis untuk sesi ini]"); break
        messages.append({"role":"user","content":user})
        reply, messages, used = agent_turn(messages)
        total_tokens += used
        print(f"Agent: {reply}\n")
    print(f"\n--- Session end. Total tokens: {total_tokens} ---")

if __name__ == "__main__":
    main()
```

## Kriteria Selesai (Rubrik)

| Aspek | Cukup (1) | Baik (2) | Sangat Baik (3) |
|---|---|---|---|
| 3 tool jalan dengan schema valid | 1–2 tool | 3 tool, schema longgar | 3 tool + required + enum + description tajam |
| Conversation multi-turn berfungsi | 1 turn | 2 turn | 3+ turn, context dipertahankan |
| Skenario A & B & C teruji | 1 skenario | 2 skenario | 3 skenario + perilaku benar |
| Skenario eskalasi (C) | Tidak handle | Eskalasi tapi delay | Langsung escalate, tidak buat tiket biasa |
| Observability | Tidak ada | Print tool name | Tool + token + latency per iter |
| Termination & budget | Tidak ada | Hanya max_iter | max_iter + budget token + retry |

**Lulus capstone:** minimum total 13/18 dan dapat demo 3 skenario A/B/C tanpa error.

## Tips

- Untuk eskalasi (skenario C), system prompt harus eksplisit "JANGAN buat tiket biasa, panggil escalate_to_human".
- Kalau model panggil tool berulang untuk pertanyaan sama, perketat description atau tambahkan instruksi "jangan ulangi tool yang sudah di-call dengan argumen sama".
- Gunakan `metadata={"user_id":"..."}` di setiap call untuk audit di Console Anthropic.
- Jangan lupa **idempotency** di production — di lab ini mock cukup pakai UUID.

## Stretch Goal

- Persistensi: simpan TICKETS & transcripts ke `sessions/*.json`.
- Streaming output (`client.messages.stream`).
- Web UI sederhana (FastAPI + simple HTML) — bisa jadi PR Day 3.
- Tambah tool `get_ticket_status` untuk follow-up.

## Demo Check (5 menit terakhir)

Setiap grup demo skenario C (eskalasi) ke trainer. Trainer verifikasi: (a) tool `escalate_to_human` dipanggil, (b) tidak ada `create_ticket` paralel, (c) reply ke user menyebutkan eskalasi.
