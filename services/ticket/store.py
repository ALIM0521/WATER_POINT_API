from datetime import datetime, timezone
from uuid import uuid4
from .schemas import TicketStatus
from .states import can_transition

class TicketNotFound(Exception):
    pass

class InvalidTicketTransition(Exception):
    pass

class TicketStore:
    def __init__(self, id_factory=uuid4, clock=lambda: datetime.now(timezone.utc)):
        self._items = {}
        self._id_factory = id_factory
        self._clock = clock

    def add(self, details):
        now = self._clock()
        item = {"id": self._id_factory(), **details, "assigned_to": None,
                "status": TicketStatus.reported, "created_at": now,
                "updated_at": now, "closed_at": None}
        self._items[str(item["id"])] = item
        return item.copy()

    def list(self, status=None, limit=10, offset=0):
        items = list(self._items.values())
        if status is not None:
            items = [x for x in items if x["status"] == status]
        items.sort(key=lambda x: x["created_at"], reverse=True)
        return [x.copy() for x in items[offset:offset + limit]]

    def _find(self, ticket_id):
        item = self._items.get(str(ticket_id))
        if item is None:
            raise TicketNotFound(str(ticket_id))
        return item

    def get(self, ticket_id):
        return self._find(ticket_id).copy()

    def assign(self, ticket_id, technician_id):
        item = self._find(ticket_id)
        if not can_transition(item["status"], TicketStatus.assigned):
            raise InvalidTicketTransition(f"Cannot assign a ticket in status {item['status']}")
        item["assigned_to"] = technician_id
        item["status"] = TicketStatus.assigned
        item["updated_at"] = self._clock()
        return item.copy()

    def set_status(self, ticket_id, target):
        item = self._find(ticket_id)
        if not can_transition(item["status"], target):
            raise InvalidTicketTransition(f"Cannot move ticket from {item['status']} to {target}")
        item["status"] = target
        item["updated_at"] = self._clock()
        if target == TicketStatus.closed:
            item["closed_at"] = item["updated_at"]
        return item.copy()
