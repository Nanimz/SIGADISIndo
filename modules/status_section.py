import os
import sys
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QSizePolicy
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt


def resource_path(relative_path):
    """Mengembalikan path absolut, baik saat run .py atau .exe"""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)


def load_montserrat_font():
    font_path = resource_path(os.path.join("assets", "montserrat", "static", "Montserrat-Bold.ttf"))
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id == -1:
        print("[⚠️] Font Montserrat gagal dimuat. Menggunakan Arial.")
        return "Arial"
    families = QFontDatabase.applicationFontFamilies(font_id)
    if not families:
        return "Arial"
    return families[0]


class StatusSection(QWidget):
    def __init__(self):
        super().__init__()

        # Gunakan font Montserrat jika tersedia
        self.font_family = load_montserrat_font()

        self.setStyleSheet("""
            background-color: #f9f9f9;
            padding: 4px 5px;
        """)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(39, 0, 39, 20)
        self.layout.setSpacing(10)

        self.total_label = QLabel("Total Baris: 0")
        self.total_label.setFont(QFont(self.font_family, 11))
        self.total_label.setStyleSheet("""
            background-color: #d4edda;
            font-weight: bold;
            font-size: 13px;
            color: #212121;
            padding: 6px 12px;
            border-radius: 6px;
        """)

        self.selected_label = QLabel("")
        self.selected_label.setFont(QFont(self.font_family, 11))
        self.selected_label.setStyleSheet("""
            background-color: #d4edda;
            font-weight: bold;
            font-size: 13px;
            color: #EE6820;
            padding: 6px 12px;
            border-radius: 6px;
        """)
        self.selected_label.setVisible(False)

        self.layout.addWidget(self.total_label)
        self.layout.addWidget(self.selected_label)
        self.layout.addStretch()

        self.setLayout(self.layout)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

    def update_total(self, count):
        self.total_label.setText(f"Total Baris: {count}")

    def update_selected_row(self, index=None):
        if index is None:
            self.selected_label.setVisible(False)
        else:
            self.selected_label.setText(f"Baris Terpilih: {index + 1}")
            self.selected_label.setVisible(True)
