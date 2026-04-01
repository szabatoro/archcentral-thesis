from PySide6.QtCore import QSortFilterProxyModel
from archcentral.helpers.custom_classes import GroupInfo, GroupMemberUser
from archcentral.models.dialogs.group_manage_users_list import GroupManageUsersListTableModel
from archcentral.ui.designer.dialogs.groupmanageusersdialog import Ui_GroupManageUsersDialog
from PySide6.QtWidgets import QDialog
from PySide6.QtGui import Qt

class GroupManageUsersDialog(QDialog, Ui_GroupManageUsersDialog):
    def __init__(self, group: GroupInfo, userlist: str, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.userlist: str = userlist
        self.group: GroupInfo = group

        self.setWindowTitle(f"Manage users for group {self.group.name}")

        self.marked_users: list[list[str, bool]] = []

        self.initialize_model()

        self.user_list_table.clicked.connect(self.on_user_list_table_clicked)

    def initialize_model(self) -> None:
        model_data: list[GroupMemberUser] = []
        for user in self.userlist:
            user_in_group: bool = False
            user_in_group = user in self.group.users
            model_data.append(GroupMemberUser(False, user, user_in_group))

        self.user_list_model: GroupManageUsersListTableModel = GroupManageUsersListTableModel(model_data)
        self.user_list_proxy_model: QSortFilterProxyModel = QSortFilterProxyModel()
        self.user_list_proxy_model.setDynamicSortFilter(True)
        self.user_list_proxy_model.sort(0, Qt.AscendingOrder)
        self.user_list_proxy_model.setSourceModel(self.user_list_model)
        self.user_list_proxy_model.setFilterKeyColumn(0)

        self.user_list_table.setModel(self.user_list_proxy_model)

    def on_user_list_table_clicked(self) -> None:
        self.marked_users = self.user_list_model.get_marked_users()
