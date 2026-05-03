import pytest
from PySide6.QtWidgets import QDialog
from pytestqt.qtbot import QtBot

from archcentral.ui.views.packagemanager import PackageManagerModule

@pytest.fixture
def package_manager(qtbot: QtBot):
    """Create the widget and clean up the thread properly after each test."""
    widget = PackageManagerModule()
    qtbot.addWidget(widget)

    yield widget

    widget.cleanup_thread()

def test_thread_is_running_after_init(package_manager):
    assert package_manager.pmc_thread.isRunning()

def test_pmc_is_in_correct_thread(package_manager):
    assert package_manager.pmc.thread() == package_manager.pmc_thread

def test_cleanup_stops_the_thread(package_manager):
    package_manager.cleanup_thread()
    assert not package_manager.pmc_thread.isRunning()

def test_pacman_package_conflict_signal_opens_conflict_dialog(package_manager, qtbot: QtBot, monkeypatch):
    dialog_opened = False

    def mock_exec(self):
        nonlocal dialog_opened
        dialog_opened = True
        return QDialog.DialogCode.Rejected

    monkeypatch.setattr(
        "archcentral.ui.views.dialogs.pacman_transaction_dialog.PacmanTransactionDialog.exec",
        mock_exec
    )

    package_manager.pmc.pacman_package_conflict.emit("pkg1", "pkg2", "pkg_to_remove")
    qtbot.wait(50)
    assert dialog_opened

def test_indicate_unsupported_multichoice_signal_opens_dialog(package_manager, qtbot: QtBot, monkeypatch):
    dialog_opened = False

    def mock_exec(self):
        nonlocal dialog_opened
        dialog_opened = True
        return QDialog.DialogCode.Accepted

    monkeypatch.setattr(
        "archcentral.ui.views.dialogs.pacman_transaction_dialog.PacmanTransactionDialog.exec",
        mock_exec
    )

    package_manager.pmc.indicate_unsupported_multichoice.emit()
    qtbot.wait(50)
    assert dialog_opened

def test_pacman_lock_activated_disables_buttons_and_sets_status(package_manager, qtbot: QtBot):
    package_manager.pmc.pacman_lock_activated.emit()
    qtbot.wait(10)

    assert package_manager.status_label.text() == "Operation in progress, please wait..."
    assert not package_manager.run_transaction_button.isEnabled()
    assert not package_manager.fetch_update_button.isEnabled()
    assert not package_manager.update_button.isEnabled()


def test_pacman_lock_deactivated_enables_buttons_and_sets_status(package_manager, qtbot: QtBot):
    package_manager.pmc.pacman_lock_activated.emit()
    qtbot.wait(10)

    package_manager.pmc.pacman_lock_deactivated.emit()
    qtbot.wait(10)

    assert package_manager.status_label.text() == "Operation finished..."
    assert package_manager.run_transaction_button.isEnabled()
    assert package_manager.fetch_update_button.isEnabled()
