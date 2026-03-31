from archcentral.helpers.custom_classes import UserInfo
from archcentral.ui.designer.dialogs.userchangefullnamedialog import Ui_UserChangeFullNameDialog
from PySide6.QtWidgets import QDialog

class UserChangeFullNameDialog(QDialog, Ui_UserChangeFullNameDialog):
    def __init__(self, selected_user: UserInfo, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.user = selected_user.name

        self.full_name_edit.textChanged.connect(self.set_full_name)

    def set_full_name(self, full_name: str) -> None:
        self.full_name: str = full_name
