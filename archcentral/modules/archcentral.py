from PySide6.QtCore import QObject
from PySide6.QtWidgets import QApplication, QMainWindow
from archcentral.modules.sysinfo import sys_info
from archcentral.modules.packagemanager import package_manager
from archcentral.ui.designer.mainwindow import Ui_MainWindow
import sys

VERSION: str = "0.0.1"

# Main window of the application. All the modules will be loaded within this window
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(MainWindow=self)
        self.app_ver.setText(f"Version: {VERSION}")

        # instanciating widget modules
        self.sysinfowidget: sys_info = sys_info()
        self.packagemanagerwidget: package_manager = package_manager()

        # setting up the displayarea stacked widgets with the modules
        self.displayarea.addWidget(self.sysinfowidget)
        self.displayarea.addWidget(self.packagemanagerwidget)
        self.displayarea.setCurrentWidget(self.sysinfowidget)

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
                if self.displayarea.currentWidget() is not self.sysinfowidget:
                    self.displayarea.setCurrentWidget(self.sysinfowidget)
            case self.package_manager_button:
                if self.displayarea.currentWidget() is not self.packagemanagerwidget:
                    self.displayarea.setCurrentWidget(self.packagemanagerwidget)

# main function to launch the program
def main():
    app: QApplication = QApplication(sys.argv)
    window: MainWindow = MainWindow()
    window.show()
    sys.exit(app.exec())
