from archcentral.helpers.custom_classes import UserInfo
from archcentral.ui.designer.dialogs.userpasswordchangedialog import Ui_UserPasswordChangeDialog
from PySide6.QtWidgets import QDialog

class UserPasswordChangeDialog(QDialog, Ui_UserPasswordChangeDialog):
    def __init__(self, selected_user: UserInfo, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.user = selected_user.name

        self.password_edit.textChanged.connect(self.set_password)

    def set_password(self, password: str) -> None:
        self.password: str = password
