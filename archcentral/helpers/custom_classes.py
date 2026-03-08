from archcentral.helpers.unitconverter import unit_converter

class PacmanPkgInfo():
    """Class that contains package information extracted from the given alpm package object, with additional package manager specifics."""
    def __init__(self, alpm_pkginfo, marked: bool, installed: bool, repo: str) -> None:
        self.marked = marked
        self.installed = installed
        self.repo = repo
        self.name = alpm_pkginfo.name
        self.version = alpm_pkginfo.version
        self.size = alpm_pkginfo.size
        self.isize = alpm_pkginfo.isize
        self.desc = alpm_pkginfo.desc
        self.url = alpm_pkginfo.url
        self.licenses = alpm_pkginfo.licenses
        self.builddate = alpm_pkginfo.builddate
        self.depends = alpm_pkginfo.depends
        self.optdepends = alpm_pkginfo.optdepends
        self.groups = alpm_pkginfo.groups

class SystemdBaseInfo:
    """Base class with common fields for all systemd unit types."""
    def __init__(self, unit, dbus_path) -> None:
        self.unitname = unit.Id
        self.enabledstate = unit.UnitFileState
        self.desc = unit.Description
        self.loadstate = unit.LoadState
        self.activestate = unit.ActiveState
        self.substate = unit.SubState

class SystemdServiceInfo(SystemdBaseInfo):
    """Class that contains systemd Service information."""
    def __init__(self, unit, dbus_path) -> None:
        super().__init__(unit, dbus_path)
        self.type = "service"
        self.cgroup = unit.ControlGroup
        self.dbus_path = dbus_path
        self.memory: str = unit_converter(unit.MemoryCurrent, False)
        self.exec_start = " ".join(unit.ExecStart[0][1]) if unit.ExecStart else "No executable belongs to this service."
        match unit.Result:
            case "success":
                self.result = "Service did not report failure."
            case "resources":
                self.result = "Service couldn't start due to lack of resources."
            case "timeout":
                self.result = "Service timed out."
            case "exit-code":
                self.result = "Service process exited with an unclean exit code."
            case "signal":
                self.result = "Service process exited with an uncaught signal."
            case "core-dump":
                self.result = "Service process exited uncleanly and dumped core."
            case "watchdog":
                self.result = "Service did not send out watchdog ping messages often enough."
            case "start-limit":
                self.result = "Service started too frequently, start limit in effect."
            case _:
                self.result = "Service does not contain a result."

class SystemdTimerInfo(SystemdBaseInfo):
    """Class that contains systemd Timer information."""
    def __init__(self, unit, dbus_path) -> None:
        super().__init__(unit, dbus_path)
        self.type = "timer"
        self.dbus_path = dbus_path
        self.next_trigger = unit.NextElapseUSecRealtime

class SystemdSocketInfo(SystemdBaseInfo):
    """Class that contains systemd Socket information."""
    def __init__(self, unit, dbus_path) -> None:
        super().__init__(unit, dbus_path)
        self.type = "socket"
        self.dbus_path = dbus_path
        self.listen_address = unit.Listen[0][1]

class UserInfo():
    def __init__(self, name, uid, gid, gecos, home, shell) -> None:
        self.name = name
        self.uid = uid
        self.gid = gid
        self.gecos = gecos
        self.home = home
        self.shell = shell

class GroupInfo():
    def __init__(self, name, users) -> None:
        self.name = name
        self.users = users
