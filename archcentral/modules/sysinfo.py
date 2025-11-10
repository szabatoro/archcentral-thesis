from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget
from archcentral.ui.designer.sysinfo import Ui_SysInfo
import re

# system information module
class SysInfoModule(QWidget, Ui_SysInfo):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(SysInfo=self)

        # File IO for reading hardware info
        self.cpu_file = open("/proc/cpuinfo")
        self.ram_file = open("/proc/meminfo")
        self.cpu_str: str = self.cpu_file.read()
        self.ram_str: str = self.ram_file.read()

        # Getting RAM info
        self.ram_total: float = float(re.search(r'MemTotal:\s+(\d+)', self.ram_str).group(1))
        self.ram_avail: float = float(re.search(r'MemAvailable:\s+(\d+)', self.ram_str).group(1))
        self.ram_used: float = self.ram_total-self.ram_avail

        self.hw_info_setup()

        self.timer: QTimer = QTimer()
        self.timer.setInterval(1000)
        #self.timer.connect(self.hw_monitor_setup)

    # Initialize hardware info labels with file data
    def hw_info_setup(self) -> None:
        cpu_model: str = re.search(r'model name\s+: (.+)\n', self.cpu_str).group(1)
        self.cpu_info.setText(f"CPU: {cpu_model}")

        # Use unit most suitable for amount of ram
        if self.ram_used/1024.0 < 1024.0:
            ram_used_unit = "MiB"
            if self.ram_total/1024.0 < 1024.0:
                ram_total_unit = "MiB"
        else:
            ram_used_unit = "GiB"
            ram_total_unit = "GiB"

        self.ram_info.setText(
            f"RAM: {round(self.ram_used/1024.0/1024.0, 2)} {ram_used_unit} / {round(self.ram_total/1024.0/1024.0, 2)} {ram_total_unit}"
        )

    def hw_monitor_setup(self) -> None:
        pass

    def get_cpu_info(self) -> None:
        pass
