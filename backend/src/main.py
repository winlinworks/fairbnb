import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Query
from typing import Optional

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("startup: triggered")
    yield
    logger.info("shutdown: triggered")


app = FastAPI(lifespan=lifespan)


@app.get("/")
def hello():
    return {"Hello": "World"}

# write FastAPI endpoint to get listing record for ID
# example: GET /listing?id=1
# response: {"id": 1, "name": "Listing 1", "description": "Description of listing 1"}
# if ID does not exist, return 404 status code
# if ID is not provided, return 400 status code

# Mock database
listings = {
    1: {
        "id": 1,
        "name": "Listing 1",
        "description": "Description of listing 1",
        "beds": 2,
        "bedrooms": 2,
        "mean_rating": 4.5,
        "count_ratings": 100
    },
    2: {
        "id": 2,
        "name": "Listing 2",
        "description": "Description of listing 2"
        "beds": 3,
        "bedrooms": 3,
        "mean_rating": 4.0,
        "count_ratings": 50
    },
    # Add more listings as needed
}

@app.get("/listing")
def get_listing(id: Optional[int] = Query(None, description="The ID of the listing to retrieve")):
    """
    Get listing record for a given ID.

    Args:
        id (Optional[int]): The ID of the listing to retrieve.

    Returns:
        dict: The listing record if found.

    Raises:
        HTTPException: If the ID is not provided (400) or the listing is not found (404).
    """
    # Check if ID is provided
    if id is None:
        raise HTTPException(status_code=400, detail="ID is required")
    
    # TODO(winlin): Replace this with a database query
    # Get listing record for the given ID
    listing = listings.get(id)

    # Check if listing is found
    if listing is None:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    return listing