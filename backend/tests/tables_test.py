from app.database.session import engine
from app.models.user import Base as UserBase
from app.models.post import Base as PostBase

UserBase.metadata.create_all(bind=engine)
PostBase.metadata.create_all(bind=engine)