from PySide6.QtWidgets import QWidget
from archcentral.ui.designer.servicemanager import Ui_ServiceManager
from archcentral.controllers.servicemanager_controller import ServiceManagerController

class ServiceManagerModule(QWidget, Ui_ServiceManager):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(ServiceManager=self)

        self.smc: ServiceManagerController = ServiceManagerController()
