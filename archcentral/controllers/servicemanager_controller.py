from PySide6.QtCore import QObject, Signal
from pydbus import SessionBus, SystemBus # using pydbus instead of QtDBus as its more pythonic and far simpler
from archcentral.helpers.custom_classes import SystemdServiceInfo
from threading import Lock
from archcentral.helpers.qprocesshelper import QProcessHandler

SYSTEMD_DBUS_PATH = "org.freedesktop.systemd1"

class ServiceManagerController(QObject):
    # Signals
    services_fetched_for_init: Signal = Signal(bool, list)
    services_fetched_for_refresh: Signal = Signal(bool, list)
    systemctl_lock_activated: Signal = Signal()
    systemctl_lock_deactivated: Signal = Signal()
    systemctl_operation_done: Signal = Signal()

    def __init__(self) -> None:
        super().__init__()

        # Getting the dbus system session bus
        self.system_bus: SystemBus = SystemBus()
        self.user_bus: SessionBus = SessionBus()

        # Connecting to the systemd system and user level dbus API
        self.systemd_system_bus = self.system_bus.get(SYSTEMD_DBUS_PATH)
        self.systemd_user_bus = self.user_bus.get(SYSTEMD_DBUS_PATH)

        # Lock object to prevent native systemctl lock crashing the qprocesses or working with non-up-to-date data
        self.systemctl_lock: Lock = Lock()

        self.systemctl_operation_done.connect(self.list_system_services_for_refresh)

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

    def _list_services_internal(self, is_system_level: bool) -> list[SystemdServiceInfo]:
        """Fetches systemd services off the systemd API."""
        bus = self.system_bus if is_system_level else self.user_bus
        systemd_bus = self.systemd_system_bus if is_system_level else self.systemd_user_bus
        unitfiles = systemd_bus.ListUnitFilesByPatterns([],["*.service"])

        processed_unitlist: list[SystemdServiceInfo] = []

        for unitfile in unitfiles:
            unitname, enabledstate = unitfile
            if enabledstate in ("disabled", "enabled"):
                bare_unitname = unitname.split("/")[-1]
                if "@." not in bare_unitname: # @.service units are template units, and as such can't be loaded
                    unit_dbus_path = systemd_bus.LoadUnit(bare_unitname)
                    unit = bus.get(SYSTEMD_DBUS_PATH, unit_dbus_path)
                    processed_unitlist.append(SystemdServiceInfo(unit, unit_dbus_path))

        return processed_unitlist

    def list_system_services_for_init(self) -> None:
        system_services: list[SystemdServiceInfo] = self._list_services_internal(True)
        self.services_fetched_for_init.emit(True, system_services)
        user_services: list[SystemdServiceInfo] = self._list_services_internal(False)
        self.services_fetched_for_init.emit(False, user_services)

    def list_system_services_for_refresh(self) -> None:
        services: list[SystemdServiceInfo] = self._list_services_internal(True)
        self.services_fetched_for_refresh.emit(True, services)
        user_services: list[SystemdServiceInfo] = self._list_services_internal(False)
        self.services_fetched_for_init.emit(False, user_services)

    def call_systemctl(self, is_user_service: bool, unit: str, operation: str) -> None:
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
        systemctl_args = ["--user", operation, unit] if is_user_service else [operation, unit]
        self.systemctl_worker.start_process("systemctl", systemctl_args)
