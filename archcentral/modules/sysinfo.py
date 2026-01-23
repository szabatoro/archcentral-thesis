from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget
from archcentral.ui.designer.sysinfo import Ui_SysInfo
from archcentral.helpers.sysinfo_retrievers import SysInfoRetriever

# system information module
class SysInfoModule(QWidget, Ui_SysInfo):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(SysInfo=self)

        # Instanciate the system info retriever class and connect its signals
        self.sysret: SysInfoRetriever = SysInfoRetriever()
        self.sysret.kernel_fetched.connect(lambda kr: self.kernel_name.setText(f"Kernel: {kr}"))
        self.sysret.hostname_fetched.connect(lambda hn: self.hostname.setText(f"Hostname: {hn}"))

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
        self.network_public_ip_switch.clicked.connect(self.show_public_ip)

        # Generate legends
        self.network_legend.build(self.network_graph.get_legend_data())
        self.cpu_legend.build(self.cpu_graph.get_legend_data())
        self.ram_legend.build(self.ram_graph.get_legend_data())


    ############### Hardware info ###############
    def show_public_ip(self) -> str:
        ips: tuple[str, str] = self.sysret.fetch_public_ip()
        self.network_public_ip_switch.setDisabled(True)
        self.network_public_ip_switch.setVisible(False)
        self.network_public_ip.setText(f"Public IP:\nIPv4: {ips[0]}\nIPv6: {ips[1]}")

    # Stripped from hardware monitor method for use in static_hw_info too
    def set_ram_label(self, ram: tuple[float, str, float, str], swap: tuple[float, str, float, str]=None) -> None:
        self.ram_amount.setText(f"Used: {ram[0]} {ram[1]} / {ram[2]} {ram[3]}")

        if self.sysret.swap_exists:
            self.swap_amount.setText(f"Swap used: {swap[0]} {swap[1]} / {swap[2]} {swap[3]}")

    # Collect intitial and static hardware information (only runs once)
    def static_hw_info(self) -> None:
        ### RAM ###
        # psutil returns bytes, convert to kilobytes as a more convenient unit
        # doesn't read swap status if unnecessary
        ram = self.sysret.read_ram()
        swap_exists = ram[1] != 0.0
        if swap_exists:
            self.ram_amount.setText(f"Used: {ram[0][0]} {ram[0][1]} / {ram[0][2]} {ram[0][3]}")
            self.swap_amount.setText(f"Swap used: {ram[1][0]} {ram[1][1]} / {ram[1][2]} {ram[1][3]}")
            #self.set_ram_label(ram[0], ram[1])
        else:
            self.ram_amount.setText(f"Used: {ram[0][0]} {ram[0][1]} / {ram[0][2]} {ram[0][3]}")
            #self.set_ram_label(ram[0])

        self.ram_graph.init_plots(["Used RAM", "Used swap"] if swap_exists else ["Used RAM"])

        ### CPU ###
        cpu = self.sysret.read_cpu_info()

        self.cpu_name.setText(f"Name: {cpu[0]}")
        self.cpu_core_count.setText(f"Core count: {cpu[1]} cores, {cpu[2]} threads")

        cpu_labels = []
        for i in range(0,cpu[2]):
            cpu_labels.append(f"C{i}")
        self.cpu_graph.init_plots(cpu_labels)

        ### Network ###
        self.network_graph.init_plots(["Upload", "Download"])
        network = self.sysret.read_network_interface()
        self.network_active_interface.setText(f"Active interface: {network[1] if network[1] else "No active network interface."}")
        self.network_local_ip.setText(f"Local IP: {network[0]}")


    # Collect changing hardware information
    def hw_info_monitor(self) -> None:
        ### RAM ###
        ram = self.sysret.read_ram()
        swap_exists = ram[1] != 0.0
        if swap_exists:
            self.ram_amount.setText(f"Used: {ram[0][0]} {ram[0][1]} / {ram[0][2]} {ram[0][3]}")
            self.swap_amount.setText(f"Swap used: {ram[1][0]} {ram[1][1]} / {ram[1][2]} {ram[1][3]}")
            #self.set_ram_label(ram[0], ram[1])
        else:
            self.ram_amount.setText(f"Used: {ram[0][0]} {ram[0][1]} / {ram[0][2]} {ram[0][3]}")
            #self.set_ram_label(ram[0])

        # draw the ram graph
        self.ram_graph.plotter([ram[2], ram[3]], ram[4])

        ### CPU ###
        # get a list of cpu cores utilisation %
        cpu_corefreqs: list[float] = self.sysret.read_cpu_freqs()
        # draw the cpu graph with every core
        self.cpu_graph.plotter(cpu_corefreqs, 100.0)

        ### Network ###
        network = self.sysret.read_network_traffic()
        if network:
            # draw the network graph
            self.network_graph.plotter([network[0], network[1]])

    ############### Software info ###############
    def static_sw_info(self):
        self.sysret.fetch_hostname()
        self.sysret.fetch_kernel()

    def sw_info_monitor(self) -> None:
        uptime: str = self.sysret.fetch_uptime()
        self.uptime.setText(f"Uptime: {uptime}")
