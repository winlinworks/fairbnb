from src.db import engine
from src.models import Base

# delete all tables
Base.metadata.drop_all(bind=engine)

# create all tables
Base.metadata.create_all(bind=engine)
