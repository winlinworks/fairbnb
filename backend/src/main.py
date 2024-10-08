import logging
import sys
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from src.crud import (
    create_listing,
    create_user,
    read_listings,
    read_user,
    read_user_by_email,
    read_users,
)
from src.db import SessionLocal
from src.schemas import Listing, ListingCreate, User, UserCreate

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


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=User)
def post_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = read_user_by_email(db, user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user)


@app.get("/users/", response_model=list[User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return read_users(db, skip, limit)


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = read_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/listings/", response_model=Listing)
def post_listing(user_id: int, listing: ListingCreate, db: Session = Depends(get_db)):
    return create_listing(db, listing, user_id)


@app.get("/listings/", response_model=list[Listing])
def get_listings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return read_listings(db, skip, limit)


@app.get("/listings/{listing_id}", response_model=Listing)
def get_listing(listing_id: int, db: Session = Depends(get_db)):
    db_listing = read_listings(db, listing_id)
    if db_listing is None:
        raise HTTPException(status_code=404, detail="Listing not found")
    return db_listing
