# Jurnal Proses — Tugas 3

## Percobaan tanpa Lock
- Hasil `processed_count` yang didapat: ![Hasil percobaan tanpa lock](bukti/Log%20Output_Skeleton.png)
- Kenapa bisa meleset (jelaskan mekanisme race condition dengan kata sendiri): karena kode yang ada di order_simulator_skeleton.py tidak menggukanan lock pada variable `processed_count` dimana beberapa thread mengakses `processed_count` secara bersamaan yang mengakibatkan proses operasi diinterupsi.

## Percobaan dengan Lock
- Hasil `processed_count` setelah perbaikan: ![Hasil percobaan menggunakan lock](bukti/Log%20Output_Update.png)

## Kendala Docker
- Error yang ditemui saat `docker build`/`docker run` dan cara memperbaikinya: saat docker build terjadi error karena terimnal tidak masuk ke tugas 03. memperbaikinya masuk ke integrated terminal di tugas 3

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
|01-10-2026|GeminiAI|Bantu aku edit draft kode ini agar tidak terjadi race Condition|Tambahkan Kode ini untuk Pengisian # TODO TODO 1: Didefinisikan lock = threading.Lock() di tingkat global untuk menyediakan mutex (mutual exclusion).   TODO 2: Operasi processed_count += 1 dibungkus dalam blok with lock:. Ini menjamin bahwa hanya `1` thread dalam satu waktu yang dapat mengeksekusi increment nilai counter tersebut.   TODO 3: List order_ids berisi `100` pesanan dibagi menjadi `10` bagian (chunk), di mana masing-masing thread memegang `10` pesanan. Setiap thread di-start() secara bersamaan lalu di-join() agar fungsi main() menunggu semua thread selesai bekerja sebelum mencetak hasil akhir.|Untuk TODO 1 menambahkan lock = threading.Lock(), untuk TODO 2 menambahkan with lock: processed_count += 1, untuk TODO 3 menambahkan chunk_size = NUM_ORDERS // NUM_WORKERS|
|03-10-2026|GeminiAI|oke jadi aku kebagian tugas 3 nomor 3 tentang Docker & Containerization Specialist tuntun aku caranya|Sebagai Docker & Containerization Specialist, tugasmu adalah mengemas aplikasi Python ke dalam Docker Container, memastikan aplikasinya bisa di-build dan di-run dengan lancar| mengikuti step by step cara penggunaan docker|
