
import random
import time
import os
from multiprocessing import Pool

# Fungsi untuk perkalian serial
def perkalian_serial(a, b):
    hasil = []

    for i in range(len(a)):
        baris = []

        for j in range(len(b[0])):
            total = 0

            for k in range(len(b)):
                total += a[i][k] * b[k][j]

            baris.append(total)

        hasil.append(baris)

    return hasil


# Variabel untuk menyimpan matriks B
matriks_b_global = []

# Menyiapkan matriks B untuk setiap proses
def persiapan_worker(b):
    global matriks_b_global
    matriks_b_global = b


# Menghitung satu baris matriks
def hitung_baris(baris_a):
    hasil_baris = []

    for j in range(len(matriks_b_global[0])):
        total = 0

        for k in range(len(matriks_b_global)):
            total += baris_a[k] * matriks_b_global[k][j]

        hasil_baris.append(total)

    return hasil_baris


# Fungsi perkalian paralel
def perkalian_paralel(a, b):
    jumlah_proses = min(os.cpu_count() or 2, 4)

    with Pool(
        processes=jumlah_proses,
        initializer=persiapan_worker,
        initargs=(b,)
    ) as pool:
        hasil = pool.map(hitung_baris, a)

    return hasil


# Program utama
if __name__ == "__main__":

    ukuran = 300

    # Membuat dua matriks
    matriks_a = [
        [random.randint(1, 9) for j in range(ukuran)]
        for i in range(ukuran)
    ]

    matriks_b = [
        [random.randint(1, 9) for j in range(ukuran)]
        for i in range(ukuran)
    ]

    # Pengujian serial
    print("=== PERKALIAN MATRIKS SERIAL ===")

    mulai = time.perf_counter()
    hasil_serial = perkalian_serial(matriks_a, matriks_b)
    waktu_serial = time.perf_counter() - mulai

    print("Waktu Serial:", waktu_serial, "detik")

    # Pengujian paralel
    print("\n=== PERKALIAN MATRIKS PARALEL ===")

    mulai = time.perf_counter()
    hasil_paralel = perkalian_paralel(matriks_a, matriks_b)
    waktu_paralel = time.perf_counter() - mulai

    print("Waktu Paralel:", waktu_paralel, "detik")

    # Membandingkan hasil
    print("\n=== HASIL PENGUJIAN ===")

    if hasil_serial == hasil_paralel:
        print("Hasil kedua metode SAMA")
    else:
        print("Hasil kedua metode BERBEDA")

    print("\nContoh hasil matriks 3 x 3:")

    for baris in hasil_serial[:3]:
        print(baris[:3])

    print("\n=== KESIMPULAN WAKTU ===")

    if waktu_paralel < waktu_serial:
        print("Paralel lebih cepat.")
    else:
        print("Serial lebih cepat atau sama.")
