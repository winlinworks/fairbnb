from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

# Get the environment variables for the database connection
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASS = os.getenv("POSTGRES_PASS")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

# Define the PostgreSQL URL
DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASS}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

breakpoint()
# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

breakpoint()

# Define the base class for declarative models
Base = declarative_base()


# Define the Listing model
class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    beds = Column(Integer, nullable=False)
    bedrooms = Column(Integer, nullable=False)
    mean_rating = Column(Float, nullable=False)
    count_ratings = Column(Integer, nullable=False)
    nightly_price = Column(Float, nullable=False)


# Create the tables in the database
Base.metadata.create_all(engine)

breakpoint()

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

# Example: Add a new listing
new_listing = Listing(
    name="Cozy Cottage",
    description="A cozy cottage in the countryside",
    beds=2,
    bedrooms=1,
    mean_rating=4.5,
    count_ratings=10,
    nightly_price=120.0,
)

session.add(new_listing)
session.commit()
session.close()
