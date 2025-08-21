# Module 8: Advanced API Design

## Getting Started
1. **Create a virtual environment:**
    ```bash
    python -m venv .venv
    ```
    
    **Activate the virtual environment:**
    - On macOS/Linux:
    ```bash
    source .venv/bin/activate  
    ```
    - On Windows use `.venv\Scripts\activate`
    

## Install Dependencies
   ```bash
   pip install fastapi, uvicorn, pytest, httpx, sqlalchemy
   ```      


## Practical Exercises: Testing FastAPI backend

### ✅ Exercise 1 – Add an Example Test for the Root Endpoint

In `main.py` it is given a simple endpoint:

```python
from fastapi import FastAPI
from fastapi import HTTPException, Depends

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
```

Write a simple test in `tests/test_main.py` that:
- Calls GET /.
- Verifies that the status code is 200.
- Verifies that the response body equals {"message": "Hello, FastAPI!"}.


### ✅ Exercise 2 – Write a Unit Test for a New Mocked User

In the `main.py` it is given a user endpoint `/users/{user_id}` that depend on `get_user_from_db`.

```python

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

```

Write two tests in `tests/unit/test_users_unit.py`.
- First test:
    - Calls `GET /users/1.`
    - Confirms that the mocked user (Mocked Alice) is returned.
- Second test:
    - Calls `GET /users/999`.
    - Confirms that it returns 404 with `{"detail": "User not found"}`.

### ✅ Exercise 3 – Add Integration Test with Test Database

- In the `main.py` it is given an integration endpoint at `/users/integration/{user_id}` that queries a real database.

```python
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

```

Write two integration tests in `tests/integration/test_users_integration.py`.

- First test:
    - Call `GET /users/integration/1` after inserting a test user (Integration Alice) and confirm the correct user is returned.
- Second test:
    - Call `GET /users/integration/999` and confirm that a 404 with `{"detail": "User not found"}` is returned.