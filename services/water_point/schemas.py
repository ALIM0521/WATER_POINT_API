from datetime import datetime
from enum import Enum
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field

class WaterPointStatus(str, Enum):
    available = "available"
    breakdown = "breakdown"
    under_maintenance = "under_maintenance"
    unavailable = "unavailable"

class WaterType(str, Enum):
    borehole = "borehole"
    well = "well"
    tap = "tap"
    spring = "spring"
    other = "other"

class WaterPointCreate(BaseModel):
    model_config = ConfigDict(extra="ignore")
    name: str = Field(min_length=2, max_length=100)
    village_id: str = Field(min_length=2, max_length=40)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    water_type: WaterType
    description: str | None = Field(default=None, max_length=300)

class WaterPointUpdate(WaterPointCreate):
    pass

class WaterPointStatusUpdate(BaseModel):
    status: WaterPointStatus

class WaterPointOut(BaseModel):
    id: UUID
    name: str
    village_id: str
    latitude: float
    longitude: float
    water_type: WaterType
    description: str | None = None
    status: WaterPointStatus
    created_at: datetime
    updated_at: datetime

class WaterPointList(BaseModel):
    water_points: list[WaterPointOut]
