import pytest
from unittest.mock import MagicMock, patch
from archcentral.controllers.usergroupmanager_controller import UserGroupManagerController

@pytest.fixture
def controller():
    with patch("archcentral.controllers.usergroupmanager_controller.QProcessHandler"), \
         patch("archcentral.controllers.usergroupmanager_controller.getpwall"), \
         patch("archcentral.controllers.usergroupmanager_controller.getgrall"):

        ctrl = UserGroupManagerController()

        ctrl.useradd_worker = MagicMock()
        ctrl.passwd_worker = MagicMock()
        ctrl.chsh_process_handler = MagicMock()
        ctrl.userdel_worker = MagicMock()
        ctrl.groupadd_worker = MagicMock()
        ctrl.groupdel_worker = MagicMock()

        return ctrl

@pytest.mark.parametrize(
    "for_refresh, signal_name",
    [
        (False, "fetched_list_for_init"),
        (True, "fetched_list_for_refresh"),
    ],
)
def test_fetch_users_and_groups(controller, for_refresh, signal_name):
    with patch("archcentral.controllers.usergroupmanager_controller.getpwall") as mock_users, \
         patch("archcentral.controllers.usergroupmanager_controller.getgrall") as mock_groups:

        mock_users.return_value = [
            MagicMock(
                pw_name="tester1",
                pw_uid=1000,
                pw_gid=1000,
                pw_gecos="tester1",
                pw_dir="/home/tester1",
                pw_shell="/bin/bash"
            )
        ]

        mock_groups.return_value = [
            MagicMock(
                gr_name="wheel",
                gr_gid=0,
                gr_mem=["tester1"]
            )
        ]

        signal_mock = MagicMock()
        setattr(controller, signal_name, signal_mock)

        controller.fetch_users_and_groups(for_refresh=for_refresh)

        signal_mock.emit.assert_called_once()

        users, groups = signal_mock.emit.call_args[0]

        assert users[0].name == "tester1"
        assert users[0].uid == 1000
        assert groups[0].name == "wheel"

@patch("archcentral.controllers.usergroupmanager_controller.QProcessHandler")
def test_user_add_minimal(mock_qprocess, controller):
    mock_proc = MagicMock()
    mock_qprocess.return_value = mock_proc

    controller.user_add(
        username="tester1",
        fullname="",
        homedir="/home/tester1",
        homedirtype="none",
        password="pw",
        shell="/bin/bash",
        groups=[]
    )

    program, args = mock_proc.start_process.call_args[0]

    assert program == "pkexec"
    assert "useradd" in args
    assert "-c" not in args
    assert "-G" not in args

@patch("archcentral.controllers.usergroupmanager_controller.QProcessHandler")
def test_user_add_with_fullname(mock_qprocess, controller):
    mock_proc = MagicMock()
    mock_qprocess.return_value = mock_proc

    controller.user_add(
        username="tester1",
        fullname="tester1 Example",
        homedir="/home/tester1",
        homedirtype="none",
        password="pw",
        shell="/bin/bash",
        groups=[]
    )

    _, args = mock_proc.start_process.call_args[0]

    assert "-c" in args
    assert "tester1 Example" in args

@patch("archcentral.controllers.usergroupmanager_controller.QProcessHandler")
def test_user_add_auto_home(mock_qprocess, controller):
    mock_proc = MagicMock()
    mock_qprocess.return_value = mock_proc

    controller.user_add(
        username="tester1",
        fullname="",
        homedir="/home/tester1",
        homedirtype="auto",
        password="pw",
        shell="/bin/bash",
        groups=[]
    )

    _, args = mock_proc.start_process.call_args[0]

    assert "-m" in args
    assert "-d" not in args

@patch("archcentral.controllers.usergroupmanager_controller.QProcessHandler")
def test_user_add_select_existing_home(mock_qprocess, controller):
    mock_proc = MagicMock()
    mock_qprocess.return_value = mock_proc

    controller.user_add(
        username="tester1",
        fullname="",
        homedir="/custom/home",
        homedirtype="selectexisting",
        password="pw",
        shell="/bin/bash",
        groups=[]
    )

    _, args = mock_proc.start_process.call_args[0]

    assert "-d" in args
    assert "/custom/home" in args

@patch("archcentral.controllers.usergroupmanager_controller.QProcessHandler")
def test_user_add_groups(mock_qprocess, controller):
    mock_proc = MagicMock()
    mock_qprocess.return_value = mock_proc

    controller.user_add(
        username="tester1",
        fullname="",
        homedir="/home/tester1",
        homedirtype="none",
        password="pw",
        shell="/bin/bash",
        groups=["wheel", "audio"]
    )

    _, args = mock_proc.start_process.call_args[0]

    assert "-G" in args
    assert "wheel,audio" in args


@patch("archcentral.controllers.usergroupmanager_controller.QProcessHandler")
def test_passwd(mock_qprocess, controller):
    mock_proc = MagicMock()
    mock_qprocess.return_value = mock_proc

    controller.passwd("tester1", "secretpw", for_user_creation=False)

    program, args = mock_proc.start_process.call_args[0]

    assert program == "pkexec"
    assert args == ["passwd", "tester1", "--stdin"]

    mock_proc.write_to_stdin.assert_called_once_with("secretpw\n")

@patch("archcentral.controllers.usergroupmanager_controller.QProcessHandler")
def test_get_shell_list_user_creation(mock_qprocess, controller):
    mock_proc = MagicMock()
    mock_qprocess.return_value = mock_proc

    controller.get_shell_list(for_user_creation=True)

    program, args = mock_proc.start_process.call_args[0]

    assert program == "chsh"
    assert args == ["-l"]

@patch("archcentral.controllers.usergroupmanager_controller.QProcessHandler")
def test_change_shell(mock_qprocess, controller):
    mock_proc = MagicMock()
    mock_qprocess.return_value = mock_proc

    controller.change_shell("tester1", "/bin/zsh")

    program, args = mock_proc.start_process.call_args[0]

    assert program == "pkexec"
    assert args == ["usermod", "-s", "/bin/zsh", "tester1"]

@patch("archcentral.controllers.usergroupmanager_controller.QProcessHandler")
def test_user_delete_with_home(mock_qprocess, controller):
    mock_proc = MagicMock()
    mock_qprocess.return_value = mock_proc

    controller.user_delete("tester1", homedir_delete=True)

    program, args = mock_proc.start_process.call_args[0]

    assert program == "pkexec"
    assert args == ["userdel", "-r", "tester1"]

@patch("archcentral.controllers.usergroupmanager_controller.QProcessHandler")
def test_user_delete_without_home(mock_qprocess, controller):
    mock_proc = MagicMock()
    mock_qprocess.return_value = mock_proc

    controller.user_delete("tester1", homedir_delete=False)

    program, args = mock_proc.start_process.call_args[0]

    assert program == "pkexec"
    assert args == ["userdel", "tester1"]

@patch("archcentral.controllers.usergroupmanager_controller.QProcessHandler")
def test_change_full_name(mock_qprocess, controller):
    mock_proc = MagicMock()
    mock_qprocess.return_value = mock_proc

    controller.change_full_name("tester1", "tester1 Example")

    program, args = mock_proc.start_process.call_args[0]

    assert program == "pkexec"
    assert args == ["usermod", "-c", "tester1 Example", "tester1"]

@patch("archcentral.controllers.usergroupmanager_controller.QProcessHandler")
def test_change_homedir(mock_qprocess, controller):
    mock_proc = MagicMock()
    mock_qprocess.return_value = mock_proc

    controller.change_homedir("tester1", "/home/newtester1")

    program, args = mock_proc.start_process.call_args[0]

    assert program == "pkexec"
    assert args == ["usermod", "-d", "/home/newtester1", "tester1"]

@patch("archcentral.controllers.usergroupmanager_controller.QProcessHandler")
def test_modify_group_users(mock_qprocess, controller):
    mock_proc = MagicMock()
    mock_qprocess.return_value = mock_proc

    controller.modify_group_users(
        "devs",
        [
            ("tester1", False),  # add
            ("bob", True),     # remove
        ]
    )

    program, args = mock_proc.start_process.call_args[0]

    assert program == "pkexec"

    assert args[0] == "sh"
    assert args[1] == "-c"

    shell_cmd = args[2]

    assert "gpasswd -a tester1 devs" in shell_cmd
    assert "gpasswd -d bob devs" in shell_cmd
    assert "&&" in shell_cmd

@patch("archcentral.controllers.usergroupmanager_controller.QProcessHandler")
def test_group_add_system_group(mock_qprocess, controller):
    mock_proc = MagicMock()
    mock_qprocess.return_value = mock_proc

    controller.group_add(
        groupname="devs",
        is_system_group=True,
        users=["tester1", "bob"]
    )

    program, args = mock_proc.start_process.call_args[0]

    assert program == "pkexec"
    assert "groupadd" in args
    assert "-r" in args
    assert "-U" in args
    assert "tester1,bob" in args

@patch("archcentral.controllers.usergroupmanager_controller.QProcessHandler")
def test_group_add_normal_group(mock_qprocess, controller):
    mock_proc = MagicMock()
    mock_qprocess.return_value = mock_proc

    controller.group_add(
        groupname="devs",
        is_system_group=False,
        users=["tester1", "bob"]
    )

    program, args = mock_proc.start_process.call_args[0]

    assert program == "pkexec"
    assert "groupadd" in args
    assert "-r" not in args
    assert "-U" in args
    assert "tester1,bob" in args

@patch("archcentral.controllers.usergroupmanager_controller.QProcessHandler")
def test_group_del(mock_qprocess, controller):
    mock_proc = MagicMock()
    mock_qprocess.return_value = mock_proc

    controller.group_del("devs")

    program, args = mock_proc.start_process.call_args[0]

    assert program == "pkexec"
    assert args == ["groupdel", "devs"]
