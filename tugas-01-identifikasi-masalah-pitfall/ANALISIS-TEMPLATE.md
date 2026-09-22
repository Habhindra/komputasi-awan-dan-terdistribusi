# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** [A Day In My Life]

| Nama | NIM | Kontribusi |
|---|---|---|
| [nama 1] | [nim] | [pitfall/bagian yang dikerjakan] |
| [nama 2] | [nim] | [pitfall/bagian yang dikerjakan] |
| [Muhammad Zaki Oktaruna] | [103072400001] | [Single Point Of Failure / Pitfall 3] |

## Pitfall 1: [nama pitfall] — ditulis oleh [nama]

**Bukti di skenario:** [kutip/paraphrase bagian skenario]

**Kenapa ini keliru:** [penjelasan]

**Dampak ke FoodGo:** [mekanisme kegagalan konkret]

**Solusi desain awal:** [usulan solusi]

**Trade-off:** [apa yang dikorbankan/risiko dari solusi ini]

---

## Pitfall 2: [nama pitfall] — ditulis oleh [nama]

(ulangi struktur di atas)

---

## Pitfall 3: [Single Point Of Failure] — ditulis oleh [Muhammad Zaki Oktaruna]

 ### **Bukti di skenario:** Single Point Of Failure 

    Di skenario dijelasin kalau pas trafik lagi naik, ada satu server yang kewalahan banget. Hal ini kejadian gara-gara semua modul (mulai dari pesanan, pembayaran, sampai notifikasi kurir) 
    dijalanin barengan di satu proses monolitik yang sama persis

### **Kenapa ini keliru:** 

    Bikin sistem gede tapi semuanya digabung di satu tempat itu rawan banget. Ibaratnya nggak ada isolasi atau sekat antar fitur. Kalau ada satu modul aja yang buggy, makan memori (memory leak), atau di-spam request, modul lain yang sebenernya lagi santai bakal ikutan kena getahnya dan bisa bikin seluruh aplikasi mati total

### **Dampak ke FoodGo:**

   Karena semuanya numpuk di satu proses, pas lagi jam sibuk servernya langsung nyerah nahan beban dari semua modul sekaligus. Buntutnya, server backend mengalami crash total. Kalau satu mati, ya mati semua; user nggak bisa pesen, nggak bisa bayar, dan kurir juga nggak dapet notif.

### **Solusi desain awal:**

    Arsitekturnya mending dirombak, dari yang tadinya monolitik dipisah aja (decoupled) jadi Microservices atau dipisah-pisah modulnya. Modul pesanan, pembayaran, dan notifikasi dibikin jalan di service-nya masing-masing. Jadi kalau yang rame cuma fitur pesanan, kita cukup scale up kapasitas server untuk service pesanan aja tanpa harus ngegedein server buat service notifikasi

### **Trade-off:**

    Masalahnya, mecah modul jadi service yang beda-beda itu bikin maintenance kode dan data jadi jauh lebih ribet. Kita harus mikirin gimana cara handle transaksi yang terdistribusi. Misalnya, kalau pesanan udah telanjur kecatat di database service pesanan, tapi ternyata service pembayarannya nolak atau gagal, kita harus ngoding logika tambahan (kayak rollback manual) biar datanya nggak berantakan dan tetep sinkron antar modul
---

## Kesimpulan Kelompok

[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.]
