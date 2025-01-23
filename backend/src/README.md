## Data Models

Data model is based on [mock interfaces](https://github.com/winlinworks/fairbnb/blob/main/frontend/src/mock/types/types.ts) plus additional fields.

See here for [ERD].

### User
The `User` table stores authentication/authorization data.

- **id**: UUID of user.
- **first_name**: First name of user
- **last_name**: Last name of user
- **username**: Username of user.
- **email**: Email of user.
- **hashed_password**: Hashed password of user.
- **date_joined**: Datetime when profile was created


### Profile
The `Profile` table stores additional information about users.

- **user_id**: UUID of user associated with profile.
- **image**: URL of user profile image
- **updated_at**: Datetime when profile was last updated


### Property
The `Property` table stores information about properties.

- **id**: UUID of property
- **name**: Name of property.
- **tagline**: Tagline or short description of property.
- **category**: Category of property.
- **image**: URL of property's image.
- **location**: Location of property.
- **country**: Country where property is located.
- **description**: Description of property
- **price**: Nightly price to stay at property.
- **guests**: Maximum number of guests allowed to stay at property.
- **bedrooms**: Number of bedrooms at property.
- **beds**: Number of beds at property.
- **baths**: Number of bathrooms at property.
- **amenities**: List of amenities at property.
- **owner**: User ID of owner of property.
