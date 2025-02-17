from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


# Pydantic model for listings
class PropertyBase(BaseModel):
    name: str = Field(..., description="Name of property")
    tagline: str = Field(..., description="Tagline of property")
    category: str = Field(..., description="Category of property")
    image: str = Field(..., description="URL of property image")
    location: str = Field(..., description="Address of property")
    description: str = Field(..., description="Description of property")
    guests: int = Field(..., description="Number of guests property can accommodate")
    bedrooms: int = Field(..., description="Number of bedrooms in property")
    beds: int = Field(..., description="Number of beds in property")
    baths: int = Field(..., description="Number of bathrooms in property")
    amenities: list[str] = Field(..., description="List of amenities in property")
    price: float = Field(..., description="Nightly price of property")
    owner_id: int = Field(..., description="ID of property owner")

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v):
        if v.strip() == "":
            msg = "Property name must not be an empty string"
            raise ValueError(msg)
        return v


class PropertyCreate(PropertyBase):
    pass


class PropertyRead(PropertyBase):
    id: int = Field(..., description="The ID of the property")
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
    properties: list[PropertyRead] = []

    model_config = ConfigDict(from_attributes=True)
