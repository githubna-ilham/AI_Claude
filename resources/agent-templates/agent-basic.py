"""
Basic Single Agent — Claude API + tool use.

Pattern: while-loop sampai Claude menjawab tanpa memanggil tool.

Run:
    export ANTHROPIC_API_KEY=sk-ant-...
    pip install anthropic
    python agent-basic.py
"""

from __future__ import annotations
import json
import os
from typing import Any, Callable
from anthropic import Anthropic

client = Anthropic()

MODEL = "claude-sonnet-4-5"
MAX_ITERATIONS = 10


def tool_get_weather(location: str, unit: str = "celsius") -> dict[str, Any]:
    return {
        "location": location,
        "temperature": 31,
        "unit": unit,
        "condition": "cerah berawan",
        "humidity": 78,
    }


def tool_search_kb(query: str, top_k: int = 3) -> list[dict[str, Any]]:
    fake_db = {
        "cuti": [
            {"title": "Hak cuti tahunan", "snippet": "Karyawan tetap mendapat 12 hari cuti per tahun."},
            {"title": "Cuti melahirkan", "snippet": "Cuti melahirkan 3 bulan dengan gaji penuh."},
        ],
        "klaim": [
            {"title": "Klaim medis", "snippet": "Maks 25 juta per tahun untuk rawat inap."},
        ],
    }
    for k, docs in fake_db.items():
        if k in query.lower():
            return docs[:top_k]
    return []


def tool_send_email(to: str, subject: str, body: str) -> dict[str, str]:
    print(f"[SIMULASI KIRIM EMAIL] → {to}\nSubject: {subject}\nBody: {body[:80]}...")
    return {"status": "sent", "message_id": "msg_demo_001"}


TOOLS = [
    {
        "name": "get_weather",
        "description": "Ambil cuaca terkini di lokasi tertentu. Pakai bila user bertanya tentang kondisi cuaca atau suhu.",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "Nama kota atau wilayah"},
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"], "default": "celsius"},
            },
            "required": ["location"],
        },
    },
    {
        "name": "search_knowledge_base",
        "description": "Cari di knowledge base HR internal (cuti, klaim, kebijakan). Pakai bila user bertanya soal kebijakan HR perusahaan.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Kata kunci pencarian"},
                "top_k": {"type": "integer", "default": 3},
            },
            "required": ["query"],
        },
    },
    {
        "name": "send_email",
        "description": "Kirim email. Pakai HANYA bila user eksplisit minta dikirim email dan sudah konfirmasi penerima + isi.",
        "input_schema": {
            "type": "object",
            "properties": {
                "to": {"type": "string"},
                "subject": {"type": "string"},
                "body": {"type": "string"},
            },
            "required": ["to", "subject", "body"],
        },
    },
]

EXECUTORS: dict[str, Callable[..., Any]] = {
    "get_weather": tool_get_weather,
    "search_knowledge_base": tool_search_kb,
    "send_email": tool_send_email,
}

SYSTEM_PROMPT = """Anda adalah asisten internal Multimatics.

Aturan:
- Pakai tool yang tersedia bila pertanyaan butuh data eksternal.
- Untuk send_email: SELALU minta konfirmasi user dulu sebelum eksekusi.
- Jawaban final dalam bahasa Indonesia formal-ramah.
- Jika informasi tidak tersedia di KB, jawab "informasi tersebut belum tersedia".
"""


def run_agent(user_message: str, max_iter: int = MAX_ITERATIONS) -> str:
    messages: list[dict[str, Any]] = [{"role": "user", "content": user_message}]
    for step in range(max_iter):
        resp = client.messages.create(
            model=MODEL,
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=messages,
        )
        if resp.stop_reason == "end_turn":
            for block in resp.content:
                if block.type == "text":
                    return block.text
            return "(tidak ada respons text)"

        if resp.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": resp.content})
            tool_results = []
            for block in resp.content:
                if block.type == "tool_use":
                    fn = EXECUTORS.get(block.name)
                    if fn is None:
                        result = {"error": f"unknown tool: {block.name}"}
                        is_error = True
                    else:
                        try:
                            result = fn(**block.input)
                            is_error = False
                        except Exception as e:
                            result = {"error": str(e)}
                            is_error = True
                    print(f"[step {step}] tool={block.name} input={block.input} → {str(result)[:100]}")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result, ensure_ascii=False),
                        "is_error": is_error,
                    })
            messages.append({"role": "user", "content": tool_results})
        else:
            return f"(stop_reason tak terduga: {resp.stop_reason})"

    raise RuntimeError(f"Max iterations ({max_iter}) reached without end_turn")


if __name__ == "__main__":
    examples = [
        "Cuaca Jakarta hari ini?",
        "Berapa hari cuti tahunan saya?",
        "Tolong cek cuaca Bandung lalu kirim ringkasannya ke andi@example.com",
    ]
    for q in examples:
        print(f"\n=== USER: {q} ===")
        print("AGENT:", run_agent(q))
