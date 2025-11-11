from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget
from archcentral.ui.designer.sysinfo import Ui_SysInfo
import re # for taking data manually if info not retrievable by psutil
import psutil # for everything else

# system information module
class SysInfoModule(QWidget, Ui_SysInfo):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(SysInfo=self)

        self.static_hw_info()
        # Set up a timer for the live monitoring
        self.timer: QTimer = QTimer()
        self.timer.setInterval(1000) # 1 sec
        self.timer.timeout.connect(self.hw_info_monitor)
        self.timer.start()

    # Read /proc/cpuinfo
    def read_cpu_info(self) -> str:
        cpu_file = open("/proc/cpuinfo", "r")
        cpu_str: str = cpu_file.read()
        cpu_file.close()
        return cpu_str

    # Stripped from hardware monitor method for use in static_hw_info too
    def set_ram_label(self, ram_used: float, ram_total: float) -> None:
        # Use unit most suitable for amount of ram
        if ram_used/1024.0 < 1024.0:
            ram_used_unit = "MiB"
            if ram_total/1024.0 < 1024.0:
                ram_total_unit = "MiB"
        else:
            ram_used_unit = "GiB"
            ram_total_unit = "GiB"

        self.ram_amount.setText(
            f"RAM: {round(ram_used/1024.0/1024.0, 2)} {ram_used_unit} / {round(ram_total/1024.0/1024.0, 2)} {ram_total_unit}"
        )

    # Collect static hardware information (only runs once)
    def static_hw_info(self) -> None:
        cpu_str: str = self.read_cpu_info()
        cpu_model: str = re.search(r'model name\s+: (.+)\n', cpu_str).group(1)
        cpu_cores: str = psutil.cpu_count(logical=False)
        cpu_threads: str = psutil.cpu_count(logical=True)
        ram_total: str = float(psutil.virtual_memory().total)/1024.0
        ram_used: str = float(psutil.virtual_memory().used)/1024.0
        self.set_ram_unit_label(ram_used, ram_total)
        self.cpu_name.setText(f"CPU name: {cpu_model}")
        self.cpu_core_count.setText(f"CPU cores: {cpu_cores} cores, {cpu_threads} threads")

    # Collect changing hardware information
    def hw_info_monitor(self) -> None:
        ### RAM ###
        # psutil returns bytes, convert to kilobytes as a more convenient unit
        ram_total: float = float(psutil.virtual_memory().total)/1024.0
        ram_used: float = float(psutil.virtual_memory().used)/1024.0
        self.set_ram_unit_label(ram_used, ram_total)

        self.ram_graph.plotter([ram_used/1024], ram_total/1024)

        ### CPU ###
        cpu_corefreqs = psutil.cpu_percent(percpu=True)
        self.cpu_graph.plotter(cpu_corefreqs, 100.0)
