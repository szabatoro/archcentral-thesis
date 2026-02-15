from PySide6.QtCore import QObject, Signal
from pydbus import SystemBus # using pydbus instead of QtDBus as its more pythonic and far simpler
from archcentral.helpers.custom_classes import SystemdServiceInfo
from threading import Lock
from archcentral.helpers.qprocesshelper import QProcessHandler

SYSTEMD_DBUS_PATH = "org.freedesktop.systemd1"

class ServiceManagerController(QObject):
    # Signals
    services_fetched_for_init: Signal = Signal(list)
    services_fetched_for_refresh: Signal = Signal(list)
    systemctl_lock_activated: Signal = Signal()
    systemctl_lock_deactivated: Signal = Signal()
    systemctl_operation_done: Signal = Signal()

    def __init__(self) -> None:
        super().__init__()

        # Getting the dbus system session bus
        self.system_bus: SystemBus() = SystemBus()

        # Connecting to the systemd dbus API
        self.systemd_system_bus = self.system_bus.get(SYSTEMD_DBUS_PATH)

        # Lock object to prevent native systemctl lock crashing the qprocesses or working with non-up-to-date data
        self.systemctl_lock: Lock = Lock()

        self.systemctl_operation_done.connect(self.list_services_for_refresh)

    def _acquire_systemctl(self) -> bool:
        """Activates the systemctl lock and retuns True, if its already locked it emits a signal and returns False."""
        if self.systemctl_lock.acquire(blocking=False):
            self.systemctl_lock_activated.emit()
            return True
        return False

    def _release_systemctl(self) -> None:
        """Releases the systemctl lock and emits a signal."""
        self.systemctl_lock.release()
        self.systemctl_lock_deactivated.emit()

    def _list_services_internal(self) -> list[SystemdServiceInfo]:
        """Fetches systemd services off the systemd API."""
        unitfiles = self.systemd_system_bus.ListUnitFilesByPatterns([],["*.service"])

        processed_unitlist: list[SystemdServiceInfo] = []

        for unitfile in unitfiles:
            unitname, enabledstate = unitfile
            if enabledstate in ("disabled", "enabled"):
                bare_unitname = unitname.split("/")[-1]
                if "@." not in bare_unitname: # @.service units are template units, and as such can't be loaded
                    unit_dbus_path = self.systemd_system_bus.LoadUnit(bare_unitname)
                    unit = self.system_bus.get(SYSTEMD_DBUS_PATH, unit_dbus_path)
                    processed_unitlist.append(SystemdServiceInfo(unit, unit_dbus_path))

        return processed_unitlist

    def list_services_for_init(self) -> None:
        services: list[SystemdServiceInfo] = self._list_services_internal()
        self.services_fetched_for_init.emit(services)

    def list_services_for_refresh(self) -> None:
        services: list[SystemdServiceInfo] = self._list_services_internal()
        self.services_fetched_for_refresh.emit(services)

    def call_systemctl(self, unit: str, operation: str) -> None:
        """
        Calls systemctl.

        Arguments:
            - unit: Name of the unit. Eg: "cups.service", ".service" can be omitted.
            - operation: The type of operation systemctl runs. "enable", "disable", "start", "stop", "restart"
        """
        if not self._acquire_systemctl():
            return None

        self.systemctl_worker: QProcessHandler = QProcessHandler()
        self.systemctl_worker.finished.connect(self._release_systemctl)
        self.systemctl_worker.finished.connect(lambda: self.systemctl_operation_done.emit())
        self.systemctl_worker.start_process("systemctl", [operation, unit])
