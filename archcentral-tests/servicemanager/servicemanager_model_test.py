import pytest
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from archcentral.models.systemd_units_list import SystemdUnitListModel
from archcentral.helpers.custom_classes import SystemdServiceInfo

class FakeUnit:
    def __init__(self, name, enabled, active, sub):
        self.Id = name
        self.UnitFileState = enabled
        self.ActiveState = active
        self.SubState = sub
        self.Description = "desc"
        self.LoadState = "loaded"
        self.ControlGroup = "cg"
        self.MemoryCurrent = 0
        self.ExecStart = []
        self.Result = "success"

@pytest.fixture
def model():
    data = [
        SystemdServiceInfo(FakeUnit("svc1", "enabled", "active", "running"), "/path"),
        SystemdServiceInfo(FakeUnit("svc2", "disabled", "inactive", "dead"), "/path"),
    ]
    return SystemdUnitListModel(data)

def test_row_and_column_count(model):
    assert model.rowCount() == 2
    assert model.columnCount() == 4

def test_headers(model):
    assert model.headerData(0, Qt.Horizontal) == "Name"
    assert model.headerData(1, Qt.Horizontal) == "Launch State"
    assert model.headerData(2, Qt.Horizontal) == "Status"
    assert model.headerData(3, Qt.Horizontal) == "Substatus"

def test_display_role(model):
    idx_name = model.index(0, 0)
    idx_enabled = model.index(0, 1)
    idx_active = model.index(0, 2)
    idx_sub = model.index(0, 3)

    assert model.data(idx_name, Qt.DisplayRole) == "svc1"
    assert model.data(idx_enabled, Qt.DisplayRole) == "enabled"
    assert model.data(idx_active, Qt.DisplayRole) == "active"
    assert model.data(idx_sub, Qt.DisplayRole) == "running"

def test_launch_state_background(model):
    enabled_idx = model.index(0, 1)
    disabled_idx = model.index(1, 1)

    assert model.data(enabled_idx, Qt.BackgroundRole).name() == QColor("darkgreen").name()
    assert model.data(disabled_idx, Qt.BackgroundRole).name() == QColor("darkred").name()

def test_active_state_background(model):
    active_idx = model.index(0, 2)
    inactive_idx = model.index(1, 2)

    assert model.data(active_idx, Qt.BackgroundRole).name() == QColor("darkgreen").name()
    assert model.data(inactive_idx, Qt.BackgroundRole).name() == QColor("darkred").name()

def test_substate_background(model):
    running_idx = model.index(0, 3)
    dead_idx = model.index(1, 3)

    assert model.data(running_idx, Qt.BackgroundRole).name() == QColor("darkgreen").name()
    assert model.data(dead_idx, Qt.BackgroundRole).name() == QColor("darkred").name()

def test_refresh_replaces_data(model):
    new_data = [
        SystemdServiceInfo(
            FakeUnit("svc3", "enabled", "active", "running"),
            "/path"
        )
    ]

    model.refresh(new_data)

    assert model.rowCount() == 1
    assert model.get_unit(model.index(0, 0)).unitname == "svc3"

def test_get_unit(model):
    unit = model.get_unit(model.index(0, 0))

    assert unit.unitname == "svc1"
