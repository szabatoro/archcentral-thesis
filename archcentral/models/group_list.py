from PySide6.QtCore import QAbstractTableModel, Qt
from archcentral.helpers.custom_classes import GroupInfo

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
        group: GroupInfo = self._data[index.row()]

        if role == Qt.DisplayRole:
            mapping = {
                0: group.name,
                1: group.users
            }
            return mapping.get(index.column())
        return None

    def refresh(self, new_data):
                self.beginResetModel()
                self._data = new_data
                self.endResetModel()

    def return_all_groups(self, name_only: bool = False) -> list[GroupInfo] | list[str]:
        """Returns all groups - either only their name or the entire object, depending on the parameter."""
        groups = []
        for group in self._data:
            groups.append(group.name if name_only else group)
        return groups

    def get_group_info_by_index(self, index) -> GroupInfo:
        """Returns the object found in the specified row."""
        return self._data[index.row()]

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers[section]
            else:
                return str(section + 1)
        return None
