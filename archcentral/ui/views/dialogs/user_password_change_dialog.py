from archcentral.helpers.custom_classes import UserInfo
from archcentral.ui.designer.dialogs.userpasswordchangedialog import Ui_UserPasswordChangeDialog
from PySide6.QtWidgets import QDialog, QDialogButtonBox

class UserPasswordChangeDialog(QDialog, Ui_UserPasswordChangeDialog):
    def __init__(self, selected_user: UserInfo, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.user = selected_user.name

        self.setWindowTitle(f"Change password for user {self.user}")

        self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)

        self.password_edit.textChanged.connect(self.set_password)

    def set_password(self, password: str) -> None:
        """Checks whether the password input field is empty and saves its content as a variable on the dialog object."""
        if password:
             self.password: str = password
             self.button_box.button(QDialogButtonBox.Ok).setDisabled(False)
        else:
            self.button_box.button(QDialogButtonBox.Ok).setDisabled(True)
