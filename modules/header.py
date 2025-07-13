# modules/header.py
import os
import sys
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap, QFont, QFontDatabase
from PyQt5.QtCore import Qt

def resource_path(relative_path):
    """Dapatkan path absolut, baik saat run .py atau .exe"""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

def load_montserrat_font():
    font_path = resource_path(os.path.join("assets", "montserrat", "static", "Montserrat-Bold.ttf"))
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id == -1:
        print(f"❌ Gagal load font: {font_path}")
        return "Arial"
    return QFontDatabase.applicationFontFamilies(font_id)[0]

def create_header(toggle_callback=None):
    header_widget = QWidget()
    header_widget.setFixedHeight(132)
    header_widget.setStyleSheet("background-color: #06923E;")

    layout = QHBoxLayout()
    layout.setContentsMargins(33, 0, 33, 0)
    layout.setSpacing(30)

    # ✅ Logo menu (pakai resource_path)
    logo_label = QLabel()
    pixmap = QPixmap(resource_path("icons/menu.png"))
    if not pixmap.isNull():
        pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap)
    logo_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
    logo_label.setCursor(Qt.PointingHandCursor)

    if toggle_callback:
        def on_click(event):
            toggle_callback()
        logo_label.mousePressEvent = on_click

    # ✅ Font Montserrat dengan fallback
    font_family = load_montserrat_font()
    text_label = QLabel("Aplikasi Manajemen SIGADISIndo")
    text_label.setStyleSheet("color: white; font-size: 50px; font-weight: bold;")
    text_label.setFont(QFont(font_family, 20, QFont.Bold))
    text_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

    layout.addWidget(logo_label)
    layout.addWidget(text_label)
    layout.addStretch(1)

    header_widget.setLayout(layout)
    return header_widget
