from external import muat_data


# DATA AKUN AWAL
data_awal_akun = [
    {
        "nama": "ferdika",
        "nim": "039",
        "password": "039",
        "role": "admin"
    },
    {
        "nama": "habibur",
        "nim": "045",
        "password": "045",
        "role": "admin"
    }
]


# DATA PENDAFTAR AWAL
data_awal_pendaftars_divisi = []
# Contoh data dummy pendaftar (sebagai referensi, tidak digunakan oleh program):
# data_akun_pendaftar = [
#     {
#         "nama": "Budi Santoso",
#         "nim": "123456789",
#         "pilihan_divisi": ["ACARA", "HUMAS", "KONSUMSI"],
#         "alasan": [],
#         "status": "Menunggu Konfirmasi",
#         "divisi_diterima": "-",
#         "tanggal": "01-01-2026 10:00"
#     }
# ]


# DAFTAR DIVISI
data_daftar_divisi = (
    "ACARA",
    "HUMAS",
    "KEAMANAN",
    "KESEHATAN",
    "DANUS",
    "KONSUMSI",
    "PDD",
    "PERLENGKAPAN",
    "DEKORASI"
)


# KUOTA AWAL
kuota_awal = {
    "ACARA": 2,
    "HUMAS": 1,
    "KEAMANAN": 1,
    "KESEHATAN": 1,
    "DANUS": 1,
    "KONSUMSI": 1,
    "PDD": 1,
    "PERLENGKAPAN": 1,
    "DEKORASI": 1
}


# MEMUAT DATA DARI JSON
data_tersimpan = muat_data()


if data_tersimpan is None:

    # Jika data.json belum ada,
    # gunakan data awal
    data_akun = data_awal_akun

    data_pendaftars_divisi = data_awal_pendaftars_divisi

    kuota_divisi = kuota_awal


else:

    # Jika data.json sudah ada,
    # gunakan data yang tersimpan
    data_akun = data_tersimpan["data_akun"]

    data_pendaftars_divisi = data_tersimpan["data_pendaftar"]

    kuota_divisi = data_tersimpan["kuota_divisi"]
