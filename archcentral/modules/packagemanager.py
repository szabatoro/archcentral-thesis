from PySide6.QtWidgets import QWidget
from archcentral.ui.designer.packagemanager import Ui_package_manager

# package manager module placeholder
class package_manager(QWidget, Ui_package_manager):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(package_manager=self)
