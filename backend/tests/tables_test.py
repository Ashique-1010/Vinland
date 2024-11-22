from app.database.session import engine
from app.models.user import Base as UserBase
from app.models.post import Base as PostBase
from sqlalchemy import inspect

UserBase.metadata.create_all(bind=engine)
PostBase.metadata.create_all(bind=engine)

inspector = inspect(engine)
tables = inspector.get_table_names()

print("Tables in the database:", tables)