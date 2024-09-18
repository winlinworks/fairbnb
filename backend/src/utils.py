from typing import Any

from pydantic import BaseModel


def update_record(db_record: Any, new_record_data: BaseModel):
    """
    Args:
        db_record (Any): DB record to update, could be any SQLAlchemy model such as User, Listing, etc.
        new_record_data (BaseModel): The new data to update the record with
    """
    new_record_data = new_record_data.model_dump(exclude_unset=True)
    for key, value in new_record_data.items():
        setattr(db_record, key, value)
