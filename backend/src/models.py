# create a pydantic model for listing
from pydantic import BaseModel, Field


class CreateListing(BaseModel):
    name: str = Field(..., description="The name of the listing")
    description: str = Field(..., description="The description of the listing")
    beds: int = Field(..., description="The number of beds")
    bedrooms: int = Field(..., description="The number of bedrooms")
    mean_rating: float = Field(..., description="The mean rating of the listing")
    count_ratings: int = Field(..., description="The count of ratings")
    nightly_price: float = Field(..., description="The nightly price of the listing")


class Listing(CreateListing):
    id: int = Field(..., description="The ID of the listing")
