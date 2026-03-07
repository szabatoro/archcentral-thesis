from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QModelIndex, QSortFilterProxyModel, QThread, Signal, Qt
from archcentral.ui.designer.usergroupmanager import Ui_UserGroupManager
from archcentral.controllers.usergroupmanager_controller import UserGroupManagerController

class UserManagerModule(QWidget, Ui_UserGroupManager):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(UserGroupManager=self)

        self.destroyed.connect(self.cleanup_thread)

        self.thread = QThread()

        self.ugmc: UserGroupManagerController = UserGroupManagerController()
        self.ugmc.moveToThread(self.thread)

        self.thread.start()

    def cleanup_thread(self) -> None:
        """Gracefully stops threads."""
        if self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()
