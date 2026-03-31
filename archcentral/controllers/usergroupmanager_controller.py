from typing import Literal
from PySide6.QtCore import QObject,  Signal
from archcentral.helpers.qprocesshelper import QProcessHandler
from archcentral.helpers.custom_classes import UserInfo, GroupInfo
from pwd import getpwall
from grp import getgrall

class UserGroupManagerController(QObject):
    fetched_list_for_init: Signal = Signal(list, list)
    fetched_list_for_refresh: Signal = Signal(list, list)
    fetched_available_shells_for_user_creation: Signal = Signal(str)
    fetched_available_shells_for_shell_change: Signal = Signal(str)
    created_user_signal: Signal = Signal(str)
    changed_user_properties_signal: Signal = Signal()

    # These signals carry the user name and the underlying process call's exit code
    deleted_user_signal: Signal = Signal(str, int)
    changed_password_signal: Signal = Signal(str, int)
    changed_shell_signal: Signal = Signal(str, int)
    changed_full_name_signal: Signal = Signal(str, int)
    changed_homedir_signal: Signal = Signal(str, int)

    def __init__(self) -> None:
        super().__init__()

        # Updates the user and group models after creating a new user or modifying an existing one
        self.created_user_signal.connect(lambda: self.fetch_users_and_groups(for_refresh=True))
        self.changed_user_properties_signal.connect(lambda: self.fetch_users_and_groups(for_refresh=True))

    def fetch_users_and_groups(self, for_refresh: bool) -> None:
        """Process data provided by fetch_users_or_groups"""
        users_raw = getpwall()
        groups_raw = getgrall()
        processed_groups: list = [
            GroupInfo(group.gr_name, group.gr_mem) for group in groups_raw
        ]
        processed_users = [
            UserInfo(user.pw_name, user.pw_uid, user.pw_gid, user.pw_gecos, user.pw_dir, user.pw_shell)
            for user in users_raw
            if user.pw_uid >= 1000 and user.pw_name != "nobody"
        ]
        self.fetched_list_for_refresh.emit(processed_users, processed_groups) if for_refresh else self.fetched_list_for_init.emit(processed_users, processed_groups)

    def _get_groups_of_user(self) -> None:
        pass

    def user_add(self, username: str, fullname: str,  homedir: str, homedirtype: Literal["none", "auto", "selectexisting"], password: str, shell: str) -> None:
        """Calls the useradd comments with the appropriate parameters, then calls passwd to set the new user's password."""
        self.useradd_worker: QProcessHandler = QProcessHandler()
        self.useradd_worker.finished.connect(lambda: self.passwd(username, password, for_user_creation=True))
        match homedirtype:
            case "selectexisting":
                arguments = ["useradd", "-d", homedir,"-s", shell, "-c", fullname, username]
            case "auto":
                arguments = ["useradd", "-m", "-s", shell, "-c", fullname, username]
            case "none":
                arguments = ["useradd", "-s", shell, "-c", fullname, username]

        self.useradd_worker.start_process("pkexec", arguments)

    def passwd(self, username: str, password: str, for_user_creation: bool = False) -> None:
        """Sets the given user's password."""
        self.passwd_worker: QProcessHandler = QProcessHandler()
        self.passwd_worker.write_to_stdin(f"{password}\n")
        if for_user_creation:
            self.passwd_worker.finished.connect(lambda: self.created_user_signal.emit(username))
        else:
            self.passwd_worker.finished_with_exit_code.connect(lambda _, exit_code: self.changed_password_signal.emit(username, exit_code))
            self.passwd_worker.finished.connect(lambda: self.changed_user_properties_signal.emit())

        self.passwd_worker.start_process("pkexec", ["passwd", username, "--stdin"])

    def get_shell_list(self, for_user_creation: bool = False) -> None:
        """Runs chsh -l to get a list of available shells."""
        self.chsh_process_handler: QProcessHandler = QProcessHandler()
        self.chsh_process_handler.finished.connect(self.fetched_available_shells_for_user_creation.emit if for_user_creation else self.fetched_available_shells_for_shell_change.emit)
        self.chsh_process_handler.start_process("chsh", ["-l"])

    def change_shell(self, username: str, shell: str) -> None:
        """Runs chsh -s to set new shell for given user."""
        self.usermod_shell_worker: QProcessHandler = QProcessHandler()
        self.usermod_shell_worker.finished_with_exit_code.connect(lambda _, exit_code: self.changed_shell_signal.emit(username, exit_code))
        self.usermod_shell_worker.finished.connect(lambda: self.changed_user_properties_signal.emit())
        self.usermod_shell_worker.start_process("pkexec", ["usermod", "-s", shell, username])

    def user_delete(self, username: str, homedir_delete: bool) -> None:
        """Runs userdel to delete a given user, with the option to also delete their home directory."""
        self.userdel_worker: QProcessHandler = QProcessHandler()
        self.userdel_worker.finished_with_exit_code.connect(lambda _, exit_code: self.deleted_user_signal.emit(username, exit_code))
        self.userdel_worker.finished.connect(lambda: self.changed_user_properties_signal.emit())
        userdel_args = ["userdel", "-r", username] if homedir_delete else ["userdel", username]
        self.userdel_worker.start_process("pkexec", userdel_args)

    def change_full_name(self, username: str, full_name: str) -> None:
        """Runs usermod -c to change user's full name (GECOS comment)."""
        self.usermod_gecos_worker: QProcessHandler = QProcessHandler()
        self.usermod_gecos_worker.finished_with_exit_code.connect(lambda _, exit_code: self.changed_full_name_signal.emit(username, exit_code))
        #self.usermod_gecos_worker.finished.connect(lambda: self.changed_user_properties_signal.emit())
        self.usermod_gecos_worker.start_process("pkexec", ["usermod", "-c", full_name, username])

    def change_homedir(self, username: str, homedir: str) -> None:
        """Runs usermod -d to change the user's home directory."""
        self.usermod_homedir_worker: QProcessHandler = QProcessHandler()
        self.usermod_homedir_worker.finished_with_exit_code.connect(lambda _, exit_code: self.changed_homedir_signal.emit(username, exit_code))
        self.usermod_homedir_worker.finished.connect(lambda: self.changed_user_properties_signal.emit())
        self.usermod_homedir_worker.start_process("pkexec", ["usermod", "-d", homedir, username])
