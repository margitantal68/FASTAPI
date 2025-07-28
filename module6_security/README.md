# Module 6: Security: Authentication and Authorization
Welcome to the sixth module of the FastAPI tutorial! This module focuses on security aspects of FastAPI, including authentication and authorization.

## Getting Started
1. **Create a virtual environment:**
    ```bash
    python -m venv .venv
    ```
    
    **Activate the virtual environment:**
    - On macOS/Linux:
    ```bash

    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

1. **Install FastAPI and Uvicorn:**
    ```bash
    pip install fastapi uvicorn
    ```

## FastAPI App
1. **.env file:**
    Create a `.env` file in the root directory of your FastAPI app with the following content:
    ```plaintext
    DB_USER=postgres
    DB_PASS=postgres
1. **Create a simple FastAPI app with the following structure:**

    ```
    module6_security/
    ├── main.py
    ├── database.py
    ├── utils.py
    ├── models/
    │   ├── user.py
    └── routes/
        ├── users.py
    ```

2. **Create the database connection (`database.py`):**
    ```python
    import os

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, declarative_base, Session

    # Read DB_USER and DB_PASS from environment variables
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASS = os.getenv("DB_PASS", "postgres")
    print(f"DB_USER: {DB_USER}, DB_PASS: {DB_PASS}")

    SQLALCHEMY_DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@localhost/fastapi_week6'

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
    ```

3. **Create utility functions (`utils.py`):**
    ```python
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)
    ```

4. **Create Database model for users (`models/user.py`):**
    ```python
    from sqlalchemy import Column, Integer, String
    from sqlalchemy.orm  import declarative_base
    from database import Base
    from pydantic import BaseModel


    class User(Base):
        __tablename__ = "users"

        id = Column(Integer, primary_key=True, index=True)
        username = Column(String, unique=True, index=True)
        fullname = Column(String)
        email = Column(String, unique=True, index=True)
        hashed_password = Column(String)
    ```
5. **Create Pydantic models for user registration (`models/user.py`):**
    ```python
    class UserRequest(BaseModel):
        username: str
        fullname: str
        email: str
        password: str

    class UserResponse(BaseModel):
        username: str
        email: str 
    ```

6. **Create route for user registration (`routers/users.py`):**

    ```python
    from fastapi import APIRouter, HTTPException
    from models.user import User, UserRequest, UserResponse
    from fastapi import Depends
    from sqlalchemy.orm import Session
    from database import get_db
    from utils import hash_password 


    router = APIRouter()

    @router.post("/register", response_model=UserResponse)
    def create_user(user_req: UserRequest, db: Session = Depends(get_db)):
        print("Endpoint called")
        # Check if username exists
        existing_user = db.query(User).filter(User.username == user_req.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")
        print(f"Great! {user_req.username} is not taken")
        # Create and save user
        new_user = User(
            username=user_req.username,
            fullname=user_req.fullname,
            email=user_req.email,
            hashed_password=hash_password(user_req.password)
        )
        print(new_user)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        response = UserResponse(username=new_user.username, email=new_user.email)
        return response
    ```

7. **Create the main FastAPI app (`main.py`):**
    ```python
        import os

        from dotenv import load_dotenv
        load_dotenv()

        from fastapi import FastAPI
        from routers import users

        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from database import engine, Base
        from fastapi.middleware.cors import CORSMiddleware

        # # Create tables
        Base.metadata.create_all(bind=engine)

        app = FastAPI()

        # Allow requests from the frontend
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:5173"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        app.include_router(users.router, prefix="/users", tags=["Users"])

        @app.get("/")
        def read_root():
            return {"message": "Welcome to the FastAPI backend!"}
    ```


8. **Run the FastAPI app:**
    ```bash
    uvicorn main:app --reload
    ```

