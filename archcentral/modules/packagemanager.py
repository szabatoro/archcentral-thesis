from PySide6.QtWidgets import QWidget
from archcentral.ui.designer.packagemanager import Ui_PackageManager

# package manager module placeholder
class PackageManagerModule(QWidget, Ui_PackageManager):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(PackageManager=self)
