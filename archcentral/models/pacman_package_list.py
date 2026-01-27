from PySide6.QtCore import QAbstractTableModel, Qt

# Model for the package search table
class PacmanPackageListTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data
        self._headers = ["Status", "Repo", "Package", "Version", "Size"]

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        return None

    def get_packagenames(self):
        return [row[0] for row in self._data]

    def get_total_size(self):
        return sum([row[3] for row in self._data])

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers[section]
            else:
                return str(section + 1)
        return None
