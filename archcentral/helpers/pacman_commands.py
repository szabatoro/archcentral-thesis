from PySide6.QtCore import QObject,  Signal
from archcentral.helpers.qprocesshelper import QProcessHandler
import pyalpm
import re

class PacmanManager(QObject):
    finished_fetch: Signal = Signal(list)
    running_update: Signal = Signal(str)

    def __init__(self) -> None:
        super().__init__()

        # Read the pacman config file
        self.pacman_conf = open("/etc/pacman.conf", "r")
        self.pacman_conf_str: str = self.pacman_conf.read()
        self.pacman_conf.close()

        # Extract enabled repos from pacman config
        self.enabled_repos = re.findall(r'^(?!#)(?!.*option)\[(.*)\]$', self.pacman_conf_str, re.MULTILINE)

        # Initialize handle and get localdb
        self.handle = pyalpm.Handle(".", "/var/lib/pacman")
        self.localdb = self.handle.get_localdb()

        # Load remote repository dbs
        for repo in self.enabled_repos:
            self.handle.register_syncdb(f"{repo}", pyalpm.SIG_DATABASE_OPTIONAL)
        self.syncdbs = self.handle.get_syncdbs()

    # fetches latest package info from mirrors
    def fetch(self) -> None:
        """
        Fetches latest package info from mirrors, lists updateable packages and emits them with the finished_fetch signal.
        """
        self.pacman_worker = QProcessHandler()
        self.pacman_worker.finished.connect(self._get_update_list_fr)
        self.pacman_worker.start_process("pkexec", ["pacman", "-Sy"])

    # Finds updateable packages using pyalpm
    def _get_update_list_fr(self) -> None:
        updateable_packages: list[tuple[str,str,str]] = []
        for pkg in self.localdb.pkgcache:
            for db in self.syncdbs:
                sync_pkg = db.get_pkg(pkg.name)
                if sync_pkg:
                    if pyalpm.vercmp(sync_pkg.version, pkg.version) == 1:
                        updateable_packages.append((pkg.name, pkg.version, sync_pkg.version, sync_pkg.size))
                    break
        self.finished_fetch.emit(updateable_packages)

    def update(self, packagelist) -> None:
        """
        Runs pacman -S with the specified packages, updating the system.
        """
        self.pacman_worker: QProcessHandler = QProcessHandler()
        self.pacman_worker.stream.connect(self.running_update.emit)
        #self.pacman_worker.start_process("pkexec", ["pacman", "-S", "--noconfirm", "hplip"]) # testing
        self.pacman_worker.start_process("pkexec", ["pacman", "-S", "--noconfirm"] + packagelist)
