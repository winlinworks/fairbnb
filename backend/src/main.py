import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from src.crud import PropertyDBClient, UserDBClient
from src.schemas import PropertyCreate, PropertyRead, UserCreate, UserRead

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    logger.info("startup: triggered")
    yield
    logger.info("shutdown: triggered")


app = FastAPI(lifespan=lifespan)

# Create a user DB client
user_db = UserDBClient()

# Create a property DB client
property_db = PropertyDBClient()


@app.post("/users", response_model=UserRead)
def add_user(user: UserCreate):
    # If user with email already exists, raise an error
    if user_db.check_record_exists(email=user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    # If user with username already exists, raise an error
    if user_db.check_record_exists(username=user.username):
        raise HTTPException(status_code=400, detail="Username already registered")

    # Else, create the user and return response with user id and status code
    user_id = user_db.create(**user.model_dump())
    logger.info("User created with ID: %s", user_id)
    return user_db.read(id=user_id)


@app.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int):
    # Get user for user_id
    db_user = user_db.read(id=user_id)

    # If user does not exist, raise an error
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User ID {user_id} not found")

    return db_user


@app.put("/users/{user_id}", response_model=UserRead)
def update_user(user_id: int, user: UserCreate):
    # If user does not exist, raise an error
    if not user_db.check_record_exists(id=user_id):
        raise HTTPException(status_code=404, detail=f"User ID {user_id} not found")

    # Update user
    user_db.update(id=user_id, **user.model_dump())

    # Return updated user
    return user_db.read(id=user_id)


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    # If user does not exist, raise an error
    if not user_db.check_record_exists(id=user_id):
        raise HTTPException(status_code=404, detail=f"User ID {user_id} not found")

    # Delete user
    user_db.delete(id=user_id)
    logger.info("User deleted with ID: %s", user_id)
    return {"detail": f"User ID {user_id} deleted successfully"}


@app.post("/users/{user_id}/properties", response_model=PropertyRead)
def add_property(user_id: int, property: PropertyCreate):
    # Get user based on user_id
    if not user_db.check_record_exists(id=user_id):
        raise HTTPException(status_code=400, detail=f"User ID {user_id} not found")

    # Create property and return response with property id and status code
    property_id = property_db.create(**property.model_dump())
    logger.info("Property created with ID: %s", property_id)

    return property_db.read(id=property_id)


@app.get("/properties/{property_id}", response_model=PropertyRead)
def get_property(property_id: int):
    # Get roperty for listing_id
    db_property = property_db.read(id=property_id)

    # If property does not exist, raise an error
    if db_property is None:
        raise HTTPException(
            status_code=404, detail=f"Property ID {property_id} not found"
        )

    return db_property


@app.put("/properties/{property_id}", response_model=PropertyRead)
def update_property(property_id: int, property: PropertyCreate):
    # If property does not exist, raise an error
    if not property_db.check_record_exists(id=property_id):
        raise HTTPException(
            status_code=404, detail=f"Listing ID {property_id} not found"
        )

    # If owner does not exist, raise an error
    if not user_db.check_record_exists(id=property.owner_id):
        raise HTTPException(
            status_code=422, detail=f"Owner ID {property.owner_id} not found"
        )

    # Update property fields
    property_db.update(id=property_id, **property.model_dump())

    return property_db.read(id=property_id)


@app.delete("/properties/{property_id}")
def delete_property(property_id: int):
    # If property does not exist, raise an error
    if not property_db.check_record_exists(id=property_id):
        raise HTTPException(
            status_code=404, detail=f"Listing ID {property_id} not found"
        )

    # Delete property
    property_db.delete(id=property_id)
    logger.info("Property deleted with ID: %s", property_id)
    return {"detail": f"Property ID {property_id} deleted successfully"}
