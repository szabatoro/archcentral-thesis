import pytest
from PySide6.QtCore import Qt
from archcentral.models.user_list import UserListModel
from archcentral.helpers.custom_classes import UserInfo

@pytest.fixture
def model():
    data = [
        UserInfo(
            name="tester1",
            uid=1000,
            gid=1000,
            gecos="TESTER1",
            home="/home/tester1",
            shell="/bin/bash"
        ),
        UserInfo(
            name="tester2",
            uid=1001,
            gid=1001,
            gecos="TESTER_2",
            home="/home/tester2",
            shell="/usr/bin/zsh"
        ),
    ]
    return UserListModel(data)

def test_row_and_column_count(model):
    assert model.rowCount() == 2
    assert model.columnCount() == 6

def test_headers(model):
    assert model.headerData(0, Qt.Horizontal) == "Username"
    assert model.headerData(1, Qt.Horizontal) == "UID"
    assert model.headerData(2, Qt.Horizontal) == "GID"
    assert model.headerData(3, Qt.Horizontal) == "Full name"
    assert model.headerData(4, Qt.Horizontal) == "Home"
    assert model.headerData(5, Qt.Horizontal) == "Shell"

def test_display_role(model):
    idx_name = model.index(0, 0)
    idx_uid = model.index(0, 1)
    idx_gid = model.index(0, 2)
    idx_gecos = model.index(0, 3)
    idx_home = model.index(0, 4)
    idx_shell = model.index(0, 5)

    assert model.data(idx_name, Qt.DisplayRole) == "tester1"
    assert model.data(idx_uid, Qt.DisplayRole) == 1000
    assert model.data(idx_gid, Qt.DisplayRole) == 1000
    assert model.data(idx_gecos, Qt.DisplayRole) == "TESTER1"
    assert model.data(idx_home, Qt.DisplayRole) == "/home/tester1"
    assert model.data(idx_shell, Qt.DisplayRole) == "/bin/bash"

def test_refresh(model):
    new_data = [
        UserInfo(
            name="tester2",
            uid=1050,
            gid=1050,
            gecos="TESTER_2_NEW",
            home="/home/tester2",
            shell="/bin/sh"
        )
    ]
    model.refresh(new_data)

    assert model.rowCount() == 1
    assert model.data(model.index(0, 0), Qt.DisplayRole) == "tester2"
    assert model.data(model.index(0, 3), Qt.DisplayRole) == "TESTER_2_NEW"

def test_get_user_info_by_index(model):
    user = model.get_user_info_by_index(model.index(0, 0))
    assert user.name == "tester1"
    assert user.uid == 1000
    assert user.gecos == "TESTER1"

def test_get_user_info_by_username(model):
    user = model.get_user_info("tester2")
    assert user is not None
    assert user.name == "tester2"
    assert user.uid == 1001
    assert user.shell == "/usr/bin/zsh"

    assert model.get_user_info("nonexistent") is None

def test_return_all_users_objects(model):
    result = model.return_all_users(name_only=False)
    assert len(result) == 2
    assert result[0].name == "tester1"
    assert result[0].uid == 1000
    assert result[1].name == "tester2"
    assert result[1].shell == "/usr/bin/zsh"

def test_return_all_users_names(model):
    result = model.return_all_users(name_only=True)
    assert result == ["tester1", "tester2"]
