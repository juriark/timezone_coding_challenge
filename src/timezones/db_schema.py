from geoalchemy2 import Geometry
from sqlalchemy import Integer, Text
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

from timezones.constants import TIMEZONE_TABLE_NAME


class Base(DeclarativeBase):
    pass


class Timezones(Base):
    __tablename__ = TIMEZONE_TABLE_NAME

    index: Mapped[int] = mapped_column(Integer, primary_key=True)
    TZID: Mapped[str] = mapped_column(Text, nullable=False)
    geometry: Mapped[str] = mapped_column(Geometry, nullable=False)

# TODO: add pydantic schema for fastapi schema validation
