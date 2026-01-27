from fastapi import FastAPI
from fastapi import HTTPException, Depends

app = FastAPI()

# 0. BASIC example
def reverse_string(s: str) -> str:
    return s[::-1]
    
# 1. TEST example
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# 2. UNIT testing
fake_db = {
    1: {"id": 1, "name": "Alice"},
    2: {"id": 2, "name": "Bob"}
}

def get_user_from_db(user_id: int):
    return fake_db.get(user_id)

@app.get("/users/{user_id}")
def read_user(user_id: int, get_user=Depends(get_user_from_db)):
    user = get_user
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 3. INTEGRATION testing

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "sqlite:///./app.db"  # real DB for dev, overridden in tests

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

## --- Model ---
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

## Create tables
Base.metadata.create_all(bind=engine)

## --- Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

## --- App ---
@app.get("/users/integration/{user_id}")
def read_user2(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "name": user.name}

