from PySide6.QtCore import QSortFilterProxyModel
from PySide6.QtWidgets import QWidget, QDialog, QTreeWidgetItem
from archcentral.helpers.custom_classes import PacmanPkgInfo
from archcentral.helpers.unitconverter import unit_converter
from archcentral.ui.designer.packagemanager import Ui_PackageManager
from archcentral.models.pacman_update_list import PacmanUpdateTableModel
from archcentral.models.pacman_package_list import PacmanPackageListTableModel
from archcentral.ui.views.pacman_update_dialog import PacmanUpdateDialog
from archcentral.controllers.packagemanager_controller import PackageManagerController
#from datetime import datetime

class PackageManagerModule(QWidget, Ui_PackageManager):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(PackageManager=self)

        # Hook up model to the update table view to initialize it
        self.update_list_model: PacmanUpdateTableModel = PacmanUpdateTableModel([])
        self.update_list_proxy_model: QSortFilterProxyModel = QSortFilterProxyModel()
        self.update_list_proxy_model.setSourceModel(self.update_list_model)
        self.update_table.setModel(self.update_list_proxy_model)

        self.pmc: PackageManagerController = PackageManagerController()
        self.pmc.update_fetched.connect(self.update_list_model.refresh)
        self.pmc.update_fetched.connect(self.are_there_updates)
        self.pmc.update_stdout_stream.connect(self.pacman_output.appendPlainText)

        # Call the update fetcher method of pmc
        self.fetch_update_button.clicked.connect(self.pmc.fetch_updates)
        self.fetch_update_button.clicked.connect(lambda: self.pacman_output.setPlainText(""))

        # Update the packages listed in the update table view
        self.update_button.clicked.connect(self.update_packages)

        # Set up the table view in the instalL/manage section
        self.package_list_model: PacmanPackageListTableModel = PacmanPackageListTableModel(self.pmc.list_all_packages())
        self.package_list_proxy_model: QSortFilterProxyModel = QSortFilterProxyModel()
        self.package_list_proxy_model.setDynamicSortFilter(True)
        self.package_list_proxy_model.setSourceModel(self.package_list_model)
        self.package_list_proxy_model.setFilterKeyColumn(2)
        self.package_list_table.setModel(self.package_list_proxy_model)
        # Connects the search bar and buttons to filter view results
        self.package_search_button.pressed.connect(lambda: self.package_list_proxy_model.setFilterRegularExpression(self.package_search.text()))
        self.package_search.returnPressed.connect(lambda: self.package_list_proxy_model.setFilterRegularExpression(self.package_search.text()))

        # Connect pacman output to the appropriate textbox
        self.pmc.transaction_stdout_stream.connect(self.pacman_output_tr.appendPlainText)

        # Run package transaction and refresh the package model upon transaction completion
        self.pmc.transaction_finished.connect(lambda: self.package_list_model.refresh(self.pmc.list_all_packages()))
        self.run_transaction_button.pressed.connect(lambda: self.pmc.run_package_transaction(self.package_list_model.get_marked_packages()))

        self.pmc.pacman_lock_activated.connect(lambda: print("Pacman locked."))

        #self.fill_package_details()
        self.package_list_table.clicked.connect(self.fill_package_details)

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
            self.pmc.update_finished.connect(lambda: self.package_list_model.refresh(self.pmc.list_all_packages()))
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
        self.package_details_tree.clear()
        selected_pkg: PacmanPkgInfo = self.package_list_model.get_package(self.package_list_table.currentIndex())

        self.package_details_tree.addTopLevelItem(QTreeWidgetItem(["Name: ", selected_pkg.name]))

        self.package_details_tree.addTopLevelItem(QTreeWidgetItem(["Upstream URL: ", selected_pkg.url]))

        if selected_pkg.licenses:
            licenses_item = QTreeWidgetItem(["Licenses:"])
            for license in selected_pkg.licenses:
                licenses_item.addChild(QTreeWidgetItem([license]))
        else:
            licenses_item = QTreeWidgetItem(["Licenses:", "None"])
        self.package_details_tree.addTopLevelItem(licenses_item)

        download_size, unit = unit_converter(selected_pkg.size)
        self.package_details_tree.addTopLevelItem(QTreeWidgetItem(["Download size: ", f"{download_size} {unit}"]))

        if selected_pkg.depends:
            deps_item = QTreeWidgetItem(["Dependencies:"])
            for dep in selected_pkg.depends:
                deps_item.addChild(QTreeWidgetItem([dep]))
        else:
            deps_item = QTreeWidgetItem(["Dependencies:", "None"])
        self.package_details_tree.addTopLevelItem(deps_item)
