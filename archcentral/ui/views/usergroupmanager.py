from typing import Literal
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QModelIndex, QSortFilterProxyModel, QThread, Signal, Qt
from archcentral.ui.designer.usergroupmanager import Ui_UserGroupManager
from archcentral.controllers.usergroupmanager_controller import UserGroupManagerController
from archcentral.models.user_list import UserListModel
from archcentral.models.group_list import GroupListModel

class UserManagerModule(QWidget, Ui_UserGroupManager):
    fetch_data_signal: Signal = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(UserGroupManager=self)

        self.destroyed.connect(self.cleanup_thread)

        self.thread = QThread()

        self.ugmc: UserGroupManagerController = UserGroupManagerController()
        self.ugmc.moveToThread(self.thread)

        self.thread.start()

        self.ugmc.fetched_list.connect(self.initialize_model)

        self.fetch_data_signal.connect(self.ugmc.fetch_users_and_groups)
        self.fetch_data_signal.emit()

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

    def cleanup_thread(self) -> None:
        """Gracefully stops threads."""
        if self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()
