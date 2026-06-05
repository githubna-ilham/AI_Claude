"""
ReAct-style Agent — explicit Reasoning + Acting trace.

Beda dari agent-basic:
- System prompt mendorong Claude untuk menuliskan THOUGHT sebelum memilih tool.
- Berguna untuk task multi-step di mana traceability penting (debug, audit).

Run:
    pip install anthropic
    export ANTHROPIC_API_KEY=sk-ant-...
    python agent-react.py
"""

from __future__ import annotations
import json
from anthropic import Anthropic

client = Anthropic()
MODEL = "claude-sonnet-4-5"


def tool_calculator(expression: str) -> dict:
    try:
        # Hanya operasi aritmatika aman
        allowed = set("0123456789+-*/(). ")
        if not all(c in allowed for c in expression):
            return {"error": "expression contains disallowed characters"}
        return {"result": eval(expression, {"__builtins__": {}}, {})}
    except Exception as e:
        return {"error": str(e)}


def tool_lookup_employee(employee_id: str) -> dict:
    db = {
        "E001": {"name": "Andi", "role": "Engineer", "level": 3, "base_salary": 15_000_000},
        "E002": {"name": "Budi", "role": "Manager", "level": 5, "base_salary": 28_000_000},
        "E003": {"name": "Citra", "role": "Designer", "level": 3, "base_salary": 14_500_000},
    }
    return db.get(employee_id, {"error": "not found"})


def tool_get_bonus_rule(level: int) -> dict:
    rules = {
        1: {"multiplier": 0.5},
        2: {"multiplier": 0.75},
        3: {"multiplier": 1.0},
        4: {"multiplier": 1.25},
        5: {"multiplier": 1.5},
    }
    return rules.get(level, {"error": "level invalid"})


TOOLS = [
    {
        "name": "calculator",
        "description": "Hitung ekspresi aritmatika sederhana (+, -, *, /, parentheses).",
        "input_schema": {
            "type": "object",
            "properties": {"expression": {"type": "string"}},
            "required": ["expression"],
        },
    },
    {
        "name": "lookup_employee",
        "description": "Ambil data karyawan berdasarkan employee_id.",
        "input_schema": {
            "type": "object",
            "properties": {"employee_id": {"type": "string"}},
            "required": ["employee_id"],
        },
    },
    {
        "name": "get_bonus_rule",
        "description": "Ambil multiplier bonus untuk level karyawan tertentu.",
        "input_schema": {
            "type": "object",
            "properties": {"level": {"type": "integer"}},
            "required": ["level"],
        },
    },
]

EXECUTORS = {
    "calculator": tool_calculator,
    "lookup_employee": tool_lookup_employee,
    "get_bonus_rule": tool_get_bonus_rule,
}

SYSTEM_PROMPT = """Anda adalah agent ReAct.

Untuk SETIAP langkah:
1. Tuliskan THOUGHT singkat (1-2 kalimat) yang menjelaskan apa yang ingin Anda lakukan dan kenapa.
2. Bila perlu data, panggil tool yang tepat.
3. Setelah cukup informasi, berikan jawaban final.

Format jawaban akhir:
- THOUGHT: ...
- ANSWER: ...

Jangan menebak nilai. Selalu pakai tool untuk data riil.
"""


def run_agent(user_message: str, max_iter: int = 10) -> str:
    messages = [{"role": "user", "content": user_message}]
    for step in range(max_iter):
        resp = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )
        print(f"\n--- step {step} (stop_reason={resp.stop_reason}) ---")
        for block in resp.content:
            if block.type == "text":
                print(block.text)
            elif block.type == "tool_use":
                print(f"[TOOL CALL] {block.name}({block.input})")

        if resp.stop_reason == "end_turn":
            return next((b.text for b in resp.content if b.type == "text"), "")

        if resp.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": resp.content})
            results = []
            for block in resp.content:
                if block.type == "tool_use":
                    out = EXECUTORS[block.name](**block.input)
                    print(f"[TOOL RESULT] {out}")
                    results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(out),
                    })
            messages.append({"role": "user", "content": results})
    raise RuntimeError("max iterations")


if __name__ == "__main__":
    q = "Hitung bonus tahunan karyawan E002 jika bonus = base_salary x multiplier level dia."
    print(f"=== USER: {q} ===")
    answer = run_agent(q)
    print("\n=== FINAL ANSWER ===")
    print(answer)
