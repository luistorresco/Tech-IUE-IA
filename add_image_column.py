import os
import sqlalchemy
from sqlalchemy import create_engine, text

# Try to get URL from env or default to localhost
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/terrawish")

def add_column():
    print(f"Connecting to {DATABASE_URL}...")
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            # Check if column exists
            print("Checking if column exists...")
            result = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='soil_types' AND column_name='image_url'"))
            if result.fetchone():
                print("Column 'image_url' already exists in 'soil_types'.")
            else:
                print("Adding column 'image_url' to 'soil_types'...")
                conn.execute(text("ALTER TABLE soil_types ADD COLUMN image_url VARCHAR"))
                conn.commit()
                print("Column added successfully.")
    except Exception as e:
        print(f"Error: {e}")
        print("Please check your database connection or Docker status.")

if __name__ == "__main__":
    add_column()
