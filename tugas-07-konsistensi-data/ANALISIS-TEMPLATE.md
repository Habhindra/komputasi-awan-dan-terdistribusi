# Tugas 6 — Konsistensi Data

**Kelompok:** [PaperRex]

| Nama | NIM | Kontribusi |
|---|---|---|
| [Rizqullah Izzul Ibad Gheaz] | [103072400033] | [SRC & Testing] |
| [Habhindra Dzaky Alghifary] | [103072400095] | [Diagram Mermaid] |
| [Muhammad Zaki Oktaruna] | [103072400001] | [ ... ] |

## 1. Diagram

1.Skenario Bug Happens

```mermaid
sequenceDiagram
    autonumber
    actor C as Pelanggan (Client)
    participant J as Server Jakarta (Primary)
    participant B as Server Bandung (Replica)

    %% Step 1: Top-up di Jakarta
    C->>J: 1. Top-up Saldo (+Rp100.000)
    Note over J: Update saldo lokal<br/>(Saldo Baru: Rp150.000)
    J-->>C: 2. Konfirmasi Top-up Berhasil
    
    %% Proses Replikasi Lambat/Async
    J->>B: 3. Replikasi Asinkron (Terhambat / Delay)
    
    %% Step 2: Transaksi di Bandung sebelum replikasi selesai
    Note over C,B: Beberapa detik kemudian pelanggan memesan makanan
    C->>B: 4. Buat Pesanan (Bayar Rp50.000)
    B->>B: 5. Cek Saldo Lokal
    Note over B: Replikasi belum sampai!<br/>Saldo lokal masih Rp50.000 (Stale)
    
    alt Pembayaran Gagal
        B-->>C: 6. Transaksi Ditolak ("Saldo Tidak Cukup")
    end

    %% Replikasi baru selesai setelah transaksi gagal
    J-->>B: 7. Sync Replikasi Selesai (Saldo: Rp150.000)
```
2.Skenario Skenario Solusi Client-Centric
Skenario ini menunjukkan perbaikan menggunakan mekanisme **Read-Your-Writes (RYW)**. Klien menyimpan *version token/timestamp* setelah melakukan pembaruan saldo di Jakarta. Saat bertransaksi di Bandung, server Bandung menyadari versi lokalnya lebih lama (*outdated*) sehingga melakukan *fetch* data terbaru langsung ke Jakarta sebelum memproses transaksi.

```mermaid

sequenceDiagram
    autonumber
    actor C as Pelanggan (Client)
    participant J as Server Jakarta
    participant B as Server Bandung

    %% Step 1: Top-up di Jakarta
    C->>J: 1. Top-up Saldo (+Rp100.000)
    Note over J: Update Saldo: Rp150.000<br/>Set Version: v2
    J-->>C: 2. Konfirmasi Success + Return Client Token (Version: v2)
    Note over C: Klien menyimpan Client Version = v2

    %% Replikasi Asinkron Terhambat
    J->>B: 3. Replikasi Asinkron (Delay)

    %% Step 2: Transaksi di Bandung dengan RYW
    Note over C,B: Beberapa detik kemudian pelanggan memesan makanan
    C->>B: 4. Buat Pesanan (Bayar Rp50.000) + Pass Client Version (v2)
    
    Note over B: Cek Version Lokal (v1) vs Client Version (v2)<br/>(Versi Lokal Outdated!)
    
    %% Sync Paksa / On-Demand Fetch
    rect rgb(235, 245, 255)
        Note over B,J: Solusi Read-Your-Writes (Sync On-Demand)
        B->>J: 5. Fetch Latest State (Read-Your-Writes Sync)
        J-->>B: 6. Return State Terbaru (Saldo: Rp150.000, Version: v2)
    end

    Note over B: Update Cache Lokal ke v2<br/>Cek Saldo: Rp150.000 >= Rp50.000 (Cukup!)
    B-->>C: 7. Transaksi Berhasil Diproses
```

## 2. Analisis

### 1. Penentuan Model Konsistensi (Sequential vs Eventual) & Dampak Bisnis
Kesimpulan: Eventual Consistency murni TIDAK CUKUP untuk skenario saldo e-wallet FoodGo

Argumen Berbasis Dampak Bisnis:
1. Sensitivitas Finansial vs Aktivitas Sosial (Low-Stakes vs High-Stakes):
    - Sosial Media (Like/Comment): Menggunakan Eventual Consistency. Jika jumlah like terlambat ter-update beberapa detik antara pengguna A dan B, tidak ada kerugian finansial atau dampak sistemik terhadap pengguna
    - E-Wallet (Finansial): Mengolah nilai ekonomi nyata. Ketidaksesuaian data walau hanya berdurasi 2 detik (replication delay) langsung berdampak pada penolakan transaksi (False Rejection)
2. Dampak Operasional dan Kepercayaan Pelanggan (User Experience & Retention):
    - Pengalaman Pengguna Buruk (User Frustration): Pelanggan baru saja memindahkan saldo dari bank ke e-wallet di server Jakarta, namun transaksinya ditolak di server Bandung dengan pesan "Saldo Tidak Cukup"
    - Kehilangan Kepercayaan (Loss of Trust): Pelanggan akan merasa uangnya hilang atau aplikasi mengalami kegagalan fungsi (buggy). Hal ini memicu lonjakan tiket pengaduan ke Customer Service (meningkatkan operational cost) dan memicu perpindahan pengguna (churn rate) ke platform kompetitor
3. Risiko Double Spending:
    - Jika sistem mengizinkan pembacaan saldo lama di server Bandung, ada celah di mana pengguna dapat membelanjakan saldo yang seharusnya sudah terpotong atau diproses di tempat lain sebelum proses replikasi antar-server selesai.

### 2. Usulan Pendekatan Client-Centric Consistency (Read-Your-Writes)
Mengingat memaksakan Sequential Consistency secara global ke seluruh server/replika akan memicu latency tinggi dan menurunkan ketersediaan sistem (availability), pendekatan terbaik adalah mengombinasikan Eventual Consistency pada latar belakang (background replication) dengan jaminan Client-Centric Consistency, khususnya Read-Your-Writes (RYW) Consistency untuk akses dari klien.

Mekanisme Kerja Solusi (Read-Your-Writes):
1. Pemberian Version Token / Timestamp:
    - Setiap kali pelanggan melakukan aksi penulisan data (top-up atau pemotongan saldo) di server Jakarta, server akan meningkatkan versi data pengguna (version) dan mengembalikan token versi tersebut (Client Version = v2) bersama dengan respons sukses ke aplikasi client.
2. Penyimpanan State di Klien:
    - Aplikasi mobile pelanggan menyimpan nilai Client Version = v2 secara lokal
3. Validasi Versi & Sync On-Demand Saat Transaksi:
    - Ketika pelanggan membuat pesanan di server Bandung, aplikasi akan menyertakan Client Version = v2 dalam header request.
    - Server Bandung membandingkan versi lokalnya (v1) dengan Client Version milik klien (v2).
    - Aksi jika outdated: Karena versi lokal Bandung tertinggal (v1 < v2), server Bandung tidak menolak transaksi, melainkan melakukan on-demand fetch / redirect bacaan data terbaru secara instan ke server Jakarta (Master).
    - Setelah mendapatkan data saldo terbaru (v2), transaksi diproses dan dinyatakan berhasil.

Keuntungan Solusi: 
1. Bagi Klien (Pelanggan): Selalu melihat dan menggunakan hasil penulisan (write) terbarunya sendiri secara instan tanpa pernah mengalami inconsistent read.

2. Bagi Sistem (Infrastruktur): Replikasi antar-server tetap dapat berjalan secara asinkron (menghemat bandwidth dan menurunkan latensi secara umum), sementara lalu lintas on-demand sync hanya terjadi saat ada ketidaksesuaian versi klien.
