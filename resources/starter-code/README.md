# AI App Starter Code

Skeleton aplikasi AI berbasis Claude untuk dipakai sebagai starting point Capstone Project.

| Starter                          | Stack                                | Use case demo                  |
| -------------------------------- | ------------------------------------ | ------------------------------ |
| Chat App (Python + FastAPI)      | FastAPI + HTML/JS                    | Chat interface dengan streaming |
| Chat App (Node.js + Express)     | Express + HTML/JS                    | Alternatif JS untuk FE-heavy   |
| RAG Q&A (Python + Chroma)        | Streamlit + Chroma + voyage-3        | Internal knowledge assistant    |
| AI Agent CLI (Python)            | Anthropic SDK + Click                | Multi-tool agent dari terminal  |

## Setup Umum

```bash
# Python
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...

# Node.js
npm install
export ANTHROPIC_API_KEY=sk-ant-...
```

## File-file di Folder Ini

> Setiap starter dijabarkan lebih detail di file `materi.md` dan `lab-*/README.md` per Day.
> Folder ini berisi reference implementation yang bisa langsung di-clone.

- `chat-fastapi/` — backend FastAPI + frontend minimal HTML
- `chat-express/` — backend Express + frontend minimal
- `rag-streamlit/` — Streamlit app dengan Chroma + voyage-3
- `agent-cli/` — CLI agent dengan tool calling

## Convention

- API key di **environment variable**, tidak pernah hardcode.
- Validasi input user sebelum masuk prompt.
- Log usage (input_tokens, output_tokens, cost estimate).
- Streaming response untuk UX chat.
- Session ID di header / cookie untuk multi-user.
- Error handling: retry exponential backoff untuk rate limit.

## Security Reminder

- **Jangan expose API key di frontend** — semua call Claude lewat backend.
- **Sanitize user input** — anti prompt injection.
- **Rate limit per user** — anti abuse / cost runaway.
- **Audit log** semua call.
- **PII redaction** sebelum simpan log.

> Catatan: file starter code spesifik (Python/JS lengkap) ditempelkan di folder lab masing-masing Day. Folder ini sebagai index + konvensi.
