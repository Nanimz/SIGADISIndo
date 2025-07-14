from PyQt5.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QScrollArea, QWidget, QDialogButtonBox
)
from PyQt5.QtCore import Qt

def show_tutorial_dialog():
    dialog = QDialog()
    dialog.setWindowTitle("📖 Panduan Penggunaan Aplikasi")
    dialog.setMinimumSize(650, 500)

    layout = QVBoxLayout(dialog)

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)

    content_widget = QWidget()
    content_layout = QVBoxLayout(content_widget)

    tutorial_text = """
    <h2 style='color:#2c3e50;'>📘 Cara Menggunakan Aplikasi</h2>
    <p style='font-size:12pt;'>Berikut adalah langkah-langkah menggunakan fitur-fitur utama:</p>

    <ul style='font-size:11pt;'>
        <li><b>📂 Muat Data:</b><br>
            Klik tombol <b>'Load File'</b> lalu pilih file Excel yang ingin dimuat ke aplikasi.
        </li><br>
        <li><b>🔍 Cari Data:</b><br>
            Ketik kata kunci pada kolom pencarian. Data yang sesuai akan muncul secara otomatis.
        </li><br>
        <li><b>🎯 Terapkan Filter:</b><br>
            Pilih opsi pada dropdown filter, lalu klik <b>'Filter'</b> untuk menyaring data sesuai kriteria.
        </li><br>
        <li><b>🔄 Refresh Data:</b><br>
            Klik <b>'Refresh'</b> untuk membersihkan filter & pencarian dan menampilkan ulang seluruh data.
        </li><br>
        <li><b>🧩 Tampilkan/Sembunyikan Kolom:</b><br>
            Klik <b>'Show Columns'</b> lalu pilih kolom mana yang ingin ditampilkan atau disembunyikan.
        </li><br>
        <li><b>💾 Simpan Data:</b><br>
            Klik <b>'Save to Excel'</b> untuk menyimpan data tabel yang tampil ke dalam file Excel.
        </li>
    </ul>
    """

    tutorial_label = QLabel()
    tutorial_label.setTextFormat(Qt.RichText)
    tutorial_label.setText(tutorial_text)
    tutorial_label.setWordWrap(True)
    tutorial_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
    tutorial_label.setStyleSheet("""
        QLabel {
            font-family: 'Segoe UI';
            font-size: 11pt;
            color: #2d3436;
        }
    """)

    content_layout.addWidget(tutorial_label)
    scroll_area.setWidget(content_widget)
    layout.addWidget(scroll_area)

    button_box = QDialogButtonBox(QDialogButtonBox.Close)
    button_box.rejected.connect(dialog.reject)
    layout.addWidget(button_box)

    dialog.exec_()
