from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtGui import QColor
from archcentral.helpers.custom_classes import GroupMemberUser

class GroupManageUsersListTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data
        self._headers = ["Marked for", "User", "Member status"]

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role):
        user: GroupMemberUser = self._data[index.row()]

        if role == Qt.CheckStateRole and index.column() == 0:
            return Qt.Checked if user.marked else Qt.Unchecked

        if role == Qt.DisplayRole and index.column() == 0:
            if user.is_member and user.marked:
                return "Remove"
            if not user.is_member and user.marked:
                return "Add"
            return None

        if role == Qt.BackgroundRole and index.column() == 2:
            return QColor("darkgreen") if user.is_member else QColor("darkred")

        if role == Qt.DisplayRole and index.column() == 2:
            if not user.is_member:
                return "Is not a member"
            if user.is_member:
                return "Is a member"
            return None

        if role == Qt.DisplayRole:
            mapping = {
                1: user.name
            }
            return mapping.get(index.column())

        return None

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid():
            return False

        user: GroupMemberUser = self._data[index.row()]

        if role == Qt.CheckStateRole and index.column() == 0:
            user.marked = True if value == Qt.Checked.value else False
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

    def get_package(self, index) -> GroupMemberUser:
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
