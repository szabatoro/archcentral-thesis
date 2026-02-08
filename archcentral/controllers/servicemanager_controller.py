from PySide6.QtCore import QObject
from pydbus import SessionBus # using pydbus instead of QtDBus as its far simpler

class ServiceManagerController(QObject):
    def __init__(self) -> None:
        super().__init__()

        # Getting the dbus user session bus
        self.session_bus: SessionBus() = SessionBus()

        # Connecting to the systemd dbus API
        self.systemd_user_bus = self.session_bus.get("org.freedesktop.systemd1")
