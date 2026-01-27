import os
from config import DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session


SQLALCHEMY_DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base class
Base = declarative_base()

# Dependency for FastAPI routes
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

