import pytest
from fastapi.testclient import TestClient

from src.crud import create_user
from src.main import app
from src.schemas import UserCreate

client = TestClient(app)

API_URL = "http://localhost:8000"


@pytest.fixture(scope="function")
def mock_user():
    return {
        "username": "john_doe",
        "email": "john@example.com",
        "password": "hashed_password_1",
    }


class TestUser:
    @pytest.mark.parametrize(
        "mock_user_changes,expected_status_code",
        [
            pytest.param({}, 200, id="Valid user"),
            pytest.param({}, 400, id="Duplicate email"),
            pytest.param({"email": ""}, 422, id="Missing email"),
        ],
    )
    def test_post_user(self, mock_user, mock_user_changes, expected_status_code):
        user = mock_user
        user.update(mock_user_changes)

        endpoint = f"{API_URL}/users"
        response = client.post(endpoint, json=user)

        assert response.status_code == expected_status_code  # noqa: S101

    @pytest.mark.parametrize(
        "mock_user_id,expected_status_code",
        [
            pytest.param(1, 200, id="Valid user ID"),
            pytest.param(0, 404, id="Invalid user ID"),
        ],
    )
    def test_get_user(self, test_db, mock_user, mock_user_id, expected_status_code):
        # Create a user
        user = UserCreate(**mock_user)
        user = create_user(test_db, user)

        # Get the user
        endpoint = f"{API_URL}/users/{mock_user_id}"
        response = client.get(endpoint)

        assert response.status_code == expected_status_code  # noqa: S101

    @pytest.fixture
    def mock_update_user(self, mock_user):
        mock_update_user = mock_user.copy()
        mock_update_user.update(
            {
                "is_active": True,
                "listings": [],
            }
        )
        return mock_update_user

    @pytest.mark.parametrize(
        "mock_user_changes,expected_status_code",
        [
            pytest.param({}, 200, id="No updates"),
            pytest.param({"email": "john@update.com"}, 200, id="Update email"),
            pytest.param({"email": ""}, 422, id="Update email: empty string"),
        ],
    )
    def test_put_user(
        self,
        test_db,
        mock_user,
        mock_update_user,
        mock_user_changes,
        expected_status_code,
    ):
        # Update mock updated user
        update_user = mock_update_user.copy()
        update_user.update(mock_user_changes)

        # Create a user
        user = UserCreate(**mock_user)
        user = create_user(test_db, user)

        # Add the user ID to the update user
        update_user["id"] = user.id

        # Update the user
        endpoint = f"{API_URL}/users/{user.id}"
        response = client.put(endpoint, json=update_user)

        # If the update of valid email was successful, check the email
        if expected_status_code == 200:
            assert response.json()["email"] == update_user["email"]  # noqa: S101

        # Check the status code
        assert response.status_code == expected_status_code  # noqa: S101

    def test_delete_user(self, test_db, mock_user):
        # Create a user
        user = UserCreate(**mock_user)
        user = create_user(test_db, user)

        # Delete the user
        endpoint = f"{API_URL}/users/{user.id}"
        response = client.delete(endpoint)

        assert response.status_code == 200  # noqa: S101


@pytest.fixture
def mock_listing():
    return {
        "name": "Cozy Cottage",
        "description": "A cozy cottage in the countryside.",
        "beds": 2,
        "bedrooms": 1,
        "mean_rating": 4.5,
        "count_ratings": 10,
        "nightly_price": 100.0,
    }


class TestListing:
    @pytest.mark.parametrize(
        "mock_listing_changes,expected_status_code",
        [
            pytest.param({}, 200, id="Valid listing"),
            pytest.param({"name": ""}, 422, id="Missing name"),
        ],
    )
    def test_post_listing(
        self,
        test_db,
        mock_user,
        mock_listing,
        mock_listing_changes,
        expected_status_code,
    ):
        listing = mock_listing.copy()
        listing.update(mock_listing_changes)

        # Create a user
        user = UserCreate(**mock_user)
        user = create_user(test_db, user)

        # Create a listing
        listing_endpoint = f"{API_URL}/users/{user.id}/listings"
        response = client.post(listing_endpoint, json=listing)

        assert response.status_code == expected_status_code  # noqa: S101

    @pytest.mark.skip(reason="WIP")
    def test_read_listing(
        self,
        test_db,
        mock_user,
        mock_listing,
        mock_listing_changes,
        expected_status_code,
    ):
        pass
