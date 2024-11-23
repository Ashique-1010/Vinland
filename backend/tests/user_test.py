from app.models import user, post
from app.database.session import SessionLocal
from app.services.auth import create_user, authenticate_user
from app.schemas.user import UserCreate

db = SessionLocal()
user_ = UserCreate(email="test5@test.com", username="testuser5", password="testpass5")

db_user = create_user(db, user_)

auth_user = authenticate_user(db, "test5@test.com", "testpass5")
assert auth_user is not None, "Authentication failed: User not found or incorrect password."
print("User authenticated successfully.")