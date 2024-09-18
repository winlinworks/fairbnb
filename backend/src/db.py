import os

from fastapi import Depends
from sqlalchemy import URL, Engine, create_engine
from sqlalchemy.orm import sessionmaker

# Get the environment variables for the database connection
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASS = os.getenv("POSTGRES_PASS")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")

# Define the PostgreSQL URL
DB_URL = URL.create(
    "postgresql+psycopg2",
    username=POSTGRES_USER,
    password=POSTGRES_PASS,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    database=POSTGRES_DB,
)

# DB engine
db_engine = create_engine(DB_URL)


# Dependency to get DB engine
def get_engine():
    return db_engine


# Dependency to get DB session from API endpoints
def get_db(engine: Engine = Depends(get_engine)):
    # Create DB session factory
    DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # noqa: N806

    # Create DB session and yield it
    session = DBSession()
    try:
        yield session
    finally:
        session.close()
