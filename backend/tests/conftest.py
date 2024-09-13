import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base

# URL for sqlite in memory database
TEST_DB_URL = "sqlite:///test_db.sqlite"

# Remove sqlite db file if it exists
if os.path.exists("test_db.sqlite"):
    os.remove("test_db.sqlite")

# Create an engine
engine = create_engine(TEST_DB_URL)


# Override the get_db dependency with get_test_db
def get_test_db():
    # If the backend is not using SQLite, raise an error
    if engine.url.get_backend_name() != "sqlite":
        error_msg = "Use SQLite backend to run tests"
        raise RuntimeError(error_msg)

    # Create a DB session factory method
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create all tables
    Base.metadata.create_all(bind=engine)

    try:
        # Create a session and yield it
        session_local = session()
        yield session_local
    finally:
        session_local.close()
