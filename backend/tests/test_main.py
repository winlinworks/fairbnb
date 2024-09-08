import pytest
from fastapi.testclient import TestClient

from src.main import app, listings

client = TestClient(app)


@pytest.mark.parametrize(
    "id, expected_status, expected_detail",
    [
        (1, 200, None),
        (
            999,
            404,
            "Listing listing_id=999 not found",
        ),  # Assuming 999 is an ID that does not exist
    ],
)
def test_get_listing(id, expected_status, expected_detail):
    response = client.get(f"/listings/{id}")

    assert response.status_code == expected_status  # noqa: S101
    if expected_status != 200:
        assert response.json()["detail"] == expected_detail  # noqa: S101


def test_get_listings():
    response = client.get("/listings")

    assert response.status_code == 200  # noqa: S101
    assert len(response.json()) == len(listings)  # noqa: S101
