from typing import Literal
from PySide6.QtCore import QObject,  Signal
from archcentral.helpers.qprocesshelper import QProcessHandler
from archcentral.helpers.custom_classes import UserInfo, GroupInfo

class UserGroupManagerController(QObject):
    fetched_list: Signal = Signal(list, str)

    def __init__(self) -> None:
        super().__init__()

    def fetch_users_and_groups(self) -> None:
        """Fetches users and groups from /etc/passwd and /etc/group respectively."""
        self.user_process_handler: QProcessHandler = QProcessHandler()
        self.user_process_handler.finished.connect(lambda x: self._return_users_or_groups(x, "users"))
        self.user_process_handler.start_process("getent", ["passwd"])

        self.groups_process_handler: QProcessHandler = QProcessHandler()
        self.groups_process_handler.finished.connect(lambda x: self._return_users_or_groups(x, "groups"))
        self.groups_process_handler.start_process("getent", ["group"])

    def _return_users_or_groups(self, raw_data: str, processtype: Literal["users", "groups"]) -> None:
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
                    final_data.append(GroupInfo(processed_line[0], processed_line[-1]))
                self.fetched_list.emit(final_data, processtype)
            case "users":
                # Process the sorted data line by line for needed information
                for line in sorted_data:
                    processed_line: list[str] = line.split(":")
                    # Only list normal users (UID>1000), don't list "nobody" user
                    if (int)(processed_line[2]) >= 1000 and processed_line[0] != "nobody":
                        final_data.append(UserInfo(processed_line[0], processed_line[2], processed_line[3], processed_line[4], processed_line[5], processed_line[6]))
                self.fetched_list.emit(final_data, processtype)
