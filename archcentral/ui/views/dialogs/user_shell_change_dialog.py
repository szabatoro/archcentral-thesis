from archcentral.helpers.custom_classes import UserInfo
from archcentral.ui.designer.dialogs.userchangeshelldialog import Ui_UserChangeShellDialog
from PySide6.QtWidgets import QDialog

class UserChangeShellDialog(QDialog, Ui_UserChangeShellDialog):
    def __init__(self, selected_user: UserInfo, shell_list: list[str], parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.init_shell_list(shell_list)

        self.user = selected_user.name

        self.setWindowTitle(f"Change shell for user {self.user}")

        self.available_shells_box.textActivated.connect(self.set_shell)

    def set_shell(self, shell: str) -> None:
        """Saves the chosen shell from the combobox as a variable on the dialog object."""
        self.shell: str = shell

    def init_shell_list(self, raw_data: str) -> None:
        """Fills shells_box with the available shells, make bash the default if present"""
        sorted_data: list[str] = raw_data.splitlines()
        for data in sorted_data:
            self.available_shells_box.addItem(data)
        if "/usr/bin/bash" in sorted_data:
            self.available_shells_box.setCurrentText("/usr/bin/bash")
