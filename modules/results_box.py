import os
import sys
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QWidget, QSizePolicy
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt

def load_montserrat_font():
    font_path = resource_path(os.path.join("assets", "montserrat", "static", "Montserrat-Bold.ttf"))
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id == -1:
        print("❌ Gagal load font:", font_path)
        return "Arial"
    return QFontDatabase.applicationFontFamilies(font_id)[0]

def resource_path(relative_path):
    """Dapatkan path absolut, baik saat run .py atau .exe"""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

class ResultBoxWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.font_family = load_montserrat_font()
        self.box_labels = {}  # Untuk menyimpan referensi label nilai
        self.init_ui()

    def init_ui(self):
        title_label = QLabel("Informasi Hasil")
        title_label.setFont(QFont(self.font_family, 12, QFont.Bold))
        title_label.setAlignment(Qt.AlignLeft)
        title_label.setStyleSheet("color: black; padding-bottom: 8px;")

        box_layout = QHBoxLayout()
        box_layout.setSpacing(16)
        box_layout.setContentsMargins(6, 0, 0, 0)

        for label in ["Jumlah PNS", "Jumlah NON PNS", "Jumlah PPPK"]:
            box_container = QWidget()
            box_container.setStyleSheet("""
                background-color: #d4edda;
                border-radius: 8px;
                padding: 0px;
            """)
            box_container.setFixedHeight(110)
            box_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

            inner_layout = QVBoxLayout()
            inner_layout.setContentsMargins(10, 8, 10, 8)
            inner_layout.setSpacing(5)

            title = QLabel(label)
            title.setFont(QFont(self.font_family, 10, QFont.Bold))
            title.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

            value = QLabel("0")
            value.setFont(QFont(self.font_family, 12, QFont.Bold))
            value.setAlignment(Qt.AlignCenter)
            value.setStyleSheet("color: #EE6820;")

            # Simpan referensinya
            self.box_labels[label] = value

            inner_layout.addWidget(title)
            inner_layout.addStretch(1)
            inner_layout.addWidget(value)
            inner_layout.addStretch(1)

            box_container.setLayout(inner_layout)
            box_layout.addWidget(box_container)

        vertical_layout = QVBoxLayout()
        vertical_layout.setSpacing(5)
        vertical_layout.setContentsMargins(100, 20, 20, 0)
        vertical_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        vertical_layout.addWidget(title_label)

        box_wrapper = QWidget()
        box_wrapper.setLayout(box_layout)
        vertical_layout.addWidget(box_wrapper)

        self.setLayout(vertical_layout)

    def update_counts(self, df):
        """Update jumlah berdasarkan DataFrame hasil filter"""
        if df is None or df.empty:
            for key in self.box_labels:
                self.box_labels[key].setText("0")
            return

        if "STATUS PEGAWAI" in df.columns:
            self.box_labels["Jumlah PNS"].setText(str((df["STATUS PEGAWAI"] == "PNS").sum()))
            self.box_labels["Jumlah NON PNS"].setText(str((df["STATUS PEGAWAI"] == "NON PNS").sum()))
            self.box_labels["Jumlah PPPK"].setText(str((df["STATUS PEGAWAI"] == "PPPK").sum()))
        else:
            # Jika kolom tidak tersedia, tampilkan 0 semua
            for key in self.box_labels:
                self.box_labels[key].setText("0")

