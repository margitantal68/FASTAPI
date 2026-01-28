import logging

from fastapi import Depends, HTTPException, APIRouter, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.orm import Session

from models.user import (
    User,
    UserRequest,
    UserResponse,
    UserLoginRequest,
    UserLoginResponse,
    ResponseMessage
)

from database import get_db
from utils import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token
)

logging.basicConfig(level=logging.INFO)

router = APIRouter()

# --- Bearer scheme for Swagger ---
bearer_scheme = HTTPBearer()


# --- Auth helper ---
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
    db: Session = Depends(get_db)
):
    token = credentials.credentials  # Extract JWT token string

    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    logging.info(f"Token received: {token}")

    try:
        payload = decode_access_token(token)
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

    except Exception:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception

    return user


# --- Protected endpoint ---
@router.get("/", response_model=list[UserResponse])
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    users = db.query(User).all()
    return users


# --- Register ---
@router.post("/register", response_model=UserResponse)
def create_user(user_req: UserRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user_req.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(
        username=user_req.username,
        fullname=user_req.fullname,
        email=user_req.email,
        hashed_password=hash_password(user_req.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponse(
        username=new_user.username,
        email=new_user.email
    )


# --- Login ---
@router.post("/login", response_model=UserLoginResponse)
def login(user_req: UserLoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_req.username).first()

    if not user or not verify_password(user_req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token(data={"sub": user.username})

    return UserLoginResponse(
        message="Login successful",
        username=user.username,
        access_token=access_token
    )


# --- Delete user ---
@router.delete("/{id}", response_model=ResponseMessage)
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return ResponseMessage(message="User deleted successfully")

