from fastapi import FastAPI

from timezones import schema
from timezones.database import TimezoneDB
from timezones.models import Timezones
import typing as t

app = FastAPI()


@app.get("/timezones", response_model=schema.TimezoneBase)  # does validation, filtering and provides schema in swagger
def get_timezones() -> t.Dict[str, t.List[str]]:
    """
    Deliver all available timezones
    :return:  # TODO
    """
    with TimezoneDB() as db:
        timezones = db.get_distinct_timezones()
    return {"TZID": timezones}
