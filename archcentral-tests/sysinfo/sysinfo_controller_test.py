import pytest
from unittest.mock import MagicMock, patch
from archcentral.controllers.sysinfo_controller import SysInfoController

@pytest.fixture
def controller():
    return SysInfoController()

@patch("builtins.open", new_callable=MagicMock)
@patch("archcentral.controllers.sysinfo_controller.re.search")
@patch("archcentral.controllers.sysinfo_controller.psutil.cpu_count")
def test_read_cpu_info(mock_count, mock_search, mock_open, controller):
    mock_search.return_value.group.return_value = "Intel i7"
    mock_count.side_effect = [4, 8]  # cores, threads

    emitted = []
    controller.cpu_info_fetched.connect(lambda *args: emitted.append(args))

    controller.read_cpu_info()

    assert emitted[0] == ("Intel i7", 4, 8)

@patch("archcentral.controllers.sysinfo_controller.urlopen")
def test_fetch_public_ip(mock_urlopen, controller):
    mock_urlopen.return_value.read.return_value = b"123.123.123.123"

    emitted = []
    controller.public_ip_fetched.connect(lambda v4, v6: emitted.append((v4, v6)))

    controller.fetch_public_ip()

    assert emitted[0] == ("123.123.123.123", "123.123.123.123")

@patch("archcentral.controllers.sysinfo_controller.psutil.virtual_memory")
@patch("archcentral.controllers.sysinfo_controller.psutil.swap_memory")
def test_read_ram(mock_swap, mock_mem, controller):

    mock_mem.return_value.total = 8589934592 # 8 gig total ram
    mock_mem.return_value.used = 1073741824 # 1 gig used ram

    mock_swap.return_value.total = 8589934592 # 8 gig total swap
    mock_swap.return_value.used = 536870912 # 8 gig used swap

    emitted = []
    controller.initial_ram_info_fetched.connect(lambda *args: emitted.append(args))

    controller.read_ram(is_for_init=True)

    assert len(emitted) == 1

    args = emitted[0]

    assert args[0] == (1, "GiB", 8, "GiB")   # RAM label
    assert args[1] == (512, "MiB", 8, "GiB")   # SWAP label
    assert args[2] == 1073741824
    assert args[3] == 536870912
    assert args[4] == 8589934592

@patch("archcentral.controllers.sysinfo_controller.psutil.net_if_addrs")
@patch("archcentral.controllers.sysinfo_controller.psutil.net_if_stats")
def test_read_network_interface(mock_stats, mock_addrs, controller):
    mock_stats.return_value = {
        "eth0": MagicMock(isup=True)
    }

    mock_addrs.return_value = {
        "eth0": [
            MagicMock(family=2, address="192.168.1.10")
        ]
    }

    emitted = []
    controller.network_interface_fetched.connect(lambda *args: emitted.append(args))

    controller.read_network_interface()

    assert emitted[0][0] == "eth0"
    assert emitted[0][1] == "192.168.1.10"

@patch("archcentral.controllers.sysinfo_controller.psutil.net_io_counters")
def test_read_network_traffic(mock_io, controller):
    controller.active_network_interface = "eth0"

    mock_io.side_effect = [
        {"eth0": MagicMock(bytes_sent=1000, bytes_recv=2000)},
        {"eth0": MagicMock(bytes_sent=2100, bytes_recv=3000)},
    ]

    emitted = []
    controller.network_traffic_fetched.connect(lambda *args: emitted.append(args))

    controller.read_network_traffic()
    controller.read_network_traffic()

    assert emitted[0] == (1100, 1000)

@patch("archcentral.controllers.sysinfo_controller.os.uname")
def test_fetch_system_info(mock_uname, controller):
    mock_uname.return_value.release = "Linux 6.1"
    mock_uname.return_value.nodename = "test-machine"

    emitted = []
    controller.system_info_fetched.connect(lambda *args: emitted.append(args))

    controller.fetch_system_info()

    assert emitted[0] == ("Linux 6.1", "test-machine")

@patch("archcentral.controllers.sysinfo_controller.time.time")
@patch("archcentral.controllers.sysinfo_controller.psutil.boot_time")
def test_fetch_uptime(mock_boot, mock_time, controller):
    mock_boot.return_value = 1000
    mock_time.return_value = 1060

    emitted = []
    controller.uptime_fetched.connect(lambda x: emitted.append(x))

    controller.fetch_uptime()

    assert "00h:01m" in emitted[0]

@patch("archcentral.controllers.sysinfo_controller.psutil.process_iter")
@patch("archcentral.controllers.sysinfo_controller.os.environ.get")
def test_fetch_de_info(mock_env, mock_proc, controller):
    mock_proc.return_value = [
        MagicMock(info={"name": "kwin"})
    ]

    mock_env.side_effect = lambda k: {
        "XDG_SESSION_DESKTOP": "KDE",
        "XDG_SESSION_TYPE": "wayland",
        "LANG": "hu_HU.UTF-8"
    }.get(k)

    emitted = []
    controller.de_info_fetched.connect(lambda *args: emitted.append(args))

    controller.fetch_de_info()

    assert "KWin" in emitted[0]
    assert "KDE Plasma" in emitted[0]
    assert "Wayland" in emitted[0]
    assert "hu_HU.UTF-8" in emitted[0]

def test_fetch_build_info(controller):
    emitted = []
    controller.build_info_fetched.connect(lambda *args: emitted.append(args))

    with patch("archcentral.controllers.sysinfo_controller.sys.version", "Python 3.3"), \
         patch("archcentral.controllers.sysinfo_controller.pysidever", "6.6"):

        controller.fetch_build_info()

    assert emitted[0] == ("Python 3.3", "6.6")
