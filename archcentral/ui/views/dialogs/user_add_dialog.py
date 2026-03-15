from archcentral.helpers.custom_classes import EditedUser
from archcentral.ui.designer.dialogs.useradddialog import Ui_UserAddDialog
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QFileDialog

class UserAddDialog(QDialog, Ui_UserAddDialog):
    def __init__(self, userlist, available_shells, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.current_edited_user = EditedUser()
        self.userlist: list[str] = userlist

        # initialize shell list
        self.init_shell_list(available_shells)

        # connect user edited properties with the User() setter functions
        self.user_name_edit.textChanged.connect(self.set_user_name)
        self.full_name_edit.textChanged.connect(self.set_full_name)
        self.password_edit.textChanged.connect(self.set_user_password)
        self.home_dir_edit.textChanged.connect(self.set_user_home_dir)
        self.shells_box.textActivated.connect(self.set_user_shell)

        # check which radio button is clicked
        self.home_button_group.buttonClicked.connect(lambda: self.check_clicked_home_button())

        self.file_browser_button.clicked.connect(self.open_homedir_selector)

    def set_user_name(self, username) -> None:
        """Setters for the current_edited_user object"""
        if username not in self.userlist:
            self.current_edited_user.username = username
            self.button_box.button(QDialogButtonBox.Ok).setEnabled(True)
        else:
            self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)
    def set_full_name(self, fullname) -> None:
        self.current_edited_user.fullname = fullname
    def set_user_home_dir(self, homedir) -> None:
        self.current_edited_user.homedir = homedir
    def set_user_password(self, password) -> None:
        self.current_edited_user.password = password
    def set_user_shell(self, shell) -> None:
        self.current_edited_user.shell = shell

    def init_shell_list(self, raw_data: str) -> None:
        """Fills shells_box with the available shells, make bash the default if present"""
        sorted_data: list[str] = raw_data.splitlines()
        for data in sorted_data:
            self.shells_box.addItem(data)
        if "/usr/bin/bash" in sorted_data:
            self.shells_box.setCurrentText("/usr/bin/bash")

    def check_clicked_home_button(self) -> None:
        """Checks which button is clicked and sets the homedir selector accordingly"""
        checked_button = self.home_button_group.checkedButton().objectName()
        match checked_button:
            case "no_home_button":
                self.current_edited_user.homedirtype = "none"
                self.home_dir_edit.setEnabled(False)
                self.file_browser_button.setEnabled(False)
            case "existing_home_button":
                self.current_edited_user.homedirtype = "selectexisting"
                self.home_dir_edit.setEnabled(True)
                self.file_browser_button.setEnabled(True)
            case "auto_home_button":
                self.current_edited_user.homedirtype = "auto"
                self.home_dir_edit.setEnabled(False)
                self.file_browser_button.setEnabled(False)

    def open_homedir_selector(self):
        """Opens a folder selector and sets the homedir path to the selected folder."""
        homedir = QFileDialog.getExistingDirectory(
            parent=self,
            caption="Select the new user's home directory",
            dir="/home"
        )
        if homedir:
            self.home_dir_edit.setText(homedir)
