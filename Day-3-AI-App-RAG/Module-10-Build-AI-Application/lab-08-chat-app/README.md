# Lab 08 — Chat App dengan Claude

**Modul induk**: Module 10 — Build AI Application
**Durasi**: 90 menit
**Tingkat**: Intermediate

---

## Tujuan

Membangun chat application end-to-end dengan Claude sebagai backend reasoning, mencakup:

- Backend Python (FastAPI) dengan endpoint streaming.
- Frontend minimal (HTML+JS) atau Streamlit alternatif.
- Session management dengan conversation history.
- Streaming response via Server-Sent Events.
- (Bonus) Summarization sliding-window dan session reset.

---

## Prasyarat

- Python 3.11+ dengan virtualenv aktif.
- `ANTHROPIC_API_KEY` di environment variable.
- Paket: `pip install anthropic fastapi uvicorn pydantic`.
- Untuk varian Streamlit: `pip install streamlit`.
- Browser modern (Chrome/Edge/Firefox).
- Editor (VS Code direkomendasikan).

Cek kesiapan:

```bash
python -c "import anthropic, fastapi; print('OK')"
echo $ANTHROPIC_API_KEY | cut -c1-10   # harus muncul prefix key
```

---

## Struktur Direktori Target

```
lab-08-chat-app/
├── README.md             (file ini)
├── backend/
│   ├── main.py           (FastAPI app, harus Anda lengkapi)
│   ├── prompts/system.md (system prompt eksternal)
│   └── requirements.txt
└── frontend/
    └── index.html        (HTML + JS streaming)
```

> Skeleton file disediakan di folder backend/ dan frontend/. Tugas Anda mengisi bagian bertanda `TODO`.

---

## Langkah

1. **Setup proyek**
   - Aktifkan virtualenv, install dependencies.
   - Pastikan API key ter-load: `python -c "import os; assert os.environ['ANTHROPIC_API_KEY']"`.

2. **Implementasi endpoint `POST /chat`**
   - Terima body `{session_id: str, message: str}`.
   - Simpan history di dict in-memory `SESSIONS`.
   - Panggil `client.messages.stream(...)` dengan `claude-sonnet-4-5`.
   - Kembalikan `StreamingResponse` media_type `text/event-stream`.
   - Pastikan menambahkan response assistant ke history setelah stream selesai.

3. **Implementasi frontend**
   - Form input + tombol kirim.
   - Pakai `fetch` dengan `ReadableStream` reader untuk konsumsi SSE.
   - Render token secara incremental ke `<pre>` atau `<div>`.

4. **Tambah endpoint `POST /reset/{session_id}`**
   - Hapus history untuk session_id tersebut.
   - Frontend menampilkan tombol "Reset".

5. **Uji manual**
   - Tanyakan 3 pertanyaan berurutan yang saling merujuk (mis. "Nama saya Andi", "Hobi saya catur", "Apa nama dan hobi saya?").
   - Verifikasi Claude mengingat konteks.
   - Reset, lalu ulang pertanyaan ke-3 — Claude harus tidak tahu.

6. **(Bonus 1) Summarization sliding-window**
   - Implement fungsi `maybe_summarize(history)` yang ringkas 10 turn lama jika total > 20.
   - Gunakan `claude-haiku-4-5` untuk hemat biaya.

7. **(Bonus 2) Cost & latency logging**
   - Log per request: `session_id`, `input_tokens`, `output_tokens`, `latency_ms`.
   - Tampilkan running total cost di console (asumsikan tarif Sonnet 4.5 $3/MTok input, $15/MTok output).

8. **(Bonus 3) Ganti frontend ke Streamlit**
   - Gunakan `st.chat_input` + `st.write_stream`.
   - Bandingkan dev-experience dengan HTML murni.

---

## Kriteria Selesai

Lab dianggap selesai jika:

- [ ] `uvicorn` berjalan tanpa error.
- [ ] Frontend dapat mengirim pesan dan menerima respon streaming token-by-token.
- [ ] Conversation history dipertahankan dalam satu session.
- [ ] Endpoint `/reset` bekerja.
- [ ] API key tidak ter-hardcode (cek dengan `grep -r "sk-ant" .` — harus kosong).
- [ ] (Bonus tercapai untuk peserta dengan latar developer)

---

## Rubrik Penilaian (untuk fasilitator)

| Kriteria | Bobot | Catatan |
|----------|-------|---------|
| Backend streaming jalan | 30% | SSE token tampak di Network tab |
| Session history correct | 25% | Test pertanyaan berurutan lulus |
| Frontend usable | 20% | Tidak freeze, render incremental |
| Security (no hardcoded secret) | 15% | grep clean |
| Bonus features | 10% | Summarization atau logging |

---

## Skeleton Cepat (jika peserta kesulitan setup)

`backend/requirements.txt`:

```
anthropic>=0.40.0
fastapi>=0.110
uvicorn[standard]>=0.27
pydantic>=2.6
```

Jalankan:

```bash
cd backend
uvicorn main:app --reload --port 8000
# di terminal lain:
cd frontend && python -m http.server 5500
# buka http://localhost:5500/index.html
```

> Jika browser blok CORS, tambahkan `CORSMiddleware` di `main.py` dengan `allow_origins=["http://localhost:5500"]`.

---

## Troubleshooting

| Gejala | Kemungkinan penyebab | Fix |
|--------|----------------------|-----|
| Tidak ada token muncul di frontend | Lupa `media_type="text/event-stream"` | Set di `StreamingResponse` |
| `401 Unauthorized` | API key salah / tidak ter-load | Cek `echo $ANTHROPIC_API_KEY` |
| Conversation lupa konteks | History tidak di-append assistant message | Pastikan append setelah `with stream:` selesai |
| CORS error di console | Origin frontend beda port | Tambah `CORSMiddleware` |
| Stream berhenti di tengah | Exception saat append | Bungkus `try/finally` |
