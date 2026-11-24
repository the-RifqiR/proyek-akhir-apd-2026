# admin.py

from data import *
from utiliti import (
    clear,
    enter_kembali,
    pilih_divisi,
    konfirmasi,
    menu_admin)
from prettytable import PrettyTable
from colorama import Fore, Style
from external import simpan_data

# READ + KONFIRMASI
def lihat_pendaftar():
    while True:

        print("\n=== DAFTAR DATA PENDAFTAR ===")

        if not data_pendaftars_divisi:
            print("Belum ada data pendaftar.")
            enter_kembali()
            return

        tabel = PrettyTable()
        tabel.field_names = [
            "No",
            "Nama",
            "Divisi 1",
            "Divisi 2",
            "Divisi 3",
            "Status",
            "Diterima"
        ]

        for i, pendaftar in enumerate(data_pendaftars_divisi):
            tabel.add_row([
                i + 1,
                pendaftar["nama"],
                pendaftar["pilihan_divisi"][0],
                pendaftar["pilihan_divisi"][1],
                pendaftar["pilihan_divisi"][2],
                pendaftar["status"],
                pendaftar["divisi_diterima"]
            ])

        print(tabel)

        while True:
            pilihan = input(
                "\nMasukkan nomor pendaftar atau 'kembali': "
            ).strip()

            if pilihan.lower() == "kembali":
                return

            try:
                nomor = int(pilihan)

                if 1 <= nomor <= len(data_pendaftars_divisi):
                    break
                else:
                    print("Nomor pendaftar tidak tersedia.")

            except ValueError:
                print("Input harus berupa angka.")

        pendaftar = data_pendaftars_divisi[nomor - 1]

        clear()
        print("\n=== DETAIL PENDAFTAR ===")
        print(f"Nama : {pendaftar['nama']}")
        print(f"NIM : {pendaftar['nim']}\n")
        for i in range(len(pendaftar['pilihan_divisi'])):
            print(f"Divisi {i+1} : {pendaftar['pilihan_divisi'][i]}")
            print(f"Alasan {pendaftar['pilihan_divisi'][i]}: {pendaftar['alasan'][i]}")
        print(f"\nStatus : {pendaftar['status']}")
        print(f"Divisi diterima : {pendaftar['divisi_diterima']}")

        if pendaftar["status"] != "Menunggu Konfirmasi":
            print("\nPendaftar ini sudah dikonfirmasi.")
            enter_kembali()
            continue

        print("\nPendaftar belum dikonfirmasi.")

        lanjut = konfirmasi("Apakah ingin mengonfirmasi pendaftar ini? (ya/tidak): ")

        if not lanjut:
            continue

        divisi_tersedia = []

        for divisi in pendaftar["pilihan_divisi"]:
            if kuota_divisi[divisi] > 0:
                divisi_tersedia.append(divisi)

        if not divisi_tersedia:
            print("\nSemua kuota pilihan divisi sudah habis.")
            enter_kembali()
            continue

        while True:
            divisi_diterima = pilih_divisi("Pilih divisi yang akan diterima:", divisi_tersedia + ["Batalkan memilih"])

            if divisi_diterima == "Batalkan memilih":
                break

            setuju = konfirmasi(f"Terima pendaftar ke divisi {divisi_diterima}? (ya/tidak): ")

            if not setuju:
                continue

            pendaftar["status"] = "Diterima"
            pendaftar["divisi_diterima"] = divisi_diterima

            kuota_divisi[divisi_diterima] -= 1
            simpan_data(data_akun, data_pendaftars_divisi, kuota_divisi)

            print(Fore.GREEN + "\nPendaftar berhasil diterima." + Style.RESET_ALL)
            enter_kembali()
            break

# READ
def lihat_kuota():
    clear()

    print("\n=== SISA KUOTA DIVISI ===")

    tabel = PrettyTable()
    tabel.field_names = ["No", "Divisi", "Sisa Kuota"]

    for i, divisi in enumerate(data_daftar_divisi):
        tabel.add_row([
            i + 1,
            divisi,
            kuota_divisi[divisi]
        ])

    print(tabel)
    enter_kembali()

# UPDATE
def update_divisi():
    while True:
        clear()

        print("\n=== UPDATE DIVISI PENDAFTAR ===")

        daftar_diterima = []

        for i, pendaftar in enumerate(data_pendaftars_divisi):
            if pendaftar["status"] == "Diterima":
                daftar_diterima.append((i, pendaftar))

        if not daftar_diterima:
            print("Belum ada pendaftar yang diterima.")
            enter_kembali()
            return

        tabel = PrettyTable()
        tabel.field_names = ["No", "Nama", "Divisi Saat Ini"]

        for nomor, (index, pendaftar) in enumerate(daftar_diterima):
            tabel.add_row([
                nomor + 1,
                pendaftar["nama"],
                pendaftar["divisi_diterima"]
            ])

        print(tabel)

        while True:

            pilihan = input("\nMasukkan nomor pendaftar atau 'kembali': ").strip()

            if pilihan.lower() == "kembali":
                return

            try:
                nomor = int(pilihan)

                if 1 <= nomor <= len(daftar_diterima):
                    break
                else:
                    print("Nomor pendaftar tidak tersedia.")

            except ValueError:
                print("Input harus berupa angka.")

        index = daftar_diterima[nomor - 1][0]
        pendaftar = data_pendaftars_divisi[index]

        divisi_lama = pendaftar["divisi_diterima"]

        print("\n=== DATA PENDAFTAR ===")
        print(f"Nama : {pendaftar['nama']}")
        print(f"Divisi saat ini : {divisi_lama}")

        print("\nPilihan divisi sebelumnya:")
        for i, divisi in enumerate(pendaftar["pilihan_divisi"]):
            print(f"{i + 1}. {divisi}")

        pilihan_baru = []

        for divisi in data_daftar_divisi:
            if divisi != divisi_lama and kuota_divisi[divisi] > 0:
                pilihan_baru.append(divisi)

        if not pilihan_baru:
            print("\nTidak ada divisi lain yang memiliki kuota.")
            enter_kembali()
            return

        divisi_baru = pilih_divisi("Pilih divisi baru:", pilihan_baru)

        setuju = konfirmasi(f"Pindahkan dari {divisi_lama} ke {divisi_baru}? (ya/tidak): ")

        if setuju:

            kuota_divisi[divisi_lama] += 1
            kuota_divisi[divisi_baru] -= 1

            pendaftar["divisi_diterima"] = divisi_baru
            simpan_data(data_akun, data_pendaftars_divisi, kuota_divisi)

            print(Fore.GREEN + "\nDivisi berhasil diperbarui." + Style.RESET_ALL)

        else:
            print("\nPerubahan dibatalkan.")
            continue

        enter_kembali()


# DELETE
def hapus_pendaftar():
    clear()

    print("\n=== HAPUS DATA PENDAFTAR ===")

    if not data_pendaftars_divisi:
        print("Belum ada data pendaftar.")
        enter_kembali()
        return

    tabel = PrettyTable()
    tabel.field_names = [
        "No",
        "Nama",
        "Status",
        "Divisi Diterima"
    ]

    for i, pendaftar in enumerate(data_pendaftars_divisi):
        tabel.add_row([
            i + 1,
            pendaftar["nama"],
            pendaftar["status"],
            pendaftar["divisi_diterima"]
        ])

    print(tabel)

    while True:

        pilihan = input("\nMasukkan nomor pendaftar atau 'kembali': ").strip()

        if pilihan.lower() == "kembali":
            return

        try:
            nomor = int(pilihan)

            if 1 <= nomor <= len(data_pendaftars_divisi):
                break
            else:
                print("Nomor pendaftar tidak tersedia.")

        except ValueError:
            print("Input harus berupa angka.")

    pendaftar = data_pendaftars_divisi[nomor - 1]

    print("\n=== DATA YANG AKAN DIHAPUS ===")
    print(f"Nama : {pendaftar['nama']}")
    print(f"Status : {pendaftar['status']}")

    setuju = konfirmasi("\nYakin ingin menghapus data ini? (ya/tidak): ")

    if setuju:

        # Kalau sudah diterima,
        # kuota divisinya dikembalikan
        if pendaftar["status"] == "Diterima":
            divisi_lama = pendaftar["divisi_diterima"]
            kuota_divisi[divisi_lama] += 1

        data_pendaftars_divisi.pop(nomor - 1)
        simpan_data(data_akun, data_pendaftars_divisi, kuota_divisi)

        print(Fore.GREEN + "\nData pendaftar berhasil dihapus." + Style.RESET_ALL)

    else:
        print("\nPenghapusan dibatalkan.")

    enter_kembali()


# MENU ADMIN
def menu_admin_login():
    while True:

        pilihan = menu_admin()

        if pilihan == "1":
            lihat_pendaftar()

        elif pilihan == "2":
            lihat_kuota()

        elif pilihan == "3":
            update_divisi()

        elif pilihan == "4":
            hapus_pendaftar()

        elif pilihan == "5":
            from analisis import grafik_minat_divisi
            grafik_minat_divisi()

        elif pilihan == "6":
            print(Fore.MAGENTA + "\nAnda berhasil logout." + Style.RESET_ALL)
            enter_kembali()
            break

        else:
            print("Pilihan tidak valid.")
            enter_kembali()