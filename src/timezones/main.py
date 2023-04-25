from fastapi import FastAPI, status, HTTPException

from timezones import schema
from timezones.database import TimezoneDB
from timezones.geo import validate_coordinate_input, get_utc_offset_from_lon
import typing as t

app = FastAPI()


@app.get("/timezones", response_model=schema.TimezoneBase, status_code=status.HTTP_200_OK)
def get_timezones(lat: t.Optional[float] = None, lon: t.Optional[float] = None) -> t.Dict[str, t.List[str]]:
    """
    Deliver available timezones. If query parameters are defined, return timezone for specific location.

    :param lat: latitude of location, in range (-90, 90)
    :param lon: longitude of location, in range (-180, 180)
    :return: Timezone ID
    """
    # Return all timezones
    if lat is None and lon is None:
        with TimezoneDB() as db:
            timezones = db.get_distinct_timezones()
        return {"TZID": timezones}

    # Return timezone filtered by coordinate
    elif isinstance(lat, (float, int)) and isinstance(lon, (float, int)):
        # Validate input
        valid_input = validate_coordinate_input(lat=float(lat), lon=float(lon))
        if not valid_input:
            raise HTTPException(status_code=422, detail="Invalid query parameters.")

        # If input is valid, query for coordinates
        with TimezoneDB() as db:
            timezone = db.get_timezone_for_location(lat=float(lat), lon=float(lon))
            if timezone is None:  # no data at coordinate (e.g. ocean)
                raise HTTPException(status_code=404, detail="Resource not found")
            elif timezone[0] == "uninhabited":
                timezone = [get_utc_offset_from_lon(lon=lon)]
        return {"TZID": [timezone[0]]}

    # Do not understand input values, e.g. lat is given, but lon is not
    elif None in [lat, lon] and (any([lat, lon]) or 0 in [lat, lon]):
        raise HTTPException(status_code=422, detail="Missing query parameters.")

    # Undefined client-side error
    else:
        raise HTTPException(status_code=400)
