from fastapi.testclient import TestClient
from services.ticket.main import create_app
from services.ticket.store import TicketStore

client = TestClient(create_app(TicketStore()))

def test_ticket_workflow():
    created = client.post("/tickets", json={
        "water_point_id": "WP-001", "reported_by": "Village committee",
        "description": "Pump is not working", "priority": "high"
    })
    assert created.status_code == 201
    ticket_id = created.json()["id"]
    assigned = client.put(f"/tickets/{ticket_id}/assign", json={"technician_id": "TECH-01"})
    assert assigned.status_code == 200
    assert assigned.json()["status"] == "assigned"
    assert client.patch(f"/tickets/{ticket_id}/status", json={"status": "in_progress"}).status_code == 200
    assert client.patch(f"/tickets/{ticket_id}/status", json={"status": "repaired"}).status_code == 200
    closed = client.post(f"/tickets/{ticket_id}/close")
    assert closed.status_code == 200
    assert closed.json()["status"] == "closed"

def test_invalid_ticket_transition_returns_409():
    created = client.post("/tickets", json={
        "water_point_id": "WP-002", "reported_by": "Resident",
        "description": "Broken tap"
    }).json()
    response = client.patch(f"/tickets/{created['id']}/status", json={"status": "closed"})
    assert response.status_code == 409
