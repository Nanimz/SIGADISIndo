import os
import sys
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QPixmap, QFontDatabase, QFont
from PyQt5.QtCore import Qt

def resource_path(relative_path):
    """Mengembalikan path absolut, baik saat run .py atau .exe"""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

class FooterCredit(QWidget):
    def __init__(self):
        super().__init__()

        font_family = self.load_montserrat_font()

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 39, 5)
        layout.setSpacing(2)
        layout.setAlignment(Qt.AlignRight | Qt.AlignBottom)

        # Path ikon menggunakan resource_path
        icon_path = resource_path("icons/copyright.png")
        icon_pixmap = QPixmap(icon_path)

        icon_label = QLabel()
        if not icon_pixmap.isNull():
            icon_label.setPixmap(icon_pixmap.scaled(16, 16, Qt.KeepAspectRatio, Qt.SmoothTransformation))

        text_label = QLabel("PKL-UINMA 2025 GPAIDA")
        text_label.setFont(QFont(font_family, 10))
        text_label.setStyleSheet("color: #212121; padding-left: 2px;")

        layout.addWidget(icon_label)
        layout.addWidget(text_label)

        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

    @staticmethod
    def load_montserrat_font():
        font_path = resource_path("assets/montserrat/static/Montserrat-Bold.ttf")
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id == -1:
            print("[⚠️] Font Montserrat gagal dimuat. Menggunakan Arial.")
            return "Arial"
        families = QFontDatabase.applicationFontFamilies(font_id)
        return families[0] if families else "Arial"
