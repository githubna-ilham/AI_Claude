# Prompt Templates Library

Koleksi template prompt siap pakai untuk berbagai use case bisnis. Salin → modifikasi `<placeholder>` → kirim ke Claude.

## Daftar Template

| Use Case                          | File                                                   |
| --------------------------------- | ------------------------------------------------------ |
| Customer Service Reply            | [`customer-service-reply.md`](./customer-service-reply.md)     |
| Document Summarization            | [`document-summarization.md`](./document-summarization.md)     |
| Information Extraction → JSON     | [`extraction-to-json.md`](./extraction-to-json.md)             |
| Ticket Classification             | [`ticket-classification.md`](./ticket-classification.md)       |
| Meeting Notes → Action Items      | [`meeting-action-items.md`](./meeting-action-items.md)         |
| Data Analysis Q&A                 | [`data-analysis-qa.md`](./data-analysis-qa.md)                 |
| Email Draft Generator             | [`email-draft.md`](./email-draft.md)                           |
| Internal Knowledge Assistant      | [`knowledge-assistant.md`](./knowledge-assistant.md)           |

## Prinsip Penyusunan

Setiap template mengikuti anatomi:

```
[ROLE]    Anda adalah ...
[CONTEXT] Informasi latar yang relevan
[TASK]    Apa yang harus dilakukan
[INPUT]   Data masukan (variable)
[CONSTRAINT] Aturan & larangan
[OUTPUT]  Format yang diharapkan (markdown / JSON / ...)
```

Lihat materi Day 1 Module 2 untuk pembahasan anatomi.
