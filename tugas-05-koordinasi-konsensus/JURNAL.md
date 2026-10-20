# Jurnal Proses — Tugas 5

## Implementasi Bully
- Kendala saat mengisi TODO 1-4:
  - Pada TODO 1 (`on_message`), perlu memastikan penanganan pesan `ELECTION` dilakukan secara asinkron (menggunakan `threading.Thread`) saat memanggil `start_election()` agar proses penerimaan/pembalasan pesan `OK` tidak terhalang (*blocking*).
  - Pada TODO 2 (`start_election`), penanganan timeout untuk `ok_received` harus di-reset (`clear()`) dengan benar sebelum mengirimkan pesan `ELECTION` ke node-node yang lebih tinggi.
  - Pada TODO 4 (`monitor_leader`), harus memastikan pengecekan status leader menggunakan blok `lock` agar tidak terjadi race condition saat meng-update `self.leader_id` ketika koneksi `PING` gagal.

## Skenario 1: Start normal
- Leader yang terpilih: Node-5
- Log/observasi: Saat Node 1 hingga Node 5 dinyalakan hampir bersamaan di port 5001–5005, masing-masing node mulai mengirimkan pesan `ELECTION` ke peer dengan ID yang lebih tinggi. Node 1–4 menerima balasan `OK` dari node di atasnya sehingga menghentikan pencalonan. Node 5 (memiliki ID tertinggi) tidak memiliki peer yang lebih tinggi (`higher_peers: {}`), sehingga langsung memanggil `declare_leader()` dan melakukan broadcast pesan `COORDINATOR` ke seluruh peer. Seluruh node (Node 1–4) berhasil menerima pesan `COORDINATOR` dari Node 5 dan mencatat Node 5 sebagai Leader Utama.

## Skenario 2: Leader dimatikan
- Leader baru yang terpilih: Node-4
- Berapa lama waktu sampai leader baru terdeteksi: ± 3 hingga 5 detik.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
|20-10-2026|GeminiAI|Bolehkan minta bantuan ide alur dan pengisian jurnal skenario Bully Algorithm?|Memberikan gambaran alur deteksi timeout dan struktur observasi log untuk jurnal.|Ditulis ulang dengan kalimat sendiri dan disesuaikan dengan variabel/output log aktual dari `node.py`.|
