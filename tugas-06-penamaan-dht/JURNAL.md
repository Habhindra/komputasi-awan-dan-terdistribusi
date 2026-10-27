# Jurnal Proses — Tugas 6

## Implementasi find_successor
- Kesalahan pertama yang ditemui (mis. lupa wrap-around di ring): Pada awalnya, pencarian successor mengembalikan `None` jika nilai `key_hash` lebih besar dari seluruh ID node yang ada di dalam ring, karena mengabaikan sifat melingkar (*wrap-around*) dari ring Chord.
- Cara memperbaikinya: Menambahkan kondisi logika *wrap-around* di mana jika tidak ada node dengan ID $\ge$ `key_hash`, fungsi akan mengembalikan node dengan ID terkecil di dalam ring (`sorted_node_ids[0]`).

## Skenario join/leave
- Hasil sebelum & sesudah node baru bergabung: Sebelum node baru (`node-medan-1`) bergabung, pemetaan kurir ditangani oleh node-node awal. Setelah bergabung, node baru mengambil alih rentang ID tertentu, dan log program mencatat proses pengambilalihan data dari *successor* lama.
- Hasil sebelum & sesudah node keluar: Ketika `node-jakarta-1` keluar, data kurir yang sebelumnya dipegang otomatis dialihkan ke node successor berikutnya, memastikan fungsi `lookup` tetap mengembalikan IP yang benar tanpa terputus.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 27 Oktober 2026 | GeminiAI | Meminta penjelasan konsep dasar ring topology dan aturan successor pada Chord DHT untuk bahan analisis. | Penjelasan mengenai mekanisme *consistent hashing*, pencarian successor dengan *wrap-around*, serta perbandingan arsitektur DHT vs DNS/flat naming. | Disarikan dan disesuaikan secara manual ke dalam poin-poin analisis kelompok pada `JURNAL.md` dan `ANALISIS-TEMPLATE.md`. |