# Tugas 3 — MultiThreading Container

**Kelompok:** [PaperRex]

| Nama | NIM | Kontribusi |
|---|---|---|
| [Rizqullah Izzul Ibad Gheaz] | [103072400033] | [Analisis] |
| [Habhindra Dzaky Alghifary] | [103072400095] | [MQ] |
| [Muhammad Zaki Oktaruna] | [103072400001] | [RPC] |

## 1. Analisis Jalur A: Remote Procedure Call (RPC) — Komunikasi Sinkron
Mekanisme Kerja & Bukti Percobaan
Pada Jalur A, modul Pesanan bertindak sebagai client yang memanggil fungsi jarak jauh (cek_saldo dan proses_pembayaran) yang diekspos oleh modul Pembayaran sebagai server menggunakan library xmlrpc.
- Berdasarkan tangkapan layar eksekusi program, ketika client.py memanggil cek_saldo('user1'), program client secara eksplisit menunggu (blocking) hingga server memberikan respons balasan dengan waktu tempuh eksekusi terukur (sekitar 2.0261 detik).
- Setelah itu, pemanggilan fungsi proses_pembayaran('user1', 20000) dijalankan dan langsung mengembalikan status sukses beserta saldo akhir secara seketika (immediate feedback).
Kenapa RPC Cocok untuk Skenario Ini?
- Konsistensi Data Seketika (Immediate Consistency): Operasi seperti pengecekan saldo dan pemotongan saldo saat checkout pesanan memerlukan kepastian mutlak sebelum transaksi dilanjutkan. Jika saldo tidak mencukupi, sistem harus langsung menghentikan proses saat itu juga.
- Alur Bisnis Berurutan: Modul Pesanan wajib tahu hasil akhir dari modul Pembayaran sebelum memberikan konfirmasi kepada pengguna bahwa pesanan berhasil dibuat.

## 2. Analisis Jalur B: Message Queue (RabbitMQ) — Komunikasi Asinkron (Asynchronous Decoupling)
Mekanisme Kerja & Bukti Percobaan
Pada Jalur B, modul Pembayaran (publisher) mengirimkan event pembayaran_berhasil ke broker pesan RabbitMQ tanpa harus menunggu modul Kurir (consumer) merespons.
- Berdasarkan uji coba pengiriman event, publisher.py sukses mengirimkan 3 data transaksi secara berturut-turut (user1, user2, user3) dan langsung selesai (non-blocking).
- Uji Coba Ketahanan Pesan (Decoupling & Durability): Ketika consumer.py dimatikan (tidak aktif), pesan yang dikirimkan oleh publisher tidak hilang, melainkan disimpan secara aman di dalam antrean broker RabbitMQ dengan status Ready sebanyak 3 pesan (terlihat pada dashboard manajemen RabbitMQ di http://localhost:15672).
- Begitu consumer.py dihidupkan kembali, consumer langsung mendeteksi dan memproses seluruh antrean pesan yang tertunda secara otomatis, lalu mengirimkan acknowledgement (ch.basic_ack) sehingga pesan terhapus dari antrean setelah selesai diproses.

## 3. Analisis Risiko: Dampak Jika Menggunakan Pola yang Salah
Pemilihan pola komunikasi yang keliru dalam arsitektur sistem terdistribusi dapat menimbulkan masalah fatal pada performa dan keandalan sistem:
A. Jika RPC (Sinkron) Dipakai untuk Notifikasi Kurir
- Dampak: Modul Pembayaran akan mengalami blocking karena harus menunggu respons dari modul Kurir/Notifikasi.
- Risiko Kegagalan: Jika modul kurir sedang mengalami heavy load, jaringan lambat, atau down, maka proses pembayaran pengguna di sisi frontend akan ikut tertahan (hanging) atau mengalami kegagalan total (cascading failure). Padahal, pembayaran utama pengguna sudah sukses dilakukan. Hal ini melanggar prinsip loose coupling.

B. Jika Message Queue (Asinkron) Dipakai untuk Cek Saldo
- Dampak: Modul Pesanan tidak bisa langsung mendapatkan kepastian hasil cek saldo secara instan karena pesan dikirim ke antrean terlebih dahulu (eventual consistency).
- Risiko Kegagalan: Proses checkout pesanan memerlukan respons seketika untuk memvalidasi apakah saldo pengguna cukup atau tidak. Jika menggunakan antrean asinkron untuk operasi baca/cek saldo, sistem akan kesulitan mengembalikan nilai balik secara langsung ke client pada detik yang sama, yang berpotensi memicu race condition atau pengalaman pengguna yang buruk.

## Kesimpulan
- Gunakan RPC (Sinkron) untuk operasi yang membutuhkan respons langsung dan konsistensi data seketika (seperti cek_saldo dan proses_pembayaran).
- Gunakan Message Queue (Asinkron) untuk proses latar belakang (background processing) atau pengiriman event notifikasi yang tidak menghambat alur utama (seperti kirim notifikasi ke modul kurir) guna memastikan sistem tetap responsif dan tahan terhadap gangguan (fault tolerant).
