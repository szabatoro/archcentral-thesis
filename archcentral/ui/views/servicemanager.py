from PySide6.QtCore import QModelIndex, QSortFilterProxyModel, QThread, Signal
from PySide6.QtWidgets import QWidget
from pyqtgraph.Qt.QtWidgets import QTreeWidgetItem
from archcentral.helpers.custom_classes import SystemdServiceInfo
from archcentral.ui.designer.servicemanager import Ui_ServiceManager
from archcentral.controllers.servicemanager_controller import ServiceManagerController
from archcentral.models.systemd_services_list import SystemdServiceListModel

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

        # Searching services
        self.service_search_button.pressed.connect(lambda: self.service_list_proxy_model.setFilterRegularExpression(self.service_search.text()))
        self.service_search.returnPressed.connect(lambda: self.service_list_proxy_model.setFilterRegularExpression(self.service_search.text()))

        self.smc.services_fetched.connect(self.initalize_service_model)
        self.fetch_systemd_units_signal.connect(self.smc.list_services)
        self.fetch_systemd_units_signal.emit()

        self.systemctl_operation_signal.connect(self.smc.call_systemctl)

    def initalize_service_model(self, services: list) -> None:
        """Initializes the systemd service model with services from the systemd dbus API and populates the service table."""
        self.service_list_model: SystemdServiceListModel = SystemdServiceListModel(services)
        self.service_list_proxy_model: QSortFilterProxyModel = QSortFilterProxyModel()
        self.service_list_proxy_model.setDynamicSortFilter(True)
        self.service_list_proxy_model.setSourceModel(self.service_list_model)
        self.service_list_proxy_model.setFilterKeyColumn(0)
        self.service_list_table.setModel(self.service_list_proxy_model)
        self.service_list_table.selectionModel().currentRowChanged.connect(self.fill_service_details)

    def fill_service_details(self) -> None:
        """Fills out the service details tab with information about the selected service."""
        self.service_details_tree.clear()

        source_index: QModelIndex = self.service_list_proxy_model.mapToSource(self.service_list_table.currentIndex())
        selected_service: SystemdServiceInfo = self.service_list_model.get_unit(source_index)

        self.service_details_tree.addTopLevelItem(QTreeWidgetItem(["Name: ", selected_service.unitname]))

        self.service_details_tree.addTopLevelItem(QTreeWidgetItem(["Description: ", selected_service.desc]))

    def cleanup_thread(self) -> None:
        """Gracefully stops threads."""
        if self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()
