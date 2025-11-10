from PySide6.QtWidgets import QWidget, QVBoxLayout
from pyqtgraph import PlotWidget

# Base class for resource visualizer widgets
class ResourceGraph(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        # Create the plot widget
        self.graphWidget: PlotWidget = PlotWidget()
        self.graphWidget.setMouseEnabled(False, False)

        # Create a layout to make the plot widget fit its host widget
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.graphWidget)

# Graph widget for visualizing CPU clocks
class CPUGraph(ResourceGraph):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

# Graph widget for visualizing GPU clocks/mem usage (??Undecided)
class GPUGraph(ResourceGraph):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

# Graph widget for visualizing RAM usage
class RAMGraph(ResourceGraph):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
