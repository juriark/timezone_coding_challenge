import pytest

from timezones.geo import is_in_range, get_utc_offset_from_lon


@pytest.mark.parametrize("value, lower_boundary, upper_boundary, expected",
                         [(80.0, -90.0, 90.0, True), (-90, -90, 90, False), (0, 0, 0, False)])
def test_is_in_range(value: float, lower_boundary: float, upper_boundary: float, expected: bool) -> None:
    assert is_in_range(value=value, lower_boundary=lower_boundary, upper_boundary=upper_boundary) is expected


@pytest.mark.parametrize("lon, expected", [(0.0, "UTC+0"), (-179.999, "UTC-12"), (179, "UTC+12"), (-7.4, "UTC+0")])
def test_get_utc_offset_from_lon(lon: float, expected: str) -> None:
    assert get_utc_offset_from_lon(lon) == expected
