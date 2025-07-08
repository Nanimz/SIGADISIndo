import os
import sys
from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame, QWidget,
    QDialog, QCheckBox, QScrollArea, QDialogButtonBox
)
from PyQt5.QtGui import QPixmap, QFont, QIcon, QFontDatabase
from PyQt5.QtCore import Qt, QSize
from modules.data_table import get_data_table
from functions.display_table import get_loaded_data

# ✅ Tambahan: import dialog tutorial
from modules.tutorial_dialog import show_tutorial_dialog
from modules.deskripsi_dialog import show_deskripsi_dialog


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

def show_columns_dialog():
    table = get_data_table()
    if not table or not table.model():
        return

    model = table.model()
    column_count = model.columnCount()
    column_names = [model.headerData(i, Qt.Horizontal) for i in range(column_count)]

    dialog = QDialog()
    dialog.setWindowTitle("Pilih Kolom yang Ditampilkan")
    layout = QVBoxLayout(dialog)

    checkbox_container = QWidget()
    checkbox_layout = QVBoxLayout(checkbox_container)
    checkboxes = []

    for i, name in enumerate(column_names):
        cb = QCheckBox(str(name))
        cb.setChecked(not table.isColumnHidden(i))
        checkboxes.append((i, cb))
        checkbox_layout.addWidget(cb)

    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setWidget(checkbox_container)
    layout.addWidget(scroll)

    bulk_buttons_layout = QHBoxLayout()
    btn_check_all = QPushButton("Checklist Semua")
    btn_uncheck_all = QPushButton("Uncheck Semua")
    btn_check_all.clicked.connect(lambda: [cb.setChecked(True) for _, cb in checkboxes])
    btn_uncheck_all.clicked.connect(lambda: [cb.setChecked(False) for _, cb in checkboxes])
    bulk_buttons_layout.addWidget(btn_check_all)
    bulk_buttons_layout.addWidget(btn_uncheck_all)
    layout.addLayout(bulk_buttons_layout)

    button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    layout.addWidget(button_box)

    def apply_changes():
        for col_index, checkbox in checkboxes:
            table.setColumnHidden(col_index, not checkbox.isChecked())
        dialog.accept()

    button_box.accepted.connect(apply_changes)
    button_box.rejected.connect(dialog.reject)

    dialog.setMinimumSize(320, 450)
    dialog.exec_()


def create_sidebar(on_load_callback=None, filter_widget=None, on_reset_callback=None):
    font_family = load_montserrat_font()
    sidebar = QVBoxLayout()
    sidebar.setContentsMargins(0, 10, 0, 10)
    sidebar.setSpacing(10)
    sidebar.setAlignment(Qt.AlignTop)

    header_container = QWidget()
    header_container.setFixedHeight(112)
    header_layout = QHBoxLayout()
    header_layout.setSpacing(10)
    header_layout.setContentsMargins(20, 0, 0, 0)

    logo_label = QLabel()
    pixmap = QPixmap(resource_path("icons/logo-kemenag.png")).scaled(90, 81, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
    logo_label.setPixmap(pixmap)
    logo_label.setAlignment(Qt.AlignVCenter)

    text_label = QLabel("Kementerian<br>Agama <b style='color:#C1A910;'>Kota</b><br><b style='color:#C1A910;'>Malang</b>")
    text_label.setFont(QFont(font_family, 16, QFont.Bold))
    text_label.setStyleSheet("color: white;")
    text_label.setTextFormat(Qt.RichText)
    text_label.setWordWrap(True)
    text_label.setAlignment(Qt.AlignVCenter)

    header_layout.addWidget(logo_label)
    header_layout.addWidget(text_label)
    header_layout.addStretch(1)
    header_container.setLayout(header_layout)
    sidebar.addWidget(header_container)

    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setStyleSheet("background-color: gray; margin-bottom: 2px")
    sidebar.addWidget(line)

    button_widgets = []
    buttons_top = [
        ("Load File", "icons/load-file.png"),
        ("Refresh", "icons/refresh.png"),
        ("Show Columns", "icons/show-columns.png"),
        ("Save to Excel", "icons/save-to-excel.png"),
    ]

    def create_button(name, icon_path):
        btn = QPushButton(f"   {name}")
        btn.setObjectName(name)
        if icon_path:
            icon_full_path = resource_path(icon_path)
            icon_pix = QPixmap(icon_full_path).scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            btn.setIcon(QIcon(icon_pix))
            btn.setIconSize(QSize(50, 50))
        btn.setStyleSheet("""
            QPushButton {
                background: none;
                color: white;
                text-align: left;
                padding-left: 20px;
                padding-top: 8px;
                padding-bottom: 8px;
                border: none;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #C1A910;
            }
        """)
        btn.setFont(QFont(font_family, 12, QFont.Bold))
        button_widgets.append(btn)
        return btn


    for name, icon in buttons_top:
        btn = create_button(name, icon)
        if name == "Load File" and on_load_callback:
            btn.clicked.connect(on_load_callback)
        elif name == "Refresh" and on_reset_callback:
            btn.clicked.connect(on_reset_callback)
        elif name == "Show Columns":
            btn.clicked.connect(show_columns_dialog)
        elif name == "Save to Excel":
            from functions.export_excel import export_current_table_to_excel
            btn.clicked.connect(export_current_table_to_excel)
        sidebar.addWidget(btn)

    sidebar.addStretch(1)

    buttons_bottom = [
        ("Tutorial", "icons/tutorial.png"),
        ("Deskripsi", "icons/deskripsi.png"),
    ]
    for name, icon in buttons_bottom:
        btn = create_button(name, icon)

        # ✅ Tambahkan aksi jika tombol tutorial ditekan
        if name == "Tutorial":
            btn.clicked.connect(show_tutorial_dialog)
        elif name == "Deskripsi":
            btn.clicked.connect(show_deskripsi_dialog)

        sidebar.addWidget(btn)

    frame = QFrame()
    default_width = 320
    mini_width = logo_label.pixmap().width() + 40

    frame.setFixedWidth(default_width)
    frame.setStyleSheet("background-color: #212121; color: white;")
    frame.setLayout(sidebar)

    def toggle_sidebar(mini: bool):
        if mini:
            frame.setFixedWidth(mini_width)
            for btn in button_widgets:
                btn.setText("")
                btn.setStyleSheet("""
                    QPushButton {
                        background: none;
                        color: white;
                        text-align: center;
                        padding: 8px 0;
                        border: none;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #C1A910;
                    }
                """)
            text_label.setVisible(False)
        else:
            frame.setFixedWidth(default_width)
            for btn in button_widgets:
                btn.setText(f"   {btn.objectName()}")
                btn.setStyleSheet("""
                    QPushButton {
                        background: none;
                        color: white;
                        text-align: left;
                        padding-left: 20px;
                        padding-top: 8px;
                        padding-bottom: 8px;
                        border: none;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #C1A910;
                    }
                """)
            text_label.setVisible(True)

    return frame, toggle_sidebar
