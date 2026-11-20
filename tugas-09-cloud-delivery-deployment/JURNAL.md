# Jurnal Proses — Tugas 9

## Diskusi deployment model
- Kelompok membandingkan Public Cloud murni, Private Cloud murni, dan Hybrid Cloud untuk Sistem Data Kependudukan.
- Public Cloud murni dinilai kurang tepat karena data kependudukan (NIK, alamat, biometrik) bersifat sangat rahasia dan diatur regulasi perlindungan data pribadi sehingga membutuhkan kendali penuh negara.
- Private Cloud murni dinilai kurang optimal untuk menghadapi lonjakan trafik musiman (pemilu atau pendaftaran sekolah) secara elastis.
- Hybrid Cloud dipilih karena memungkinkan database utama dan pemrosesan biometrik tetap aman di Sovereign Private Cloud, sementara portal publik, API Gateway, dan penskalaan beban memanfaatkan Public Cloud yang terhubung lewat jalur terenkripsi TLS 1.3 dan ZTNA.

## Diskusi service model per komponen
- Database Utama Kependudukan dan Audit & Security Logs di Private Cloud diarahkan ke IaaS agar negara memiliki kontrol penuh atas OS, penyimpanan terenkripsi, dan isolasi jaringan.
- Core Middleware / Biometric Matcher Engine serta API Gateway Verifikasi KYC dan Cache diarahkan ke PaaS/IaaS terkelola agar pengembangan dan penskalaan layanan lebih efisien tanpa mengorbankan keamanan.
- Web Server Portal Status diarahkan ke SaaS / layanan aplikasi terkelola di Public Cloud agar mudah diskalakan saat lonjakan akses warga.

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

## Log Penggunaan AI (Level 2)

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 20-11-2026 | Gemini | Membantu pembagian jobdesk 3 orang dan menyusun draf analisis risiko, perbandingan alternatif ditolak, skenario tandingan, serta jurnal Tugas 9 | Memberikan pembagian tugas per anggota, ide risiko spesifik (cache Redis & jalur Direct Connect), alasan penolakan Public Cloud murni, serta contoh skenario tandingan Dukcapil daerah. | Disesuaikan dengan diagram arsitektur kelompok PaperRex, dirapikan alur bahasanya, lalu dilengkapi identitas anggota dan detail finalisasi dokumen. |
