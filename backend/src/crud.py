from src.fairbnb.models import Property, User


class DBClient:
    """
    Generic database client class to handle CRUD operations. Extend this class to create model specific database clients (e.g., User, Property, etc.).
    """

    def __init__(self, model):
        self.model = model

    def create(self, **fields):
        """
        Create an object in the database.

        Args:
            **fields: The fields to set on the object.

        Returns:
            The ID of the created object.
        """
        obj = self.model.objects.create(**fields)
        return obj.id

    def read(self, **filters):
        """
        Read an object from the database.

        Args:
            **filters: The fields to filter by.

        Returns:
            The object if found, None otherwise.
        """
        return self.model.objects.filter(**filters).first()

    def update(self, id: int, **fields):
        """
        Update an object in the database.

        Args:
            id (int): The ID of the object to update.
            **fields: The fields to update and their new values.

        Returns:
            The updated object.
        """
        obj = self.read(id=id)
        for key, value in fields.items():
            setattr(obj, key, value)
        obj.save()
        return obj

    def delete(self, id: int):
        """
        Delete an object from the database.

        Args:
            id (int): The ID of the object to delete.
        """
        obj = self.read(id=id)
        obj.delete()

    def check_record_exists(self, **filters) -> bool:
        """
        Check if a record exists in the database.

        Args:
            field (str): The field to check.
            value (str): The value to check.
        """
        return self.read(**filters) is not None


# User DB client
class UserDBClient(DBClient):
    """
    User database client to handle CRUD operations.
    """

    def __init__(self):
        super().__init__(User)


# Property DB client
class PropertyDBClient(DBClient):
    """
    Property database client to handle CRUD operations.
    """

    def __init__(self):
        super().__init__(Property)
