import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

API_URL = "http://localhost:8000"


@pytest.fixture
def mock_user():
    return {
        "username": "john_doe",
        "email": "john@example.com",
        "password": "hashed_password_1",
    }


# @pytest.mark.skip(reason="Not implemented")
@pytest.mark.parametrize(
    "mock_user_changes,expected_status_code",
    [
        pytest.param({}, 200, id="Base case, no changes"),
        pytest.param({}, 400, id="Duplicate email"),
        pytest.param({"email": ""}, 422, id="Empty string email"),
        pytest.param({"email": None}, 422, id="Missing email"),
    ],
)
def test_post_user(mock_user, mock_user_changes, expected_status_code):
    user = mock_user.copy()
    user.update(mock_user_changes)

    endpoint = f"{API_URL}/users"
    response = client.post(endpoint, json=user)

    assert response.status_code == expected_status_code  # noqa: S101


@pytest.fixture
def mock_listing_base():
    return {
        "name": "Cozy Cottage",
        "description": "A cozy cottage in the countryside.",
        "beds": 2,
        "bedrooms": 1,
        "mean_rating": 4.5,
        "count_ratings": 10,
        "nightly_price": 100.0,
    }


@pytest.fixture
def mock_listing(mock_listing_base):
    mock_listing = mock_listing_base.copy()
    mock_listing["id"] = 1
    mock_listing["owner_id"] = 1

    return mock_listing
