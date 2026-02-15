from PySide6.QtCore import QSortFilterProxyModel, QModelIndex, QThread, Signal
from PySide6.QtWidgets import QWidget, QDialog, QTreeWidgetItem
from archcentral.helpers.custom_classes import PacmanPkgInfo
from archcentral.helpers.unitconverter import unit_converter
from archcentral.ui.designer.packagemanager import Ui_PackageManager
from archcentral.models.pacman_update_list import PacmanUpdateTableModel
from archcentral.models.pacman_package_list import PacmanPackageListTableModel
from archcentral.ui.views.pacman_update_dialog import PacmanUpdateDialog
from archcentral.controllers.packagemanager_controller import PackageManagerController
from datetime import datetime

class PackageManagerModule(QWidget, Ui_PackageManager):
    # signals
    fetch_package_list_signal: Signal = Signal()
    refresh_package_list_signal: Signal = Signal()
    initiate_update_signal: Signal = Signal()
    initiate_package_transaction_signal: Signal = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(PackageManager=self)

        # Instantiate the package manager controller and move it to its own thread
        self.pmc_thread: QThread = QThread()
        self.pmc: PackageManagerController = PackageManagerController()
        self.pmc.moveToThread(self.pmc_thread)
        self.pmc_thread.start()

        # Connecting module signals to pmc
        self.fetch_package_list_signal.connect(lambda: self.pmc.list_all_packages(False))
        self.initiate_update_signal.connect(self.pmc.fetch_updates)
        self.refresh_package_list_signal.connect(lambda: self.pmc.list_all_packages(True))
        self.initiate_package_transaction_signal.connect(lambda: self.pmc.run_package_transaction(self.package_list_model.get_marked_packages()))

        # Hook up model to the update table view to initialize it
        self.update_list_model: PacmanUpdateTableModel = PacmanUpdateTableModel([])
        self.update_list_proxy_model: QSortFilterProxyModel = QSortFilterProxyModel()
        self.update_list_proxy_model.setSourceModel(self.update_list_model)
        self.update_table.setModel(self.update_list_proxy_model)

        self.pmc.update_fetched.connect(self.update_list_model.refresh)
        self.pmc.update_finished.connect(self.fetch_package_list_signal.emit)
        self.pmc.update_fetched.connect(self.are_there_updates)
        self.pmc.update_stdout_stream.connect(self.pacman_output.appendPlainText)

        # Call the update fetcher method of pmc
        self.fetch_update_button.clicked.connect(self.on_update_button_clicked)

        # Update the packages stored in the update table model
        self.update_button.clicked.connect(self.update_packages)

        # Set up the table view in the instalL/manage section
        self.package_list_model: PacmanPackageListTableModel = None
        self.package_list_proxy_model: QSortFilterProxyModel = None
        self.pmc.package_list_fetched_for_init.connect(self.initialize_package_list)
        self.fetch_package_list_signal.emit()
        self.pmc.package_list_fetched_for_refresh.connect(self.refresh_package_list)

        # Connects the search bar and buttons to filter view results
        self.package_search_button.pressed.connect(lambda: self.package_list_proxy_model.setFilterRegularExpression(self.package_search.text()))
        self.package_search.returnPressed.connect(lambda: self.package_list_proxy_model.setFilterRegularExpression(self.package_search.text()))

        # Connect pacman output to the appropriate textbox
        self.pmc.transaction_stdout_stream.connect(self.pacman_output_tr.appendPlainText)

        # Run package transaction and refresh the package model upon transaction completion
        self.pmc.transaction_started.connect(lambda: self.package_det_out_tabs.setCurrentIndex(1))
        self.pmc.transaction_finished.connect(self.refresh_package_list_signal.emit)
        self.run_transaction_button.pressed.connect(self.initiate_package_transaction_signal.emit)

        # Connecting action buttons status and status message label to pacman lock state
        self.pmc.pacman_lock_activated.connect(self.on_pacman_lock_activated)
        self.pmc.pacman_lock_deactivated.connect(self.on_pacman_lock_deactivated)

    def initialize_package_list(self, packages) -> None:
        self.package_list_model: PacmanPackageListTableModel = PacmanPackageListTableModel(packages)
        self.package_list_proxy_model: QSortFilterProxyModel = QSortFilterProxyModel()
        self.package_list_proxy_model.setDynamicSortFilter(True)
        self.package_list_proxy_model.setSourceModel(self.package_list_model)
        self.package_list_proxy_model.setFilterKeyColumn(2)
        self.package_list_table.setModel(self.package_list_proxy_model)
        # Populate the package details widget with the selected package's information
        self.package_list_table.selectionModel().currentRowChanged.connect(self.fill_package_details)

    def refresh_package_list(self, packages) -> None:
        self.package_list_model.refresh(packages)

    def on_pacman_lock_activated(self) -> None:
        self.status_label.setText("Operation in progress, please wait...")
        self.run_transaction_button.setEnabled(False)
        self.fetch_update_button.setEnabled(False)
        self.update_button.setEnabled(False)

    def on_pacman_lock_deactivated(self) -> None:
        self.status_label.setText("Operation finished...")
        self.run_transaction_button.setEnabled(True)
        self.fetch_update_button.setEnabled(True)
        self.are_there_updates()

    def on_update_button_clicked(self) -> None:
        self.initiate_update_signal.emit()
        self.pacman_output.setPlainText("")

    def are_there_updates(self) -> None:
        """Checks if there are updates available and sets the state of the update button accordingly."""
        if not self.update_list_model.get_packagenames():
            self.update_button.setText("Up to date")
            self.update_button.setEnabled(False)
        else:
            self.update_button.setText("Update")
            self.update_button.setEnabled(True)

    def update_packages(self) -> None:
        """Initiates the package update process depending on the dialog box return value."""
        if self.open_update_confirm_dialog():
            self.pmc.perform_update(self.update_list_model.get_packagenames())

    def open_update_confirm_dialog(self) -> bool:
        """Opens dialog box for update confirmation. Returns a boolean value depending on if the dialog is accepted or not."""
        dialog: PacmanUpdateDialog = PacmanUpdateDialog(self.update_list_model.get_total_size())
        result = dialog.exec()
        if result == QDialog.Accepted:
            return True
        elif result == QDialog.Rejected:
            return False

    def fill_package_details(self) -> None:
        """Fills out the package details tab with information about the selected package."""
        self.package_details_tree.clear()

        source_index: QModelIndex = self.package_list_proxy_model.mapToSource(self.package_list_table.currentIndex())
        selected_pkg: PacmanPkgInfo = self.package_list_model.get_package(source_index)

        self.package_details_tree.addTopLevelItem(QTreeWidgetItem(["Name: ", selected_pkg.name]))

        self.package_details_tree.addTopLevelItem(QTreeWidgetItem(["Description: ", selected_pkg.desc]))

        self.package_details_tree.addTopLevelItem(QTreeWidgetItem(["Upstream URL: ", selected_pkg.url]))

        if selected_pkg.licenses:
            licenses_item: QTreeWidgetItem = QTreeWidgetItem(["Licenses:"])
            for license in selected_pkg.licenses:
                licenses_item.addChild(QTreeWidgetItem([license]))
        else:
            licenses_item: QTreeWidgetItem = QTreeWidgetItem(["Licenses:", "None"])
        self.package_details_tree.addTopLevelItem(licenses_item)

        if selected_pkg.size > 0:
            download_size, unit = unit_converter(selected_pkg.size)
            self.package_details_tree.addTopLevelItem(QTreeWidgetItem(
                ["Download size: ", f"{download_size:.2f} {unit}"])
            )

        if selected_pkg.depends:
            deps_item: QTreeWidgetItem = QTreeWidgetItem(["Dependencies:"])
            for dep in selected_pkg.depends:
                deps_item.addChild(QTreeWidgetItem([dep]))
        else:
            deps_item: QTreeWidgetItem = QTreeWidgetItem(["Dependencies:", "None"])
        self.package_details_tree.addTopLevelItem(deps_item)

        if selected_pkg.optdepends:
            optdepends_item: QTreeWidgetItem = QTreeWidgetItem(["Optional dependencies:"])
            for optdepend in selected_pkg.optdepends:
                optdepends_item.addChild(QTreeWidgetItem([optdepend]))
        else:
            optdepends_item: QTreeWidgetItem = QTreeWidgetItem(["Optional dependencies:", "None"])
        self.package_details_tree.addTopLevelItem(optdepends_item)

        builddate_str: str = datetime.fromtimestamp(selected_pkg.builddate).strftime("%Y-%m-%d %H:%M:%S")
        self.package_details_tree.addTopLevelItem(QTreeWidgetItem(["Build date: ", builddate_str]))

        if selected_pkg.groups:
            groups_item: QTreeWidgetItem = QTreeWidgetItem(["Groups:"])
            for group in selected_pkg.groups:
                groups_item.addChild(QTreeWidgetItem([group]))
        else:
            groups_item: QTreeWidgetItem = QTreeWidgetItem(["Groups:", "None"])
        self.package_details_tree.addTopLevelItem(groups_item)

    def cleanup_thread(self) -> None:
        """Gracefully stops threads."""
        if self.pmc_thread.isRunning():
            self.pmc_thread.quit()
            self.pmc_thread.wait()
