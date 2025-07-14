from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant

class PandasTableModel(QAbstractTableModel):
    def __init__(self, dataframe, parent=None):
        super().__init__(parent)
        self._dataframe = dataframe

    def rowCount(self, parent=None):
        return self._dataframe.shape[0]

    def columnCount(self, parent=None):
        return self._dataframe.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return QVariant()

        if role == Qt.DisplayRole:
            value = self._dataframe.iloc[index.row(), index.column()]
            return str(value)

        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

        return QVariant()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()

        if orientation == Qt.Horizontal:
            return str(self._dataframe.columns[section]).upper()
        else:
            return str(section + 1)

    def set_dataframe(self, dataframe):
        self.beginResetModel()
        self._dataframe = dataframe
        self.endResetModel()
