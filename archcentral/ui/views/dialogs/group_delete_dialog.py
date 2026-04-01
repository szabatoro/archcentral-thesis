from archcentral.helpers.custom_classes import GroupInfo
from archcentral.ui.designer.dialogs.groupdeletedialog import Ui_GroupDeleteDialog
from PySide6.QtWidgets import QDialog
from PySide6.QtGui import Qt

class GroupDeleteDialog(QDialog, Ui_GroupDeleteDialog):
    def __init__(self, selected_group: GroupInfo, parent=None) -> None:
        super().__init__(parent)
        self.setupUi(self)

        self.setWindowTitle(f"Deleting group \"{selected_group.name}\"")
        self.group_delete_label.setText(f"Are you sure you want to delete group \"{selected_group.name}\"?")
