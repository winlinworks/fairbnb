"""
Integration tests for the FastAPI app. These tests are written to test the endpoints of the FastAPI app, including CRUD operations for the following resources:
- Users
- Profile
- Property

The tests are written using pytest and the FastAPI TestClient.
"""

from typing import List, Optional

import pytest
from django.contrib.auth.models import Group, User
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


@pytest.fixture(scope="function")
def user1_dict():
    return {
        "username": "john_doe",
        "email": "john@test.com",
        "password": "hashed_password_1",
    }


def create_user(
    username: str,
    password: Optional[str] = None,
    first_name: Optional[str] = "first name",
    last_name: Optional[str] = "last name",
    email: Optional[str] = "foo@bar.com",
    is_staff: str = False,
    is_superuser: str = False,
    is_active: str = True,
    groups: List[Group] = [],
) -> User:
    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
        email=email,
        is_staff=is_staff,
        is_superuser=is_superuser,
        is_active=is_active,
    )
    user.groups.add(*groups)
    return user


class TestUser:
    """
    Tests are coupled (e.g., test_post_user and test_get_user depend on the same data). Will try transactional_db fixture to isolate tests.
    """

    @pytest.mark.parametrize(
        "user_changes,expected_status_code",
        [
            pytest.param(
                {"username": "jane_doe", "email": "jane@test.com"}, 200, id="Valid user"
            ),
            pytest.param({"email": "jane@test.com"}, 400, id="Duplicate username"),
            pytest.param({"username": "jane_doe"}, 400, id="Duplicate email"),
            pytest.param({"email": ""}, 422, id="Missing email"),
        ],
    )
    def test_post_user(
        self,
        transactional_db,  # noqa: ARG002
        user1_dict,
        user_changes,
        expected_status_code,
    ):
        # Seed 1st user for duplicate test cases
        create_user(**user1_dict)

        # Create dict for 2nd user
        user2 = user1_dict.copy()
        user2.update(user_changes)

        # Create 2nd user w/ endpoint
        endpoint = "/users"
        response = client.post(endpoint, json=user2)

        assert response.status_code == expected_status_code  # noqa: S101

    @pytest.mark.parametrize(
        "user_id,expected_status_code",
        [
            pytest.param(None, 200, id="Valid user ID"),
            pytest.param(0, 404, id="Invalid user ID"),
        ],
    )
    def test_get_user(
        self,
        transactional_db,  # noqa: ARG002
        user1_dict,
        user_id,
        expected_status_code,
    ):
        # Create user
        user = create_user(**user1_dict)

        # Set user ID to created user ID to test endpoint
        user_id = user.id if user_id is None else user_id

        # Get user w/ endpoint
        endpoint = f"/users/{user_id}"
        response = client.get(endpoint)

        assert response.status_code == expected_status_code  # noqa: S101

    @pytest.mark.parametrize(
        "user_id,user_changes,expected_status_code",
        [
            pytest.param(None, {}, 200, id="No updates"),
            pytest.param(
                None,
                {"username": "john_doe_update", "email": "john@update.com"},
                200,
                id="Update username and email",
            ),
            pytest.param(
                None,
                {"username": "", "email": ""},
                422,
                id="Update username and email: empty string",
            ),
        ],
    )
    def test_put_user(
        self,
        transactional_db,  # noqa: ARG002
        user1_dict,
        user_id,
        user_changes,
        expected_status_code,
    ):
        # Create user
        user = create_user(**user1_dict)

        # Create dict for updated user
        updated_user1 = user1_dict.copy()
        updated_user1.update(user_changes)

        # Set user ID to created user ID to test endpoint
        user_id = user.id if user_id is None else user_id

        # Update the user
        endpoint = f"/users/{user_id}"
        response = client.put(endpoint, json=updated_user1)

        # Check status code
        assert response.status_code == expected_status_code  # noqa: S101

        # If expected status of update is success (200), check value of updated field
        if expected_status_code == 200:
            assert response.json()["username"] == updated_user1["username"]  # noqa: S101
            assert response.json()["email"] == updated_user1["email"]  # noqa: S101

    @pytest.mark.parametrize(
        "user_id,expected_status_code",
        [
            pytest.param(None, 200, id="Delete valid ID"),
            pytest.param(0, 404, id="Delete invalid ID"),
        ],
    )
    def test_delete_user(
        self,
        transactional_db,  # noqa: ARG002
        user1_dict,
        user_id,
        expected_status_code,
    ):
        # Create user
        user = create_user(**user1_dict)

        # Set user ID to created user ID to test endpoint
        user_id = user.id if user_id is None else user_id

        # Delete user
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
