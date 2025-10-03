# backend/app/database.py (Corrected Version)

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL is None:
    raise Exception("FATAL ERROR: DATABASE_URL environment variable is not set.")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# --- THIS FUNCTION IS NOW IN THE CORRECT FILE ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()