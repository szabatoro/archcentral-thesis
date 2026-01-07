from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QColor

class LegendWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        # placeholder for data
        self.items = []

    def build(self, data):
        """
        data: list of tuples [(color, name), ...]
        color: QColor or hex string
        name: str
        """
        # clear previous items
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().deleteLater()

        for color, name in data:
            row = QHBoxLayout()

            # color box
            color_label = QLabel()
            color_label.setFixedSize(20, 20)
            if isinstance(color, str):
                color = QColor(color)
            color_label.setStyleSheet(f"background-color: {color.name()};")

            # name label
            name_label = QLabel(name)

            row.addWidget(color_label)
            row.addWidget(name_label)
            row.addStretch()  # push items to left
            self.layout.addLayout(row)
