from PySide6.QtCore import QObject,  Signal
from archcentral.helpers.pacman_commands import PacmanManager

class PackageManagerController(QObject):
    # Signals
    update_fetched: Signal = Signal(list)
    update_stdout_stream: Signal = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.pacman_worker: PacmanManager = PacmanManager()

    # Set up pacman worker for fetching updates
    def fetch_updates(self) -> None:
        self.pacman_worker.finished_fetch.connect(self.update_fetched.emit)
        self.pacman_worker.fetch()

    def perform_update(self, packagelist) -> None:
        self.pacman_worker.running_update.connect(self.update_stdout_stream.emit)
        self.pacman_worker.update(packagelist)
