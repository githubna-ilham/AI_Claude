# Requirements — Spesifikasi Komputer & Aplikasi

> Persyaratan teknis untuk **peserta** dan **fasilitator** pelatihan AI Claude (4 hari).
> Verifikasi semua item ini selesai **H-1** sebelum pelatihan dimulai.

---

## A. Spesifikasi Hardware (Laptop Peserta)

### A.1 Minimum (Mampu mengikuti, tapi terbatas)

| Komponen      | Spesifikasi                                  |
| ------------- | -------------------------------------------- |
| **CPU**       | Intel Core i5 gen 8 / AMD Ryzen 5 / Apple M1 |
| **RAM**       | 8 GB                                         |
| **Storage**   | 20 GB free space                             |
| **OS**        | Windows 10/11, macOS 12+, Ubuntu 22.04+      |
| **Display**   | 13" 1080p                                    |
| **Network**   | WiFi 802.11n + ethernet backup               |
| **Battery**   | Min 4 jam (atau colokan tersedia di kursi)   |

### A.2 Direkomendasikan (Lancar untuk semua lab)

| Komponen      | Spesifikasi                                          |
| ------------- | ---------------------------------------------------- |
| **CPU**       | Intel Core i7 gen 11+ / AMD Ryzen 7 / Apple M2/M3/M4 |
| **RAM**       | **16 GB** (paling impactful)                         |
| **Storage**   | 50 GB free SSD                                       |
| **OS**        | Windows 11, macOS 14+, Ubuntu 24.04                  |
| **Display**   | 14"+ 1440p / Retina                                  |
| **Network**   | WiFi 6 + ethernet backup                             |

### A.3 Catatan Penting

- **RAM 16 GB sangat direkomendasikan** untuk Day 3 (vector DB lokal + embedding model + IDE + browser). Dengan 8 GB masih bisa, tapi peserta perlu tutup aplikasi lain.
- **GPU tidak wajib.** Semua inference LLM lewat Claude API (cloud). Embedding bisa pakai cloud (Voyage AI) atau CPU lokal (sentence-transformers — lebih lambat tapi tetap jalan).
- **Tablet / Chromebook TIDAK direkomendasikan** — banyak lab perlu install Python, Node.js, dan jalankan server lokal.
- **Mouse eksternal** opsional tapi membantu untuk Day 3-4 (banyak coding).

---

## B. Software Wajib (Pre-Install H-3 sampai H-1)

### B.1 Runtime & Bahasa

| Software       | Versi minimum | Wajib?                         | Link install                                  |
| -------------- | ------------- | ------------------------------ | --------------------------------------------- |
| **Python**     | 3.11+         | Wajib (default lab)            | https://www.python.org/downloads/             |
| **pip**        | (bundled)     | Wajib                          | (ikut Python)                                 |
| **Node.js**    | 20 LTS+       | Opsional (alternatif JS)       | https://nodejs.org/                           |
| **Git**        | latest        | Wajib                          | https://git-scm.com/downloads                 |

### B.2 Editor / IDE (pilih salah satu)

| Editor                 | Rekomendasi untuk                                  |
| ---------------------- | -------------------------------------------------- |
| **VS Code**            | Default — paling universal                         |
| **Cursor**             | Rekomendasi #1 (sinergi dengan pelatihan AI Cursor)|
| **PyCharm Community**  | Bila peserta sudah biasa JetBrains                 |
| **Jupyter Lab**        | Tambahan untuk eksplorasi notebook                 |

### B.3 Browser

- **Chrome / Edge / Firefox** versi terbaru
- Direkomendasikan: profile khusus pelatihan agar terisolasi dari akun pribadi

### B.4 Tools Tambahan

| Tool                  | Fungsi di pelatihan                          | Wajib? |
| --------------------- | -------------------------------------------- | ------ |
| **Postman / Insomnia**| Test Claude API request manual               | Opsional |
| **Docker Desktop**    | Run Chroma / pgvector via container          | Opsional (alternatif ada) |
| **DBeaver**           | Inspect vector DB (pgvector)                 | Opsional |
| **Slack / Telegram**  | Channel pelatihan untuk Q&A                  | Wajib (1 dari ini) |

---

## C. Python Packages (Install di Virtual Environment)

Buat virtualenv & install. Pre-install H-1.

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -U pip
pip install -r requirements.txt
```

**`requirements.txt`:**

```
anthropic>=0.40.0
python-dotenv>=1.0.0
fastapi>=0.115.0
uvicorn[standard]>=0.32.0
streamlit>=1.40.0
chromadb>=0.5.0
sentence-transformers>=3.0.0
voyageai>=0.3.0
pypdf>=5.0.0
python-docx>=1.1.0
pandas>=2.2.0
tiktoken>=0.8.0
tenacity>=9.0.0
pydantic>=2.9.0
httpx>=0.27.0
```

**Verifikasi instalasi:**

```bash
python -c "import anthropic, chromadb, fastapi; print('OK')"
```

### Node.js Packages (Opsional, untuk peserta JS)

```bash
npm init -y
npm install @anthropic-ai/sdk dotenv express
```

---

## D. Akun & Layanan Cloud (Setup H-3)

| Layanan                       | Wajib?  | Cara setup                                                    | Catatan biaya                              |
| ----------------------------- | ------- | ------------------------------------------------------------- | ------------------------------------------ |
| **Anthropic Console**         | **WAJIB** | https://console.anthropic.com → sign up → generate API key  | Top-up min $5; pelatihan habiskan ~$2-5/peserta |
| **Voyage AI**                 | Rekomendasi | https://www.voyageai.com → sign up → API key              | Free tier cukup untuk pelatihan            |
| **GitHub**                    | Wajib   | Akun GitHub aktif                                             | Free                                       |
| **Google Account**            | Wajib   | Untuk akses Google Form pretest/posttest                      | Free                                       |
| **OpenAI API** (alternatif embedding) | Opsional | https://platform.openai.com                            | Bayar per token                            |
| **Pinecone / Weaviate**       | Opsional | Hanya jika mau cloud vector DB                                | Free tier ada                              |

### D.1 Setup API Key (penting!)

Tiap peserta WAJIB:

1. Generate Anthropic API key dari https://console.anthropic.com/settings/keys
2. Top-up minimum $5 (atau gunakan key yang disediakan fasilitator)
3. Set environment variable:

   **macOS / Linux:**
   ```bash
   echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.zshrc
   source ~/.zshrc
   ```

   **Windows (PowerShell):**
   ```powershell
   [Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-...", "User")
   ```

4. Verifikasi:
   ```bash
   python -c "from anthropic import Anthropic; print(Anthropic().messages.create(model='claude-haiku-4-5', max_tokens=20, messages=[{'role':'user','content':'ping'}]).content[0].text)"
   ```

### D.2 `.env` Template

Setiap project folder pakai `.env` (jangan commit ke git):

```env
ANTHROPIC_API_KEY=sk-ant-...
VOYAGE_API_KEY=pa-...
```

Pastikan `.gitignore` berisi:
```
.env
.venv/
__pycache__/
chroma_demo/
```

---

## E. Per-Hari Yang Perlu Disiapkan

### Day 1 — Prompt Engineering Fundamentals

**Peserta cukup:** browser + akun Anthropic Console. **Belum perlu coding.**

- [ ] Akses https://claude.ai (free tier OK)
- [ ] Akses https://console.anthropic.com/workbench (untuk demo parameter)
- [ ] Pretest sudah diisi

### Day 2 — AI Workflow & Agent

**Mulai coding:**

- [ ] Python venv siap, `pip install anthropic python-dotenv` jalan
- [ ] API key sudah di env var (verifikasi dengan curl/python test)
- [ ] Editor + GitHub repo materi sudah di-clone
- [ ] Postman/Insomnia (opsional, untuk eksplorasi raw API)

### Day 3 — AI App + RAG

**Paling intensive di hardware/software:**

- [ ] FastAPI + uvicorn berfungsi: `uvicorn --version`
- [ ] Streamlit berfungsi: `streamlit hello`
- [ ] Chroma jalan lokal: `python -c "import chromadb; chromadb.PersistentClient(path='./test_db')"`
- [ ] Voyage AI key (atau sentence-transformers downloaded — first run ~80 MB)
- [ ] Sample dokumen sudah ada di folder lab
- [ ] Disk space cek: minimum 5 GB free (untuk models + chroma)

### Day 4 — Product, Governance, Capstone

- [ ] Slide deck tool: Google Slides / PowerPoint / Keynote
- [ ] Optional: Figma/Miro untuk diagram arsitektur
- [ ] Form rubrik (Google Form) sudah dibuat oleh fasilitator
- [ ] Backup API key budget untuk capstone (tiap tim bisa pakai 50-100 calls demo)

---

## F. Setup untuk Fasilitator (Tambahan)

### F.1 Hardware Fasilitator

| Komponen  | Spesifikasi                             |
| --------- | --------------------------------------- |
| Laptop    | Spek **direkomendasikan** (B.2), 16 GB RAM |
| Layar tambahan | Untuk presentasi + notes              |
| HDMI/USB-C adapter | Untuk proyektor ruang kelas      |

### F.2 Software Fasilitator

- Semua yang ada di B + C
- **Anthropic Console** dengan **budget cukup** ($50-100 untuk demo intensif 4 hari)
- **OBS / Loom** untuk rekaman sesi (jika perlu)
- **Screen annotation tool** (Annotate, Presentify) untuk highlight saat demo
- **Timer / stopwatch** (banyak lab time-boxed)

### F.3 Konten yang Harus Siap (per ringkasan agen)

- [ ] Slide presentasi per Module (slide deck di-export dari `materi.md`)
- [ ] Sample dokumen HR (PDF kebijakan cuti, SOP DOCX, FAQ CSV) di `lab-09/sample_docs/`
- [ ] Sample bug invoice fiktif untuk Lab 03
- [ ] 5 contoh tweet bahasa Indonesia untuk Lab 02
- [ ] Golden Q&A set 10-20 pasang untuk eval Lab 11
- [ ] Mock data tiket helpdesk untuk Capstone opsi 6
- [ ] PDF dummy berisi indirect prompt injection untuk demo Module 14
- [ ] Cetak: Use Case Canvas A3 (1/peserta), checklist Responsible AI, OWASP LLM Top 10

### F.4 Backup Plan

- **API key cadangan** bila key utama kena rate limit
- **Hotspot 4G/5G** bila WiFi ruang kelas drop
- **Offline embeddings** (sentence-transformers) bila Voyage AI bermasalah
- **Pre-recorded demo video** untuk segmen kritis bila live demo gagal
- **Snapshot Chroma DB** sudah berisi data, agar peserta yang lambat ingest bisa skip ke retrieval

---

## G. Setup untuk Ruang Pelatihan

| Item                          | Spesifikasi                                     |
| ----------------------------- | ----------------------------------------------- |
| **Proyektor / TV**            | Min 4K untuk teks code yang jelas              |
| **Audio**                     | Wireless mic + speaker                          |
| **Internet**                  | Min 50 Mbps untuk 15-20 peserta, redundant      |
| **Power outlet**              | 1 colokan per peserta minimum                   |
| **Whiteboard / flipchart**    | Untuk Module 7-8 (diagram agent), Module 13 (canvas) |
| **AC / sirkulasi**            | Banyak laptop = panas                           |
| **Snack & kopi**              | Sesi intensif 8 jam butuh asupan                |

---

## H. Checklist Final (H-1)

**Untuk Peserta:**

- [ ] Hardware memenuhi minimum (idealnya direkomendasikan)
- [ ] Python 3.11+, Node.js (opsional), Git terinstal
- [ ] Editor (VS Code / Cursor) terinstal
- [ ] `requirements.txt` ter-install di virtualenv
- [ ] Anthropic API key didapat & ada di env var
- [ ] Voyage AI key (opsional)
- [ ] Akun GitHub aktif
- [ ] Pretest sudah diisi
- [ ] Repo materi sudah di-clone
- [ ] Sample dokumen sudah di-download
- [ ] Test ping API berhasil (jalankan snippet verifikasi)
- [ ] Browser dengan profile pelatihan

**Untuk Fasilitator:**

- [ ] Semua di atas (sebagai backup demo)
- [ ] Slide deck final per Module
- [ ] Sample data & golden set
- [ ] API key budget cukup ($50-100)
- [ ] Aset cetak (Canvas A3, checklist)
- [ ] Ruang kelas tervalidasi (proyektor, internet, listrik)
- [ ] Backup plan teruji (hotspot, offline embeddings, video)

---

## I. FAQ Singkat

**Q: Apakah harus pakai Mac?**
A: Tidak. Windows / Linux / Mac semuanya kompatibel. Mac M-series memang lebih cepat untuk embedding lokal.

**Q: Berapa biaya total Anthropic API untuk 1 peserta 4 hari?**
A: Estimasi $2-5 untuk semua hands-on bila peserta tertib (pakai Haiku untuk task ringan, Sonnet untuk yang perlu kualitas). Top-up $10 sudah aman.

**Q: Apakah bisa offline?**
A: TIDAK. Claude API mutlak butuh internet. Embedding bisa lokal (sentence-transformers), tapi inference LLM cloud-only.

**Q: Apakah bisa pakai LLM open-source (Llama, Mistral)?**
A: Konsep prompting & agent transferable, tapi materi pelatihan ini spesifik Claude API (tool use format, prompt caching, dll.). Untuk Capstone bila ingin demo dengan LLM lokal, perlu adaptasi pribadi.

**Q: Boleh pakai akun Anthropic team / organization?**
A: Boleh, dan justru lebih praktis untuk fasilitator (1 API key, multiple users via metadata).

**Q: Bagaimana kalau peserta belum punya kartu kredit untuk Anthropic?**
A: Fasilitator sediakan API key bersama dengan budget tracking per user via `metadata.user_id`.
