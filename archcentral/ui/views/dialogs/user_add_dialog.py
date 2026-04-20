from os.path import isdir
from PySide6.QtGui import Qt
from archcentral.helpers.custom_classes import EditedUser, GroupInfo, UserInfo
from archcentral.ui.designer.dialogs.useradddialog import Ui_UserAddDialog
from PySide6.QtWidgets import QDialog, QDialogButtonBox, QFileDialog, QListWidgetItem

class UserAddDialog(QDialog, Ui_UserAddDialog):
    def __init__(self, userlist: list[UserInfo], available_shells: list[str], groups: list[GroupInfo], parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)

        self.current_edited_user = EditedUser()
        self.userlist: list[UserInfo] = userlist

        # initialize shell list and group list
        self.init_shell_list(available_shells)
        self.init_groups(groups)

        # connect user edited properties with the User() setter functions
        self.user_name_edit.textChanged.connect(self.set_user_name)
        self.full_name_edit.textChanged.connect(self.set_full_name)
        self.password_edit.textChanged.connect(self.set_user_password)
        self.home_dir_edit.textChanged.connect(self.set_user_home_dir)
        self.shells_box.textActivated.connect(self.set_user_shell)
        self.group_list.itemChanged.connect(self.group_list_signal_transmitter)

        # check which radio button is clicked
        self.home_button_group.buttonClicked.connect(lambda: self.check_clicked_home_button())

        self.admin_checkbox.checkStateChanged.connect(self.check_admin_checkbox)

        self.file_browser_button.clicked.connect(self.open_homedir_selector)

    def field_validator(self) -> None:
        """Checks fields for validity, disables OK button and shows status message accordingly."""
        username_taken = any(user.name == self.current_edited_user.username for user in self.userlist)
        username_empty = self.current_edited_user.username == ""
        homedir_taken = any(user.home == self.current_edited_user.homedir for user in self.userlist)
        homedir_empty = self.current_edited_user.homedir == "" and self.home_dir_edit.isEnabled()
        homedir_does_not_exist = not isdir(self.current_edited_user.homedir) and self.current_edited_user.homedir != "" and self.home_dir_edit.isEnabled()
        password_empty = self.current_edited_user.password == ""

        self.user_name_edit.setStyleSheet("background: #6d3c3c;") if username_taken else self.user_name_edit.setStyleSheet("")
        self.home_dir_edit.setStyleSheet("background: #6d3c3c;")if homedir_taken or homedir_does_not_exist else self.home_dir_edit.setStyleSheet("")

        status_messages: list[str] = []
        if username_taken:
            status_messages.append(f"User with name: \"{self.current_edited_user.username}\" already exists.")
        if homedir_taken:
            status_messages.append(f"\"{self.current_edited_user.homedir}\" directory is already taken.")
        if homedir_does_not_exist:
            status_messages.append(f"\"{self.current_edited_user.homedir}\" directory does not exist.")

        self.status_label.setText(" ".join(status_messages))
        dialogbox_status = (username_taken or
            homedir_taken or
            username_empty or
            homedir_empty or
            homedir_does_not_exist or
            password_empty
        )

        self.button_box.button(QDialogButtonBox.Ok).setDisabled(dialogbox_status)

    def group_list_signal_transmitter(self) -> None:
        """Groups functions that are called by changes in the group list selector."""
        self.check_wheel_status()
        self.set_groups()

    def set_user_name(self, username) -> None:
        """Setters for the current_edited_user object"""
        self.current_edited_user.username = username
        self.field_validator()
    def set_full_name(self, fullname) -> None:
        self.current_edited_user.fullname = fullname
    def set_user_home_dir(self, homedir) -> None:
        self.current_edited_user.homedir = homedir
        self.field_validator()
    def set_user_password(self, password) -> None:
        self.current_edited_user.password = password
        self.field_validator()
    def set_user_shell(self, shell) -> None:
        self.current_edited_user.shell = shell
    def set_groups(self) -> None:
        selected_groups: list = []
        for i in range(self.group_list.count()):
            item = self.group_list.item(i)
            if item.checkState() == Qt.Checked:
                selected_groups.append(item.text())
        self.current_edited_user.groups = selected_groups

    def init_shell_list(self, raw_data: str) -> None:
        """Fills shells_box with the available shells, make bash the default if present"""
        sorted_data: list[str] = raw_data.splitlines()
        for data in sorted_data:
            self.shells_box.addItem(data)
        if "/usr/bin/bash" in sorted_data:
            self.shells_box.setCurrentText("/usr/bin/bash")

    def init_groups(self, groups: list[str]) -> None:
        """Fills the group list with available groups on the system."""
        for group in groups:
            item: QListWidgetItem = QListWidgetItem(group)
            item.setCheckState(Qt.Unchecked)
            self.group_list.addItem(item)

    def check_admin_checkbox(self, check_status) -> None:
        """Updates the status of the wheel item in the group selector."""
        wheel_item: QListWidgetItem = self.group_list.findItems("wheel", Qt.MatchExactly)[0]
        match check_status:
            case Qt.Checked:
                wheel_item.setCheckState(Qt.Checked)
            case Qt.Unchecked:
                wheel_item.setCheckState(Qt.Unchecked)

    def check_wheel_status(self) -> None:
        """Updates the status of the admin checkbox depending on the wheel item status."""
        wheel_item: QListWidgetItem = self.group_list.findItems("wheel", Qt.MatchExactly)[0]
        match wheel_item.checkState():
            case Qt.Checked:
                self.admin_checkbox.setCheckState(Qt.Checked)
            case Qt.Unchecked:
                self.admin_checkbox.setCheckState(Qt.Unchecked)

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
        self.field_validator()

    def open_homedir_selector(self):
        """Opens a folder selector and sets the homedir path to the selected folder."""
        homedir = QFileDialog.getExistingDirectory(
            parent=self,
            caption="Select the new user's home directory",
            dir="/home"
        )
        if homedir:
            self.home_dir_edit.setText(homedir)
