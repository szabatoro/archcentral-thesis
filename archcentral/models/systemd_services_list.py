from PySide6.QtCore import QAbstractTableModel, Qt
from PySide6.QtGui import QColor
from archcentral.helpers.custom_classes import SystemdServiceInfo

# Model for the systemd service table
class SystemdServiceListModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data
        self._headers = ["Name", "State", "Status", "Substatus"]

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._headers)

    def data(self, index, role):
        service: SystemdServiceInfo = self._data[index.row()]

        if role == Qt.BackgroundRole and index.column() == 1:
            match service.enabledstate:
                case "enabled":
                    return QColor("green")
                case "disabled":
                    return QColor("red")

        if role == Qt.DisplayRole:
            mapping = {
                0: service.unitname,
                1: service.enabledstate,
                2: service.activestate,
                3: service.substate
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

    def get_unit(self, index) -> SystemdServiceInfo:
        """Returns the SystemdUnitInfo object found in the specified row."""
        return self._data[index.row()]

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self._headers[section]
            else:
                return str(section + 1)
        return None
