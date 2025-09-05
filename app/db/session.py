from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "DATABASE_URL=postgresql://postgres:admin123@localhost:5432/mitra_db")  # Replace with your DB URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency function for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
