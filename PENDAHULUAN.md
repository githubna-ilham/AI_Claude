# Pendahuluan, Prerequisite & Persiapan — AI Claude Training

> Dokumen pembuka pelatihan **"Prompt Engineering, AI Agent & AI App Development with Claude"** (4 hari / 40 jam) — Multimatics.
> Wajib Anda baca **sebelum Day-1** dimulai.

---

## 1. Pendahuluan

### 1.1 Latar Belakang

Adopsi Large Language Model (LLM) telah bergeser dari sekadar *chatbot* menjadi fondasi otomasi, *knowledge worker augmentation*, dan produk digital generasi baru. **Claude** dari Anthropic merupakan salah satu LLM paling matang untuk konteks enterprise — unggul dalam *reasoning*, *long-context* (200K+ token), *tool use*, dan *responsible AI*.

Namun demikian, sebagian besar organisasi masih berhenti pada tahap **"prompt biasa"**. Untuk benar-benar memperoleh nilai bisnis, tim teknis perlu menguasai spektrum yang lebih luas:

```
Prompt Engineering  →  AI Workflow  →  AI Agent  →  AI Application + RAG  →  Governance
```

Pelatihan ini dirancang untuk menutup gap tersebut secara end-to-end dalam **4 hari intensif**, dengan komposisi **30% konsep — 60% hands-on — 5% case study — 5% diskusi**.

### 1.2 Tujuan Pembelajaran

Setelah menyelesaikan pelatihan ini, Anda akan mampu:

1. Memahami konsep dan arsitektur LLM (Claude family, context window, sampling, tokenization).
2. Mendesain prompt yang profesional, terukur, dan *reproducible*.
3. Mengoptimalkan output AI menggunakan *advanced prompting* (CoT, few-shot, structured output, evals).
4. Menggunakan **Claude API** (Python/JS) untuk pengembangan aplikasi AI.
5. Membangun AI Application end-to-end berbasis Claude.
6. Mengembangkan **AI Agent** untuk otomasi workflow dengan *tool use*.
7. Mengimplementasikan **RAG** (Retrieval Augmented Generation) menggunakan vector database.
8. Mengintegrasikan AI dengan tools, database, dan API eksternal secara aman.
9. Mendesain AI use case yang sesuai kebutuhan bisnis dengan ROI yang jelas.
10. Mengembangkan solusi AI yang *scalable* dan *responsible* (governance, risk, security).

### 1.3 Peta Pelatihan

| Hari      | Fokus                                                            | Module       |
| --------- | ---------------------------------------------------------------- | ------------ |
| **Day 1** | Prompt Engineering Fundamentals + Advanced                       | 1–4          |
| **Day 2** | AI Workflow + AI Agent (Concept → Orchestration → Claude API)    | 5–9          |
| **Day 3** | AI App Development + RAG                                         | 10–12        |
| **Day 4** | AI Product Design + Governance + **Capstone Project**            | 13–14 + Cap. |

### 1.4 Untuk Siapa Pelatihan Ini

Pelatihan ini dirancang untuk Anda yang berperan sebagai:

- Software Developer (Backend / Frontend / Full-Stack)
- AI / ML Engineer (Beginner – Intermediate)
- Data Analyst / Data Engineer
- Product Manager / Product Owner
- IT Solution Architect / Tech Lead
- Anggota tim Digital Transformation atau Innovation Lab

---

## 2. Prerequisite

Bagian ini berisi **syarat minimum** yang sebaiknya Anda penuhi sebelum hari pertama. Jika Anda belum memenuhi seluruhnya, Anda tetap dapat mengikuti pelatihan — namun perlu usaha mandiri lebih untuk mengejar materi.

### 2.1 Pengetahuan yang Diperlukan

| Area                   | Tingkat        | Indikator "siap"                                                   |
| ---------------------- | -------------- | ------------------------------------------------------------------ |
| Konsep AI / LLM        | Awareness      | Pernah menggunakan ChatGPT/Claude, memahami istilah *prompt* dan *token* |
| Pemrograman            | Basic          | Mampu membaca dan menulis fungsi sederhana di **Python** atau **JavaScript** |
| API & HTTP             | Basic          | Memahami `GET`/`POST`, JSON, header, status code                   |
| Command line / Terminal | Basic         | Mampu menjalankan `cd`, `ls`, eksekusi script, dan setting environment variable |
| Git                    | Basic (opsional)| Mampu menjalankan `clone`, `pull` — cukup untuk mengambil materi |
| Workflow bisnis        | Awareness      | Memahami proses digital di domain pekerjaan Anda                    |

> **Anda tidak perlu**: latar belakang ML, statistik lanjut, atau pengalaman *training* model. Pelatihan ini berfokus pada *application*, bukan *research*.

### 2.2 Hardware Minimum

Detail lengkap tersedia di [`REQUIREMENTS-Spek-Komputer-Aplikasi.md`](REQUIREMENTS-Spek-Komputer-Aplikasi.md). Ringkasan:

| Komponen   | Minimum                                            | Direkomendasikan                            |
| ---------- | -------------------------------------------------- | ------------------------------------------- |
| CPU        | Intel i5 gen 8 / Ryzen 5 / Apple M1                | Intel i7 gen 11+ / Ryzen 7 / Apple M2+      |
| RAM        | **8 GB**                                           | **16 GB** (penting untuk Day-3 RAG lab)     |
| Storage    | 20 GB free                                         | 50 GB free SSD                              |
| OS         | Windows 10/11, macOS 12+, Ubuntu 22.04+            | Windows 11, macOS 14+, Ubuntu 24.04         |
| Internet   | WiFi stabil minimal 10 Mbps                        | WiFi 6 + ethernet backup                    |
| Battery    | Minimal 4 jam (atau pastikan colokan tersedia)     | —                                           |

> ❌ **Tidak didukung**: Tablet, Chromebook, atau perangkat yang tidak mampu menginstal Python/Node.js dan menjalankan server lokal.

### 2.3 Akun & Akses

- ✅ Akun **Anthropic Console** — daftar di https://console.anthropic.com
- ✅ **Anthropic API key** — disediakan oleh fasilitator, atau generate sendiri (top-up minimal **$5** untuk seluruh lab)
- ✅ Akun **GitHub** (untuk meng-clone materi)
- ✅ Email aktif untuk korespondensi dan sertifikat

---

## 3. Persiapan yang Perlu Anda Lakukan

Checklist berikut diurutkan berdasarkan *deadline*. Centang setiap item ketika sudah Anda selesaikan.

### 3.1 H-7 sampai H-3 — Administratif

- [ ] Konfirmasi kehadiran Anda kepada penyelenggara
- [ ] Isi **[Pretest](pretest/PRETEST-AI-Claude.md)** dengan *deadline* **H-3**. Jawaban Anda akan digunakan untuk menyesuaikan kedalaman materi dan pilihan use case selama pelatihan.
- [ ] Tentukan **satu use case nyata** dari pekerjaan Anda yang ingin dibawa ke Capstone Day-4 (misalnya: otomasi tiket support, RAG dokumen SOP internal, dan sebagainya)
- [ ] Baca cepat `README.md` repo ini untuk memahami peta materi keseluruhan

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

Anda direkomendasikan menggunakan salah satu dari:
- **Cursor** — https://cursor.com (AI-native, paling nyaman untuk pelatihan ini)
- **VS Code** — https://code.visualstudio.com beserta ekstensi: *Python*, *Jupyter*, *Prettier*

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

> ⚠️ **Jangan commit file `.env` ke git.** Pastikan file ini tercantum di `.gitignore`.

#### Step 6 — Smoke Test (verifikasi seluruh setup berjalan)

Buat file `smoke-test.py`:
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

Jalankan:
```bash
python smoke-test.py
```

✅ Jika sebaris jawaban berhasil muncul → setup Anda sudah berhasil.
❌ Jika muncul error → simpan screenshot dan hubungi penyelenggara **sebelum** Day-1 dimulai.

### 3.3 H-1 — Pengecekan Akhir

- [ ] Laptop terisi penuh, jangan lupa membawa charger
- [ ] Mouse eksternal (opsional, namun membantu kenyamanan)
- [ ] Headset (jika Anda mengikuti sesi hybrid atau online)
- [ ] Kuota internet cadangan (tethering dari ponsel) untuk berjaga-jaga jika WiFi bermasalah
- [ ] Buku catatan dan pulpen untuk mencatat konsep
- [ ] Tutup aplikasi berat yang tidak diperlukan (Slack, Spotify masih boleh; namun proyek IDE yang berat sebaiknya ditutup)

### 3.4 Day-1 Pagi — Sebelum Sesi Dimulai

- [ ] Datang 30 menit lebih awal untuk registrasi
- [ ] Sambungkan laptop ke WiFi ruang kelas
- [ ] Verifikasi API key masih aktif (jalankan ulang `smoke-test.py`)
- [ ] Tarik versi terbaru repo: `git pull origin main`

---

## 4. Bantuan & Eskalasi

Jika Anda mengalami kendala, gunakan tabel berikut untuk menentukan saluran yang tepat:

| Masalah                         | Hubungi                                |
| ------------------------------- | -------------------------------------- |
| Pendaftaran & administrasi      | Multimatics — www.multimatics.co.id    |
| Setup teknis (Python/API/dll.)  | Penyelenggara via channel komunikasi resmi pelatihan |
| API key tidak berfungsi         | Penyelenggara (untuk pengecekan kuota dan billing) |
| Pertanyaan materi & repo        | Buka issue di GitHub repo ini          |

---

## 5. Referensi Lanjutan

- [`README.md`](README.md) — overview pelatihan
- [`REQUIREMENTS-Spek-Komputer-Aplikasi.md`](REQUIREMENTS-Spek-Komputer-Aplikasi.md) — detail spesifikasi hardware dan software
- [`pretest/PRETEST-AI-Claude.md`](pretest/PRETEST-AI-Claude.md) — pretest peserta
- [`resources/claude-api-cheatsheet.md`](resources/claude-api-cheatsheet.md) — cheatsheet Claude API
- [`resources/references.md`](resources/references.md) — bacaan lanjutan
- Dokumentasi resmi Anthropic: https://docs.anthropic.com

---

*Sudah siap belajar? Silakan lanjut ke [Day-1 — Prompt Engineering](Day-1-Prompt-Engineering/README.md).*
