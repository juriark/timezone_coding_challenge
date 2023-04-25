import logging

_logger = logging.getLogger(__name__)


def is_in_range(value: float, lower_boundary: float, upper_boundary: float) -> bool:
    """Check if given value is within range defined by boundaries."""
    if lower_boundary < value < upper_boundary:
        return True
    return False


def get_utc_offset_from_lon(lon: float) -> str:
    """
    Maps longitude to meridians, and returns the UTC offset for that meridian

    Meridians are 15° apart, except that UTC−12 and UTC+12 are each 7.5° wide and are separated by the 180° meridian.
    :param lon: The longitude in range(-180, 180)
    :return: A string in the format 'UTC+/-offset'
    """
    if not is_in_range(lon, -180.0, 180.0):
        raise ValueError("Longitude not in range(-180, 180)")
    offset = int((abs(lon) + 7.5) / 15)
    meridian_string = f"UTC+{offset}" if lon >= -7.5 else f"UTC-{offset}"
    return meridian_string


def validate_coordinate_input(lat: float, lon: float) -> bool:
    """Validate if coordinates are in correct range."""
    # Check if coordinates are in correct range
    if not is_in_range(lat, -90.0, 90.0) or not is_in_range(lon, -180.0, 180.0):
        _logger.debug(f"Coordinates are not in range, {lat=}, {lon=}, expected range(-90, 90) and range(-180, 180")
        return False
    return True
