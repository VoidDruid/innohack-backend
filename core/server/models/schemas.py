from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Extra

StrDict = Dict[str, Any]


class DBJson(BaseModel):
    class Config:
        extra = Extra.forbid
        use_enum_values = True
        validate_assignment = True
        orm_mode = True


class SiteLayoutPosition(DBJson):
    lat: float
    lon: float


class SiteLayout(DBJson):
    layout: Optional[StrDict]
    position: SiteLayoutPosition


class SiteShiftConfig(DBJson):
    starts_at: datetime
    ends_at: datetime


class SiteConfig(DBJson):
    shifts: List[SiteShiftConfig]


class FreeDBJson(DBJson):
    class Config:
        extra = Extra.allow


class SensorReportData(FreeDBJson):
    pass


class SiteEventData(DBJson):
    pass
