from PySide6.QtCore import QAbstractTableModel, Qt
from archcentral.helpers.unitconverter import unit_converter

# Model for the update table
class PacmanUpdateTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data
        self._headers = ["Package", "Installed Version", "New Version", "Update Size"]

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        update = self._data[index.row()]

        if role == Qt.DisplayRole and index.column() == 3:
            value, unit = unit_converter(update[3])
            return f"{value:.2f} {unit}"

        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        return None

    def refresh(self, new_data):
            self.beginResetModel()
            self._data = new_data
            self.endResetModel()

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
