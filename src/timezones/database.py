import logging
from pathlib import Path
import typing as t

import geopandas
from geoalchemy2 import Geometry
from sqlalchemy import create_engine, Engine, text, Connection
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

from timezones.constants import INPUT_FILE, Status, CONNECTION_STRING, TIMEZONE_TABLE_NAME
from timezones import models

_logger = logging.getLogger(__name__)

engine = create_engine(CONNECTION_STRING, echo=True)
SessionLocal = sessionmaker(engine)


class TimezoneDB:
    def __init__(self) -> None:
        self.session = SessionLocal()

    def __enter__(self) -> "TimezoneDB":
        return self

    def __exit__(self, *args: t.Any) -> None:
        self.session.close()

    def _get_engine(self) -> t.Union[Engine, Connection]:
        """Get sqlachemy engine object from current session"""
        return self.session.get_bind()

    def create_table_from_shapefile(
            self,
            file_path: Path = INPUT_FILE,
            rows: t.Optional[int] = None,
            table_name: str = TIMEZONE_TABLE_NAME,
            schema: t.Optional[None] = None,
    ) -> Status:
        """
        Write shapefile to PostGIS database.

        :param file_path: Path to the shapefile.
        :param rows: Number of rows to read from shapefile.
        :param table_name: Name of the table to create.
        :param schema: Name of the schema. If None, uses default schema 'public'.
        :return: Status object defining whether operation was successful or not.
        """
        try:
            assert file_path.suffix == ".shp"
            assert file_path.exists()
        except AssertionError:
            _logger.error(f"Cannot find shapefile at location {file_path}")
            return Status.FAIL

        # Read data
        gdf = geopandas.read_file(filename=file_path, rows=rows)
        _logger.info(f"Successfully read geodata from shapefile {file_path}")

        # Write to database
        try:
            gdf.to_postgis(name=table_name, con=self._get_engine(), schema=schema, index=True,
                           dtype={'geometry': Geometry('POLYGON', srid=4326)})
        except ValueError as error:
            _logger.error(f"Failed to write dataframe to database: {error}")
            return Status.FAIL

        _logger.info("Successfully written to database.")
        return Status.SUCCESS

    def get_distinct_timezones(self) -> t.List[str]:
        """Get all timezones from database."""
        timezones = self.session.query(models.Timezones.TZID).distinct().all()
        result = [timezone[0] for timezone in timezones]
        return result

    def get_timezone_for_location(self, lat: float, lon: float) -> t.Optional[t.List[str]]:
        """Get the timezone for the location specified by lat and lon."""
        location = f'SRID=4326;POINT({lon:.5f} {lat:.5f})'
        result = self.session.query(models.Timezones.TZID).filter(
            models.Timezones.geometry.ST_Intersects(location)).first()
        return result  # type: ignore


if __name__ == '__main__':
    # This script is being called when spinning up the docker network from `docker compose`, and effectively writes the
    # timezones to the database.

    from time import sleep

    # Initial database setup
    _logger.info(f"Trying to write timezone table to database {CONNECTION_STRING}")

    # Might run into race condition for first container spinup.
    num_tries = 0
    max_tries = 10
    while num_tries <= max_tries:
        try:
            with TimezoneDB() as db:
                write_to_db_status = db.create_table_from_shapefile()
                break
        except OperationalError:
            if num_tries == max_tries:
                _logger.error("Cannot connect to database - number of tries exceeded")
                raise
            num_tries += 1
            sleep(3)
