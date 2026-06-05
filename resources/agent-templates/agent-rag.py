"""
RAG-Enhanced Agent — Claude API + vector search + tool use.

Pattern:
- Claude memiliki tool `search_knowledge_base` yang mengembalikan chunk relevan dari ChromaDB.
- Agent memutuskan kapan retrieval dipakai.
- Setiap jawaban menyertakan sumber dari chunk yang diretrieve.

Run:
    pip install anthropic chromadb sentence-transformers
    export ANTHROPIC_API_KEY=sk-ant-...
    python agent-rag.py
"""

from __future__ import annotations
import json
import os
from typing import Any
from anthropic import Anthropic
import chromadb
from chromadb.utils import embedding_functions

client = Anthropic()
MODEL = "claude-sonnet-4-5"


# ============================================================
# Setup vector DB (Chroma + sentence-transformers embeddings)
# ============================================================

chroma_client = chromadb.PersistentClient(path="./chroma_demo")
embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
collection = chroma_client.get_or_create_collection(
    name="internal_kb",
    embedding_function=embed_fn,
)


def seed_knowledge_base():
    """Seed contoh dokumen HR. Jalankan sekali."""
    if collection.count() > 0:
        return
    docs = [
        {
            "id": "hr-001",
            "text": "Karyawan tetap mendapat 12 hari cuti tahunan setelah masa kerja 1 tahun. Cuti dapat diajukan via HRIS paling lambat H-3.",
            "metadata": {"source": "SOP_Cuti_2024.pdf", "section": "Cuti Tahunan", "page": 3},
        },
        {
            "id": "hr-002",
            "text": "Cuti melahirkan diberikan 3 bulan dengan gaji penuh. Pengajuan paling lambat 30 hari sebelum HPL.",
            "metadata": {"source": "SOP_Cuti_2024.pdf", "section": "Cuti Melahirkan", "page": 5},
        },
        {
            "id": "hr-003",
            "text": "Klaim medis rawat inap maks Rp 25.000.000 per tahun. Rawat jalan maks Rp 5.000.000 per tahun.",
            "metadata": {"source": "Kebijakan_Benefit_2024.pdf", "section": "Klaim Medis", "page": 12},
        },
        {
            "id": "hr-004",
            "text": "Jam kerja standar 09:00 - 18:00 dengan istirahat 1 jam. Hybrid: 3 hari WFO, 2 hari WFH.",
            "metadata": {"source": "Panduan_HRIS.docx", "section": "Jam Kerja"},
        },
        {
            "id": "hr-005",
            "text": "Reimbursement perjalanan dinas: tiket pesawat ekonomi, hotel maks Rp 1.500.000/malam, taksi/grab dengan bukti.",
            "metadata": {"source": "SOP_Perjalanan_Dinas.pdf", "section": "Reimbursement", "page": 8},
        },
    ]
    collection.add(
        ids=[d["id"] for d in docs],
        documents=[d["text"] for d in docs],
        metadatas=[d["metadata"] for d in docs],
    )


# ============================================================
# Tool: retrieval
# ============================================================

def tool_search_knowledge_base(query: str, top_k: int = 3) -> list[dict[str, Any]]:
    res = collection.query(query_texts=[query], n_results=top_k)
    out = []
    for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
        out.append({
            "text": doc,
            "source": meta.get("source"),
            "section": meta.get("section"),
            "page": meta.get("page"),
            "score": round(1 - dist, 3),
        })
    return out


TOOLS = [
    {
        "name": "search_knowledge_base",
        "description": (
            "Cari informasi di knowledge base HR internal. "
            "Pakai SELALU bila user bertanya tentang kebijakan, prosedur, atau hak karyawan. "
            "JANGAN menjawab pertanyaan HR tanpa memanggil tool ini terlebih dahulu."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Pertanyaan natural language"},
                "top_k": {"type": "integer", "default": 3},
            },
            "required": ["query"],
        },
    },
]

EXECUTORS = {"search_knowledge_base": tool_search_knowledge_base}

SYSTEM_PROMPT = """Anda adalah asisten HR internal Multimatics.

Aturan KETAT:
1. SEMUA pertanyaan HR (cuti, klaim, jam kerja, gaji, reimbursement) WAJIB dijawab berdasarkan hasil tool `search_knowledge_base`.
2. SELALU sertakan sumber dalam format [Sumber: <nama_dokumen>, bagian <X>, halaman <Y>].
3. Bila informasi tidak ditemukan di KB → "Informasi tersebut belum tersedia di knowledge base internal. Silakan hubungi HRBP."
4. JANGAN menebak angka, tanggal, atau nominal yang tidak ada di hasil retrieval.
5. Bahasa Indonesia formal-ramah.
"""


def run_agent(user_message: str, max_iter: int = 5) -> str:
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
            return "(no text)"

        if resp.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": resp.content})
            tool_results = []
            for block in resp.content:
                if block.type == "tool_use":
                    result = EXECUTORS[block.name](**block.input)
                    print(f"[step {step}] retrieved {len(result)} chunks")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result, ensure_ascii=False),
                    })
            messages.append({"role": "user", "content": tool_results})
    raise RuntimeError("max iterations")


if __name__ == "__main__":
    seed_knowledge_base()
    examples = [
        "Berapa hari cuti tahunan saya?",
        "Bagaimana cuti melahirkan diatur?",
        "Apakah perusahaan menanggung biaya rawat jalan?",
        "Berapa gaji direktur?",  # tidak ada di KB
    ]
    for q in examples:
        print(f"\n=== USER: {q} ===")
        print("AGENT:", run_agent(q))
