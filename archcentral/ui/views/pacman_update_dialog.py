from archcentral.ui.designer.pacmanupdatedialog import Ui_PacmanUpdateDialog
from PySide6.QtWidgets import QDialog

class PacmanUpdateDialog(QDialog, Ui_PacmanUpdateDialog):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
