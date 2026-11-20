"""
Tugas 10 - Load Test Sederhana

Mengirim banyak request konkuren ke Load Balancer (http://localhost:8080)
dan menghitung berapa kali masing-masing instance app menangani request,
untuk membuktikan distribusi beban.
"""

import urllib.request
import threading
import time
from collections import Counter

TARGET_URL = "http://localhost:8080/"
TOTAL_REQUESTS = 300
CONCURRENCY = 30

hasil = Counter()
lock = threading.Lock()
semaphore = threading.Semaphore(CONCURRENCY)


def kirim_request():
    # TODO 1 & TODO 3: batasi thread aktif dengan semaphore, lakukan GET request
    # ke TARGET_URL, baca body response, ekstrak instance_id, lalu update
    # `hasil` secara thread-safe menggunakan `lock`.
    with semaphore:
        try:
            with urllib.request.urlopen(TARGET_URL, timeout=5) as resp:
                body = resp.read().decode("utf-8").strip()

                # TODO 2: ekstrak instance_id dari `body` sesuai format response
                # "Ditangani oleh instance: <INSTANCE_ID>"
                prefix = "Ditangani oleh instance:"
                if prefix in body:
                    instance_id = body.split(prefix, 1)[1].strip()
                else:
                    instance_id = body or "TIDAK_DIKETAHUI"

                with lock:
                    hasil[instance_id] += 1
        except Exception:
            with lock:
                hasil["ERROR"] += 1


def main():
    print(f"Mengirim {TOTAL_REQUESTS} request dengan concurrency {CONCURRENCY} ...")
    start = time.time()

    threads = []
    for _ in range(TOTAL_REQUESTS):
        t = threading.Thread(target=kirim_request)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    durasi = time.time() - start
    print(f"\nSelesai dalam {durasi:.2f} detik")
    print("Distribusi beban per instance:")
    for instance_id, jumlah in hasil.most_common():
        print(f"  {instance_id}: {jumlah} request")


if __name__ == "__main__":
    main()
