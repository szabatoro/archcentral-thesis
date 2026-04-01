from os.path import isdir
from archcentral.helpers.custom_classes import UserInfo
from archcentral.ui.designer.dialogs.userchangehomedirdialog import Ui_UserChangeHomeDirDialog
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QFileDialog

class UserChangeHomeDirDialog(QDialog, Ui_UserChangeHomeDirDialog):
    def __init__(self, selected_user: UserInfo, userlist: list[UserInfo],parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.user = selected_user.name
        self.userlist = userlist

        self.setWindowTitle(f"Change home directory for user {self.user}")

        self.homedir_edit.setText(selected_user.home)

        self.homedir_edit.textChanged.connect(self.set_homedir)

        self.homedir_button.clicked.connect(self.open_homedir_selector)

    def field_validator(self) -> None:
        """Checks fields for validity, disables OK button and shows status message accordingly."""
        homedir_taken = any((user.home == self.homedir and user.name != self.user) for user in self.userlist)
        homedir_empty = self.homedir == "" and self.homedir_edit.isEnabled()
        homedir_does_not_exist = not isdir(self.homedir) and self.homedir != "" and self.homedir_edit.isEnabled()

        self.homedir_edit.setStyleSheet("background: #6d3c3c;")if homedir_taken or homedir_does_not_exist else self.homedir_edit.setStyleSheet("")

        status_messages: list[str] = []
        if homedir_taken:
            status_messages.append(f"\"{self.homedir}\" directory is already taken.")
        if homedir_does_not_exist:
            status_messages.append(f"\"{self.homedir}\" directory does not exist.")

        self.status_label.setText(" ".join(status_messages))
        dialogbox_status = homedir_taken or homedir_empty or homedir_does_not_exist

        self.button_box.button(QDialogButtonBox.Ok).setDisabled(dialogbox_status)

    def set_homedir(self, homedir: str) -> None:
        """Saves the homedir input field's content as a variable on the dialog object."""
        self.homedir: str = homedir
        self.field_validator()

    def open_homedir_selector(self) -> None:
        """Opens a folder selector and sets the homedir path to the selected folder."""
        homedir = QFileDialog.getExistingDirectory(
            parent=self,
            caption="Select the new home directory",
            dir="/home"
        )
        if homedir:
            self.homedir_edit.setText(homedir)
