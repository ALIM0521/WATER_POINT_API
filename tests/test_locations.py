from fastapi.testclient import TestClient
from services.location.main import create_app

client = TestClient(create_app())

def test_regions_and_villages():
    regions = client.get("/regions")
    assert regions.status_code == 200
    villages = client.get("/regions/REG-LT/villages")
    assert villages.status_code == 200
    assert len(villages.json()["villages"]) >= 1

def test_unknown_region_is_404():
    assert client.get("/regions/NOPE/villages").status_code == 404
