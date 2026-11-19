from fastapi.testclient import TestClient
from services.payment.main import create_app
from services.payment.store import PaymentStore

client = TestClient(create_app(PaymentStore()))

def test_record_contribution_and_balance():
    response = client.post("/payments", json={
        "household_id": "HH-001", "amount": 1500, "method": "cash"
    })
    assert response.status_code == 201
    assert response.json()["status"] == "recorded"
    balance = client.get("/funds/balance")
    assert balance.status_code == 200
    assert balance.json()["balance"] == 1500

def test_invalid_amount_is_rejected():
    response = client.post("/payments", json={
        "household_id": "HH-001", "amount": 0, "method": "cash"
    })
    assert response.status_code == 422
