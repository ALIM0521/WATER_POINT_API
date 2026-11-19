# Water Point Management API — Contract v1 (project proposal)

This is the project-specific API contract implemented by this starter. Unlike the Orders API
used in the laboratory, this contract is designed for the water-point domain. The PDF supplies
the implementation methodology, not these domain-specific endpoint names or field rules.

## Common conventions
- JSON request and response bodies.
- UUIDs are minted by the service for water points, tickets and payments.
- UTC timestamps are minted by the store.
- Invalid path/body/query data: FastAPI/Pydantic `422`.
- A valid identifier that does not exist: `404` with `{"detail":"..."}`.
- Collection endpoints return an object containing the collection.
- `limit` is 1–100 (default 10); `offset` is >= 0 (default 0).
- Response models whitelist public fields.

## Water Point Service — port 8001
| Method | Path | Success | Purpose |
|---|---|---:|---|
| GET | `/water-points` | 200 | List; optional `village_id`, `status`, `limit`, `offset` |
| POST | `/water-points` | 201 | Register a water point |
| GET | `/water-points/{water_point_id}` | 200 | Retrieve one |
| PUT | `/water-points/{water_point_id}` | 200 | Replace editable details |
| DELETE | `/water-points/{water_point_id}` | 204 | Delete |
| PATCH | `/water-points/{water_point_id}/status` | 200 | Change operational status |

Water-point statuses: `available`, `breakdown`, `under_maintenance`, `unavailable`.
Water type: `borehole`, `well`, `tap`, `spring`, `other`.

## Maintenance Ticket Service — port 8002
| Method | Path | Success | Purpose |
|---|---|---:|---|
| GET | `/tickets` | 200 | List; optional `status`, `limit`, `offset` |
| POST | `/tickets` | 201 | Report a fault |
| GET | `/tickets/{ticket_id}` | 200 | Retrieve one |
| PUT | `/tickets/{ticket_id}/assign` | 200 | Assign a technician |
| PATCH | `/tickets/{ticket_id}/status` | 200 | Advance/update ticket status |
| POST | `/tickets/{ticket_id}/close` | 200 | Close a repaired ticket |

Ticket statuses: `reported`, `assigned`, `in_progress`, `repaired`, `closed`.
Priority: `low`, `medium`, `high`, `urgent`.
Allowed status transitions are declared in `services/ticket/states.py`.

## Payment Service — port 8003
| Method | Path | Success | Purpose |
|---|---|---:|---|
| GET | `/payments` | 200 | List payments |
| POST | `/payments` | 201 | Record a household contribution |
| GET | `/payments/{payment_id}` | 200 | Retrieve one payment |
| GET | `/households/{household_id}/payments` | 200 | List a household's payments |
| GET | `/payments/unpaid` | 200 | List household IDs marked unpaid |
| GET | `/funds/balance` | 200 | Sum recorded contributions |

Payment methods: `cash`, `mobile_money`, `bank_transfer`.
This first API records contributions only. It does not debit a mobile-money account.

## Location Service — port 8004
| Method | Path | Success | Purpose |
|---|---|---:|---|
| GET | `/regions` | 200 | List regions |
| GET | `/regions/{region_id}/villages` | 200 | List villages in a region |
| GET | `/villages/{village_id}` | 200 | Retrieve one village |
| GET | `/locations/map` | 200 | Return village/water-point coordinates available to this service |

The initial location service contains illustrative seed regions and villages. Coordinates are
sample data and must be replaced with verified field coordinates before real use.

## State transitions
- Water point: `available → breakdown → under_maintenance → available`.
  `unavailable` is an administrative status and can be set explicitly.
- Ticket: `reported → assigned → in_progress → repaired → closed`.
  The API refuses unsupported transitions with `409` because this project contract explicitly
  defines them. This is a project decision; it is not specified by the Orders API lab.
