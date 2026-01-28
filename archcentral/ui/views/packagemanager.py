from PySide6.QtCore import QSortFilterProxyModel
from PySide6.QtWidgets import QWidget, QDialog
from archcentral.ui.designer.packagemanager import Ui_PackageManager
from archcentral.models.pacman_update_list import PacmanUpdateTableModel
from archcentral.models.pacman_package_list import PacmanPackageListTableModel
from archcentral.ui.views.pacman_update_dialog import PacmanUpdateDialog
from archcentral.controllers.packagemanager_controller import PackageManagerController

# package manager module placeholder
class PackageManagerModule(QWidget, Ui_PackageManager):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(PackageManager=self)

        self.pmc: PackageManagerController = PackageManagerController()
        self.pmc.update_fetched.connect(self.refresh_update_model)
        self.pmc.update_fetched.connect(self.are_there_updates)
        self.pmc.update_stdout_stream.connect(self.pacman_output.appendPlainText)

        # Hook up model to the update table view to initialize it
        self.update_list_model: PacmanUpdateTableModel = PacmanUpdateTableModel([])
        self.update_list_proxy_model: QSortFilterProxyModel = QSortFilterProxyModel()
        self.update_list_proxy_model.setSourceModel(self.update_list_model)
        self.update_table.setModel(self.update_list_proxy_model)

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
        self.package_search_button.pressed.connect(lambda: self.package_list_proxy_model.setFilterRegularExpression(self.package_search.text()))
        self.package_search.returnPressed.connect(lambda: self.package_list_proxy_model.setFilterRegularExpression(self.package_search.text()))

        self.pmc.transaction_stdout_stream.connect(self.pacman_output_tr.appendPlainText)
        self.pmc.transaction_finished.connect(lambda: self.package_list_proxy_model.setFilterRegularExpression(""))

        self.run_transaction_button.pressed.connect(lambda: self.pmc.run_package_transaction(self.package_list_model.get_marked_packages()))

    def refresh_update_model(self, updates) -> None:
        """Fills the update model with updateable packages."""
        self.update_list_model = PacmanUpdateTableModel(updates)
        self.update_list_proxy_model.setSourceModel(self.update_list_model)

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
