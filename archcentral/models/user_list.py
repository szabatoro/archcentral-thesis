from PySide6.QtCore import QAbstractTableModel, Qt
from archcentral.helpers.custom_classes import UserInfo

class UserListModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data
        self._headers = ["Username", "UID", "GID", "Full name", "Home", "Shell"]

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

    def refresh(self, new_data):
            self.beginResetModel()
            self._data = new_data
            self.endResetModel()

    def get_user_info(self, username: str) -> UserInfo:
        for user in self._data:
            if user.name == username:
                return user

    def get_user_info_by_index(self, index) -> UserInfo:
        """Returns the object found in the specified row."""
        return self._data[index.row()]

    def return_all_users(self, name_only: bool = False) -> list[UserInfo] | list[str]:
        """Returns all users - either only their name or the entire object, depending on the parameter."""
        users = []
        for user in self._data:
            users.append(user.name if name_only else user)
        return users

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers[section]
            else:
                return str(section + 1)
        return None
