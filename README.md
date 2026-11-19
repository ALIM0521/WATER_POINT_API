# Water Point Management System — API / FastAPI Microservices

This project implements **only the backend API layer**. It does not include a frontend,
GIS map interface, persistent database, authentication, or deployment configuration.

The structure follows the supplied MSA 302 Lab 2 methodology:
- API contract first (see `docs/api-contract.md`);
- Pydantic request and response schemas;
- FastAPI path operations;
- separate in-memory stores that own IDs and timestamps;
- explicit status transitions;
- response models as output whitelists;
- tests with FastAPI `TestClient`.

## Microservices and ports

| Service | Port | Main purpose |
|---|---:|---|
| Water Point Service | 8001 | Register and manage water points |
| Maintenance Ticket Service | 8002 | Report breakdowns and track repairs |
| Payment Service | 8003 | Record household contributions |
| Location Service | 8004 | Regions, villages and coordinates |

Each service is independently runnable and has its own in-memory store. The services are
separated by responsibility; this starter does not yet implement inter-service HTTP calls.
For example, the ticket service stores a `water_point_id` reference but does not call the
Water Point Service to verify it. That boundary is deliberately documented rather than hidden.

## 1. Open the project

Extract the ZIP, open the `WATER_POINT_API_MICROSERVICES` folder in VS Code, then open
Terminal → New Terminal.

## 2. Create a virtual environment

Windows PowerShell:
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Windows CMD:
```bat
py -m venv .venv
.venv\Scripts\activate.bat
```

Linux/macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies
```bash
python -m pip install -r requirements.txt
```

## 4. Start a microservice

Run each service in a separate terminal, with the virtual environment activated.

```bash
uvicorn services.water_point.main:app --reload --port 8001
uvicorn services.ticket.main:app --reload --port 8002
uvicorn services.payment.main:app --reload --port 8003
uvicorn services.location.main:app --reload --port 8004
```

Open the Swagger API documentation:
- Water points: `http://127.0.0.1:8001/docs`
- Tickets: `http://127.0.0.1:8002/docs`
- Payments: `http://127.0.0.1:8003/docs`
- Locations: `http://127.0.0.1:8004/docs`

Use `http://127.0.0.1` even when the computer has no internet connection. `localhost`
is local to your own computer.

## 5. Run tests
```bash
pytest -q
```

## 6. Example requests

Create a water point:
```bash
curl -X POST http://127.0.0.1:8001/water-points ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Village Centre Borehole\",\"village_id\":\"VIL-001\",\"latitude\":4.0511,\"longitude\":9.7679,\"water_type\":\"borehole\"}"
```

Create a maintenance ticket:
```bash
curl -X POST http://127.0.0.1:8002/tickets ^
  -H "Content-Type: application/json" ^
  -d "{\"water_point_id\":\"REPLACE-WITH-WATER-POINT-ID\",\"reported_by\":\"Village committee\",\"description\":\"Pump is not working\",\"priority\":\"high\"}"
```

Record a household contribution:
```bash
curl -X POST http://127.0.0.1:8003/payments ^
  -H "Content-Type: application/json" ^
  -d "{\"household_id\":\"HH-001\",\"amount\":1000,\"method\":\"cash\"}"
```

## Important limitations (same honesty principle as the lab)

- Data is stored in memory. Restarting a service resets its data.
- No authentication/authorization is implemented.
- No concurrency guarantees are provided for simultaneous writes.
- The services do not yet call each other or validate foreign IDs across services.
- GIS coordinates are stored and exposed by the API; displaying an interactive map is outside
  this API-only stage.
- Contributions are recorded, not processed through mobile money.
- A ticket workflow is tracked, but no technician notification is sent.

These are explicit boundaries for this API exercise, not completed features.
