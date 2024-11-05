import logging
import sys
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from src.crud import (
    create_listing,
    create_user,
    delete_listing,
    delete_user,
    read_listing,
    read_listings,
    read_user,
    read_user_by_email,
    read_users,
    update_listing,
    update_user,
)
from src.db import get_db
from src.schemas import ListingCreate, ListingRead, UserCreate, UserRead

load_dotenv()

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
def post_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = read_user_by_email(db, user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user)


@app.get("/users", response_model=list[UserRead])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return read_users(db, skip, limit)


@app.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = read_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User ID {user_id} not found")
    return db_user


@app.put("/users/{user_id}", response_model=UserRead)
def put_user(user_id: int, user: UserRead, db: Session = Depends(get_db)):
    db_user = read_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User ID {user_id} not found")

    return update_user(db, user_id, user)


@app.delete("/users/{user_id}")
def remove_user(user_id: int, db: Session = Depends(get_db)):
    db_user = read_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User ID {user_id} not found")

    return delete_user(db, user_id)


@app.post("/users/{user_id}/listings", response_model=ListingRead)
def post_listing(user_id: int, listing: ListingCreate, db: Session = Depends(get_db)):
    return create_listing(db, listing, user_id)


@app.get("/listings", response_model=list[ListingRead])
def get_listings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return read_listings(db, skip, limit)


@app.get("/listings/{listing_id}", response_model=ListingRead)
def get_listing(listing_id: int, db: Session = Depends(get_db)):
    db_listing = read_listing(db, listing_id)
    if db_listing is None:
        raise HTTPException(
            status_code=404, detail=f"Listing ID {listing_id} not found"
        )
    return db_listing


@app.put("/listings/{listing_id}", response_model=ListingRead)
def put_listing(listing_id: int, listing: ListingRead, db: Session = Depends(get_db)):
    db_listing = read_listing(db, listing_id)
    if db_listing is None:
        raise HTTPException(
            status_code=404, detail=f"Listing ID {listing_id} not found"
        )

    return update_listing(db, listing_id, listing)


@app.delete("/listings/{listing_id}")
def remove_listing(listing_id: int, db: Session = Depends(get_db)):
    db_listing = read_listing(db, listing_id)
    if db_listing is None:
        raise HTTPException(
            status_code=404, detail=f"Listing ID {listing_id} not found"
        )

    return delete_listing(db, listing_id)
