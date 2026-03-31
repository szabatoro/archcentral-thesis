from archcentral.helpers.custom_classes import UserInfo
from archcentral.ui.designer.dialogs.userchangehomedirdialog import Ui_UserChangeHomeDirDialog
from PySide6.QtWidgets import QDialog, QFileDialog

class UserChangeHomeDirDialog(QDialog, Ui_UserChangeHomeDirDialog):
    def __init__(self, selected_user: UserInfo, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.user = selected_user.name
        self.homedir_edit.setText(selected_user.home)

        self.homedir_edit.textChanged.connect(self.set_full_name)

        self.homedir_button.clicked.connect(self.open_homedir_selector)

    def set_full_name(self, homedir: str) -> None:
        self.homedir: str = homedir

    def open_homedir_selector(self) -> None:
        """Opens a folder selector and sets the homedir path to the selected folder."""
        homedir = QFileDialog.getExistingDirectory(
            parent=self,
            caption="Select the new home directory",
            dir="/home"
        )
        if homedir:
            self.homedir_edit.setText(homedir)
