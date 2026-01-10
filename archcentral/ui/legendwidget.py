from PySide6.QtWidgets import QWidget, QLabel, QGridLayout, QHBoxLayout
from PySide6.QtGui import QColor

# Widget that auto-builds legend for a graph with the given plot names and color codes
class LegendWidget(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.items = []

    def build(self, data) -> None:
        # clear previous items (widgets and layouts)
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())

        columns = 3  # number of columns in the grid

        for index, (color, name) in enumerate(data):
            row = index // columns
            col = index % columns

            # container widget for one legend item
            item_widget = QWidget()
            row_layout = QHBoxLayout(item_widget)
            row_layout.setContentsMargins(0, 0, 0, 0)

            # color box
            color_label = QLabel()
            color_label.setFixedSize(10, 10)
            if isinstance(color, str):
                color = QColor(color)
            color_label.setStyleSheet(f"background-color: {color.name()};")

            # name label
            name_label = QLabel(name)

            row_layout.addWidget(color_label)
            row_layout.addWidget(name_label)
            row_layout.addStretch()

            self.layout.addWidget(item_widget, row, col)
