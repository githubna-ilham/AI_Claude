# Lab 06 — Tool Calling

**Modul:** 8 — AI Agent Orchestration
**Durasi:** 25–30 menit
**Mode:** Python

---

## Tujuan

Peserta mengimplementasikan **tool calling loop** dengan Claude API: mendaftarkan 3 tool dummy, menangani `tool_use` → `tool_result` cycle, menguji keputusan model terhadap beragam user query.

## Skenario

Anda membangun asisten internal yang punya 3 kemampuan:
1. `get_weather(city)` — cuaca (mock).
2. `search_database(query)` — cari customer di mock DB.
3. `send_email(to, subject, body)` — kirim email (mock, hanya print).

Anda harus memastikan model **memilih tool yang tepat** dan **tidak memanggil tool yang tidak perlu**.

## Prasyarat

- Python 3.10+, `pip install anthropic python-dotenv`.
- `.env` berisi `ANTHROPIC_API_KEY=sk-...`. **Jangan commit ke git.**
- Sudah membaca materi Modul 8 (tool use cycle).

## Langkah

1. **Setup proyek** seperti Lab-05 (`venv`, install, `.env`, `.gitignore`).

2. **Definisikan 3 tool schema** di list `TOOLS`. Pastikan:
   - `description` jelas, sebut kapan TIDAK dipakai.
   - `input_schema` punya `required` field.
   - `send_email` punya field `to`, `subject`, `body`.

3. **Implementasikan `execute_tool(name, args)`** untuk 3 tool tersebut dengan mock data:
   - `get_weather`: return dict dengan `temp_c`, `condition`.
   - `search_database`: dict customer kecil (3–5 entry).
   - `send_email`: print ke stdout, return `{"status":"sent","id":"mock-123"}`.

4. **Implementasikan `run_agent(user_msg, max_iter=6)`** loop:
   - Call `client.messages.create(model, tools, messages, max_tokens)`.
   - Cek `stop_reason`. Jika `end_turn` → return text.
   - Jika `tool_use`: iterasi content blocks, eksekusi setiap tool_use, kumpulkan tool_results, append ke messages.
   - Handle exception di tool: kirim `is_error=True`.
   - Stop kalau iterasi habis.

5. **Uji minimal 4 user query**:
   - "Cuaca Jakarta hari ini?" (expect: 1 tool call)
   - "Cari customer bernama Budi" (expect: 1 tool call)
   - "Cek cuaca Bandung dan kirim email ringkasan ke admin@toko.id" (expect: 2 tool call)
   - "Apa ibu kota Indonesia?" (expect: tidak ada tool call, jawab langsung)

6. **(Stretch)** Tambahkan logging: print tiap iterasi → tool dipilih, input, output, latency.

7. **(Stretch 2)** Tambahkan tool `give_up(reason)` agar model bisa graceful exit.

## Skeleton

```python
import os, json
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()
MODEL = "claude-sonnet-4-5"

TOOLS = [
    {
        "name": "get_weather",
        "description": "Get current weather for a city. Use ONLY for weather questions.",
        "input_schema": {
            "type":"object",
            "properties":{"city":{"type":"string"}},
            "required":["city"],
        },
    },
    {
        "name": "search_database",
        "description": "Search customer database by name. Use ONLY for customer lookup.",
        "input_schema": {
            "type":"object",
            "properties":{"query":{"type":"string"}},
            "required":["query"],
        },
    },
    {
        "name": "send_email",
        "description": "Send an email. Use ONLY when user explicitly asks to send/email someone.",
        "input_schema": {
            "type":"object",
            "properties":{
                "to":{"type":"string"},
                "subject":{"type":"string"},
                "body":{"type":"string"},
            },
            "required":["to","subject","body"],
        },
    },
]

MOCK_DB = {
    "budi": {"email":"budi@toko.id","tier":"gold"},
    "siti": {"email":"siti@toko.id","tier":"silver"},
}

def execute_tool(name, args):
    if name == "get_weather":
        return {"city":args["city"], "temp_c":31, "condition":"sunny"}
    if name == "search_database":
        return MOCK_DB.get(args["query"].lower(), {"error":"not found"})
    if name == "send_email":
        print(f"[MOCK EMAIL] to={args['to']} subject={args['subject']}")
        return {"status":"sent","id":"mock-001"}
    raise ValueError(f"Unknown tool: {name}")

def run_agent(user_msg: str, max_iter=6) -> str:
    messages = [{"role":"user","content":user_msg}]
    for i in range(max_iter):
        resp = client.messages.create(
            model=MODEL, max_tokens=1024, tools=TOOLS, messages=messages
        )
        print(f"\n--- iter {i} stop={resp.stop_reason} ---")
        if resp.stop_reason == "end_turn":
            return "".join(b.text for b in resp.content if b.type=="text")
        if resp.stop_reason == "tool_use":
            messages.append({"role":"assistant","content":resp.content})
            results = []
            for block in resp.content:
                if block.type == "tool_use":
                    print(f"-> tool={block.name} input={block.input}")
                    try:
                        out = execute_tool(block.name, block.input)
                        results.append({
                            "type":"tool_result",
                            "tool_use_id": block.id,
                            "content": json.dumps(out),
                        })
                    except Exception as e:
                        results.append({
                            "type":"tool_result",
                            "tool_use_id": block.id,
                            "content": str(e),
                            "is_error": True,
                        })
            messages.append({"role":"user","content":results})
    return "[STOP] Max iterations reached."

if __name__ == "__main__":
    queries = [
        "Cuaca Jakarta hari ini?",
        "Cari customer bernama Budi.",
        "Cek cuaca Bandung dan kirim email ringkasan ke admin@toko.id.",
        "Apa ibu kota Indonesia?",
    ]
    for q in queries:
        print("="*60); print("Q:", q)
        print("A:", run_agent(q))
```

## Kriteria Selesai (Rubrik)

| Aspek | Cukup (1) | Baik (2) | Sangat Baik (3) |
|---|---|---|---|
| 3 tool didaftarkan dengan schema valid | Hanya 1–2 | 3 dengan required field | 3 + description tajam (kapan TIDAK dipakai) |
| Loop tool_use → tool_result | Tidak loop | Loop tapi tanpa error handling | Loop + is_error + max_iter |
| 4 query teruji | Hanya 1–2 | 3 query | 4 query semua perilaku sesuai harapan |
| Query non-tool ditangani benar | Model panggil tool tak perlu | Kadang | Model jawab langsung tanpa tool |
| Logging | Tidak ada | Print mentah | Per-iter tool name + input + output |

**Lulus lab:** minimum total 10/15 dan kasus "ibu kota Indonesia" TIDAK memicu tool call.

## Tips

- Kalau model panggil tool tidak perlu, perketat description ("Use ONLY when ...").
- `stop_reason` adalah penentu utama loop — jangan asumsi end_turn.
- Selalu append **list** of tool_result (bukan satu per satu di message terpisah) jika model panggil paralel.
- Untuk debugging, dump `messages` ke file JSON.

## Stretch Goal

- Tambahkan tool ke-4 `give_up(reason)` dan instruksi: "If unsure, call give_up instead of guessing."
- Tambahkan streaming output untuk text final.
