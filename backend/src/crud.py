from src.fairbnb.models import User

# TODO(winlinworks): Create a Django client class to handle database operations

# User CRUD ops


class DBClient:
    """
    Generic database client class to handle CRUD operations. Extend this class to create model specific database clients (e.g., User, Property, etc.).
    """

    def __init__(self, model):
        self.model = model

    def create(self, **kwargs):
        obj = self.model.objects.create(**kwargs)
        return obj.id

    def read(self, **kwargs):
        return self.model.objects.filter(**kwargs).first()

    def update(self, id: int, **kwargs):
        obj = self.read(id=id)
        for key, value in kwargs.items():
            setattr(obj, key, value)
        obj.save()
        return obj

    def delete(self, id: int):
        obj = self.read(id=id)
        obj.delete()

    def check_record_exists(self, field: str, value: str) -> bool:
        return self.read(**{field: value}) is not None


# User DB client
class UserDBClient(DBClient):
    """
    User database client to handle CRUD operations.
    """

    def __init__(self):
        super().__init__(User)


# # Property CRUD ops


# def create_listing(listing: PropertyCreate, user_id: int) -> Property:
#     db_listing = Property(**listing.model_dump(), owner_id=user_id)
#     db.add(db_listing)
#     db.commit()
#     db.refresh(db_listing)
#     return db_listing


# def read_listing(listing_id: int) -> Property:
#     return db.query(Property).filter(Property.id == listing_id).first()


# def read_listings(skip: int = 0, limit: int = 100) -> list[Property]:
#     return db.query(Property).offset(skip).limit(limit).all()


# def update_listing(
#     listing_id: int, new_listing_data: PropertyRead
# ) -> Property:
#     db_listing = read_listing(db, listing_id)

#     # Update listing fields
#     update_record(db_listing, new_listing_data)

#     # Save changes
#     db.add(db_listing)
#     db.commit()
#     db.refresh(db_listing)
#     return db_listing


# def delete_listing(listing_id: int):
#     db_listing = read_listing(db, listing_id)
#     db.delete(db_listing)
#     db.commit()
#     return {"message": "Property deleted", "listing_id": listing_id}
