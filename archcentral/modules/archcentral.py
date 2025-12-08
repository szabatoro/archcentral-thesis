from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication, QMainWindow
from archcentral.modules.sysinfo import SysInfoModule
from archcentral.modules.packagemanager import PackageManagerModule
from archcentral.ui.designer.mainwindow import Ui_MainWindow
import sys

VERSION: str = "0.0.5"

# Main window of the application. All the modules will be loaded within this window
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(MainWindow=self)
        self.app_ver.setText(f"Version: {VERSION}")

        # instanciating widget modules
        self.sysinfo_widget: SysInfoModule = SysInfoModule()
        self.package_manager_widget: PackageManagerModule = PackageManagerModule()

        # setting up the displayarea stacked widgets with the modules
        self.display_area.addWidget(self.sysinfo_widget)
        self.display_area.addWidget(self.package_manager_widget)
        self.display_area.setCurrentWidget(self.sysinfo_widget)

        # setting up the buttons
        self.sys_info_button.setChecked(True)
        self.sys_info_button.clicked.connect(self.handle_sidebar)
        self.package_manager_button.clicked.connect(self.handle_sidebar)

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

# main function to launch the program
def main():
    app: QApplication = QApplication(sys.argv)
    window: MainWindow = MainWindow()
    window.show()
    sys.exit(app.exec())
