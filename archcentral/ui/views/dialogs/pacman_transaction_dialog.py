from typing import Literal
from archcentral.ui.designer.dialogs.pacmantransactiondialog import Ui_PacmanTransactionDialog
from PySide6.QtWidgets import QDialog, QDialogButtonBox


class PacmanTransactionDialog(QDialog, Ui_PacmanTransactionDialog):
    def __init__(self, spawn_reason: Literal["multichoice", "conflict"],
        package1: str = None, package2: str = None, package_to_remove: str = None) -> None:
        super().__init__()
        self.setupUi(self)

        match spawn_reason:
            case "conflict":
                self.info_label.setText(f"Package conflict detected between {package1} and {package2}. Remove {package_to_remove}?")
            case "multichoice":
                self.setWindowTitle("Unsupported operation detected")
                self.info_label.setText("""
Pacman operations requiring multiple choices are unsupported due to technical limitations.
Quitting the process requires elevated privilages, so you'll be prompted for a password.
                """)
                self.button_box.button(QDialogButtonBox.StandardButton.No).setDisabled(True)
