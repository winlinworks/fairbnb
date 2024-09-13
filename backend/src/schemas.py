from pydantic import BaseModel, EmailStr, Field, field_validator


# Pydantic model for listings
class ListingBase(BaseModel):
    name: str = Field(..., description="The name of the listing")
    description: str = Field(..., description="The description of the listing")
    beds: int = Field(..., description="The number of beds")
    bedrooms: int = Field(..., description="The number of bedrooms")
    mean_rating: float = Field(..., description="The mean rating of the listing")
    count_ratings: int = Field(..., description="The count of ratings")
    nightly_price: float = Field(..., description="The nightly price of the listing")


class ListingCreate(ListingBase):
    pass


class Listing(ListingBase):
    id: int = Field(..., description="The ID of the listing")
    owner_id: int = Field(..., description="The ID of the owner")

    class Config:
        orm_mode = True


# Pydanitc model for users
class UserBase(BaseModel):
    username: str = Field(..., description="The username of the user")
    email: EmailStr = Field(..., description="The email of the user")

    @field_validator("email")
    @classmethod
    def email_must_not_be_empty(cls, v):
        if v.strip() == "":
            msg = "Email must not be an empty string"
            raise ValueError(msg)
        return v


class UserCreate(UserBase):
    password: str = Field(..., description="The password of the user")


class User(UserBase):
    id: int = Field(..., description="The ID of the user")
    is_active: bool = Field(..., description="The active status of the user")
    listings: list[Listing] = []

    class Config:
        orm_mode = True
