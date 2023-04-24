from pydantic import BaseModel
import typing as t


class TimezoneBase(BaseModel):
    TZID: t.List[str]
