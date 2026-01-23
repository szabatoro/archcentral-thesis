from PySide6.QtCore import QObject,  Signal
from archcentral.helpers.qprocesshelper import QProcessHandler

class PacmanUpdater(QObject):
    finished_fetch: Signal = Signal(list)
    running_update: Signal = Signal(str)

    # fetches latest package info from mirrors
    def fetch(self) -> None:
        """
        Fetches latest package info from mirrors, lists updateable packages and emits them with the finished_fetch signal.
        """
        self.pacman_worker = QProcessHandler()
        self.pacman_worker.finished.connect(self._get_update_list)
        self.pacman_worker.start_process("pkexec", ["pacman", "-Sy"])

    # reads updateable packages
    def _get_update_list(self) -> None:
        self.pacman_worker = QProcessHandler()
        self.pacman_worker.finished.connect(self._process_pacman_fetch_output)
        self.pacman_worker.start_process("pacman", ["-Qu"])

    # processes updateable packages into a list
    def _process_pacman_fetch_output(self, raw_updates) -> None:
        updates: list = raw_updates.splitlines()

        processed_updates: list = []
        for upd in updates:
            processed_update: str = upd.split()
            processed_update.remove('->')
            processed_updates.append(processed_update)

        self.finished_fetch.emit(processed_updates)

    def update(self, packagelist) -> None:
        """
        Runs pacman -S with the specified packages, updating the system.
        """
        self.pacman_worker: QProcessHandler = QProcessHandler()
        self.pacman_worker.stream.connect(self.running_update.emit)
        #self.pacman_worker.start_process("pkexec", ["pacman", "-S", "--noconfirm", "hplip"]) # testing
        self.pacman_worker.start_process("pkexec", ["pacman", "-S", "--noconfirm"] + packagelist)
