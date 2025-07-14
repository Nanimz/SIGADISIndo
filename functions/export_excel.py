import pandas as pd
from PyQt5.QtWidgets import QFileDialog
from modules.data_table import get_data_table

def export_current_table_to_excel():
    table = get_data_table()
    if table is None or table.model() is None:
        return False, "❌ Tidak ada data untuk disimpan."

    model = table.model()

    # Ambil hanya kolom yang terlihat
    visible_columns = [
        i for i in range(model.columnCount())
        if not table.isColumnHidden(i)
    ]

    if not visible_columns:
        return False, "❌ Tidak ada kolom yang ditampilkan untuk disimpan."

    headers = [model.headerData(i, table.horizontalHeader().orientation()) for i in visible_columns]

    data = []
    for row in range(model.rowCount()):
        row_data = []
        for col in visible_columns:
            index = model.index(row, col)
            row_data.append(model.data(index))
        data.append(row_data)

    df = pd.DataFrame(data, columns=headers)

    # Dialog untuk menyimpan file
    path, _ = QFileDialog.getSaveFileName(
        None, "Simpan File Excel", "", "Excel Files (*.xlsx)"
    )
    if path:
        if not path.endswith(".xlsx"):
            path += ".xlsx"
        try:
            df.to_excel(path, index=False)
            return True, f"✅ Data berhasil disimpan:\n{path}"
        except Exception as e:
            return False, f"❌ Gagal menyimpan data:\n{str(e)}"

    return False, "❌ Operasi dibatalkan."
