from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QModelIndex, QSortFilterProxyModel, QThread, Signal, Qt
from archcentral.helpers.custom_classes import GroupInfo, UserInfo
from archcentral.ui.designer.usergroupmanager import Ui_UserGroupManager
from archcentral.controllers.usergroupmanager_controller import UserGroupManagerController
from archcentral.models.user_list import UserListModel
from archcentral.models.group_list import GroupListModel
from archcentral.ui.views.dialogs.group_add_dialog import GroupAddDialog
from archcentral.ui.views.dialogs.group_delete_dialog import GroupDeleteDialog
from archcentral.ui.views.dialogs.group_manage_users_dialog import GroupManageUsersDialog
from archcentral.ui.views.dialogs.user_add_dialog import UserAddDialog
from archcentral.ui.views.dialogs.user_delete_dialog import UserDeleteDialog
from archcentral.ui.views.dialogs.user_full_name_change_dialog import UserChangeFullNameDialog
from archcentral.ui.views.dialogs.user_homedir_change_dialog import UserChangeHomeDirDialog
from archcentral.ui.views.dialogs.user_password_change_dialog import UserPasswordChangeDialog
from archcentral.ui.views.dialogs.user_shell_change_dialog import UserChangeShellDialog

class UserGroupManager(QWidget, Ui_UserGroupManager):
    create_user_signal: Signal = Signal(str, str, str, str, str, str, list)
    delete_user_signal: Signal = Signal(str, bool)
    create_group_signal: Signal = Signal(str, bool, list)
    delete_group_signal: Signal = Signal(str)
    fetch_data_signal: Signal = Signal(bool) # True for refreshing, False for initalizing
    fetch_shells_signal: Signal = Signal(bool)
    change_user_password_signal: Signal = Signal(str, str)
    change_user_shell_signal: Signal = Signal(str, str)
    change_user_full_name_signal: Signal = Signal(str, str)
    change_user_homedir_signal: Signal = Signal(str, str)
    modify_group_users_signal: Signal = Signal(str, list)

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(UserGroupManager=self)

        self.destroyed.connect(self.cleanup_thread)

        self.ugmc_thread = QThread()

        self.ugmc: UserGroupManagerController = UserGroupManagerController()
        self.ugmc.moveToThread(self.ugmc_thread)

        self.ugmc_thread.start()

        # Connecting data sources from the controller for model initialization and refreshing
        self.ugmc.fetched_list_for_init.connect(self.initialize_models)
        self.ugmc.fetched_list_for_refresh.connect(self.refresh_lists)

        # User modification status messages
        self.ugmc.created_user_signal.connect(
            lambda user, exit_code: self.status_label.setText(f"{user} created." if exit_code == 0 else "User creation aborted.")
        )
        self.ugmc.changed_password_signal.connect(
            lambda user, exit_code: self.status_label.setText(f"Password changed for user {user}." if exit_code == 0 else "Password change aborted.")
        )
        self.ugmc.changed_shell_signal.connect(
            lambda user, exit_code: self.status_label.setText(f"Shell changed for user {user}." if exit_code == 0 else "Shell change aborted.")
        )
        self.ugmc.changed_full_name_signal.connect(
            lambda user, exit_code: self.status_label.setText(f"Full name changed for user {user}." if exit_code == 0 else "Full name change aborted.")
        )
        self.ugmc.changed_homedir_signal.connect(
            lambda user, exit_code: self.status_label.setText(f"Home directory changed for user {user}." if exit_code == 0 else "Home directory change aborted.")
        )
        self.ugmc.deleted_user_signal.connect(
            lambda user, exit_code: self.status_label.setText(f"{user} successfully deleted." if exit_code == 0 else "User deletion aborted.")
        )
        self.ugmc.changed_group_members_signal.connect(
            lambda group, exit_code: self.status_label.setText(f"Group member changes in {group} group performed successfully." if exit_code == 0 else "Group member changes aborted.")
        )
        self.ugmc.created_group_signal.connect(
            lambda group, exit_code: self.status_label.setText(f"{group} group created successfully." if exit_code == 0 else "Group creation aborted.")
        )
        self.ugmc.deleted_group_signal.connect(
            lambda group, exit_code: self.status_label.setText(f"{group} group deleted successfully." if exit_code == 0 else "Group deletion aborted.")
        )

        # Calls data fetcher controller function to initialize the models
        self.fetch_data_signal.connect(self.ugmc.fetch_users_and_groups)
        self.fetch_data_signal.emit(False)

        # Sets up the user creator by first fetching all available shells, then calling the user creator dialog
        self.fetch_shells_signal.connect(self.ugmc.get_shell_list)
        self.ugmc.fetched_available_shells_for_user_creation.connect(self.open_user_add_dialog)
        self.add_user_button.clicked.connect(lambda: self.fetch_shells_signal.emit(True))

        # Calls the shell fetcher, then opens the shell changer dialog
        self.ugmc.fetched_available_shells_for_shell_change.connect(self.open_user_change_shell_dialog)
        self.change_shell_button.clicked.connect(lambda: self.fetch_shells_signal.emit(False))

        self.change_password_button.clicked.connect(self.open_user_change_password_dialog)

        self.change_full_name_button.clicked.connect(self.open_user_change_full_name_dialog)

        self.change_homedir_button.clicked.connect(self.open_user_change_homedir_dialog)

        self.delete_user_button.clicked.connect(self.open_user_deletion_dialog)

        self.manage_users_button.clicked.connect(self.open_manage_group_members_dialog)

        self.create_group_button.clicked.connect(self.open_create_group_dialog)

        self.delete_group_button.clicked.connect(self.open_group_deletion_dialog)

        # Connect signals emitted after finishing the dialogs to their respective controller functions
        self.create_user_signal.connect(self.ugmc.user_add)
        self.change_user_password_signal.connect(self.ugmc.passwd)
        self.change_user_shell_signal.connect(self.ugmc.change_shell)
        self.change_user_full_name_signal.connect(self.ugmc.change_full_name)
        self.change_user_homedir_signal.connect(self.ugmc.change_homedir)
        self.modify_group_users_signal.connect(self.ugmc.modify_group_users)
        self.create_group_signal.connect(self.ugmc.group_add)

    def _get_selected_row(self) -> UserInfo | GroupInfo:
        """Returns the object connected to the selected row from the model."""
        match self.users_groups_tab.currentIndex():
            case 0:
                source_index: QModelIndex = self.user_list_proxy_model.mapToSource(self.user_list_table.currentIndex())
                selected_service: UserInfo = self.user_list_model.get_user_info_by_index(source_index)
            case 1:
                source_index: QModelIndex = self.group_list_proxy_model.mapToSource(self.group_list_table.currentIndex())
                selected_service: GroupInfo = self.group_list_model.get_group_info_by_index(source_index)

        return selected_service

    def initialize_models(self, user_data, group_data) -> None:
        """Initializes the models with relevant data."""
        self.user_list_model: UserListModel = UserListModel(user_data)
        self.user_list_proxy_model: QSortFilterProxyModel = QSortFilterProxyModel()
        self.user_list_proxy_model.setDynamicSortFilter(True)
        self.user_list_proxy_model.sort(0, Qt.AscendingOrder)
        self.user_list_proxy_model.setSourceModel(self.user_list_model)
        self.user_list_proxy_model.setFilterKeyColumn(0)

        self.user_list_table.setModel(self.user_list_proxy_model)

        self.group_list_model: GroupListModel = GroupListModel(group_data)
        self.group_list_proxy_model: QSortFilterProxyModel = QSortFilterProxyModel()
        self.group_list_proxy_model.setDynamicSortFilter(True)
        self.group_list_proxy_model.sort(0, Qt.AscendingOrder)
        self.group_list_proxy_model.setSourceModel(self.group_list_model)
        self.group_list_proxy_model.setFilterKeyColumn(0)

        self.group_list_table.setModel(self.group_list_proxy_model)

    def refresh_lists(self, new_user_data, new_group_data) -> None:
        """Refreshes the user and/or group lists with the given data."""
        self.user_list_model.refresh(new_user_data)
        self.group_list_model.refresh(new_group_data)

    def open_user_add_dialog(self, available_shells) -> None:
        """Pops up a user creation window."""
        users: list[str] = self.user_list_model.return_all_users()
        groups: list[GroupInfo] = self.group_list_model.return_all_groups(name_only=True)
        dialog: UserAddDialog = UserAddDialog(users, available_shells, groups, parent=self)
        result = dialog.exec()
        match result:
            case 0:
                self.status_label.setText("Adding user aborted.")
            case 1:
                self.status_label.setText("Adding user in process...")
                self.create_user_signal.emit(
                    dialog.current_edited_user.username,
                    dialog.current_edited_user.fullname,
                    dialog.current_edited_user.homedir,
                    dialog.current_edited_user.homedirtype,
                    dialog.current_edited_user.password,
                    dialog.current_edited_user.shell,
                    dialog.current_edited_user.groups
                )
            case _:
                self.status_label.setText("Adding user aborted.")

    def open_user_change_password_dialog(self) -> None:
        """Pops up password change dialog."""
        dialog: UserPasswordChangeDialog = UserPasswordChangeDialog(selected_user=self._get_selected_row(), parent=self)
        result = dialog.exec()
        match result:
            case 0:
                self.status_label.setText("Password change aborted.")
            case 1:
                self.status_label.setText("Password change in process...")
                self.change_user_password_signal.emit(
                    dialog.user,
                    dialog.password
                )
            case _:
                self.status_label.setText("Password change aborted.")

    def open_user_change_shell_dialog(self, available_shells) -> None:
        """Pops up shell change dialog."""
        dialog: UserChangeShellDialog = UserChangeShellDialog(selected_user=self._get_selected_row(), shell_list=available_shells, parent=self)
        result = dialog.exec()
        match result:
            case 0:
                self.status_label.setText("Shell change aborted.")
            case 1:
                self.status_label.setText("Shell change in process...")
                self.change_user_shell_signal.emit(
                    dialog.user,
                    dialog.shell
                )
            case _:
                self.status_label.setText("Shell change aborted.")

    def open_user_change_full_name_dialog(self) -> None:
        """Pops up full name change dialog."""
        dialog: UserChangeFullNameDialog = UserChangeFullNameDialog(selected_user=self._get_selected_row(), parent=self)
        result = dialog.exec()
        match result:
            case 0:
                self.status_label.setText("Full name change aborted.")
            case 1:
                self.status_label.setText("Full name change in process...")
                self.change_user_full_name_signal.emit(
                    dialog.user,
                    dialog.full_name
                )
            case _:
                self.status_label.setText("Full name change aborted.")

    def open_user_change_homedir_dialog(self) -> None:
        """Pops up home directory change dialog."""
        dialog: UserChangeHomeDirDialog = UserChangeHomeDirDialog(
            selected_user=self._get_selected_row(),
            userlist=self.user_list_model.return_all_users(),
            parent=self
        )
        result = dialog.exec()
        match result:
            case 0:
                self.status_label.setText("Home directory change aborted.")
            case 1:
                self.status_label.setText("Home directory change in process...")
                self.change_user_homedir_signal.emit(
                    dialog.user,
                    dialog.homedir
                )
            case _:
                self.status_label.setText("Home directory change aborted.")

    def open_user_deletion_dialog(self) -> None:
        """Pops up user deletion dialog."""
        dialog: UserDeleteDialog = UserDeleteDialog(selected_user=self._get_selected_row(), parent=self)
        result = dialog.exec()
        match result:
            case 0:
                self.status_label.setText("User deletion aborted.")
            case 1:
                self.status_label.setText("User deletion in progress...")
                self.delete_user_signal.emit(
                    dialog.user,
                    dialog.homedir_delete
                )
            case _:
                self.status_label.setText("User deletion aborted.")

    def open_manage_group_members_dialog(self) -> None:
        """Pops up group member manager dialog."""
        dialog: GroupManageUsersDialog = GroupManageUsersDialog(
            group=self._get_selected_row(), userlist=self.user_list_model.return_all_users(name_only=True), parent=self
        )
        result = dialog.exec()
        match result:
            case 0:
                self.status_label.setText("Group member changes aborted.")
            case 1:
                if dialog.marked_users:
                    self.status_label.setText("Group member changes in process...")
                    self.modify_group_users_signal.emit(
                        dialog.group.name,
                        dialog.marked_users
                    )
            case _:
                self.status_label.setText("Group member changes aborted.")

    def open_create_group_dialog(self) -> None:
        """Pops up group creation dialog."""
        dialog: GroupAddDialog = GroupAddDialog(
            groups=self.group_list_model.return_all_groups(name_only=True),
            userlist=self.user_list_model.return_all_users(name_only=True),
            parent=self
        )
        result = dialog.exec()
        match result:
            case 0:
                self.status_label.setText("Group creation aborted.")
            case 1:
                self.status_label.setText("Group creation in process...")
                self.create_group_signal.emit(
                     dialog.current_edited_group.group_name,
                     dialog.current_edited_group.is_system_group,
                     dialog.current_edited_group.users
                )
            case _:
                self.status_label.setText("Group creation aborted.")

    def open_group_deletion_dialog(self) -> None:
        """Pops up user deletion dialog."""
        dialog: GroupDeleteDialog = GroupDeleteDialog(selected_group=self._get_selected_row(), parent=self)
        result = dialog.exec()
        match result:
            case 0:
                self.status_label.setText("Group deletion aborted.")
            case 1:
                self.status_label.setText("Group deletion in progress...")
                self.delete_group_signal.emit(
                    dialog.group
                )
            case _:
                self.status_label.setText("Group deletion aborted.")

    def cleanup_thread(self) -> None:
        """Gracefully stops threads."""
        if self.ugmc_thread.isRunning():
            self.ugmc_thread.quit()
            self.ugmc_thread.wait()
