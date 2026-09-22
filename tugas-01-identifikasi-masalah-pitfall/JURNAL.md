# Jurnal Proses — Tugas 1

> Isi jurnal ini selama proses diskusi berlangsung, bukan ditulis ulang rapi di akhir. Tulis dengan gaya bebas — poin diskusi, kebuntuan, perubahan pikiran.

## [Tanggal 22 September 2026]
- Peserta: [Muhammad Zaki Oktaruna,Habhindra Dzaky Alghifary,Rizqullah Izzul Ibad]
- Poin diskusi:
  1. Pembagian analisia Pitfall
  2. Pengambilan kesimpulan berdasarkan analisa 3 Pitfall
- Perbedaan pendapat (jika ada): ...

## [Tanggal diskusi 2]
- ...

## Review Silang
- [Habhindra] mengomentari analisis [Ibad]: Solusi yang ditawarkan cuma berdasarkan teori, tapi memang industry standard untuk mengatasi masalah blocking di sistem terdistribusi. trade-off yang dibahas juga menunjukkan bahwa analisis ini memikirkan risiko jangka panjangnya.
- [Habhindra] mengomentari analisis [Zaky]: Alur dampak dari resource exhaustion hingga lumpuh total layanan  sangat logis. menggambarkan risiko nyata dari sistem yang tidak punya isolasi sumber daya.
- [Zaki] mengomentari analisis [Habhindra]: sebaiknya bagian trade-off difokuskan pada risiko dari solusi circuit breaker dan backoff itu sendiri (misalnya menambah kompleksitas sistem), bukan malah membahas bahaya retry tanpa jeda yang sebenarnya tidak ia sarankan di poin sebelumnya
- [Zaki] mengomentari analisis [Ibad]: sudah tidak ada yang bisa direview 

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
|22-09-2026|GeminiAI|jadi aku disuruh menganalisis mengenai pitfal "latency is zero" dari studi kasus ini, kasih aku saran  1. kutipan skenario yang keliru 2. kenapa keliru? 3. dampak ke FoodGo 4. solusi desain awal 5. Trade-off|AI memberikan saran dari 5 poin yang diperlukan untuk melengkapi analisa pitfall 1|aku pahami poin-poin penting yang diberikan oleh AI lalu menulis kembali menggunakan pemahaman saya pribadi|
