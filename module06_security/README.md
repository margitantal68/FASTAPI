# Module 6: Security: Authentication and Authorization
Welcome to the sixth module of the FastAPI tutorial! This module focuses on security aspects of FastAPI, including authentication and authorization.

**It is recommended to use Python 3.11 for this module.**
1. List your installed Python versions
- On MacOS/Linux terminal run:
    ```bash
    which -a python
    ```
- On Windows Command Prompt run:
    ```bash
    where python
    ```
2. Install Python 3.11 if not already installed
3. Create a virtual environment with Python 3.11
    ```bash
    python3.11 -m venv .venv
    ```
4. Activate the virtual environment
    - On macOS/Linux:
    ```bash
    source .venv/bin/activate  
    ```
    - On Windows use `.venv\Scripts\activate`

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

    ```bash
    pip install -r requirements.txt
    ```

## GitHub app registration
✅ Step-by-Step: Register an OAuth App on GitHub
1. Go to GitHub Developer Settings
Open your browser and go to:
https://github.com/settings/developers

2. Choose "OAuth Apps"
On the left-hand sidebar, under "Developer settings", click on "OAuth Apps".

3. Click "New OAuth App"
You'll see a list (if any exist) and a button to "New OAuth App". Click it.

4. Fill Out the OAuth Application Form
Here’s what each field means:
- Field	Description
Application name	Name of your app (e.g., MyCoolApp)
Homepage URL	`http://localhost:5173`
- Authorization callback URL	`http://localhost:8000/auth/github/callback`
- Application description (optional)	Short description of your app

5. Click "Register application"
🎉 After Registration
Once registered, GitHub will give you:
- `Client ID` – Public identifier of your app
- `Client Secret` – Keep this secret! Used to authenticate your app

You’ll use these values when implementing OAuth in your app.




## Configure Environment Variables
1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```
2. **Edit the `.env` file:**
   - Set your database user and password in the `.env` file:
   ```plaintext
   DB_USER=your_db_user
   DB_PASS=your_db_password 
   GITHUB_CLIENT_ID=your_client_id
   GITHUB_CLIENT_SECRET=your_client_secret
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


### Part 3: GitHub OAuth2 Authentication

#### ✅ Exercise 7: Implement GitHub Login Flow
- Goal: Add `/auth/github/login` and redirect to **GitHub**.
- Tasks:
    - Redirect users to GitHub OAuth consent screen.
    - Use environment variables for `GITHUB_CLIENT_ID` and `SECRET`.

    - Use your GitHub OAuth App credentials.

#### ✅ Exercise 8: GitHub Callback & User Creation
- Goal: Handle GitHub OAuth callback.
- Tasks:
    - Exchange code for access_token.
    - Fetch user profile and verified email.
    - Create new user or link to an existing one.
    - Add GitHub fields to the User model: `github_id`, `avatar_url`, `auth_provider`.

    - Log the user in automatically with a JWT.

#### ✅ Exercise 9: Redirect with Token
- Goal: Issue JWT and redirect to frontend.
- Tasks:
    - On successful OAuth, create a JWT.
    - Redirect to frontend with ?token=... in the URL.
    - Allow frontend to decode and store the token.
    
    - Verify the decoded token in the frontend.



## Hints
1. **.env file:**
    Copy the `.env.example` file in the project directory:
    ```
    cp .env.example .env
    ```
    Set the `DB_USER` and `DB_PASS` environment variables in the `.env` file to your PostgreSQL credentials.
    Set the `CLIENT_ID` and `CLIENT_SECRET` for OAuth2 authentication.
    ```
    DB_USER=your_db_user
    DB_PASS=your_db_password
    CLIENT_ID=your_client_id
    CLIENT_SECRET=your_client_secret
    ```
1. **Create a simple FastAPI app with the following structure:**

    ```
    module6_security/
    ├── main.py
    ├── database.py
    ├── utils.py
    ├── models/
    │   ├── user.py
    └── routers/
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

