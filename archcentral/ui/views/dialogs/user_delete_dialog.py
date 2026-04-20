from archcentral.helpers.custom_classes import UserInfo
from archcentral.ui.designer.dialogs.userdeletedialog import Ui_UserDeleteDialog
from PySide6.QtWidgets import QDialog
from PySide6.QtGui import Qt

class UserDeleteDialog(QDialog, Ui_UserDeleteDialog):
    def __init__(self, selected_user: UserInfo, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.user = selected_user.name
        self.homedir_delete: bool = False

        self.user_delete_label.setText(f"Are you sure you want to delete user \"{self.user}\"?")

        self.delete_homedir_checkbox.checkStateChanged.connect(self.set_homedir_delete)

    def set_homedir_delete(self, checkstate) -> None:
        match checkstate:
            case Qt.Unchecked:
                self.homedir_delete = False
            case Qt.Checked:
                self.homedir_delete = True
