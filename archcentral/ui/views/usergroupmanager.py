from typing import Literal
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QModelIndex, QSortFilterProxyModel, QThread, Signal, Qt
from archcentral.helpers.custom_classes import GroupInfo, UserInfo
from archcentral.ui.designer.usergroupmanager import Ui_UserGroupManager
from archcentral.controllers.usergroupmanager_controller import UserGroupManagerController
from archcentral.models.user_list import UserListModel
from archcentral.models.group_list import GroupListModel
from archcentral.ui.views.dialogs.user_add_dialog import UserAddDialog

class UserManagerModule(QWidget, Ui_UserGroupManager):
    create_user_signal: Signal = Signal(str, str, str, str, str, str)
    fetch_data_signal: Signal = Signal(bool)

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(UserGroupManager=self)

        self.destroyed.connect(self.cleanup_thread)

        self.thread = QThread()

        self.ugmc: UserGroupManagerController = UserGroupManagerController()
        self.ugmc.moveToThread(self.thread)

        self.thread.start()

        self.ugmc.fetched_list_for_init.connect(self.initialize_model)
        self.ugmc.fetched_list_for_refresh.connect(self.refresh_lists)

        self.fetch_data_signal.connect(self.ugmc.fetch_users_and_groups)
        self.fetch_data_signal.emit(False)

        self.ugmc.fetched_available_shells.connect(self.open_user_add_dialog)
        self.add_user_button.clicked.connect(self.ugmc.get_shell_list)

        self.create_user_signal.connect(self.ugmc.user_add)

    def _get_selected_row(self) -> UserInfo | GroupInfo:
        """Fetches the object stored in the selected row."""
        match self.users_groups_tab.currentIndex():
            case 0:
                source_index: QModelIndex = self.user_list_proxy_model.mapToSource(self.user_list_table.currentIndex())
                selected_service = self.user_list_model.get_user_info_by_index(source_index)
            case 1:
                source_index: QModelIndex = self.groups_list_proxy_model.mapToSource(self.group_list_table.currentIndex())
                selected_service = self.groups_list_model.get_group_info_by_index(source_index)

        return selected_service

    def initialize_model(self, data, data_type: Literal["users", "groups"]) -> None:
        """Initializes the selected model with relevant data."""
        match data_type:
            case "users":
                self.user_list_model: UserListModel = UserListModel(data)
                self.user_list_proxy_model: QSortFilterProxyModel = QSortFilterProxyModel()
                self.user_list_proxy_model.setDynamicSortFilter(True)
                self.user_list_proxy_model.sort(0, Qt.AscendingOrder)
                self.user_list_proxy_model.setSourceModel(self.user_list_model)
                self.user_list_proxy_model.setFilterKeyColumn(0)

                self.user_list_table.setModel(self.user_list_proxy_model)

            case "groups":
                self.groups_list_model: GroupListModel = GroupListModel(data)
                self.groups_list_proxy_model: QSortFilterProxyModel = QSortFilterProxyModel()
                self.groups_list_proxy_model.setDynamicSortFilter(True)
                self.groups_list_proxy_model.sort(0, Qt.AscendingOrder)
                self.groups_list_proxy_model.setSourceModel(self.groups_list_model)
                self.groups_list_proxy_model.setFilterKeyColumn(0)

                self.group_list_table.setModel(self.groups_list_proxy_model)

    def refresh_lists(self, new_data, data_type: Literal["users", "groups"]) -> None:
        """Refreshes the user and/or group lists with the given data."""
        match data_type:
            case "users":
                    self.user_list_model.refresh(new_data)
            case "groups":
                    self.groups_list_model.refresh(new_data)

    def open_user_add_dialog(self, available_shells) -> None:
        """Pops up a user creation window."""
        users: list[str] = self.user_list_model.return_all_users(name_only=True)
        dialog: UserAddDialog = UserAddDialog(users, available_shells, parent=self)
        result = dialog.exec()
        match result:
            case 0:
                print("aborted")
            case 1:
                self.create_user_signal.emit(
                    dialog.current_edited_user.username,
                    dialog.current_edited_user.fullname,
                    dialog.current_edited_user.homedir,
                    dialog.current_edited_user.homedirtype,
                    dialog.current_edited_user.password,
                    dialog.current_edited_user.shell
                )
            case _:
                print("something went wrong")

    def cleanup_thread(self) -> None:
        """Gracefully stops threads."""
        if self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()
