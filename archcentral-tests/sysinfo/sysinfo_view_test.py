import pytest
from unittest.mock import MagicMock, patch

from archcentral.ui.views.sysinfo import SysInfoModule

@pytest.fixture
def sysinfo(qtbot):
    with patch("archcentral.ui.views.sysinfo.SysInfoController") as mock_ctrl_cls:

        mock_ctrl = MagicMock()
        mock_ctrl_cls.return_value = mock_ctrl

        widget = SysInfoModule()
        qtbot.addWidget(widget)

        yield widget, mock_ctrl

        widget.cleanup_thread()

def test_sysinfo_thread_is_running(sysinfo):
    widget, _ = sysinfo

    assert widget.sysret_thread.isRunning()

def test_sysinfo_controller_moved_to_thread(sysinfo):
    widget, mock_ctrl = sysinfo

    mock_ctrl.moveToThread.assert_called_once_with(widget.sysret_thread)

def test_ram_labels_update(sysinfo):
    widget, _ = sysinfo

    widget.populate_ram_labels([2, "GB", 8, "GB"])

    assert "Used: 2 GB / 8 GB" in widget.ram_amount.text()

def test_initial_ram_populates_ui(sysinfo):
    widget, _ = sysinfo

    widget.ram_graph = MagicMock()
    widget.ram_legend = MagicMock()

    widget.populate_initial_ram_info(
        [2, "GiB", 8, "GiB"],
        [1, "GiB", 4, "GiB"],
        2.0,
        1.0,
        8.0
    )

    widget.ram_graph.init_plots.assert_called()
    widget.ram_graph.plotter.assert_called()

    assert widget.ram_amount.text() == "Used: 2 GiB / 8 GiB"
    assert widget.swap_amount.text() == "Swap used: 1 GiB / 4 GiB"

def test_initial_ram_populates_ui_no_swap(sysinfo):
    widget, _ = sysinfo

    widget.ram_graph = MagicMock()
    widget.ram_legend = MagicMock()

    widget.populate_initial_ram_info(
        [2, "GiB", 8, "GiB"],
        [0.0, "GiB", 0.0, "GiB"],
        2.0,
        1.0,
        8.0
    )

    assert widget.swap_amount.text() == "Swap disabled."

def test_cpu_info_updates(sysinfo):
    widget, _ = sysinfo

    widget.cpu_graph = MagicMock()
    widget.cpu_legend = MagicMock()

    widget.populate_cpu_info("Ryzen 5 5600", 6, 12)

    assert "Ryzen 5 5600" in widget.cpu_name.text()
    assert "6 cores, 12 threads" in widget.cpu_core_count.text()

    widget.cpu_graph.init_plots.assert_called()

def test_cpu_freq_plot(sysinfo):
    widget, _ = sysinfo

    widget.cpu_graph = MagicMock()

    widget.populate_cpu_freqs(45.0, [10, 20, 30])

    widget.cpu_graph.plotter.assert_called_with([10, 20, 30], 100.0)

def test_network_info(sysinfo):
    widget, _ = sysinfo

    widget.network_graph = MagicMock()
    widget.network_legend = MagicMock()

    widget.populate_network_info("eth0", "192.168.0.10")

    assert "eth0" in widget.network_active_interface.text()
    assert "192.168.0.10" in widget.network_local_ip.text()

def test_network_traffic(sysinfo, monkeypatch):
    widget, _ = sysinfo

    widget.network_graph = MagicMock()

    monkeypatch.setattr(
        "archcentral.helpers.unitconverter.unit_converter",
        lambda x, as_tuple=False: f"{x}KB"
    )

    widget.populate_network_traffic(1024, 2*1024**2)

    assert "Network traffic: 1.00 KiB/s UP, 2.00 MiB/s DOWN" in widget.network_traffic_label.text()

    widget.network_graph.plotter.assert_called()

def test_system_info(sysinfo):
    widget, _ = sysinfo

    widget.populate_system_info("6.8.1", "archbox")

    assert "6.8.1" in widget.kernelver_label.text()
    assert "archbox" in widget.hostname.text()

def test_de_info(sysinfo):
    widget, _ = sysinfo

    widget.populate_de_info("Xfwm4", "XFCE", "X11", "en_US")

    assert "Xfwm4" in widget.wm_label.text()
    assert "XFCE" in widget.de_label.text()
    assert "X11" in widget.ds.text()

def test_build_info(sysinfo):
    widget, _ = sysinfo

    widget.populate_archcentral_build_info("3.11", "6.5")

    assert "3.11" in widget.pythonver_label.text()
    assert "6.5" in widget.pysidever_label.text()

def test_public_ip(sysinfo):
    widget, _ = sysinfo

    widget.show_public_ip("1.1.1.1", "2001::1")

    assert "1.1.1.1" in widget.network_public_ip.text()
    assert "2001::1" in widget.network_public_ip.text()
    assert not widget.network_public_ip_switch.isVisible()

def test_cleanup_stops_thread(sysinfo):
    widget, _ = sysinfo

    widget.cleanup_thread()

    assert not widget.sysret_thread.isRunning()
