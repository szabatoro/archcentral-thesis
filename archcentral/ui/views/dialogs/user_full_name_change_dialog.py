from archcentral.helpers.custom_classes import UserInfo
from archcentral.ui.designer.dialogs.userchangefullnamedialog import Ui_UserChangeFullNameDialog
from PySide6.QtWidgets import QDialog, QDialogButtonBox

class UserChangeFullNameDialog(QDialog, Ui_UserChangeFullNameDialog):
    def __init__(self, selected_user: UserInfo, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.user = selected_user.name

        self.setWindowTitle(f"Change full name for user {self.user}")

        self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)

        self.full_name_edit.textChanged.connect(self.set_full_name)

    def set_full_name(self, full_name: str) -> None:
        """Checks whether full name input field is empty and saves its content as a variable on the dialog object."""
        if full_name:
            self.full_name: str = full_name
            self.button_box.button(QDialogButtonBox.Ok).setDisabled(False)
        else:
            self.button_box.button(QDialogButtonBox.Ok).setDisabled(True)
