from fastapi import FastAPI

from timezones.database import TimezoneDB
from timezones.db_schema import Timezones

app = FastAPI()


@app.get("/")
def read_root():
    """
    This is awesome
    """
    return {"Hello": "World"}


@app.get("/timezones_tmp")
def read_first_timezone():
    with TimezoneDB() as db:
        timezones = db.session.query(Timezones).first()
    return {"index": str(timezones.index),
            "TZID": str(timezones.TZID),
            "geometry": str(timezones.geometry),
            }
