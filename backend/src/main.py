import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from src.models import CreateListing, Listing

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
        "count_ratings": 100,
        "nightly_price": 100,
    },
    2: {
        "id": 2,
        "name": "Listing 2",
        "description": "Description of listing 2",
        "beds": 3,
        "bedrooms": 3,
        "mean_rating": 4.0,
        "count_ratings": 50,
        "nightly_price": 150,
    },
    # Add more listings as needed
}


@app.post("/listings", response_model=Listing)
async def create_listing(listing: CreateListing):
    # Check if the listing exists
    # TODO: Replace with database logic
    if listing_exists():
        raise HTTPException(
            status_code=400, detail="Listing with this ID already exists"
        )

    listings[listing.id] = listing.model_dump()
    return listing


def listing_exists():
    """
    Check if a listing exists in the database given metadata.
    """
    return False


@app.get("/listings", response_model=list[Listing])
async def get_listings():
    # Return all listings
    # TODO: Replace with database logic
    return [Listing(**listing) for listing in listings.values()]


@app.get("/listings/{listing_id}", response_model=Listing)
async def get_listing(listing_id: int):
    # Check if the listing exists
    # TODO: Replace with database logic
    listing = listings.get(listing_id)

    if listing is None:
        raise HTTPException(status_code=404, detail=f"Listing {listing_id=} not found")

    return listing


@app.put("/listings/{listing_id}", response_model=Listing)
async def update_listing(listing_id: int, listing: Listing):
    # Check if the listing exists
    # TODO: Replace with database logic
    if listing_id not in listings:
        raise HTTPException(status_code=404, detail=f"Listing {listing_id=} not found")

    # Update the listing in the mock database
    listings[listing_id] = listing.model_dump()
    return listing


@app.delete("/listings/{listing_id}")
async def delete_listing(listing_id: int):
    # Check if the listing exists
    # TODO: Replace with database logic
    listing = listings.pop(listing_id, None)

    # If the listing does not exist, raise an error
    if listing is None:
        raise HTTPException(status_code=404, detail=f"Listing {listing_id=} not found")

    return {"ok": True}
