from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtGui import QColor

# Model for the package search table
class PacmanPackageListTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data
        self._headers = ["Marked for", "Repo", "Package", "Version", "Size", "Install Status"]

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role):
        if role == Qt.CheckStateRole and index.column() == 0:
            return Qt.Checked if self._data[index.row()][0] else Qt.Unchecked

        if role == Qt.DisplayRole and index.column() == 0:
            if self._data[index.row()][5] and self._data[index.row()][0]:
                return "Removal"
            if not self._data[index.row()][5] and self._data[index.row()][0]:
                return "Installation"
            return None

        if role == Qt.BackgroundRole and index.column() == 5:
            return QColor("green") if self._data[index.row()][5] else QColor("red")

        if role == Qt.DisplayRole and index.column() == 5:
            if not self._data[index.row()][5]:
                return "Not Installed"
            if self._data[index.row()][5]:
                return "Installed"
            return None

        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]

        return None

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid():
            return False

        if role == Qt.CheckStateRole and index.column() == 0:
            self._data[index.row()][0] = True if value == Qt.Checked.value else False
            self.dataChanged.emit(index, index, [Qt.CheckStateRole])
            return True

        return False

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        base_flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable

        if index.column() == 0:
            return base_flags | Qt.ItemIsUserCheckable

        return base_flags

    def get_marked_packages(self):
        marked_packages: list[list[bool, bool]] = []
        for row in self._data:
            if row[0]:
                marked_packages.append([row[2], row[5]])
        return marked_packages

    def get_total_size(self):
        return sum([row[3] for row in self._data])

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers[section]
            else:
                return str(section + 1)
        return None
