import os
import sys
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QLabel, QWidget, QSizePolicy, QPushButton
from PyQt5.QtGui import QFont, QFontDatabase, QPixmap, QIcon
from PyQt5.QtCore import Qt, pyqtSignal

def load_montserrat_font():
    font_path = resource_path(os.path.join("assets", "montserrat", "static", "Montserrat-Bold.ttf"))
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id == -1:
        print("❌ Gagal load font:", font_path)
        return "Arial"
    return QFontDatabase.applicationFontFamilies(font_id)[0]

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

class ResultBoxWidget(QWidget):
    resume_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.font_family = load_montserrat_font()
        self.box_labels = {}
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
            box_container.setFixedHeight(92)
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
        vertical_layout.addWidget(self.create_footer_boxes())

        self.setLayout(vertical_layout)

    def update_counts(self, df):
        if df is None or df.empty:
            for key in self.box_labels:
                self.box_labels[key].setText("0")
            return

        df.columns = df.columns.str.lower()

        if "status pegawai" in df.columns:
            status_series = df["status pegawai"].dropna().str.lower().str.strip()
            self.box_labels["Jumlah PNS"].setText(str((status_series == "pns").sum()))
            self.box_labels["Jumlah NON PNS"].setText(str((status_series == "non pns").sum()))
            self.box_labels["Jumlah PPPK"].setText(str((status_series == "pppk").sum()))
        else:
            for key in ["Jumlah PNS", "Jumlah NON PNS", "Jumlah PPPK"]:
                self.box_labels[key].setText("0")

        if "nama sekolah" in df.columns:
            unique_school_count = df["nama sekolah"].dropna().str.lower().str.strip().nunique()
            self.box_labels["Jumlah Sekolah"].setText(str(unique_school_count))
        else:
            self.box_labels["Jumlah Sekolah"].setText("0")

    def create_footer_boxes(self):
        layout = QHBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(6, 0, 0, 0)

        school_widget = QWidget()
        school_widget.setStyleSheet("""
            background-color: #d4edda;
            border-radius: 8px;
        """)
        school_widget.setFixedHeight(50)
        school_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        school_layout = QVBoxLayout()
        school_layout.setContentsMargins(10, 8, 10, 8)
        school_layout.setSpacing(0)
        school_layout.setAlignment(Qt.AlignCenter)

        content_widget = QWidget()
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(8)
        content_layout.setAlignment(Qt.AlignCenter)

        logo_label = QLabel()
        logo_path = resource_path("icons/school.png")
        logo_pixmap = QPixmap(logo_path).scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignVCenter)

        label_text = QLabel("Jumlah Sekolah:")
        label_text.setFont(QFont(self.font_family, 10, QFont.Bold))
        label_text.setAlignment(Qt.AlignVCenter)

        jumlah_label = QLabel("0")
        jumlah_label.setFont(QFont(self.font_family, 12, QFont.Bold))
        jumlah_label.setAlignment(Qt.AlignVCenter)
        jumlah_label.setStyleSheet("color: #EE6820;")
        self.box_labels["Jumlah Sekolah"] = jumlah_label

        content_layout.addWidget(logo_label)
        content_layout.addWidget(label_text)
        content_layout.addWidget(jumlah_label)

        content_widget.setLayout(content_layout)
        school_layout.addWidget(content_widget)
        school_widget.setLayout(school_layout)

        resume_button = QPushButton()
        resume_button.setText(" Resume")
        resume_button.setIcon(QIcon(resource_path("icons/resume.png")))
        resume_button.setFont(QFont(self.font_family, 10, QFont.Bold))
        resume_button.setCursor(Qt.PointingHandCursor)
        resume_button.setStyleSheet("""
            QPushButton {
                background-color: #cce5ff;
                color: #004085;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #b8daff;
            }
        """)
        resume_button.setFixedHeight(50)
        resume_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        resume_button.clicked.connect(self.resume_clicked.emit)

        layout.addWidget(school_widget)
        layout.addWidget(resume_button)

        container = QWidget()
        container.setLayout(layout)
        return container
