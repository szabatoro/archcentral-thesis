import pytest
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from archcentral.models.pacman_package_list import PacmanPackageListTableModel
from archcentral.helpers.custom_classes import PacmanPkgInfo

class FakeALPMPkg:
    def __init__(self, name, version, size=1000, isize=1000):
        self.name = name
        self.version = version
        self.size = size
        self.isize = isize
        self.desc = "desc"
        self.url = "url"
        self.licenses = []
        self.builddate = 0
        self.depends = []
        self.optdepends = []
        self.groups = []

@pytest.fixture
def model():
    data = [
        PacmanPkgInfo(FakeALPMPkg("pkg1", "1.0", 1500), False, False, "core"),
        PacmanPkgInfo(FakeALPMPkg("pkg2", "2.0", 2500), True, True, "core"),
    ]

    return PacmanPackageListTableModel(data)

def test_row_and_column_count(model):
    assert model.rowCount() == 2
    assert model.columnCount() == 6

def test_headers(model):
    assert model.headerData(0, Qt.Horizontal) == "Marked for"
    assert model.headerData(1, Qt.Horizontal) == "Repo"
    assert model.headerData(2, Qt.Horizontal) == "Package"
    assert model.headerData(5, Qt.Horizontal) == "Install Status"

def test_check_state_role(model):
    idx = model.index(1, 0)

    value = model.data(idx, Qt.CheckStateRole)

    assert value == Qt.Checked

def test_display_role_basic_fields(model):
    idx_repo = model.index(0, 1)
    idx_name = model.index(0, 2)
    idx_version = model.index(0, 3)

    assert model.data(idx_repo, Qt.DisplayRole) == "core"
    assert model.data(idx_name, Qt.DisplayRole) == "pkg1"
    assert model.data(idx_version, Qt.DisplayRole) == "1.0"

def test_install_status_display(model):
    installed_idx = model.index(1, 5)
    not_installed_idx = model.index(0, 5)

    assert model.data(installed_idx, Qt.DisplayRole) == "Installed"
    assert model.data(not_installed_idx, Qt.DisplayRole) == "Not Installed"

def test_background_role(model):
    installed_idx = model.index(1, 5)
    not_installed_idx = model.index(0, 5)

    assert isinstance(model.data(installed_idx, Qt.BackgroundRole), QColor)
    assert isinstance(model.data(not_installed_idx, Qt.BackgroundRole), QColor)

    assert model.data(installed_idx, Qt.BackgroundRole).name() == QColor("darkgreen").name()
    assert model.data(not_installed_idx, Qt.BackgroundRole).name() == QColor("darkred").name()

def test_flags_behavior(model):
    idx = model.index(0, 0)

    flags = model.flags(idx)

    assert flags & Qt.ItemIsEnabled
    assert flags & Qt.ItemIsSelectable
    assert flags & Qt.ItemIsUserCheckable

def test_setdata_marks_package(model):
    idx = model.index(0, 0)

    result = model.setData(idx, Qt.Checked.value, Qt.CheckStateRole)

    assert result is True
    assert model._data[0].marked is True

def test_get_marked_packages(model):
    result = model.get_marked_packages()

    assert len(result) == 1
    assert result[0][0] == "pkg2"
    assert result[0][1] is True

def test_total_size(model):
    assert model.get_total_size() == 4000

def test_get_package(model):
    idx = model.index(0, 0)
    pkg = model.get_package(idx)

    assert pkg.name == "pkg1"
    assert pkg.version == "1.0"

def test_refresh_replaces_data(model):
    new_data = [
        PacmanPkgInfo(FakeALPMPkg("pkg3", "3.0", 500), False, False, "extra")
    ]

    model.refresh(new_data)

    assert model.rowCount() == 1
    assert model.get_package(model.index(0, 0)).name == "pkg3"
