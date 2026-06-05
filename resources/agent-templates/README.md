# AI Agent Templates

Koleksi skeleton kode AI Agent berbasis Claude API. Pakai sebagai starting point untuk Capstone atau implementasi internal.

| Template                          | File                                                | Use case                              |
| --------------------------------- | --------------------------------------------------- | ------------------------------------- |
| Basic Single Agent                | [`agent-basic.py`](./agent-basic.py)                | Chat agent dengan tool use            |
| ReAct Agent (Reason + Act)        | [`agent-react.py`](./agent-react.py)                | Multi-step reasoning explicit         |
| Multi-Agent Orchestrator          | [`agent-multi.py`](./agent-multi.py)                | Coordinator + specialist sub-agents   |
| RAG-Enhanced Agent                | [`agent-rag.py`](./agent-rag.py)                    | Agent yang search KB sebelum jawab    |

## Prinsip Umum

1. **Agent loop = while-loop dengan tool dispatch.** Claude memilih tool → Anda eksekusi → kirim hasil kembali → ulangi sampai `stop_reason == "end_turn"`.
2. **Selalu set `max_iterations`** untuk hindari infinite loop.
3. **Tool harus idempotent** atau punya guard against duplicate execution.
4. **Log setiap tool call** untuk debugging & audit.
5. **Validasi input tool** dari Claude — jangan trust mentah (mis. parameter SQL → parameterize).
6. **Cache system prompt** bila panjang (lihat `claude-api-cheatsheet.md`).

## Anatomy Agent Sederhana

```python
def run_agent(user_msg, tools, executors, max_iter=10):
    messages = [{"role": "user", "content": user_msg}]
    for i in range(max_iter):
        resp = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2048,
            tools=tools,
            messages=messages,
        )
        if resp.stop_reason == "end_turn":
            return resp.content[-1].text
        if resp.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": resp.content})
            tool_results = []
            for block in resp.content:
                if block.type == "tool_use":
                    result = executors[block.name](**block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(result),
                    })
            messages.append({"role": "user", "content": tool_results})
    raise RuntimeError(f"Max iterations ({max_iter}) reached")
```

## Tool Definition Pattern

```python
def define_tool(name, description, params_schema):
    return {
        "name": name,
        "description": description,
        "input_schema": {
            "type": "object",
            "properties": params_schema,
            "required": [k for k, v in params_schema.items() if v.get("required")],
        },
    }
```

## Best Practices

- **Tool description = setengah pekerjaan.** Tulis sejelas mungkin kapan tool ini dipakai, kapan tidak.
- **Parameter required eksplisit** — kurangi error parameter hilang.
- **Return error sebagai content `tool_result` dengan `is_error: True`** — Claude bisa coba lagi atau ganti strategi.
- **Stateful tool?** Pertimbangkan session_id untuk isolasi user.
- **Long-running tool?** Return job_id dulu, agent polling pakai tool `check_status`.
