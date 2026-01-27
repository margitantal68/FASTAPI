# Module 6: Security: OAuth2 Authentication with GitHub
Welcome to the sixth module of the FastAPI tutorial! 

This module focuses on security aspects of FastAPI, including authentication and authorization.
This time we will also set up **Alembic** for database migrations.
We will add **OAuth2** authentication using GitHub as the provider.

## Getting Started
1. **Clone the repository**
    ```bash
    git clone https://github.com/margitantal68/FASTAPI/tree/main/module6_security_oauth2
    ```

1. **Go to the cloned app folder**
    ```bash
    cd module6_security_oauth2
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
    - For Python **3.14**:
    ```bash
    pip install -r requirements_py314.txt
    ```

## Alembic setup

### Initialize Alembic

    ```bash
    alembic init alembic
    ```

This creates:
    ```bash
    alembic/
    env.py
    script.py.mako
    versions/
    alembic.ini
    ```

### Your project structure

```bash
module06_security_oauth2/
│
├── .venv/
├── main.py
├── database.py
├── config.py
├── models/
│   └── user.py
│
├── alembic.ini
└── alembic/
    ├── env.py
    └── versions/
```

### Configure Alembic

1. **Edit `alembic.ini` to set the SQLAlchemy URL:**
   Find the line starting with `sqlalchemy.url` and set it to your database URL, for example:
   ```
   sqlalchemy.url = postgresql://postgres:postgres123!@localhost:5432/fastapi_week6
   ```
2. **Edit `alembic/env.py` to include your models' metadata:**
    ```python
    from logging.config import fileConfig
    from sqlalchemy import engine_from_config, pool
    from alembic import context

    from database import Base
    from models import user  # ensures User model is registered

    config = context.config

    if config.config_file_name is not None:
        fileConfig(config.config_file_name)

    target_metadata = Base.metadata
    ```
3. **Migration flow"

    Since your DB already has users table + data:
    ```bash
    alembic revision --autogenerate -m "baseline"
    alembic stamp head
    ```
    Then:
    ```bash
    alembic revision --autogenerate -m "add github oauth fields"
    alembic upgrade head
    ```
## GitHub OAuth2 Setup
To enable OAuth2 authentication with GitHub, you need to register your application on GitHub to obtain a Client ID and Client Secret.

### GitHub app registration
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

### Configure Environment Variables
1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```
2. **Edit the `.env` file:**
   - Set your client ID and secret in the `.env` file:
   ```plaintext
   GITHUB_CLIENT_ID=your_client_id
   GITHUB_CLIENT_SECRET=your_client_secret
   ```

## Practical exercises

### Part 3: GitHub OAuth2 Authentication

Implement the following exercises in `routers/auth.py`

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
1. **Create a copy of the module06_security; add `auth.py` to the `routers` directory:**

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
        |── auth.py
    ```

2. `.env` file:

    Set the `CLIENT_ID` and `CLIENT_SECRET` for OAuth2 authentication.

3. **Modify `config.py` in order to read GITHUB_CLIENT_ID and GITHUB_CLIENT_SECRET:**

    ```python
    
    # OAuth Configuration
    GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
    GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")

    GITHUB_REDIRECT_URI = "http://localhost:8000/auth/github/callback"
    FRONTEND_REDIRECT_URL = "http://localhost:5173/oauth/callback"
    ```
 
4. **Modify the model for users (`models/user.py`):**
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
            # New fields for GitHub authentication
        github_id = Column(String, unique=True, index=True, nullable=True)
        avatar_url = Column(String, nullable=True)
        auth_provider = Column(String, default="local")  # e.g., 'local' or 'github'
    ```

5. **Create `routers/auth.py`: implement GitHub OAuth2 routes:**
    
    ```python
    import httpx
    from fastapi import APIRouter, HTTPException, Request, Depends
    from starlette.responses import RedirectResponse
    from jose import jwt

    from sqlalchemy.orm import Session
    from database import get_db  # Your DB session dependency
    from models.user import User  

    from config import (
        GITHUB_CLIENT_ID,
        GITHUB_CLIENT_SECRET,
        GITHUB_REDIRECT_URI,
        JWT_SECRET_KEY,
        JWT_ALGORITHM,
        FRONTEND_REDIRECT_URL,
    )

    router = APIRouter()

    @router.get("/github/login")
    def login_with_github():
        print(GITHUB_CLIENT_ID, GITHUB_CLIENT_SECRET)
        if not GITHUB_CLIENT_ID or not GITHUB_CLIENT_SECRET:
            raise HTTPException(status_code=500, detail="GitHub OAuth credentials are not set")
        else:
            print("GitHub OAuth credentials are set")
            
        github_auth_url = (
            f"https://github.com/login/oauth/authorize"
            f"?client_id={GITHUB_CLIENT_ID}"
            f"&redirect_uri={GITHUB_REDIRECT_URI}"
            f"&scope=read:user user:email"
        )
        return RedirectResponse(github_auth_url)


    @router.get("/github/callback")
    async def github_callback(request: Request, db: Session = Depends(get_db)):
        print("GitHub callback received")
        code = request.query_params.get("code")
        print(f"Received code: {code}")

        if not code:
            raise HTTPException(status_code=400, detail="Missing GitHub code")

        # Step 1: Exchange code for access token
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                "https://github.com/login/oauth/access_token",
                headers={"Accept": "application/json"},
                data={
                    "client_id": GITHUB_CLIENT_ID,
                    "client_secret": GITHUB_CLIENT_SECRET,
                    "code": code,
                    "redirect_uri": GITHUB_REDIRECT_URI,
                },
            )
            token_data = token_response.json()
            access_token = token_data.get("access_token")
            print(f"Access token: {access_token}")
            if not access_token:
                raise HTTPException(status_code=400, detail="GitHub token exchange failed")

            # Step 2: Fetch GitHub user profile
            user_response = await client.get(
                "https://api.github.com/user",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            user_data = user_response.json()
            print(f"User data: {user_data}")

            # Step 3: Get primary email
            email_response = await client.get(
                "https://api.github.com/user/emails",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            email_data = email_response.json()
            primary_email = next((e["email"] for e in email_data if e.get("primary") and e.get("verified")), None)
            if not primary_email:
                raise HTTPException(status_code=400, detail="No verified primary email found")

            # Step 4: Create or get user
            user = get_or_create_user(
                db=db,
                github_id=str(user_data["id"]),
                email=primary_email,
                fullname=user_data.get("name"),
                avatar_url=user_data.get("avatar_url"),
            )
            print(f"Store user's data in a local db: {user}")

            # Step 5: Generate JWT
            jwt_payload = {"sub": user.username, "email": user.email}
            token = jwt.encode(jwt_payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

            # Step 6: Redirect to frontend with token
            return RedirectResponse(f"{FRONTEND_REDIRECT_URL}?token={token}")

    def get_or_create_user(
        db: Session,
        github_id: str,
        email: str,
        fullname: str = None,
        avatar_url: str = None,
    ):
        # 1. Try to find user by GitHub ID
        user = db.query(User).filter(User.github_id == github_id).first()

        # 2. If not found, try to find user by email (account linking)
        if not user and email:
            user = db.query(User).filter(User.email == email).first()
            if user:
                # Link GitHub to existing user
                user.github_id = github_id
                user.avatar_url = avatar_url
                user.auth_provider = "github"
                db.commit()
                db.refresh(user)

        # 3. If still not found, create new user
        if not user:
            user = User(
                username=email.split("@")[0],  # You can refine this logic
                fullname=fullname,
                email=email,
                github_id=github_id,
                avatar_url=avatar_url,
                auth_provider="github",
                hashed_password=None  # GitHub users don’t have local passwords
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        return user

    ```

6. **Modify `main.py`: include auth router:**
    
    ```python
    app.include_router(users.router, prefix="/users", tags=["Users"])
    app.include_router(auth.router, prefix="/auth", tags=["Auth"])
    ```


7. **Run the FastAPI app:**
    ```bash
    uvicorn main:app --reload
    ```

