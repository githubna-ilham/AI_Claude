# Lab 04 — Use Case Prompt Pack

**Modul:** 5 — Prompt for Business Use Cases
**Durasi:** 20–25 menit (grup 3–4 orang)
**Mode:** No-code (markdown saja). Validasi opsional via Anthropic Console.

---

## Tujuan

Peserta mampu menyusun **prompt pack** produksi-grade untuk 3 use case bisnis berbeda, lengkap dengan test cases untuk evaluasi.

## Prasyarat

- Sudah mengikuti materi Modul 5.
- Akses ke editor markdown (VS Code, Obsidian, dll.).
- *Opsional*: akses [console.anthropic.com](https://console.anthropic.com) untuk uji prompt.
  - **Reminder keamanan:** jika menggunakan API key, simpan di environment variable, jangan paste ke shared chat / commit ke git.

## Output yang Diharapkan

Satu file `prompt-pack.md` berisi 3 section, satu per use case:

1. **Customer Service Reply** — generate balasan empati untuk komplain.
2. **Meeting Summary → Action Items** — ekstrak ringkasan + action items dari notulen.
3. **Helpdesk Ticket Classifier** — klasifikasi kategori + priority.

## Langkah

1. **Pilih satu use case sebagai pilot** dalam grup. Diskusikan: siapa user-nya, output dipakai untuk apa, risiko bisnis apa kalau salah?
2. **Tulis system prompt** untuk use case pilot, mengandung minimal: role, policy/guardrail, output format spec.
3. **Tulis user prompt template** dengan placeholder `{{variable}}` yang jelas.
4. **Susun 5 test cases** untuk pilot use case: 3 happy path + 2 edge case (input kosong, bahasa campur, sarkasme, data tidak lengkap).
5. **Ulangi langkah 2–4** untuk 2 use case lain. Bagi tugas antar anggota grup agar paralel.
6. **(Opsional)** Jalankan prompt di Console Anthropic dengan model `claude-sonnet-4-5`. Catat output, bandingkan dengan ekspektasi.
7. **Review silang**: tukar prompt-pack dengan grup lain, beri 2 feedback konstruktif.

## Template `prompt-pack.md`

```markdown
# Prompt Pack — [Nama Grup]

## Use Case 1: Customer Service Reply

### System Prompt
<isi system prompt>

### User Prompt Template
<isi user prompt dengan placeholder>

### Output Spec
<JSON schema / Markdown structure>

### Test Cases
| # | Input | Expected Behavior | Actual Output | Pass? |
|---|---|---|---|---|
| 1 | ... | ... | ... | ✅/❌ |

## Use Case 2: Meeting Summary → Action Items
... (struktur sama)

## Use Case 3: Helpdesk Ticket Classifier
... (struktur sama)
```

## Kriteria Selesai (Rubrik)

| Aspek | Cukup (1) | Baik (2) | Sangat Baik (3) |
|---|---|---|---|
| Struktur prompt | Hanya task, tanpa role/format | Role + task + format | Role + policy + format + few-shot |
| Output format | Bebas | JSON/Markdown konsisten | Schema eksplisit + validator concept |
| Guardrails | Tidak ada | Disebut 1–2 | Disebut + dijelaskan kasusnya |
| Test cases | < 3 | 3–5 happy path | 5+ termasuk edge case |
| Review silang | Tidak dilakukan | Komentar generik | Feedback spesifik & actionable |

**Lulus lab:** minimal total 10/15 dengan tidak ada aspek di level "Cukup".

## Tips

- Mulai dari output format dulu, baru rumuskan task. Output yang jelas memudahkan instruksi.
- Untuk klasifikasi, **selalu** sebutkan label valid + apa yang dilakukan jika tidak yakin.
- Jangan lupa instruksi bahasa output (Indonesia / Inggris).

## Stretch Goal (jika waktu cukup)

Buat prompt versi *few-shot* (tambahkan 2 contoh input→output) untuk salah satu use case dan bandingkan kualitasnya dengan versi zero-shot.
