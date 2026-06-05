# Speaker Notes — Module 9

**Durasi total:** 120 menit (capstone Day 2)
**Energi audiens:** Sesi penutup, lelah tapi excited karena ini "puncak" Day 2. Buat lab sebagai highlight — agent demo nyata.

## Alokasi Waktu

| Segmen | Menit | Cue |
|---|---|---|
| Recap M5–M8 + framing capstone | 10 | "Kita rangkai semuanya jadi satu agent" |
| Claude API essentials + auth & secrets | 15 | Tekankan praktik aman; tunjukkan .env + .gitignore |
| Backend integration pattern | 10 | Whiteboard arsitektur produksi |
| Conversation loop + state | 10 | Pseudocode di slide |
| Input/output handling + streaming | 10 | Demo streaming singkat |
| Demo live mini agent helpdesk | 20 | Live coding berdasarkan Contoh 1 |
| Deployment basics | 10 | Singgung Docker, secrets, observability |
| Lab 07 briefing + kerja capstone | 30 | Trainer keliling, prioritaskan grup tertinggal |
| Wrap-up Day 2 + preview Day 3 | 5 | Tunjuk grup share demo singkat |

## Jawaban Kunci Q&A

1. **Tidak boleh terjadi pada API key**: (a) hardcode di source, (b) commit ke git, (c) ekspos ke frontend / browser, (d) share di chat, (e) pakai key prod di dev tanpa segregasi.
2. **Context vs Redis**: context window cuma 1 request lifecycle, mahal kalau dibawa-bawa; Redis = persistence lintas request + cheap retrieval. Untuk multi-turn lintas waktu → wajib eksternal.
3. **Idempotency `create_ticket`**: kalau retry / network glitch tanpa idempotency key, tiket bisa dibuat dobel. Pakai client-generated UUID per intent.
4. **Observability minimal**: session_id, user_id, model, input_tokens, output_tokens, latency_ms, tool_called, stop_reason, error.
5. **Cost-guard sederhana**: token budget per user per hari (counter Redis), alert kalau > threshold, hard cap di middleware.

## Anekdot

- Cerita: tim launching agent tanpa observability → akhirnya tidak tahu kenapa cost membengkak. Setelah pasang trace → ketahuan satu user trigger 200 tool call/hari karena prompt looping.
- Cerita: key leak via screenshot di Slack publik → key revoked dalam 10 menit oleh Anthropic. Ingatkan rotasi & per-environment key.

## Common Pitfalls

- **Pitfall 1**: simpan messages tanpa batas → context bloat → 503 / cost meledak. Solusi: trim + summarize berkala.
- **Pitfall 2**: tidak handle RateLimitError → user lihat 500 generic.
- **Pitfall 3**: streaming tanpa cleanup connection → resource leak.
- **Pitfall 4**: tool create_ticket tanpa idempotency.
- **Pitfall 5**: log full PII / chat → masalah privacy.
- **Pitfall 6**: tidak pin model version → behavior tiba-tiba berubah saat model update.

## Wrap-up Day 2 (5 menit)

> "Hari ini Anda naik 3 level: prompt produksi → workflow → agent. Lab-07 adalah miniatur sistem produksi nyata. Day 3 kita akan masuk ke **AI App Development** dan **integrasi enterprise**: RAG, fine-tuning approach, MCP, dan pola arsitektur."

Tanya audiens: **1 hal yang paling membekas hari ini** — bikin daftar di whiteboard, gunakan untuk recap Day 3.
