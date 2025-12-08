from PySide6.QtWidgets import QWidget, QVBoxLayout
from pyqtgraph import PlotWidget

# Base class for resource visualizer widgets
class ResourceGraph(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        # Initialize plot data
        self.value_store: list[list[float]]= [] # values needed for plotting are stored here
        self.graph_length: int = 30
        self.plots: list = []

        # Create and configure the plot widget
        self.graph_widget: PlotWidget = PlotWidget()
        self.graph_widget.setMouseEnabled(False, False)
        self.graph_widget.getAxis('bottom').setStyle(showValues=False)
        self.graph_widget.setXRange(0, self.graph_length)

        # Create a layout to make the plot widget fit its host widget
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.graph_widget)

    # Plot the graph with the relevant data, handles multiple plots if needed
    def plotter(self, value_points: list[float], upper_limit: float = None) -> None:
        self.value_store.append(value_points)
        # set graph range on the y axis, use largest value in value store unless the upper_limit parameter is given
        self.graph_widget.setYRange(0, upper_limit if upper_limit else max(self.value_store[-1]))

        # for keeping the plot within the length of the graph, pop the first value at every step after the length limit is reached
        if len(self.value_store) > self.graph_length:
            self.value_store.pop(0)

        # make a plot for each value point
        for i in range(len(value_points)):
            ydata: list[float] = [val[i] for val in self.value_store]
            self.graph_widget.plot(ydata, clear=(i==0), pen=(i, len(value_points)))


# Graph widget for visualizing CPU clocks
class CPUGraph(ResourceGraph):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

# Graph widget for visualizing GPU clocks/mem usage (??Undecided)
class NetworkGraph(ResourceGraph):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

# Graph widget for visualizing RAM usage
class RAMGraph(ResourceGraph):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
