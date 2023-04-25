from pydantic import BaseModel
import typing as t


class TimezoneBase(BaseModel):
    """Output schema for endpoint. Used for validation."""
    TZID: t.List[str]
