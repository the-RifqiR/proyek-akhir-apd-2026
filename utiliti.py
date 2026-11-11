import os
from prettytable import PrettyTable
from colorama import Fore, Style
import inquirer

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def enter_kembali():
    input(Fore.GREEN + "\nTekan ENTER untuk kembali..." + Style.RESET_ALL)

def enter_ulang():
    input(Fore.GREEN + "\nTekan ENTER untuk mencoba ulang..." + Style.RESET_ALL)

def pilih_divisi(pesan, daftar_pilihan):
    pertanyaan = [
        inquirer.List(
            "divisi",
            message=pesan,
            choices=daftar_pilihan
        )
    ]

    jawaban = inquirer.prompt(pertanyaan)

    return jawaban["divisi"]

def konfirmasi(pesan):
    while True:
        jawaban = input(pesan).strip().lower()

        if jawaban == "ya":
            return True
        elif jawaban == "tidak":
            return False
        else:
            print("Input tidak valid. Masukkan 'ya' atau 'tidak'.")