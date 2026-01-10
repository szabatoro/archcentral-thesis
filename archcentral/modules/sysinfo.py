import socket
import time
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget
from archcentral.ui.designer.sysinfo import Ui_SysInfo
from archcentral.ui.legendwidget import LegendWidget
from archcentral.helpers.qprocesshelper import QProcessHandler
from archcentral.helpers.unitconverter import convert_mem_unit
import re # for taking data manually if info not retrievable by psutil
import psutil # for everything else

# system information module
class SysInfoModule(QWidget, Ui_SysInfo):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(SysInfo=self)

        # module-level variables
        self.active_network_interface: str
        self.bs: float = None # bytes sent
        self.br: float = None # bytes recieved
        # variable to determine if getting swap info is needed
        self.swap_exists: bool = False if psutil.swap_memory().total == 0.0 else True

        # Process runner
        self.hostname_handler: QProcessHandler = QProcessHandler()
        self.kernel_handler: QProcessHandler = QProcessHandler()

        # Gather info once at launch
        self.static_hw_info()
        self.static_sw_info()

        # Set up a timer for the live monitoring
        self.timer: QTimer = QTimer()
        self.timer.setInterval(1000) # 1 sec
        self.timer.timeout.connect(self.hw_info_monitor)
        self.timer.timeout.connect(self.sw_info_monitor)
        self.timer.start()

        # Connect buttons
        self.network_public_ip_switch.clicked.connect(self.fetch_public_ip)

        # Generate legends
        self.network_legend.build(self.network_graph.get_legend_data())
        self.cpu_legend.build(self.cpu_graph.get_legend_data())
        self.ram_legend.build(self.ram_graph.get_legend_data())


    ############### Hardware info ###############

    # Read /proc/cpuinfo
    def read_cpu_info(self) -> str:
        cpu_file = open("/proc/cpuinfo", "r")
        cpu_str: str = cpu_file.read()
        cpu_file.close()
        return cpu_str

    # fetch ipify.org for public ip
    def fetch_public_ip(self) -> str:
        try:
            public_ip_v4 = urlopen('https://api.ipify.org').read().decode('utf8')
        except HTTPError:
            public_ip_v4 = "A network error occured."
        except URLError:
            public_ip_v4 = "There is no IPv4 connectivity."

        try:
            public_ip_v6 = urlopen('https://api6.ipify.org').read().decode('utf8')
        except HTTPError:
            public_ip_v6 = "A network error occured."
        except URLError:
            public_ip_v6 = "There is no IPv6 connectivity."

        self.network_public_ip_switch.setDisabled(True)
        self.network_public_ip_switch.setVisible(False)

        self.network_public_ip.setText(f"Public IP:\nIPv4: {public_ip_v4}\nIPv6: {public_ip_v6}")



    # Stripped from hardware monitor method for use in static_hw_info too
    def set_ram_label(self, ram: tuple[float, str, float, str], swap: tuple[float, str, float, str]=None) -> None:
        self.ram_amount.setText(f"Used: {ram[0]} {ram[1]} / {ram[2]} {ram[3]}")

        if self.swap_exists:
            self.swap_amount.setText(f"Swap used: {swap[0]} {swap[1]} / {swap[2]} {swap[3]}")

    # Collect intitial and static hardware information (only runs once)
    def static_hw_info(self) -> None:
        ### RAM ###
        # psutil returns bytes, convert to kilobytes as a more convenient unit
        # doesn't read swap status if unnecessary
        ram_total: float = float(psutil.virtual_memory().total)
        ram_used: float = float(psutil.virtual_memory().used)
        ram_readable: tuple[float, str, float, str] = convert_mem_unit(ram_used, ram_total)
        if self.swap_exists:
            swap_total: float = float(psutil.swap_memory().total)
            swap_used: float = float(psutil.swap_memory().used)
            swap_readable: tuple[float, str, float, str] = convert_mem_unit(swap_used, swap_total)
            self.set_ram_label(ram_readable, swap_readable)
        else:
            self.set_ram_label(ram_readable)


        self.ram_graph.init_plots(["Used RAM", "Used swap"] if self.swap_exists else ["Used RAM"])

        ### CPU ###
        cpu_str: str = self.read_cpu_info()
        cpu_model: str = re.search(r'model name\s+: (.+)\n', cpu_str).group(1)
        cpu_cores: str = psutil.cpu_count(logical=False)
        cpu_threads: str = psutil.cpu_count(logical=True)

        self.cpu_name.setText(f"Name: {cpu_model}")
        self.cpu_core_count.setText(f"Core count: {cpu_cores} cores, {cpu_threads} threads")

        cpu_labels = []
        for i in range(1,cpu_threads):
            cpu_labels.append(f"C{i-1}")
        self.cpu_graph.init_plots(cpu_labels)

        ### Network ###
        self.network_graph.init_plots(["Upload", "Download"])
        addresses = psutil.net_if_addrs()
        stats = psutil.net_if_stats()

        for intface, addr_list in addresses.items():
            if intface in stats and getattr(stats[intface], "isup") and intface.startswith(("enp", "wlp", "wlan", "eth")):
                self.active_network_interface = intface
                break
            else:
                self.active_network_interface = None

        ip: str
        for addr in addresses[intface]:
            if addr.family == socket.AF_INET:
                ip = addr.address
                break
            else:
                ip = "Not connected."

        self.network_active_interface.setText(f"Active interface: {self.active_network_interface if self.active_network_interface else "No active network interface."}")
        self.network_local_ip.setText(f"Local IP: {ip}")


    # Collect changing hardware information
    def hw_info_monitor(self) -> None:
        ### RAM ###
        # psutil returns bytes, convert to kilobytes as a more convenient unit
        # doesn't read swap status if unnecessary
        ram_total: float = float(psutil.virtual_memory().total)
        ram_used: float = float(psutil.virtual_memory().used)
        ram_readable: tuple[float, str, float, str] = convert_mem_unit(ram_used, ram_total)
        if self.swap_exists:
            swap_total: float = float(psutil.swap_memory().total)
            swap_used: float = float(psutil.swap_memory().used)
            swap_readable: tuple[float, str, float, str] = convert_mem_unit(swap_used, swap_total)
            self.set_ram_label(ram_readable, swap_readable)
        else:
            self.set_ram_label(ram_readable)

        # draw the ram graph
        self.ram_graph.plotter([ram_used, swap_used], ram_total)

        ### CPU ###
        # get a list of cpu cores utilisation %
        cpu_corefreqs: list[float] = psutil.cpu_percent(percpu=True)
        # draw the cpu graph with every core
        self.cpu_graph.plotter(cpu_corefreqs, 100.0)
        ### Network ###
        # only perform if there is an active network interface
        if self.active_network_interface:
            # if no value has been recorded yet don't do calculations
            if (self.bs is None) and (self.br is None):
                self.bs = psutil.net_io_counters(pernic=True)[self.active_network_interface].bytes_sent
                self.br = psutil.net_io_counters(pernic=True)[self.active_network_interface].bytes_recv
            else:
                # provided network traffic is cumulative, need to calculate the difference for network speed
                current_bs: float = psutil.net_io_counters(pernic=True)[self.active_network_interface].bytes_sent
                diff_bs: float = current_bs - self.bs
                self.bs = current_bs
                current_br: float = psutil.net_io_counters(pernic=True)[self.active_network_interface].bytes_recv
                diff_br: float = current_br - self.br
                self.br = current_br

                self.network_graph.plotter([diff_bs, diff_br])

    ############### Software info ###############

    def static_sw_info(self) -> None:
        self.hostname_handler.start_process("uname",  ["-n"])
        self.hostname_handler.finished.connect(lambda hn: self.hostname.setText(f"Hostname: {hn}"))

        self.kernel_handler.start_process("uname",  ["-sr"])
        self.kernel_handler.finished.connect(lambda kr: self.kernel_name.setText(f"Kernel: {kr}"))

    def sw_info_monitor(self) -> None:
        uptime: str = time.strftime("%Hh:%Mm:%Ss", time.gmtime(time.time() - psutil.boot_time()))
        self.uptime.setText(f"Uptime: {uptime}")
