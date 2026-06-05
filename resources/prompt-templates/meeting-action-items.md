# Template: Meeting Notes → Action Items

## System Prompt

```
Anda adalah asisten rapat yang mengekstrak ringkasan, keputusan, dan action items dari transkrip rapat.

Aturan:
- Hanya gunakan informasi dari transkrip. Jangan menebak nama yang tidak disebutkan.
- Action item harus punya: pemilik (orang/tim), aksi, deadline (jika disebut).
- Pisahkan KEPUTUSAN (sudah disepakati) dari DISKUSI (belum diputuskan).
- Output bahasa Indonesia formal.
```

## User Message

```
Konteks rapat:
- Topik: <topik>
- Peserta: <list nama>
- Tanggal: <YYYY-MM-DD>

Transkrip:
"""
<paste transkrip>
"""

Tugas:
1. Ringkasan eksekutif (3 kalimat).
2. Keputusan (bullet).
3. Action items (tabel: Pemilik | Aksi | Deadline | Status).
4. Open questions / item yang ditunda ke rapat berikutnya.
5. Risiko / blocker yang disebutkan.

Output: markdown.
```

## Output Schema (jika ingin JSON)

```json
{
  "summary": "string (3 kalimat)",
  "decisions": ["string", ...],
  "action_items": [
    {
      "owner": "string",
      "action": "string",
      "deadline": "string|null (YYYY-MM-DD)",
      "priority": "high|medium|low"
    }
  ],
  "open_questions": ["string", ...],
  "risks": ["string", ...]
}
```

## Variasi: Audio → Action Items

Jika input berupa audio:

1. Transkripsi dulu (Whisper API / Deepgram / Speech-to-Text).
2. Bersihkan transkrip (hapus "ehm", duplikasi).
3. Kirim ke Claude dengan template ini.

## Variasi: Multi-Meeting Tracking

Untuk tracking action items lintas rapat (mingguan):

```
Anda akan menerima:
1. Action items dari rapat sebelumnya (dengan status terakhir).
2. Transkrip rapat hari ini.

Tugas:
- Update status action items lama berdasarkan diskusi hari ini.
- Tambah action items baru.
- Tandai action items yang carry-over ke minggu depan.

Output JSON dengan struktur yang sama.
```

## Test Cases

| ID  | Input                                          | Verifikasi                                          |
| --- | ---------------------------------------------- | --------------------------------------------------- |
| TC1 | Rapat singkat 30 menit dengan 3 decision       | Semua decision tertangkap, action items punya owner |
| TC2 | Rapat panjang 2 jam, banyak digresi            | Ringkasan tetap fokus, action items relevan         |
| TC3 | Transkrip dengan crosstalk (interrupting)      | Tidak salah attribusi                               |
| TC4 | Rapat tanpa action item eksplisit              | `action_items: []`, tidak fabrikasi                 |
| TC5 | Rapat berisi info sensitif (gaji, evaluasi)    | Tetap diekstrak, tapi flag confidentiality          |
