from PySide6.QtCore import QObject,  Signal
from archcentral.helpers.qprocesshelper import QProcessHandler

class UserGroupManagerController(QObject):
    fetched_user_list: Signal = Signal()

    def __init__(self) -> None:
        super().__init__()

        self.fetch_users()

    def fetch_users(self) -> None:
        """Fetches users from /etc/passwd."""
        self.user_process_handler: QProcessHandler = QProcessHandler()
        self.user_process_handler.finished.connect(lambda x: print(x))
        self.user_process_handler.start_process("getent", ["passwd"])
