# Jurnal Proses — Tugas 2

## [26-09-2026]
- Opsi arsitektur yang dipertimbangkan: Kombinasi Service-Oriented Architecture (SOA) dan Publish-Subscribe (Pub-Sub)
- Kenapa akhirnya pilih [SOA/Pub-Sub]: dipilih karena memberikan keseimbangan antara keandalan data transaksi (lewat SOA) dan performa yang longgar serta cepat tanpa ketergantungan langsung antar-modul (lewat Pub-Sub). Jika modul kurir mengalami kendala, modul pembayaran dan pesanan tidak akan ikut down
- Revisi diagram (versi 1 → versi 2, apa yang berubah dan kenapa): merevisi di modul (pesanan, pembayaran, kurir, dan resto) karena terhubung ke database tunggal

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
|26-09-2026|Gemini Ai|Brainstroming soal ini dan berikan detail yang dimaksudkan|Tugas ini meminta Anda dan kelompok untuk mengubah arsitektur aplikasi FoodGo yang sebelumnya berbentuk monolit (semua jadi satu, kalau ada yang di-update bisa bikin sistem mati total/downtime) menjadi arsitektur yang terdistribusi dan ter-decouple (terpisah-pisah). Fokus utamanya adalah memilih gaya arsitektur (SOA atau Pub-Sub, atau kombinasinya), menggambar rancangan sistemnya, menjelaskan alur data dari end-to-end, serta menganalisis kelebihan dan kekurangannya (trade-off)|Memahami yang dimaksudkan oleh Ai lalu mengisi jawaban dengan sesuai instruksi atau sedikit arahan dari Ai|
