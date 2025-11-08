from PySide6.QtWidgets import QWidget
from archcentral.ui.designer.sysinfo import Ui_sys_info

# system information module placeholder
class sys_info(QWidget, Ui_sys_info):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(sys_info=self)
