# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** [PaperRex]

| Nama | NIM | Kontribusi |
|---|---|---|
| [nama 1] | [nim] | [pitfall/bagian yang dikerjakan] |
| [Habhindra Dzaky Alghifary] | [103072400095] | [The Network is Reliable/Pitfall 2] |
| [Muhammad Zaki Oktaruna] | [103072400001] | [Single Point Of Failure / Pitfall 3] |

## Pitfall 1: [nama pitfall] — ditulis oleh [nama]

**Bukti di skenario:** [kutip/paraphrase bagian skenario]

**Kenapa ini keliru:** [penjelasan]

**Dampak ke FoodGo:** [mekanisme kegagalan konkret]

**Solusi desain awal:** [usulan solusi]

**Trade-off:** [apa yang dikorbankan/risiko dari solusi ini]

---

## Pitfall 2: [The Network is Reliable] — ditulis oleh [Habhindra Dzaky Alghifary]

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

## Pitfall 3: [Single Point Of Failure] — ditulis oleh [Muhammad Zaki Oktaruna]

 ### **Bukti di skenario:** Single Point Of Failure 

    Berdasarkan skenario FoodGo, ditemukan masalah saat terjadi lonjakan trafik di mana satu server menjadi sangat kewalahan karena harus menangani seluruh modul (pesanan, pembayaran, dan notifikasi kurir) yang digabung dalam satu proses monolitik yang sama

### **Kenapa ini keliru:** 

    Pendekatan desain ini sangat berisiko untuk sistem berskala besar karena tidak adanya isolasi sumber daya (resource isolation). Jika semua fungsi aplikasi dijalankan dalam satu proses, masalah pada satu fungsi tunggal (misalnya penggunaan memori atau CPU yang berlebih) akan berdampak langsung pada kinerja fungsi-fungsi lainnya, sehingga sistem menjadi rentan tumbang secara keseluruhan

### **Dampak ke FoodGo:**

   Karena semua operasional menumpuk di satu tempat, beban komputasi yang tinggi dari satu alur kerja menyebabkan server tidak mampu lagi memproses request apa pun. Hal ini memicu crash total pada server backend, yang berarti seluruh layanan (pemesanan, pembayaran, dan sistem kurir) lumpuh total secara bersamaan

### **Solusi desain awal:**

    Kami mengusulkan pemisahan arsitektur monolitik tersebut menjadi arsitektur berbasis Microservices atau layanan yang terdistribusi. Modul pesanan, pembayaran, dan notifikasi harus dipisah menjadi service yang berdiri sendiri. Dengan isolasi ini, jika trafik pemesanan sedang tinggi, sistem hanya perlu melakukan scaling up pada service pesanan saja menggunakan Load Balancer, tanpa membebani modul lainnya

### **Trade-off:**

    Pemisahan service ini mengorbankan kesederhanaan sistem dan meningkatkan kompleksitas pengelolaan data. Tim pengembang kini harus merancang mekanisme penanganan transaksi terdistribusi untuk menjaga konsistensi data. Sebagai contoh, sistem memerlukan logika tambahan seperti kompensasi transaksi atau rollback otomatis apabila modul pesanan berhasil memproses pesanan, namun pemanggilan ke modul pembayaran berujung gagal
---

## Kesimpulan Kelompok

[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.]
