from datetime import datetime, timezone
from uuid import uuid4
from .schemas import WaterPointStatus

class WaterPointNotFound(Exception):
    pass

class WaterPointStore:
    def __init__(self, id_factory=uuid4, clock=lambda: datetime.now(timezone.utc)):
        self._items = {}
        self._id_factory = id_factory
        self._clock = clock

    def add(self, details: dict) -> dict:
        now = self._clock()
        item = {"id": self._id_factory(), **details, "status": WaterPointStatus.available,
                "created_at": now, "updated_at": now}
        self._items[str(item["id"])] = item
        return item.copy()

    def list(self, village_id=None, status=None, limit=10, offset=0):
        items = list(self._items.values())
        if village_id is not None:
            items = [x for x in items if x["village_id"] == village_id]
        if status is not None:
            items = [x for x in items if x["status"] == status]
        items.sort(key=lambda x: x["created_at"], reverse=True)
        return [x.copy() for x in items[offset:offset + limit]]

    def _find(self, water_point_id):
        item = self._items.get(str(water_point_id))
        if item is None:
            raise WaterPointNotFound(str(water_point_id))
        return item

    def get(self, water_point_id):
        return self._find(water_point_id).copy()

    def replace(self, water_point_id, details):
        item = self._find(water_point_id)
        item.update(details)
        item["updated_at"] = self._clock()
        return item.copy()

    def set_status(self, water_point_id, status):
        item = self._find(water_point_id)
        item["status"] = status
        item["updated_at"] = self._clock()
        return item.copy()

    def delete(self, water_point_id):
        self._find(water_point_id)
        del self._items[str(water_point_id)]
