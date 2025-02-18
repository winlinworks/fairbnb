# filepath: /Users/winlin/fairbnb/backend/src/seed.py
import json
from pathlib import Path

from src.crud import PropertyDBClient, UserDBClient
from src.schemas import PropertyCreate, UserCreate

user_db = UserDBClient()
property_db = PropertyDBClient()


def seed_database():
    seed_users()
    seed_properties()


def seed_users():
    # Load users from JSON file
    users_file = Path(__file__).parent / "data" / "users.json"
    with open(users_file) as f:
        users = json.load(f)

    # Create users
    for user_data in users:
        user = UserCreate(**user_data)
        if not user_db.check_record_exists(email=user.email):
            user_db.create(**user.model_dump())


def seed_properties():
    # Load properties from JSON file
    properties_file = Path(__file__).parent / "data" / "properties.json"
    with open(properties_file) as f:
        properties = json.load(f)

    # Create properties
    for property_data in properties:
        owner = user_db.read(username=property_data["owner_username"])
        property_data["owner_id"] = owner.id
        property = PropertyCreate(**property_data)
        if not property_db.check_record_exists(name=property.name):
            property_db.create(**property.model_dump())
