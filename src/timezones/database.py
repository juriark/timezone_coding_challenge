import logging
from pathlib import Path
import typing as t

import geopandas
from sqlalchemy import create_engine, engine
from sqlalchemy.orm import sessionmaker

from timezones.constants import INPUT_FILE, Status, CONNECTION_STRING

_logger = logging.getLogger(__name__)

engine = create_engine(CONNECTION_STRING, echo=True)
Session = sessionmaker(engine)  # use sessionmaker to avoid passing around engine object


class TimezoneDB:
    def __init__(self) -> None:
        self.session = Session()

    def __enter__(self) -> "TimezoneDB":
        return self

    def __exit__(self, *args: t.Any) -> None:
        self.session.close()

    def _get_engine(self) -> engine:
        """Get sqlachemy engine from current Session"""
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
            gdf.to_postgis(name=table_name, con=self._get_engine(), schema=schema)
        except ValueError as error:
            _logger.error(f"Failed to write dataframe to database: {error}")
            return Status.FAIL

        return Status.SUCCESS
