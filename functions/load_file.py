from PyQt5.QtWidgets import QFileDialog

def load_file_dialog(parent=None):
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly
    file_path, _ = QFileDialog.getOpenFileName(
        parent,
        "Pilih File",
        "",
        "All Files (*);Excel Files (*.xlsx *.xls);;CSV Files (*.csv);",
        options=options
    )
    return file_path
