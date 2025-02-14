import logging
import sys
from contextlib import asynccontextmanager

# from sqlalchemy.orm import Session
# import models
from django.contrib.auth.models import User
from fastapi import FastAPI, HTTPException

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


@app.post("/users", response_model=UserRead)
def create_user(user: UserCreate):
    # If user with email already exists, raise an error
    db_user = User.objects.filter(email=user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # If user with username already exists, raise an error
    db_user = User.objects.filter(username=user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Else, create the user
    return User.objects.create_user(
        username=user.username, email=user.email, password=user.password
    )


# TODO(winlinworks): Update to use Django ORM
# @app.get("/users", response_model=list[UserRead])
# def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     return read_users(db, skip, limit)


@app.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int):
    db_user = User.objects.filter(id=user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User ID {user_id} not found")
    return db_user


@app.put("/users/{user_id}", response_model=UserRead)
def update_user(user_id: int, user: UserCreate):
    # Get user based on user_id
    db_user = User.objects.filter(id=user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User ID {user_id} not found")

    # Update user fields and save user
    db_user.username = user.username
    db_user.email = user.email
    db_user.password = user.password
    db_user.save()

    return db_user


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    # Get user based on user_id
    db_user = User.objects.filter(id=user_id).first()

    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User ID {user_id} not found")

    db_user.delete()


# TODO(winlinworks): Update to use Django ORM
# @app.post("/users/{user_id}/listings", response_model=ListingRead)
# def post_listing(user_id: int, listing: ListingCreate, db: Session = Depends(get_db)):
#     db_user = read_user(db, user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail=f"User ID {user_id} not found")

#     return create_listing(db, listing, user_id)

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
