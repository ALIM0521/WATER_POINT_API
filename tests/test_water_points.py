from fastapi.testclient import TestClient
from services.water_point.main import create_app
from services.water_point.store import WaterPointStore

client = TestClient(create_app(WaterPointStore()))

def test_create_and_read_water_point():
    response = client.post("/water-points", json={
        "name": "Village Centre Borehole", "village_id": "VIL-001",
        "latitude": 4.05, "longitude": 9.76, "water_type": "borehole"
    })
    assert response.status_code == 201
    created = response.json()
    assert created["status"] == "available"
    assert "id" in created and "created_at" in created
    fetched = client.get(f"/water-points/{created['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["name"] == "Village Centre Borehole"

def test_invalid_coordinates_are_rejected():
    response = client.post("/water-points", json={
        "name": "Bad point", "village_id": "VIL-001",
        "latitude": 120, "longitude": 9.76, "water_type": "well"
    })
    assert response.status_code == 422

def test_unknown_water_point_is_404():
    assert client.get("/water-points/unknown-id").status_code == 404
