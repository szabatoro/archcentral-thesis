from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication, QMainWindow
from archcentral.ui.views.sysinfo import SysInfoModule
from archcentral.ui.views.packagemanager import PackageManagerModule
from archcentral.ui.views.servicemanager import ServiceManagerModule
from archcentral.ui.views.usergroupmanager import UserManagerModule
from archcentral.ui.designer.mainwindow import Ui_MainWindow
import sys
from getpass import getuser

# Main window of the application. All the modules will be loaded within this window
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(MainWindow=self)

        # instanciating widget modules
        self.sysinfo_widget: SysInfoModule = SysInfoModule()
        self.package_manager_widget: PackageManagerModule = PackageManagerModule()
        self.service_manager_widget: ServiceManagerModule = ServiceManagerModule()
        self.user_group_manager_widget: UserManagerModule = UserManagerModule()

        self.welcome_label.setText(f"Welcome, {getuser()}!")

        # Gracefully shut down threads when exiting the app
        QApplication.instance().aboutToQuit.connect(self._call_module_thread_cleaners)

        # setting up the displayarea stacked widgets with the modules
        self.display_area.addWidget(self.sysinfo_widget)
        self.display_area.addWidget(self.package_manager_widget)
        self.display_area.addWidget(self.service_manager_widget)
        self.display_area.addWidget(self.user_group_manager_widget)
        self.display_area.setCurrentWidget(self.sysinfo_widget)

        # setting up the buttons
        self.sys_info_button.setChecked(True)
        self.sys_info_button.clicked.connect(self.handle_sidebar)
        self.package_manager_button.clicked.connect(self.handle_sidebar)
        self.service_manager_button.clicked.connect(self.handle_sidebar)
        self.user_group_manager_button.clicked.connect(self.handle_sidebar)

    # handling switching between modules via sidebar
    def handle_sidebar(self) -> None:
        # check the sender of the signal
        clicked_button: QObject = self.sender()
        # open the appropriate module
        match clicked_button:
            case self.sys_info_button:
                if self.display_area.currentWidget() is not self.sysinfo_widget:
                    self.display_area.setCurrentWidget(self.sysinfo_widget)
            case self.package_manager_button:
                if self.display_area.currentWidget() is not self.package_manager_widget:
                    self.display_area.setCurrentWidget(self.package_manager_widget)
            case self.service_manager_button:
                if self.display_area.currentWidget() is not self.service_manager_widget:
                    self.display_area.setCurrentWidget(self.service_manager_widget)
            case self.user_group_manager_button:
                if self.display_area.currentWidget() is not self.user_group_manager_widget:
                    self.display_area.setCurrentWidget(self.user_group_manager_widget)

    def _call_module_thread_cleaners(self) -> None:
        self.package_manager_widget.cleanup_thread()
        self.service_manager_widget.cleanup_thread()
        self.user_group_manager_widget.cleanup_thread()


# main function to launch the program
def main():
    app: QApplication = QApplication(sys.argv)
    window: MainWindow = MainWindow()
    window.show()
    sys.exit(app.exec())
