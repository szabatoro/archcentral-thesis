import pytest
from PySide6.QtCore import Qt
from archcentral.models.group_list import GroupListModel
from archcentral.helpers.custom_classes import GroupInfo

@pytest.fixture
def model():
    data = [
        GroupInfo("wheel", 0, ["tester1", "tester2"]),
        GroupInfo("docker", 1001, ["tester3"]),
    ]
    return GroupListModel(data)

def test_row_and_column_count(model):
    assert model.rowCount() == 2
    assert model.columnCount() == 3

def test_headers(model):
    assert model.headerData(0, Qt.Horizontal) == "Group"
    assert model.headerData(1, Qt.Horizontal) == "GID"
    assert model.headerData(2, Qt.Horizontal) == "Users"

def test_display_role(model):
    idx_name = model.index(0, 0)
    idx_gid = model.index(0, 1)
    idx_users = model.index(0, 2)

    assert model.data(idx_name, Qt.DisplayRole) == "wheel"
    assert model.data(idx_gid, Qt.DisplayRole) == 0
    assert model.data(idx_users, Qt.DisplayRole) == "tester1, tester2"

def test_refresh(model):
    new_data = [
        GroupInfo("randomgroup", 50, ["tester3"])
    ]

    model.refresh(new_data)

    assert model.rowCount() == 1
    assert model.data(model.index(0, 0), Qt.DisplayRole) == "randomgroup"

def test_get_group_info_by_index(model):
    group = model.get_group_info_by_index(model.index(0, 0))

    assert group.name == "wheel"
    assert group.gid == 0

def test_return_all_groups_objects(model):
    result = model.return_all_groups(name_only=False)

    assert len(result) == 2
    assert result[0].name == "wheel"
    assert result[0].gid == 0
    assert result[1].name == "docker"
    assert result[1].gid == 1001

def test_return_all_groups_names(model):
    result = model.return_all_groups(name_only=True)

    assert result == ["wheel", "docker"]
