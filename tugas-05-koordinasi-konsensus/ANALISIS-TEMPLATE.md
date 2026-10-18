# Tugas 5— Koordinasi Konsensus

**Kelompok:** [PaperRex]

| Nama | NIM | Kontribusi |
|---|---|---|
| [Rizqullah Izzul Ibad Gheaz] | [103072400033] | [Testing] |
| [Habhindra Dzaky Alghifary] | [103072400095] | [Analisis] |
| [Muhammad Zaki Oktaruna] | [103072400001] | [SRC] |

## 1. Urgensi Node Leader pada kasus Foodgo
Dalam sistem terdistribusi FoodGo, perbedaan waktu jam (clock skew) antar server dapat memicu race condition,seperti urutan pesanan acak atau pemrosesan stok ganda. Node Leader sebagai Single Source of Truth yang bertindak sebagai koordinator terpusat. Leader mengatur antrean pesanan pusat dan memberikan logical timestamp agar setiap transaksi diproses dalam urutan yang tepat di seluruh node.

## 2. Alasan Pemilihan BullyAlgorithm
Selalu memilih node aktif dengan ID tertinggi sebagai leader tanpa perlu voting kompleks.dan sangat efisien digunakan pada sistem terisolasi dengan jumlah node yang sudah terdefinisi dari awal

## 3. Kelemahan Bully Algorithm dibanding Raft Consensus
Bully memerlukan hingga pesan saat election, sedangkan Raft lebih efisien karena berbasis majority vote.Jika node ID tertinggi sering crash/restart, Bully akan terus memicu re-election paksa yang mengganggu pemrosesan transaksi. Raft lebih stabil karena leader baru wajib memiliki log transaksi yang paling mutakhir.Bully rawan menghasilkan dua leader saat network partition. Raft mencegah hal ini secara alami dengan syarat dukungan mayoritas

## 4. Ringkasan hasil pengetesan
- Skenario 1 Node 1-5 di nyalakan bersamaan.Node 5 (ID tertinggi) merespons pesan ELECTION dan mem-broadcast COORDINATOR ke seluruh peer sebagai Leader Utama.
- Skenario 2 Node 5 dimatikan. Node 1–4 mendeteksi kegagalan ping, memicu re-election, dan Node 4 terpilih menjadi Leader Baru
