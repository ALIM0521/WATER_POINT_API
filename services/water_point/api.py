from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response, status
from .schemas import (WaterPointCreate, WaterPointUpdate, WaterPointStatusUpdate,
                      WaterPointOut, WaterPointList, WaterPointStatus)
from .store import WaterPointStore, WaterPointNotFound

router = APIRouter()

def get_store(request: Request) -> WaterPointStore:
    return request.app.state.store

Store = Annotated[WaterPointStore, Depends(get_store)]

@router.get("/water-points", response_model=WaterPointList)
def list_water_points(store: Store,
    village_id: str | None = None,
    point_status: Annotated[WaterPointStatus | None, Query(alias="status")] = None,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0)):
    return {"water_points": store.list(village_id, point_status, limit, offset)}

@router.post("/water-points", response_model=WaterPointOut, status_code=status.HTTP_201_CREATED)
def create_water_point(payload: WaterPointCreate, store: Store):
    return store.add(payload.model_dump(exclude_none=True))

@router.get("/water-points/{water_point_id}", response_model=WaterPointOut)
def get_water_point(water_point_id: str, store: Store):
    try:
        return store.get(water_point_id)
    except WaterPointNotFound:
        raise HTTPException(404, f"Water point {water_point_id} not found")

@router.put("/water-points/{water_point_id}", response_model=WaterPointOut)
def update_water_point(water_point_id: str, payload: WaterPointUpdate, store: Store):
    try:
        return store.replace(water_point_id, payload.model_dump(exclude_none=True))
    except WaterPointNotFound:
        raise HTTPException(404, f"Water point {water_point_id} not found")

@router.patch("/water-points/{water_point_id}/status", response_model=WaterPointOut)
def update_status(water_point_id: str, payload: WaterPointStatusUpdate, store: Store):
    try:
        return store.set_status(water_point_id, payload.status)
    except WaterPointNotFound:
        raise HTTPException(404, f"Water point {water_point_id} not found")

@router.delete("/water-points/{water_point_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_water_point(water_point_id: str, store: Store):
    try:
        store.delete(water_point_id)
    except WaterPointNotFound:
        raise HTTPException(404, f"Water point {water_point_id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
