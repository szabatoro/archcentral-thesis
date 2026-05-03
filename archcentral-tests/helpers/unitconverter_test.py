import pytest
from archcentral.helpers.unitconverter import unit_converter, convert_mem_unit

@pytest.mark.parametrize(
    "input_bytes, expected_value, expected_unit",
    [
        (500, 500.0, "B"),
        (2048, 2.0, "KiB"),
        (1024 * 1024, 1.0, "MiB"),
        (1024 * 1024 * 1024, 1.0, "GiB"),
        (1024 * 1024 * 1024 * 1024, 1.0, "TiB"),
    ],
)
def test_unit_converter_correct_conversion(input_bytes, expected_value, expected_unit):
    result = unit_converter(input_bytes)
    assert result == (expected_value, expected_unit)


@pytest.mark.parametrize(
    "input_bytes, expected_string",
    [
        (500, "500.00 B"),
        (2048, "2.00 KiB"),
        (1024 * 1024, "1.00 MiB"),
        (5 * 1024 * 1024 * 1024, "5.00 GiB"),
    ],
)
def test_unit_converter_string_output_when_as_tuple_false(input_bytes, expected_string):
    result = unit_converter(input_bytes, as_tuple=False)
    assert isinstance(result, str)
    assert result == expected_string

@pytest.mark.parametrize(
    "bytes_used, bytes_total, expected",
    [
        # === Default behavior ===
        (512 * 1024, 2048 * 1024, (512.0, "KiB", 2.0, "MiB")),
        (512 * 1024 * 1024, 4 * 1024**3, (512.0, "MiB", 4.0, "GiB")),
        (1.5 * 1024**3, 8 * 1024**3, (1.5, "GiB", 8.0, "GiB")),
        (256 * 1024 * 1024, 32 * 1024**3, (256.0, "MiB", 32.0, "GiB")),
        (1536 * 1024 * 1024, 8 * 1024**3, (1.5, "GiB", 8.0, "GiB")),
        (4 * 1024**3, 16 * 1024**3, (4.0, "GiB", 16.0, "GiB")),
        (7.5 * 1024**3, 32 * 1024**3, (7.5, "GiB", 32.0, "GiB")),
        (1234567 * 1024, 16 * 1024**3, (1.18, "GiB", 16.0, "GiB")),
        (987654321, 17179869184, (941.90, "MiB", 16.0, "GiB")),
    ],
)
def test_convert_mem_unit(bytes_used, bytes_total, expected):
    result = convert_mem_unit(bytes_used, bytes_total)
    assert result == expected


@pytest.mark.parametrize(
    "bytes_used, bytes_total",
    [
        (1536 * 1024, 1536 * 1024),
        (10_000 * 1024, 20_000 * 1024),
        (5 * 1024**3, 32 * 1024**3),
    ],
)
def test_convert_mem_unit_rounding_to_two_decimals(bytes_used, bytes_total):
    used, _, total, _ = convert_mem_unit(bytes_used, bytes_total)
    assert used == round(used, 2)
    assert total == round(total, 2)
