import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db import get_engine
from src.main import app
from src.models import Base

# URL for test DB (sqlite in-memory)
TEST_DB_URL = "sqlite:///:memory:"

# Test DB engine
test_engine = create_engine(TEST_DB_URL)

# Create all tables in test DB
Base.metadata.create_all(bind=test_engine)


# Dependency to get test DB engine for overriding DB engine
def get_test_engine():
    return test_engine


# Override DB engine with test DB engine via FastAPI dependency injection
app.dependency_overrides[get_engine] = get_test_engine

# Create a test DB session factory for dependency injection within tests
TestDBSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def test_db():
    """
    Returns session for test DB for dependency injection in integration tests (e.g., creating users for listings)
    """
    return TestDBSession()
