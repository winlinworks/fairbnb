import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base

# URL for sqlite in memory database
TEST_DB_URL = "sqlite:///test_db.sqlite"

# Remove sqlite db file if it exists
if os.path.exists("test_db.sqlite"):
    os.remove("test_db.sqlite")

# Create an engine for test DV
test_engine = create_engine(TEST_DB_URL)

# Create all tables
Base.metadata.create_all(bind=test_engine)

# Create a test DB session factory method
TestDBSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


# Override the get_db dependency with get_test_db
def get_test_db():
    # If the backend is not using SQLite, raise an error
    if test_engine.url.get_backend_name() != "sqlite":
        error_msg = "Use SQLite backend to run tests"
        raise RuntimeError(error_msg)

    try:
        # Create a session and yield it
        session = TestDBSession()
        yield session
    finally:
        session.close()
