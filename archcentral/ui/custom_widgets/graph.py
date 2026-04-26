from PySide6.QtWidgets import QWidget, QVBoxLayout
from pyqtgraph import PlotWidget, AxisItem, mkPen

# Custom Y axis to dynamically change displayed unit
class ByteAxis(AxisItem):
    def tickStrings(self, values, scale, spacing) -> list:
        min_val, max_val = self.range

        if max_val < 1024:
            divisor = 1
            #unit = "B"
        elif max_val < 1024**2:
            divisor = 1024
            #unit = "KB"
        elif max_val < 1024**3:
            divisor = 1024**2
            #unit = "MB"
        else:
            divisor = 1024**3
            #unit = "GB"

        self.setLabel(units="B")

        strings = []
        for value in values:
            scaled = value / divisor
            strings.append(f"{scaled:.2f}")

        return strings

# Base class for resource visualizer widgets
class ResourceGraph(QWidget):
    def __init__(self, parent=None, not_byte=None) -> None:
        super().__init__(parent)
        self.value_store: list[list[float]]= [] # values needed for plotting are stored here
        self.graph_length: int = 30
        self.plots: list = []
        self.x_index: int = 0

        # Create and configure the plot widget
        if not_byte: # Specifically for the CPU plot as it's the only one not measured in bytes
            self.graph_widget: PlotWidget = PlotWidget()
        else:
            self.axis = ByteAxis("left")
            self.graph_widget: PlotWidget = PlotWidget(axisItems={"left": self.axis})
        self.graph_legend = self.graph_widget.addLegend()
        self.graph_legend.hide()
        self.graph_widget.setMouseEnabled(False, False)
        self.graph_widget.getAxis('bottom').setStyle(showValues=False)
        self.graph_widget.setXRange(0, self.graph_length)

        # Create a layout to make the plot widget fit its host widget
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.graph_widget)

    def get_legend_data(self):
        """Extracting plot name and color for creating a legend"""
        legend_data = []

        for plot in self.plots:
            pen = plot.opts['pen']
            color = pen.color()
            legend_data.append((color, plot.name()))

        return legend_data

    def init_plots(self, line_labels) -> None:
        """Set up plots as needed"""
        self.plots.clear()
        for i, label in enumerate(line_labels):
            pen = mkPen(color=i)
            plot = self.graph_widget.plot(
                name=label,
                pen=pen
            )
            self.plots.append(plot)

    def plotter(self, value_points: list[float], upper_limit: float = None) -> None:
        """Plot the graph with the relevant data, handles multiple plots if needed"""
        self.x_index += 1

        self.value_store.append(value_points)

        if len(self.value_store) > self.graph_length:
            self.value_store.pop(0)

        if upper_limit is not None:
            ymax = upper_limit
        else:
            ymax = max(max(row) for row in self.value_store)

        self.graph_widget.setYRange(0, ymax)

        start = self.x_index - len(self.value_store)
        x_data = [start + i for i in range(len(self.value_store))]

        for i, plot in enumerate(self.plots):
            ydata = [row[i] for row in self.value_store]
            plot.setData(x=x_data, y=ydata)

        if len(self.value_store) < self.graph_length:
            self.graph_widget.setXRange(0, self.graph_length)
        else:
            self.graph_widget.setXRange(
                self.x_index - self.graph_length,
                self.x_index
            )

# Graph widget for visualizing CPU clocks
class CPUGraph(ResourceGraph):
    def __init__(self, parent=None) -> None:
        super().__init__(parent, True)

# Graph widget for visualizing network traffic
class NetworkGraph(ResourceGraph):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

# Graph widget for visualizing RAM usage
class RAMGraph(ResourceGraph):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
