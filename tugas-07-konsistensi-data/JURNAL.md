# Jurnal Proses — Tugas 7

## Diskusi pemilihan model konsistensi
- Argumen yang dipertimbangkan: 
    1. Eventual Consistency murni: Latensi rendah dan ketersediaan tinggi (high availability), namun rentan mengalami inconsistent read (saldo basi/stale), yang berdampak fatal pada sistem finansial (false rejection saat memesan makanan).
    2. Sequential Consistency (Global): Menjamin konsistensi data secara mutlak di seluruh server/replika, namun latensi menjadi sangat tinggi (blocking) dan mengorbankan ketersediaan sistem (availability) secara keseluruhan.
    3. Client-Centric Consistency (Read-Your-Writes): Solusi berimbang (trade-off optimal) di mana replikasi antar-server tetap berjalan asinkron di latar belakang, namun pengguna individual dijamin selalu melihat saldo terbarunya sendiri lewat pelacakan versi data (version token)
- Kesimpulan akhir & alasan: Menggunakan kombinasi Eventual Consistency dengan mekanisme Read-Your-Writes (RYW). Karena kasus saldo e-wallet sangat sensitif terhadap pengalaman pengguna (user experience). Dengan RYW, bug saldo basi dapat diatasi sepenuhnya tanpa perlu memberlakukan sinkronisasi ketat (blocking) ke seluruh replika server yang akan memperlambat performa sistem

## Simulasi (jika dikerjakan)
- Hasil skenario naif vs Read-Your-Writes:
    1. Skenario Naif (Tanpa RYW): Setelah top-up saldo Rp50.000 di server Jakarta (versi 1), pembacaan saldo langsung di server Bandung (< 2 detik) menghasilkan saldo 0.0 (BUG). Hal ini terjadi karena proses replikasi belum selesai
    2. Skenario Read-Your-Writes: Setelah top-up tambahan Rp20.000 (total saldo Rp70.000, versi 2), pembacaan saldo segera di server Bandung dengan menyertakan versi_minimal = 2 mendeteksi bahwa data Bandung masih basi (1 < 2). Sistem secara otomatis mengalihkan (redirect) pembacaan ke server Jakarta, sehingga saldo yang dibaca SELALU BENAR (70000.0)

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
|30-10-2026|GeminiAi|Minta gambaran umum dan poin outline tentang konsep konsistensi data|Memberikan penjelasan ringkas dan singkat perbedaan Eventual Consistency dan Sequential Consistency secara umum|Menggunakan poin-poin tersebut sebagai kerangka acuan awal, lalu menyusun analisis dan pengerjaan tugas secara mandiri.|
