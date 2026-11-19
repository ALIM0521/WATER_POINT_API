from pydantic import BaseModel, Field

class RegionOut(BaseModel):
    id: str
    name: str

class VillageOut(BaseModel):
    id: str
    name: str
    region_id: str
    latitude: float
    longitude: float

class RegionList(BaseModel):
    regions: list[RegionOut]

class VillageList(BaseModel):
    villages: list[VillageOut]

class MapPoint(BaseModel):
    id: str
    name: str
    category: str
    latitude: float
    longitude: float

class MapData(BaseModel):
    locations: list[MapPoint]
