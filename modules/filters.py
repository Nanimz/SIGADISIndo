import os
import sys
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QGridLayout, QVBoxLayout
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt, pyqtSignal

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

def load_montserrat_font():
    font_path = resource_path("assets/montserrat/static/Montserrat-Medium.ttf")
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id == -1:
        print("[⚠️] Font Montserrat gagal dimuat. Menggunakan Arial.")
        return "Arial"
    families = QFontDatabase.applicationFontFamilies(font_id)
    return families[0] if families else "Arial"

class FilterWidget(QWidget):
    filter_changed = pyqtSignal(dict)

    def __init__(self, available_filters=None):
        super().__init__()
        self.available_filters = available_filters or {}
        self.filter_combos = {}
        self.init_ui()

    def init_ui(self):
        font_family = load_montserrat_font()
        self.setMaximumWidth(700)
        self.setStyleSheet("background-color: white;")
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(20, 20, 0, 0)
        outer_layout.setSpacing(10)

        title_label = QLabel("Filter")
        title_label.setFont(QFont(font_family, 12, QFont.Bold))
        outer_layout.addWidget(title_label)

        grid = QGridLayout()
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(10)

        filter_data = [
            ("Jenjang Sekolah", ["Semua", "SD", "SMP", "SMA", "SMK"]),
            ("Status Pegawai", ["Semua", "PNS", "NON PNS", "PPPK"]),
            ("Jenis Kelamin", ["Semua", "L", "P"]),
            ("Sertifikasi", ["Semua", "Sudah", "Belum"]),
            ("Inpassing", ["Semua", "Sudah", "Belum"]),
            ("Pensiun", ["Semua", "Sudah", "Belum"]),
        ]

        count = 0
        for label_text, options in filter_data:
            if self.available_filters and label_text not in self.available_filters:
                continue

            label = QLabel(label_text)
            label.setFont(QFont(font_family, 11))

            combo = QComboBox()
            combo.addItems(options)
            combo.setStyleSheet("""
                QComboBox {
                    background-color: #C1A910;
                    color: black;
                    font-weight: bold;
                    padding: 5px;
                }
                QComboBox:focus {
                    border: none;
                    outline: none;
                }
                QComboBox QAbstractItemView:focus {
                    background: transparent;
                    outline: none;
                }
            """)
            combo.setMinimumWidth(100)

            self.filter_combos[label_text] = combo
            combo.currentTextChanged.connect(self.on_filter_changed)

            row = count % 3
            col = (count // 3) * 2
            grid.addWidget(label, row, col)
            grid.addWidget(combo, row, col + 1)
            count += 1

        outer_layout.addLayout(grid)

    def on_filter_changed(self):
        filters = {}
        for label, combo in self.filter_combos.items():
            value = combo.currentText()
            if value != "Semua":
                filters[label] = value
        self.filter_changed.emit(filters)

    def get_current_filters(self):
        filters = {}
        for label, combo in self.filter_combos.items():
            value = combo.currentText()
            if value != "Semua":
                filters[label] = value
        return filters

    def reset_filters(self):
        for combo in self.filter_combos.values():
            combo.setCurrentIndex(0)

def create_filter_section(available_filters=None):
    return FilterWidget(available_filters=available_filters)
