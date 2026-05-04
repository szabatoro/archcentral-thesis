import pytest
from unittest.mock import MagicMock, patch
from archcentral.controllers.packagemanager_controller import PackageManagerController

@pytest.fixture
def controller():
    with patch("builtins.open", MagicMock()), \
         patch("archcentral.controllers.packagemanager_controller.re.findall", return_value=["core"]):

        return PackageManagerController()

@pytest.fixture
def mock_process():
    with patch("archcentral.controllers.packagemanager_controller.QProcessHandler") as mock_cls:
        process = MagicMock()
        mock_cls.return_value = process
        yield process

@pytest.mark.parametrize(
    "line,expected_signal",
    [
        (":: Proceed with installation? [Y/n]", "y\n"),
        (":: Do you want to remove these packages? [Y/n]", "y\n"),
    ],
)
def test_pacman_prompts_emit_yes(controller, line, expected_signal):
    emitted = []
    controller.write_to_stdin.connect(lambda x: emitted.append(x))

    controller._handle_pacman_prompts(line)

    assert expected_signal in emitted

def test_conflict_emits_signal(controller):
    captured = []
    controller.pacman_package_conflict.connect(lambda a, b, c: captured.append((a, b, c)))

    line = ":: pkg1 and pkg2 are in conflict. Remove pkg1?"
    controller._handle_pacman_prompts(line)

    assert captured[0] == ("pkg1", "pkg2", "pkg1")

@patch("archcentral.controllers.packagemanager_controller.QProcessHandler")
def test_fetch_updates_starts_process(mock_qprocess, controller):
    mock_process = MagicMock()
    mock_qprocess.return_value = mock_process

    controller._acquire_pacman = MagicMock(return_value=True)
    controller._release_pacman = MagicMock()
    controller._get_update_list_fr = MagicMock()

    controller.fetch_updates()

    mock_process.start_process.assert_called_once_with(
        "pkexec",
        ["pacman", "-Sy"]
    )

@patch("archcentral.controllers.packagemanager_controller.pyalpm.Handle")
def test_get_update_list_emits_packages(mock_handle, controller):

    mock_local_pkg = MagicMock()
    mock_local_pkg.name = "pkg"
    mock_local_pkg.version = "1.0"

    mock_sync_pkg = MagicMock()
    mock_sync_pkg.name = "pkg"
    mock_sync_pkg.version = "2.0"
    mock_sync_pkg.size = 10737418

    mock_db = MagicMock()
    mock_db.pkgcache = [mock_sync_pkg]
    mock_db.get_pkg.return_value = mock_sync_pkg

    handle_instance = MagicMock()
    handle_instance.get_localdb.return_value.pkgcache = [mock_local_pkg]
    handle_instance.get_syncdbs.return_value = [mock_db]

    mock_handle.return_value = handle_instance

    emitted = []
    controller.update_fetched.connect(lambda x: emitted.append(x))

    controller._get_update_list_fr()

    assert len(emitted) == 1
    updates = emitted[0]

    assert len(updates) > 0

    # tuple-based validation
    name, old_version, new_version, update_size = updates[0]

    assert name == "pkg"
    assert old_version == "1.0"
    assert new_version == "2.0"
    assert update_size == 10737418

@pytest.mark.parametrize(
    "packages,mode",
    [
        (["vim", False], "install"),
        (["firefox", True], "remove"),
        (["vim", False], "both_vim_firefox"),
    ],
)
def test_run_package_transaction(controller, mock_process, packages, mode):

    controller._acquire_pacman = MagicMock(return_value=True)

    if mode == "install":
        controller.run_package_transaction([["vim", False]])

        args = mock_process.start_process.call_args[0][1]
        assert "-S" in args
        assert "vim" in args
        assert "-Rns" not in args

    elif mode == "remove":
        controller.run_package_transaction([["firefox", True]])

        args = mock_process.start_process.call_args[0][1]
        assert "-Rns" in args
        assert "firefox" in args
        assert "-S" not in args

    elif mode == "both_vim_firefox":
        controller.run_package_transaction([
            ["vim", False],
            ["firefox", True]
        ])

        args = mock_process.start_process.call_args[0][1]

        assert "sh" in args
        assert "-c" in args

        cmd = args[-1]
        assert "pacman -S vim" in cmd
        assert "pacman -Rns firefox" in cmd

def test_cancel_transaction_emits_signal(controller):
    emitted = []
    controller.send_sigint_to_transaction.connect(lambda: emitted.append(True))

    controller.cancel_transaction()

    assert emitted[0] is True
