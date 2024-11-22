from app.core.security import get_password_hash, verify_password

password = "testpass123"
hashed = get_password_hash(password)

assert verify_password(password, hashed) == True
"""
If no exceptions occur on running this above code,
password hashing is succesfull.
"""


print(f"Password: {password}")
print(f"Hashed Password: {hashed}")
print(f"Verification Result: {verify_password(password, hashed)}")