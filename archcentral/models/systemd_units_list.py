from PySide6.QtCore import QAbstractTableModel, Qt
from archcentral.helpers.custom_classes import SystemdServiceInfo

# Model for the systemd service table
class SystemdServiceListModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data
        self._headers = ["Name", "State", "Substate"]

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role):
        service: SystemdServiceInfo = self._data[index.row()]

        if role == Qt.DisplayRole:
            mapping = {
                0: service.unitname,
                1: service.servicestate,
                2: service.runstate,
            }
            return mapping.get(index.column())

        return None

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid():
            return False
        return False

    def refresh(self, new_data):
            self.beginResetModel()
            self._data = new_data
            self.endResetModel()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers[section]
            else:
                return str(section + 1)
        return None
