import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

@pytest.mark.parametrize("id, expected_status, expected_detail", [
    (None, 400, "ID is required"),
    (999, 404, "Listing not found"),  # Assuming 999 is an ID that does not exist
])
def test_get_listing(id, expected_status, expected_detail):
    params = {"id": id} if id is not None else {}
    response = client.get("/listing", params=params)
    
    assert response.status_code == expected_status
    assert response.json()["detail"] == expected_detail