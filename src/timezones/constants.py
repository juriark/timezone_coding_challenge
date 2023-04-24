from enum import Enum
from pathlib import Path

BASE_DIR = Path().cwd().parent
INPUT_FILE = BASE_DIR.joinpath("data/world/tz_world.shp")

CRS = "EPSG:4326"
CONNECTION_STRING = "postgresql://postgres:postgres@db:5432"


class Status(Enum):
    SUCCESS = "success"
    FAIL = "fail"
