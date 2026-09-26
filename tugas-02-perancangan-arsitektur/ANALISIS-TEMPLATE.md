# Tugas 2 — Perancangan Arsitektur

**Kelompok:** [PaperRex]

| Nama | NIM | Kontribusi |
|---|---|---|
| [Rizqullah Izzul Ibad Gheaz] | [103072400033] | [] |
| [Habhindra Dzaky Alghifary] | [103072400095] | [] |
| [Muhammad Zaki Oktaruna] | [103072400001] | [] |

## Soal 1 — ditulis oleh []

**Bukti di skenario:**
"Aplikasi jadi sangat lambat, beberapa permintaan timeout."
"(modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu)."

**Kenapa ini keliru:**
Mengasumsikan latency is zero yaitu menganggap komunikasi antar layanan berjalan secara instan tanpa penundaan waktu transpor data. Pada nyatanya, pengiriman pesan atau panggilan antar layanan membutuhkan waktu siklus. Ketika sistem menangani beban tinggi, latency jaringan akan membesar. Menunggu respons tanpa batas waktu mengabaikan fakta bahwa latency itu ada dan bisa membengkak drastis saat trafik melonjak. 

**Dampak ke FoodGo:**
- Penumpukan Thread/Resource Locking: Karena modul pesanan menunggu modul pembayaran tanpa batas waktu, thread server terus tertahan menunggu respons.
- Cascading Slowdown & Timeout: Penundaan pada satu modul merembet ke seluruh sistem, membuat aplikasi menjadi sangat lambat dan permintaan pengguna mengalami timeout.
- Kehabisan Memori/Resource: Antrean proses yang menggantung terus menumpuk hingga akhirnya membuat server backend crash total dan harus direstart manual.  

**Solusi desain awal:**
- Terapkan Timeout Eksplisit: Tetapkan batas waktu maksimum menunggu respons (misalnya 2-3 detik) pada pemanggilan antar modul/layanan. Jika batas waktu terlampaui, pemanggilan langsung digagalkan secara aman.
- Komunikasi Asinkron: Gunakan sistem antrean untuk proses yang tidak membutuhkan jawaban cepat agar modul pengirim tidak perlu menunggu.
- Pola Circuit Breaker: Hentikan sementara pemanggilan ke modul yang sedang lambat/bermasalah agar penumpukan thread tidak merambat ke modul lainnya.

**Trade-off:**
- Kompleksitas Kode & Penanganan Error: Aplikasi harus siap menangani skenario kegagalan dengan lebih jelas seperti menampilkan pesan error yang ramah atau mekanisme pemesanan ulang.
- Konsistensi Data: Mengalihkan proses menjadi asinkron berarti data mungkin tidak langsung update secara real-time, melainkan membutuhkan jeda beberapa saat sampai proses di latar belakang selesai.

---

## Soal 2 — ditulis oleh []

**Bukti di skenario:** [The Network is Reliable]
Tim menemukan bahwa kode mereka menulis asumsi seperti # network is always reliable, no need for retry dan tidak ada timeout sama sekali pada pemanggilan antar service (modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu).

**Kenapa ini keliru:** 
Di dunia nyata jaringan tidak pernah 100% stabil.bisa jadi gangguan fisik,packet loss,latensi yang melonjak atau gangguan yang terjadi di router.jadi aplikasi akan lag saat koneksi atau jaringan terputus

**Dampak ke FoodGo:** 
Saat modul pembayaran mengalami keterlambatan atau gangguan, proses di modul pesanan akan terus menunggu secara blocking tanpa batas waktu. Akibatnya, alokasi thread di server cepat habis, sehingga pesanan baru gagal diproses, aplikasi jadi sangat lambat, dan berujung pada timeout ke seluruh pengguna

**Solusi desain awal:** 
Mengonfigurasi batas waktu,ditambah dengan retry berpola exponential backoff dan circuit breaker untuk melindungi sistem dari lonjakan beban saat terjadi gangguan

**Trade-off:** 
Jika retry dilakukan secara sembarangan tanpa jeda yang jelas, server tujuan yang tadinya mau bangkit malah bisa langsung tumbang lagi gara-gara lonjakan permintaan secara bersamaan.

---

## Soal 3 — ditulis oleh []

**Bukti di skenario:** Single Point Of Failure 
Berdasarkan skenario FoodGo, ditemukan masalah saat terjadi lonjakan trafik di mana satu server menjadi sangat kewalahan karena harus menangani seluruh modul (pesanan, pembayaran, dan notifikasi kurir) yang digabung dalam satu proses monolitik yang sama

**Kenapa ini keliru:** 
Pendekatan desain ini sangat berisiko untuk sistem berskala besar karena tidak adanya isolasi sumber daya (resource isolation). Jika semua fungsi aplikasi dijalankan dalam satu proses, masalah pada satu fungsi tunggal (misalnya penggunaan memori atau CPU yang berlebih) akan berdampak langsung pada kinerja fungsi-fungsi lainnya, sehingga sistem menjadi rentan tumbang secara keseluruhan

**Dampak ke FoodGo:**
Karena semua operasional menumpuk di satu tempat, beban komputasi yang tinggi dari satu alur kerja menyebabkan server tidak mampu lagi memproses request apa pun. Hal ini memicu crash total pada server backend, yang berarti seluruh layanan (pemesanan, pembayaran, dan sistem kurir) lumpuh total secara bersamaan

**Solusi desain awal:**
Kami mengusulkan pemisahan arsitektur monolitik tersebut menjadi arsitektur berbasis Microservices atau layanan yang terdistribusi. Modul pesanan, pembayaran, dan notifikasi harus dipisah menjadi service yang berdiri sendiri. Dengan isolasi ini, jika trafik pemesanan sedang tinggi, sistem hanya perlu melakukan scaling up pada service pesanan saja menggunakan Load Balancer, tanpa membebani modul lainnya

**Trade-off:**
Pemisahan service ini mengorbankan kesederhanaan sistem dan meningkatkan kompleksitas pengelolaan data. Tim pengembang kini harus merancang mekanisme penanganan transaksi terdistribusi untuk menjaga konsistensi data. Sebagai contoh, sistem memerlukan logika tambahan seperti kompensasi transaksi atau rollback otomatis apabila modul pesanan berhasil memproses pesanan, namun pemanggilan ke modul pembayaran berujung gagal

---

## Soal 4 — ditulis oleh []

## Kesimpulan Kelompok

Secara garis besar, kegagalan sistem FoodGo disebabkan oleh kombinasi asumsi jaringan yang keliru (Latency is Zero dan The Network is Reliable) serta desain arsitektur monolitik tanpa isolasi (Single Point of Failure). Jika FoodGo memperbaiki ketiga pitfall ini, arsitektur yang disarankan adalah Arsitektur Microservices berbasis Event-Driven (Event-Driven Microservices Architecture)
