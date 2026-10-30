"""
Tugas 7 (opsional) - Simulasi Replikasi Dua Server (Jakarta & Bandung)

Mensimulasikan delay replikasi dan masalah inconsistent read,
lalu memperbaikinya dengan mekanisme Read-Your-Writes sederhana.
"""

import time
import threading

REPLICATION_DELAY = 2.0  # detik, simulasi lambatnya sinkronisasi antar server


class Replica:
    def __init__(self, name: str):
        self.name = name
        self.saldo: dict[str, float] = {}
        self.last_write_version: dict[str, int] = {}

    def write(self, user_id: str, saldo_baru: float, version: int):
        self.saldo[user_id] = saldo_baru
        self.last_write_version[user_id] = version
        print(f"[{self.name}] WRITE saldo {user_id} = {saldo_baru} (versi {version})")

    def read(self, user_id: str) -> float:
        return self.saldo.get(user_id, 0.0)
        
    def get_version(self, user_id: str) -> int:
        return self.last_write_version.get(user_id, 0)


class ReplicationSystem:
    def __init__(self):
        self.jakarta = Replica("Jakarta")
        self.bandung = Replica("Bandung")
        self.version_counter = 0

    def top_up(self, user_id: str, jumlah: float):
        """Top-up selalu ditulis dulu ke server Jakarta (mis. server terdekat pelanggan)."""
        self.version_counter += 1
        version = self.version_counter
        saldo_baru = self.jakarta.read(user_id) + jumlah
        self.jakarta.write(user_id, saldo_baru, version)

        # TODO 1: Replikasi ke Bandung tertunda menggunakan threading.Timer
        def replicate_to_bandung():
            self.bandung.write(user_id, saldo_baru, version)
            
        timer = threading.Timer(REPLICATION_DELAY, replicate_to_bandung)
        timer.start()
        print(f"[TODO] Replikasi ke Bandung akan tertunda {REPLICATION_DELAY} detik")

    def baca_saldo_naif(self, user_id: str, server: str) -> float:
        """Baca saldo TANPA mekanisme Read-Your-Writes - bisa saja stale."""
        replica = self.jakarta if server == "Jakarta" else self.bandung
        return replica.read(user_id)

    def baca_saldo_read_your_writes(self, user_id: str, server: str, versi_minimal: int) -> float:
        """TODO 2: Implementasi Read-Your-Writes 
        Jika replika yang dituju versinya masih di bawah versi_minimal,
        kita tunggu atau arahkan (redirect) ke Jakarta yang sudah pasti sinkron.
        """
        replica = self.jakarta if server == "Jakarta" else self.bandung
        
        # Sederhana: Polling sampai replika mengejar versi minimal, atau redirect ke Jakarta
        while replica.get_version(user_id) < versi_minimal:
            print(f"[{server}] Versi data masih basi ({replica.get_version(user_id)} < {versi_minimal}). Menunggu sinkronisasi/mengalihkan ke Jakarta...")
            # Alternatif solusi: Redirect langsung ke master (Jakarta) agar instan
            replica = self.jakarta 
            time.sleep(0.2)
            
        return replica.read(user_id)


def main():
    system = ReplicationSystem()
    user_id = "user1"

    print("=== Skenario NAIF (tanpa Read-Your-Writes) ===")
    system.top_up(user_id, 50000)
    time.sleep(0.5)  # pelanggan langsung pesan makanan < REPLICATION_DELAY detik kemudian
    print("Baca saldo dari Bandung (naif):", system.baca_saldo_naif(user_id, "Bandung"))
    print("-> Harusnya 50000, tapi karena delay replikasi, hasilnya bisa 0 (BUG)\n")

    # Tunggu replikasi selesai sepenuhnya sebelum lanjut ke skenario berikutnya
    time.sleep(REPLICATION_DELAY + 0.5)

    print("\n=== Skenario dengan Read-Your-Writes ===")
    system.top_up(user_id, 20000)
    versi_terakhir = system.version_counter
    
    # TODO 3: panggil baca_saldo_read_your_writes dan tunjukkan hasilnya SELALU benar
    saldo_terbaru = system.baca_saldo_read_your_writes(user_id, "Bandung", versi_terakhir)
    print(f"Baca saldo dengan Read-Your-Writes (segera < {REPLICATION_DELAY} detik): {saldo_terbaru}")
    print("-> Hasilnya TETAP BENAR karena sistem mendeteksi versi dan mengarahkan/menunggu data sinkron.")


if __name__ == "__main__":
    main()