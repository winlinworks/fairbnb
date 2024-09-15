import pytest
from fastapi.testclient import TestClient

from src.main import app, get_db
from tests.conftest import get_test_db

# Override the get_db dependency with get_test_db
app.dependency_overrides[get_db] = get_test_db

client = TestClient(app)

API_URL = "http://localhost:8000"


class TestUser:
    @pytest.fixture
    def mock_user(self):
        return {
            "username": "john_doe",
            "email": "john@example.com",
            "password": "hashed_password_1",
        }

    @pytest.mark.parametrize(
        "mock_user_changes,expected_status_code",
        [
            pytest.param({}, 200, id="Valid user"),
            pytest.param({}, 400, id="Duplicate email"),
            pytest.param({"email": ""}, 422, id="Empty string email"),
            pytest.param({"email": None}, 422, id="Missing email"),
        ],
    )
    def test_post_user(self, mock_user, mock_user_changes, expected_status_code):
        user = mock_user.copy()
        user.update(mock_user_changes)

        endpoint = f"{API_URL}/users"
        response = client.post(endpoint, json=user)

        assert response.status_code == expected_status_code  # noqa: S101

    @pytest.fixture
    def mock_update_user(self):
        return {
            "id": 1,
            "username": "john_doe",
            "email": "john@example.com",
            "password": "hashed_password_1",
            "is_active": True,
            "listings": [],
        }

    @pytest.mark.parametrize(
        "mock_user_changes,expected_status_code",
        [
            pytest.param({}, 200, id="No updates"),
            pytest.param({"email": "john@update.com"}, 200, id="Update email"),
            pytest.param({"email": ""}, 422, id="Update email: empty string"),
            pytest.param({"email": None}, 422, id="Update email: none"),
        ],
    )
    def test_put_user(self, mock_update_user, mock_user_changes, expected_status_code):
        update_user = mock_update_user.copy()
        update_user.update(mock_user_changes)

        user_id = update_user["id"]

        # Update the user
        endpoint = f"{API_URL}/users/{user_id}"
        response = client.put(endpoint, json=update_user)

        # If the update of valid email was successful, check the email
        if expected_status_code == 200:
            assert response.json()["email"] == update_user["email"]  # noqa: S101

        # Check the status code
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
