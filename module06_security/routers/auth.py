import os 
import httpx
from fastapi import APIRouter, HTTPException, Request, Depends
from starlette.responses import RedirectResponse
from jose import jwt

from sqlalchemy.orm import Session
from database import get_db  # Your DB session dependency
from models.user import User  


GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
GITHUB_REDIRECT_URI = "http://localhost:8000/auth/github/callback"
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
FRONTEND_REDIRECT_URL = "http://localhost:5173/oauth/callback"

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


@router.get("/home")
def auth_home():
    return {"message": "Welcome to the authentication home page!"}