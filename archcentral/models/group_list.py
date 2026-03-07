from PySide6.QtCore import QAbstractTableModel, Qt

class GroupListModel(QAbstractTableModel):
    def __init__(self, data) -> None:
        super().__init__()
        self._data = data
        self._headers: list[str] = ["Group", "Users"]

    def rowCount(self, parent=None) -> int:
        return len(self._data)

    def columnCount(self, parent=None) -> int:
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers[section]
            else:
                return str(section + 1)
        return None
