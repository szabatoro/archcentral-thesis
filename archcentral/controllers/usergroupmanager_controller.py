from typing import Literal
from PySide6.QtCore import QObject,  Signal
from archcentral.helpers.qprocesshelper import QProcessHandler
from archcentral.helpers.custom_classes import UserInfo, GroupInfo

class UserGroupManagerController(QObject):
    fetched_list_for_init: Signal = Signal(list, str)
    fetched_list_for_refresh: Signal = Signal(list, str)
    fetched_available_shells: Signal = Signal(str)
    created_user_signal: Signal = Signal()

    def __init__(self) -> None:
        super().__init__()

        self.created_user_signal.connect(lambda: self.fetch_users_and_groups(for_refresh=True))

    def fetch_users_and_groups(self, for_refresh: bool) -> None:
        """Fetches users and groups from /etc/passwd and /etc/group respectively."""
        self.user_process_handler: QProcessHandler = QProcessHandler()
        self.user_process_handler.finished.connect(lambda x: self._return_users_or_groups(x, "users", for_refresh))
        self.user_process_handler.start_process("getent", ["passwd"])

        self.groups_process_handler: QProcessHandler = QProcessHandler()
        self.groups_process_handler.finished.connect(lambda x: self._return_users_or_groups(x, "groups", for_refresh))
        self.groups_process_handler.start_process("getent", ["group"])

    def _return_users_or_groups(self, raw_data: str, processtype: Literal["users", "groups"], for_refresh: bool) -> None:
        """Process data provided by fetch_users_or_groups"""
        # Split the getent output up line by line for further processing
        sorted_data: list[str] = raw_data.splitlines()
        # Prepare the list the data will be returned in
        final_data: list= []
        match processtype:
            case "groups":
                # Process the sorted data line by line for needed information
                for line in sorted_data:
                    processed_line: list[str] = line.split(":")
                    processed_users: list[str] = processed_line[-1].split(",")
                    final_data.append(GroupInfo(processed_line[0], processed_users))
                self.fetched_list_for_refresh.emit(final_data, processtype) if for_refresh else self.fetched_list_for_init.emit(final_data, processtype)
            case "users":
                # Process the sorted data line by line for needed information
                for line in sorted_data:
                    processed_line: list[str] = line.split(":")
                    # Only list normal users (UID>1000), don't list "nobody" user
                    if (int)(processed_line[2]) >= 1000 and processed_line[0] != "nobody":
                        final_data.append(UserInfo(processed_line[0], processed_line[2], processed_line[3], processed_line[4], processed_line[5], processed_line[6]))
                self.fetched_list_for_refresh.emit(final_data, processtype) if for_refresh else self.fetched_list_for_init.emit(final_data, processtype)

    def _get_groups_of_user(self) -> None:
        pass

    def user_add(self, username: str, fullname: str,  homedir: str, homedirtype: Literal["none", "auto", "selectexisting"], password: str, shell: str) -> None:
        """Calls the useradd comments with the appropriate parameters, then calls passwd to set the new user's password."""
        self.useradd_worker: QProcessHandler = QProcessHandler()
        self.useradd_worker.finished.connect(lambda: self.passwd(username, password))
        match homedirtype:
            case "selectexisting":
                arguments = ["useradd", "-d", homedir,"-s", shell, "-c", fullname, username]
            case "auto":
                arguments = ["useradd", "-m", "-s", shell, "-c", fullname, username]
            case "none":
                arguments = ["useradd", "-s", shell, "-c", fullname, username]

        self.useradd_worker.start_process("pkexec", arguments)

    def passwd(self, username: str, password: str) -> None:
        """Sets the given user's password."""
        self.passwd_worker: QProcessHandler = QProcessHandler()
        self.passwd_worker.start_process("pkexec", ["passwd", username, "--stdin"])
        self.passwd_worker.write_to_stdin(f"{password}\n")
        self.passwd_worker.finished.connect(lambda: self.created_user_signal.emit())

    def get_shell_list(self) -> None:
        """Runs chsh -l to get a list of available shells."""
        self.chsh_process_handler: QProcessHandler = QProcessHandler()
        self.chsh_process_handler.finished.connect(self.fetched_available_shells.emit)
        self.chsh_process_handler.start_process("chsh", ["-l"])
