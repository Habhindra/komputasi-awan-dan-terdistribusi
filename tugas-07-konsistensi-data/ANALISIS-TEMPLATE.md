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
    J--)B: 3. Replikasi Asinkron (Terhambat / Delay)
    
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

    2.Skenario Dengan Solusi Client-Centric
    Skenario ini menunjukkan perbaikan menggunakan mekanisme **Read-Your-Writes (RYW)**. Klien menyimpan *version token/timestamp* setelah melakukan pembaruan saldo di Jakarta. Saat bertransaksi di Bandung, server Bandung menyadari versi lokalnya lebih lama (*outdated*) sehingga melakukan *fetch* data terbaru langsung ke Jakarta sebelum memproses transaksi.

    ```markdown
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
    J--)B: 3. Replikasi Asinkron (Delay)

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
    


## 2. 