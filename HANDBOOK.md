# Handbook Mahasiswa — Sistem Terdistribusi & Komputasi Awan

Panduan ini menjelaskan **cara teknis** mengerjakan seluruh tugas di repo ini: dari nol (belum pernah pakai Git) sampai submit tugas terakhir. Baca Bagian 1–3 sekali di awal semester. Bagian 4 dst jadi referensi tiap kali mengerjakan tugas baru.

---

## 1. Setup Laptop (sekali di awal semester)

Semua tool di bawah **gratis** dan cukup diinstal sekali di laptop kalian.

### 1.1 Git & Akun GitHub

- Install Git: [git-scm.com](https://git-scm.com/downloads) (Mac biasanya sudah ada lewat Xcode Command Line Tools: `xcode-select --install`).
- Buat akun di [github.com](https://github.com) kalau belum punya (satu akun per kelompok cukup, atau tiap anggota punya akun sendiri dan collaborator di repo fork).
- Set identitas Git di laptop:
  ```bash
  git config --global user.name "Nama Kalian"
  git config --global user.email "email@kalian.com"
  ```

### 1.2 Docker Desktop

Dipakai untuk mensimulasikan container, VM, load balancer, message broker — semuanya **lokal**, tanpa server sungguhan.

- Download di [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/) (Mac/Windows/Linux).
- Verifikasi instalasi:
  ```bash
  docker --version
  docker compose version
  ```
- Kalau laptop RAM ≤ 8GB, batasi resource Docker Desktop di Settings → Resources (mis. 2–4GB RAM untuk Docker) agar laptop tidak lag.

### 1.3 Python 3

- Cek versi (biasanya sudah ada di Mac/Linux): `python3 --version`. Kalau belum ada / versi terlalu lama, install dari [python.org](https://www.python.org/downloads/).
- Selalu pakai **virtual environment** per tugas supaya dependency antar tugas tidak bentrok:
  ```bash
  python3 -m venv venv
  source venv/bin/activate        # Mac/Linux
  venv\Scripts\activate           # Windows
  pip install -r requirements.txt
  ```

### 1.4 Editor

Pakai editor apa saja (VS Code disarankan, gratis, punya extension Docker & Python resmi).

---

## 2. Fork, Clone, dan Alur Kerja Kelompok

### 2.1 Fork Repositori

1. Buka repo asal di GitHub, klik tombol **Fork** (pojok kanan atas) → pilih akun kelompok.
2. Clone hasil fork ke laptop:
   ```bash
   git clone https://github.com/<akun-kelompok>/<nama-repo>.git
   cd <nama-repo>
   ```

### 2.2 Alur Kerja per Tugas (untuk semua anggota kelompok)

Supaya commit history mencerminkan kontribusi tiap orang (dicek sesuai [`RUBRIK-UMUM.md`](RUBRIK-UMUM.md)), setiap anggota **push dari laptop masing-masing** — bukan satu orang mengetik semua lalu commit atas nama sendiri.

```bash
# tiap kali mulai kerja
git pull origin main

# setelah selesai satu bagian kecil (bukan nunggu 100% selesai)
git add tugas-03-multithreading-container/
git commit -m "Tugas 3: implementasi worker thread untuk simulasi pesanan"
git push origin main
```

Kalau kelompok mau lebih rapi, boleh pakai branch per anggota (`git checkout -b nama-fitur`) lalu merge — tapi tidak wajib, yang wajib adalah **commit atas nama masing-masing** dan **bertahap**, bukan satu commit besar di menit-menit terakhir.

### 2.3 Menulis `JURNAL.md`

Ini bukan laporan formal — ini catatan proses, boleh berantakan. Contoh isi yang baik:

```markdown
## Hari 1
Coba pakai `threading.Thread` langsung tanpa lock, ternyata race condition
di penghitung total pesanan (angka akhir sering meleset).

## Hari 2
Ketemu solusinya: pakai `threading.Lock()` di sekitar increment counter.
Sempat coba `Queue` dulu tapi malah bikin ribet untuk kasus ini.
```

Jurnal seperti ini justru jadi bukti kuat kerja asli — hindari menulis ulang jurnal jadi rapi/formal di akhir, karena itu terlihat dibuat-buat.

### 2.4 Cara Pakai AI di Level 2 (Boleh, Tapi Terbatas)

Mata kuliah ini memakai kebijakan **Level 2 — AI Assisted Idea Generation & Structuring** dari kerangka 5-Level Penggunaan AI Telkom University:

| Level | Nama | Berlaku di mata kuliah ini? |
|---|---|---|
| 1 | No AI | Tidak — AI boleh dipakai untuk ideation/structuring |
| **2** | **AI Assisted Idea Generation & Structuring** | **Ya, ini levelnya** |
| 3 | AI Editing | Tidak — AI tidak boleh mengedit/memperbaiki kode atau tulisan kalian |
| 4 | AI Task Completion with Human Evaluation | Tidak — AI tidak boleh menyelesaikan tugas walau nanti dicek manusia |
| 5 | Full AI | Tidak |

**Contoh pemakaian yang BOLEH (Level 2):**
- "Apa saja pendekatan umum untuk menyelesaikan race condition di Python?" (mencari opsi/ide, bukan minta kode jadi)
- "Bantu saya susun outline/kerangka untuk laporan analisis pitfall ini, bagian apa saja yang biasanya dibahas?" (structuring, bukan isi)
- "Apa saja komponen yang biasanya ada di arsitektur pub-sub?" (brainstorming konsep sebelum menggambar sendiri)

**Contoh pemakaian yang TIDAK BOLEH:**
- "Tuliskan kode Python untuk `order_simulator.py` sesuai skeleton ini" (AI menghasilkan isi akhir)
- "Perbaiki bug di kode saya ini" (ini Level 3 — AI Editing)
- "Buatkan analisis lengkap pitfall FoodGo" atau "Tuliskan README saya" (AI menghasilkan konten akhir yang tinggal disalin)
- Menempelkan output AI apa adanya ke `README.md`/kode tanpa menuliskannya ulang dengan pemahaman sendiri

**Wajib dicatat:** setiap kali AI dipakai (walau cuma untuk brainstorming), catat di bagian **"Log Penggunaan AI"** di `JURNAL.md` tugas terkait — tools yang dipakai, prompt yang diberikan, ringkasan saran AI, dan bagaimana kalian mengolahnya jadi keputusan/tulisan/kode sendiri. Kosongkan (tulis "Tidak memakai AI") jika memang tidak dipakai. Lihat [`RUBRIK-UMUM.md`](RUBRIK-UMUM.md) untuk konsekuensi jika ditemukan pelanggaran batas Level 2 (mis. konten akhir yang terbukti hasil generate AI tanpa diolah ulang).

### 2.5 Cara Submit Tugas: Git Tag + Link ke LMS (Moodle)

Submission **tidak** memakai Pull Request. Karena satu repo fork dipakai terus-menerus untuk 15 tugas sepanjang semester, PR ke repo asal akan menumpuk dan sulit dipisah per minggu. Sebagai gantinya, tiap tugas diselesaikan dengan membuat **git tag** yang menandai commit final tugas tersebut, lalu link ke tag itu yang dikumpulkan ke Moodle.

**Kenapa tag, bukan PR:** tag membuat snapshot commit yang presisi dan tidak berubah (*immutable*) — bukti nyata kondisi repo kalian tepat di titik deadline, tanpa mengotori repo asal dosen dengan ratusan PR yang tidak pernah di-merge.

#### Langkah-langkah

1. Pastikan semua perubahan untuk tugas tersebut sudah di-commit dan di-push ke `main`.
2. Buat tag dengan format **`tugas-XX-submit`** (ganti `XX` dengan nomor tugas 2 digit):
   ```bash
   git tag tugas-03-submit
   git push origin tugas-03-submit
   ```
3. (Opsional, disarankan) Jadikan tag tersebut sebuah **GitHub Release** — lewat halaman **Releases → Draft a new release** di GitHub (pilih tag `tugas-03-submit`), atau via CLI:
   ```bash
   gh release create tugas-03-submit --title "Tugas 03" --notes "Submission Tugas 03"
   ```
4. Salin link **halaman tag/release** (format `releases/tag/<nama-tag>`), **bukan** link folder/file (`tree/...` atau `blob/...`):
   ```
   https://github.com/<akun-kelompok>/<nama-repo>/releases/tag/tugas-03-submit
   ```
   Link ini tetap valid walaupun belum dibuat Release — GitHub akan menampilkan halaman tag beserta commit yang ditunjuknya.
5. Tempel link tersebut ke kolom submission (Online text/URL) di **assignment Moodle** untuk tugas yang bersangkutan.

> ❌ **Salah:** `https://github.com/<akun-kelompok>/<nama-repo>/tree/tugas-03-submit/tugas-03-multithreading-container` (link tree folder)
> ❌ **Salah:** `https://github.com/<akun-kelompok>/<nama-repo>/tree/main/...` (link branch, isinya terus berubah)
> ✅ **Benar:** `https://github.com/<akun-kelompok>/<nama-repo>/releases/tag/tugas-03-submit`

#### Contoh Konkret

Misal kelompok kalian bernama `kelompok7-foodgo`, repo hasil fork bernama `komputasi-awan`, dan sedang mengumpulkan Tugas 5:

```bash
git tag tugas-05-submit
git push origin tugas-05-submit
```

Link yang ditempel ke Moodle:
```
https://github.com/kelompok7-foodgo/komputasi-awan/releases/tag/tugas-05-submit
```

Dari halaman tag/release ini dosen/asisten bisa melihat commit yang ditandai, mengunduh snapshot repo (zip/tar.gz) **persis seperti saat kalian submit**, lalu menelusuri folder `tugas-05-koordinasi-konsensus/` pada tag tersebut.

#### Kalau Perlu Revisi Sebelum Deadline

Tag yang sudah di-push bisa dipindah ke commit terbaru (selama masih sebelum deadline):
```bash
git tag -f tugas-05-submit          # pindahkan tag ke commit HEAD saat ini
git push origin tugas-05-submit --force
```
Link yang sudah ditempel di Moodle **tidak perlu diganti** — link `releases/tag/tugas-05-submit` otomatis menunjuk ke posisi tag yang baru. (Jika sudah membuat Release, Release tersebut ikut menunjuk ke tag yang dipindah; cek kembali halamannya setelah push.)

Setelah deadline lewat, jangan pindahkan tag lagi — commit setelah deadline dianggap di luar submission (kecuali ada kebijakan terlambat dari dosen).

---

## 3. Konsep Teknis yang Dipakai Berulang

### 3.1 Menjalankan Beberapa "Node" di Satu Laptop

Banyak tugas (Tugas 5, 6, 10, 15) minta simulasi beberapa node/server. Dua cara termudah:

**Cara A — beberapa proses Python di port berbeda** (paling sederhana, dipakai di Tugas 5 & 6):
```bash
python3 node.py --port 5001 --id 1
python3 node.py --port 5002 --id 2
# ...buka terminal tab baru untuk tiap node
```

**Cara B — Docker Compose** (dipakai di Tugas 3, 4, 10, 11, 15) — satu file `docker-compose.yml` menjalankan banyak "server" sekaligus:
```bash
docker compose up --build      # jalankan semua service
docker compose logs -f         # lihat log semua service
docker compose down            # matikan semua
```

### 3.2 Docker Dasar (dipakai mulai Tugas 3)

```bash
docker build -t nama-image .          # build image dari Dockerfile
docker run -p 8000:8000 nama-image    # jalankan, map port 8000 laptop ke 8000 container
docker ps                             # lihat container yang jalan
docker logs <container-id>            # lihat output/log
docker stop <container-id>
```

### 3.3 Cara Ambil Screenshot/Video Demo (`bukti/`)

- **Screenshot terminal**: pastikan prompt terminal (nama user@hostname) ikut kefoto — jadi bukti itu jalan di laptop kalian, bukan tempel dari internet.
- **Video demo**: rekam layar 1–3 menit (Mac: `Cmd+Shift+5`, Windows: Xbox Game Bar `Win+G`, Linux: `SimpleScreenRecorder`/OBS). Tidak perlu diedit — cukup jelas terlihat command dijalankan dan hasilnya.
- Simpan di folder `bukti/` masing-masing tugas. Video besar cukup ditaruh link Google Drive/YouTube unlisted di `README.md` (jangan commit file video >50MB ke Git).

### 3.4 Troubleshooting Umum

| Masalah | Solusi |
|---|---|
| `docker compose` tidak dikenali | Update Docker Desktop, versi lama pakai `docker-compose` (dengan strip) |
| Port sudah dipakai (`address already in use`) | Ganti port di command/`docker-compose.yml`, atau `lsof -i :PORT` untuk cari & matikan proses lama |
| Container langsung exit | Cek `docker logs <container-id>` untuk lihat error |
| `git push` ditolak (`rejected`) | Jalankan `git pull origin main` dulu, selesaikan konflik, baru push lagi |
| Laptop lemot saat Docker jalan | Kurangi jumlah service yang jalan bersamaan, batasi RAM Docker Desktop |

---

## 4. Alur Umum Mengerjakan Satu Tugas

1. Baca `README.md` di folder `tugas-XX-.../` — pahami studi kasus dan **apa yang harus dihasilkan**.
2. Diskusi kelompok: bagi peran (siapa pegang bagian mana), catat di tabel kontribusi.
3. Kerjakan bertahap, commit tiap kali ada progres kecil, update `JURNAL.md`.
4. Jalankan/uji hasilnya secara nyata di laptop — jangan cuma menulis kode yang tidak pernah dieksekusi.
5. Ambil bukti (screenshot/video) di folder `bukti/`.
6. Tulis analisis akhir di `README.md` submission (kenapa solusi ini, apa trade-off-nya, apa yang akan diperbaiki kalau ada waktu lagi).
7. Buat git tag `tugas-XX-submit`, push, lalu kumpulkan link halaman tag/release-nya (`.../releases/tag/tugas-XX-submit`, bukan link `tree/` folder) ke assignment Moodle terkait (lihat [2.5](#25-cara-submit-tugas-git-tag--link-ke-lms-moodle)).

Selamat mengerjakan!
