"""
Integration tests for the FastAPI app. These tests are written to test the endpoints of the FastAPI app, including CRUD operations for the following resources:
- Users
- Profile
- Property

The tests are written using pytest and the FastAPI TestClient.
"""

import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


@pytest.fixture(scope="function")
def user_dict():
    return {
        "username": "john_doe",
        "email": "john@example.com",
        "password": "hashed_password_1",
    }


class TestUser:
    """
    Tests are coupled (e.g., test_post_user and test_get_user depend on the same data). I tried fixing this by moving django_db mark above each test, but couldn't get it working. Need to figure out how to decouple tests.
    """

    @pytest.mark.parametrize(
        "user_changes,expected_status_code",
        [
            pytest.param({}, 200, id="Valid user"),
            pytest.param({}, 400, id="Duplicate email"),
            pytest.param({"email": ""}, 422, id="Missing email"),
        ],
    )
    def test_post_user(self, db, user_dict, user_changes, expected_status_code):  # noqa: ARG002
        # Update dict for creating user
        user = user_dict.copy()
        user.update(user_changes)

        # Create user w/ endpoint
        endpoint = "/users"
        response = client.post(endpoint, json=user)

        assert response.status_code == expected_status_code  # noqa: S101

    @pytest.mark.parametrize(
        "user_id,expected_status_code",
        [
            pytest.param(1, 200, id="Valid user ID"),
            pytest.param(0, 404, id="Invalid user ID"),
        ],
    )
    def test_get_user(self, db, user_id, expected_status_code):  # noqa: ARG002
        # Get user w/ endpoint
        endpoint = f"/users/{user_id}"
        response = client.get(endpoint)

        assert response.status_code == expected_status_code  # noqa: S101

    @pytest.mark.parametrize(
        "user_id,user_changes,expected_status_code",
        [
            pytest.param(1, {}, 200, id="No updates"),
            pytest.param(
                1,
                {"username": "john_doe_update", "email": "john@update.com"},
                200,
                id="Update username and email",
            ),
            pytest.param(
                1,
                {"username": "", "email": ""},
                422,
                id="Update username and email: empty string",
            ),
        ],
    )
    def test_put_user(self, db, user_dict, user_id, user_changes, expected_status_code):  # noqa: ARG002
        # Update dict for updating user
        updated_user = user_dict.copy()
        updated_user.update(user_changes)

        # Add user ID
        updated_user["id"] = user_id

        # Update the user
        endpoint = f"/users/{user_id}"
        response = client.put(endpoint, json=updated_user)

        # Check the status code
        assert response.status_code == expected_status_code  # noqa: S101

        # If the expected status of update is success (200), check the value of updated field
        if expected_status_code == 200:
            assert response.json()["username"] == updated_user["username"]  # noqa: S101
            assert response.json()["email"] == updated_user["email"]  # noqa: S101

    @pytest.mark.parametrize(
        "user_id,expected_status_code",
        [
            pytest.param(1, 200, id="Delete valid ID"),
            pytest.param(0, 404, id="Delete invalid ID"),
        ],
    )
    def test_delete_user(self, db, user_id, expected_status_code):  # noqa: ARG002
        # Delete the user
        endpoint = f"/users/{user_id}"
        response = client.delete(endpoint)

        assert response.status_code == expected_status_code  # noqa: S101


# TODO(winlinworks): Update to use Django ORM
# @pytest.fixture
# def mock_listing():
#     return {
#         "name": "Cozy Cottage",
#         "tagline": "A cozy cottage in the countryside.",
#         "location": "Houston, TX",
#         "image": "https://example.com/image.jpg",
#         "price": 100.0,
#     }


# @pytest.mark.skip(reason="Needs update")
# class TestListing:
#     @pytest.mark.skip(reason="need to update w/ Django ORM")
#     @pytest.mark.parametrize(
#         "mock_listing_changes,expected_status_code",
#         [
#             pytest.param({}, 200, id="Valid listing"),
#             pytest.param({"name": ""}, 422, id="Missing name"),
#             pytest.param({}, 404, id="Owner not found"),
#         ],
#     )
#     def test_post_listing(
#         self,
#         test_db,
#         mock_user,
#         mock_listing,
#         mock_listing_changes,
#         expected_status_code,
#     ):
#         listing = mock_listing.copy()
#         listing.update(mock_listing_changes)

#         # Create a user
#         user = UserCreate(**mock_user)
#         user = create_user(test_db, user)

#         # If test case is for valid user record (not expecting 404 status code), set user ID to 0 (invalid)
#         if expected_status_code == 404:
#             user.id = 0

#         # Create a listing
#         listing_endpoint = f"/users/{user.id}/listings"
#         response = client.post(listing_endpoint, json=listing)

#         assert response.status_code == expected_status_code  # noqa: S101

#     @pytest.mark.skip(reason="need to update w/ Django ORM")
#     @pytest.mark.parametrize(
#         "mock_listing_id,expected_status_code",
#         [
#             pytest.param(1, 200, id="Valid listing ID"),
#             pytest.param(0, 404, id="Invalid listing ID"),
#         ],
#     )
#     def test_get_listing(
#         self,
#         test_db,
#         mock_user,
#         mock_listing,
#         mock_listing_id,
#         expected_status_code,
#     ):
#         # Create a user
#         user = UserCreate(**mock_user)
#         user = create_user(test_db, user)

#         # Create a listing
#         listing = ListingCreate(**mock_listing)
#         listing = create_listing(test_db, listing, user.id)

#         # Get the listing
#         endpoint = f"/listings/{mock_listing_id}"
#         response = client.get(endpoint)

#         assert response.status_code == expected_status_code  # noqa: S101

#     @pytest.mark.skip(reason="need to update w/ Django ORM")
#     @pytest.mark.parametrize(
#         "mock_listing_changes,expected_status_code",
#         [
#             pytest.param({}, 200, id="No updates"),
#             pytest.param(
#                 {"name": "A cozy house in the country"}, 200, id="Update valid name"
#             ),
#             pytest.param({"name": ""}, 422, id="Update invalid name"),
#             pytest.param({"id": 0, "owner_id": 1}, 404, id="Listing not found"),
#             pytest.param({"id": 1, "owner_id": 0}, 404, id="Owner not found"),
#         ],
#     )
#     def test_update_listing(
#         self,
#         test_db,
#         mock_user,
#         mock_listing,
#         mock_listing_changes,
#         expected_status_code,
#     ):
#         # Create a user
#         user = UserCreate(**mock_user)
#         user = create_user(test_db, user)

#         # Create a listing
#         listing = ListingCreate(**mock_listing)
#         listing = create_listing(test_db, listing, user.id)

#         # Update the mock updated listing for test case
#         updated_listing = mock_listing.copy()
#         updated_listing.update(mock_listing_changes)

#         # If test case is for valid listing and user records (not expecting 404 status code), match listing ID and owner ID of the updated listing to created listing
#         if expected_status_code != 404:
#             updated_listing["id"] = listing.id
#             updated_listing["owner_id"] = user.id

#         # Update the listing
#         endpoint = f"/listings/{listing.id}"
#         response = client.put(endpoint, json=updated_listing)

#         # If the update of valid listing was successful, check the name
#         if expected_status_code == 200:
#             assert response.json()["name"] == updated_listing["name"]  # noqa: S101

#         # Check the status code
#         assert response.status_code == expected_status_code  # noqa: S101

#     @pytest.mark.skip(reason="need to update w/ Django ORM")
#     @pytest.mark.parametrize(
#         "mock_listing_id,expected_status_code",
#         [
#             pytest.param(1, 200, id="Delete valid ID"),
#             pytest.param(0, 404, id="Delete invalid ID"),
#         ],
#     )
#     def test_delete_listing(
#         self, test_db, mock_user, mock_listing, mock_listing_id, expected_status_code
#     ):
#         # Create a user
#         user = UserCreate(**mock_user)
#         user = create_user(test_db, user)

#         # Create a listing
#         listing = ListingCreate(**mock_listing)
#         listing = create_listing(test_db, listing, user.id)

#         # Delete the listing
#         endpoint = f"/listings/{mock_listing_id}"
#         response = client.delete(endpoint)

#         assert response.status_code == expected_status_code  # noqa: S101
