import pytest
from fastapi.testclient import TestClient

from src.crud import create_listing, create_user
from src.main import app
from src.schemas import ListingCreate, UserCreate

client = TestClient(app)


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

        endpoint = "/users"
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
        endpoint = f"/users/{mock_user_id}"
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
        # Create a user
        user = UserCreate(**mock_user)
        user = create_user(test_db, user)

        # Update mock updated user
        update_user = mock_update_user.copy()
        update_user.update(mock_user_changes)

        # Add the user ID to the update user
        update_user["id"] = user.id

        # Update the user
        endpoint = f"/users/{user.id}"
        response = client.put(endpoint, json=update_user)

        # If the update of valid email was successful, check the email
        if expected_status_code == 200:
            assert response.json()["email"] == update_user["email"]  # noqa: S101

        # Check the status code
        assert response.status_code == expected_status_code  # noqa: S101

    @pytest.mark.parametrize(
        "mock_user_id,expected_status_code",
        [
            pytest.param(1, 200, id="Delete valid ID"),
            pytest.param(0, 404, id="Delete invalid ID"),
        ],
    )
    def test_delete_user(self, test_db, mock_user, mock_user_id, expected_status_code):
        # Create a user
        user = UserCreate(**mock_user)
        user = create_user(test_db, user)

        # Delete the user
        endpoint = f"/users/{mock_user_id}"
        response = client.delete(endpoint)

        assert response.status_code == expected_status_code  # noqa: S101


@pytest.fixture
def mock_listing():
    return {
        "name": "Cozy Cottage",
        "tagline": "A cozy cottage in the countryside.",
        "location": "Houston, TX",
        "image": "https://example.com/image.jpg",
        "price": 100.0,
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
        listing_endpoint = f"/users/{user.id}/listings"
        response = client.post(listing_endpoint, json=listing)

        assert response.status_code == expected_status_code  # noqa: S101

    @pytest.mark.parametrize(
        "mock_listing_id,expected_status_code",
        [
            pytest.param(1, 200, id="Valid listing ID"),
            pytest.param(0, 404, id="Invalid listing ID"),
        ],
    )
    def test_get_listing(
        self,
        test_db,
        mock_user,
        mock_listing,
        mock_listing_id,
        expected_status_code,
    ):
        # Create a user
        user = UserCreate(**mock_user)
        user = create_user(test_db, user)

        # Create a listing
        listing = ListingCreate(**mock_listing)
        listing = create_listing(test_db, listing, user.id)

        # Get the listing
        endpoint = f"/listings/{mock_listing_id}"
        response = client.get(endpoint)

        assert response.status_code == expected_status_code  # noqa: S101

    @pytest.fixture
    def mock_update_listing(self, mock_listing):
        return mock_listing.copy()

    @pytest.mark.parametrize(
        "mock_listing_changes,expected_status_code",
        [
            pytest.param({}, 200, id="No updates"),
            pytest.param(
                {"name": "A cozy house in the country"}, 200, id="Update valid name"
            ),
            pytest.param({"name": ""}, 422, id="Update invalid name"),
        ],
    )
    def test_update_listing(
        self,
        test_db,
        mock_user,
        mock_listing,
        mock_update_listing,
        mock_listing_changes,
        expected_status_code,
    ):
        # Create a user
        user = UserCreate(**mock_user)
        user = create_user(test_db, user)

        # Create a listing
        listing = ListingCreate(**mock_listing)
        listing = create_listing(test_db, listing, user.id)

        # Update the mock updated listing
        update_listing = mock_update_listing.copy()
        update_listing.update(mock_listing_changes)

        # Add the listing ID and owner ID to the update user
        update_listing["id"] = listing.id
        update_listing["owner_id"] = user.id

        # Update the listing
        endpoint = f"/listings/{listing.id}"
        response = client.put(endpoint, json=update_listing)

        # If the update of valid email was successful, check the email
        if expected_status_code == 200:
            assert response.json()["name"] == update_listing["name"]  # noqa: S101

        # Check the status code
        assert response.status_code == expected_status_code  # noqa: S101

    @pytest.mark.parametrize(
        "mock_listing_id,expected_status_code",
        [
            pytest.param(1, 200, id="Delete valid ID"),
            pytest.param(0, 404, id="Delete invalid ID"),
        ],
    )
    def test_delete_listing(
        self, test_db, mock_user, mock_listing, mock_listing_id, expected_status_code
    ):
        # Create a user
        user = UserCreate(**mock_user)
        user = create_user(test_db, user)

        # Create a listing
        listing = ListingCreate(**mock_listing)
        listing = create_listing(test_db, listing, user.id)

        # Delete the listing
        endpoint = f"/listings/{mock_listing_id}"
        response = client.delete(endpoint)

        assert response.status_code == expected_status_code  # noqa: S101
