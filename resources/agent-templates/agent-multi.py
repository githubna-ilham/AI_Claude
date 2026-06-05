"""
Multi-Agent Orchestrator — Coordinator + 2 Specialist sub-agents.

Pattern:
- Coordinator (Sonnet) menerima request, mendelegasikan ke specialist.
- Specialist research (Sonnet) ahli cari informasi.
- Specialist writer (Sonnet) ahli menulis ringkasan.
- Coordinator menggabungkan hasil → respons akhir.

Run:
    pip install anthropic
    export ANTHROPIC_API_KEY=sk-ant-...
    python agent-multi.py
"""

from __future__ import annotations
import json
from anthropic import Anthropic

client = Anthropic()
MODEL_COORDINATOR = "claude-sonnet-4-5"
MODEL_SPECIALIST = "claude-sonnet-4-5"


# ============================================================
# Specialist Agents (jadi tool dari sudut pandang coordinator)
# ============================================================

def specialist_researcher(topic: str) -> str:
    """Sub-agent: mencari informasi tentang topic dari mock KB."""
    mock_kb = {
        "claude": "Claude adalah LLM dari Anthropic. Versi terbaru: Sonnet 4.5, Opus 4.7, Haiku 4.5. Mendukung tool use, vision, document input, prompt caching.",
        "rag": "RAG (Retrieval Augmented Generation) menggabungkan vector search dengan generation. Komponen utama: chunking, embedding, vector store, retrieval, augmentation.",
        "ai agent": "AI Agent: sistem yang menggunakan LLM untuk merencanakan, memilih tool, dan mengeksekusi action menuju tujuan. Berbeda dari chatbot karena multi-step & goal-oriented.",
    }
    facts = []
    for k, v in mock_kb.items():
        if k in topic.lower():
            facts.append(v)
    facts_str = "\n".join(facts) if facts else "(tidak ada informasi spesifik di KB)"
    resp = client.messages.create(
        model=MODEL_SPECIALIST,
        max_tokens=512,
        system="Anda peneliti. Sajikan fakta dari sumber, jangan menambah info baru. Maks 5 poin.",
        messages=[{"role": "user", "content": f"Topic: {topic}\n\nSumber:\n{facts_str}\n\nSajikan 3-5 fakta kunci."}],
    )
    return resp.content[0].text


def specialist_writer(brief: str, facts: str) -> str:
    """Sub-agent: menulis ringkasan untuk audiens executive."""
    resp = client.messages.create(
        model=MODEL_SPECIALIST,
        max_tokens=512,
        system="Anda writer. Tulis ringkasan eksekutif 1 paragraf yang ringkas, jelas, untuk pembaca non-teknis.",
        messages=[{"role": "user", "content": f"Brief: {brief}\n\nFakta dari peneliti:\n{facts}"}],
    )
    return resp.content[0].text


# ============================================================
# Coordinator
# ============================================================

TOOLS = [
    {
        "name": "specialist_researcher",
        "description": "Delegasikan ke peneliti untuk mencari fakta tentang topic tertentu.",
        "input_schema": {
            "type": "object",
            "properties": {"topic": {"type": "string"}},
            "required": ["topic"],
        },
    },
    {
        "name": "specialist_writer",
        "description": "Delegasikan ke writer untuk menulis ringkasan eksekutif berdasar brief + fakta.",
        "input_schema": {
            "type": "object",
            "properties": {
                "brief": {"type": "string"},
                "facts": {"type": "string"},
            },
            "required": ["brief", "facts"],
        },
    },
]

EXECUTORS = {
    "specialist_researcher": specialist_researcher,
    "specialist_writer": specialist_writer,
}

COORDINATOR_SYSTEM = """Anda adalah coordinator agent.

Strategi:
1. Identifikasi pertanyaan/permintaan user.
2. Delegasikan ke specialist_researcher untuk mencari fakta.
3. Delegasikan ke specialist_writer dengan fakta yang diperoleh untuk membuat ringkasan.
4. Sajikan output writer sebagai jawaban final.

Jangan menjawab langsung — selalu lewat specialist.
"""


def run_coordinator(user_message: str, max_iter: int = 8) -> str:
    messages = [{"role": "user", "content": user_message}]
    for step in range(max_iter):
        resp = client.messages.create(
            model=MODEL_COORDINATOR,
            max_tokens=1024,
            system=COORDINATOR_SYSTEM,
            tools=TOOLS,
            messages=messages,
        )
        if resp.stop_reason == "end_turn":
            return next((b.text for b in resp.content if b.type == "text"), "")

        if resp.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": resp.content})
            results = []
            for block in resp.content:
                if block.type == "tool_use":
                    print(f"[coordinator] → delegasi ke {block.name}")
                    out = EXECUTORS[block.name](**block.input)
                    results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": out,
                    })
            messages.append({"role": "user", "content": results})
    raise RuntimeError("max iterations")


if __name__ == "__main__":
    q = "Jelaskan apa itu AI Agent untuk audiens executive non-teknis."
    print(f"=== USER: {q} ===")
    print("FINAL:", run_coordinator(q))
