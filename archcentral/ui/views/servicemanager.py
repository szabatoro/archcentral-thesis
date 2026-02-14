from PySide6.QtCore import QSortFilterProxyModel, QThread, Signal
from PySide6.QtWidgets import QWidget
from archcentral.ui.designer.servicemanager import Ui_ServiceManager
from archcentral.controllers.servicemanager_controller import ServiceManagerController
from archcentral.models.systemd_units_list import SystemdServiceListModel

class ServiceManagerModule(QWidget, Ui_ServiceManager):
    fetch_systemd_units_signal: Signal = Signal()
    systemctl_operation_signal: Signal = Signal(str,bool)

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(ServiceManager=self)

        self.destroyed.connect(self.cleanup_thread)

        self.thread = QThread()

        self.smc: ServiceManagerController = ServiceManagerController()
        self.smc.moveToThread(self.thread)

        self.thread.start()

        self.smc.services_fetched.connect(self.initalize_service_model)
        self.fetch_systemd_units_signal.connect(self.smc.list_services)
        self.fetch_systemd_units_signal.emit()

        self.systemctl_operation_signal.connect(self.smc.call_systemctl)

    def initalize_service_model(self, services: list):
        """Initializes the systemd service model with services from the systemd dbus API and populates the service table."""
        self.service_list_model: SystemdServiceListModel = SystemdServiceListModel(services)
        self.service_list_proxy_model: QSortFilterProxyModel = QSortFilterProxyModel()
        self.service_list_proxy_model.setDynamicSortFilter(True)
        self.service_list_proxy_model.setSourceModel(self.service_list_model)
        self.service_list_proxy_model.setFilterKeyColumn(2)
        self.service_list_table.setModel(self.service_list_proxy_model)

    def cleanup_thread(self):
        """Gracefully stops threads."""
        if self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()
