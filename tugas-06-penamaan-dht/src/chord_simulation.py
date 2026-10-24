"""
Tugas 6 - Simulasi Chord DHT (single-process, tanpa jaringan sungguhan)

Fungsi hashing & struktur data ring sudah disediakan.
Lengkapi TODO untuk lookup(), join(), dan leave().
"""

import hashlib

M_BITS = 8               # ruang identifier 0..255 (disederhanakan dari Chord asli yang pakai 160-bit)
RING_SIZE = 2 ** M_BITS


def hash_id(key: str) -> int:
    """Hash string (ID node atau ID kurir) ke ruang identifier 0..RING_SIZE-1."""
    digest = hashlib.sha1(key.encode()).digest()
    return int.from_bytes(digest, "big") % RING_SIZE


class ChordRing:
    def __init__(self):
        # node_id (hasil hash) -> alamat IP node tersebut
        self.nodes: dict[int, str] = {}
        # key kurir (hasil hash) -> IP kurir yang disimpan node yang bertanggung jawab
        self.data: dict[int, tuple[str, str]] = {}  # hash -> (kurir_id, ip_kurir)

    def join(self, node_name: str, node_ip: str):
        """Tambahkan node baru ke ring. Pindahkan data yang seharusnya
        menjadi tanggung jawab node baru ini dari successor lamanya."""
        node_id = hash_id(node_name)

        # TODO 2: Cari successor LAMA sebelum node baru ditambahkan ke self.nodes
        old_successor_id = self.find_successor(node_id)

        # TODO 1: Tambahkan node_id -> node_ip ke self.nodes
        self.nodes[node_id] = node_ip

        # TODO 3: Log pengambilalihan tanggung jawab key dari successor lama
        print(f"Node '{node_name}' (id={node_id}) bergabung, alamat {node_ip}")
        if old_successor_id is not None and old_successor_id != node_id:
            takeover_keys = []
            for k_hash in list(self.data.keys()):
                if self.find_successor(k_hash) == node_id:
                    kurir_id, _ = self.data[k_hash]
                    takeover_keys.append(kurir_id)
            if takeover_keys:
                print(f"  └─> Mengambil alih data kurir {takeover_keys} dari Node ID {old_successor_id}")

    def leave(self, node_name: str):
        """Keluarkan sebuah node dari ring. Data yang dipegangnya harus
        berpindah ke successor-nya."""
        node_id = hash_id(node_name)
        if node_id not in self.nodes:
            return

        # Catat key yang dikelola oleh node ini sebelum dihapus
        keys_held = [k_hash for k_hash in self.data.keys() if self.find_successor(k_hash) == node_id]

        # TODO 4: Hapus node_id dari self.nodes
        del self.nodes[node_id]
        print(f"Node '{node_name}' (id={node_id}) keluar dari ring")

        # TODO 5: Pindahkan/alihkan tanggung jawab ke successor baru
        if keys_held and self.nodes:
            for k_hash in keys_held:
                new_succ_id = self.find_successor(k_hash)
                kurir_id, _ = self.data[k_hash]
                print(f"  └─> Tanggung jawab data '{kurir_id}' dialihkan ke Node ID {new_succ_id}")

    def find_successor(self, key_hash: int) -> int | None:
        """Cari node_id dengan nilai hash TERKECIL yang >= key_hash
        (successor menurut aturan Chord). Jika tidak ada, wrap-around
        ke node dengan hash terkecil di ring (karena ring melingkar)."""
        # TODO 6: Implementasi logika successor
        if not self.nodes:
            return None
        
        sorted_node_ids = sorted(self.nodes.keys())
        for node_id in sorted_node_ids:
            if node_id >= key_hash:
                return node_id
        
        return sorted_node_ids[0]

    def register_kurir(self, kurir_id: str, ip_kurir: str):
        """Simpan mapping ID Kurir -> IP di node yang bertanggung jawab."""
        key_hash = hash_id(kurir_id)
        # TODO 7: Panggil find_successor(key_hash) dan simpan ke self.data[key_hash]
        succ_id = self.find_successor(key_hash)
        if succ_id is not None:
            self.data[key_hash] = (kurir_id, ip_kurir)

    def lookup(self, kurir_id: str) -> str | None:
        """Cari alamat IP terkini untuk sebuah ID Kurir."""
        key_hash = hash_id(kurir_id)
        # TODO 8: Temukan node penanggung jawab dan kembalikan ip_kurir jika ada
        succ_id = self.find_successor(key_hash)
        if succ_id is not None and key_hash in self.data:
            return self.data[key_hash][1]
        return None


def main():
    ring = ChordRing()

    # Skenario awal: 4 node bergabung
    ring.join("node-jakarta-1", "10.0.0.1")
    ring.join("node-jakarta-2", "10.0.0.2")
    ring.join("node-bandung-1", "10.0.0.3")
    ring.join("node-surabaya-1", "10.0.0.4")

    # Daftarkan beberapa kurir
    ring.register_kurir("kurir-001", "192.168.1.10")
    ring.register_kurir("kurir-002", "192.168.1.11")
    ring.register_kurir("kurir-003", "192.168.1.12")

    print("\n--- Lookup sebelum perubahan topologi ---")
    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))

    print("\n--- Node baru bergabung ---")
    ring.join("node-medan-1", "10.0.0.5")
    print("kurir-001 ->", ring.lookup("kurir-001"))

    print("\n--- Sebuah node keluar ---")
    ring.leave("node-jakarta-1")
    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))


if __name__ == "__main__":
    main()