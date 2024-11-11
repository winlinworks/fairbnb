from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


# Pydantic model for listings
class ListingBase(BaseModel):
    name: str = Field(..., description="Name of listing")
    tagline: str = Field(..., description="Tagline of listing")
    location: str = Field(..., description="City and state of listing")
    image: str = Field(..., description="URL of listing image")
    price: float = Field(..., description="Nightly price of listing")

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v):
        if v.strip() == "":
            msg = "Listing name must not be an empty string"
            raise ValueError(msg)
        return v


class ListingCreate(ListingBase):
    pass


class ListingRead(ListingBase):
    id: int = Field(..., description="The ID of the listing")
    owner_id: int = Field(..., description="The ID of the owner")

    model_config = ConfigDict(from_attributes=True)


# Pydantic model for users
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


class UserRead(UserBase):
    id: int | None = Field(..., description="The ID of the user")
    is_active: bool = Field(..., description="The active status of the user")
    listings: list[ListingRead] = []

    model_config = ConfigDict(from_attributes=True)
