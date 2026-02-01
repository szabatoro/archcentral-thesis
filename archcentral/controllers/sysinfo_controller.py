from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from archcentral.helpers.unitconverter import convert_mem_unit
from PySide6.QtCore import QObject,  Signal
from archcentral.helpers.qprocesshelper import QProcessHandler
import re # for taking data from files if info not retrievable by psutil
import psutil # for everything else
import socket
import time

# Class intended to be used by the sysinfo module to fetch system information
class SysInfoController(QObject):
    # Signals
    kernel_fetched: Signal = Signal(str)
    hostname_fetched: Signal = Signal(str)

    def __init__(self) -> None:
        super().__init__()

        # Process runners
        self.hostname_handler: QProcessHandler = QProcessHandler()
        self.kernel_handler: QProcessHandler = QProcessHandler()

        # module-level variables
        self.active_network_interface: str
        self.bs: float = None # bytes sent
        self.br: float = None # bytes recieved
        self.swap_exists: bool = False if psutil.swap_memory().total == 0.0 else True

    # Read /proc/cpuinfo
    def read_cpu_info(self) -> tuple[str, str, str]:
        """
        Returns a tuple with the following items:
            0: Name/Model of the CPU
            1: Number of CPU cores
            2: Number of CPU threads
        """

        cpu_file = open("/proc/cpuinfo", "r")
        cpu_str: str = cpu_file.read()
        cpu_file.close()

        cpu_model: str = re.search(r'model name\s+: (.+)\n', cpu_str).group(1)
        cpu_cores: str = psutil.cpu_count(logical=False)
        cpu_threads: str = psutil.cpu_count(logical=True)

        return (cpu_model, cpu_cores, cpu_threads)

    # get a list of cpu cores utilisation %
    def read_cpu_freqs(self) -> list[float]:
        """
        Returns a list of floats containing the load on each thread.
        """

        return psutil.cpu_percent(percpu=True)


    # fetch ipify.org for public ip
    def fetch_public_ip(self) -> tuple[str, str]:
        """
        Returns a tuple with the following items:
            0: The public IPv4 address
            1: The public IPv6 address
        """

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

        return (public_ip_v4, public_ip_v6)


    ### RAM ###
    # psutil returns bytes, convert to kilobytes as a more convenient unit
    # doesn't read swap status if unnecessary
    def read_ram(self):
        """
        Returns a tuple with the following items:
            0: Used/Total RAM (for label)
            1: Used/Total swap (for label)
            2: Used RAM
            3: Used swap
            4: Total available RAM
        """

        ram_total: float = float(psutil.virtual_memory().total)
        ram_used: float = float(psutil.virtual_memory().used)
        ram_readable: str = convert_mem_unit(ram_used, ram_total)
        swap_total: float = float(psutil.swap_memory().total)
        swap_used: float = float(psutil.swap_memory().used)
        swap_readable: str = convert_mem_unit(swap_used, swap_total)
        return (ram_readable, swap_readable, ram_used, swap_used, ram_total)

    def read_network_interface(self):
        """
        Returns a tuple with the following items:
            0: Local IP address
            1: Name of the active network interface
        """
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

        return (ip, self.active_network_interface)

    def read_network_traffic(self):
        """
        Returns a tuple with the following items:
            0: Current upload speed
            1: Current download speed

        If no active network interface is present, returns None.
        """

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
                return (diff_bs, diff_br)
        else:
            return None

    def fetch_kernel(self):
        """
        Runs uname through qprocess and emits the kernel_fetched signal.
        """
        self.kernel_handler.start_process("uname",  ["-sr"])
        self.kernel_handler.finished.connect(self._fetch_kernel_internal)

    def _fetch_kernel_internal(self, data):
        self.kernel_fetched.emit(data)

    def fetch_hostname(self):
        """
        Runs uname through qprocess and emits the hostname_fetched signal.
        """
        self.hostname_handler.start_process("uname",  ["-n"])
        self.hostname_handler.finished.connect(self._fetch_hostname_internal)

    def _fetch_hostname_internal(self, data):
        self.hostname_fetched.emit(data)

    def fetch_uptime(self):
        """
        Returns a H:M:S formatted uptime string.
        """
        return time.strftime("%Hh:%Mm:%Ss", time.gmtime(time.time() - psutil.boot_time()))
