import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from src.crud import UserDBClient
from src.schemas import UserCreate, UserRead

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


@app.post("/users", response_model=UserRead)
def add_user(user: UserCreate):
    # If user with email already exists, raise an error
    if user_db.check_record_exists("email", user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    # If user with username already exists, raise an error
    if user_db.check_record_exists("username", user.username):
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
    # Get user for user_id
    db_user = user_db.read(id=user_id)

    # If user does not exist, raise an error
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User ID {user_id} not found")

    # Update user fields
    user_db.update(id=user_id, **user.model_dump())

    # Return updated user
    return user_db.read(id=user_id)


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    # Get user based on user_id
    db_user = user_db.read(id=user_id)

    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User ID {user_id} not found")

    user_db.delete(id=user_id)


# @app.post("/users/{user_id}/properties", response_model=PropertyRead)
# def post_listing(user_id: int, property: PropertyCreate):
#     # Get user based on user_id
#     db_user = User.objects.filter(id=user_id).first()

#     if db_user is None:
#         raise HTTPException(status_code=404, detail=f"User ID {user_id} not found")

#     return Property.objects.create(property, owner=db_user)

# TODO(winlinworks): Update to use Django ORM
# @app.get("/listings", response_model=list[ListingRead])
# def get_listings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     return read_listings(db, skip, limit)

# TODO(winlinworks): Update to use Django ORM
# @app.get("/listings/{listing_id}", response_model=ListingRead)
# def get_listing(listing_id: int, db: Session = Depends(get_db)):
#     db_listing = read_listing(db, listing_id)
#     if db_listing is None:
#         raise HTTPException(
#             status_code=404, detail=f"Listing ID {listing_id} not found"
#         )
#     return db_listing

# TODO(winlinworks): Update to use Django ORM
# @app.put("/listings/{listing_id}", response_model=ListingRead)
# def put_listing(listing_id: int, listing: ListingRead, db: Session = Depends(get_db)):
#     # Verify if user exists
#     db_user = read_user(db, listing.owner_id)
#     if db_user is None:
#         raise HTTPException(
#             status_code=404, detail=f"User ID {listing.owner_id} not found"
#         )

#     # Verify if listing exists
#     db_listing = read_listing(db, listing_id)
#     if db_listing is None:
#         raise HTTPException(
#             status_code=404, detail=f"Listing ID {listing_id} not found"
#         )

#     return update_listing(db, listing_id, listing)

# TODO(winlinworks): Update to use Django ORM
# @app.delete("/listings/{listing_id}")
# def remove_listing(listing_id: int, db: Session = Depends(get_db)):
#     db_listing = read_listing(db, listing_id)
#     if db_listing is None:
#         raise HTTPException(
#             status_code=404, detail=f"Listing ID {listing_id} not found"
#         )

#     return delete_listing(db, listing_id)
