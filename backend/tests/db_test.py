from app.database.session import engine
from sqlalchemy import text


try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print(result.scalar())
        print("Database connection Successfull..!")

except Exception as e:
    print(e)
    print("Database connection Failed!")
        
