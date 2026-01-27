# Module 6: Security: Authentication and Authorization
Welcome to the sixth module of the FastAPI tutorial! 
This module focuses on security aspects of FastAPI, including authentication and authorization.

## Getting Started
1. **Clone the repository**
    ```bash
    git clone https://github.com/margitantal68/FASTAPI/tree/main/module6_security
    ```

1. **Go to the cloned app folder**
    ```bash
    cd module6_security
    ```

1. **Create a virtual environment:**
    ```bash
    python -m venv .venv
    ```
    
1. **Activate the virtual environment:**
    - On macOS/Linux:
    ```bash
    source .venv/bin/activate  
    ```
    - On Windows use `.venv\Scripts\activate`

1. **Install dependencies**
    - For Python **3.11**:
    ```bash
    pip install -r requirements.txt
    ```
    - For Python **3.14**:
    ```bash
    pip install -r requirements_py314.txt
    ```


## Practical exercises

### Part 1: DB-based Authentication

#### ✅ Exercise 1: Setup the User Model & Table
- Goal: Define and migrate the users table.
- Tasks:
    - Use SQLAlchemy to define a User model. Add fields: `username`, `fullname`, `email`, `hashed_password`.
    - Run `Base.metadata.create_all()` to create the table.

    - Test by querying the database directly.

#### ✅ Exercise 2: Register a User
- Goal: Implement a `POST /users/register` endpoint.
- Tasks:
    - Validate uniqueness of username and email.
    - Hash the password using bcrypt.
    - Return only public data (e.g., username, email).

    - Test using Postman or Swagger.

#### ✅ Exercise 3: Login and Verify Password
- Goal: Implement a `POST /users/login` endpoint.
- Tasks:
    - Verify if the provided password matches the hashed password.
    - Return a success message or a 401 error on failure.
    - Use plain DB authentication, no JWT yet.

### Part 2: JWT Token-Based Authorization

#### ✅ Exercise 4: Issue JWT Token on Login
- Goal: Securely issue JWT tokens on login.
- Tasks:
    - Modify login to return a JWT using sub: username.
    - Set a short expiry time for access tokens.
    - Return the token in a structured response.

    - Store the token on the client side (localStorage or in tests).

### ✅ Exercise 5: Protect Routes Using JWT
- Goal: Secure the `/users/` endpoint.
- Tasks:
    - Create a `get_current_user()` dependency.
    - Decode the token and retrieve the current user.
    - Use `Depends(get_current_user)` to protect the route.

    - Test with and without token headers.

### ✅ Exercise 6: Delete a User
- Goal: Add a secure delete endpoint.
- Tasks:
    - Use `DELETE /users/{id}`.
    - Only allow access if a valid token is provided.
    - Handle “user not found” with a 404.

    - Return a success or error message.



## Hints
1. **.env file:**
    Copy the `.env.example` file in the project directory:
    ```
    cp .env.example .env
    ```
    Set the `DB_USER`, `DB_PASS`, `DB_HOST`, `DB_PORT`, and `DB_NAME` environment variables in the `.env` file to your PostgreSQL credentials.

    ```
    DB_USER=your_db_user
    DB_PASS=your_db_password
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=fastapi_week6
    ```
2. **Create a simple FastAPI app with the following structure:**

    ```
    module6_security/
    ├── main.py
    ├── database.py
    ├── utils.py
    ├── config.py
    ├── models/
    │   ├── user.py
    └── routers/
        ├── users.py
        
    ```
3. **Read the environment variables in `config.py`:**

    ```python
    import os
    from dotenv import load_dotenv

    load_dotenv()

    # Read DB_USER and DB_PASS from environment variables
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASS = os.getenv("DB_PASS", "postgres")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "fastapi_week6")

    # JWT Configuration
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_secret_key")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30) 
    ACCESS_TOKEN_EXPIRE_MINUTES = int(ACCESS_TOKEN_EXPIRE_MINUTES) 

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


6. **Create the database connection (`database.py`):**
    ```python
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
    ```

7. **Create utility functions (`utils.py`):**
    ```python
    import os
    from config import JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
    from passlib.context import CryptContext
    from datetime import datetime, timedelta
    from jose import jwt

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return encoded_jwt

    def decode_access_token(token: str):
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.JWTError:
            return None    
    ```


8. **Create route for user registration (`routers/users.py`):**

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

9. **Create the main FastAPI app (`main.py`):**
    ```python
        from fastapi import FastAPI
        from routers import users

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


10. **Run the FastAPI app:**
    ```bash
    uvicorn main:app --reload
    ```

