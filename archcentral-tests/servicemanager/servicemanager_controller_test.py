import pytest
from unittest.mock import MagicMock, patch
from archcentral.controllers.servicemanager_controller import ServiceManagerController

@pytest.fixture
def controller():
    with patch("archcentral.controllers.servicemanager_controller.SystemBus"), \
         patch("archcentral.controllers.servicemanager_controller.SessionBus"):

        ctrl = ServiceManagerController()

        # prevent real dbus usage in tests
        ctrl.system_bus.get = MagicMock()
        ctrl.user_bus.get = MagicMock()

        return ctrl

def test_acquire_systemctl_success(controller):
    result = controller._acquire_systemctl()

    assert result is True

def test_acquire_systemctl_fails_when_locked(controller):
    controller._acquire_systemctl()

    result = controller._acquire_systemctl()

    assert result is False

def test_release_systemctl_emits_signal(controller):
    emitted = []
    controller.systemctl_lock_deactivated.connect(lambda: emitted.append(True))

    controller._acquire_systemctl()
    controller._release_systemctl()

    assert emitted[0] is True

@patch("archcentral.controllers.servicemanager_controller.QProcessHandler")
def test_call_systemctl_starts_process(mock_qprocess, controller):
    mock_process = MagicMock()
    mock_qprocess.return_value = mock_process

    controller._acquire_systemctl = MagicMock(return_value=True)

    controller.call_systemctl(
        is_user_unit=False,
        unit="cups.service",
        operation="restart",
        unit_type="service"
    )

    mock_process.start_process.assert_called_once()

    program = mock_process.start_process.call_args[0][0]
    args = mock_process.start_process.call_args[0][1]

    assert "systemctl" == program
    assert "restart" in args
    assert "cups.service" in args

@patch("archcentral.controllers.servicemanager_controller.QProcessHandler")
def test_call_systemctl_user_mode(mock_qprocess, controller):
    mock_process = MagicMock()
    mock_qprocess.return_value = mock_process

    controller._acquire_systemctl = MagicMock(return_value=True)

    controller.call_systemctl(
        is_user_unit=True,
        unit="cups.service",
        operation="start",
        unit_type="service"
    )

    program = mock_process.start_process.call_args[0][0]
    args = mock_process.start_process.call_args[0][1]

    assert "systemctl" == program
    assert "--user" in args
    assert "start" in args

@patch("archcentral.controllers.servicemanager_controller.QProcessHandler")
def test_call_systemctl_fails_if_locked(mock_qprocess, controller):
    controller._acquire_systemctl = MagicMock(return_value=False)

    controller.call_systemctl(
        is_user_unit=False,
        unit="cups.service",
        operation="stop",
        unit_type="service"
    )

    mock_qprocess.return_value.start_process.assert_not_called()

def test_operation_done_triggers_list_units(controller):
    controller.list_units = MagicMock()

    controller.systemctl_operation_done.emit(True, "service")

    controller.list_units.assert_called_once_with(True, True, "service")

def test_list_units_emits_services(controller):
    fake_units = ["unit1", "unit2"]

    controller._acquire_systemctl = MagicMock(return_value=True)
    controller._release_systemctl = MagicMock()
    controller._list_units_internal = MagicMock(return_value=fake_units)

    emitted = []
    controller.services_fetched_for_init.connect(lambda a, b: emitted.append(b))

    controller.list_units(False, False, "service")

    assert emitted[0] == fake_units

def test_list_units_refresh_branch(controller):
    controller._acquire_systemctl = MagicMock(return_value=True)
    controller._release_systemctl = MagicMock()
    controller._list_units_internal = MagicMock(return_value=[])

    init_emitted = []
    refresh_emitted = []

    controller.services_fetched_for_init.connect(lambda a, b: init_emitted.append(True))
    controller.services_fetched_for_refresh.connect(lambda a, b: refresh_emitted.append(True))

    controller.list_units(False, False, "service")  # init
    controller.list_units(True, False, "service")   # refresh

    assert len(init_emitted) == 1
    assert len(refresh_emitted) == 1
