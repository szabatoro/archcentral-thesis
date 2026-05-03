import pytest
from PySide6.QtCore import Qt
from archcentral.models.pacman_update_list import PacmanUpdateTableModel

@pytest.fixture(autouse=True)
def patch_unit_converter(monkeypatch):
    monkeypatch.setattr(
        "archcentral.helpers.unitconverter.unit_converter",
        lambda x: (x / 1000, "KB")
    )

@pytest.fixture
def update_model():
    data = [
        ("pkg1", "1.0", "2.0", 1500),
        ("pkg2", "1.1", "2.1", 2500),
    ]
    return PacmanUpdateTableModel(data)

def test_update_model_dimensions(update_model):
    assert update_model.rowCount() == 2
    assert update_model.columnCount() == 4

def test_update_model_headers(update_model):
    assert update_model.headerData(0, Qt.Horizontal) == "Package"
    assert update_model.headerData(1, Qt.Horizontal) == "Installed Version"

def test_update_model_formats_size_column(update_model):
    index = update_model.index(0, 3)
    value = update_model.data(index, Qt.DisplayRole)

    assert "KiB" in value

def test_get_packagenames(update_model):
    assert update_model.get_packagenames() == ["pkg1", "pkg2"]

def test_get_total_size(update_model):
    assert update_model.get_total_size() == 4000

def test_update_model_refresh(update_model):
    new_data = [("pkg3", "3.0", "4.0", 1000)]

    update_model.refresh(new_data)

    assert update_model.rowCount() == 1
    assert update_model.get_packagenames() == ["pkg3"]
