# Speaker Notes — Module 7

**Durasi total:** 90 menit
**Energi audiens:** Sesi setelah lunch — risiko mengantuk. Banyak diskusi & whiteboard, sedikit slide.

## Alokasi Waktu

| Segmen | Menit | Cue |
|---|---|---|
| Hook: "Apa beda chatbot dan agent?" | 5 | Tanya open mic, kumpulkan jawaban, lalu unveil definisi |
| Definisi + tabel komparasi | 15 | Whiteboard. Pancing peserta isi kolom |
| Arsitektur agent (diagram) | 15 | Pakai mermaid dari materi, jelaskan komponen satu per satu |
| Planning & reasoning (ReAct) | 15 | Roleplay: trainer jadi "model", peserta jadi "user" + "tool" |
| Memory concept | 10 | Tunjukkan trade-off: context bloat vs retrieval staleness |
| Whiteboard exercise peserta | 15 | Setiap peserta sketsa agent untuk use case kerjanya |
| Wrap-up + transisi | 15 | Lemparkan ke Modul 8 (orchestration & tool calling) |

## Jawaban Kunci Q&A

1. **Definisi 1 kalimat**: "Agent adalah sistem AI yang diberi goal lalu memilih sendiri rangkaian aksi (call tool, tanya user, jawab) sampai goal tercapai." Hindari kata "AGI" / "otonom penuh".
2. **Use case wajib agent**: task open-ended di mana urutan step tidak bisa diketahui di awal (ex: research multi-source, debugging IT lintas sistem, schedule negotiation). Kalau urutan tetap → workflow.
3. **Risiko & mitigasi**: hallucinated tool call, infinite loop, action destructive. Mitigasi: tool whitelist, max iterations, human-in-the-loop untuk action irreversible, dry-run mode, audit log.
4. **Termination wajib**: tanpa itu = potensi infinite loop, cost runaway, locked thread.
5. **Long-term memory perlu**: lintas sesi (preferensi user, history transaksi). **Short-term cukup**: task one-shot di satu sesi (ringkas dokumen sekali jalan).

## Anekdot

- Cerita agent yang stuck di loop "self-correcting" karena tool returns error vague. Solusi: error message yang lebih informatif + max iterations.
- Cerita agent customer service yang refund $1000 karena tidak ada whitelist tool — pakai untuk highlight bahaya tool tanpa guardrail.

## Common Pitfalls

- **Pitfall 1**: "Saya akan bikin agent" untuk task yang sebenarnya workflow → over-engineering, susah debug.
- **Pitfall 2**: Lupa termination → infinite loop di production.
- **Pitfall 3**: Tools tidak idempotent → retry bikin double action (double email, double charge).
- **Pitfall 4**: Memory disimpan semua di context window → cost meledak setelah 50 turn.
- **Pitfall 5**: Tool error message tidak informatif → model tidak bisa recover sendiri.

## Transisi ke Modul 8

> "Konsep sudah. Sekarang **bagaimana** model bisa benar-benar memilih tool? Lewat fitur tool use di Claude API. Itu yang kita masuki di Modul 8, plus pola single-agent vs multi-agent."
