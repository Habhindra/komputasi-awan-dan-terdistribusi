# Tugas 6— Penamaan DHT

**Kelompok:** [PaperRex]

| Nama | NIM | Kontribusi |
|---|---|---|
| [Rizqullah Izzul Ibad Gheaz] | [103072400033] | [Analisis] |
| [Habhindra Dzaky Alghifary] | [103072400095] | [Testing] |
| [Muhammad Zaki Oktaruna] | [103072400001] | [No 1 dan 3] |

## 1. Rekomendasi Deployment Model: Hybrid Cloud [Zaki]
Berdasarkan analisis ketegangan arsitektural antara tuntutan kedaulatan data mutlak dan elastisitas akses massal, model penyebaran yang paling tepat Hybrid Cloud. Arsitektur ini memisahkan beban kerja secara tegas ke dalam dua segmen terintegrasi: 
- Segmen Private Cloud (Pusat Data Nasional): Dikelola dan dikendalikan sepenuhnya oleh pemerintah untuk menyimpan basis data inti kependudukan (NIK, biodata, dan template biometrik) serta menjalankan mesin pencocokan identitas internal
- Segmen Public Cloud (Lapisan Antarmuka & Komputasi Publik): Berfungsi sebagai lapisan pemrosesan tanpa penyimpanan permanen (stateless compute layer) yang menampung API Gateway, penyeimbang beban (load balancer), dan antarmuka verifikasi bagi ribuan instansi mitraSegmen Public Cloud (Lapisan Antarmuka & Komputasi Publik): Berfungsi sebagai lapisan pemrosesan tanpa penyimpanan permanen (stateless compute layer) yang menampung API Gateway, penyeimbang beban (load balancer), dan antarmuka verifikasi bagi ribuan instansi mitra
## 2. Diagram Ring Topology
1. Rekomendasi Deployment Model & Arsitektur Utama

```mermaid
graph TD
    subgraph Clients ["Public & External Access"]
        C1["Portal Warga (Cek Status / Mandiri)"]
        C2["Instansi / Bank / Polisi (Verifikasi KYC)"]
        C3["Dukcapil Daerah (Petugas Operasional)"]
    end

    subgraph PublicCloud ["Public Cloud Segment (Managed Government Public Cloud)"]
        direction TB
        LB["Global Load Balancer"]
        WAF["Shield / WAF & Auto-Scaling Group"]
        PortalApp["Web Server Portal Status (SaaS / Frontend)"]
        APIGateway["API Gateway Verifikasi KYC (PaaS Level)"]
        Cache["Read-Only Hash Cache / Redis (Tokenized Data)"]
    end

    subgraph Connectivity ["Secure Transit Link"]
        DirectConnect["Dedicated Leased Line / Direct Connect (TLS 1.3 + ZTNA)"]
    end

    subgraph PrivateCloud ["Private Cloud Segment (Sovereign Private Cloud / Data Center Negara)"]
        direction TB
        IntFW["Internal Firewall & ZTNA Controller"]
        CoreMiddleware["Core Middleware / Biometric Matcher Engine (IaaS / PaaS)"]
        
        subgraph DataVault ["Isolated Secure Data Vault"]
            PrimaryDB[("Database Utama Kependudukan (NIK, Alamat, Biometrik Raw)")]
            AuditLog[("Audit & Security Logs")]
        end
    end

    C1 --> LB
    C2 --> LB
    C3 --> LB

    LB --> WAF
    WAF --> PortalApp
    WAF --> APIGateway

    APIGateway <-->|Fast Lookup| Cache
    APIGateway <-->|Verify Request| DirectConnect
    PortalApp <-->|Status Check| DirectConnect

    DirectConnect <--> IntFW
    IntFW <--> CoreMiddleware
    CoreMiddleware <--> PrimaryDB
    CoreMiddleware -. Log Activity .-> AuditLog

    %% Styling Classes Applied at the End
    classDef publicLayer fill:#e1f5fe,stroke:#0288d1,stroke-width:2px,color:#01579b;
    classDef gatewayLayer fill:#fff3e0,stroke:#f57c00,stroke-width:2px,color:#e65100;
    classDef privateLayer fill:#e8f5e9,stroke:#388e3c,stroke-width:2px,color:#1b5e20;
    classDef externalClient fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px,color:#4a148c;

    class C1,C2,C3 externalClient;
    class LB,WAF,PortalApp,APIGateway,Cache publicLayer;
    class DirectConnect gatewayLayer;
    class IntFW,CoreMiddleware,PrimaryDB,AuditLog privateLayer;
```
2. Alur Verifikasi Data & Keamanan
```   
sequenceDiagram
    autonumber
    actor Instansi as Instansi / Bank (Client)
    participant PublicGW as Public Cloud (API Gateway & Cache)
    participant DirectLink as Dedicated Link (TLS 1.3 / ZTNA)
    participant PrivateMW as Private Cloud (Biometric Matcher)
    participant PrivateDB as Database Inti (NIK & Biometrics)

    Instansi->>PublicGW: 1. Request Verifikasi KYC (Tokenized Header)
    alt Cache Hit (Hash Verifikasi Ada)
        PublicGW-->>Instansi: 2a. Return Status (Match / Valid)
    else Cache Miss (Membutuhkan Query Inti)
        PublicGW->>DirectLink: 2b. Forward Encrypted Payload
        DirectLink->>PrivateMW: 3. Authorize via ZTNA & Decrypt
        PrivateMW->>PrivateDB: 4. Match NIK & Data Biometrik Raw
        PrivateDB-->>PrivateMW: 5. Match Result
        PrivateMW-->>DirectLink: 6. Encrypted Verification Response
        DirectLink-->>PublicGW: 7. Response + Update Cache Token
        PublicGW-->>Instansi: 8. Return Status Verified
    end
```
## 3. Analisis Risiko Spesifik & Strategi Mitigasi [Zaki]
Penerapan Hybrid Cloud pada sistem identitas nasional menghadirkan tantangan spesifik terkait perlindungan data kependudukan dan akurasi status warga negara:

Risiko 1: Kebocoran Template Biometrik & Rekonstruksi Identitas pada Jalur Verifikasi KYC
- Skenario Risiko: Saat perbankan atau kepolisian melakukan verifikasi wajah maupun sidik jari secara massal melalui segmen Public Cloud, pengiriman data biometrik mentah melintasi batas jaringan (public-to-private) berisiko mengekspos data biometrik warga. Berbeda dengan kata sandi, data biometrik bersifat permanen seumur hidup dan tidak dapat diganti apabila bocor
- Strategi Mitigasi: Menerapkan Cancelable Biometrics & Feature Extraction di Sisi Klien sebelum permintaan dikirim ke Public Cloud, melalui jalur privat terenkripsi (Dedicated Leased Line dengan Mutual TLS). Proses pencocokan (biometric matching) dilakukan sepenuhnya di dalam Private Cloud negara, sedangkan Public Cloud hanya meneruskan vektor terenkripsi dan mengembalikan skor kecocokan (match score) tanpa pernah menyimpan citra wajah atau NIK mentah

Risiko 2: Inkonsistensi Status Kependudukan (Data Kematian/Perubahan NIK) Saat Lonjakan Pemilu atau PPDB
- Skenario Risiko: Pembaruan data penduduk (seperti pencatatan kematian, perubahan domisili, atau status hak pilih oleh Dukcapil daerah) berlangsung langsung di Private Cloud. Apabila lapisan cache pada API Gateway di Public Cloud terlambat tersinkronisasi saat beban akses memuncak, identitas penduduk yang sudah tidak berlaku berpotensi lolos proses verifikasi pemilu atau seleksi sekolah
- Strategi Mitigasi: Menerapkan mekanisme Event-Driven Cache Invalidation berbasis Change Data Capture (CDC) dari basis data inti di Private Cloud menuju lapisan API Gateway. Setiap perubahan status krusial warga negara secara otomatis memicu penghapusan token verifikasi lama dalam hitungan milidetik (near real-time) tanpa perlu mentransfer rincian data pribadi ke segmen publik
