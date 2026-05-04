import pytest
from unittest.mock import MagicMock, patch
from archcentral.ui.views.usergroupmanager import UserGroupManager
from archcentral.models.group_list import GroupListModel
from archcentral.helpers.custom_classes import GroupInfo
from archcentral.models.user_list import UserListModel
from archcentral.helpers.custom_classes import UserInfo

@pytest.fixture
def user_group_manager(qtbot):
    with patch("archcentral.ui.views.usergroupmanager.UserGroupManagerController") as mock_ctrl_cls, \
         patch("archcentral.ui.views.usergroupmanager.QThread") as mock_thread_cls:

        mock_ctrl = MagicMock()
        mock_ctrl.moveToThread = MagicMock()
        mock_ctrl_cls.return_value = mock_ctrl

        mock_thread = MagicMock()
        mock_thread.isRunning.return_value = False
        mock_thread_cls.return_value = mock_thread

        widget = UserGroupManager()
        qtbot.addWidget(widget)

        yield widget, mock_ctrl

        widget.cleanup_thread()

def test_get_selected_row_user(user_group_manager):
    widget, _ = user_group_manager

    user = UserInfo("tester1", 1000, 1000, "TESTER1", "/home/tester1", "/bin/bash")

    group = GroupInfo("wheel", 0, ["tester1"])

    widget.users_groups_tab.currentIndex = MagicMock(return_value=0)

    widget.user_list_proxy_model = MagicMock()
    widget.group_list_proxy_model = MagicMock()
    widget.user_list_model = MagicMock()
    widget.group_list_model = MagicMock()

    mock_index = MagicMock()
    mock_index.row.return_value = 0
    mock_index.column.return_value = 0

    widget.user_list_proxy_model.mapToSource.return_value = mock_index
    widget.group_list_proxy_model.mapToSource.return_value = mock_index

    widget.user_list_model.get_user_info_by_index.return_value = user
    widget.group_list_model.get_group_info_by_index.return_value = group

    result = widget._get_selected_row()

    assert isinstance(result, UserInfo)
    assert result.name == "tester1"
    assert result.gecos == "TESTER1"

def test_get_selected_row_group(user_group_manager):
    widget, _ = user_group_manager

    user = UserInfo("tester1", 1000, 1000, "TESTER1", "/home/tester1", "/bin/bash")

    group = GroupInfo("wheel", 0, ["tester1"])

    widget.users_groups_tab.currentIndex = MagicMock(return_value=1)
    widget.user_list_proxy_model = MagicMock()
    widget.group_list_proxy_model = MagicMock()
    widget.user_list_model = MagicMock()
    widget.group_list_model = MagicMock()

    mock_index = MagicMock()
    mock_index.row.return_value = 0
    mock_index.column.return_value = 0

    widget.user_list_proxy_model.mapToSource.return_value = mock_index
    widget.group_list_proxy_model.mapToSource.return_value = mock_index

    widget.user_list_model.get_user_info_by_index.return_value = user
    widget.group_list_model.get_group_info_by_index.return_value = group

    result = widget._get_selected_row()

    assert isinstance(result, GroupInfo)
    assert result.name == "wheel"
    assert "tester1" in result.users


def test_initialize_models(user_group_manager):
    widget, _ = user_group_manager

    users = [
        UserInfo("tester1", 1000, 1000, "TESTER1", "/home", "/bin/bash")
    ]

    groups = [
        GroupInfo("wheel", 0, ["tester1"])
    ]

    widget.user_list_table = MagicMock()
    widget.group_list_table = MagicMock()

    widget.initialize_models(users, groups)

    assert isinstance(widget.user_list_model, UserListModel)
    assert widget.user_list_model.rowCount() == 1
    assert widget.user_list_model._data[0].name == "tester1"

    assert isinstance(widget.user_list_proxy_model, MagicMock) is False  # real QSortFilterProxyModel

    widget.user_list_table.setModel.assert_called_once_with(widget.user_list_proxy_model)

    assert widget.user_list_proxy_model.sourceModel() == widget.user_list_model

    assert widget.user_list_proxy_model.filterKeyColumn() == 0

    assert isinstance(widget.group_list_model, GroupListModel)
    assert widget.group_list_model.rowCount() == 1
    assert widget.group_list_model._data[0].name == "wheel"

    widget.group_list_table.setModel.assert_called_once_with(widget.group_list_proxy_model)

    assert widget.group_list_proxy_model.sourceModel() == widget.group_list_model

    assert widget.group_list_proxy_model.filterKeyColumn() == 0

def test_refresh_lists(user_group_manager):
    widget, _ = user_group_manager

    users = [UserInfo("tester1", 1000, 1000, "TESTER1", "/home/tester1", "/bin/bash")]
    groups = [GroupInfo("wheel", 0, ["tester1"])]

    widget.user_list_model = UserListModel(users)
    widget.group_list_model = GroupListModel(groups)

    new_users = [
        UserInfo("tester2", 1001, 1001, "TESTER_2", "/home/tester2", "/bin/zsh")
    ]

    new_groups = [
        GroupInfo("sudo", 27, ["tester2"])
    ]

    widget.refresh_lists(new_users, new_groups)

    users_after = widget.user_list_model.return_all_users()
    groups_after = widget.group_list_model.return_all_groups()

    assert users_after[0].name == "tester2"
    assert users_after[0].uid == 1001

    assert groups_after[0].name == "sudo"
    assert groups_after[0].gid == 27


def test_open_user_add_dialog_success(user_group_manager):
    widget, _ = user_group_manager

    users = [UserInfo("tester1", 1000, 1000, "tester1", "/home/tester1", "/bin/bash")]
    groups = [GroupInfo("wheel", 0, ["tester1"])]

    widget.user_list_model = MagicMock()
    widget.group_list_model = MagicMock()

    widget.user_list_model.return_all_users.return_value = ["tester1"]
    widget.group_list_model.return_all_groups.return_value = groups

    fake_dialog = MagicMock()
    fake_dialog.exec.return_value = 1

    fake_dialog.current_edited_user = MagicMock(
        username="tester2",
        fullname="TESTER_2",
        homedir="/home/tester2",
        homedirtype="user",
        password="nagyontitkosjelszo",
        shell="/bin/bash",
        groups=["wheel"]
    )

    with patch(
        "archcentral.ui.views.usergroupmanager.UserAddDialog",
        return_value=fake_dialog
    ):
        widget.create_user_signal = MagicMock()
        widget.status_label = MagicMock()

        widget.open_user_add_dialog(["/bin/bash", "/bin/zsh"])

        widget.status_label.setText.assert_called_with("Adding user in process...")

        widget.create_user_signal.emit.assert_called_once_with(
            "tester2",
            "TESTER_2",
            "/home/tester2",
            "user",
            "nagyontitkosjelszo",
            "/bin/bash",
            ["wheel"]
        )

def test_open_user_add_dialog_abort(user_group_manager):
    widget, _ = user_group_manager

    widget.user_list_model = MagicMock()
    widget.group_list_model = MagicMock()

    widget.user_list_model.return_all_users.return_value = []
    widget.group_list_model.return_all_groups.return_value = []

    fake_dialog = MagicMock()
    fake_dialog.exec.return_value = 0

    with patch(
        "archcentral.ui.views.usergroupmanager.UserAddDialog",
        return_value=fake_dialog
    ):
        widget.create_user_signal = MagicMock()
        widget.status_label = MagicMock()

        widget.open_user_add_dialog(["/bin/bash"])

        widget.status_label.setText.assert_called_with("Adding user aborted.")
        widget.create_user_signal.emit.assert_not_called()

def test_open_user_change_password_dialog(user_group_manager):
    widget, _ = user_group_manager

    widget._get_selected_row = MagicMock(return_value="tester1")

    fake_dialog = MagicMock()
    fake_dialog.exec.return_value = 1
    fake_dialog.user = "tester1"
    fake_dialog.password = "verytitkospasszword"

    with patch(
        "archcentral.ui.views.usergroupmanager.UserPasswordChangeDialog",
        return_value=fake_dialog
    ):
        widget.change_user_password_signal = MagicMock()
        widget.status_label = MagicMock()

        widget.open_user_change_password_dialog()

        widget.status_label.setText.assert_called_with("Password change in process...")

        widget.change_user_password_signal.emit.assert_called_once_with(
            "tester1",
            "verytitkospasszword"
        )

def test_open_user_change_shell_dialog(user_group_manager):
    widget, _ = user_group_manager

    widget._get_selected_row = MagicMock(return_value="tester1")

    fake_dialog = MagicMock()
    fake_dialog.exec.return_value = 1
    fake_dialog.user = "tester1"
    fake_dialog.shell = "/bin/zsh"

    with patch(
        "archcentral.ui.views.usergroupmanager.UserChangeShellDialog",
        return_value=fake_dialog
    ):
        widget.change_user_shell_signal = MagicMock()
        widget.status_label = MagicMock()

        widget.open_user_change_shell_dialog(["/bin/bash", "/bin/zsh"])

        widget.status_label.setText.assert_called_with("Shell change in process...")

        widget.change_user_shell_signal.emit.assert_called_once_with(
            "tester1",
            "/bin/zsh"
        )

def test_open_user_change_full_name_dialog(user_group_manager):
    widget, _ = user_group_manager

    widget._get_selected_row = MagicMock(return_value="tester1")

    fake_dialog = MagicMock()
    fake_dialog.exec.return_value = 1
    fake_dialog.user = "tester1"
    fake_dialog.full_name = "TESTER1"

    with patch(
        "archcentral.ui.views.usergroupmanager.UserChangeFullNameDialog",
        return_value=fake_dialog
    ):
        widget.change_user_full_name_signal = MagicMock()
        widget.status_label = MagicMock()

        widget.open_user_change_full_name_dialog()

        widget.status_label.setText.assert_called_with("Full name change in process...")

        widget.change_user_full_name_signal.emit.assert_called_once_with(
            "tester1",
            "TESTER1"
        )

def test_open_user_change_homedir_dialog(user_group_manager):
    widget, _ = user_group_manager

    widget._get_selected_row = MagicMock(return_value="tester1")

    widget.user_list_model = MagicMock()
    widget.user_list_model.return_all_users.return_value = ["tester1"]

    fake_dialog = MagicMock()
    fake_dialog.exec.return_value = 1
    fake_dialog.user = "tester1"
    fake_dialog.homedir = "/home/new"

    with patch(
        "archcentral.ui.views.usergroupmanager.UserChangeHomeDirDialog",
        return_value=fake_dialog
    ):
        widget.change_user_homedir_signal = MagicMock()
        widget.status_label = MagicMock()

        widget.open_user_change_homedir_dialog()

        widget.status_label.setText.assert_called_with("Home directory change in process...")

        widget.change_user_homedir_signal.emit.assert_called_once_with(
            "tester1",
            "/home/new"
        )

def test_open_user_deletion_dialog(user_group_manager):
    widget, _ = user_group_manager

    widget._get_selected_row = MagicMock(return_value="tester1")

    fake_dialog = MagicMock()
    fake_dialog.exec.return_value = 1
    fake_dialog.user = "tester1"
    fake_dialog.homedir_delete = True

    with patch(
        "archcentral.ui.views.usergroupmanager.UserDeleteDialog",
        return_value=fake_dialog
    ):
        widget.delete_user_signal = MagicMock()
        widget.status_label = MagicMock()

        widget.open_user_deletion_dialog()

        widget.status_label.setText.assert_called_with("User deletion in progress...")

        widget.delete_user_signal.emit.assert_called_once_with(
            "tester1",
            True
        )

def test_open_manage_group_members_dialog(user_group_manager):
    widget, _ = user_group_manager

    group = GroupInfo("wheel", 0, ["tester1"])

    users = ["tester1", "tester2"]

    widget._get_selected_row = MagicMock(return_value=group)
    widget.user_list_model = MagicMock()
    widget.user_list_model.return_all_users.return_value = users

    fake_dialog = MagicMock()
    fake_dialog.exec.return_value = 1
    fake_dialog.group = group
    fake_dialog.marked_users = ["tester1"]

    with patch(
        "archcentral.ui.views.usergroupmanager.GroupManageUsersDialog",
        return_value=fake_dialog
    ) as dialog_cls:

        widget.modify_group_users_signal = MagicMock()
        widget.status_label = MagicMock()

        widget.open_manage_group_members_dialog()

        dialog_cls.assert_called_once()

        widget.status_label.setText.assert_called_with(
            "Group member changes in process..."
        )

        widget.modify_group_users_signal.emit.assert_called_once_with(
            "wheel",
            ["tester1"]
        )

def test_open_create_group_dialog(user_group_manager):
    widget, _ = user_group_manager

    widget.group_list_model = MagicMock()
    widget.group_list_model.return_all_groups.return_value = []
    widget.user_list_model = MagicMock()
    widget.user_list_model.return_all_users.return_value = ["tester1"]

    fake_group = MagicMock()
    fake_group.group_name = "wheel"
    fake_group.is_system_group = False
    fake_group.users = ["tester1"]

    fake_dialog = MagicMock()
    fake_dialog.exec.return_value = 1
    fake_dialog.current_edited_group = fake_group

    with patch(
        "archcentral.ui.views.usergroupmanager.GroupAddDialog",
        return_value=fake_dialog
    ):
        widget.create_group_signal = MagicMock()
        widget.status_label = MagicMock()

        widget.open_create_group_dialog()

        widget.status_label.setText.assert_called_with("Group creation in process...")

        widget.create_group_signal.emit.assert_called_once_with(
            "wheel",
            False,
            ["tester1"]
        )

def test_open_group_deletion_dialog(user_group_manager):
    widget, _ = user_group_manager

    widget._get_selected_row = MagicMock(return_value="wheel")

    fake_dialog = MagicMock()
    fake_dialog.exec.return_value = 1
    fake_dialog.group = "wheel"

    with patch(
        "archcentral.ui.views.usergroupmanager.GroupDeleteDialog",
        return_value=fake_dialog
    ):
        widget.delete_group_signal = MagicMock()
        widget.status_label = MagicMock()

        widget.open_group_deletion_dialog()

        widget.status_label.setText.assert_called_with("Group deletion in progress...")

        widget.delete_group_signal.emit.assert_called_once_with(
            "wheel"
        )

def test_cleanup_thread_running(user_group_manager):
    widget, _ = user_group_manager

    # simulate running thread
    widget.ugmc_thread.isRunning = MagicMock(return_value=True)
    widget.ugmc_thread.quit = MagicMock()
    widget.ugmc_thread.wait = MagicMock()

    widget.cleanup_thread()

    widget.ugmc_thread.quit.assert_called_once()
    widget.ugmc_thread.wait.assert_called_once()

def test_cleanup_thread_not_running(user_group_manager):
    widget, _ = user_group_manager

    widget.ugmc_thread.isRunning = MagicMock(return_value=False)
    widget.ugmc_thread.quit = MagicMock()
    widget.ugmc_thread.wait = MagicMock()

    widget.cleanup_thread()

    widget.ugmc_thread.quit.assert_not_called()
    widget.ugmc_thread.wait.assert_not_called()
