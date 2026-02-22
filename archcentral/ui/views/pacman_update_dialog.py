from archcentral.ui.designer.pacmanupdatedialog import Ui_PacmanUpdateDialog
from archcentral.helpers.unitconverter import unit_converter
from PySide6.QtWidgets import QDialog

class PacmanUpdateDialog(QDialog, Ui_PacmanUpdateDialog):
    def __init__(self, updatesize) -> None:
        super().__init__()
        self.setupUi(self)

        value, unit = unit_converter(updatesize)

        self.update_info.setText(f"Total size of update: {value:.2f} {unit}.")
