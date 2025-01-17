## Data Models

Data model is based on [mock interfaces](https://github.com/winlinworks/fairbnb/blob/main/frontend/src/mock/types/types.ts) plus additional fields.

See here for [ERD].

### User
The `User` table stores authentication/authorization data.

- **id**: UUID of user.
- **username**: Username of user.
- **email**: Email of user.
- **hashed_password**: Hashed password of user.


### Profile
The `Profile` table stores additional information about users.

- **user_id**: UUID of user associated with profile.
- **first_name**: First name of user
- **last_name**: Last name of user
- **profile_image_url**: URL of user profile image
- **created_at**: Datetime when profile was created
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
- **price**: Price of property.
- **guests**: Maximum number of guests allowed to stay at property.
- **bedrooms**: Number of bedrooms at property.
- **beds**: Number of beds at property.
- **baths**: Number of bathrooms at property.
- **amenities**: List of amenities at property.
- **owner_id**: User ID of owner of property.
