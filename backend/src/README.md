## Data Models

### Profile
The `Profile` model stores additional information about users.

- **user**: The user this profile belongs to. User is nested as a separate object within Profile to keep authentication/authorization clean as profile fields get added.

### Property
The `Property` model stores information about properties.

- **name**: Name of the property.
- **tagline**: Tagline or short description of the property.
- **location**: Location of the property.
- **image**: URL of the property's image.
- **price**: Price of the property.
- **owner**: The owner of the property.
