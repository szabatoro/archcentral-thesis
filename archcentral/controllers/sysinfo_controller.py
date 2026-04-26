import sys
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from archcentral.helpers.unitconverter import convert_mem_unit
from PySide6.QtCore import QObject,  Signal
from PySide6 import __version__ as pysidever
from archcentral.helpers.qprocesshelper import QProcessHandler
import re # for taking data from files if info not retrievable by psutil
import psutil # for everything else
import socket
import time
import os

# Class intended to be used by the sysinfo module to fetch system information
class SysInfoController(QObject):
    # Signals
    public_ip_fetched: Signal = Signal(str, str)
    cpu_info_fetched: Signal = Signal(str, int, int)
    initial_ram_info_fetched: Signal = Signal(list, list, float, float, float)
    ram_info_fetched: Signal = Signal(list, list, float, float, float)
    network_interface_fetched: Signal = Signal(str, str)
    cpu_freqs_fetched: Signal = Signal(float, list)
    network_traffic_fetched: Signal = Signal(int, int)

    system_info_fetched: Signal = Signal(str, str)
    uptime_fetched: Signal = Signal(str)
    de_info_fetched: Signal = Signal(str, str, str, str)
    build_info_fetched: Signal = Signal(str, str)

    def __init__(self) -> None:
        super().__init__()

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
        cpu_cores: int = psutil.cpu_count(logical=False)
        cpu_threads: int = psutil.cpu_count(logical=True)

        self.cpu_info_fetched.emit(cpu_model, cpu_cores, cpu_threads)

    # get a list of cpu cores utilisation %
    def read_cpu_freqs(self) -> list[float]:
        """
        Returns a list of floats containing the load on each thread.
        """
        cpu_util_avg = psutil.cpu_percent()
        cpu_freqs_per_thread = psutil.cpu_percent(percpu=True)
        self.cpu_freqs_fetched.emit(cpu_util_avg, cpu_freqs_per_thread)


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

        self.public_ip_fetched.emit(public_ip_v4, public_ip_v6)


    ### RAM ###
    # psutil returns bytes, convert to kilobytes as a more convenient unit
    # doesn't read swap status if unnecessary
    def read_ram(self, is_for_init: bool):
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
        if is_for_init:
            self.ram_info_fetched.emit(ram_readable, swap_readable, ram_used, swap_used, ram_total)
        else:
            self.initial_ram_info_fetched.emit(ram_readable, swap_readable, ram_used, swap_used, ram_total)

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

        self.network_interface_fetched.emit(self.active_network_interface, ip)

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
                self.network_traffic_fetched.emit(diff_bs, diff_br)
        else:
            return

    def fetch_system_info(self):
        """Fetches kernel version and hostname."""
        uname = os.uname()
        self.system_info_fetched.emit(uname.release, uname.nodename)

    def fetch_uptime(self):
        """
        Returns a H:M:S formatted uptime string.
        """
        self.uptime_fetched.emit(time.strftime("%Hh:%Mm:%Ss", time.gmtime(time.time() - psutil.boot_time())))

    def fetch_de_info(self):
        """Fetches various information about the graphical environment."""
        detected_wm: str = ""
        detected_de: str = ""
        wm_list = {
            "kwin": "KWin",
            "kwin_wayland": "KWin",
            "gnome-shell": "Mutter",
            "xfwm4": "Xfwm4",
            "cosmic-comp": "Cosmic",
            "i3": "i3",
            "sway": "Sway",
            "openbox": "Openbox",
            "awesome": "Awesome",
            "bspwm": "bspwm",
            "hyprland": "Hyprland",
            "labwc": "Labwc"
        }

        for proc in psutil.process_iter(["name"]):
            name = proc.info["name"]
            if name in wm_list.keys():
                detected_wm = wm_list.get(name)
                break

        match os.environ.get("XDG_SESSION_DESKTOP"):
            case "KDE":
                detected_de = "KDE Plasma"
            case "gnome":
                detected_de = "GNOME"
            case "lxqt" | "lxqt-wayland":
                detected_de = "LXQT"
            case "xfce":
                detected_de = "XFCE"
            case "cosmic":
                detected_de = "Cosmic"

        display_server_env = os.environ.get("XDG_SESSION_TYPE")
        display_server_type = "Wayland" if display_server_env == 'wayland' else "X11"
        locale = os.environ.get("LANG")

        self.de_info_fetched.emit(detected_wm, detected_de, display_server_type, locale)

    def fetch_build_info(self):
        """Fetches python and pyside versions used by the application."""
        self.build_info_fetched.emit(sys.version, pysidever)
