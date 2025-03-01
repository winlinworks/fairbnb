"""
Integration tests for the FastAPI app. These tests are written to test the endpoints of the FastAPI app, including CRUD operations for the following resources:
- User
- Profile
- Property

The tests are written using pytest and the FastAPI TestClient.
"""

from typing import Optional

import pytest
from django.contrib.auth.models import Group
from fastapi.testclient import TestClient

from src.db.properties.models import Property
from src.db.users.models import User
from src.main import app

client = TestClient(app)


@pytest.fixture(scope="function")
def user1_dict():
    return {
        "email": "john@test.com",
        "password": "hashed_password_1",
    }


@pytest.fixture(scope="function")
def user2_dict():
    return {
        "email": "jane@test.com",
        "password": "hashed_password_2",
    }


def create_user(
    password: Optional[str] = None,
    first_name: Optional[str] = "first name",
    last_name: Optional[str] = "last name",
    email: Optional[str] = "foo@bar.com",
    is_staff: str = False,
    is_superuser: str = False,
    is_active: str = True,
    groups: list[Group] = [],
) -> User:
    user = User.objects.create_user(
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
            pytest.param({"email": "jane@test.com"}, 200, id="Valid user"),
            pytest.param({}, 400, id="Duplicate email"),
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
                {"email": "john@update.com"},
                200,
                id="Update email",
            ),
            pytest.param(
                None,
                {"email": ""},
                422,
                id="Update email: empty string",
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


@pytest.fixture
def property1_dict():
    return {
        "name": "Cozy Cottage",
        "tagline": "A cozy cottage in the countryside.",
        "category": "Cottage",
        "image": "https://example.com/image.jpg",
        "location": "Houston, TX",
        "description": "A cozy cottage in the countryside.",
        "guests": 4,
        "bedrooms": 2,
        "beds": 2,
        "baths": 1,
        "amenities": ["wifi", "kitchen", "parking"],
        "price": 100.0,
        "owner_id": 1,
    }


def create_property(
    name: str,
    tagline: Optional[str] = None,
    category: Optional[str] = None,
    image: Optional[str] = None,
    location: Optional[str] = None,
    description: Optional[str] = None,
    guests: Optional[int] = None,
    bedrooms: Optional[int] = None,
    beds: Optional[int] = None,
    baths: Optional[int] = None,
    amenities: list[str] = [],
    price: Optional[float] = None,
    owner_id: int = 1,
) -> Property:
    return Property.objects.create(
        name=name,
        tagline=tagline,
        category=category,
        image=image,
        location=location,
        description=description,
        guests=guests,
        bedrooms=bedrooms,
        beds=beds,
        baths=baths,
        amenities=amenities,
        price=price,
        owner_id=owner_id,
    )


# @pytest.mark.skip(reason="Needs update")
class TestProperty:
    @pytest.mark.parametrize(
        "property_changes,expected_status_code",
        [
            pytest.param({}, 200, id="Valid property"),
            pytest.param({"name": ""}, 422, id="Missing property name"),
            pytest.param({}, 404, id="Owner not found"),
        ],
    )
    def test_post_property(
        self,
        transactional_db,  # noqa: ARG002
        user1_dict,
        property1_dict,
        property_changes,
        expected_status_code,
    ):
        # If test case is for valid user (not expecting 400 status code)
        if expected_status_code != 404:
            # Create use and set user ID to created user ID
            user = create_user(**user1_dict)
            user_id = user.id

            # Create dict for updated property and set owner ID to created user ID
            property1_dict.update(property_changes)
            property1_dict["owner_id"] = user_id

            # Create property
            create_property(
                **property1_dict
            )  # Django automatically updates owner foreign key based on owner_id, so no need to set owner explicitly?

        # Else, set user ID to 0 for invalid user
        else:
            user_id = 0

        # Create property w/ endpoint
        property_endpoint = f"/users/{user_id}/properties"
        response = client.post(property_endpoint, json=property1_dict)

        assert response.status_code == expected_status_code  # noqa: S101

    @pytest.mark.parametrize(
        "property_id,expected_status_code",
        [
            pytest.param(None, 200, id="Valid property ID"),
            pytest.param(0, 404, id="Invalid property ID"),
        ],
    )
    def test_get_property(
        self,
        transactional_db,  # noqa: ARG002
        user1_dict,
        property1_dict,
        property_id,
        expected_status_code,
    ):
        # If test case is for valid property ID, create user and property
        if expected_status_code == 200:
            # Create user and set property owner ID to created user ID
            user = create_user(**user1_dict)
            property1_dict["owner_id"] = user.id

            # Create property and set property ID to created property ID if test case is for valid property ID
            property = create_property(**property1_dict)
            property_id = property.id

        # Get property with endpoint
        endpoint = f"/properties/{property_id}"
        response = client.get(endpoint)

        assert response.status_code == expected_status_code  # noqa: S101

    @pytest.mark.parametrize(
        "property_changes,expected_status_code",
        [
            pytest.param({}, 200, id="No updates"),
            pytest.param(
                {"name": "A cozy house in the country"}, 200, id="Update valid name"
            ),
            pytest.param({"name": ""}, 422, id="Update invalid name"),
            # pytest.param({"owner_id": 2}, 200, id="Update valid owner"),
            # pytest.param({"owner_id": 0}, 422, id="Update invalid owner"),
        ],
    )
    def test_put_property_fields(
        self,
        transactional_db,  # noqa: ARG002
        user1_dict,
        property1_dict,
        property_changes,
        expected_status_code,
    ):
        # If test case is for valid property and valid owner (not expecting 4* status code), create user and property
        if expected_status_code == 200:
            # Create user and set property owner ID to created user ID
            user1 = create_user(**user1_dict)
            property1_dict["owner_id"] = user1.id

            # Create property and set property ID to created property ID
            property = create_property(**property1_dict)
            property_id = property.id

        # Else, set property ID to 0 for invalid property
        else:
            property_id = 0

        # Create dict for updated property and set property ID to created property ID
        updated_property1_dict = property1_dict.copy()
        updated_property1_dict.update(property_changes)

        # Update property
        endpoint = f"/properties/{property_id}"
        response = client.put(endpoint, json=updated_property1_dict)

        # Check the status code
        assert response.status_code == expected_status_code  # noqa: S101

    @pytest.mark.parametrize(
        "property_changes,expected_status_code",
        [
            pytest.param({}, 200, id="Update valid owner"),
            pytest.param({"owner_id": 0}, 422, id="Update invalid owner"),
        ],
    )
    def test_put_property_owner(
        self,
        transactional_db,  # noqa: ARG002
        user1_dict,
        user2_dict,
        property1_dict,
        property_changes,
        expected_status_code,
    ):
        # Create user and set property owner ID to created user ID
        user1 = create_user(**user1_dict)
        property1_dict["owner_id"] = user1.id

        # Create property and set property ID to created property ID
        property = create_property(**property1_dict)
        property_id = property.id

        # Create 2nd user and set updated property owner ID to created user ID
        user2 = create_user(**user2_dict)

        # If test case is for valid updated owner (not expecting 4* status code)
        if expected_status_code == 200:
            # Set updated property owner ID to created user ID
            property_changes["owner_id"] = user2.id

        # Create dict for updated property and set property ID to created property ID
        updated_property1_dict = property1_dict.copy()
        updated_property1_dict.update(property_changes)

        # Update property
        endpoint = f"/properties/{property_id}"
        response = client.put(endpoint, json=updated_property1_dict)

        # Check the status code
        assert response.status_code == expected_status_code  # noqa: S101

    @pytest.mark.parametrize(
        "property_id,expected_status_code",
        [
            pytest.param(None, 200, id="Delete valid ID"),
            pytest.param(0, 404, id="Delete invalid ID"),
        ],
    )
    def test_delete_listing(
        self,
        transactional_db,  # noqa: ARG002
        user1_dict,
        property1_dict,
        property_id,
        expected_status_code,
    ):
        # Create user and set property owner ID to created user ID
        user1 = create_user(**user1_dict)
        property1_dict["owner_id"] = user1.id

        # Create property and set property ID to created property ID
        property = create_property(**property1_dict)

        # If test case is for valid property ID, set property ID to created property ID
        property_id = property.id if expected_status_code == 200 else property_id

        # Delete the listing
        endpoint = f"/properties/{property_id}"
        response = client.delete(endpoint)

        assert response.status_code == expected_status_code  # noqa: S101
