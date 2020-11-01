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


class SiteShiftConfig(DBJson):
    starts_at: datetime
    ends_at: datetime


class SiteConfig(DBJson):
    shifts: Optional[List[SiteShiftConfig]]


class FreeDBJson(DBJson):
    class Config:
        extra = Extra.allow


class SensorReportData(FreeDBJson):
    pass


class SiteEventData(FreeDBJson):
    pass


class SiteLayout(FreeDBJson):
    pass
