import logging
from pathlib import Path
import typing as t

import geopandas
from geoalchemy2 import Geometry
from sqlalchemy import create_engine, Engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker

from timezones.constants import INPUT_FILE, Status, CONNECTION_STRING

_logger = logging.getLogger(__name__)

engine = create_engine(CONNECTION_STRING, echo=True)
Session = sessionmaker(engine)


class TimezoneDB:
    def __init__(self) -> None:
        self.session = Session()

    def __enter__(self) -> "TimezoneDB":
        return self

    def __exit__(self, *args: t.Any) -> None:
        self.session.close()

    def _get_engine(self) -> Engine:
        """Get sqlachemy engine object from current session"""
        return self.session.get_bind()

    def create_table_from_shapefile(
            self,
            file_path: Path = INPUT_FILE,
            rows: t.Optional[int] = None,
            table_name: str = "timezones",
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
            gdf.to_postgis(name=table_name, con=self._get_engine(), schema=schema,
                           dtype={'geometry': Geometry('POLYGON', srid=4326)})
        except ValueError as error:
            _logger.error(f"Failed to write dataframe to database: {error}")
            return Status.FAIL

        _logger.info("Successfully written to database.")
        return Status.SUCCESS


if __name__ == '__main__':
    # This script is being called when spinning up the docker network from `docker compose`, and effectively writes the
    # timezones to the database.

    from time import sleep

    # Initial database setup
    _logger.info(f"Trying to write timezone table to database {CONNECTION_STRING}")

    # Might run into race condition for first container spinup.
    num_tries = 0
    max_tries = 4
    while num_tries <= max_tries:
        try:
            with TimezoneDB() as db:
                write_to_db_status = db.create_table_from_shapefile(
                    rows=10)  # TODO: write sqlalchemy schema for timezones
                break
        except OperationalError:
            if num_tries == max_tries:
                _logger.error("Cannot connect to database - number of tries exceeded")
                raise
            num_tries += 1
            sleep(5)
