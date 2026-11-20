# Tugas 6— Penamaan DHT

**Kelompok:** [PaperRex]

| Nama | NIM | Kontribusi |
|---|---|---|
| [Rizqullah Izzul Ibad Gheaz] | [103072400033] | [Analisis] |
| [Habhindra Dzaky Alghifary] | [103072400095] | [2. Diagram ] |
| [] | [] | [] |

## 1. Rekomendasi Deployment Model: Hybrid Cloud []

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
```
2. Alur Verifikasi Data & Keamanan
```mermaid
sequenceDiagram
    autonumber
    actor Instansi as Instansi / Bank Client
    participant PublicGW as Public Cloud API Gateway & Cache
    participant DirectLink as Dedicated Link TLS 1.3 / ZTNA
    participant PrivateMW as Private Cloud Biometric Matcher
    participant PrivateDB as Database Inti NIK & Biometrics

    Instansi->>PublicGW: Request Verifikasi KYC Tokenized Header
    alt Cache Hit (Hash Verifikasi Ada)
        PublicGW-->>Instansi: Return Status Match / Valid
    else Cache Miss (Membutuhkan Query Inti)
        PublicGW->>DirectLink: Forward Encrypted Payload
        DirectLink->>PrivateMW: Authorize via ZTNA & Decrypt
        PrivateMW->>PrivateDB: Match NIK & Data Biometrik Raw
        PrivateDB-->>PrivateMW: Match Result
        PrivateMW-->>DirectLink: Encrypted Verification Response
        DirectLink-->>PublicGW: Response + Update Cache Token
        PublicGW-->>Instansi: Return Status Verified
    end
```
