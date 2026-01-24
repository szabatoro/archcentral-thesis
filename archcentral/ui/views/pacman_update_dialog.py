from archcentral.ui.designer.pacmanupdatedialog import Ui_PacmanUpdateDialog
from PySide6.QtWidgets import QDialog

class PacmanUpdateDialog(QDialog, Ui_PacmanUpdateDialog):
    def __init__(self, updatesize) -> None:
        super().__init__()
        self.setupUi(self)

        self.update_info.setText(f"Total size of update: {updatesize}")
