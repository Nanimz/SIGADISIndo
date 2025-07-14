![App Logo](icons/splash.png)

## SIGADISIndo

**SISTEM INFORMASI GURU AGAMA ISLAM INDONESIA**  
Aplikasi desktop untuk manajemen data guru Pendidikan Agama Islam (PAI) di Indonesia.

## 📝 Deskripsi

SIGADISIndo adalah sistem informasi yang dikembangkan untuk membantu dalam mengelola data guru PAI, termasuk fitur pencarian, filter, dan ekspor data. Aplikasi ini dibangun dengan Python dan PyQt5, serta memiliki antarmuka pengguna yang intuitif untuk memudahkan pengguna non-teknis.

## 🛠️ Teknologi yang Dibutuhkan

- Python 3.10
- PyQT5
- Qt Designer (Sebagai Desain UI)
- Pandas
- Openpyxl

## 🚀 Cara Menjalankan

1. Clone Repository

   ```bash
   git clone https://github.com/Nanimz/SIGADISIndo.git
   ```

2. Install Dependensi

   ```bash
   pip install PyQt5 pandas openpyxl python-docx
   ```

3. Jalankan Aplikasi
   ```bash
   python ./main.py
   ```

## ✨ Fitur Utama

- Manajemen data guru PAI
- Antarmuka pengguna berbasis PyQt5
- Fitur pencarian dan filter data
- Ekspor data ke Word atau Excel
- Struktur modular memudahkan pengembangan dan pemeliharaan

## 📷 Tampilan Aplikasi

![Tampilan Aplikasi](icons/TAMPILAN.png)

## 📌 Catatan Tambahan

- Proyek ini dibuat sebagai bagian dari kegiatan magang di Kantor Kementerian Agama Kota Malang, dengan tujuan membantu digitalisasi dan pengelolaan data guru Pendidikan Agama Islam (PAI).
- Folder `venv/` tidak termasuk dalam versi Git dan apabila ingin membuat virtual enviroment maka sebaiknya dibuat ulang secara lokal dan mulai menginstall semua dependensi yang diperlukan di dalamnya.
- File antarmuka pengguna dibuat dengan Qt Designer dan dapat diedit ulang melalui file .ui yang terdapat di folder UI/.
