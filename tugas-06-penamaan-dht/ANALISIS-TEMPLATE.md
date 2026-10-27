# Tugas 6— Penamaan DHT

**Kelompok:** [PaperRex]

| Nama | NIM | Kontribusi |
|---|---|---|
| [Rizqullah Izzul Ibad Gheaz] | [103072400033] | [Analisis] |
| [Habhindra Dzaky Alghifary] | [103072400095] | [Testing] |
| [Muhammad Zaki Oktaruna] | [103072400001] | [SRC] |

## 1. Mengapa DHT/Chord Lebih Cocok Dibanding Flat Naming atau DNS Konvensional?
- **Dibandingkan dengan Flat Naming Sederhana (Tabel Pusat ID→IP):** Flat naming menggunakan database/tabel terpusat menjadi *single point of failure* (SPOF) dan *bottleneck*. Jika server pusat down atau mengalami lonjakan akses (misal ribuan kurir FoodGo memperbarui IP secara bersamaan), sistem akan lumpuh. Chord DHT mendistribusikan penyimpanan mapping ke seluruh node secara terdesentralisasi tanpa server pusat.
- **Dibandingkan dengan DNS Konvensional:** DNS dioptimalkan untuk entitas yang relatif statis atau jarang berubah dengan mekanisme *caching* TTL yang panjang. Alamat IP kurir FoodGo sangat dinamis (sering berpindah jaringan seluler/Wi-Fi). DNS tidak dirancang untuk menangani pembaruan frekuensi tinggi secara *real-time* dan efisien seperti halnya struktur ring berbasis *consistent hashing* pada DHT.

## 2. Diagram Ring Topology
Berdasarkan hasil simulasi (dengan ruang identifier $m=8$ atau $0-255$), berikut adalah urutan posisi node pada ring dan tanggung jawab data kurir:

```mermaid
graph TD
    N40["node-bandung-1 (id=40)"] --> N102["node-jakarta-2 (id=102)"]
    N102 --> N123["node-medan-1 (id=123)"]
    N123 --> N136["node-surabaya-1 (id=136)"]
    N136 --> N177["node-jakarta-1 (id=177)"]
    N177 --> N40

    classDef node fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    class N40,N102,N123,N136,N177 node;