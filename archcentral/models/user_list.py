from PySide6.QtCore import QAbstractTableModel, Qt
from archcentral.helpers.custom_classes import UserInfo

class UserListModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data
        self._headers = ["Username", "UID", "GID", "GECOS", "Home", "Shell"]

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role=Qt.DisplayRole):
        user: UserInfo = self._data[index.row()]

        if role == Qt.DisplayRole:
            mapping = {
                0: user.name,
                1: user.uid,
                2: user.gid,
                3: user.gecos,
                4: user.home,
                5: user.shell
            }
            return mapping.get(index.column())
        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers[section]
            else:
                return str(section + 1)
        return None
