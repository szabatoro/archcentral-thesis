import pytest
from unittest.mock import MagicMock, patch
from PySide6.QtCore import Qt
from archcentral.ui.views.servicemanager import ServiceManagerModule

@pytest.fixture
def service_manager(qtbot):
    with patch("archcentral.ui.views.servicemanager.ServiceManagerController") as mock_ctrl_cls, \
         patch("archcentral.ui.views.servicemanager.QThread") as mock_thread_cls:

        mock_ctrl = MagicMock()
        mock_ctrl.moveToThread = MagicMock()
        mock_ctrl_cls.return_value = mock_ctrl

        mock_thread = MagicMock()
        mock_thread.isRunning.return_value = False
        mock_thread_cls.return_value = mock_thread

        widget = ServiceManagerModule()
        qtbot.addWidget(widget)

        yield widget, mock_ctrl

        widget.cleanup_thread()

def test_get_selected_row_system(service_manager):
    widget, _ = service_manager

    widget.user_system_tab.setCurrentIndex(0)

    widget.system_unit_list_table = MagicMock()
    widget.system_unit_list_proxy_model = MagicMock()
    widget.system_unit_list_model = MagicMock()

    mock_index = MagicMock()
    mapped_index = MagicMock()
    mock_unit = MagicMock()

    widget.system_unit_list_table.currentIndex.return_value = mock_index
    widget.system_unit_list_proxy_model.mapToSource.return_value = mapped_index
    widget.system_unit_list_model.get_unit.return_value = mock_unit

    result = widget._get_selected_row()

    assert result == (mock_unit, False)

    widget.system_unit_list_proxy_model.mapToSource.assert_called_once_with(mock_index)
    widget.system_unit_list_model.get_unit.assert_called_once_with(mapped_index)

def test_get_selected_row_user(service_manager):
    widget, _ = service_manager

    widget.user_system_tab.setCurrentIndex(1)

    widget.user_unit_list_table = MagicMock()
    widget.user_unit_list_proxy_model = MagicMock()
    widget.user_unit_list_model = MagicMock()

    mock_index = MagicMock()
    mapped_index = MagicMock()
    mock_unit = MagicMock()

    widget.user_unit_list_table.currentIndex.return_value = mock_index
    widget.user_unit_list_proxy_model.mapToSource.return_value = mapped_index
    widget.user_unit_list_model.get_unit.return_value = mock_unit

    result = widget._get_selected_row()

    assert result == (mock_unit, True)

    widget.user_unit_list_proxy_model.mapToSource.assert_called_once_with(mock_index)
    widget.user_unit_list_model.get_unit.assert_called_once_with(mapped_index)

def test_adapt_buttons_active(service_manager):
    widget, _ = service_manager

    widget._get_selected_row = MagicMock(return_value=(
        MagicMock(activestate="active", enabledstate="enabled"),
        False
    ))

    widget._adapt_buttons_status()

    assert widget.start_stop_button.text() == "Stop"
    assert widget.restart_button.isEnabled()
    assert widget.enable_disable_button.text() == "Disable"

def test_adapt_buttons_inactive(service_manager):
    widget, _ = service_manager

    widget._get_selected_row = MagicMock(return_value=(
        MagicMock(activestate="inactive", enabledstate="disabled"),
        False
    ))

    widget._adapt_buttons_status()

    assert widget.start_stop_button.text() == "Start"
    assert not widget.restart_button.isEnabled()
    assert widget.enable_disable_button.text() == "Enable"

def test_interface_lock(service_manager):
    widget, _ = service_manager

    widget.interface_lock()

    assert not widget.enable_disable_button.isEnabled()
    assert not widget.restart_button.isEnabled()
    assert not widget.start_stop_button.isEnabled()
    assert not widget.unit_types_box.isEnabled()
    assert "progress" in widget.status_label.text()

def test_interface_unlock(service_manager):
    widget, _ = service_manager

    widget.interface_unlock()

    assert widget.enable_disable_button.isEnabled()
    assert widget.restart_button.isEnabled()
    assert widget.start_stop_button.isEnabled()
    assert widget.unit_types_box.isEnabled()
    assert "finished" in widget.status_label.text()

def test_handle_unit_type_services(service_manager):
    widget, mock_ctrl = service_manager

    widget.handle_unit_type_selection("Services")

    assert mock_ctrl.list_units.call_count == 4

def test_handle_unit_type_timers(service_manager):
    widget, mock_ctrl = service_manager

    widget.handle_unit_type_selection("Timers")

    assert mock_ctrl.list_units.call_count == 4

def test_handle_unit_type_sockets(service_manager):
    widget, mock_ctrl = service_manager

    widget.handle_unit_type_selection("Sockets")

    assert mock_ctrl.list_units.call_count == 4

def test_initialize_models_user(service_manager):
    widget, _ = service_manager

    mock_units = ["unit1", "unit2"]

    with patch("archcentral.ui.views.servicemanager.SystemdUnitListModel") as mock_model_cls, \
         patch("archcentral.ui.views.servicemanager.QSortFilterProxyModel") as mock_proxy_cls:

        mock_model = MagicMock()
        mock_proxy = MagicMock()

        mock_model_cls.return_value = mock_model
        mock_proxy_cls.return_value = mock_proxy

        mock_selection_model = MagicMock()
        widget.user_unit_list_table = MagicMock()
        widget.user_unit_list_table.selectionModel.return_value = mock_selection_model

        widget.initalize_models(True, mock_units)

        mock_model_cls.assert_called_once_with(mock_units)

        mock_proxy.setDynamicSortFilter.assert_called_once_with(True)
        mock_proxy.setFilterCaseSensitivity.assert_called_once_with(Qt.CaseSensitivity.CaseInsensitive)
        mock_proxy.setSortCaseSensitivity.assert_called_once_with(Qt.CaseSensitivity.CaseInsensitive)
        mock_proxy.sort.assert_called_once_with(0, Qt.AscendingOrder)
        mock_proxy.setSourceModel.assert_called_once_with(mock_model)
        mock_proxy.setFilterKeyColumn.assert_called_once_with(0)

        widget.user_unit_list_table.setModel.assert_called_once_with(mock_proxy)

        assert mock_selection_model.currentRowChanged.connect.call_count == 2

def test_initialize_models_system(service_manager):
    widget, _ = service_manager

    mock_units = ["unit1", "unit2"]

    with patch("archcentral.ui.views.servicemanager.SystemdUnitListModel") as mock_model_cls, \
         patch("archcentral.ui.views.servicemanager.QSortFilterProxyModel") as mock_proxy_cls:

        mock_model = MagicMock()
        mock_proxy = MagicMock()

        mock_model_cls.return_value = mock_model
        mock_proxy_cls.return_value = mock_proxy

        mock_selection_model = MagicMock()
        widget.system_unit_list_table = MagicMock()
        widget.system_unit_list_table.selectionModel.return_value = mock_selection_model

        widget.initalize_models(False, mock_units)

        mock_model_cls.assert_called_once_with(mock_units)

        mock_proxy.setDynamicSortFilter.assert_called_once_with(True)
        mock_proxy.setFilterCaseSensitivity.assert_called_once_with(Qt.CaseSensitivity.CaseInsensitive)
        mock_proxy.setSortCaseSensitivity.assert_called_once_with(Qt.CaseSensitivity.CaseInsensitive)
        mock_proxy.sort.assert_called_once_with(0, Qt.AscendingOrder)
        mock_proxy.setSourceModel.assert_called_once_with(mock_model)
        mock_proxy.setFilterKeyColumn.assert_called_once_with(0)

        widget.system_unit_list_table.setModel.assert_called_once_with(mock_proxy)

        assert mock_selection_model.currentRowChanged.connect.call_count == 2

def test_refresh_unit_list_user(service_manager):
    widget, _ = service_manager

    widget.user_unit_list_model = MagicMock()
    widget.system_unit_list_model = MagicMock()

    services = ["svc1", "svc2"]

    widget.refresh_unit_list(True, services)

    widget.user_unit_list_model.refresh.assert_called_once_with(services)
    widget.system_unit_list_model.refresh.assert_not_called()

def test_refresh_unit_list_system(service_manager):
    widget, _ = service_manager

    widget.user_unit_list_model = MagicMock()
    widget.system_unit_list_model = MagicMock()

    services = ["svc1", "svc2"]

    widget.refresh_unit_list(False, services)

    widget.system_unit_list_model.refresh.assert_called_once_with(services)
    widget.user_unit_list_model.refresh.assert_not_called()

def test_refresh_without_models(service_manager):
    widget, _ = service_manager

    with pytest.raises(AttributeError):
        widget.refresh_unit_list(True, [])

def get_tree_items(widget):
    return [
        (widget.unit_details_tree.topLevelItem(i).text(0),
         widget.unit_details_tree.topLevelItem(i).text(1))
        for i in range(widget.unit_details_tree.topLevelItemCount())
    ]

def test_fill_unit_details_service_basic(service_manager):
    widget, _ = service_manager

    mock_unit = MagicMock(
        unitname="nginx.service",
        desc="Web server",
        type="service",
        exec_start="/usr/bin/nginx",
        result="success",
        substate="dead"
    )

    widget._get_selected_row = MagicMock(return_value=(mock_unit, False))

    widget.fill_unit_details()

    items = get_tree_items(widget)

    assert ("Name: ", "nginx.service") in items
    assert ("Description: ", "Web server") in items
    assert ("Executable: ", "/usr/bin/nginx") in items
    assert ("Result: ", "success") in items

    assert not any("Used memory:" in i[0] for i in items)

def test_fill_unit_details_service_running(service_manager):
    widget, _ = service_manager

    mock_unit = MagicMock(
        unitname="nginx.service",
        desc="Web server",
        type="service",
        exec_start="/usr/bin/nginx",
        result="success",
        substate="running",
        memory="10M",
        cgroup="/system.slice/nginx.service"
    )

    widget._get_selected_row = MagicMock(return_value=(mock_unit, False))

    widget.fill_unit_details()

    items = get_tree_items(widget)

    assert ("Used memory: ", "10M") in items
    assert ("CGroup: ", "/system.slice/nginx.service") in items

def test_fill_unit_details_timer_waiting(service_manager):
    widget, _ = service_manager

    mock_unit = MagicMock(
        unitname="backup.timer",
        desc="Backup job",
        type="timer",
        substate="waiting",
        next_trigger=1_000_000
    )

    widget._get_selected_row = MagicMock(return_value=(mock_unit, False))

    widget.fill_unit_details()

    items = get_tree_items(widget)

    assert ("Name: ", "backup.timer") in items

    assert any("Next Trigger:" in i[0] for i in items)

def test_fill_unit_details_socket(service_manager):
    widget, _ = service_manager

    mock_unit = MagicMock(
        unitname="docker.socket",
        desc="Docker socket",
        type="socket",
        listen_address="/run/docker.sock"
    )

    widget._get_selected_row = MagicMock(return_value=(mock_unit, False))

    widget.fill_unit_details()

    items = get_tree_items(widget)

    assert ("Listen address: ", "/run/docker.sock") in items

def test_start_stop_unit_active(service_manager, qtbot):
    widget, _ = service_manager

    mock_unit = MagicMock(
        activestate="active",
        unitname="nginx.service",
        type="service"
    )
    widget._get_selected_row = MagicMock(return_value=(mock_unit, False))

    with qtbot.waitSignal(widget.systemctl_operation_signal) as blocker:
        widget.start_stop_unit()

    assert blocker.args == [False, "nginx.service", "stop", "service"]


def test_start_stop_unit_inactive(service_manager, qtbot):
    widget, _ = service_manager

    mock_unit = MagicMock(
        activestate="inactive",
        unitname="nginx.service",
        type="service"
    )
    widget._get_selected_row = MagicMock(return_value=(mock_unit, True))

    with qtbot.waitSignal(widget.systemctl_operation_signal) as blocker:
        widget.start_stop_unit()

    assert blocker.args == [True, "nginx.service", "start", "service"]

def test_enable_disable_unit(service_manager, qtbot):
    widget, _ = service_manager

    mock_unit = MagicMock(
        enabledstate="enabled",
        unitname="nginx.service",
        type="service"
    )
    widget._get_selected_row = MagicMock(return_value=(mock_unit, True))

    with qtbot.waitSignal(widget.systemctl_operation_signal) as blocker:
        widget.enable_disable_unit()

    assert blocker.args == [True, "nginx.service", "disable", "service"]

def test_restart_unit(service_manager, qtbot):
    widget, _ = service_manager

    mock_unit = MagicMock(
        unitname="nginx.service",
        type="service"
    )

    widget._get_selected_row = MagicMock(return_value=(mock_unit, True))

    with qtbot.waitSignal(widget.systemctl_operation_signal) as blocker:
        widget.restart_unit()

    assert blocker.args == [True, "nginx.service", "restart", "service"]

def test_cleanup_thread_running(service_manager):
    widget, _ = service_manager

    widget.smc_thread = MagicMock()
    widget.smc_thread.isRunning.return_value = True

    widget.cleanup_thread()

    widget.smc_thread.quit.assert_called_once()
    widget.smc_thread.wait.assert_called_once()

def test_cleanup_thread_not_running(service_manager):
    widget, _ = service_manager

    widget.smc_thread = MagicMock()
    widget.smc_thread.isRunning.return_value = False

    widget.cleanup_thread()

    widget.smc_thread.quit.assert_not_called()
    widget.smc_thread.wait.assert_not_called()
