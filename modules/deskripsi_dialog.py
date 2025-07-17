from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QScrollArea, QWidget, QDialogButtonBox
from PyQt5.QtCore import Qt

def show_deskripsi_dialog():
    dialog = QDialog()
    dialog.setWindowTitle("📘 Panduan Aplikasi Manajemen SIGADISIndo")
    dialog.setMinimumSize(700, 550)

    layout = QVBoxLayout(dialog)

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)

    content_widget = QWidget()
    content_layout = QVBoxLayout(content_widget)

    panduan_teks = """
    <h2 style='color:#2c3e50;'>Selamat Datang di <span style='color:#1abc9c;'>Aplikasi Manajemen SIGADISIndo</span>!</h2>
    <p style='font-size:12pt;'>
    Aplikasi ini dirancang untuk memudahkan pengelolaan data pegawai melalui berbagai fitur canggih dan ramah pengguna.
    </p>

    <h3 style='color:#2980b9;'>🔧 Fitur Utama:</h3>
    <ul style='font-size:11pt;'>
        <li><b>Pembacaan Data dari Excel:</b><br>
            Memuat data dari file Excel (.xlsx) secara instan.
        </li><br>
        <li><b>Penampilan Data:</b><br>
            Menampilkan data dalam bentuk tabel interaktif dengan kolom yang bisa disesuaikan.<br>
            Menyediakan filter berdasarkan <i>jenjang sekolah, sertifikasi, status pegawai, inpassing, jenis kelamin</i>, dan <i>status pensiun</i>.
        </li><br>
        <li><b>Pencarian Data:</b><br>
            Menyediakan pencarian kata kunci dengan <i>highlight</i> hasil pencocokan otomatis.
        </li><br>
        <li><b>Penyaringan Kolom:</b><br>
            Pengguna bebas memilih kolom mana yang ingin ditampilkan atau disembunyikan.
        </li><br>
        <li><b>Ekspor Data:</b><br>
            Ekspor tampilan tabel ke file Excel dengan satu klik.
        </li>
    </ul>

    <h3 style='color:#27ae60;'>👨‍💻 Pengembang dan Kontak:</h3>
    <p style='font-size:11pt;'>
    Aplikasi ini dikembangkan oleh <b>Tim PKL UIN Malang</b>:<br>
    - Moch. Minanur Rahman<br>
    - Muhamad Radiyudin<br>
    <i>Periode PKL: 01 Juli – 31 Juli 2025</i><br><br>

    Untuk pertanyaan atau informasi lebih lanjut:<br>
    📞 0821-4673-6240 / 0877-4104-0885
    </p>
    """

    label = QLabel()
    label.setText(panduan_teks)
    label.setAlignment(Qt.AlignTop)
    label.setTextInteractionFlags(Qt.TextSelectableByMouse)
    label.setWordWrap(True)
    label.setStyleSheet("""
        QLabel {
            font-family: 'Segoe UI';
            font-size: 11pt;
            color: #2d3436;
        }
    """)

    content_layout.addWidget(label)
    scroll_area.setWidget(content_widget)
    layout.addWidget(scroll_area)

    button_box = QDialogButtonBox(QDialogButtonBox.Close)
    button_box.rejected.connect(dialog.reject)
    layout.addWidget(button_box)

    dialog.exec_()
