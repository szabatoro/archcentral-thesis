from PySide6.QtWidgets import QWidget
from archcentral.ui.designer.servicemanager import Ui_ServiceManager

class ServiceManagerModule(QWidget, Ui_ServiceManager):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(ServiceManager=self)
