from PySide6.QtCore import QObject,  Signal
from archcentral.helpers.qprocesshelper import QProcessHandler
from archcentral.helpers.custom_classes import PacmanPkgInfo
import pyalpm
import re
from threading import Lock

class PackageManagerController(QObject):
    # Signals
    package_list_fetched_for_init: Signal = Signal(list)
    package_list_fetched_for_refresh: Signal = Signal(list)
    update_fetched: Signal = Signal(list)
    update_stdout_stream: Signal = Signal(str)
    update_finished: Signal = Signal()
    transaction_started: Signal = Signal()
    transaction_stdout_stream: Signal = Signal(str)
    transaction_finished: Signal = Signal()
    pacman_lock_activated: Signal = Signal()
    pacman_lock_deactivated: Signal = Signal()
    write_to_stdin: Signal = Signal(str)
    pacman_package_conflict: Signal = Signal(str, str, str)

    def __init__(self) -> None:
        super().__init__()

        # Read the pacman config file
        self.pacman_conf = open("/etc/pacman.conf", "r")
        self.pacman_conf_str: str = self.pacman_conf.read()
        self.pacman_conf.close()

        # Extract enabled repos from pacman config
        self.enabled_repos = re.findall(r'^(?!#)(?!.*option)\[(.*)\]$', self.pacman_conf_str, re.MULTILINE)

        # Lock object to prevent native pacman lock crashing the qprocesses or working with non-up-to-date data
        self.pacman_lock: Lock = Lock()

        self.transaction_stdout_stream.connect(self._handle_pacman_prompts)
        self.update_stdout_stream.connect(self._handle_pacman_prompts)

    def _acquire_pacman(self) -> bool:
        """Activates the pacman lock and retuns True, if its already locked it emits a signal and returns False."""
        if self.pacman_lock.acquire(blocking=False):
            self.pacman_lock_activated.emit()
            return True
        return False

    def _release_pacman(self):
        """Releases the pacman lock and emits a signal."""
        self.pacman_lock.release()
        self.pacman_lock_deactivated.emit()

    def _fetch_dbs(self) -> None:
        """
        Fetches the local and repo package databases.
        """

        # Initialize handle and get localdb
        self.handle = pyalpm.Handle(".", "/var/lib/pacman")
        self.localdb = self.handle.get_localdb()

        # Load remote repository dbs
        for repo in self.enabled_repos:
            self.handle.register_syncdb(f"{repo}", pyalpm.SIG_DATABASE_OPTIONAL)
        self.syncdbs = self.handle.get_syncdbs()

    # fetches latest package info from mirrors
    def fetch_updates(self) -> None:
        """
        Fetches latest package info from mirrors, lists updateable packages and emits them with the update_fetched signal.
        """
        if not self._acquire_pacman():
            return None
        try:
            self.pacman_fetch_worker = QProcessHandler()
            self.pacman_fetch_worker.finished.connect(self._release_pacman)
            self.pacman_fetch_worker.finished.connect(self._get_update_list_fr)
            self.pacman_fetch_worker.start_process("pkexec", ["pacman", "-Sy"])
        except:
            self._release_pacman()
            raise

    def _get_update_list_fr(self) -> None:
        """Finds updateable packages using pyalpm and retuns them via the update_fetched signal."""
        self._fetch_dbs()
        updateable_packages: list[tuple[str,str,str,str]] = []
        for pkg in self.localdb.pkgcache:
            for db in self.syncdbs:
                sync_pkg = db.get_pkg(pkg.name)
                if sync_pkg:
                    if pyalpm.vercmp(sync_pkg.version, pkg.version) == 1:
                        updateable_packages.append((pkg.name, pkg.version, sync_pkg.version, sync_pkg.size))
                    break
        self.update_fetched.emit(updateable_packages)

    def perform_update(self, packagelist) -> None:
        """
        Runs pacman -S with the specified packages, updating the system.
        """
        if not self._acquire_pacman():
            return None
        self.pacman_update_worker: QProcessHandler = QProcessHandler()
        self.pacman_update_worker.finished.connect(self._release_pacman)
        self.pacman_update_worker.finished.connect(lambda: self.update_finished.emit())
        self.pacman_update_worker.finished.connect(lambda: self._fetch_dbs())
        self.pacman_update_worker.stream.connect(self.update_stdout_stream.emit)
        self.write_to_stdin.connect(self.pacman_update_worker.write_to_stdin)
        try:
            #self.pacman_worker.start_process("pkexec", ["pacman", "-S", "--noconfirm", "hplip"]) # testing
            self.pacman_update_worker.start_process("pkexec", ["pacman", "-S"] + packagelist)
        except:
            self._release_pacman()
            raise

    def _list_all_packages_internal(self):
        """
        Fetch a list of every repo package.
        """
        self._fetch_dbs()
        pkg_list: list[tuple[str,str,str,str,str]] = []
        for db in self.syncdbs:
            for pkg in db.pkgcache:
                local_pkg = self.localdb.get_pkg(pkg.name)
                if local_pkg:
                    pkg_list.append(PacmanPkgInfo(local_pkg, False, True, db.name))
                else:
                    pkg_list.append(PacmanPkgInfo(pkg, False, False, db.name))

        return pkg_list

    def list_all_packages_for_init(self) -> None:
        """Runs at start."""
        packages = self._list_all_packages_internal()
        self.package_list_fetched_for_init.emit(packages)

    def list_all_packages_for_refresh(self) -> None:
        """Runs when only a model refresh is needed."""
        packages = self._list_all_packages_internal()
        self.package_list_fetched_for_refresh.emit(packages)

    def _handle_pacman_prompts(self, line: str) -> None:
        install_prompt = ":: Proceed with installation? [Y/n]"
        remove_prompt = ":: Do you want to remove these packages? [Y/n]"

        if install_prompt in line:
            self.write_to_stdin.emit("y\n")
        if remove_prompt in line:
            self.write_to_stdin.emit("y\n")

        conflict_pattern = r":: (\S+) and (\S+) are in conflict\. Remove (\S+)\?"
        match = re.search(conflict_pattern, line)
        if match:
            package1, package2, to_remove = match.groups()
            self.pacman_package_conflict.emit(package1, package2, to_remove)

    def decide_pacman_conflict(self, choice: bool) -> None:
        self.write_to_stdin.emit("y\n" if choice else "n\n")

    def run_package_transaction(self, packagelist: list[list[str,bool]]) -> None:
        """
        Runs the pacman package manager directly and installs/removes packages depending on their flags.
        Arguments:
            packagelist: list of packages marked of transaction in the following format: [package_name(str), install_status(bool)]
        """
        if not packagelist:
            return None
        if not self._acquire_pacman():
            return None

        pkg_install: list[str] = []
        pkg_remove: list[str] = []
        for pkg in packagelist:
            if pkg[1]:
                pkg_remove.append(pkg[0])
            elif not pkg[1]:
                pkg_install.append(pkg[0])

        try:
            self.pacman_transaction_worker: QProcessHandler = QProcessHandler()
            self.pacman_transaction_worker.started.connect(self.transaction_started.emit)
            self.pacman_transaction_worker.finished.connect(self._release_pacman)
            self.pacman_transaction_worker.finished.connect(lambda: self.transaction_finished.emit())
            self.pacman_transaction_worker.stream.connect(self.transaction_stdout_stream.emit)
            self.write_to_stdin.connect(self.pacman_transaction_worker.write_to_stdin)
            if not pkg_install:
                self.pacman_transaction_worker.start_process("pkexec",
                    ["pacman", "-Rns"] + pkg_remove
                )
            elif not pkg_remove:
                self.pacman_transaction_worker.start_process("pkexec",
                    ["pacman", "-S"] + pkg_install
                )
            else:
                # Not exactly secure, temp until I find a better solution or decide to separate the transaction types instead
                self.pacman_transaction_worker.start_process("pkexec",
                    ["sh", "-c", f"pacman -S {(' '.join(pkg_install))} && pacman -Rns {(' '.join(pkg_remove))}"]
                )
        except:
            self._release_pacman()
            raise
