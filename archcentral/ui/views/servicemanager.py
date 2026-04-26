from datetime import datetime
from typing import Literal
from PySide6.QtCore import QModelIndex, QSortFilterProxyModel, QThread, Signal, Qt
from PySide6.QtWidgets import QWidget
from pyqtgraph.Qt.QtWidgets import QTreeWidgetItem
from archcentral.ui.designer.servicemanager import Ui_ServiceManager
from archcentral.controllers.servicemanager_controller import ServiceManagerController
from archcentral.models.systemd_units_list import SystemdUnitListModel

class ServiceManagerModule(QWidget, Ui_ServiceManager):
    fetch_systemd_units_signal: Signal = Signal(bool, bool, str)
    systemctl_operation_signal: Signal = Signal(bool, str, str, str)

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(ServiceManager=self)

        self.destroyed.connect(self.cleanup_thread)

        self.smc_thread = QThread()

        self.smc: ServiceManagerController = ServiceManagerController()
        self.smc.moveToThread(self.smc_thread)

        self.smc_thread.start()

        self.unit_types_box.addItems(["Services", "Timers", "Sockets"])

        # Searching services
        self.unit_search_button.pressed.connect(lambda: self.system_unit_list_proxy_model.setFilterRegularExpression(self.service_search.text()))
        self.unit_search.returnPressed.connect(lambda: self.system_unit_list_proxy_model.setFilterRegularExpression(self.service_search.text()))

        self.smc.services_fetched_for_init.connect(self.initalize_models)
        self.smc.services_fetched_for_refresh.connect(self.refresh_unit_list)
        self.smc.timers_fetched_for_init.connect(self.initalize_models)
        self.smc.timers_fetched_for_refresh.connect(self.refresh_unit_list)
        self.smc.sockets_fetched_for_init.connect(self.initalize_models)
        self.smc.sockets_fetched_for_refresh.connect(self.refresh_unit_list)

        self.smc.systemctl_lock_activated.connect(self.interface_lock)
        self.smc.systemctl_lock_deactivated.connect(self.interface_unlock)

        self.fetch_systemd_units_signal.connect(self.smc.list_units)
        self.fetch_systemd_units_signal.emit(False, True, "service")
        self.fetch_systemd_units_signal.emit(False, False, "service")

        self.unit_types_box.textActivated.connect(self.handle_unit_type_selection)

        self.systemctl_operation_signal.connect(self.smc.call_systemctl)

        self.start_stop_button.clicked.connect(self.start_stop_unit)
        self.enable_disable_button.clicked.connect(self.enable_disable_unit)
        self.restart_button.clicked.connect(self.restart_unit)

    def _get_selected_row(self):
        """Fetches the SystemdBaseInfo object stored in the selected row."""
        match self.user_system_tab.currentIndex():
            case 0:
                source_index: QModelIndex = self.system_unit_list_proxy_model.mapToSource(self.system_unit_list_table.currentIndex())
                selected_unit = self.system_unit_list_model.get_unit(source_index)
                is_user_unit = False
            case 1:
                source_index: QModelIndex = self.user_unit_list_proxy_model.mapToSource(self.user_unit_list_table.currentIndex())
                selected_unit = self.user_unit_list_model.get_unit(source_index)
                is_user_unit = True

        return selected_unit, is_user_unit

    def _adapt_buttons_status(self) -> None:
        """Changes the service buttons names depending on selected service status."""
        selected_unit, _ = self._get_selected_row()

        if selected_unit.activestate == "active":
            self.start_stop_button.setText("Stop")
            self.restart_button.setEnabled(True)
        else:
            self.start_stop_button.setText("Start")
            self.restart_button.setEnabled(False)

        if selected_unit.enabledstate == "enabled":
            self.enable_disable_button.setText("Disable")
        else:
            self.enable_disable_button.setText("Enable")

    def interface_lock(self) -> None:
        """Locks the interface when a systemctl operation starts."""
        self.status_label.setText("Operation in progress, please wait...")
        self.enable_disable_button.setEnabled(False)
        self.restart_button.setEnabled(False)
        self.start_stop_button.setEnabled(False)
        self.unit_types_box.setEnabled(False)

    def interface_unlock(self) -> None:
        """Unlocks the interface after a systemctl operation finishes."""
        self.status_label.setText("Operation finished...")
        self.enable_disable_button.setEnabled(True)
        self.restart_button.setEnabled(True)
        self.start_stop_button.setEnabled(True)
        self.unit_types_box.setEnabled(True)

    def handle_unit_type_selection(self, unit_type: Literal["Services", "Timers", "Sockets"]) -> None:
        """Fetches list of units of the type selected in the type selector."""
        match unit_type:
            case "Services":
                self.fetch_systemd_units_signal.emit(True, True, "service")
                self.fetch_systemd_units_signal.emit(True, False, "service")
            case "Timers":
                self.fetch_systemd_units_signal.emit(True, True, "timer")
                self.fetch_systemd_units_signal.emit(True, False, "timer")
            case "Sockets":
                self.fetch_systemd_units_signal.emit(True, True, "socket")
                self.fetch_systemd_units_signal.emit(True, False, "socket")

    def initalize_models(self, is_user: bool, units: list) -> None:
        """Initializes the user and system unit models with services from the systemd dbus API and populates their tables."""

        if is_user:
            self.user_unit_list_model: SystemdUnitListModel = SystemdUnitListModel(units)
            self.user_unit_list_proxy_model: QSortFilterProxyModel = QSortFilterProxyModel()
            self.user_unit_list_proxy_model.setDynamicSortFilter(True)
            self.user_unit_list_proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            self.user_unit_list_proxy_model.setSortCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            self.user_unit_list_proxy_model.sort(0, Qt.AscendingOrder)
            self.user_unit_list_proxy_model.setSourceModel(self.user_unit_list_model)
            self.user_unit_list_proxy_model.setFilterKeyColumn(0)

            self.user_unit_list_table.setModel(self.user_unit_list_proxy_model)
            self.user_unit_list_table.selectionModel().currentRowChanged.connect(self.fill_unit_details)
            self.user_unit_list_table.selectionModel().currentRowChanged.connect(self._adapt_buttons_status)
        else:
            self.system_unit_list_model: SystemdUnitListModel = SystemdUnitListModel(units)
            self.system_unit_list_proxy_model: QSortFilterProxyModel = QSortFilterProxyModel()
            self.system_unit_list_proxy_model.setDynamicSortFilter(True)
            self.system_unit_list_proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            self.system_unit_list_proxy_model.setSortCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            self.system_unit_list_proxy_model.sort(0, Qt.AscendingOrder)
            self.system_unit_list_proxy_model.setSourceModel(self.system_unit_list_model)
            self.system_unit_list_proxy_model.setFilterKeyColumn(0)

            self.system_unit_list_table.setModel(self.system_unit_list_proxy_model)
            self.system_unit_list_table.selectionModel().currentRowChanged.connect(self.fill_unit_details)
            self.system_unit_list_table.selectionModel().currentRowChanged.connect(self._adapt_buttons_status)

    def refresh_unit_list(self, is_user: bool, services: list) -> None:
        """Refreshes the service list model."""
        self.user_unit_list_model.refresh(services) if is_user else self.system_unit_list_model.refresh(services)

    def fill_unit_details(self) -> None:
        """Fills out the service details tab with information about the selected service."""
        self.unit_details_tree.clear()

        selected_unit, _ = self._get_selected_row()

        self.unit_details_tree.addTopLevelItem(QTreeWidgetItem(["Name: ", selected_unit.unitname]))

        self.unit_details_tree.addTopLevelItem(QTreeWidgetItem(["Description: ", selected_unit.desc]))

        if selected_unit.type == "service":
            self.unit_details_tree.addTopLevelItem(QTreeWidgetItem(["Executable: ", selected_unit.exec_start]))
            self.unit_details_tree.addTopLevelItem(QTreeWidgetItem(["Result: ", selected_unit.result]))

            if selected_unit.substate == "running":
                self.unit_details_tree.addTopLevelItem(QTreeWidgetItem(["Used memory: ", selected_unit.memory]))
                self.unit_details_tree.addTopLevelItem(QTreeWidgetItem(["CGroup: ", selected_unit.cgroup]))

        if selected_unit.type == "timer":
            if selected_unit.substate == "waiting":
                next_trigger = datetime.fromtimestamp(selected_unit.next_trigger/1000000).strftime('%Y-%m-%d %H:%M:%S')
                self.unit_details_tree.addTopLevelItem(QTreeWidgetItem(["Next Trigger: ", next_trigger]))

        if selected_unit.type == "socket":
            self.unit_details_tree.addTopLevelItem(QTreeWidgetItem(["Listen address: ", selected_unit.listen_address]))

    def start_stop_unit(self) -> None:
        """Stops or starts the selected service depending on its substate."""
        selected_unit, is_user_unit = self._get_selected_row()
        if selected_unit.activestate == "active":
            operation = "stop"
        else:
            operation = "start"
        self.systemctl_operation_signal.emit(is_user_unit, selected_unit.unitname, operation, selected_unit.type)

    def enable_disable_unit(self) -> None:
        """Enables or disables the selected service depending on its enabledstate."""
        selected_unit, is_user_unit = self._get_selected_row()
        if selected_unit.enabledstate == "enabled":
            operation = "disable"
        else:
            operation = "enable"
        self.systemctl_operation_signal.emit(is_user_unit, selected_unit.unitname, operation, selected_unit.type)

    def restart_unit(self) -> None:
        """Restarts the selected service."""
        selected_unit, is_user_unit = self._get_selected_row()
        self.systemctl_operation_signal.emit(is_user_unit, selected_unit.unitname, "restart", selected_unit.type)

    def cleanup_thread(self) -> None:
        """Gracefully stops threads."""
        if self.smc_thread.isRunning():
            self.smc_thread.quit()
            self.smc_thread.wait()
