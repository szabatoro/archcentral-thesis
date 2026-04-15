from archcentral.ui.designer.dialogs.pacmanconflictdialog import Ui_PacmanConflictDialog
from PySide6.QtWidgets import QDialog

class PacmanConflictDialog(QDialog, Ui_PacmanConflictDialog):
    def __init__(self, package1, package2, package_to_remove) -> None:
        super().__init__()
        self.setupUi(self)

        self.conflict_label.setText(f"Package conflict detected between {package1} and {package2}. Remove {package_to_remove}?")
