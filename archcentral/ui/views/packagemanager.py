from PySide6.QtWidgets import QWidget, QDialog
from archcentral.ui.designer.packagemanager import Ui_PackageManager
from archcentral.models.pacman_update_list import PacmanUpdateTableModel
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

        # Refresh model data with output of pacman -Qu, blank out previous pacman output
        self.fetch_update_button.clicked.connect(self.pmc.fetch_updates)
        self.fetch_update_button.clicked.connect(lambda: self.pacman_output.setPlainText(""))

        # Update the packages listed in the update table view
        self.update_button.clicked.connect(self.update_packages)

    # Hook up model with fresh data to the update table view
    def fill_update_table(self, updates) -> None:
        self.update_table.model = PacmanUpdateTableModel(updates)
        self.update_table.setModel(self.update_table.model)

    # Gray out update button if there are no packages to update
    def are_there_updates(self) -> None:
        if not self.update_table.model.get_packagenames():
            self.update_button.setText("Up to date")
            self.update_button.setEnabled(False)
        else:
            self.update_button.setText("Update")
            self.update_button.setEnabled(True)

    # Set up pacman worker for performing updates
    def update_packages(self) -> None:
        if self.open_update_confirm_dialog():
            self.pmc.perform_update(self.update_table.model.get_packagenames())

    # Opens dialog box for update confirmation
    def open_update_confirm_dialog(self) -> bool:
        dialog: PacmanUpdateDialog = PacmanUpdateDialog(self.update_table.model.get_total_size())
        result = dialog.exec()
        if result == QDialog.Accepted:
            return True
        elif result == QDialog.Rejected:
            return False
