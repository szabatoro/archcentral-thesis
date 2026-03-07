from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtGui import QColor
from archcentral.helpers.unitconverter import unit_converter
from archcentral.helpers.custom_classes import PacmanPkgInfo

# Model for the package search table
class PacmanPackageListTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data
        self._headers = ["Marked for", "Repo", "Package", "Version", "Installed Size", "Install Status"]

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role):
        pkg: PacmanPkgInfo = self._data[index.row()]

        if role == Qt.CheckStateRole and index.column() == 0:
            return Qt.Checked if pkg.marked else Qt.Unchecked

        if role == Qt.DisplayRole and index.column() == 0:
            if pkg.installed and pkg.marked:
                return "Removal"
            if not pkg.installed and pkg.marked:
                return "Installation"
            return None

        if role == Qt.DisplayRole and index.column() == 4:
            value, unit = unit_converter(pkg.isize)
            return f"{value:.2f} {unit}"

        if role == Qt.BackgroundRole and index.column() == 5:
            return QColor("darkgreen") if pkg.installed else QColor("darkred")

        if role == Qt.DisplayRole and index.column() == 5:
            if not pkg.installed:
                return "Not Installed"
            if pkg.installed:
                return "Installed"
            return None

        if role == Qt.DisplayRole:
            mapping = {
                1: pkg.repo,
                2: pkg.name,
                3: pkg.version,
            }
            return mapping.get(index.column())

        return None

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid():
            return False

        pkg: PacmanPkgInfo = self._data[index.row()]

        if role == Qt.CheckStateRole and index.column() == 0:
            pkg.marked = True if value == Qt.Checked.value else False
            self.dataChanged.emit(index, index, [Qt.CheckStateRole])
            return True

        return False

    def refresh(self, new_data):
            self.beginResetModel()
            self._data = new_data
            self.endResetModel()

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        base_flags = Qt.ItemIsEnabled | Qt.ItemIsSelectable

        if index.column() == 0:
            return base_flags | Qt.ItemIsUserCheckable

        return base_flags

    def get_marked_packages(self):
        marked_packages: list[list[str, bool]] = []
        for pkg in self._data:
            if pkg.marked:
                marked_packages.append([pkg.name, pkg.installed])
        return marked_packages

    def get_package(self, index) -> PacmanPkgInfo:
        """Returns the PacmanPkgInfo object found in the specified row."""
        return self._data[index.row()]

    def get_total_size(self):
        return sum([pkg.size for pkg in self._data])

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers[section]
            else:
                return str(section + 1)
        return None
