from enum import Enum
from pathlib import Path

# Paths
BASE_DIR: Path = Path().cwd().parent
INPUT_FILE: Path = BASE_DIR.joinpath("data/world/tz_world.shp")

# Database
CONNECTION_STRING: str = "postgresql://postgres:postgres@db:5432"
TIMEZONE_TABLE_NAME: str = "timezones"

# Geodata
CRS: str = "EPSG:4326"


# Enums
class Status(Enum):
    SUCCESS = "success"
    FAIL = "fail"
