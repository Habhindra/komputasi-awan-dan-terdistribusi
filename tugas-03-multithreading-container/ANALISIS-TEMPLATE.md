# Tugas 3 — MultiThreading Container

**Kelompok:** [PaperRex]

| Nama | NIM | Kontribusi |
|---|---|---|
| [Rizqullah Izzul Ibad Gheaz] | [103072400033] | [Soal 1 & 2] |
| [Habhindra Dzaky Alghifary] | [103072400095] | [Soal 3] |
| [Muhammad Zaki Oktaruna] | [103072400001] | [Soal 4] |

## Analisis Kenapa Threading Bukan Proses Berat [Muhammad Zaki Oktaruna]

1. Perbedaan Mendasar: Process vs. Thread
Proses OS (Proses Berat / fork()): Setiap proses dibuat oleh sistem operasi memiliki ruang memori (memory space), tabel file, dan sumber daya sistem yang terisolasi dan independen. Saat server FoodGo menerima 100 pesanan dan membuat 100 proses baru menggunakan fork(), OS harus menduplikasi seluruh alokasi memori untuk setiap proses tersebut. Ini menyebabkan lonjakan konsumsi memori (memory overhead) yang sangat besar hingga akhirnya server kehabisan memori (out of memory).

Thread (Ringan): Sisi lain, thread berada di dalam satu proses yang sama. Seluruh thread dalam proses tersebut berbagi ruang memori yang sama (seperti heap memory, variabel global, dan deskriptor file). Thread hanya memiliki stack dan register sendiri yang ukurannya sangat kecil

2. Efisiensi Penggunaan Sumber Daya (Memori & CPU)
Memori: Karena thread berbagi ruang memori utama dari proses induknya, pembuatan ratusan thread tidak akan membebani RAM secara drastis seperti pembuatan ratusan proses baru. Sangat cocok untuk skenario server FoodGo yang harus menangani ribuan permintaan pesanan secara bersamaan tanpa membuat server crash akibat kehabisan RAM.
Waktu Pembuatan (Creation Overhead): Meluncurkan proses baru memerlukan waktu dan siklus CPU yang lebih lama karena OS harus menyiapkan struktur memori baru dari awal. Sementara itu, pembuatan thread jauh lebih cepat dan murah dari segi komputasi

4. Biaya Peralihan Konteks (Context Switching)
Saat CPU harus berpindah tugas dari satu alur eksekusi ke alur lainnya (context switching):

Perpindahan antar-proses memerlukan pertukaran direktori memori virtual (page table), yang berdampak pada cache misses yang tinggi dan lambat.

Perpindahan antar-thread di dalam proses yang sama jauh lebih cepat karena alamat memori dasarnya tidak berubah, sehingga cache CPU tetap dapat digunakan secara efektif.

Kesimpulan Untuk Studi Kasus FoodGo: 
Penggunaan multithreading (threading di Python) adalah solusi ideal untuk server FoodGo karena memungkinkan konkurensi (pemrosesan banyak pesanan secara bersamaan) dengan jejak memori (footprint) yang kecil, mencegah terjadinya kehabisan memori, serta menghindari overhead sistem operasi yang tidak perlu seperti pada pendekatan fork() tradisional
