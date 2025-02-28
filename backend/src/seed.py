# filepath: /Users/winlin/fairbnb/backend/src/seed.py
import json
from pathlib import Path

from src.fairbnb.models import Property, User
from src.schemas import PropertyCreate, UserCreate


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
        if not User.objects.filter(email=user.email).first():
            User.objects.create(**user.model_dump())


def seed_properties():
    # Load properties from JSON file
    properties_file = Path(__file__).parent / "data" / "properties.json"
    with open(properties_file) as f:
        properties = json.load(f)

    # Create properties
    for property_data in properties:
        owner = User.objects.filter(username=property_data["owner_username"]).first()
        property_data["owner_id"] = owner.id
        property = PropertyCreate(**property_data)
        if not Property.objects.filter(name=property.name).first():
            Property.objects.create(**property.model_dump())
