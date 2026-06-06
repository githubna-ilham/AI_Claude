# Pendahuluan, Prerequisite & Persiapan — AI Claude Training

> Dokumen pembuka pelatihan **"Prompt Engineering, AI Agent & AI App Development with Claude"** (4 hari / 40 jam) — Multimatics.
> Wajib dibaca **sebelum Day-1** oleh seluruh peserta & fasilitator.

---

## 1. Pendahuluan

### 1.1 Latar Belakang

Adopsi Large Language Model (LLM) telah bergeser dari sekadar *chatbot* menjadi fondasi otomasi, *knowledge worker augmentation*, dan produk digital generasi baru. **Claude** dari Anthropic adalah salah satu LLM paling matang untuk konteks enterprise — kuat di *reasoning*, *long-context* (200K+ token), *tool use*, dan *responsible AI*.

Namun, sebagian besar organisasi masih berhenti di tahap **"prompt biasa"**. Untuk benar-benar mendapat nilai bisnis, tim teknis harus menguasai *spectrum* yang lebih luas:

```
Prompt Engineering  →  AI Workflow  →  AI Agent  →  AI Application + RAG  →  Governance
```

Pelatihan ini menutup gap tersebut secara end-to-end dalam **4 hari intensif**, dengan komposisi **30% konsep — 60% hands-on — 5% case study — 5% diskusi**.

### 1.2 Tujuan Pembelajaran (Learning Objectives)

Setelah pelatihan, peserta mampu:

1. Memahami konsep dan arsitektur LLM (Claude family, context window, sampling, tokenization).
2. Mendesain prompt yang profesional, terukur, dan *reproducible*.
3. Mengoptimalkan output AI dengan *advanced prompting* (CoT, few-shot, structured output, evals).
4. Menggunakan **Claude API** (Python/JS) untuk pengembangan aplikasi AI.
5. Membangun AI Application end-to-end berbasis Claude.
6. Mengembangkan **AI Agent** untuk otomasi workflow dengan *tool use*.
7. Mengimplementasikan **RAG** (Retrieval Augmented Generation) dengan vector database.
8. Mengintegrasikan AI dengan tools, database, dan API eksternal secara aman.
9. Mendesain AI use case yang sesuai kebutuhan bisnis & ROI yang jelas.
10. Mengembangkan solusi AI yang *scalable* dan *responsible* (governance, risk, security).

### 1.3 Peta Pelatihan

| Hari      | Fokus                                                            | Module       |
| --------- | ---------------------------------------------------------------- | ------------ |
| **Day 1** | Prompt Engineering Fundamentals + Advanced                       | 1–4          |
| **Day 2** | AI Workflow + AI Agent (Concept → Orchestration → Claude API)    | 5–9          |
| **Day 3** | AI App Development + RAG                                         | 10–12        |
| **Day 4** | AI Product Design + Governance + **Capstone Project**            | 13–14 + Cap. |

### 1.4 Target Peserta

- Software Developers (Backend / Frontend / Full-Stack)
- AI / ML Engineers (Beginner – Intermediate)
- Data Analysts / Data Engineers
- Product Managers / Product Owners
- IT Solution Architects / Tech Leads
- Tim Digital Transformation & Innovation Lab

---

## 2. Prerequisite

Bagian ini adalah **syarat minimum** yang harus dipenuhi peserta sebelum hari pertama. Peserta yang belum memenuhi prerequisite tetap bisa ikut, namun perlu effort mandiri lebih untuk mengejar.

### 2.1 Pengetahuan (Knowledge Prerequisite)

| Area                   | Tingkat        | Indikator "siap"                                                   |
| ---------------------- | -------------- | ------------------------------------------------------------------ |
| Konsep AI / LLM        | Awareness      | Pernah pakai ChatGPT/Claude, tahu apa itu *prompt* & *token*       |
| Pemrograman            | Basic          | Bisa baca & tulis fungsi sederhana di **Python** atau **JavaScript** |
| API & HTTP             | Basic          | Paham `GET`/`POST`, JSON, header, status code                      |
| Command line / Terminal | Basic         | Bisa `cd`, `ls`, jalankan script, set environment variable         |
| Git                    | Basic (opsional)| Bisa `clone`, `pull` — cukup untuk ambil materi                    |
| Workflow bisnis        | Awareness      | Paham proses digital di domain kerja masing-masing                 |

> **Tidak perlu:** background ML, statistik lanjut, atau pengalaman training model. Pelatihan ini *application-focused*, bukan *research-focused*.

### 2.2 Hardware Minimum

Detail lengkap di [`REQUIREMENTS-Spek-Komputer-Aplikasi.md`](REQUIREMENTS-Spek-Komputer-Aplikasi.md). Ringkasan:

| Komponen   | Minimum                                            | Direkomendasikan                            |
| ---------- | -------------------------------------------------- | ------------------------------------------- |
| CPU        | Intel i5 gen 8 / Ryzen 5 / Apple M1                | Intel i7 gen 11+ / Ryzen 7 / Apple M2+      |
| RAM        | **8 GB**                                           | **16 GB** (penting untuk Day-3 RAG lab)     |
| Storage    | 20 GB free                                         | 50 GB free SSD                              |
| OS         | Windows 10/11, macOS 12+, Ubuntu 22.04+            | Windows 11, macOS 14+, Ubuntu 24.04         |
| Internet   | WiFi stabil minimal 10 Mbps                        | WiFi 6 + ethernet backup                    |
| Battery    | Min 4 jam (atau pastikan colokan tersedia)         | —                                           |

> ❌ **Tidak didukung:** Tablet, Chromebook, atau perangkat tanpa kemampuan install Python/Node.js & jalankan server lokal.

### 2.3 Akun & Akses

- ✅ Akun **Anthropic Console** — daftar di https://console.anthropic.com
- ✅ **Anthropic API key** — dari fasilitator, atau generate sendiri (top-up minimal **$5** untuk semua lab)
- ✅ Akun **GitHub** (untuk clone materi)
- ✅ Email aktif untuk korespondensi & sertifikat

---

## 3. Persiapan yang Harus Dilakukan

Checklist berikut diurutkan berdasarkan *deadline*. Centang setiap item saat sudah selesai.

### 3.1 H-7 sampai H-3 — Administratif

- [ ] Konfirmasi kehadiran ke fasilitator Multimatics
- [ ] Isi **[Pretest](pretest/PRETEST-AI-Claude.md)** (deadline **H-3**) — hasilnya dipakai fasilitator untuk menyesuaikan kedalaman materi & contoh use case
- [ ] Tentukan **1 use case nyata** dari pekerjaan sendiri yang ingin dibawa ke Capstone Day-4 (misal: otomasi tiket support, RAG SOP internal, dll.)
- [ ] Baca cepat `README.md` repo ini agar paham peta materi

### 3.2 H-3 sampai H-1 — Setup Teknis

#### Step 1 — Install Runtime

```bash
# Python (default)
python --version          # harus >= 3.11

# Node.js (opsional, alternatif JS)
node --version            # harus >= 20
```

Link install:
- Python 3.11+: https://www.python.org/downloads/
- Node.js 20 LTS: https://nodejs.org/

#### Step 2 — Install Editor

Direkomendasikan salah satu:
- **Cursor** — https://cursor.com (AI-native, paling nyaman untuk pelatihan ini)
- **VS Code** — https://code.visualstudio.com + ekstensi: *Python*, *Jupyter*, *Prettier*

#### Step 3 — Clone Repository Materi

```bash
git clone https://github.com/githubna-ilham/AI_Claude.git
cd AI_Claude
```

#### Step 4 — Install Dependencies

**Python:**
```bash
python -m venv .venv
source .venv/bin/activate          # macOS/Linux
# .venv\Scripts\activate           # Windows PowerShell

pip install anthropic chromadb python-dotenv jupyter
```

**Node.js (alternatif):**
```bash
npm install @anthropic-ai/sdk dotenv
```

#### Step 5 — Konfigurasi API Key

Buat file `.env` di root repo:

```env
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

> ⚠️ **Jangan commit `.env` ke git.** Pastikan ada di `.gitignore`.

#### Step 6 — Smoke Test (verifikasi semuanya jalan)

`smoke-test.py`:
```python
import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

resp = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=128,
    messages=[{"role": "user", "content": "Sebut 1 keuntungan utama Claude untuk enterprise dalam 1 kalimat."}],
)
print(resp.content[0].text)
```

```bash
python smoke-test.py
```

✅ Jika sebaris jawaban muncul → setup berhasil.
❌ Jika error → screenshot dan kirim ke fasilitator **sebelum** Day-1.

### 3.3 H-1 — Final Check

- [ ] Laptop ter-charge penuh + bawa charger
- [ ] Mouse eksternal (opsional, membantu)
- [ ] Headset (jika sesi hybrid/online)
- [ ] Kuota internet backup (tethering HP) jika WiFi kelas bermasalah
- [ ] Notebook + pulpen untuk catatan konsep
- [ ] Tutup aplikasi berat yang tidak perlu (Slack, Spotify, dll. boleh, tapi tutup *heavy IDE project* lain)

### 3.4 Day-1 Pagi — Sebelum Sesi Dimulai

- [ ] Hadir 30 menit lebih awal untuk registrasi
- [ ] Konek ke WiFi ruang kelas
- [ ] Verifikasi API key masih aktif (jalankan ulang `smoke-test.py`)
- [ ] Pull versi terbaru repo: `git pull origin main`

---

## 4. Untuk Fasilitator

Checklist tambahan khusus fasilitator (tidak wajib dibaca peserta):

- [ ] Analisis hasil **pretest** → tentukan kedalaman teknis & use case dominan
- [ ] Siapkan **Anthropic Console** dengan budget cukup (~$50 untuk 1 batch demo & hands-on)
- [ ] Siapkan **dummy data**: dokumen SOP, CSV transaksi, sample tiket, kontrak PDF
- [ ] Verifikasi **vector DB lokal** (Chroma docker / pgvector) jalan di mesin demo
- [ ] Cetak handout: *cheatsheet API* & *checklist responsible AI*
- [ ] Setup proyektor, audio, internet ruang kelas, UPS minimal untuk demo
- [ ] Siapkan link backup (Google Drive) jika repo bermasalah
- [ ] Briefing co-fasilitator: pembagian peran demo vs. lab support

---

## 5. Bantuan & Eskalasi

| Masalah                         | Hubungi                                |
| ------------------------------- | -------------------------------------- |
| Pendaftaran & administrasi      | Multimatics — www.multimatics.co.id    |
| Setup teknis (Python/API/dll.)  | Fasilitator via channel komunikasi resmi pelatihan |
| API key tidak jalan             | Fasilitator (cek quota & billing)      |
| Materi & repo                   | Issue di GitHub repo ini               |

---

## 6. Referensi Lanjutan

- [`README.md`](README.md) — overview pelatihan
- [`REQUIREMENTS-Spek-Komputer-Aplikasi.md`](REQUIREMENTS-Spek-Komputer-Aplikasi.md) — detail spek hardware & software
- [`pretest/PRETEST-AI-Claude.md`](pretest/PRETEST-AI-Claude.md) — pretest peserta
- [`resources/claude-api-cheatsheet.md`](resources/claude-api-cheatsheet.md) — cheatsheet Claude API
- [`resources/references.md`](resources/references.md) — bacaan lanjutan
- Dokumentasi resmi Anthropic: https://docs.anthropic.com

---

*Siap belajar? Lanjut ke [Day-1 — Prompt Engineering](Day-1-Prompt-Engineering/README.md).*
