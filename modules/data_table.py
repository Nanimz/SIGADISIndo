from PyQt5.QtWidgets import (
    QTableView, QVBoxLayout, QWidget, QHeaderView,
    QSizePolicy, QProxyStyle, QStyle
)
from PyQt5.QtCore import Qt

# Style khusus untuk menghilangkan kotak fokus
class NoFocusRectStyle(QProxyStyle):
    def drawPrimitive(self, element, option, painter, widget=None):
        if element == QStyle.PE_FrameFocusRect:
            return
        super().drawPrimitive(element, option, painter, widget)
_data_table_instance = None

def create_data_table():
    global _data_table_instance

    table_view = QTableView()
    table_view.setStyle(NoFocusRectStyle())

    table_view.setAlternatingRowColors(True)
    table_view.setSelectionBehavior(QTableView.SelectRows)
    table_view.setSelectionMode(QTableView.SingleSelection)
    table_view.horizontalHeader().setStretchLastSection(False)
    table_view.setSortingEnabled(True)
    table_view.verticalHeader().setVisible(False)
    
    table_view.setMinimumHeight(528)
    table_view.setMaximumHeight(528)
    
    table_view.setWordWrap(False)
    table_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
    table_view.setStyleSheet("""
        QTableView {
            background-color: #ffffff;
            alternate-background-color: #f9f9f9;
            gridline-color: #e0e0e0;
            font-size: 13px;
            color: #212121;
            border: none;
        }

        QHeaderView::section {
            background-color: #4CAF50;
            color: white;
            padding: 8px;
            border: none;
            font-size: 14px;
            font-weight: bold;
        }

        QTableView::item {
            padding: 4px;
        }

        QTableView::item:hover {
            background-color: #FFF8DC;
        }

        QTableView::item:selected {
            background-color: #C1A910;
            color: black;
        }

        QTableView::item:focus {
            outline: none;
            border: none;
        }

        QScrollBar:vertical {
            width: 12px;
            background: #f1f1f1;
        }

        QScrollBar::handle:vertical {
            background: #bbb;
            min-height: 20px;
        }

        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            height: 0;
        }

        QScrollBar:horizontal {
            height: 12px;
            background: #f1f1f1;
        }

        QScrollBar::handle:horizontal {
            background: #bbb;
            min-width: 20px;
        }

        QScrollBar::add-line:horizontal,
        QScrollBar::sub-line:horizontal {
            width: 0;
        }
    """)

    container = QWidget()
    layout = QVBoxLayout()
    layout.setContentsMargins(40, 18, 40, 18)
    layout.addWidget(table_view)
    layout.addSpacing(10)
    
    container.setLayout(layout)
    container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    _data_table_instance = table_view
    return container

def get_data_table():
    return _data_table_instance

def set_table_model(model):
    """Set model ke QTableView"""
    if _data_table_instance:
        _data_table_instance.setModel(model)
        resize_columns_smart(_data_table_instance, sample_rows=30)

def resize_columns_smart(table_view, sample_rows=30):
    """Atur lebar kolom berdasarkan header dan sebagian isi baris (sample_rows pertama)"""
    model = table_view.model()
    if not model:
        return

    font_metrics = table_view.fontMetrics()
    for column in range(model.columnCount()):
        header_text = str(model.headerData(column, Qt.Horizontal, Qt.DisplayRole))
        max_width = font_metrics.boundingRect(header_text).width()

        # Cek sample isi
        for row in range(min(sample_rows, model.rowCount())):
            index = model.index(row, column)
            value = str(model.data(index, Qt.DisplayRole))
            max_width = max(max_width, font_metrics.boundingRect(value).width())

        # Padding ekstra
        table_view.setColumnWidth(column, max_width + 40)
