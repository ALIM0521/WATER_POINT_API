from fastapi import APIRouter, Depends, HTTPException, Request
from .schemas import RegionList, VillageList, VillageOut, MapData
from .store import LocationStore

router = APIRouter()

def get_store(request: Request) -> LocationStore:
    return request.app.state.store

@router.get("/regions", response_model=RegionList)
def list_regions(store: LocationStore = Depends(get_store)):
    return {"regions": store.list_regions()}

@router.get("/regions/{region_id}/villages", response_model=VillageList)
def villages_for_region(region_id: str, store: LocationStore = Depends(get_store)):
    try:
        return {"villages": store.villages_for_region(region_id)}
    except KeyError:
        raise HTTPException(404, f"Region {region_id} not found")

@router.get("/villages/{village_id}", response_model=VillageOut)
def get_village(village_id: str, store: LocationStore = Depends(get_store)):
    try:
        return store.get_village(village_id)
    except KeyError:
        raise HTTPException(404, f"Village {village_id} not found")

@router.get("/locations/map", response_model=MapData)
def map_locations(store: LocationStore = Depends(get_store)):
    return {"locations": store.map_locations()}
