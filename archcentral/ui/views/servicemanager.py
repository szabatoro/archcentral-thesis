from PySide6.QtCore import QModelIndex, QSortFilterProxyModel, QThread, Signal, Qt
from PySide6.QtWidgets import QWidget
from pyqtgraph.Qt.QtWidgets import QTreeWidgetItem
from archcentral.helpers.custom_classes import SystemdServiceInfo
from archcentral.ui.designer.servicemanager import Ui_ServiceManager
from archcentral.controllers.servicemanager_controller import ServiceManagerController
from archcentral.models.systemd_services_list import SystemdServiceListModel

class ServiceManagerModule(QWidget, Ui_ServiceManager):
    fetch_systemd_units_signal: Signal = Signal()
    systemctl_operation_signal: Signal = Signal(str,str)

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(ServiceManager=self)

        self.destroyed.connect(self.cleanup_thread)

        self.thread = QThread()

        self.smc: ServiceManagerController = ServiceManagerController()
        self.smc.moveToThread(self.thread)

        self.thread.start()

        # Searching services
        self.service_search_button.pressed.connect(lambda: self.system_service_list_proxy_model.setFilterRegularExpression(self.service_search.text()))
        self.service_search.returnPressed.connect(lambda: self.system_service_list_proxy_model.setFilterRegularExpression(self.service_search.text()))

        self.smc.services_fetched_for_init.connect(self.initalize_system_service_model)
        self.smc.services_fetched_for_refresh.connect(self.refresh_service_list)

        self.fetch_systemd_units_signal.connect(self.smc.list_system_services_for_init)
        self.fetch_systemd_units_signal.emit()

        self.systemctl_operation_signal.connect(self.smc.call_systemctl)

        self.start_stop_button.clicked.connect(self.start_stop_service)
        self.enable_disable_button.clicked.connect(self.enable_disable_service)

    def _get_selected_row(self) -> None:
        """Fetches the systemdserviceinfo object stored in the selected row."""
        source_index: QModelIndex = self.system_service_list_proxy_model.mapToSource(self.system_service_list_table.currentIndex())
        selected_service: SystemdServiceInfo = self.system_service_list_model.get_unit(source_index)

        return selected_service

    def _adapt_buttons_status(self) -> None:
        """Changes the service buttons names depending on selected service status."""
        selected_service: SystemdServiceInfo = self._get_selected_row()

        if selected_service.substate == "running":
            self.start_stop_button.setText("Stop")
        else:
            self.start_stop_button.setText("Start")

        if selected_service.enabledstate == "enabled":
            self.enable_disable_button.setText("Disable")
        else:
            self.enable_disable_button.setText("Enable")

    def initalize_system_service_model(self, is_system: bool, services: list) -> None:
        """Initializes the systemd service model with services from the systemd dbus API and populates the service table."""
        if is_system:
            self.system_service_list_model: SystemdServiceListModel = SystemdServiceListModel(services)
            self.system_service_list_proxy_model: QSortFilterProxyModel = QSortFilterProxyModel()
            self.system_service_list_proxy_model.setDynamicSortFilter(True)
            self.system_service_list_proxy_model.sort(0, Qt.AscendingOrder)
            self.system_service_list_proxy_model.setSourceModel(self.system_service_list_model)
            self.system_service_list_proxy_model.setFilterKeyColumn(0)
            self.system_service_list_table.setModel(self.system_service_list_proxy_model)
            self.system_service_list_table.selectionModel().currentRowChanged.connect(self.fill_service_details)
            self.system_service_list_table.selectionModel().currentRowChanged.connect(self._adapt_buttons_status)
        else:
            self.user_service_list_model: SystemdServiceListModel = SystemdServiceListModel(services)
            self.user_service_list_proxy_model: QSortFilterProxyModel = QSortFilterProxyModel()
            self.user_service_list_proxy_model.setDynamicSortFilter(True)
            self.user_service_list_proxy_model.sort(0, Qt.AscendingOrder)
            self.user_service_list_proxy_model.setSourceModel(self.user_service_list_model)
            self.user_service_list_proxy_model.setFilterKeyColumn(0)
            self.user_service_list_table.setModel(self.user_service_list_proxy_model)
            self.user_service_list_table.selectionModel().currentRowChanged.connect(self.fill_service_details)
            self.user_service_list_table.selectionModel().currentRowChanged.connect(self._adapt_buttons_status)



    def refresh_service_list(self, is_system: bool, services: list) -> None:
        """Refreshes the service list model."""
        self.system_service_list_model.refresh(services) if is_system else self.user_service_list_model.refresh(services)


    def fill_service_details(self) -> None:
        """Fills out the service details tab with information about the selected service."""
        self.service_details_tree.clear()

        selected_service: SystemdServiceInfo = self._get_selected_row()

        self.service_details_tree.addTopLevelItem(QTreeWidgetItem(["Name: ", selected_service.unitname]))

        self.service_details_tree.addTopLevelItem(QTreeWidgetItem(["Description: ", selected_service.desc]))

    def start_stop_service(self) -> None:
        """Stops or starts the selected service depending on its substate."""
        selected_service: SystemdServiceInfo = self._get_selected_row()
        if selected_service.substate == "running":
            operation = "stop"
        else:
            operation = "start"
        self.systemctl_operation_signal.emit(selected_service.unitname, operation)

    def enable_disable_service(self) -> None:
        """Enables or disables the selected service depending on its enabledstate."""
        selected_service: SystemdServiceInfo = self._get_selected_row()
        if selected_service.enabledstate == "enabled":
            operation = "disable"
        else:
            operation = "enable"
        self.systemctl_operation_signal.emit(selected_service.unitname, operation)

    def cleanup_thread(self) -> None:
        """Gracefully stops threads."""
        if self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()
