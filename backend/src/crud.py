from sqlalchemy.orm import Session

from src.models import Listing, User
from src.schemas import ListingCreate, UserCreate


def create_user(db: Session, user: UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(
        email=user.email, username=user.username, hashed_password=fake_hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def read_user(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()


def read_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()


def read_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()


def create_listing(db: Session, listing: ListingCreate, user_id: int):
    db_listing = Listing(**listing.model_dump(), owner_id=user_id)
    db.add(db_listing)
    db.commit()
    db.refresh(db_listing)
    return db_listing


def read_listing(db: Session, listing_id: int) -> Listing:
    return db.query(Listing).filter(Listing.id == listing_id).first()


def read_listings(db: Session, skip: int = 0, limit: int = 100) -> list[Listing]:
    return db.query(Listing).offset(skip).limit(limit).all()
