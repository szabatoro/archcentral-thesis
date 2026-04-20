from PySide6.QtGui import Qt
from archcentral.helpers.custom_classes import EditedGroup
from archcentral.ui.designer.dialogs.groupadddialog import Ui_GroupAddDialog
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QFileDialog, QListWidgetItem

class GroupAddDialog(QDialog, Ui_GroupAddDialog):
    def __init__(self, userlist: list[str], groups: list[str], parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.current_edited_group = EditedGroup()

        self.groups = groups

        self.init_users(userlist)

        self.group_name_edit.textChanged.connect(self.set_groupname)
        self.user_list.clicked.connect(self.set_users)
        self.system_group_checkbox.checkStateChanged.connect(self.set_system_group_status)

    def set_groupname(self, groupname: str) -> None:
        """Checks whether there already is a group with the given groupname on the system."""
        if groupname in self.groups:
            self.group_name_edit.setStyleSheet("background: #6d3c3c;")
            self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)
            self.status_label.setText(f"Group with name: \"{groupname}\" already exists.")
        else:
            self.current_edited_group.group_name = groupname
            self.group_name_edit.setStyleSheet("")
            self.button_box.button(QDialogButtonBox.Ok).setEnabled(True)
            self.status_label.setText("")

    def set_users(self) -> None:
        selected_users: list = []
        for i in range(self.user_list.count()):
            item = self.user_list.item(i)
            if item.checkState() == Qt.Checked:
                selected_users.append(item.text())
        self.current_edited_group.users = selected_users

    def set_system_group_status(self, checkstate) -> None:
        match checkstate:
            case Qt.Unchecked:
                self.current_edited_group.is_system_group = False
            case Qt.Checked:
                self.current_edited_group.is_system_group = True

    def init_users(self, users: list[str]) -> None:
        """Fills the users list with available users on the system."""
        for user in users:
            item: QListWidgetItem = QListWidgetItem(user)
            item.setCheckState(Qt.Unchecked)
            self.user_list.addItem(item)
