from PySide6.QtWidgets import QWidget
from archcentral.ui.designer.sysinfo import Ui_SysInfo

# system information module placeholder
class SysInfoModule(QWidget, Ui_SysInfo):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(SysInfo=self)
