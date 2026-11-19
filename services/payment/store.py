from datetime import datetime, timezone
from uuid import uuid4

class PaymentNotFound(Exception):
    pass

class PaymentStore:
    def __init__(self, id_factory=uuid4, clock=lambda: datetime.now(timezone.utc)):
        self._items = {}
        self._id_factory = id_factory
        self._clock = clock
        # Illustrative list of households expected to contribute.
        self._households = {"HH-001", "HH-002", "HH-003"}

    def add(self, details):
        item = {"id": self._id_factory(), **details,
                "payment_date": self._clock(), "status": "recorded"}
        self._items[str(item["id"])] = item
        self._households.add(details["household_id"])
        return item.copy()

    def list(self, limit=10, offset=0):
        items = sorted(self._items.values(), key=lambda x: x["payment_date"], reverse=True)
        return [x.copy() for x in items[offset:offset + limit]]

    def get(self, payment_id):
        item = self._items.get(str(payment_id))
        if item is None:
            raise PaymentNotFound(str(payment_id))
        return item.copy()

    def household_payments(self, household_id):
        items = [x.copy() for x in self._items.values() if x["household_id"] == household_id]
        items.sort(key=lambda x: x["payment_date"], reverse=True)
        return items

    def unpaid_households(self):
        paid = {x["household_id"] for x in self._items.values()}
        return sorted(self._households - paid)

    def balance(self):
        return sum((x["amount"] for x in self._items.values()), start=0)
