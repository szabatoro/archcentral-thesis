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
        self.pmc.update_fetched.connect(self.fill_update_table)
        self.pmc.update_fetched.connect(self.are_there_updates)
        self.pmc.update_stdout_stream.connect(self.pacman_output.appendPlainText)

        # Hook up model to the update table view to initialize it
        self.update_table.model = PacmanUpdateTableModel([])
        self.update_table.setModel(self.update_table.model)

        # Set up the table view in the instalL/manage section
        self.package_list_table.model = PacmanPackageListTableModel([])
        self.package_list_table.setModel(self.package_list_table.model)
        self.fill_package_table(self.pmc.list_all_packages())
        self.package_search.textChanged.connect(self.package_table_search)

        # Refresh model data with output of pacman -Qu, blank out previous pacman output
        self.fetch_update_button.clicked.connect(self.pmc.fetch_updates)
        self.fetch_update_button.clicked.connect(lambda: self.pacman_output.setPlainText(""))

        # Update the packages listed in the update table view
        self.update_button.clicked.connect(self.update_packages)

    def fill_update_table(self, updates) -> None:
        """Initializes the update table widget with the latest model data."""
        self.update_table.model = PacmanUpdateTableModel(updates)
        self.update_table.setModel(self.update_table.model)

    def fill_package_table(self, packagelist) -> None:
        """Initializes the package table widget with the latest model data."""
        self.package_list_table.model = PacmanPackageListTableModel(packagelist)
        self.package_list_table.setModel(self.package_list_table.model)

    def package_table_search(self, search_text) -> None:
        """Takes a string and filters data in the package list model with it."""
        proxyModel = QSortFilterProxyModel(self)
        proxyModel.setSourceModel(self.package_list_table.model)

    def are_there_updates(self) -> None:
        """Checks if there are updates available and sets the state of the update button accordingly."""
        if not self.update_table.model.get_packagenames():
            self.update_button.setText("Up to date")
            self.update_button.setEnabled(False)
        else:
            self.update_button.setText("Update")
            self.update_button.setEnabled(True)

    def update_packages(self) -> None:
        """Initiates the package update process depending on the dialog box return value."""
        if self.open_update_confirm_dialog():
            self.pmc.perform_update(self.update_table.model.get_packagenames())

    def open_update_confirm_dialog(self) -> bool:
        """Opens dialog box for update confirmation. Returns a boolean value depending on if the dialog is accepted or not."""
        dialog: PacmanUpdateDialog = PacmanUpdateDialog(self.update_table.model.get_total_size())
        result = dialog.exec()
        if result == QDialog.Accepted:
            return True
        elif result == QDialog.Rejected:
            return False
