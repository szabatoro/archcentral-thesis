from PySide6.QtCore import QThread, QTimer, Signal
from PySide6.QtWidgets import QWidget
from archcentral.helpers.unitconverter import unit_converter
from archcentral.ui.designer.sysinfo import Ui_SysInfo
from archcentral.controllers.sysinfo_controller import SysInfoController

# system information module
class SysInfoModule(QWidget, Ui_SysInfo):
    fetch_ram_info_signal: Signal = Signal(bool)
    fetch_cpu_info_signal: Signal = Signal()
    fetch_cpu_freqs_signal: Signal = Signal()
    fetch_network_interface_signal: Signal = Signal()
    fetch_network_traffic_signal: Signal = Signal()

    fetch_hostname_signal: Signal = Signal()
    fetch_kernel_signal: Signal = Signal()
    fetch_uptime_signal: Signal = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(SysInfo=self)

        self.destroyed.connect(self.cleanup_thread)

        self.sysret_thread = QThread()

        # Instanciate the system info retriever class and connect its signals
        self.sysret: SysInfoController = SysInfoController()
        self.sysret.moveToThread(self.sysret_thread)

        self.sysret_thread.start()

        self.sysret.public_ip_fetched.connect(self.show_public_ip)
        self.sysret.initial_ram_info_fetched.connect(self.populate_initial_ram_info)
        self.sysret.ram_info_fetched.connect(self.populate_ram_info)
        self.sysret.cpu_info_fetched.connect(self.populate_cpu_info)
        self.sysret.network_interface_fetched.connect(self.populate_network_info)
        self.sysret.cpu_freqs_fetched.connect(self.populate_cpu_freqs)
        self.sysret.network_traffic_fetched.connect(self.populate_network_traffic)

        self.sysret.kernel_fetched.connect(lambda kr: self.kernel_name.setText(f"Kernel: {kr}"))
        self.sysret.hostname_fetched.connect(lambda hn: self.hostname.setText(f"Hostname: {hn}"))
        self.sysret.uptime_fetched.connect(lambda up: self.uptime.setText(f"Uptime: {up}"))

        self.fetch_cpu_info_signal.connect(self.sysret.read_cpu_info)
        self.fetch_cpu_freqs_signal.connect(self.sysret.read_cpu_freqs)
        self.fetch_ram_info_signal.connect(self.sysret.read_ram)
        self.fetch_network_interface_signal.connect(self.sysret.read_network_interface)
        self.fetch_network_traffic_signal.connect(self.sysret.read_network_traffic)

        self.fetch_kernel_signal.connect(self.sysret.fetch_kernel)
        self.fetch_hostname_signal.connect(self.sysret.fetch_hostname)
        self.fetch_uptime_signal.connect(self.sysret.fetch_uptime)

        # Gather info once at launch
        self.fetch_cpu_info_signal.emit()
        self.fetch_network_interface_signal.emit()
        self.fetch_ram_info_signal.emit(True)

        self.fetch_hostname_signal.emit()
        self.fetch_kernel_signal.emit()
        self.fetch_uptime_signal.emit()

        # Set up a timer for the live monitoring
        self.timer: QTimer = QTimer()
        self.timer.setInterval(1000) # 1 sec
        self.timer.timeout.connect(self.timer_connector)
        self.timer.start()

        # Connect buttons
        self.network_public_ip_switch.clicked.connect(self.sysret.fetch_public_ip)

        # Generate legends
        self.network_legend.build(self.network_graph.get_legend_data())
        self.cpu_legend.build(self.cpu_graph.get_legend_data())
        self.ram_legend.build(self.ram_graph.get_legend_data())

    def timer_connector(self) -> None:
        self.fetch_ram_info_signal.emit(False)
        self.fetch_cpu_freqs_signal.emit()
        self.fetch_network_traffic_signal.emit()
        self.fetch_uptime_signal.emit()

    ############### Hardware info ###############
    def show_public_ip(self, ipv4: str, ipv6: str) -> None:
        self.network_public_ip_switch.setDisabled(True)
        self.network_public_ip_switch.setVisible(False)
        self.network_public_ip.setText(f"Public IP:\nIPv4: {ipv4}\nIPv6: {ipv6}")

    def populate_ram_labels(self, label_total_ram: list, label_total_swap: list = None):
        self.ram_amount.setText(f"Used: {label_total_ram[0]} {label_total_ram[1]} / {label_total_ram[2]} {label_total_ram[3]}")
        if label_total_swap:
            self.swap_amount.setText(f"Swap used: {label_total_swap[0]} {label_total_swap[1]} / {label_total_swap[2]} {label_total_swap[3]}")

    def populate_initial_ram_info(self, label_total_ram: list, label_total_swap: list, used_ram: float, used_swap: float, total_ram: float) -> None:
        #ram = self.sysret.read_ram()
        swap_exists = label_total_swap[2] != 0.0
        self.populate_ram_labels(label_total_ram, label_total_swap) if swap_exists else self.populate_ram_labels(label_total_ram)

        self.ram_graph.init_plots(["Used RAM", "Used swap"] if swap_exists else ["Used RAM"])
        self.ram_legend.build(self.ram_graph.get_legend_data())

        # draw the ram graph
        self.ram_graph.plotter([used_ram, used_swap], total_ram)

    def populate_ram_info(self, label_total_ram: list, label_total_swap: list, used_ram: float, used_swap: float, total_ram: float) -> None:
        #ram = self.sysret.read_ram()
        swap_exists = label_total_swap[2] != 0.0
        self.populate_ram_labels(label_total_ram, label_total_swap) if swap_exists else self.populate_ram_labels(label_total_ram)

        # draw the ram graph
        self.ram_graph.plotter([used_ram, used_swap], total_ram)

    def populate_cpu_info(self, cpu_model, cpu_cores, cpu_threads):
        self.cpu_name.setText(f"Name: {cpu_model}")
        self.cpu_core_count.setText(f"Core count: {cpu_cores} cores, {cpu_threads} threads")
        cpu_labels = []
        for i in range(0,cpu_threads):
            cpu_labels.append(f"C{i}")
        self.cpu_graph.init_plots(cpu_labels)
        self.cpu_legend.build(self.cpu_graph.get_legend_data())

    def populate_network_info(self, interface: str, local_ip: str):
        self.network_graph.init_plots(["Upload", "Download"])
        self.network_active_interface.setText(f"Active interface: {interface if interface else "No active network interface."}")
        self.network_local_ip.setText(f"Local IP: {local_ip}")
        self.network_legend.build(self.network_graph.get_legend_data())

    def populate_cpu_freqs(self, cpu_corefreqs):
        ### CPU ###
        # get a list of cpu cores utilisation %
        # draw the cpu graph with every core
        self.cpu_graph.plotter(cpu_corefreqs, 100.0)

    def populate_network_traffic(self, bytes_sent, bytes_recieved):
        bytes_sent_readable: str = unit_converter(bytes_sent, as_tuple=False)
        bytes_recieved_readable : str= unit_converter(bytes_recieved, as_tuple=False)
        self.network_traffic_label.setText(f"Network traffic: {bytes_sent_readable}/s UP, {bytes_recieved_readable}/s DOWN")
        self.network_graph.plotter([bytes_sent, bytes_recieved])

    ############### Software info ###############
    def static_sw_info(self):
        self.sysret.fetch_hostname()
        self.sysret.fetch_kernel()

    def sw_info_monitor(self) -> None:
        uptime: str = self.sysret.fetch_uptime()
        self.uptime.setText(f"Uptime: {uptime}")

    def cleanup_thread(self) -> None:
        """Gracefully stops threads."""
        if self.sysret_thread.isRunning():
            self.sysret_thread.quit()
            self.sysret_thread.wait()
