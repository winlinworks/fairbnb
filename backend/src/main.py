import logging
import os
import sys
from contextlib import asynccontextmanager

import django
from asgiref.sync import sync_to_async
from django.core.wsgi import get_wsgi_application
from fastapi import FastAPI, HTTPException
from fastapi.middleware.wsgi import WSGIMiddleware

# Initialize Django app before importing models
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.fairbnb.settings")
django.setup()

# from src.crud import PropertyDBClient, UserDBClient  # noqa: E402
from src.fairbnb.models import Property, User  # noqa: E402
from src.fairbnb.settings import DEBUG  # noqa: E402
from src.schemas import PropertyCreate, PropertyRead, UserCreate, UserRead  # noqa: E402
from src.seed import seed_database  # noqa: E402

logger = logging.getLogger(__name__)

if DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    logger.info("startup: triggered")

    # Seed database if in DEBUG mode
    if DEBUG:
        await sync_to_async(seed_database)()
        logger.info("Database seeded")
    yield
    logger.info("shutdown: triggered")


app = FastAPI(lifespan=lifespan)

# Mount the Django WSGI application
django_app = get_wsgi_application()
app.mount("/django", WSGIMiddleware(django_app))


@app.post("/users", response_model=UserRead)
def add_user(user: UserCreate):
    # If user with email already exists, raise an error
    if User.objects.filter(email=user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # If user with username already exists, raise an error
    if User.objects.filter(username=user.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")

    # Else, create user
    user = User.objects.create(**user.model_dump())
    logger.info("User created with ID: %s", user.id)

    return user


@app.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int):
    # Get user for user_id
    db_user = User.objects.filter(id=user_id).first()

    # If user does not exist, raise an error
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User ID {user_id} not found")

    return db_user


@app.get("/users", response_model=list[UserRead])
def get_users():
    # Get all users
    return User.objects.all()


@app.put("/users/{user_id}", response_model=UserRead)
def update_user(user_id: int, user: UserCreate):
    # Get user
    db_user = User.objects.filter(id=user_id).first()

    # If user does not exist, raise an error
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User ID {user_id} not found")

    # Update user
    for key, value in user.model_dump().items():
        setattr(db_user, key, value)
    db_user.save()

    return db_user


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    # Get user
    db_user = User.objects.filter(id=user_id).first()

    # If user does not exist, raise an error
    if not db_user:
        raise HTTPException(status_code=404, detail=f"User ID {user_id} not found")

    # Delete user
    db_user.delete()
    logger.info("User deleted with ID: %s", user_id)

    return {"detail": f"User ID {user_id} deleted successfully"}


@app.post("/users/{user_id}/properties", response_model=PropertyRead)
def add_property(user_id: int, property: PropertyCreate):
    # Get user based on user_id
    if not User.objects.filter(id=user_id).first():
        raise HTTPException(status_code=404, detail=f"User ID {user_id} not found")

    # Create property
    property = Property.objects.create(**property.model_dump())
    logger.info("Property created with ID: %s", property.id)

    return property


@app.get("/properties", response_model=list[PropertyRead])
def get_properties():
    # Get all properties
    return Property.objects.all()


@app.get("/properties/{property_id}", response_model=PropertyRead)
def get_property(property_id: int):
    # Get roperty for listing_id
    db_property = Property.objects.filter(id=property_id).first()

    # If property does not exist, raise an error
    if not db_property:
        raise HTTPException(
            status_code=404, detail=f"Property ID {property_id} not found"
        )

    return db_property


@app.put("/properties/{property_id}", response_model=PropertyRead)
def update_property(property_id: int, property: PropertyCreate):
    # Get property
    db_property = Property.objects.filter(id=property_id).first()

    # If property does not exist, raise an error
    if not db_property:
        raise HTTPException(
            status_code=404, detail=f"Listing ID {property_id} not found"
        )

    # If owner of updated property does not exist, raise an error
    if not User.objects.filter(id=property.owner_id).first():
        raise HTTPException(
            status_code=422, detail=f"Owner ID {property.owner_id} not found"
        )

    # Update property fields
    for key, value in property.model_dump().items():
        setattr(db_property, key, value)
    db_property.save()

    return db_property


@app.delete("/properties/{property_id}")
def delete_property(property_id: int):
    # Get property
    db_property = Property.objects.filter(id=property_id).first()

    # If property does not exist, raise an error
    if not db_property:
        raise HTTPException(
            status_code=404, detail=f"Listing ID {property_id} not found"
        )

    # Delete property
    db_property.delete()
    logger.info("Property deleted with ID: %s", property_id)

    return {"detail": f"Property ID {property_id} deleted successfully"}
