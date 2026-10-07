# Jurnal Proses — Tugas 4

## Jalur yang dipilih
- [RPC / MQ / keduanya], alasan: ...

## Kendala teknis
- code py dijalankan sebelum virtual environment (venv) diaktifkan
- keamanan default windows ngeblokir eksekusi aktivasi code nya

## Uji "pesan tidak hilang" (khusus Jalur B)
- Langkah uji: matikan consumer → jalankan publisher → nyalakan consumer
- Hasil yang diamati:
- Saat Consumer mati publisher dijalankan sebanyak 4 kali tanpa menyalakan consumer.py, pesan tidak hilang melainkan tersimpan aman di RabbitMQ. Pada dashboard RabbitMQ,grafik Queued messages menunjukkan peningkatan bertangga hingga mencapai Ready: 12 pesan(3 saat pengetesan ulang untuk mengambil bukti) dengan status Persistent dan Consumers: 0.
- Kondisi Consumer dinyalakan,script secara otomatis mengambil seluruh 12 pesan yang menumpuk di antrean pembayaran_berhasil secara berurutan hingga selesai.setelah semua pesan terproses, jumlah pesan tertahan di dashboard RabbitMQ kembali turun menjadi 0.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|10-7-2026|GeminiAi|berikan aku panduan untuk memahami konsep tugas dan struktur  kode pika step by step |memberikan alur kerja pika mq rabbit,memberikan komponen utama pemahaman pika py dari publisher dan consumer,panduan langkah untuk pengujian|memahami point point pemahaman tentang pika dan langkah untuk pengujian|
| ... | ... | ... | ... | ... |
