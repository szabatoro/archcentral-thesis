from PySide6.QtCore import QObject, Signal
from pydbus import SystemBus # using pydbus instead of QtDBus as its more pythonic and far simpler
from archcentral.helpers.custom_classes import SystemdServiceInfo

class ServiceManagerController(QObject):
    # Signals
    services_fetched: Signal = Signal(list)

    def __init__(self) -> None:
        super().__init__()

        # Getting the dbus system session bus
        self.system_bus: SystemBus() = SystemBus()

        # Connecting to the systemd dbus API
        self.systemd_system_bus = self.system_bus.get("org.freedesktop.systemd1")

    def list_services(self):
        """Fetches systemd services off the systemd API."""
        unitlist: [list[SystemdServiceInfo]] = []
        for unit in self.systemd_system_bus.ListUnitsByPatterns([],["*.service"]):
            unitname, desc, loadstate, activestate, substate, unitfollowed, objpath, queued, jobtype, jobpath = unit
            unitlist.append(SystemdServiceInfo(unitname, desc, activestate, substate))

        self.services_fetched.emit(unitlist)
