import os
import sys
from PyQt5.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QLineEdit, QPushButton, QLabel, QWidget
)
from PyQt5.QtGui import QFontDatabase, QFont, QIcon
from PyQt5.QtCore import Qt

def resource_path(relative_path):
    """Dapatkan path absolut, baik saat run .py atau .exe"""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

def load_montserrat_font():
    font_path = resource_path(os.path.join("assets", "montserrat", "static", "Montserrat-Medium.ttf"))
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id == -1:
        print("❌ Gagal load font:", font_path)
        return "Arial"
    return QFontDatabase.applicationFontFamilies(font_id)[0]

def create_search_bar(on_search_text_changed=None):
    font_family = load_montserrat_font()
    wrapper_layout = QVBoxLayout()
    wrapper_layout.setContentsMargins(35, 10, 0, 0)
    layout = QHBoxLayout()
    layout.setSpacing(8)

    title_label = QLabel("Cari Data")
    title_label.setFont(QFont(font_family, 12))
    title_label.setFixedWidth(196)
    title_label.setStyleSheet("QLabel { padding-bottom: 2px; }")
    layout.addWidget(title_label, alignment=Qt.AlignVCenter)

    input_container = QWidget()
    input_container.setFixedSize(581, 35)
    input_container.setStyleSheet("background: transparent;")

    search_input = QLineEdit(input_container)
    search_input.setGeometry(0, 0, 581, 35)
    search_input.setStyleSheet(f"""
        QLineEdit {{
            border: 1px solid black;
            border-radius: 10px;
            padding-right: 35px;
            padding-left: 10px;
            font-size: 14px;
            font-family: "{font_family}";
            background-color: white;
        }}
    """)

    if on_search_text_changed:
        search_input.textChanged.connect(on_search_text_changed)

    # Tombol ikon pencarian 
    search_icon_btn = QPushButton(input_container)
    search_icon_btn.setIcon(QIcon(resource_path("icons/search.png")))
    search_icon_btn.setIconSize(search_icon_btn.size())
    search_icon_btn.setGeometry(540, 5, 24, 24)
    search_icon_btn.setStyleSheet("""
        QPushButton {
            border: none;
            background: transparent;
        }
    """)
    search_icon_btn.setCursor(Qt.PointingHandCursor)

    layout.addWidget(input_container, alignment=Qt.AlignLeft)
    wrapper_layout.addLayout(layout)

    container = QWidget()   
    container.setLayout(wrapper_layout)

    return container, search_input
