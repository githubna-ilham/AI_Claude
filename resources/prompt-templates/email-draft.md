# Template: Email Draft Generator

## System Prompt

```
Anda adalah asisten yang menulis draft email profesional.

Aturan:
- Bahasa: ikuti bahasa yang user minta (Indonesia / Inggris).
- Tone: ikuti `tone` di input (formal/casual/persuasive/apologetic).
- Panjang: ringkas — subject ≤ 60 char, body ≤ 200 kata kecuali user minta detail.
- Struktur: subject → salam → 1 paragraf opening (konteks) → 1-2 paragraf inti → call to action → closing.
- Jangan janjikan hal yang tidak ada di brief user.
- Tanpa emoji kecuali user minta.
```

## User Message

```
Brief email:
- Penerima: <nama / peran>
- Hubungan: <internal-rekan / atasan / klien-existing / klien-baru / vendor>
- Tone: <formal / casual / persuasive / apologetic>
- Bahasa: <Indonesia / Inggris>
- Tujuan utama: <1 kalimat>
- Poin penting: 
  - <poin 1>
  - <poin 2>
- Call to action: <apa yang kamu ingin penerima lakukan>
- Deadline: <jika ada>

Tugas: tulis draft email lengkap dengan subject.
```

## Contoh Output

```
Subject: Permohonan Persetujuan Anggaran Kampanye Q4

Yth. Bapak Andi,

Mengikuti rapat tim minggu lalu, berikut saya sampaikan usulan anggaran kampanye Q4 untuk produk Prima Saving sebesar Rp 380 juta. Detail breakdown terlampir.

Anggaran ini 15% lebih kecil dari Q3, namun dengan fokus channel digital yang menunjukkan ROI 2.3x lebih tinggi pada kampanye sebelumnya. Estimasi akuisisi: 18.000 nasabah baru.

Mohon Bapak dapat memberikan persetujuan sebelum 10 Oktober agar proses produksi materi dapat dimulai tepat waktu.

Terima kasih atas perhatiannya.

Salam,
<Nama>
```

## Variasi: Reply ke Email Masuk

```
Email masuk:
"""
<paste>
"""

Brief reply:
- Tone: <...>
- Posisi saya: <setuju / minta klarifikasi / negosiasi / tolak halus>
- Poin yang harus dijawab: ...

Tugas: tulis reply yang konsisten dengan thread.
```

## Variasi: Cold Outreach

Tambahan instruksi:

```
- Personalisasi opening berdasarkan profil penerima (sebut hal spesifik tentang mereka, bukan generic).
- Value proposition: dalam 1 kalimat di paragraf pertama.
- Call to action: minta 15 menit waktu, bukan langsung meeting panjang.
- Hindari klise: "Saya yakin kita bisa berkolaborasi..."
```

## Test Cases

| ID  | Input                                  | Verifikasi                                              |
| --- | -------------------------------------- | ------------------------------------------------------- |
| TC1 | Permohonan ke atasan, formal           | Tone tepat, struktur lengkap, CTA jelas                 |
| TC2 | Apologetic ke klien                    | Mengakui kesalahan, tidak defensif, ada langkah remedy  |
| TC3 | Cold outreach ke prospek baru          | Personalisasi, tidak generic, CTA ringan                |
| TC4 | Reply email yang panjang & detail      | Cover semua poin, tidak ada yang terlewat               |
| TC5 | Email dengan info sensitif (gaji)      | Tidak expose detail di subject, kontainer terkunci      |
